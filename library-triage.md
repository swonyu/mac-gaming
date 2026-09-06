# Library triage — living compatibility map

Updated 2026-09-06 11:12 +0300. Source of truth for what to try next. Buckets are re-derived by `data/make_triage.py`; per-game test results live in `data/results.json`.

**Library found locally: 145 apps (46 games/demos, 99 tools/DLC).** The Steam profile is private and there is no Web API key, so this is the set the signed-in client cached (library cache + playtime); titles never opened in the client may be missing. Paste a fuller list into `data/owned_ids.txt` and re-run to extend.

| Bucket | Games | Meaning |
|---|---|---|
| Confirmed working here | 1 | launched and verified on this Mac by the setup session |
| Native macOS | 9 | has a Mac build on Steam — run it in the native Steam app, no CrossOver needed |
| Should work well | 6 | no kernel anti-cheat, CrossOver database rates it Runs/Runs well/Runs great |
| Works with tweaks | 0 | needs a renderer switch, launcher workaround or Winetricks component (see notes) |
| Unknown / untested | 23 | no kernel anti-cheat and no CrossOver verdict found — just try it (D3DMetal first, DXMT if black screen) |
| Known broken | 1 | CrossOver database says it does not run |
| Kernel anti-cheat (blocked online) | 6 | online play is a hard wall on any Wine-based tool; single-player/offline modes may still run when the game offers an EAC-free launch |

Realistic coverage right now: **16 of 46 games (34%)** are native, confirmed, or rated by CrossOver as working; 6 are blocked online by kernel anti-cheat; 23 need a first try.

## Confirmed working here (1)

| Game | AppID | Played | Anti-cheat | CrossOver rating | Renderer | Cloud (GFN) | Notes |
|---|---|---|---|---|---|---|---|
| ELDEN RING | 1245620 | 223h 40m | Easy Anti-Cheat | Runs | D3DMetal | - | CodeWeavers: runs with D3DMetal; launches with EAC disabled = offline only. Source codeweavers.com/compatibility/crossover/elden-ring (search snippet, medium confidence) |

## Native macOS (9)

| Game | AppID | Played | Anti-cheat | CrossOver rating | Renderer | Cloud (GFN) | Notes |
|---|---|---|---|---|---|---|---|
| Bloons TD 6 | 960090 | 79h 32m | - | - | - | - |  |
| 3DMark Demo | 231350 | 52h 0m | - | - | - | - |  |
| Call of Duty®: Black Ops III | 311210 | 42h 32m | VAC, Treyarch Anti-Cheat | - | - | - | Native Mac build (Aspyr) exists; maintenance status unverified |
| 3DMark | 223850 | 17h 53m | - | - | - | - | Store lists a Mac build; CrossOver rating for modern 3DMark unverified |
| Town of Salem 2 | 2140510 | 0h 46m | - | - | - | - |  |
| Crab Game | 1782210 | 0h 12m | - | - | - | - |  |
| Dota 2 | 570 | 0h 0m | VAC | - | - | yes |  |
| Half-Life 2: Demo | 219 | 0h 0m | - | - | - | - |  |
| Portal: First Slice | 410 | 0h 0m | - | - | - | - |  |

## Should work well (6)

| Game | AppID | Played | Anti-cheat | CrossOver rating | Renderer | Cloud (GFN) | Notes |
|---|---|---|---|---|---|---|---|
| Marvel Rivals | 2767030 | 96h 40m | NetEase Game Security | Runs well | - | - | NetEase anti-cheat currently tolerates CrossOver ('happy accident' per CodeWeavers, not guaranteed); bans reversed Jan 2025 |
| RuneScape: Dragonwilds | 1374490 | 39h 15m | - | Runs | - | - | Community video only, no CodeWeavers badge captured (low confidence) |
| Hogwarts Legacy | 990080 | 25h 1m | - | Runs well | D3DMetal | - | 60 fps reported on macOS 26 with Metal 4 + GPTK 3.0 (Notebookcheck) |
| Counter-Strike 2 | 730 | 20h 20m | VAC | Runs | D3DMetal or DXMT | yes | Community: playable online; D3DMetal faster start but stutters in fights, DXMT stutters first rounds; VAC status not documented |
| Sons Of The Forest | 1326470 | 3h 13m | - | Runs | DXMT + FSR | - | Mixed reports (M2 Pro: 15-25 fps with glitches); CodeWeavers users recommend DXMT+FSR over D3DMetal |
| Black Myth: Wukong | 2358720 | 0h 19m | - | Runs well | D3DMetal | - | Needs GPTK 2.0+ (26.x ships 3.0); 60 fps on macOS 26 reported |

