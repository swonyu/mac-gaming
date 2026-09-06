2026-09-06 10:38 +0300 INSTALL CrossOver 26.3.0 trial -> /Applications/CrossOver.app (from media.codeweavers.com/pub/crossover/cxmac/demo/crossover-26.3.0.zip, unzip, no sudo). Remove: rm -rf /Applications/CrossOver.app ~/Library/Application\ Support/CrossOver
2026-09-06 10:41 +0300 INSTALL Steam (Windows) into CrossOver bottle 'Steam' via SteamSetup.exe /S + copy of ~/.wine-steam-11 Steam dir (session carried over). Remove: cxbottle --bottle Steam --delete --force
2026-09-06 10:47 +0300 CONFIG bottle Steam: CX_GRAPHICS_BACKEND=d3dmetal, D3DM_ENABLE_METALFX=1 in cxbottle.conf [EnvironmentVariables]; ELDEN RING (1245620, 49.9 GB) downloading into the bottle (carried-over partial). Revert: delete those two lines
2026-09-06 10:49 +0300 CONFIG bottle Steam: WINEMSYNC=1 (revert: delete the line in cxbottle.conf)
2026-09-06 10:51 +0300 CONFIG bottle Steam: MTL_HUD_ENABLED=1 (FPS overlay; revert: delete line)
2026-09-06 11:12 +0300 RESULT ELDEN RING (1245620) runs in CrossOver 26.3 bottle 'Steam' with D3DMetal 3.0 at 3024x1964, 60 fps cap, 8.13 ms GPU (HUD), offline mode
2026-09-06 11:25 +0300 CONFIG bottle Steam registry: GPUAccelWebViewsV3=0 H264HWAccel=0 SmoothScrollWebViews=0 (HKCU\Software\Valve\Steam), UsePreciseScrolling=n (HKCU\Software\Wine\Mac Driver); localconfig.vdf LibraryLowPerfMode/LibraryLowBandwidthMode/LibraryDisableCommunityContent=1 (backup localconfig.vdf.bak-*). Revert: reg delete / set to 0 in Steam settings
2026-09-06 11:46 +0300 CONFIG Steam: ELDEN RING AutoUpdateBehavior=1 (update only on launch), auto-update window 03:00-04:00; revert in Steam settings
2026-09-06 12:11 +0300 TESTED DWriteEnable=0 (GDI text): no gain, higher CPU -> reverted. launch-game.sh now passes -noverifyfiles (startup skips file verification; remove the flag to restore)
