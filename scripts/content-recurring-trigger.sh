#!/bin/bash
# ════════════════════════════════════════════════════════════════
# content-recurring-trigger.sh — 콘텐츠팀 주기 업무 자동 트리거
# ════════════════════════════════════════════════════════════════
# 역할: launchd 스케줄에 맞춰 broker task ledger에 콘텐츠 업무를 등록한다.
#       Discord는 결과 표시 UI로만 쓰고, 역할멘션으로 봇을 직접 깨우지 않는다.
# 사용법: content-recurring-trigger.sh {c1|ping}
# 등록 근거: admin/outputs/approved/registry-콘텐츠팀-업무목록-20260602.md (CONT-01)
# ════════════════════════════════════════════════════════════════
set -euo pipefail

TASK="${1:-}"
ENV_FILE="$HOME/.openclaw/workspace/claude-broker/.env"
CONTENT_ROLE="1510282095539519673"     # 콘텐츠 역할 ID
CONTENT_CHANNEL="1510446872295379065"  # 콘텐츠 스레드 ID (parent: 컨텐츠-제작소)
LOG="$HOME/projects/_meta/logs/content-recurring-trigger.log"
ENQUEUE="$HOME/.openclaw/workspace/claude-broker/scripts/enqueue-task.mjs"

BOT_TOKEN=$(grep DISCORD_BOT_TOKEN "$ENV_FILE" 2>/dev/null | cut -d= -f2- | tr -d "'" | tr -d '"' | tr -d ' ')

ts() { date '+%Y-%m-%d %H:%M:%S'; }

case "$TASK" in
  c1)
    MSG="[주기 CONT-01] 팩트블록 생산 (일 1회 자동 트리거). **전제(불변): 미검증 데이터로 제작 금지.** 절차: ① ~/projects/_meta/agents/data/outputs/approved/에서 **최근 48시간 내 최신 green verdict-extraction**을 확인. ② 그 green 인사이트 중 **아직 팩트블록으로 만들지 않은 것만** 대상 — content/assets/cadam/index.md의 data_source와 대조해 **이미 처리한 verdict는 건너뛴다(중복 생산 금지=멱등).** ③ 대상이 없으면 **조용히 종료**(보고 불필요). ④ 대상이 있으면 fact-block 생산 — **한 번에 최대 3건까지만**(턴·시간 한도 보호). 나머지는 다음 실행으로 미루고 'N건 대기 중' 한 줄만 보고. 생산물은 content/assets/cadam/fact-blocks/ (프론트매터 topic·data_source·created·expires·used_in 필수) + content/outputs/pending/에 저장 후 [APPROVAL:대표님] 결재카드. 데이터 풀 대조 정확성 필수(틀리면 소스 통째 무효). 참고: GWP-1 라이브 유지 — 이 생산물은 이관 검증용이며 production 미배선." ;;
  ping)
    MSG="[스케줄러 설치 검증] content-recurring-trigger.sh task-ledger 등록 테스트" ;;
  *)
    echo "usage: $0 {c1|ping}" >&2; exit 2 ;;
esac

TASK_JSON=$(node "$ENQUEUE" --owner "콘텐츠" --origin-channel "$CONTENT_CHANNEL" --requester "scheduler" --kind "scheduled:$TASK" --instruction "$MSG")
echo "$(ts) [$TASK] OK task-ledger 등록: $TASK_JSON" | tee -a "$LOG"