## Unknown / untested (23)

| Game | AppID | Played | Anti-cheat | CrossOver rating | Renderer | Cloud (GFN) | Notes |
|---|---|---|---|---|---|---|---|
| Schedule I | 3164500 | 53h 59m | - | - | - | - | No CrossOver data found; Unity title, no anti-cheat — try it |
| Smart Game Booster | 1278480 | 35h 23m | - | - | - | - |  |
| Wallpaper Engine | 431960 | 23h 14m | - | - | - | - |  |
| Red Dead Online | 1404210 | 7h 4m | - | - | - | - |  |
| Sekiro™: Shadows Die Twice - GOTY Edition | 814380 | 5h 10m | - | - | - | - | CodeWeavers page exists, rating not captured; FromSoftware DX11 title, D3DMetal likely |
| LOCKDOWN Protocol | 2780980 | 3h 2m | - | - | - | - |  |
| Poppy Playtime | 1721470 | 1h 26m | - | - | - | - |  |
| V Rising | 1604030 | 0h 47m | Valve Anti-Cheat | - | - | - |  |
| Dying Light 2 Stay Human: Reloaded Edition | 534380 | 0h 41m | - | - | - | yes | CodeWeavers page exists, few testers |
| REANIMAL | 2129530 | 0h 39m | - | - | - | - |  |
| One-armed cook | 1977530 | 0h 31m | - | - | - | - |  |
| PCMark 10 | 524390 | 0h 10m | - | - | - | - |  |
| Europa Universalis III Complete Demo | 22150 | 0h 0m | - | - | - | - |  |
| Lepton | 3029110 | 0h 0m | - | - | - | - |  |
| Precipice of Darkness, Episode One Demo | 18010 | 0h 0m | - | - | - | - |  |
| Precipice of Darkness, Episode Two Demo | 18030 | 0h 0m | - | - | - | - |  |
| Resident Evil 6 Benchmark Tool | 229950 | 0h 0m | - | - | - | - |  |
| Source Filmmaker | 1840 | 0h 0m | - | - | - | - |  |
| Steam 360 Video Player | 613220 | 0h 0m | - | - | - | - |  |
| SteamVR | 250820 | 0h 0m | - | - | - | - |  |
| Team Fortress 2 | 440 | 0h 0m | VAC | - | - | yes | Valve dropped the native Mac build; needs CrossOver now, verdict unverified |
| VRMark | 464170 | 0h 0m | - | - | - | - |  |
| Yu-Gi-Oh! Master Duel | 1449850 | 0h 0m | - | - | - | - |  |

## Known broken (1)

| Game | AppID | Played | Anti-cheat | CrossOver rating | Renderer | Cloud (GFN) | Notes |
|---|---|---|---|---|---|---|---|
| Overwatch® | 2357570 | 9h 23m | Warden | Broken | - | - | Broken after a Blizzard update; needs unofficial community patch (MoltenVK/DXVK) — not supported |

## Kernel anti-cheat (blocked online) (6)

| Game | AppID | Played | Anti-cheat | CrossOver rating | Renderer | Cloud (GFN) | Notes |
|---|---|---|---|---|---|---|---|
| Destiny 2 | 1085660 | 37h 1m | BattlEye | Unplayable | - | yes | BattlEye: 'not compatible with Wine or CrossOver' (CodeWeavers page); online blocked |
| Dead by Daylight | 381210 | 15h 22m | Easy Anti-Cheat | - | - | yes |  |
| Paragon: The Overprime | 1531430 | 5h 9m | XIGNCODE3 | - | - | - |  |
| VRChat | 438100 | 2h 48m | Easy Anti-Cheat | - | - | - | EAC; old CodeWeavers rating flagged stale |
| Sea of Thieves: 2026 Edition | 1172620 | 1h 21m | Easy Anti-Cheat | - | - | - | EAC; playable via Xbox Cloud Gaming (trueachievements, Sept 2026) |
| Call of Duty: World at War | 10090 | 0h 21m | PunkBuster, Treyarch Anti-Cheat | - | - | - |  |

## Tools / DLC / non-game (99)

