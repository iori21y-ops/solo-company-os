#!/bin/bash
# ════════════════════════════════════════════════════════════════
# content-recurring-trigger.sh — 콘텐츠팀 주기 업무 자동 트리거
# ════════════════════════════════════════════════════════════════
# 역할: launchd 스케줄에 맞춰 콘텐츠 스레드에 역할멘션 트리거 메시지를 POST.
#       broker가 멘션을 보고 콘텐츠 봇을 깨워 해당 주기 업무를 수행시킨다.
# 새 메커니즘 아님 — data-recurring-trigger.sh와 동일 패턴(Discord POST + broker 라우팅).
# 사용법: content-recurring-trigger.sh {c1|ping}
# 등록 근거: admin/outputs/approved/registry-콘텐츠팀-업무목록-20260602.md (CONT-01)
# ════════════════════════════════════════════════════════════════
set -euo pipefail

TASK="${1:-}"
ENV_FILE="$HOME/.openclaw/workspace/claude-broker/.env"
CONTENT_ROLE="1510282095539519673"     # 콘텐츠 역할 ID
CONTENT_CHANNEL="1510446872295379065"  # 콘텐츠 스레드 ID (parent: 컨텐츠-제작소)
LOG="$HOME/projects/_meta/logs/content-recurring-trigger.log"

BOT_TOKEN=$(grep DISCORD_BOT_TOKEN "$ENV_FILE" 2>/dev/null | cut -d= -f2- | tr -d "'" | tr -d '"' | tr -d ' ')

ts() { date '+%Y-%m-%d %H:%M:%S'; }

case "$TASK" in
  c1)
    MSG="<@&${CONTENT_ROLE}> [주기 CONT-01] 팩트블록 생산 (일 1회 자동 트리거). **전제(불변): 미검증 데이터로 제작 금지.** 절차: ① ~/projects/_meta/agents/data/outputs/approved/에서 **최근 48시간 내 최신 green verdict-extraction**을 확인. ② 그 green 인사이트 중 **아직 팩트블록으로 만들지 않은 것만** 대상 — content/assets/cadam/index.md의 data_source와 대조해 **이미 처리한 verdict는 건너뛴다(중복 생산 금지=멱등).** ③ 대상이 없으면 **조용히 종료**(보고 불필요). ④ 대상이 있으면 fact-block 생산 — **한 번에 최대 3건까지만**(턴·시간 한도 보호). 나머지는 다음 실행으로 미루고 'N건 대기 중' 한 줄만 보고. 생산물은 content/assets/cadam/fact-blocks/ (프론트매터 topic·data_source·created·expires·used_in 필수) + content/outputs/pending/에 저장 후 [APPROVAL:관리팀장] 결재카드. 데이터 풀 대조 정확성 필수(틀리면 소스 통째 무효). 참고: GWP-1 라이브 유지 — 이 생산물은 이관 검증용이며 production 미배선." ;;
  ping)
    # 테스트: 역할멘션 없이 채널에만 POST → 어떤 봇도 깨우지 않고 전송경로만 검증
    MSG="🔧 [스케줄러 설치 검증] content-recurring-trigger.sh 전송경로 테스트 메시지입니다. (역할멘션 없음 — 무시하세요)" ;;
  *)
    echo "usage: $0 {c1|ping}" >&2; exit 2 ;;
esac

if [ -z "$BOT_TOKEN" ]; then
  echo "$(ts) [$TASK] FAIL: BOT_TOKEN 비어있음" | tee -a "$LOG" >&2; exit 1
fi

PAYLOAD=$(printf '{"content":%s}' "$(printf '%s' "$MSG" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')")

HTTP=$(curl -s -w '%{http_code}' -o /tmp/content-trigger-resp.json \
  -X POST \
  -H "Authorization: Bot $BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" \
  "https://discord.com/api/v10/channels/${CONTENT_CHANNEL}/messages")

if [ "$HTTP" = "200" ] || [ "$HTTP" = "201" ]; then
  echo "$(ts) [$TASK] OK ($HTTP) 트리거 전송" | tee -a "$LOG"
else
  echo "$(ts) [$TASK] FAIL ($HTTP): $(cat /tmp/content-trigger-resp.json 2>/dev/null)" | tee -a "$LOG" >&2
  exit 1
fi
