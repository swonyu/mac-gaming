# HANDOFF — Mac gaming setup (Windows Steam on M5 Max, macOS 27)

Written 2026-09-06 10:33 +03 by the Claude Code session that set up Steam-under-Wine. Read this first after a compaction or in a new session. good-spender must be ON (owner rule).

## State as of this handoff

**Working today (verified by measurement, not assumption):**
- Windows Steam client runs under Wine via `/Applications/Merlot Apps/Steam (Merlot).app` (repo: https://github.com/ByMedion/macos-wine-steam, patched copy at `~/macos-wine-steam`). Login window renders, auto-login works (user account already signed in once), Store/Library navigate.
- Engine: Sikarugir "WineCX 24.0.7" (CrossOver-24 lineage, wine-9.0) at `~/wine-crossover-24.0.7/Frameworks/wswine.bundle`; support dylibs in `~/wine-crossover-24.0.7/Frameworks`, symlinked into `wswine.bundle/lib` (Wine resolves bare dylib names via rpath `@loader_path/../../`, NOT via DYLD_* — ignored under Rosetta). DXMT 0.74 at `~/DXMT`, loaded via `WINEDLLPATH_PREPEND` (this engine honors it; Gcenx stock builds do not). Prefix `~/.wine-steam-11`.
- Why not stock Wine: stock Wine cannot present Chromium's cross-process frames → Steam UI black (3Shain/dxmt#141). CrossOver's kernelbase.dll hardcodes `--no-sandbox --in-process-gpu --disable-gpu` for steamwebhelper.exe → UI is software-rendered by design; GPU-on is a documented dead end (no text on 2026 Steam builds).
- Perf pass done: registry `HKCU\Software\Valve\Steam` GPUAccelWebViewsV3=0, H264HWAccel=0, SmoothScrollWebViews=0; `HKCU\Software\Wine\Mac Driver` UsePreciseScrolling=n (set by run.command). WINEMSYNC measured: no gain, SIGFPE in short-lived steam.exe helpers → default 0 (opt-in via `WINEMSYNC=1`). Measured nav→repaint latency (steam://open/games ↔ steam://open/downloads, n=6 per run, steady-state second run): 61–82 ms median; CPU 128–154% of one core during the burst; baseline run before changes 397 ms median (n=4, store↔library, network-dependent — not strictly comparable).
- Honest ceiling: native-Steam smoothness is NOT reachable for the Wine client UI; use native `/Applications/Steam.app` for browsing/chat, Merlot Steam only to launch Windows-only games (games render through DXMT/Metal).

**Phase 1 diagnostics (2026-09-06 10:31 +03):** macOS 27.0 build 26A5425a; MacBook Pro Mac17,7, Apple M5 Max, 18 CPU cores, 40-core GPU, Metal 4, 48 GB unified memory; 3024x1964 display (14-inch panel); disk 1.8 TB, 1.5 TB free; Rosetta 2 INSTALLED and functional (`/Library/Apple/usr/libexec/oah` present, `arch -x86_64 /usr/bin/true` OK, oahd running) — contradicts the brief's claim that macOS 27 removes it; Homebrew 6.0.12; Apps present: Steam.app (native), UTM.app, Merlot launchers; NOT present: CrossOver, Whisky, Sikarugir, Parallels; automatic macOS updates ON (AutomaticDownload=1, AutomaticallyInstallMacOSUpdates=1, App Store AutoUpdate=1); Xcode 26.6 installed but license NOT accepted (git/clang/otool/strings blocked; python/curl/gh/codesign fine).

## In flight / pending
- Two Sonnet research workers (Phase 2 step 3): (a) CrossOver current version/CrossOver 27/trial/pricing/anti-cheat from codeweavers.com; (b) macOS 27 + CrossOver/Rosetta/DLSS reports, Whisky status, Sikarugir official brew command. Results feed the Phase 2 recommendation. STOP for the owner's go-ahead before Phase 3 (brief says so).
- Not yet done: Phase 2 step 2 (disable auto-updates — GUI walkthrough or sudo, ask first), Phases 3–9.

## Owner rules for this project (from the brief)
Ask before every install/download/sudo (show exact command); never touch anti-cheat, SIP, Gatekeeper; never enter Steam credentials; log every install for reversal; official sources only (CrossOver from codeweavers.com; Sikarugir via `brew install --cask Sikarugir-App/sikarugir/sikarugir` — verify README); stop and report on phase failure; no "works perfectly" claims; trust fresh web search over the brief's Critical Context and say what changed.

## Files
- `~/mac-gaming/` — this project folder (brief's "./"): HANDOFF.md now; MAC-GAMING-SETUP.md, library-triage.md, launch-game.sh, troubleshoot.sh to come.
- `~/macos-wine-steam/run.command` — patched launcher script (WINE_LIBS/WINE_APP layout, ensure_wine_libs_linked, UsePreciseScrolling, WINEMSYNC default 0).
- Memory: `~/.claude/projects/-Users-saleh/memory/macos-wine-steam-setup.md`, `feedback-good-spender-always-on.md`.
- Measurement harness (session scratch, will vanish): drives Steam with `steam://open/games` / `steam://open/downloads` via a second `steam.exe` and diffs per-window `screencapture -l` frames; scripted macOS input is blocked (Claude app not Accessibility-trusted); Wine's WScript.Shell lacks SendKeys/AppActivate.

## Phase 2 research results (2026-09-06 10:34 +03, two Sonnet workers; codeweavers.com blocks direct fetch → indexed snippets + AppleInsider/Phoronix/MacRumors)
- CrossOver latest stable: 26.3.0 (2026-07-21, bug-fix); no newer point release found through 2026-09-06. Bundled Wine 11.0 / D3DMetal 3.0 / DXMT 0.72 / vkd3d 1.18 confirmed for 26.0 (Feb 10 2026), not re-confirmed for 26.3. 26.x needs Rosetta 2. Trial 14 days/no card and $74/yr, $494 Life: UNVERIFIED (snippets only).
- CrossOver 27: Apple-Silicon-native preview since late July 2026; no D3DMetal, no D3D12, many launchers broken, no bottle migration; target early 2027. Not usable for gaming now.
- No CodeWeavers macOS 27 compatibility statement found; no first-hand r/macgaming or forum reports for macOS 27 found (gap, not a negative). macOS 27 described as still in developer beta as of the sources (this Mac runs build 26A5425a).
- Rosetta: Apple keeps full Rosetta through macOS 27; the Golden Gate installer removes a previously-installed Rosetta but it is reinstallable; a gaming-focused subset survives past 27. On THIS Mac Rosetta is installed and working.
- Direct evidence from this machine: CrossOver-24-lineage Wine + DXMT runs Windows Steam on this exact macOS 27 build (see above). D3DMetal untested here (not present).
- DLSS/Metal 4 on macOS 27: no reports either way; must test empirically in Phase 7.
- Whisky: original developer stopped (Apr 2025) but a community continuation shipped 3.4.0 (2026-06-13) and 3.6.0 (2026-08-04); archived-badge status UNVERIFIED. Still not recommended per brief.
- Sikarugir official install (README verbatim): `brew upgrade` / `brew trust Sikarugir-App/sikarugir` / `brew install --cask Sikarugir-App/sikarugir/sikarugir`; README warns sikarugir.com is unaffiliated.
- Recommendation given: stay on Golden Gate; run the CrossOver 26.3 trial as the smoke test; keep Tahoe-on-external-SSD as fallback only if D3DMetal fails; disable auto-updates first. Awaiting owner go-ahead for Phase 3.
- Owner 10:34: granted full computer control for visual/internal testing (computer-use MCP; request_access dialog still required per tool).

## Phase 3-6 progress (2026-09-06 ~10:55 +03, owner: "do whatever you think is best without asking"; good-spender auto ON for this session only — turn OFF at close)
- CrossOver 26.3 trial installed at /Applications/CrossOver.app (notarized, from media.codeweavers.com/pub/crossover/cxmac/demo/crossover-26.3.0.zip, sha256 starts 8688e0848c4e5f79). CLI works without the GUI: cxbottle/cxstart. Bottle "Steam" (win10_64) at ~/Library/Application Support/CrossOver/Bottles/Steam; Steam installed silently and the signed-in session copied from ~/.wine-steam-11 (auto-login OK; Merlot Steam shut down, left installed).
- Bottle config [EnvironmentVariables]: CX_GRAPHICS_BACKEND=d3dmetal, D3DM_ENABLE_METALFX=1, WINEMSYNC=1, MTL_HUD_ENABLED=1 (renderer switch = this env var: d3dmetal|dxmt|dxvk|wined3d; DXMT DLSS analogue = DXMT_ENABLE_NVEXT=1). D3DMetal payload: CrossOver/lib64/apple_gptk/external/D3DMetal.framework; DXMT at lib/dxmt.
- CrossOver's kernelbase.dll injects "--no-sandbox --in-process-gpu --disable-gpu" for steamwebhelper (same as the Sikarugir engine) → Steam UI software-rendered; verified Steam client renders and logs in inside the bottle.
- Library: 145 candidate owned appids from the client's librarycache (profile is private; no API key); names/platforms resolved via store API into data/names.json; triage generated by data/make_triage.py → library-triage.md (46 games: 9 native Mac, 6 should-work, 23 unknown, 1 broken, 7 kernel anti-cheat). Ratings in data/cx_ratings.json from a Sonnet research pass (codeweavers.com blocks fetches; snippet-level).
- ELDEN RING (1245620) fully downloaded into the bottle (53,557,604,400 bytes); launching for the smoke test next. Sons of the Forest install queued via steam://install (no dialog seen; unconfirmed).
- Still owner-only: disable automatic macOS updates (admin auth). Not done: DLSS/Metal 4 empirical test, 1080p vs 1440p comparison, MAC-GAMING-SETUP.md, Phase 8 cost recommendation.

## Closeout 2026-09-06 11:17 +03
- ELDEN RING verified in gameplay under CrossOver 26.3 / D3DMetal 3.0 (60 fps cap, 8.1-9.7 ms GPU, n=2); owner: "i like it no lag now"; game closed on request, Steam left running in the bottle.
- Deliverables written: ~/mac-gaming/MAC-GAMING-SETUP.md, library-triage.md, launch-game.sh, troubleshoot.sh, INSTALL-LOG.md, data/*. good-spender auto mode turned OFF (was session-only).
- Open for owner: disable automatic macOS updates (admin); confirm Sons Of The Forest install in Steam for the DLSS/Metal 4 check; decide on CrossOver+ before ~2026-09-20; optionally remove the Merlot setup via ~/macos-wine-steam/uninstall.command.

## 11:25 +03 — Steam client optimization in the CrossOver bottle + private repo
- Owner: no more downloads; they will try games themselves. Sons Of The Forest install left unconfirmed (nothing downloads unless Install is clicked).
- Applied in bottle (Steam closed): Valve registry perf keys, UsePreciseScrolling=n, localconfig LibraryLowPerfMode/LowBandwidth/DisableCommunityContent=1. Harness: nav->repaint median 470/496 ms before (n=6 each) -> 82/100/607 ms after (n=5 each). launch-game.sh fixed for bash 3 empty-array under set -u.
- Private repo created: https://github.com/swonyu/mac-gaming (gh CLI account swonyu). System git is blocked by the Xcode licence, so files are uploaded through the GitHub contents API (data/upload_repo.sh). Layout: root = ~/mac-gaming docs/scripts, data/ (scripts + resolved library json, no big datasets), merlot/ = patched ~/macos-wine-steam.

## 11:50 +03 — "improve it more without Low Performance Mode", "open the app", "make a desktop shortcut"
- LibraryLowPerfMode/LowBandwidth/DisableCommunityContent reverted to 0. Registry perf keys + UsePreciseScrolling=n stay.
- GPU-rendered Steam UI is closed by Valve: the trailing "--no-sandbox --in-process-gpu --disable-gpu" is added by the Steam client when it detects CrossOver (text exists nowhere in CrossOver 26.3's bundle; kernelbase.dll table only exists in the older Sikarugir CX24 engine); Steam's -cef-force-gpu leaves it and costs 532-617% CPU → never use. Bottle-local kernelbase override dir ~/Library/Application Support/CrossOver/Bottles/Steam/dlloverride was created but is unused (safe to delete).
- ELDEN RING optional 16 GB update auto-ran and completed; AutoUpdateBehavior=1 set for it; localconfig AutoUpdateWindow 03:00-04:00. Owner wants no downloads.
- Desktop shortcut ~/Desktop/Steam (CrossOver).app (osacompile wrapper → launch-game.sh, icon from steam.exe). Steam relaunched cleanly; final harness after clean relaunch: 64 ms (n=6) and 125 ms (n=4) medians; CPU during those runs was inflated by the concurrent update download.

## 12:15 +03 — "improve even more" round 3, "overclock", "loading links"
- Vendor Steam profile in crossover.tie has no perf entries since 2025-06-05 (GPUAccelWebViews + LargeAddressAware removed); bottle matches vendor stance. Wine debug already quiet; font AA already grayscale.
- DWriteEnable=0 tested: no gain, more CPU → reverted (value deleted). -noverifyfiles added to launch-game.sh (kept).
- Baseline medians 120/55/78 ms (n=6 each), ~100% core during burst. Store pages: server TTFB 0.45-0.57 s (v4≈v6, IPv6 OK), first repaint 100-440 ms after click; rest is page content + software video decode. Suggested user action: store account preference "Autoplay videos" off.
- Mac: powermode 2 (High Power) already on, AC. No overclocking on Apple Silicon.
- Verdict recorded in MAC-GAMING-SETUP.md 5b: client at practical ceiling under CrossOver.

## 12:20 +03 — "improve the app more" round 4
- Extra CEF windows identified: Steam "Special Offers" ad popup (706x830) reopens each start (account notification preference, cached in localconfig CachedNotificationPreferences — server-authoritative, not settable locally); Friends list (300x650) restores if left open. Owner action: Settings > Notifications > Special offers = Don't notify; close Friends list.
- Idle CPU ~2% total; display refresh not reported by system_profiler; no further local levers. Client declared at ceiling (documented).

## 13:40 +03 — "I want all the games in the library to work but I dont wanna test every single one"
- Dropped the FPS-unlock attempt (owner: "nvm nvm the 120 fps"); removed the downloaded EldenRingFPSUnlockAndMore_v1.1.0.0.exe and its folder — clean.
- Interpreted the ask as: research + configure every game so it has its best shot, without downloading/testing all 46 titles myself (owner had already said no more downloads). Three Sonnet research batches filled CrossOver-database verdicts for the 22 previously-untested games (cx_ratings.json now 30 entries). Two appids (Lepton 3029110 = Valve's Android compat layer, Smart Game Booster 1278480 = Windows-only utility) reclassified out of the games count via a NOT_A_GAME set in make_triage.py.
- New: switch-renderer.sh <d3dmetal|dxmt|dxvk|wined3d> [appid] — restarts Steam under a different bottle renderer, optionally launches a game after. Yu-Gi-Oh! Master Duel needs dxvk (rated EXCELLENT there, not D3DMetal); Sons Of The Forest needs dxmt+FSR.
- Fixed a bucket-precedence bug in make_triage.py: a "tweaks" rating now wins over a plain "Runs" rating (Sons Of The Forest was being bucketed as plain "Should work well", losing the DXMT-not-D3DMetal warning).
- Current triage: 38 real games, 1 confirmed (Elden Ring), 9 native, 8 should-work, 1 works-with-tweaks, 12 genuinely unknown anywhere, 1 broken (Overwatch 2), 6 kernel-anticheat-blocked (one of those, Paragon Overprime, is also a dead game — servers shut April 2024).

## 13:52 +03 — "i want 0 bugs in the code" — code review pass
Reviewed every script (shellcheck on all .sh/.command, py_compile on all .py, manual logic trace). Found and fixed 4 real issues:
1. **extract_library.py — confirmed non-functional, deleted.** Its primary path checked `hasattr(vdf, 'appinfo')`, which the installed vdf package never has, so it always fell to a fallback whose regex loop was a bare `pass` — it wrote zero real fields. Proven by an actual prior run's own output: "type=game: 0". Dead code besides — make_triage.py never reads library.json. Removed the script + its stale output + its two upload_repo.sh references. owned_library.py + resolve_names.py are the real, working pipeline.
2. **switch-renderer.sh — silent no-op on a bottle with no `[EnvironmentVariables]` section at all** (a genuinely fresh bottle, e.g. one created per the setup doc's "dedicated bottle for a problem game" advice). The patcher only handled "key exists" and "section exists but key doesn't" — now it also creates the section header itself when missing. Verified against an isolated test file.
3. **make_triage.py — a `|` in any future free-text name/note would have corrupted the markdown table.** No current data triggers it, but notes are hand-written text; added an escape helper. Regenerated triage.md, counts unchanged (38 games, same buckets) — confirms the fix is behavior-preserving for existing data.
4. **troubleshoot.sh — removed a dead unused variable** (shellcheck-flagged).
Left alone (checked, not bugs): launch-game.sh's steam.exe case vs Steam.exe on disk — confirmed harmless, this Mac's boot volume is case-insensitive APFS (verified directly). Three remaining shellcheck notes (SC2034/SC2009/SC2012) are style-only on fully-controlled inputs, no evidence of actual breakage, left as-is per ponytail (no unrequested churn). run.command/install_merlot.command/uninstall.command: shellcheck clean, patched sections (WINEMSYNC default, UsePreciseScrolling) re-verified logically correct.
Cannot claim literally zero bugs — no review proves that. This is what was reviewed and what was found; residual risk is unreviewed edge cases, not known issues.
