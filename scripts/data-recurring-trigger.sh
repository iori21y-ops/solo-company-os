#!/bin/bash
# ════════════════════════════════════════════════════════════════
# data-recurring-trigger.sh — 데이터팀 주기 업무 자동 트리거
# ════════════════════════════════════════════════════════════════
# 역할: launchd 스케줄에 맞춰 broker task ledger에 데이터 업무를 등록한다.
#       Discord는 결과 표시 UI로만 쓰고, 역할멘션으로 봇을 직접 깨우지 않는다.
# 사용법: data-recurring-trigger.sh {a1|a2|a3|a5|ping}
# 등록 근거: admin/outputs/approved/registry-데이터팀-업무목록-20260602.md (Part A)
# ════════════════════════════════════════════════════════════════
set -euo pipefail

TASK="${1:-}"
ENV_FILE="$HOME/.openclaw/workspace/claude-broker/.env"
DATA_ROLE="1510267413403275326"     # 데이터 역할 ID
DATA_CHANNEL="1510447003107070155"  # 데이터 채널 ID
LOG="$HOME/projects/_meta/logs/data-recurring-trigger.log"
ENQUEUE="$HOME/.openclaw/workspace/claude-broker/scripts/enqueue-task.mjs"

BOT_TOKEN=$(grep DISCORD_BOT_TOKEN "$ENV_FILE" 2>/dev/null | cut -d= -f2- | tr -d "'" | tr -d '"' | tr -d ' ')

ts() { date '+%Y-%m-%d %H:%M:%S'; }

case "$TASK" in
  a1)
    MSG="[주기 A-1] 차량 공급 데이터 정합성 verdict (주 1회 자동 트리거). 입력: vehicles, pricing, vehicle_trims, trim_options, vehicle_msrp, vehicle_used_prices, finance_rates. audit-rules(referential/internal/semantic)+thresholds 적용. 산출: data/outputs/pending/verdict-supply-\$(date +%Y%m%d).md. 합격: 위반 0건·thresholds 내. 완료 후 [APPROVAL:대표님] 결재카드로 보고. green-all이면 경량 승인 대상. 이상 시만 즉시 알림." ;;
  a2)
    MSG="[주기 A-2] 사이트 표시 데이터 신선도 점검 (주 1회 자동 트리거). 입력: fuel_prices, ev_chargers, gas_stations, insurance_stats, repair_shops. freshness-thresholds 적용. 산출: data/outputs/pending/freshness-display-\$(date +%Y%m%d).md. 합격: 만료 0건. 완료 후 [APPROVAL:대표님] 결재카드로 보고. 만료 발견 시 항목·경과시간 명시." ;;
  a3)
    MSG="[주기 A-3] 크롤러 수집 결과 검증 (일 1회, 크롤 후 자동 트리거). 입력: info_articles 신규분. 점검: 건수 정상범위·중복/누락 이상치. **정상이면 조용히 종료(보고 불필요), 이상 시에만 즉시 알림 보고.** 수집 0건/중복 폭증 등은 탐지·flag만(재실행은 ops). 함께 A-4(환율·보조금·정책 변동) 가벼운 확인 — 변동 감지 시 스팟 수집 전환 제안만." ;;
  a5)
    MSG="[주기 A-5/DATA-05] 추출 인사이트 정합성 게이트 (일 1회, 추출 배치 후 자동 트리거). 입력: insights 신규 추출분(vehicle_spec/pricing/market_trend — GWP-1 Gemini추출 산출). 점검: 추출 타입 스키마 정합·환각·중복 이상치·thresholds. **한 번에 최대 50건까지만 검증**(턴·시간 한도 보호), 초과분은 다음 회차로 미루고 'N건 미검증 대기' 명시. 산출: data/outputs/pending/verdict-extraction-\$(date +%Y%m%d).md (항목별 green/amber/red 분류). **신규 추출분 없으면 조용히 종료(보고 불필요, A-3 패턴).** 완료 후 [APPROVAL:대표님] 결재카드. green-all이면 경량 승인 대상. green 인사이트만 다운스트림(content CONT-01) 통과 전제. 참고: GWP-1 라이브 유지 — 이 verdict는 검증·게이트용이며 GWP-1 자체 curate/write와 병행." ;;
  ping)
    # 테스트: 역할멘션 없이 채널에만 POST → 어떤 봇도 깨우지 않고 전송경로만 검증
    MSG="[스케줄러 설치 검증] data-recurring-trigger.sh task-ledger 등록 테스트" ;;
  *)
    echo "usage: $0 {a1|a2|a3|a5|ping}" >&2; exit 2 ;;
esac

TASK_JSON=$(node "$ENQUEUE" --owner "데이터" --origin-channel "$DATA_CHANNEL" --requester "scheduler" --kind "scheduled:$TASK" --instruction "$MSG")
echo "$(ts) [$TASK] OK task-ledger 등록: $TASK_JSON" | tee -a "$LOG"
