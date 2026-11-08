#!/usr/bin/env bash
# Create a Frontier workspace from the templates in this folder.
# Usage: bash scripts/init.sh [TARGET_DIR]   (default: $FRONTIER_HOME or ~/frontier)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-${FRONTIER_HOME:-$HOME/frontier}}"

if [ -e "$TARGET" ] && [ -n "$(ls -A "$TARGET" 2>/dev/null || true)" ]; then
  echo "Target $TARGET exists and is not empty. Refusing to overwrite." >&2
  echo "Choose another directory or move the existing one aside." >&2
  exit 1
fi

mkdir -p "$TARGET"/{data,reports,inbox,tools}

cp "$HERE/templates/CLAUDE.md"         "$TARGET/CLAUDE.md"
cp "$HERE/templates/PROFILE.example.md" "$TARGET/PROFILE.md"
cp "$HERE/templates/STATE.example.md"   "$TARGET/STATE.md"
cp "$HERE/templates/SOURCES.example.md" "$TARGET/SOURCES.md"
cp "$HERE/WORKFLOW.md"                  "$TARGET/WORKFLOW.md"
cp "$HERE/README.md"                    "$TARGET/FRONTIER_README.md"
cp "$HERE/tools/extract_bing_cookies.py" "$TARGET/tools/extract_bing_cookies.py" 2>/dev/null || true

[ -f "$TARGET/data/events.jsonl" ] || : > "$TARGET/data/events.jsonl"
[ -f "$TARGET/inbox/.gitkeep" ]    || : > "$TARGET/inbox/.gitkeep"
[ -f "$TARGET/reports/.gitkeep" ]  || : > "$TARGET/reports/.gitkeep"

if [ ! -d "$TARGET/.git" ]; then
  git -C "$TARGET" init -q
  git -C "$TARGET" add -A
  git -C "$TARGET" commit -q -m "init: Frontier workspace from template" || true
fi

cat <<EOF
Frontier workspace created at: $TARGET

Next steps:
  1. Edit $TARGET/PROFILE.md  — fill in your background and owner-priority clusters.
  2. Edit $TARGET/SOURCES.md  — adjust the domain checklist and entity watchlist.
  3. Source config.example in your shell profile (FRONTIER_HOME, SEARCH_SCRIPT, ...).
  4. Run the workflow once by hand:
       cd $TARGET && claude
       > Read WORKFLOW.md and run today's routine.
  5. Schedule it (cron / launchd / a Claude Code scheduled task) when it feels right.

Note: by default the workspace git has NO remote. Add a private remote only if you want
off-machine backup of your PROFILE/STATE/ledger.
EOF
