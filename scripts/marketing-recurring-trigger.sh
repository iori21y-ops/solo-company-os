#!/bin/bash
# ════════════════════════════════════════════════════════════════
# marketing-recurring-trigger.sh — 마케팅팀 주기 업무 자동 트리거
# ════════════════════════════════════════════════════════════════
# 역할: launchd 스케줄에 맞춰 broker task ledger에 마케팅 업무를 등록한다.
#       Discord는 결과 표시 UI로만 쓰고, 역할멘션으로 봇을 직접 깨우지 않는다.
# 사용법: marketing-recurring-trigger.sh {b|c|ping}
# 대상 주기:
#   b — 주기B: 신규 주제 발굴·선정 (매주 월요일, 게이트1 전까지만 자율)
#   c — 주기C: 발행 D+7 노출 측정·환류 (매일, 보고형·결재 없음)
# ※ 주기A(확정 발행계획 실행)는 schedule 트리거 대상 아님(trigger_source: content/self).
# 등록 근거: marketing/SKILL.md §주기 업무 3종 + process-marketing-task-list-20260602.md
# ════════════════════════════════════════════════════════════════
set -euo pipefail

TASK="${1:-}"
ENV_FILE="$HOME/.openclaw/workspace/claude-broker/.env"
MARKETING_ROLE="1510266153208119398"      # 마케팅 역할 ID
MARKETING_CHANNEL="1510444722433429514"   # 마케팅 채널 ID
LOG="$HOME/projects/_meta/logs/marketing-recurring-trigger.log"
ENQUEUE="$HOME/.openclaw/workspace/claude-broker/scripts/enqueue-task.mjs"

BOT_TOKEN=$(grep DISCORD_BOT_TOKEN "$ENV_FILE" 2>/dev/null | cut -d= -f2- | tr -d "'" | tr -d '"' | tr -d ' ')

ts() { date '+%Y-%m-%d %H:%M:%S'; }

case "$TASK" in
  b)
    # 주기B: 신규 주제 발굴·선정 (매주 월요일 자동 트리거)
    # 주의: 게이트1(Tier 판정 사람 승인) 직전까지만 자율 실행. 발행계획 확정은 사람 결재 대기.
    MSG="[주기 B] 신규 주제 발굴·선정 (주 1회 자동 트리거). **게이트1(Tier 판정) 직전까지 자율 실행 — 발행계획 확정은 사람 승인 필수.** 절차: ① marketing/raw/cycles/ 및 pending/approved/에서 이미 진행 중이거나 확정된 주제 목록 확인(중복 발굴 금지=멱등). ② 콘텐츠팀 approved/(팩트블록·스카우트 후보) + data approved/(최근 48시간 내 green verdict) 스캔. ③ 5질문 Tier 판정 수행 — Q1(검색수요)·Q2(사이트 연관성)·Q3(자사 차별점)·Q4(경쟁도)·Q5(발행 여력). ④ **대상 없거나 모든 후보가 이미 처리된 경우 조용히 종료(보고 불필요).** ⑤ 새 후보 있으면 Tier 판정 결과 + 추천 발행계획(초안) → raw/cycles/cadam/cycle-NNN-b-{슬러그}.md 개설 후 [APPROVAL:대표님] 결재카드 상신(게이트1). 결재 전 발행계획 확정 금지."
    ;;
  c)
    # 주기C: D+7 노출 측정·환류 (매일 자동 트리거)
    # 주의: 보고형 — 별도 결재 없음. 측정 결과는 채널에 직접 게시.
    MSG="[주기 C] 발행 D+7 노출 측정·환류 (매일 자동 트리거). **보고형 — 결재 없음. 측정 완료 후 채널에 직접 게시.** 절차: ① marketing/outputs/approved/ 및 raw/cycles/cadam/ 에서 발행일 기준 **정확히 7일(±1일 허용)** 이 된 cycle 파일 탐색. ② 해당 없으면 **조용히 종료(보고 불필요).** ③ 해당 있으면 cycle §5 노출 측정 기록 — 채널별 지표(조회·도달·노출; 전환·매출은 sales 영역 건드리지 않음). ④ 측정 기록 후 [CALL:데이터] 로 sales conversion-report 핸드오프 요청(다음 주기B Tier Q4 환류 소재). ⑤ cycle status: measured → archived 전이. **이 업무는 마케팅이 단독으로 완결 — 결재카드 상신 불필요.** 측정 완료 시 채널에 한 줄 요약 게시."
    ;;
  ping)
    # 테스트: 역할멘션 없이 채널에만 POST → 어떤 봇도 깨우지 않고 전송경로만 검증
    MSG="[스케줄러 설치 검증] marketing-recurring-trigger.sh task-ledger 등록 테스트"
    ;;
  *)
    echo "usage: $0 {b|c|ping}" >&2; exit 2
    ;;
esac

TASK_JSON=$(node "$ENQUEUE" --owner "마케팅" --origin-channel "$MARKETING_CHANNEL" --requester "scheduler" --kind "scheduled:$TASK" --instruction "$MSG")
echo "$(ts) [$TASK] OK task-ledger 등록: $TASK_JSON" | tee -a "$LOG"
