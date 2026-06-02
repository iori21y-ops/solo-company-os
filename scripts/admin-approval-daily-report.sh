#!/bin/bash
# admin-approval-daily-report.sh — 관리팀장 익일 07:00 결재 요약 보고 트리거
set -euo pipefail

TASK="${1:-marketing}"
ENV_FILE="$HOME/.openclaw/workspace/claude-broker/.env"
ADMIN_ROLE="1510185782822830211"
CEO_USER="1471821518672756879"
MARKETING_CHANNEL="1510444722433429514"
LOG="$HOME/projects/_meta/logs/admin-approval-daily-report.log"

BOT_TOKEN=$(grep DISCORD_BOT_TOKEN "$ENV_FILE" 2>/dev/null | cut -d= -f2- | tr -d "'" | tr -d '"' | tr -d ' ')

ts() { date '+%Y-%m-%d %H:%M:%S'; }
yesterday() { date -v-1d '+%Y-%m-%d' 2>/dev/null || date -d 'yesterday' '+%Y-%m-%d'; }

case "$TASK" in
  marketing)
    CHANNEL="$MARKETING_CHANNEL"
    MSG="<@&${ADMIN_ROLE}> [익일 07:00 결재 요약 보고] #마케팅 스레드에서 어제($(yesterday)) 관리팀장이 대표결재로 진행했거나 결재받은 사안을 정리해 <@${CEO_USER}> 대표님께 보고하세요. 포함: 결재 제목, 승인/수정/반려/대기 상태, 결과물 링크·파일, 후속 액션, 오늘 대표님 결정이 필요한 항목. 없으면 '전일 결재 사안 없음'으로 짧게 보고."
    ;;
  ping)
    CHANNEL="$MARKETING_CHANNEL"
    MSG="🔧 [스케줄러 설치 검증] admin-approval-daily-report.sh 전송경로 테스트 메시지입니다. (역할멘션 없음 — 무시하세요)"
    ;;
  *)
    echo "usage: $0 {marketing|ping}" >&2
    exit 2
    ;;
esac

if [ -z "$BOT_TOKEN" ]; then
  echo "$(ts) [$TASK] FAIL: BOT_TOKEN 비어있음" | tee -a "$LOG" >&2
  exit 1
fi

PAYLOAD=$(printf '{"content":%s}' "$(printf '%s' "$MSG" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")

HTTP=$(curl -s -w '%{http_code}' -o /tmp/admin-approval-report-resp.json \
  -X POST \
  -H "Authorization: Bot $BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  "https://discord.com/api/v10/channels/${CHANNEL}/messages")

if [ "$HTTP" = "200" ] || [ "$HTTP" = "201" ]; then
  echo "$(ts) [$TASK] OK ($HTTP) 보고 트리거 전송" | tee -a "$LOG"
else
  echo "$(ts) [$TASK] FAIL ($HTTP): $(cat /tmp/admin-approval-report-resp.json 2>/dev/null)" | tee -a "$LOG" >&2
  exit 1
fi
