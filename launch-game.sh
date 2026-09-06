#!/bin/bash
# launch-game.sh — start the Windows Steam client inside the CrossOver "Steam" bottle directly (no CrossOver UI),
# optionally launching a game by Steam AppID. Usage: ./launch-game.sh [APPID]   e.g. ./launch-game.sh 1245620
set -euo pipefail
BOTTLE="${BOTTLE:-Steam}"
CX="/Applications/CrossOver.app/Contents/SharedSupport/CrossOver/bin"
BOTTLE_DIR="$HOME/Library/Application Support/CrossOver/Bottles/$BOTTLE"
STEAM_EXE="$BOTTLE_DIR/drive_c/Program Files (x86)/Steam/steam.exe"
[[ -x "$CX/cxstart" ]] || { echo "CrossOver not found at /Applications/CrossOver.app" >&2; exit 1; }
[[ -d "$BOTTLE_DIR" ]] || { echo "bottle '$BOTTLE' not found under $BOTTLE_DIR" >&2; exit 1; }
[[ -f "$STEAM_EXE" ]] || { echo "steam.exe not found in bottle: $STEAM_EXE" >&2; exit 1; }
LOG="$HOME/mac-gaming/logs/steam-$(date +%Y%m%d-%H%M%S).log"; mkdir -p "$(dirname "$LOG")"
ARGS=()
[[ $# -ge 1 ]] && ARGS=(-applaunch "$1")
echo "bottle: $BOTTLE"; echo "renderer: $(grep -E '^"CX_GRAPHICS_BACKEND"' "$BOTTLE_DIR/cxbottle.conf" | cut -d'"' -f4 || true)"; echo "log: $LOG"
nohup "$CX/cxstart" --bottle "$BOTTLE" "C:/Program Files (x86)/Steam/steam.exe" -noverifyfiles ${ARGS[@]+"${ARGS[@]}"} </dev/null >"$LOG" 2>&1 &
disown
echo "started (pid $!). Steam keeps running after this terminal closes."
