#!/bin/bash
# 5-new-migration self-test: builds fake migration folders under the system temp dir.
# Never touches a database or the real ~/projects (root overridden by env).
set -uo pipefail
cd "$(dirname "$0")"
TMP="$(mktemp -d)"; P="$TMP/projects"; export MIG_PROJECTS_ROOT="$P"
mkdir -p "$P/a/db/migrations" "$P/b/db/migrations" "$P/c/supabase/migrations" "$P/d/db/migrations" "$P/a/docs"
touch "$P/a/db/migrations/20261024_trend_keywords.sql" "$P/a/db/migrations/20261024_trend_keywords_rollback.sql"
touch "$P/b/db/migrations/005_x.sql" "$P/b/db/migrations/006_brand_policy.sql"
touch "$P/c/supabase/migrations/20261113120000_erp.sql"
echo "alter table public.shorts_plans add column x text;" > "$P/a/db/migrations/20261112_shorts_plans_key.sql"
echo "create table public.shorts_plans (id int);" > "$P/c/supabase/migrations/20260101000000_old.sql"

pass=0; fail=0
ok() { if eval "$2"; then echo "PASS: $1"; pass=$((pass+1)); else echo "FAIL: $1"; fail=$((fail+1)); fi; }

OUT="$(./new.sh 2>&1)";                                   ok "인자 없음 → 사용법" 'echo "$OUT" | grep -q 사용법'
OUT="$(./new.sh "$P/a/db/migrations" Bad-Name 2>&1)";     ok "이름 규칙 위반 거부" 'echo "$OUT" | grep -q 거부'
OUT="$(./new.sh "$P/a/docs" add_x 2>&1)";                 ok "migrations 아닌 폴더 거부" 'echo "$OUT" | grep -q 거부'
OUT="$(./new.sh "$TMP" add_x 2>&1)";                      ok "~/projects 밖 거부" 'echo "$OUT" | grep -q 거부'
OUT="$(./new.sh "$P/zz/migrations" add_x 2>&1)";          ok "없는 폴더 거부(새로 안 만듦)" 'echo "$OUT" | grep -q 거부 && [ ! -d "$P/zz" ]'

./new.sh "$P/a/db/migrations" add_y >/dev/null 2>&1
D="$(date +%Y%m%d)"
ok "날짜형 폴더 → YYYYMMDD_ 본파일" '[ -f "$P/a/db/migrations/${D}_add_y.sql" ]'
ok "롤백 파일 같이 생김" '[ -f "$P/a/db/migrations/${D}_add_y_rollback.sql" ]'
ok "머리말 필수 칸(대상 DB·승인·백업·롤백·적용)" 'for k in "대상 DB" 승인 백업 롤백 적용; do grep -q "$k" "$P/a/db/migrations/${D}_add_y.sql" || exit 1; done'
ok "트랜잭션으로 감쌈" 'grep -q "^begin;" "$P/a/db/migrations/${D}_add_y.sql" && grep -q "^commit;" "$P/a/db/migrations/${D}_add_y.sql"'
ok "실행되는 DROP 줄 없음(주석만)" '! grep -hiE "^[^-]*\bdrop\b" "$P/a/db/migrations/${D}_add_y.sql" "$P/a/db/migrations/${D}_add_y_rollback.sql"'
OUT="$(./new.sh "$P/a/db/migrations" add_y 2>&1)";        ok "같은 이름 덮어쓰기 거부" 'echo "$OUT" | grep -q "이미 있음"'

./new.sh "$P/b/db/migrations" add_z >/dev/null 2>&1;      ok "번호형 폴더 → 다음 번호 007_" '[ -f "$P/b/db/migrations/007_add_z.sql" ]'
./new.sh "$P/c/supabase/migrations" add_w >/dev/null 2>&1; ok "타임스탬프형 폴더 → 14자리" 'ls "$P/c/supabase/migrations" | grep -qE "^[0-9]{14}_add_w\.sql$"'

OUT="$(./find.sh shorts_plans 2>&1)";  ok "find: 가장 최근에 표를 다룬 폴더 제시" 'echo "$OUT" | grep -q "따를 폴더: ~/projects/a/db/migrations"'

# Plain db/ folder (like cadam/db/) newer than the migrations/ subfolder; dumps and create scripts ignored.
echo "alter table public.erp_tasks add column a int;" > "$P/a/db/migrations/20260709_erp_tasks_a.sql"
echo "revoke select on public.erp_tasks from anon;"  > "$P/a/db/20261022_erp_tasks_drop_public_read.sql"
echo "create table public.erp_tasks (id int);"       > "$P/a/db/erp_tasks_create.sql"
echo "-- dump erp_tasks"                              > "$P/a/db/db_backup_20261201.sql"
OUT="$(./find.sh erp_tasks 2>&1)"
ok "find: db/ 바로 아래 파일도 찾음(더 최근)" 'echo "$OUT" | grep -q "따를 폴더: ~/projects/a/db (" && echo "$OUT" | grep -q 20261022_erp_tasks'
ok "find: 덤프·이름 없는 create 스크립트는 제외" '! echo "$OUT" | grep -qE "db_backup|erp_tasks_create"'
./new.sh "$P/a/db" add_v >/dev/null 2>&1
ok "new: db/ 폴더 허용 + 날짜형(이름 없는 파일 무시)" '[ -f "$P/a/db/$(date +%Y%m%d)_add_v.sql" ]'
OUT="$(./find.sh no_such_table 2>&1)"; ok "find: 처음 다루는 표면 사장님께 묻기" 'echo "$OUT" | grep -q "사장님께 묻는다"'
OUT="$(./find.sh 'x;rm' 2>&1)";        ok "find: 이상한 이름 거부" 'echo "$OUT" | grep -q 사용법'

echo ""
echo "=== 결과: PASS $pass / FAIL $fail (임시 폴더: $TMP, DB·실제 폴더 무손상) ==="
[ "$fail" = 0 ]
