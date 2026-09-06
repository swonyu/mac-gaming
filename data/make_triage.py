#!/opt/homebrew/bin/python3
"""Build ~/mac-gaming/library-triage.md from local data: names.json (store API), owned.json (playtime),
awacy.json (anti-cheat), gfn.json (GeForce NOW), optional cx_ratings.json (CrossOver verdicts, hand-filled from research)
and optional results.json (our own test results). Zero LLM. Re-run any time."""
import json as J, os, re, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, '..', 'library-triage.md')
def load(n, default):
    p = os.path.join(HERE, n)
    return J.load(open(p)) if os.path.exists(p) else default
names = load('names.json', {}); owned = load('owned.json', {}); awacy = load('awacy.json', []); gfn = load('gfn.json', [])
cx = load('cx_ratings.json', {}); results = load('results.json', {})
by_steam = {(g.get('storeIds') or {}).get('steam'): g for g in awacy if (g.get('storeIds') or {}).get('steam')}
by_name = {g['name'].lower(): g for g in awacy}
gfn_ids = {m.group(1) for g in gfn for m in [re.search(r'/app/(\d+)', g.get('steamUrl') or '')] if m}
KERNEL = {'Easy Anti-Cheat', 'BattlEye', 'nProtect GameGuard', 'XIGNCODE3', 'Vanguard', 'Ricochet', 'EA anticheat', 'FACEIT',
          'Anti-Cheat Expert', 'Nexon Game Security', 'Arkos', 'X-Trap', 'PunkBuster', 'NetEase Game Security', 'mhyprot2', 'Denuvo Anti-Cheat'}
# Steam's store API tags these as type=game but they aren't things to "get working" — Lepton is Valve's own
# Android compat layer (not a Windows app at all), the rest are utilities/benchmarks with no gameplay.
NOT_A_GAME = {'3029110', '1278480', '229950', '464170', '524390', '1840', '250820', '613220'}
# CrossOver 26 supported anti-cheat titles (filled from research; appid -> note)
cx_ac_ok = {k: v for k, v in cx.items() if v.get('anticheat_supported')}
rows = []
for aid, v in names.items():
    n = v.get('name') or f'appid {aid}'; typ = v.get('type') or '?'; p = v.get('platforms') or {}
    ac = by_steam.get(aid) or by_name.get(n.lower()); acs = ac.get('anticheats', []) if ac else []
    kern = [a for a in acs if a in KERNEL]
    pt = owned.get(aid, {}).get('playtime_min', 0)
    r = cx.get(aid, {}); res = results.get(aid, {})
    if typ in ('dlc', 'music', 'video', 'application', 'tool') or typ not in ('game', 'demo') or aid in NOT_A_GAME:
        bucket = 'Tools / DLC / non-game'
    elif p.get('mac'):
        bucket = 'Native macOS'
    elif res.get('status') == 'works':
        bucket = 'Confirmed working here'
    elif kern and aid not in cx_ac_ok and not res.get('status') == 'works':
        bucket = 'Kernel anti-cheat (blocked online)'
    elif r.get('rating') in ('Unplayable', 'Does not run', 'Broken'):
        bucket = 'Known broken'
    elif r.get('tweaks'):
        bucket = 'Works with tweaks'
    elif r.get('rating') in ('Runs great', 'Runs well', 'Runs') or res.get('status') == 'works':
        bucket = 'Should work well'
    else:
        bucket = 'Unknown / untested'
    rows.append(dict(bucket=bucket, pt=pt, aid=aid, name=n, ac=', '.join(acs) or '-', gfn='yes' if aid in gfn_ids else '-',
                     rating=r.get('rating', '-'), renderer=r.get('renderer', '-'), note=r.get('note', '') or res.get('note', ''), mac='yes' if p.get('mac') else '-'))
order = ['Confirmed working here', 'Native macOS', 'Should work well', 'Works with tweaks', 'Unknown / untested', 'Known broken', 'Kernel anti-cheat (blocked online)', 'Tools / DLC / non-game']
rows.sort(key=lambda r: (order.index(r['bucket']), -r['pt'], r['name'].lower()))
games = [r for r in rows if r['bucket'] != 'Tools / DLC / non-game']
counts = {b: sum(1 for r in games if r['bucket'] == b) for b in order[:-1]}
playable = counts['Confirmed working here'] + counts['Native macOS'] + counts['Should work well'] + counts['Works with tweaks']
now = datetime.datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %z')
L = [f'# Library triage — living compatibility map', f'', f'Updated {now}. Source of truth for what to try next. Buckets are re-derived by `data/make_triage.py`; per-game test results live in `data/results.json`.', '',
     f'**Library found locally: {len(names)} apps ({len(games)} games/demos, {len(rows)-len(games)} tools/DLC).** The Steam profile is private and there is no Web API key, so this is the set the signed-in client cached (library cache + playtime); titles never opened in the client may be missing. Paste a fuller list into `data/owned_ids.txt` and re-run to extend.', '',
     '| Bucket | Games | Meaning |', '|---|---|---|']
meaning = {'Confirmed working here': 'launched and verified on this Mac by the setup session',
           'Native macOS': 'has a Mac build on Steam — run it in the native Steam app, no CrossOver needed',
           'Should work well': 'no kernel anti-cheat, CrossOver database rates it Runs/Runs well/Runs great',
           'Works with tweaks': 'needs a renderer switch, launcher workaround or Winetricks component (see notes)',
           'Unknown / untested': 'no kernel anti-cheat and no CrossOver verdict found — just try it (D3DMetal first, DXMT if black screen)',
           'Known broken': 'CrossOver database says it does not run',
           'Kernel anti-cheat (blocked online)': 'online play is a hard wall on any Wine-based tool; single-player/offline modes may still run when the game offers an EAC-free launch'}
for b in order[:-1]:
    L.append(f'| {b} | {counts[b]} | {meaning[b]} |')
L += ['', f'Realistic coverage right now: **{playable} of {len(games)} games ({100*playable//max(1,len(games))}%)** are native, confirmed, or rated by CrossOver as working; {counts["Kernel anti-cheat (blocked online)"]} are blocked online by kernel anti-cheat; {counts["Unknown / untested"]} need a first try.', '']
for b in order:
    sub = [r for r in rows if r['bucket'] == b]
    if not sub: continue
    L += [f'## {b} ({len(sub)})', '', '| Game | AppID | Played | Anti-cheat | CrossOver rating | Renderer | Cloud (GFN) | Notes |', '|---|---|---|---|---|---|---|---|']
    for r in sub:
        L.append(f"| {r['name']} | {r['aid']} | {r['pt']//60}h {r['pt']%60}m | {r['ac']} | {r['rating']} | {r['renderer']} | {r['gfn']} | {r['note']} |")
    L.append('')
open(OUT, 'w').write('\n'.join(L))
print('wrote', os.path.abspath(OUT), '| games', len(games), '| counts', counts)
