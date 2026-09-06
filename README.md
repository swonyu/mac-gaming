# mac-gaming

Windows Steam games on a MacBook Pro M5 Max running macOS 27 "Golden Gate". Two working paths, one library map, and the scripts that drive them. Set up and verified on 2026-09-06; see `MAC-GAMING-SETUP.md` for the full record and `library-triage.md` for the living compatibility map.

## What's here

| Path | What it is |
|---|---|
| `MAC-GAMING-SETUP.md` | specs, Golden Gate status, every install with rollback, bottle inventory, per-game results, cost recommendation |
| `library-triage.md` | the library bucketed: native Mac, confirmed, should work, tweaks, untested, broken, kernel anti-cheat |
| `launch-game.sh [APPID]` | start the CrossOver bottle's Steam directly (skips the CrossOver UI), optionally launching a game |
| `switch-renderer.sh <backend> [APPID]` | change the bottle's D3D renderer (d3dmetal, dxmt, dxvk, wined3d), restart Steam, optionally launch a game — use when `library-triage.md` names a non-default renderer for a title, or when a game black-screens on D3DMetal |
| `troubleshoot.sh` | one-shot report for support posts: OS, Rosetta, CrossOver version, bottle settings, installed games, last log |
| `INSTALL-LOG.md` | everything installed, with the exact removal command |
| `HANDOFF.md` | session state for the assistant that maintains this |
| `data/` | library extraction and triage scripts plus the resolved library data (`make_triage.py` regenerates the map; `owned_library.py` + `resolve_names.py` rebuild the raw library from scratch) |
| `merlot/` | the free fallback: patched copy of [ByMedion/macos-wine-steam](https://github.com/ByMedion/macos-wine-steam) that uses a CrossOver-lineage engine (stock Wine cannot draw Steam's UI on macOS) |

## The two paths

1. **CrossOver 26.3** (primary): bottle `Steam`, renderer D3DMetal 3.0, MetalFX on, msync on. Elden Ring verified in gameplay at native 3024x1964, 60 fps cap, 8 to 10 ms GPU frame time.
2. **Merlot / Wine** (free fallback): `merlot/install_merlot.command` builds launcher apps into `/Applications/Merlot Apps`; `merlot/run.command` downloads the Sikarugir WineCX 24.0.7 engine, its support libraries and DXMT, sets up the prefix and starts Steam.

## Rules baked in

No anti-cheat bypasses, no SIP or Gatekeeper changes, no credentials in this repo. The kernel anti-cheat titles are listed so nobody wastes time on them; cloud services are the only path for those.
