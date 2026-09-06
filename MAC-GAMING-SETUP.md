# MAC-GAMING-SETUP — Windows Steam games on this Mac

Date stamp: 2026-09-06 11:15 +03. Everything below was verified by running commands on this machine unless marked UNVERIFIED. CrossOver, macOS and game updates can each break any line of this; re-run `./troubleshoot.sh` first when something stops working.

## 1. Detected specs

| Item | Value |
|---|---|
| macOS | 27.0 "Golden Gate", build 26A5425a (press coverage as of 2026-09-06 still describes macOS 27 as developer beta; this build carries a beta-style suffix) |
| Machine | MacBook Pro Mac17,7, 14-inch (3024x1964 Liquid Retina XDR, running at 1x scaling) |
| Chip | Apple M5 Max, 18 CPU cores, 40-core GPU, Metal 4, 48 GB unified memory |
| Disk | 1.8 TB, 1.5 TB free before installs (Elden Ring took 55 GB) |
| Rosetta 2 | installed and working (`/Library/Apple/usr/libexec/oah`, `arch -x86_64` OK, `oahd` running) |
| Homebrew | 6.0.12 |
| Xcode | 26.6 installed, license NOT accepted (git, clang, otool, strings fail until `sudo xcodebuild -license`; python, curl, gh, codesign work) |
| Automatic macOS updates | still ON (needs admin auth to change — see Open issues) |

## 2. Golden Gate status

- **Worked:** Rosetta 2 present; CrossOver 26.3 installs, runs its command-line tools, creates a Windows 10 64-bit bottle, runs the Windows Steam client (signs in, downloads, launches games); D3DMetal 3.0 / Game Porting Toolkit 3.0 renders Elden Ring (D3D12) at native 3024x1964, 60.00 fps (game cap), 8.1 to 9.7 ms GPU frame time (n=2 gameplay samples), 65 to 73% GPU utilisation, CPU about 360 to 414% of one core (Rosetta). `msync` reports "up and running". Metal 4 present.
- **Broke / caveats:** none of CrossOver's parts failed on this OS. The Steam client UI is software-rendered by design (CrossOver injects `--no-sandbox --in-process-gpu --disable-gpu` into steamwebhelper.exe); it is usable but not as smooth as the native Steam app. Xcode license blocks several dev tools (unrelated to gaming).
- **What the brief got wrong (verified by search + this machine):** Apple keeps full Rosetta through macOS 27 (the installer removes a previously installed copy, reinstallable; a gaming subset survives past 27); Whisky's original author stopped in April 2025 but a community continuation shipped 3.4.0 (June 2026) and 3.6.0 (Aug 2026), still not recommended; no CodeWeavers macOS 27 statement exists yet; CrossOver 27 is an Apple-Silicon-native preview without D3DMetal/D3D12, targeted early 2027.
- **Workaround used:** none needed on the OS level. Steam's session was carried over from an earlier Wine install so no credentials were typed.

## 3. Software installed (log also in INSTALL-LOG.md)

| Software | Version | Method | Remove |
|---|---|---|---|
| CrossOver (14-day trial, timer started 2026-09-06 10:42 +03 at first run) | 26.3 (bundle says 26.3; Wine 11.0, D3DMetal 3.0, DXMT 0.72, vkd3d 1.18 per release notes for 26.0, not re-verified for 26.3) | zip from https://media.codeweavers.com/pub/crossover/cxmac/demo/crossover-26.3.0.zip, sha256 begins 8688e0848c4e5f79, unzipped to /Applications, Gatekeeper: notarized Developer ID, no sudo | `rm -rf /Applications/CrossOver.app "~/Library/Application Support/CrossOver"` |
| Windows Steam client in bottle "Steam" | current (build 1788652215 at install) | SteamSetup.exe /S via cxstart, then copy of the signed-in Steam directory from `~/.wine-steam-11` | `cxbottle --bottle Steam --delete --force` |
| ELDEN RING in the bottle | 55,123,319,452 bytes on disk | Steam download | uninstall in Steam or delete steamapps/common/ELDEN RING |
| Python package `vdf` 3.4 | user site-packages | `pip install --user --break-system-packages vdf` | `pip uninstall vdf` |
| Earlier session (still present): Merlot launchers + Sikarugir WineCX 24.0.7 engine + DXMT 0.74 + prefix `~/.wine-steam-11` | — | github.com/ByMedion/macos-wine-steam, patched copy in `~/macos-wine-steam` | run `~/macos-wine-steam/uninstall.command` (asks per item; needs sudo only for /Applications/Merlot Apps) |

