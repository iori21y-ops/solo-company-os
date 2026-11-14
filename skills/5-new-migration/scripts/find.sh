#!/bin/bash
# List migration SQL files that mention a table, newest first, so the new
# migration goes to the same folder as the last change to that table.
#   find.sh <table_name>
set -uo pipefail
TABLE="${1:-}"
ROOT="${MIG_PROJECTS_ROOT:-$HOME/projects}"
if [ -z "$TABLE" ] || ! echo "$TABLE" | grep -qE '^[a-z_][a-z0-9_]*$'; then
  echo "사용법: find.sh <표 이름(영어 소문자·_)>"; exit 2
fi
echo "=== '$TABLE'을(를) 다룬 마이그레이션 (최근 순) ==="
HITS="$(find "$ROOT" \( -name node_modules -o -name _archive -o -name .git -o -name '_wt-*' \) -prune -o \
  -type f -name '*.sql' -path '*migrations*' -print 2>/dev/null \
  | while IFS= read -r f; do grep -qiwE "$TABLE" "$f" && printf '%s\t%s\n' "$(basename "$f")" "$f"; done \
  | sort -r | cut -f2)"
if [ -z "$HITS" ]; then
  echo "(없음) → 처음 다루는 표다. 어느 폴더에 둘지 사장님께 묻는다 (SKILL.md 폴더 표 참고)."
  exit 0
fi
echo "$HITS" | head -10 | sed "s#^$ROOT/#  ~/projects/#"
LAST_DIR="$(dirname "$(echo "$HITS" | head -1)")"
echo ""
echo "→ 따를 폴더: ${LAST_DIR/#$ROOT/~/projects} (가장 최근에 이 표를 다룬 곳)"
