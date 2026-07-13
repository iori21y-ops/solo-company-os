#!/bin/bash
# 서버 자동 점검 스크립트 — 문제 있을 때만 디스코드 알림
# 실행: launchd 매일 07:00

LOG_FILE="$HOME/projects/_meta/logs/health-check.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
PROBLEMS=""

# --- 1. 디스크 용량 (90% 이상 경고) ---
DISK_USAGE=$(df -H / | awk 'NR==2 {gsub(/%/,""); print $5}')
if [ "$DISK_USAGE" -ge 90 ]; then
  PROBLEMS="${PROBLEMS}🔴 디스크 ${DISK_USAGE}% 사용 중\n　→ docker system prune -a 또는 로그 정리 필요\n"
fi

# --- 2. 메모리 사용률 (90% 이상 경고) ---
MEM_PRESSURE=$(memory_pressure 2>/dev/null | grep "System-wide memory free percentage" | awk '{print $NF}' | tr -d '%')
if [ -n "$MEM_PRESSURE" ] && [ "$MEM_PRESSURE" -le 10 ]; then
  PROBLEMS="${PROBLEMS}🔴 메모리 여유 ${MEM_PRESSURE}%만 남음\n　→ 불필요 프로세스 종료 또는 Ollama 모델 언로드 필요\n"
fi

# --- 3. claude-broker 프로세스 ---
if ! pgrep -f "node src/main.js" > /dev/null 2>&1; then
  PROBLEMS="${PROBLEMS}🔴 claude-broker 프로세스 없음\n　→ 복구: launchctl kickstart gui/501/com.rentailor.claude-broker\n"
fi

# --- 4. OpenClaw 프로세스 ---
if ! pgrep -f "openclaw" > /dev/null 2>&1; then
  PROBLEMS="${PROBLEMS}🔴 OpenClaw(기획팀장) 프로세스 없음\n　→ 복구: launchctl kickstart gui/501/ai.openclaw.gateway\n"
fi

# --- 5. n8n Docker 컨테이너 ---
# launchd 스케줄: 23:00 기동 / 07:00 종료 → 07:00~22:59는 정상 종료 시간대이므로 체크 제외
HOUR=$(date '+%H')
N8N_ACTIVE_HOUR=false
if [ "$HOUR" -ge 23 ] || [ "$HOUR" -lt 7 ]; then
  N8N_ACTIVE_HOUR=true
fi
if [ "$N8N_ACTIVE_HOUR" = "true" ]; then
  if ! docker ps --format '{{.Names}}' 2>/dev/null | grep -qi "n8n"; then
    PROBLEMS="${PROBLEMS}🔴 n8n Docker 컨테이너 중지됨\n　→ 복구: docker start n8n\n"
  fi
fi

# --- 6. Ollama ---
if ! pgrep -f "ollama" > /dev/null 2>&1; then
  PROBLEMS="${PROBLEMS}🟡 Ollama 프로세스 없음\n　→ 복구: ollama serve &\n"
fi

# --- 7. Tailscale 연결 ---
TS_STATUS=$(tailscale status 2>/dev/null | head -1)
if [ $? -ne 0 ] || echo "$TS_STATUS" | grep -qi "stopped\|logged out"; then
  PROBLEMS="${PROBLEMS}🔴 Tailscale 연결 끊김\n　→ 복구: tailscale up\n"
fi

# --- 8. 포트 응답 (n8n 5678) ---
# launchd 스케줄 동일: 운영 시간대(23:00~06:59)에만 포트 체크
if [ "$N8N_ACTIVE_HOUR" = "true" ]; then
  if ! curl -s -o /dev/null -w '' --max-time 5 http://localhost:5678 > /dev/null 2>&1; then
    PROBLEMS="${PROBLEMS}🔴 n8n(5678) 포트 무응답\n　→ docker restart n8n 후 재확인\n"
  fi
