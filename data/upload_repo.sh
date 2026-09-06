#!/bin/bash
# upload_repo.sh — push the mac-gaming project to the private GitHub repo via the contents API (no git needed;
# the system git is blocked until the Xcode licence is accepted). Re-runnable: updates files that already exist.
# Usage: ./data/upload_repo.sh [owner/repo]
set -uo pipefail
REPO="${1:-swonyu/mac-gaming}"; GH=/opt/homebrew/bin/gh; ROOT="$HOME/mac-gaming"; MERLOT="$HOME/macos-wine-steam"
put() { # put <local file> <repo path>
  local f="$1" p="$2" sha msg
  sha=$("$GH" api "repos/$REPO/contents/$p" --jq .sha 2>/dev/null || true)
  msg="update $p"; [[ -z "$sha" ]] && msg="add $p"
  if [[ -n "$sha" ]]; then
    "$GH" api -X PUT "repos/$REPO/contents/$p" -f message="$msg" -f content="$(base64 -i "$f")" -f sha="$sha" --jq '.content.path' 2>&1 | tail -1
  else
    "$GH" api -X PUT "repos/$REPO/contents/$p" -f message="$msg" -f content="$(base64 -i "$f")" --jq '.content.path' 2>&1 | tail -1
  fi
}
cd "$ROOT" || exit 1
for f in README.md MAC-GAMING-SETUP.md library-triage.md launch-game.sh troubleshoot.sh INSTALL-LOG.md HANDOFF.md; do [[ -f "$f" ]] && put "$f" "$f"; done
for f in data/make_triage.py data/owned_library.py data/extract_library.py data/resolve_names.py data/upload_repo.sh data/cx_ratings.json data/results.json data/names.json data/owned.json data/library.json data/owned_ids.txt data/lc_ids.txt data/sc_ids.txt; do [[ -f "$f" ]] && put "$f" "$f"; done
printf '%s\n' 'data/*.zip' 'data/*.html' 'data/awacy.json' 'data/gfn.json' 'data/games-*.xml' 'data/*.log' 'logs/' '*.bak-*' > /tmp/mac-gaming.gitignore; put /tmp/mac-gaming.gitignore .gitignore
cd "$MERLOT" || exit 1
for f in LICENSE README.md README_DEV.md .gitignore install_merlot.command run.command uninstall.command app/merlot/MerlotLauncher app/merlot/AppIcon.icns merlot_configs/steam.conf merlot_configs/binding-of-isaac.conf merlot_configs/template.conf.example; do [[ -f "$f" ]] && put "$f" "merlot/$f"; done
echo "done: https://github.com/$REPO"
