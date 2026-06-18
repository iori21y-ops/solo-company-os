#!/usr/bin/env bash
# verify-distribute: 자동배분 결과 검증 (읽기 전용)
# 사용법: run-test.sh <부모카드_dashboardId>
# 판정: 1·2 (자식 생성 / parent_id 일치)
# ※ originChannelId 상속은 대시보드 API에 없는 필드라 여기서 검증 불가 → gotchas 참고

set -euo pipefail

PARENT_ID="${1:-}"
if [ -z "$PARENT_ID" ]; then
  echo "사용법: run-test.sh <부모카드_dashboardId>"
  echo "예: run-test.sh 58"
  exit 2
fi

# broker .env에서 토큰 로드 (값 출력 안 함)
ENV_FILE="$HOME/.openclaw/workspace/claude-broker/.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "FAIL: broker .env 없음 ($ENV_FILE)"
  exit 1
fi
TOKEN="$(grep '^DASHBOARD_AUTH_TOKEN=' "$ENV_FILE" | head -1 | cut -d= -f2-)"

API="http://localhost:3101/api/tasks"

# 대시보드 살아있는지 먼저 확인
if ! curl -sf -m 5 "$API" -H "x-dashboard-token: ${TOKEN}" -o /tmp/vd_tasks.json; then
  echo "FAIL: 대시보드(3101) 응답 없음. launchd com.cadam.dashboard 떠있는지 확인."
  echo "  확인: launchctl list | grep cadam"
  exit 1
fi

# jq 있는지
if ! command -v jq >/dev/null 2>&1; then
  echo "FAIL: jq 미설치. 'brew install jq' 후 재실행."
  exit 1
fi

# 부모의 자식들 추출 (parentId == PARENT_ID)
CHILDREN="$(jq -c --argjson pid "$PARENT_ID" \
  '.tasks | map(select(.parentId == $pid))' /tmp/vd_tasks.json)"
CHILD_COUNT="$(echo "$CHILDREN" | jq 'length')"

echo "=== verify-distribute: 부모 #${PARENT_ID} ==="
echo ""

# --- 판정 1: 자식 생성됐나 ---
if [ "$CHILD_COUNT" -ge 1 ]; then
  echo "[PASS] 1. 자식 카드 생성: ${CHILD_COUNT}개"
else
  echo "[FAIL] 1. 자식 카드 없음 — 배분이 안 돌았거나 다리 POST 실패"
  echo ""
  echo "=== 결과: FAIL (자식 없음) ==="
  exit 1
fi

# --- 판정 2: 각 자식의 parent_id 일치 ---
echo "$CHILDREN" | jq -c '.[]' | while read -r child; do
  CID="$(echo "$child" | jq -r '.id')"
  CPARENT="$(echo "$child" | jq -r '.parentId')"

  # 판정2: parent_id 일치
  if [ "$CPARENT" = "$PARENT_ID" ]; then
    echo "[PASS] 2. 자식 #${CID} parent_id 일치"
  else
    echo "[FAIL] 2. 자식 #${CID} parent_id=${CPARENT} (기대 ${PARENT_ID})"
  fi
done

echo ""
echo "=== 판정 완료 (위 PASS/FAIL 확인) ==="
echo "※ FAIL이 하나라도 있으면 배분 체인 점검 필요"