| Game | AppID | Played | Anti-cheat | CrossOver rating | Renderer | Cloud (GFN) | Notes |
|---|---|---|---|---|---|---|---|
| appid 480 | 480 | 0h 1m | - | - | - | - |  |
| 3DMark API Overhead feature test | 407080 | 0h 0m | - | - | - | - |  |
| 3DMark Cloud Gate benchmark | 406960 | 0h 0m | - | - | - | - |  |
| 3DMark CPU Profile benchmarks | 1654370 | 0h 0m | - | - | - | - |  |
| 3DMark Fire Strike benchmarks | 402290 | 0h 0m | - | - | - | - |  |
| 3DMark Ice Storm benchmarks | 406950 | 0h 0m | - | - | - | - |  |
| 3DMark Mesh Shader feature test | 1498800 | 0h 0m | - | - | - | - |  |
| 3DMark Night Raid benchmark | 496102 | 0h 0m | - | - | - | - |  |
| 3DMark PCI Express feature test | 496104 | 0h 0m | - | - | - | - |  |
| 3DMark Port Royal upgrade | 496103 | 0h 0m | - | - | - | - |  |
| 3DMark Sampler Feedback feature test | 1498801 | 0h 0m | - | - | - | - |  |
| 3DMark Sky Diver benchmark | 393480 | 0h 0m | - | - | - | - |  |
| 3DMark Solar Bay | 2313300 | 0h 0m | - | - | - | - |  |
| 3DMark Solar Bay Extreme | 3941790 | 0h 0m | - | - | - | - |  |
| 3DMark Speed Way Upgrade | 2019730 | 0h 0m | - | - | - | - |  |
| 3DMark Steel Nomad | 2695340 | 0h 0m | - | - | - | - |  |
| 3DMark Storage Benchmark | 1322770 | 0h 0m | - | - | - | - |  |
| 3DMark Time Spy upgrade | 496101 | 0h 0m | - | - | - | - |  |
| 3DMark VRS feature test | 556150 | 0h 0m | - | - | - | - |  |
| 3DMark Wild Life benchmarks | 1276160 | 0h 0m | - | - | - | - |  |
| appid 1007 | 1007 | 0h 0m | - | - | - | - |  |
| appid 1042420 | 1042420 | 0h 0m | - | - | - | - |  |
| appid 1054830 | 1054830 | 0h 0m | - | - | - | - |  |
| appid 1070560 | 1070560 | 0h 0m | - | - | - | - |  |
| appid 1070910 | 1070910 | 0h 0m | - | - | - | - |  |
| appid 1113280 | 1113280 | 0h 0m | - | - | - | - |  |
| appid 1161040 | 1161040 | 0h 0m | - | - | - | - |  |
| appid 1245040 | 1245040 | 0h 0m | - | - | - | - |  |
| appid 13180 | 13180 | 0h 0m | - | - | - | - |  |
| appid 1391110 | 1391110 | 0h 0m | - | - | - | - |  |
| appid 1420170 | 1420170 | 0h 0m | - | - | - | - |  |
| appid 1493710 | 1493710 | 0h 0m | - | - | - | - |  |
| appid 1580130 | 1580130 | 0h 0m | - | - | - | - |  |
| appid 1628350 | 1628350 | 0h 0m | - | - | - | - |  |
| appid 17505 | 17505 | 0h 0m | - | - | - | - |  |
| appid 17515 | 17515 | 0h 0m | - | - | - | - |  |
| appid 17525 | 17525 | 0h 0m | - | - | - | - |  |
| appid 1826330 | 1826330 | 0h 0m | - | - | - | - |  |
| appid 1874900 | 1874900 | 0h 0m | - | - | - | - |  |
| appid 1887720 | 1887720 | 0h 0m | - | - | - | - |  |
| appid 211 | 211 | 0h 0m | - | - | - | - |  |
| appid 2180100 | 2180100 | 0h 0m | - | - | - | - |  |
| appid 2230260 | 2230260 | 0h 0m | - | - | - | - |  |
| appid 223350 | 223350 | 0h 0m | - | - | - | - |  |
| appid 228980 | 228980 | 0h 0m | - | - | - | - |  |
| appid 230030 | 230030 | 0h 0m | - | - | - | - |  |
| appid 231390 | 231390 | 0h 0m | - | - | - | - |  |
| appid 233780 | 233780 | 0h 0m | - | - | - | - |  |
| appid 2348590 | 2348590 | 0h 0m | - | - | - | - |  |
| appid 243730 | 243730 | 0h 0m | - | - | - | - |  |
| appid 243750 | 243750 | 0h 0m | - | - | - | - |  |
| appid 2465200 | 2465200 | 0h 0m | - | - | - | - |  |
| appid 255470 | 255470 | 0h 0m | - | - | - | - |  |
| appid 261140 | 261140 | 0h 0m | - | - | - | - |  |
| appid 2738040 | 2738040 | 0h 0m | - | - | - | - |  |
| appid 2805730 | 2805730 | 0h 0m | - | - | - | - |  |
| appid 294420 | 294420 | 0h 0m | - | - | - | - |  |
| appid 302530 | 302530 | 0h 0m | - | - | - | - |  |
| appid 302550 | 302550 | 0h 0m | - | - | - | - |  |
| appid 3127680 | 3127680 | 0h 0m | - | - | - | - |  |
| appid 332850 | 332850 | 0h 0m | - | - | - | - |  |
| appid 34120 | 34120 | 0h 0m | - | - | - | - |  |
| appid 3658110 | 3658110 | 0h 0m | - | - | - | - |  |
| appid 374980 | 374980 | 0h 0m | - | - | - | - |  |
| appid 381690 | 381690 | 0h 0m | - | - | - | - |  |
| appid 382030 | 382030 | 0h 0m | - | - | - | - |  |
| appid 4019830 | 4019830 | 0h 0m | - | - | - | - |  |
| appid 41005 | 41005 | 0h 0m | - | - | - | - |  |
| appid 4183110 | 4183110 | 0h 0m | - | - | - | - |  |
| appid 42300 | 42300 | 0h 0m | - | - | - | - |  |
| appid 4270 | 4270 | 0h 0m | - | - | - | - |  |
| appid 42750 | 42750 | 0h 0m | - | - | - | - |  |
| appid 455130 | 455130 | 0h 0m | - | - | - | - |  |
| appid 4628710 | 4628710 | 0h 0m | - | - | - | - |  |
| appid 4628740 | 4628740 | 0h 0m | - | - | - | - |  |
| appid 545990 | 545990 | 0h 0m | - | - | - | - |  |
| appid 550140 | 550140 | 0h 0m | - | - | - | - |  |
| appid 568880 | 568880 | 0h 0m | - | - | - | - |  |
| appid 63220 | 63220 | 0h 0m | - | - | - | - |  |
| appid 635 | 635 | 0h 0m | - | - | - | - |  |
| appid 640 | 640 | 0h 0m | - | - | - | - |  |
| appid 70010 | 70010 | 0h 0m | - | - | - | - |  |
| appid 72310 | 72310 | 0h 0m | - | - | - | - |  |
| appid 72780 | 72780 | 0h 0m | - | - | - | - |  |
| appid 745 | 745 | 0h 0m | - | - | - | - |  |
| appid 858280 | 858280 | 0h 0m | - | - | - | - |  |
| appid 944490 | 944490 | 0h 0m | - | - | - | - |  |
| appid 961940 | 961940 | 0h 0m | - | - | - | - |  |
| Call of Duty®: Black Ops III - The Giant Zombies Map | 366849 | 0h 0m | - | - | - | - |  |
| Call of Duty®: Black Ops III - Zombies Chronicles | 581450 | 0h 0m | - | - | - | - |  |
| FiveM | 2676230 | 0h 0m | Unknown (Custom) | - | - | - |  |
| Hogwarts Legacy: Onyx Hippogriff Mount | 1880830 | 0h 0m | - | - | - | - |  |
| Marvel Rivals - High-Resolution Pack | 4406010 | 0h 0m | - | - | - | - |  |
| Poppy Playtime - Chapter 2 | 1817490 | 0h 0m | - | - | - | - |  |
| RedM | 4333400 | 0h 0m | - | - | - | - |  |
| RuneScape: Dragonwilds Early Adopter Soundtrack | 3637470 | 0h 0m | - | - | - | - |  |
| Smart Game Booster PRO | 1289950 | 0h 0m | - | - | - | - |  |
| VRMark Preview | 428810 | 0h 0m | - | - | - | - |  |
| Wallpaper Engine - Editor Extensions | 1790230 | 0h 0m | - | - | - | - |  |
