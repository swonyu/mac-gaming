#!/opt/homebrew/bin/python3
"""Extract the owned Steam library from the signed-in clients' local caches (no credentials, read-only).
Sources: appcache/appinfo.vdf (names, type, oslist) from the Wine and native Steam installs,
userdata/<id>/config/localconfig.vdf (playtime per app), packageinfo.bin (owned packages -> appids) when parseable.
Writes library.json next to this script."""
import os, sys, json, re
HOME = os.path.expanduser('~')
WINE = os.path.join(HOME, '.wine-steam-11/drive_c/Program Files (x86)/Steam')
NATIVE = os.path.join(HOME, 'Library/Application Support/Steam')
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'library.json')
try:
    import vdf
except Exception as e:
    print('vdf lib missing:', e); sys.exit(1)

apps = {}
def add(aid, **kw):
    a = apps.setdefault(str(aid), {})
    for k, v in kw.items():
        if v not in (None, '', []): a[k] = v

# 1) appinfo.vdf from both installs
for root, tag in ((WINE, 'wine'), (NATIVE, 'native')):
    p = os.path.join(root, 'appcache/appinfo.vdf')
    if not os.path.exists(p): continue
    try:
        with open(p, 'rb') as f:
            data = vdf.appinfo.load(f) if hasattr(vdf, 'appinfo') else None
    except Exception as e:
        print('appinfo parse failed', tag, e); data = None
    if data is None:
        # fallback: scan for common blocks textually (names only)
        raw = open(p, 'rb').read()
        for m in re.finditer(rb'\x01name\x00([^\x00]{1,120})\x00', raw):
            pass
        continue
    n = 0
    for aid, a in data.items():
        c = (a.get('data') or a).get('appinfo', {}).get('common', {}) if isinstance(a, dict) else {}
        if not c: continue
        n += 1
        add(aid, name=c.get('name'), type=(c.get('type') or '').lower(), oslist=c.get('oslist', ''),
            controller=c.get('controller_support', ''), release=c.get('steam_release_date') or c.get('original_release_date'))
        apps[str(aid)].setdefault('src', []).append(tag)
    print(tag, 'appinfo apps with common block:', n)

# 2) localconfig playtime
for root, tag in ((WINE, 'wine'), (NATIVE, 'native')):
    p = os.path.join(root, 'userdata/1130251896/config/localconfig.vdf')
    if not os.path.exists(p): continue
    try:
        lc = vdf.load(open(p, encoding='utf-8', errors='ignore'))
    except Exception as e:
        print('localconfig parse failed', tag, e); continue
    # find the apps dict wherever it lives
    def walk(d, path=''):
        if isinstance(d, dict):
            for k, v in d.items():
                if k.lower() == 'apps' and isinstance(v, dict):
                    for aid, av in v.items():
                        if aid.isdigit() and isinstance(av, dict):
                            add(aid, playtime_min=int(av.get('Playtime', av.get('playtime', 0)) or 0), lastplayed=av.get('LastPlayed', av.get('lastplayed')))
                            apps[aid].setdefault('src', []).append(tag + ':localconfig')
                walk(v, path + '/' + k)
    walk(lc)

# 3) packageinfo.bin -> owned appids (best effort)
for root, tag in ((WINE, 'wine'), (NATIVE, 'native')):
    p = os.path.join(root, 'appcache/packageinfo.bin')
    if not os.path.exists(p): continue
    try:
        raw = open(p, 'rb').read()
        # binary VDF packages: each package block contains 'appids' dict with numeric keys; scan text tokens
        ids = set(int(x) for x in re.findall(rb'\x02(\d+)\x00', raw))
        print(tag, 'packageinfo numeric tokens:', len(ids))
    except Exception as e:
        print('packageinfo scan failed', tag, e)

games = {k: v for k, v in apps.items() if v.get('type') == 'game'}
print('total apps:', len(apps), '| type=game:', len(games), '| with playtime:', sum(1 for v in apps.values() if v.get('playtime_min')))
with open(OUT, 'w') as f:
    f.write(json.dumps(apps, indent=0, sort_keys=True))
print('wrote', OUT)
top = sorted(games.items(), key=lambda kv: -kv[1].get('playtime_min', 0))[:15]
for aid, v in top:
    print(f"  {aid:>8} {v.get('playtime_min',0):>7} min  {v.get('oslist',''):<22} {v.get('name')}")
