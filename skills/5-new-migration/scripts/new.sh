#!/bin/bash
# Create a migration SQL file + its rollback file in an existing migrations folder,
# following that folder's naming pattern. Writes files only — never touches a database.
#   new.sh <migrations folder> <verb_target>     e.g. new.sh ~/projects/cadam/db/migrations add_naver_url_to_shorts_plans
set -uo pipefail
DIR="${1:-}"
NAME="${2:-}"
ROOT="${MIG_PROJECTS_ROOT:-$HOME/projects}"

if [ -z "$DIR" ] || [ -z "$NAME" ]; then
  echo "사용법: new.sh <migrations 폴더> <동사_대상(영어 소문자·_)>"; exit 2
fi
if ! echo "$NAME" | grep -qE '^[a-z][a-z0-9_]*$'; then
  echo "⛔ 거부: 이름은 영어 소문자·숫자·_ 만 (snake_case)"; exit 1
fi
DIR="${DIR/#\~/$HOME}"
[ -d "$DIR" ] || { echo "⛔ 거부: 폴더 없음 '$DIR' (새 폴더는 만들지 않는다)"; exit 1; }
DIR="$(cd "$DIR" && pwd -P)"; ROOT_REAL="$(cd "$ROOT" && pwd -P)"
case "$DIR/" in "$ROOT_REAL"/*) ;; *) echo "⛔ 거부: ~/projects 안이 아님"; exit 1;; esac
case "$DIR" in *migrations*|*/db) ;; *) echo "⛔ 거부: 마이그레이션 폴더가 아님 (…/migrations 또는 …/db 만)"; exit 1;; esac
case "$DIR" in */_archive/*|*/_wt-*) echo "⛔ 거부: 보관함·작업 사본 폴더"; exit 1;; esac

# Detect the folder's naming pattern from its newest main (non-rollback) file.
LATEST="$(ls "$DIR" 2>/dev/null | grep -E '^[0-9][0-9a-z-]*_.*\.sql$' | grep -v '_rollback' | sort | tail -1)"
if echo "$LATEST" | grep -qE '^[0-9]{3}_'; then
  N=$((10#${LATEST:0:3} + 1)); PREFIX="$(printf '%03d' "$N")"
elif echo "$LATEST" | grep -qE '^[0-9]{14}_'; then
  PREFIX="$(date +%Y%m%d%H%M%S)"
else
  PREFIX="$(date +%Y%m%d)"   # YYYYMMDD_ (cadam/db/migrations style) or empty folder
fi
MAIN="$DIR/${PREFIX}_${NAME}.sql"
BACK="$DIR/${PREFIX}_${NAME}_rollback.sql"
for f in "$MAIN" "$BACK"; do [ -e "$f" ] && { echo "⛔ 거부: 이미 있음 $f"; exit 1; }; done

TODAY="$(date +%F)"
cat > "$MAIN" <<EOF
-- ${TODAY}: ${NAME} — <무엇을 왜 바꾸나, 한두 줄>
-- 대상 DB: <운영 Supabase(사이트·ERP) / 로컬 PostgreSQL / 기타 — 확인한 근거>
-- 승인: <사장님 승인 날짜·Linear REN-N> (승인 전에는 적용하지 않는다)
-- 백업: <적용 직전 바뀌는 표를 ~/projects/_data/<사업>/backups/manual/ 에 내보낸 파일 경로·행 수>
-- 롤백: $(basename "$BACK")
-- 적용: 승인 후 MCP 또는 Management API로 (SAFETY_RULES §3: 지금 상태 → 요약 → 되돌리는 법 → 승인 → 재조회)

begin;

-- 멱등(다시 돌려도 안전)·비파괴(기존 컬럼·데이터 유지)로 쓴다. 예:
-- alter table public.<표> add column if not exists <컬럼> text;
-- comment on column public.<표>.<컬럼> is '<설명>';

commit;
EOF
cat > "$BACK" <<EOF
-- 롤백: $(basename "$MAIN")
-- DROP TABLE·TRUNCATE는 금지 — 그런 되돌리기가 필요하면 주석으로만 남기고 사장님 판단 (cadam security.md §5.1).
-- DROP COLUMN은 데이터가 사라지므로 실행 전 백업 확인 + 추가 경고.

begin;

-- alter table public.<표> drop column if exists <컬럼>;   -- ⚠ 데이터 삭제: 백업 확인 후

commit;
EOF
echo "📝 만듦: $MAIN"
echo "📝 만듦: $BACK"
echo "→ <...> 칸을 채우고, 사장님께 SQL과 영향 범위를 보여 준 뒤 승인을 받는다. 이 스크립트는 DB에 아무것도 하지 않았다."