fi
# --- 8-1. 월간 가격크롤러 수집 성공 검증 (매월 2~3일에만) ---
#   [2026-06-02 A안] 9722는 매월 1일 1회 실행 후 종료되는 배치 작업이므로 상시 포트 감시 제외.
#   대신 '이번 달 수집이 성공했는지'를 1일 다음(2~3일)에만 1회 검증한다.
DOM=$(date '+%d')
if [ "$DOM" = "02" ] || [ "$DOM" = "03" ]; then
  CRAWLER_LOG="$HOME/projects/cadam/cadam-n8n/price_crawler/crawler.log"
  THIS_MONTH=$(date '+%Y-%m')
  if [ ! -f "$CRAWLER_LOG" ]; then
    PROBLEMS="${PROBLEMS}🔴 가격크롤러 로그 없음 (이번 달 수집 미실행 의심)\n　→ 수동 실행: bash ~/projects/cadam/cadam-n8n/price_crawler/run_monthly.sh\n"
  else
    LOG_MONTH=$(date -r "$CRAWLER_LOG" '+%Y-%m')
    if [ "$LOG_MONTH" != "$THIS_MONTH" ] || ! tail -5 "$CRAWLER_LOG" | grep -q "월간 가격표 수집 끝"; then
      PROBLEMS="${PROBLEMS}🔴 이번 달(${THIS_MONTH}) 가격크롤러 월간 수집 실패/누락\n　→ 수동 실행: bash ~/projects/cadam/cadam-n8n/price_crawler/run_monthly.sh\n"
    fi
  fi
fi

# --- 9. LaunchAgent 상태 ---
for AGENT in com.rentailor.claude-broker; do
  if ! launchctl list 2>/dev/null | grep -q "$AGENT"; then
    PROBLEMS="${PROBLEMS}🔴 LaunchAgent ${AGENT} 미로드\n　→ 복구: launchctl load ~/Library/LaunchAgents/${AGENT}.plist\n"
  fi
done

# --- 10. broker 로그 최근 24시간 ERROR ---
BROKER_LOG="$HOME/.openclaw/workspace/claude-broker/logs"
if [ -d "$BROKER_LOG" ]; then
  ERROR_COUNT=$(find "$BROKER_LOG" -name "*.log" -mtime -1 -exec grep -ci "ERROR\|FATAL\|CRASH" {} + 2>/dev/null || echo 0)
  if [ "$ERROR_COUNT" -gt 0 ] 2>/dev/null; then
    PROBLEMS="${PROBLEMS}🟡 broker 로그에 ERROR ${ERROR_COUNT}건 (24h)\n　→ 로그 확인: tail -50 ~/.openclaw/workspace/claude-broker/logs/*.log | grep ERROR\n"
  fi
fi

