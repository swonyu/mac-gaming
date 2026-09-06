#!/bin/bash
# switch-renderer.sh — change the bottle's D3D renderer and restart Steam. Use when a game shows a black
# screen or crashes on D3DMetal (the default): try dxmt next, then dxvk, then plain wine as a last resort.
# Usage: ./switch-renderer.sh d3dmetal|dxmt|dxvk|wined3d [APPID-to-launch-after]
set -euo pipefail
BACKEND="${1:?usage: switch-renderer.sh d3dmetal|dxmt|dxvk|wined3d [appid]}"
case "$BACKEND" in d3dmetal|dxmt|dxvk|wined3d) ;; *) echo "unknown backend: $BACKEND (use d3dmetal, dxmt, dxvk, or wined3d)" >&2; exit 1 ;; esac
BOTTLE="${BOTTLE:-Steam}"
CXB="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin"
CXR="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver"
CONF="$HOME/Library/Application Support/CrossOver/Bottles/$BOTTLE/cxbottle.conf"
[[ -f "$CONF" ]] || { echo "bottle config not found: $CONF" >&2; exit 1; }

echo "stopping Steam in bottle '$BOTTLE'..."
"$CXB/cxstart" --bottle "$BOTTLE" "C:/Program Files (x86)/Steam/steam.exe" -shutdown >/dev/null 2>&1 || true
for i in $(seq 1 15); do pgrep -f "Steam/steam.exe|steamwebhelper" >/dev/null || break; sleep 2; done
WINEPREFIX="$HOME/Library/Application Support/CrossOver/Bottles/$BOTTLE" "$CXR/bin/wineserver" -k 2>/dev/null || true
sleep 2

/opt/homebrew/bin/python3 - "$CONF" "$BACKEND" <<'EOF'
import sys, re
p, backend = sys.argv[1], sys.argv[2]
s = open(p).read()
line = f'"CX_GRAPHICS_BACKEND" = "{backend}"'
pat = re.compile(r'^"CX_GRAPHICS_BACKEND"\s*=\s*".*"$', re.M)
s = pat.sub(line, s) if pat.search(s) else s.replace('[EnvironmentVariables]', '[EnvironmentVariables]\n' + line, 1)
open(p, 'w').write(s)
print(f"renderer set to {backend}")
EOF

echo "$(date '+%Y-%m-%d %H:%M %z') CONFIG bottle $BOTTLE: CX_GRAPHICS_BACKEND=$BACKEND" >> "$HOME/mac-gaming/INSTALL-LOG.md"

if [[ $# -ge 2 ]]; then
  echo "launching appid $2 with $BACKEND..."
  "$HOME/mac-gaming/launch-game.sh" "$2"
else
  echo "renderer switched. Launch Steam normally with ./launch-game.sh [appid]."
fi
