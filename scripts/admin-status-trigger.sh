#!/bin/bash
# ════════════════════════════════════════════════════════════════
# admin-status-trigger.sh — 관리팀장 미결재 알림 트리거
# ════════════════════════════════════════════════════════════════
# 역할: 매일 09시 에이전트별 outputs/pending/ 스캔
#       → pending 0건이면 침묵, 1건 이상이면 결재 대기 목록 알림
# 변경 이력:
#   2026-06-09 초기(09·12·15·18·21 전체 다이제스트)
#   2026-06-09 개편 — 자동 다이제스트 해제, pending 건만 알림으로 축소
#              근거: 대표님 지시 (A안: 자동 알림 완전 해제 + 미결재건 보고 유지)
# ════════════════════════════════════════════════════════════════
set -euo pipefail

TASK="${1:-pending}"
ENV_FILE="$HOME/.openclaw/workspace/claude-broker/.env"
ADMIN_ROLE="1510185782822830211"          # 관리팀장 역할 ID
ADMIN_CHANNEL="1510306207573741719"       # 관리팀장실 채널 ID
AGENTS_DIR="$HOME/projects/_meta/agents"
LOG="$HOME/projects/_meta/logs/admin-status-trigger.log"

BOT_TOKEN=$(grep DISCORD_BOT_TOKEN "$ENV_FILE" 2>/dev/null | cut -d= -f2- | tr -d "'" | tr -d '"' | tr -d ' ')

ts() { date '+%Y-%m-%d %H:%M:%S'; }

case "$TASK" in
  pending)
    # pending 파일 수집
    PENDING_LIST=""
    TOTAL=0
    for agent_dir in "$AGENTS_DIR"/*/outputs/pending/; do
      [ -d "$agent_dir" ] || continue
      FILES=$(find "$agent_dir" -maxdepth 1 -type f -name "*.md" | sort)
      [ -z "$FILES" ] && continue
      AGENT_NAME=$(echo "$agent_dir" | sed 's|.*/agents/\([^/]*\)/outputs/pending/|\1|')
      COUNT=$(echo "$FILES" | wc -l | tr -d ' ')
      TOTAL=$((TOTAL + COUNT))
      while IFS= read -r f; do
        FNAME=$(basename "$f")
        PENDING_LIST="${PENDING_LIST}\n  • [${AGENT_NAME}] ${FNAME}"
      done <<< "$FILES"
    done

    if [ "$TOTAL" -eq 0 ]; then
      echo "$(ts) [pending] 미결재 0건 — 침묵" | tee -a "$LOG"
      exit 0
    fi

    MSG="<@&${ADMIN_ROLE}> [미결재 알림] 결재 대기 **${TOTAL}건** — 검토 바랍니다.$(printf '%b' "$PENDING_LIST")"
    ;;
  ping)
    # 테스트: 역할멘션 없이 채널에만 POST
    MSG="[스케줄러 설치 검증] admin-status-trigger.sh 전송경로 테스트 메시지입니다. (역할멘션 없음 — 무시하세요)"
    ;;
  *)
    echo "usage: $0 {pending|ping}" >&2; exit 2
    ;;
esac

if [ -z "$BOT_TOKEN" ]; then
  echo "$(ts) [$TASK] FAIL: BOT_TOKEN 비어있음" | tee -a "$LOG" >&2; exit 1
fi

PAYLOAD=$(printf '{"content":%s}' "$(printf '%s' "$MSG" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")

HTTP=$(curl -s -w '%{http_code}' -o /tmp/admin-trigger-resp.json \
  -X POST \
  -H "Authorization: Bot $BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  "https://discord.com/api/v10/channels/${ADMIN_CHANNEL}/messages")

if [ "$HTTP" = "200" ] || [ "$HTTP" = "201" ]; then
  echo "$(ts) [$TASK] OK ($HTTP) 전송" | tee -a "$LOG"
else
  echo "$(ts) [$TASK] FAIL ($HTTP): $(cat /tmp/admin-trigger-resp.json 2>/dev/null)" | tee -a "$LOG" >&2
  exit 1
fi
