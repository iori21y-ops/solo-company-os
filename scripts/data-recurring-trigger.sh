#!/bin/bash
# ════════════════════════════════════════════════════════════════
# data-recurring-trigger.sh — 데이터팀 주기 업무 자동 트리거
# ════════════════════════════════════════════════════════════════
# 역할: launchd 스케줄에 맞춰 데이터 채널에 역할멘션 트리거 메시지를 POST.
#       broker가 멘션을 보고 데이터 봇을 깨워 해당 주기 업무를 수행시킨다.
# 새 메커니즘 아님 — health-check.sh의 Discord POST + broker [CALL:] 라우팅 재사용.
# 사용법: data-recurring-trigger.sh {a1|a2|a3|ping}
# 등록 근거: admin/outputs/approved/registry-데이터팀-업무목록-20260602.md (Part A)
# ════════════════════════════════════════════════════════════════
set -euo pipefail

TASK="${1:-}"
ENV_FILE="$HOME/.openclaw/workspace/claude-broker/.env"
DATA_ROLE="1510267413403275326"     # 데이터 역할 ID
DATA_CHANNEL="1510447003107070155"  # 데이터 채널 ID
LOG="$HOME/projects/_meta/logs/data-recurring-trigger.log"

BOT_TOKEN=$(grep DISCORD_BOT_TOKEN "$ENV_FILE" 2>/dev/null | cut -d= -f2- | tr -d "'" | tr -d '"' | tr -d ' ')

ts() { date '+%Y-%m-%d %H:%M:%S'; }

case "$TASK" in
  a1)
    MSG="<@&${DATA_ROLE}> [주기 A-1] 차량 공급 데이터 정합성 verdict (주 1회 자동 트리거). 입력: vehicles, pricing, vehicle_trims, trim_options, vehicle_msrp, vehicle_used_prices, finance_rates. audit-rules(referential/internal/semantic)+thresholds 적용. 산출: data/outputs/pending/verdict-supply-\$(date +%Y%m%d).md. 합격: 위반 0건·thresholds 내. 완료 후 [APPROVAL:관리팀장] 결재카드로 보고. green-all이면 경량 승인 대상. 이상 시만 즉시 알림." ;;
  a2)
    MSG="<@&${DATA_ROLE}> [주기 A-2] 사이트 표시 데이터 신선도 점검 (주 1회 자동 트리거). 입력: fuel_prices, ev_chargers, gas_stations, insurance_stats, repair_shops. freshness-thresholds 적용. 산출: data/outputs/pending/freshness-display-\$(date +%Y%m%d).md. 합격: 만료 0건. 완료 후 [APPROVAL:관리팀장] 결재카드로 보고. 만료 발견 시 항목·경과시간 명시." ;;
  a3)
    MSG="<@&${DATA_ROLE}> [주기 A-3] 크롤러 수집 결과 검증 (일 1회, 크롤 후 자동 트리거). 입력: info_articles 신규분. 점검: 건수 정상범위·중복/누락 이상치. **정상이면 조용히 종료(보고 불필요), 이상 시에만 즉시 알림 보고.** 수집 0건/중복 폭증 등은 탐지·flag만(재실행은 ops). 함께 A-4(환율·보조금·정책 변동) 가벼운 확인 — 변동 감지 시 스팟 수집 전환 제안만." ;;
  ping)
    # 테스트: 역할멘션 없이 채널에만 POST → 어떤 봇도 깨우지 않고 전송경로만 검증
    MSG="🔧 [스케줄러 설치 검증] data-recurring-trigger.sh 전송경로 테스트 메시지입니다. (역할멘션 없음 — 무시하세요)" ;;
  *)
    echo "usage: $0 {a1|a2|a3|ping}" >&2; exit 2 ;;
esac

if [ -z "$BOT_TOKEN" ]; then
  echo "$(ts) [$TASK] FAIL: BOT_TOKEN 비어있음" | tee -a "$LOG" >&2; exit 1
fi

PAYLOAD=$(printf '{"content":%s}' "$(printf '%s' "$MSG" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")

HTTP=$(curl -s -w '%{http_code}' -o /tmp/data-trigger-resp.json \
  -X POST \
  -H "Authorization: Bot $BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  "https://discord.com/api/v10/channels/${DATA_CHANNEL}/messages")

if [ "$HTTP" = "200" ] || [ "$HTTP" = "201" ]; then
  echo "$(ts) [$TASK] OK ($HTTP) 트리거 전송" | tee -a "$LOG"
else
  echo "$(ts) [$TASK] FAIL ($HTTP): $(cat /tmp/data-trigger-resp.json 2>/dev/null)" | tee -a "$LOG" >&2
  exit 1
fi
