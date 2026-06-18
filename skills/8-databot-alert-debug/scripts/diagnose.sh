#!/bin/bash
# 데이터봇 알림 디버그 런북 — 1~4단계를 한 번에 요약. 읽기 전용(로그 grep만).
set -uo pipefail

LOG="$HOME/.openclaw/workspace/claude-broker/broker.log"
ERRLOG="$HOME/.openclaw/workspace/claude-broker/broker.error.log"
N="${1:-15}"   # 각 항목 표시 줄 수 (기본 15)

if [ ! -f "$LOG" ]; then
  echo "FAIL: broker.log 없음 ($LOG). broker가 한 번이라도 떴는지 확인."
  exit 1
fi

echo "================ 데이터봇 알림 디버그 ================"
echo "로그: $LOG (최근 ${N}줄씩)"
echo ""

echo "=== 1. originChannelId 누락 (CALL→PING-FAIL) — 1순위 ==="
grep "CALL→PING-FAIL" "$LOG" | tail -n "$N" || true
grep -q "CALL→PING-FAIL" "$LOG" \
  && echo ">> originChannelId 누락 사례 있음. 해당 task가 #대표이사실 주입 경로를 탔는지 확인." \
  || echo ">> (PING-FAIL 기록 없음 — originChannelId 누락은 아닐 가능성)"
echo ""

echo "=== 2. CALL 분기 마커 ==="
grep -E "\[CALL→OPENCLAW-PING\]|\[CALL→TASK\]|\[CALL→PING-FAIL\]|\[CALL→FAIL\]|\[CALL-DEDUP\]" \
  "$LOG" | tail -n "$N" || echo "(CALL 마커 없음)"
echo ">> CALL→TASK는 일반 에이전트 정상 위임(멘션 아닌 카드+폴러). DEDUP은 5분내 중복 차단."
echo ""

echo "=== 3. 에스컬레이션(결재) 알림 ==="
grep -E "\[ESCALATE→APPROVAL\]|\[ESCALATE-FAIL\]" "$LOG" | tail -n "$N" || echo "(에스컬레이션 기록 없음)"
echo ""

echo "=== 4. broker 생존/에러 ==="
if launchctl list | grep -q claude-broker; then
  echo "PID: $(launchctl list | grep claude-broker | awk '{print $1}') (떠있음)"
else
  echo ">> ⚠️ claude-broker가 launchctl에 없음 — 죽었을 수 있음."
fi
echo "--- broker.error.log 최근 ${N}줄 ---"
[ -f "$ERRLOG" ] && tail -n "$N" "$ERRLOG" || echo "(에러로그 없음)"

echo ""
echo "================ 끝 (읽기 전용, 변경 0) ================"
