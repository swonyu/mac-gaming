#!/bin/bash
# troubleshoot.sh — collect what a CodeWeavers/r/macgaming support post needs. Usage: ./troubleshoot.sh [BOTTLE] > report.txt
BOTTLE="${1:-Steam}"
BOTTLES="$HOME/Library/Application Support/CrossOver/Bottles"
echo "=== $(date '+%Y-%m-%d %H:%M %z') troubleshoot: bottle $BOTTLE ==="
echo "--- macOS"; sw_vers
echo "--- hardware"; system_profiler SPHardwareDataType 2>/dev/null | grep -E 'Model Identifier|Chip|Memory' | sed 's/^ *//'
echo "--- Rosetta"; /usr/bin/arch -x86_64 /usr/bin/true 2>/dev/null && echo "installed and working" || echo "MISSING (softwareupdate --install-rosetta --agree-to-license)"
echo "--- CrossOver"; defaults read /Applications/CrossOver.app/Contents/Info.plist CFBundleShortVersionString 2>/dev/null || echo "not installed"
echo "--- bottles"; ls "$BOTTLES" 2>/dev/null
echo "--- bottle settings ($BOTTLE)"; grep -E '^"(WineArch|CX_GRAPHICS_BACKEND|D3DM_ENABLE_METALFX|DXMT_ENABLE_NVEXT|WINEMSYNC|WINEESYNC)"' "$BOTTLES/$BOTTLE/cxbottle.conf" 2>/dev/null || echo "(defaults: auto backend)"
echo "--- Steam in bottle"; ls "$BOTTLES/$BOTTLE/drive_c/Program Files (x86)/Steam/steam.exe" 2>/dev/null && grep -E 'AccountName|RememberPassword' "$BOTTLES/$BOTTLE/drive_c/Program Files (x86)/Steam/config/loginusers.vdf" 2>/dev/null | tr -s ' \t' ' '
echo "--- installed games (appmanifests)"; for m in "$BOTTLES/$BOTTLE/drive_c/Program Files (x86)/Steam/steamapps"/appmanifest_*.acf; do [[ -f "$m" ]] && awk -F'"' '/"appid"|"name"|"StateFlags"/{printf "%s=%s ", $2, $4} END{print ""}' "$m"; done 2>/dev/null
echo "--- running wine processes"; ps -Ao pid,%cpu,rss,command | grep -iE '\.exe|wineserver' | grep -v grep | cut -c1-140
LATEST=$(ls -t "$HOME/mac-gaming/logs"/steam-*.log 2>/dev/null | head -1)
echo "--- last 200 lines of latest launch log: ${LATEST:-none}"; [[ -n "$LATEST" ]] && tail -200 "$LATEST" | grep -v '^\[mvk-info\]'
