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
