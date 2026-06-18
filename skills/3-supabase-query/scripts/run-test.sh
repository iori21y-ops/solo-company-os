#!/bin/bash
# query.py의 _guard를 직접 호출해 위험 SQL 차단 + SELECT 통과 검증
cd "$(dirname "$0")"
PASS=0; FAIL=0
check() {  # $1=SQL  $2=expect(allow|block)
  python3 -c "
import sys; sys.argv=['x']
import importlib.util
spec=importlib.util.spec_from_file_location('q','query.py')
m=importlib.util.module_from_spec(spec)
# _load_env가 .env 없어도 죽지 않게: spec 로드 전 더미 환경
import os; os.environ.setdefault('SUPABASE_PROJECT_REF','x'); os.environ.setdefault('SUPABASE_ACCESS_TOKEN','x')
spec.loader.exec_module(m)
try:
    m._guard('''$1'''); print('ALLOW')
except SystemExit:
    print('BLOCK')
" 2>/dev/null
}
test_one() {
  r=$(check "$1" "$2")
  if [ "$r" = "$2" ]; then echo "PASS [$2] $1"; PASS=$((PASS+1));
  else echo "FAIL (got $r, want $2) $1"; FAIL=$((FAIL+1)); fi
}
test_one "SELECT * FROM erp_tasks" "ALLOW"
test_one "WITH t AS (SELECT 1) SELECT * FROM t" "ALLOW"
test_one "DROP TABLE erp_tasks" "BLOCK"
test_one "DELETE FROM erp_tasks" "BLOCK"
test_one "SELECT 1; DROP TABLE erp_tasks" "BLOCK"
test_one "UPDATE erp_tasks SET x=1" "BLOCK"
test_one "INSERT INTO erp_tasks VALUES (1)" "BLOCK"
echo "=== PASS=$PASS FAIL=$FAIL ==="
