#!/opt/homebrew/bin/python3
"""Owned Steam library from the signed-in client's package cache (appcache/packageinfo.bin = owned licences),
names from Valve's public app list, playtime from localconfig.vdf. Read-only, no credentials.
Writes owned.json (appid -> {name, playtime_min, pkgs}) next to this script."""
import os, sys, json, struct, re, urllib.request
HOME = os.path.expanduser('~')
HERE = os.path.dirname(os.path.abspath(__file__))
CANDIDATES = [os.path.join(HOME, 'Library/Application Support/CrossOver/Bottles/Steam/drive_c/Program Files (x86)/Steam'),
              os.path.join(HOME, '.wine-steam-11/drive_c/Program Files (x86)/Steam'),
              os.path.join(HOME, 'Library/Application Support/Steam')]

def parse_binary_kv(buf, pos, string_table=None):
    """Old-style binary KeyValues: returns (dict, newpos)."""
    out = {}
    while True:
        t = buf[pos]; pos += 1
        if t == 0x08 or t == 0x0B:  # end
            return out, pos
        # key
        if string_table is not None and t != 0x08:
            idx = struct.unpack_from('<I', buf, pos)[0]; pos += 4; key = string_table[idx]
        else:
            end = buf.index(b'\x00', pos); key = buf[pos:end].decode('utf-8', 'replace'); pos = end + 1
        if t == 0x00:
            val, pos = parse_binary_kv(buf, pos, string_table)
        elif t == 0x01:
            end = buf.index(b'\x00', pos); val = buf[pos:end].decode('utf-8', 'replace'); pos = end + 1
        elif t == 0x02:
            val = struct.unpack_from('<i', buf, pos)[0]; pos += 4
        elif t == 0x03:
            val = struct.unpack_from('<f', buf, pos)[0]; pos += 4
        elif t == 0x04 or t == 0x06:
            val = struct.unpack_from('<I', buf, pos)[0]; pos += 4
        elif t == 0x05:
            end = buf.index(b'\x00\x00', pos)
            while (end - pos) % 2: end = buf.index(b'\x00\x00', end + 1)
            val = buf[pos:end].decode('utf-16le', 'replace'); pos = end + 2
        elif t == 0x07 or t == 0x0A:
            val = struct.unpack_from('<Q', buf, pos)[0]; pos += 8
        else:
            raise ValueError(f'unknown kv type {t:#x} at {pos}')
        out[key] = val

def parse_packageinfo(path):
    buf = open(path, 'rb').read()
    magic = struct.unpack_from('<I', buf, 0)[0]
    pos = 8  # magic + universe
    ver = magic & 0xFF
    pkgs = {}
    while pos < len(buf):
        pid = struct.unpack_from('<I', buf, pos)[0]; pos += 4
        if pid == 0xFFFFFFFF: break
        pos += 20  # sha1
        pos += 4   # change number
        if ver >= 0x28:
            pos += 8  # pics token
        kv, pos = parse_binary_kv(buf, pos)
        pkgs[pid] = kv
    return ver, pkgs

owned = {}
src_used = None
for root in CANDIDATES:
    p = os.path.join(root, 'appcache/packageinfo.bin')
    if not os.path.exists(p): continue
    try:
        ver, pkgs = parse_packageinfo(p)
    except Exception as e:
        print('packageinfo parse failed', p, e); continue
    n = 0
    for pid, kv in pkgs.items():
        body = kv.get(str(pid), kv)
        appids = body.get('appids', {}) if isinstance(body, dict) else {}
        for _, aid in appids.items():
            owned.setdefault(int(aid), {'pkgs': []})['pkgs'].append(pid); n += 1
    print(f'{p.replace(HOME, "~")}: format v{ver:#x}, {len(pkgs)} packages, {n} app refs')
    src_used = src_used or p

print('distinct owned appids:', len(owned))

# names from the public app list (no key)
names = {}
try:
    req = urllib.request.Request('https://api.steampowered.com/ISteamApps/GetAppList/v2/', headers={'User-Agent': 'Mozilla/5.0'})
    data = json.load(urllib.request.urlopen(req, timeout=60))
    for a in data['applist']['apps']:
        names[int(a['appid'])] = a['name']
    print('public app list entries:', len(names))
except Exception as e:
    print('GetAppList failed:', e)
for aid, v in owned.items():
    v['name'] = names.get(aid, '')

# playtime from localconfig (any install)
try:
    import vdf
    for root in CANDIDATES:
        p = os.path.join(root, 'userdata/1130251896/config/localconfig.vdf')
        if not os.path.exists(p): continue
        lc = vdf.load(open(p, encoding='utf-8', errors='ignore'))
        def walk(d):
            if isinstance(d, dict):
                for k, v in d.items():
                    if k.lower() == 'apps' and isinstance(v, dict):
                        for aid, av in v.items():
                            if aid.isdigit() and isinstance(av, dict):
                                pt = int(av.get('Playtime', av.get('playtime', 0)) or 0)
                                if pt: owned.setdefault(int(aid), {'pkgs': [], 'name': names.get(int(aid), '')})['playtime_min'] = max(pt, owned.get(int(aid), {}).get('playtime_min', 0))
                    walk(v)
        walk(lc)
except Exception as e:
    print('localconfig playtime skipped:', e)

unnamed = sum(1 for v in owned.values() if not v.get('name'))
print('owned apps:', len(owned), '| unnamed (DLC/tools/removed):', unnamed, '| with playtime:', sum(1 for v in owned.values() if v.get('playtime_min')))
with open(os.path.join(HERE, 'owned.json'), 'w') as f:
    f.write(json.dumps({str(k): v for k, v in sorted(owned.items())}, indent=0))
top = sorted(owned.items(), key=lambda kv: -kv[1].get('playtime_min', 0))[:20]
for aid, v in top:
    print(f"  {aid:>8} {v.get('playtime_min',0):>7} min  {v.get('name','')[:60]}")