Not installed: Whisky, Sikarugir app, Parallels, Heroic. Native Steam.app was already present.

## 4. Bottle inventory

| Bottle | Purpose | Renderer | Settings (cxbottle.conf [EnvironmentVariables]) | Games |
|---|---|---|---|---|
| Steam (win10_64) | main Steam bottle, one account (swonyu) | D3DMetal (`CX_GRAPHICS_BACKEND=d3dmetal`) | `D3DM_ENABLE_METALFX=1` (DLSS-to-MetalFX), `WINEMSYNC=1`, `MTL_HUD_ENABLED=1` (FPS overlay; delete the line to hide it) | ELDEN RING (working), Sons Of The Forest (install requested, waiting for the Install confirmation in Steam) |

Renderer switch without the GUI: edit that one line to `dxmt`, `dxvk` or `wined3d`, restart Steam. Rule of thumb from CodeWeavers' database: D3DMetal first; a black screen or crash on D3DMetal is the cue to try DXMT (Sons Of The Forest users recommend DXMT+FSR). For DXMT the DLSS analogue is `DXMT_ENABLE_NVEXT=1`.

Bottle strategy: one main "Steam" bottle for everything, plus a dedicated bottle only for titles that need a different renderer or Winetricks component (`cxbottle --create --bottle <name> --template win10_64`, then the same Steam copy). Two Steam accounts at the same time would need two bottles; switching accounts inside one bottle is just logging out and in.

## 5. Per-game results

| Game | Result | Settings | Measured |
|---|---|---|---|
| ELDEN RING (1245620) | works, gameplay reached, offline mode (CrossOver launches eldenring.exe directly; Easy Anti-Cheat not loaded, so no online play) | D3DMetal 3.0, native 3024x1964, game defaults | 60.00 fps (game cap), GPU 8.13 and 9.73 ms (n=2), GPU util 65 to 73%, Metal memory 4.5 to 4.8 GB |
| Steam client itself | works, signs in with remembered session | software-rendered UI (by design) | — |

1080p vs 1440p: not needed for Elden Ring; at native resolution the GPU has headroom (8 to 10 ms of a 16.7 ms frame). For heavier titles set the in-game resolution to 2560x1440; a Retina-style 2x render (`High resolution mode` in CrossOver) is not worth it on this 14-inch panel because it doubles pixel count for little visible gain.
DLSS via Metal 4 on macOS 27: NOT TESTED YET. The bottle already has `D3DM_ENABLE_METALFX=1`; the first DLSS-capable owned title (Sons Of The Forest, Hogwarts Legacy, Black Myth: Wukong, Dying Light 2) that gets installed can show a "DLSS" option in its graphics menu if the translation works.
Thermals: this is the 14-inch model, which throttles under sustained load sooner than the 16-inch; expect fans and lower sustained clocks after 15 to 20 minutes of AAA play. Keep it on a hard surface, prefer 60 fps caps over uncapped frame rates, and keep in-game resolution at 1440p or native rather than 2x.
Game Mode: macOS engages it automatically for a fullscreen game; nothing to configure.

## 5b. Steam client (the app itself) optimization in the bottle

