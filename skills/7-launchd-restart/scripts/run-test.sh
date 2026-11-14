#!/bin/bash
# 7-launchd-restart self-test: dry-run and refusal paths only. Never restarts anything.
set -uo pipefail
cd "$(dirname "$0")"

pass=0; fail=0
ok() { if eval "$2"; then echo "PASS: $1"; pass=$((pass+1)); else echo "FAIL: $1"; fail=$((fail+1)); fi; }

OUT="$(./restart.sh 2>&1)";                                ok "라벨 없음 → 사용법" 'echo "$OUT" | grep -q 사용법'
OUT="$(./restart.sh com.apple.Finder 2>&1)";               ok "남의 라벨 거부" 'echo "$OUT" | grep -q 거부'
OUT="$(./restart.sh com.cadam.nonexistent-fake 2>&1)";     ok "없는 라벨 경고" 'echo "$OUT" | grep -q "없습니다"'
OUT="$(./restart.sh com.cadam.nave 2>&1)";                 ok "부분 일치 라벨 거부(정확히 일치만)" 'echo "$OUT" | grep -q "없습니다"'

# Pick one loaded always-on and one scheduled label from the live list (read-only).
ALWAYS=""; SCHED=""
for L in $(launchctl list | awk 'NR>1 && $3 ~ /^com\.(cadam|blogengine|kim)\./{print $3}'); do
  O="$(./restart.sh "$L" 2>&1)"
  if [ -z "$ALWAYS" ] && echo "$O" | grep -q "상시 서비스"; then ALWAYS="$L"; fi
  if [ -z "$SCHED" ] && echo "$O" | grep -q "예약형 작업"; then SCHED="$L"; fi
  [ -n "$ALWAYS" ] && [ -n "$SCHED" ] && break
done
ok "상시 서비스 하나 찾음 ($ALWAYS)" '[ -n "$ALWAYS" ]'
ok "예약형 작업 하나 찾음 ($SCHED)" '[ -n "$SCHED" ]'

OUT="$(./restart.sh "$ALWAYS" 2>&1)";  ok "상시 dry-run 안내" 'echo "$OUT" | grep -q "DRY-RUN" && echo "$OUT" | grep -q -- "--run"'
OUT="$(./restart.sh "$SCHED" 2>&1)";   ok "예약형 dry-run 경고(지금 한 번 실행)" 'echo "$OUT" | grep -q "지금 한 번 실행"'
OUT="$(./restart.sh "$SCHED" --run 2>&1)";               ok "예약형에 --run 거부" 'echo "$OUT" | grep -q 거부'
OUT="$(./restart.sh "$ALWAYS" --run-scheduled-now 2>&1)"; ok "상시에 --run-scheduled-now 거부" 'echo "$OUT" | grep -q 거부'
OUT="$(./restart.sh "$ALWAYS" --bogus 2>&1)";            ok "모르는 옵션 거부" 'echo "$OUT" | grep -q "알 수 없는"'

echo ""
echo "=== 결과: PASS $pass / FAIL $fail (실제 재시작 0회) ==="
[ "$fail" = 0 ]
