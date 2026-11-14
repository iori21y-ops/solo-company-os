#!/bin/bash
# Restart a launchd service safely. Default is dry-run (read-only).
#   restart.sh <label>                      dry-run: show job type and the exact command
#   restart.sh <label> --run                restart an always-on service (KeepAlive)
#   restart.sh <label> --run-scheduled-now  scheduled job: run it ONCE NOW (side effects!)
# Restarting is an approval item (SAFETY_RULES section 1, cadam security.md 5.2):
# use --run / --run-scheduled-now only after the owner approved it in chat.
set -uo pipefail

LABEL="${1:-}"
MODE="${2:-}"
DOMAIN="gui/$(id -u)"
ALLOWED='^(com\.cadam\.|com\.blogengine\.|com\.kim\.|com\.rentailor\.|com\.solo\.|com\.user\.secondbrain\.)'

if [ -z "$LABEL" ]; then
  echo "사용법: restart.sh <정확한 라벨> [--run | --run-scheduled-now]"
  echo "예: restart.sh com.cadam.erp   (먼저 미리보기)"
  exit 2
fi
if ! echo "$LABEL" | grep -qE "$ALLOWED"; then
  echo "⛔ 거부: '$LABEL'는 우리 서비스 라벨이 아닙니다 (허용 접두어: com.cadam·blogengine·kim·rentailor·solo·user.secondbrain)."
  exit 1
fi

# Exact match only (a substring like com.cadam.naver would also hit naver-perf-*).
INFO="$(launchctl print "$DOMAIN/$LABEL" 2>/dev/null)"
if [ -z "$INFO" ]; then
  echo "⚠️  '$LABEL' 라벨이 정확히 일치하는 서비스가 없습니다 (꺼져 있거나 오타)."
  echo "비슷한 라벨:"
  launchctl list | awk 'NR>1{print $3}' | grep -F "$(echo "$LABEL" | sed -E 's/^com\.[a-z]+\.//; s/-.*//')" | sed 's/^/  /' || true
  exit 1
fi

PLIST="$(echo "$INFO" | awk -F' = ' '/^\tpath = /{print $2; exit}')"
PID="$(echo "$INFO" | awk -F' = ' '/^\tpid = /{print $2; exit}')"
has_key() { plutil -extract "$1" raw -o /dev/null "$PLIST" >/dev/null 2>&1 || plutil -extract "$1" xml1 -o /dev/null "$PLIST" >/dev/null 2>&1; }
KEEP="$(plutil -extract KeepAlive raw -o - "$PLIST" 2>/dev/null || (has_key KeepAlive && echo dict) || echo none)"

if [ "$KEEP" = "true" ] || [ "$KEEP" = "dict" ]; then
  TYPE="always"
  TYPE_TXT="상시 서비스 (KeepAlive) — 재시작해도 하는 일은 같음"
else
  TYPE="scheduled"
  WHEN=""
  has_key StartCalendarInterval && WHEN="정해진 시각(StartCalendarInterval)"
  has_key StartInterval && WHEN="$(plutil -extract StartInterval raw -o - "$PLIST")초마다(StartInterval)"
  has_key WatchPaths && WHEN="파일 변경 감시(WatchPaths)"
  TYPE_TXT="예약형 작업 — ${WHEN:-실행 조건 확인 필요}. kickstart는 '재시작'이 아니라 **지금 한 번 실행**이다 (글 발행·알림·DB 쓰기가 일어날 수 있음)"
fi

CMD=(launchctl kickstart -k "$DOMAIN/$LABEL")
echo "라벨: $LABEL"
echo "설정 파일: $PLIST"
echo "현재 PID: ${PID:-없음(대기 중)}"
echo "종류: $TYPE_TXT"
case "$LABEL" in
  com.cadam.erp) echo "참고: ERP 코드 변경 반영은 재시작이 아니라 web-engine/cadam-erp/scripts/deploy.sh (빌드 포함, 승인 필요)";;
esac
echo ""

run_it() {
  echo "▶ 실행: ${CMD[*]}"
  "${CMD[@]}" || { echo "❌ kickstart 실패"; exit 1; }
  sleep 2
  echo "▶ 실행 후:"
  launchctl print "$DOMAIN/$LABEL" 2>/dev/null | awk -F' = ' '/^\t(state|pid|last exit code) = /{print "  "$1" = "$2}'
}

case "$MODE" in
  --run)
    if [ "$TYPE" != "always" ]; then
      echo "⛔ 거부: 예약형 작업은 --run으로 실행하지 않습니다. 지금 한 번 돌리는 게 맞고 사장님이 승인했으면 --run-scheduled-now"
      exit 1
    fi
    run_it ;;
  --run-scheduled-now)
    if [ "$TYPE" != "scheduled" ]; then
      echo "⛔ 거부: 상시 서비스는 --run을 쓰세요."
      exit 1
    fi
    run_it ;;
  "")
    echo "[DRY-RUN] 실행될 명령: ${CMD[*]}"
    if [ "$TYPE" = "always" ]; then
      echo "[DRY-RUN] 사장님 승인 후: restart.sh $LABEL --run"
    else
      echo "[DRY-RUN] 예약형이라 보통 재시작이 필요 없다(다음 예약 시각에 새 코드로 돈다). 지금 한 번 돌려야 하면 사장님 승인 후: restart.sh $LABEL --run-scheduled-now"
    fi ;;
  *)
    echo "⛔ 알 수 없는 옵션: $MODE"; exit 2 ;;
esac