Applied 2026-09-06 11:25 +03 with Steam closed, all reversible:
- Registry `HKCU\Software\Valve\Steam`: `GPUAccelWebViewsV3=0`, `H264HWAccel=0`, `SmoothScrollWebViews=0` (DWORD). Revert: delete the values with `reg delete` inside the bottle.
- Registry `HKCU\Software\Wine\Mac Driver`: `UsePreciseScrolling=n` (line-based scroll events instead of pixel-precise floods). Revert: delete the value.
- Steam `userdata/1130251896/config/localconfig.vdf` under `UserLocalConfigStore/Software/Valve/Steam`: `LibraryLowPerfMode=1`, `LibraryLowBandwidthMode=1`, `LibraryDisableCommunityContent=1` (Steam's own "Low Performance Mode", no animations or community art in the Library). Backup kept next to the file (`localconfig.vdf.bak-HHMM`). Revert: set them to 0 in Steam's Settings, Library.
- Owner asked for Low Performance Mode OFF (2026-09-06 11:40 +03): `LibraryLowPerfMode`, `LibraryLowBandwidthMode`, `LibraryDisableCommunityContent` are back to 0. The registry values above stay.
- Not changeable: the web UI runs software-rendered. The trailing `--no-sandbox --in-process-gpu --disable-gpu` on steamwebhelper.exe is added by the Steam client itself when it recognises CrossOver (the text exists nowhere in CrossOver 26.3's bundle, and Steam's own `-cef-force-gpu` switch leaves it in place). Tested 11:41: `-cef-force-gpu` also raised CPU during navigation to 532 to 617% of a core, so never use it.
- Steam auto-updates: an optional 16 GB ELDEN RING update started by itself at 11:43 (13.9 GB done before it was stopped). Elden Ring is now set to "update only when I launch it" (`AutoUpdateBehavior=1` in its appmanifest) and Steam's auto-update window is restricted to 03:00 to 04:00 in localconfig. The remaining part of that update downloads the next time the game is launched.
- Desktop shortcut: `~/Desktop/Steam (CrossOver).app` (AppleScript wrapper around `launch-game.sh`, icon extracted from steam.exe).

Measured with the same synthetic navigation harness (Library and Downloads pages, 6 navigations per run, first repaint after each command):

| State | Median navigation to repaint | Runs |
|---|---|---|
| Before (fresh bottle) | 470 ms, 496 ms | n=6 each |
| After | 82 ms, 100 ms, 607 ms (one outlier run) | n=5 each |

## 6. Library map

See `library-triage.md` (46 games found in the local client cache, profile is private). Now: 1 confirmed working, 9 native macOS, 6 rated working by CrossOver's database, 23 untested, 1 known broken (Overwatch 2), 6 blocked online by kernel anti-cheat.

## 7. Uninstall / rollback

1. Quit Steam in the bottle (Steam menu, Exit) or `pkill -f steam.exe`.
2. `"/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin/cxbottle" --bottle Steam --delete --force`
3. `rm -rf /Applications/CrossOver.app "$HOME/Library/Application Support/CrossOver"`
4. Optional: `~/macos-wine-steam/uninstall.command` removes the earlier Merlot setup (launchers, `~/wine-crossover-24.0.7`, `~/DXMT`, `~/.wine-steam-11`).
5. Optional: `rm -rf ~/mac-gaming` (this folder) and `pip uninstall vdf`.
Nothing here touched SIP, Gatekeeper, security settings, or system files.

## 8. Open issues and next steps

- Automatic macOS updates are still on; turning them off needs your admin password: System Settings, General, Software Update, (i) next to Automatic Updates, disable "Download new updates" and "Install macOS updates".
- Sons Of The Forest: confirm the Install dialog in the Steam window, then it downloads (about 20 GB); use it for the DLSS check.
- Elden Ring online play is a hard wall (Easy Anti-Cheat); offline works. Destiny 2 (BattlEye) is blocked; Dead by Daylight, VRChat, Sea of Thieves, Paragon are kernel-anti-cheat too. Cloud options: Destiny 2 and Dead by Daylight are on GeForce NOW's Steam list; Sea of Thieves is on Xbox Cloud Gaming (Sept 2026 report).
- CrossOver trial ends about 2026-09-20. Pricing seen in search snippets (UNVERIFIED): CrossOver+ about $74 per year, CrossOver Life about $494; trial bottles carry over on purchase.
- Two Windows Steam installs exist now; CrossOver's is the primary. The Merlot one can stay as a free fallback or be removed (step 4 above).
- Xcode license unaccepted; irrelevant to gaming.

## 9. Recommended layered setup and cost

| Layer | Covers | Cost |
|---|---|---|
| Native Steam.app | 9 native titles (Bloons TD 6, Dota 2, Black Ops III, 3DMark, ...) | 0 |
| CrossOver 26.3 (buy CrossOver+ if the trial keeps working for you) | the 6 rated titles + most of the 23 untested + Elden Ring offline | about $74/yr (UNVERIFIED price) |
| GeForce NOW (Ultimate tier for 1440p/120) | Destiny 2, Dead by Daylight, CS2/TF2/Dota if you prefer cloud | about $20/month (UNVERIFIED, check current pricing) |
| Xbox Game Pass Ultimate (cloud) | Sea of Thieves and other Game Pass titles | about $20/month (UNVERIFIED) |
| Parallels Desktop | only if you need a real Windows desktop; weak for D3D12 games | about $99/yr, not recommended for games |
| Sikarugir (free) | fallback if CrossOver breaks on a future macOS build; already proven here via its engine | 0 |

Realistic total for the library as found: CrossOver+ alone covers the large majority; add one cloud service only for the anti-cheat titles you actually play.
