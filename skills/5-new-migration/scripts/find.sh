#!/bin/bash
# List migration SQL files that mention a table, newest first (by last git commit,
# falling back to file mtime), so the new migration goes where that table lives.
# If the table name shows up in more than one business's DB, it stops and asks.
#   find.sh <table_name>
set -uo pipefail
TABLE="${1:-}"
ROOT="${MIG_PROJECTS_ROOT:-$HOME/projects}"
if [ -z "$TABLE" ] || ! echo "$TABLE" | grep -qE '^[a-z_][a-z0-9_]*$'; then
  echo "사용법: find.sh <표 이름(영어 소문자·_)>"; exit 2
fi

# Which business DB a folder belongs to (rentailor code lives in cadam/ and web-engine/).
biz_of() {
  case "$1/" in
    "$ROOT/cadam/"*|"$ROOT/web-engine/"*) echo rentailor ;;
    *) local rel="${1#$ROOT/}"; echo "${rel%%/*}" ;;
  esac
}
when_of() {
  local t
  t="$(git -C "$(dirname "$1")" log -1 --format=%ct -- "$1" 2>/dev/null)"
  [ -n "$t" ] && echo "$t" || stat -f %m "$1" 2>/dev/null || stat -c %Y "$1"
}

echo "=== '$TABLE'을(를) 다룬 마이그레이션 (최근 기록 순) ==="
# Migrations live in */migrations/, directly in */db/ (e.g. cadam/db/20261022_*.sql) and in */supabase/.
# Only files whose name starts with a number/date/timestamp count (skips dumps, seeds, create scripts).
HITS="$(find "$ROOT" \( -name node_modules -o -name _archive -o -name .git -o -name '_wt-*' \) -prune -o \
  -type f -name '*.sql' \( -path '*migrations*' -o -path '*/db/*' -o -path '*/supabase/*' \) -print 2>/dev/null \
  | grep -E '/([0-9]{3}|[0-9]{8}[a-z]?|[0-9]{14}|[0-9]{4}-[0-9]{2}-[0-9]{2})_[^/]*\.sql$' \
  | while IFS= read -r f; do grep -qiwE "$TABLE" "$f" && printf '%s\t%s\n' "$(when_of "$f")" "$f"; done \
  | sort -rn | cut -f2)"
if [ -z "$HITS" ]; then
  echo "(없음) → 처음 다루는 표다. 렌테일러 DB면 ~/projects/cadam/db (2026-11-15 결정), 그 밖의 사업 DB는 어느 폴더에 둘지 사장님께 묻는다."
  exit 0
fi
echo "$HITS" | head -10 | while IFS= read -r f; do printf '  [%s] %s\n' "$(biz_of "$(dirname "$f")")" "${f/#$ROOT/~/projects}"; done
echo ""

BIZES="$(echo "$HITS" | while IFS= read -r f; do biz_of "$(dirname "$f")"; done | sort -u)"
if [ "$(echo "$BIZES" | wc -l | tr -d ' ')" -gt 1 ]; then
  echo "⚠ 같은 이름의 표가 여러 사업 DB에 있다: $(echo $BIZES | tr ' ' ',')"
  echo "→ 어느 사업 DB의 표인지 먼저 확인한다(코드·작업 맥락, 모르면 사장님께). 렌테일러면 ~/projects/cadam/db, 그 밖은 그 사업의 최근 폴더."
  exit 0
fi
LAST_DIR="$(dirname "$(echo "$HITS" | head -1)")"
if [ "$BIZES" = rentailor ]; then
  # Owner decision 2026-11-15: all new rentailor DB migrations go directly under cadam/db.
  echo "→ 따를 폴더: ~/projects/cadam/db (렌테일러 DB는 2026-11-15부터 여기 한 곳 — 마지막 기록 위치: ${LAST_DIR/#$ROOT/~/projects})"
else
  echo "→ 따를 폴더: ${LAST_DIR/#$ROOT/~/projects} (가장 최근에 이 표를 다룬 곳)"
fi