# --- 11. rentailor.co.kr 접근 ---
HTTP_CODE=$(curl -sL -o /dev/null -w '%{http_code}' --max-time 10 https://rentailor.co.kr 2>/dev/null)
if [ "$HTTP_CODE" != "200" ]; then
  PROBLEMS="${PROBLEMS}🔴 rentailor.co.kr 응답 ${HTTP_CODE}\n　→ Vercel 대시보드 확인: https://vercel.com/dashboard\n"
fi

# --- 12. Docker 디스크 사용량 (10GB 이상 경고) ---
DOCKER_USAGE=$(docker system df --format '{{.Size}}' 2>/dev/null | head -1)
if echo "$DOCKER_USAGE" | grep -qiE "^[0-9]{2,}(\.[0-9]+)?GB"; then
  PROBLEMS="${PROBLEMS}🟡 Docker 디스크 ${DOCKER_USAGE} 사용 중\n　→ 정리: docker system prune -a\n"
fi

# --- 13. 로그 파일 크기 (100MB 이상 경고) ---
LARGE_LOGS=$(find "$HOME/projects/_meta" "$HOME/.openclaw" -name "*.log" -size +100M 2>/dev/null)
if [ -n "$LARGE_LOGS" ]; then
  PROBLEMS="${PROBLEMS}🟡 100MB 초과 로그 파일 발견\n　→ 확인: find ~/projects/_meta ~/.openclaw -name '*.log' -size +100M\n"
fi

# --- 결과 처리 ---
RESULTS_FILE="$HOME/projects/_meta/logs/health-check-latest.txt"
FIXES_FILE="$HOME/projects/_meta/logs/health-check-fixes.sh"

if [ -n "$PROBLEMS" ]; then
  # 1) 원시 데이터 저장
  echo -e "TIMESTAMP=$TIMESTAMP\n\n$PROBLEMS" > "$RESULTS_FILE"

  # 2) 복구 명령어만 별도 저장 (승인 시 실행용)
  echo -e "$PROBLEMS" | grep "→ 복구:" | sed 's/.*→ 복구: //' > "$FIXES_FILE"

  # 3) 봇 토큰 / 채널 준비
  BOT_TOKEN=$(grep DISCORD_BOT_TOKEN "$HOME/.openclaw/workspace/claude-broker/.env" 2>/dev/null | cut -d= -f2 | tr -d "'" | tr -d '"')
  # 죽은 HEALTH_CHECK_CHANNEL_ID → 시스템알림 채널(secrets.env)로 교체 (2026-07-12)
  CHANNEL_ID=$(grep '^DISCORD_SYSTEM_CHANNEL_ID=' "$HOME/.cadam-secrets/secrets.env" 2>/dev/null | head -1 | cut -d= -f2 | tr -d "'" | tr -d '"' | tr -d ' ')

  # 4) Claude에게 분석 요청
  PROMPT="너는 1인 기업의 서버 관리팀장이다. 아래 서버 점검 결과를 대표에게 보고하는 형식으로 작성해라.

형식:
📊 **종합 판단** (한줄 — 심각도 상/중/하)
📋 **항목별 분석** (각 항목: 문제 → 원인 추정 → 서비스 영향 → 권고 조치)
🔧 **즉시 복구 권고** (자동 복구 가능 항목 목록)

마지막에 반드시 이 문장 추가: '자동 복구를 진행하려면 **복구 승인**이라고 입력해주세요.'
2000자 이내로 작성해.

점검 시각: $TIMESTAMP
점검 결과:
$(echo -e "$PROBLEMS")"

  ANALYSIS=$(/Users/kim/.local/bin/claude -p "$PROMPT" --dangerously-skip-permissions --model sonnet 2>/dev/null | sed 's/\x1b\[[0-9;]*m//g')

  # 5) 분석 결과 디스코드 전송
  SENT=false
  if [ -n "$ANALYSIS" ] && [ -n "$BOT_TOKEN" ] && [ -n "$CHANNEL_ID" ]; then
    TMPFILE=$(mktemp)
    echo "$ANALYSIS" > "$TMPFILE"
    PAYLOAD=$(TMPFILE="$TMPFILE" python3 << 'PYEOF'
import json, os
with open(os.environ["TMPFILE"]) as f:
    content = f.read().strip()[:1900]
print(json.dumps({"content": content}))
PYEOF
    )
    rm -f "$TMPFILE"

    if [ -n "$PAYLOAD" ]; then
      HTTP=$(curl -s -w '%{http_code}' -o /dev/null \
        -H "Authorization: Bot $BOT_TOKEN" \
        -H "Content-Type: application/json" \
        -d "$PAYLOAD" \
        "https://discord.com/api/v10/channels/$CHANNEL_ID/messages")
      [ "$HTTP" = "200" ] && SENT=true
    fi
  fi

  # 6) 웹훅 fallback 제거 (2026-07-12) — 평문 웹훅 URL 폐기, 디스코드 봇 API로 단일화

  echo "[$TIMESTAMP] ALERT (bot=$SENT, claude=$( [ -n "$ANALYSIS" ] && echo true || echo false ))" >> "$LOG_FILE"
else
  # 정상 → 로그 + 하트비트 1회.
  #   '문제 시에만 알림' 구조는 알림 경로 자체가 죽어도 무음이라 '무소식=정상'을 검증할 수 없다.
  #   매일 1회 "정상 작동 중" 신호를 같은 시스템 채널로 보내 알림 파이프라인 생존까지 함께 확인한다.
  echo "[$TIMESTAMP] ALL OK" >> "$LOG_FILE"
  source "$HOME/.cadam-secrets/notify_discord.sh"
  notify_discord "💓 [서버 자동점검] 정상 작동 중 — 이상 없음 ($TIMESTAMP)"
  echo "[$TIMESTAMP] heartbeat sent" >> "$LOG_FILE"
fi
