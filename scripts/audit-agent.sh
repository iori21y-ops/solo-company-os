#!/bin/bash
# audit-agent.sh — 시스템 도메인 메타 감사 v1
# 설계 정본: ~/second-brain/wiki/system/감사-에이전트-설계.md
#
# "점검을 점검하는 자"(메타 감사). 개별 점검을 다시 돌리지 않고, 그 흔적(로그·산출물·지도)을
# 읽어 사각(거짓성공·무알림·로그정지·하트비트누락·중복알람·잔재·미커밋)을 매일 자동 포착한다.
#
# 2단계 구조(헬스체크와 동일 패턴):
#   1단계 = 결정론 쉘 판정(A1~A9), 항상 실행 / 2단계 = claude -p sonnet 리포트, 결함 있을 때만.
#
# launchd: com.cadam.audit, 매일 07:30 (헬스체크 07:00·사이트맵스캔 06:00 직후).
# 사용법: audit-agent.sh          (실운영: 발송·카드·상태기록 수행)
#         audit-agent.sh --dry-run (검증: 수집·판정·발송예정문구만 출력, 무발송·무카드·무상태기록)

export LANG=en_US.UTF-8
HOME="${HOME:-/Users/kim}"

DRY_RUN=false
[ "$1" = "--dry-run" ] && DRY_RUN=true

TS=$(date '+%Y-%m-%d %H:%M:%S')
TODAY=$(date '+%Y-%m-%d')
HOUR=$(date '+%H')
NOW=$(date +%s)
UIDN=$(id -u)

AUDIT_DIR="$HOME/projects/_meta/audit"
LOG="$AUDIT_DIR/audit.log"
STREAK="$AUDIT_DIR/audit-streak.txt"   # A1: "label count" (연속 실패 카운트)
SEEN="$AUDIT_DIR/audit-seen.txt"        # 카드 dedup: 미해결 결함키 목록(재카드 방지)
[ "$DRY_RUN" = false ] && mkdir -p "$AUDIT_DIR"

# ── 판정 노브(열린 결정 확정값) ─────────────────────────────
A1_STREAK_N=2       # A1: 예약잡 연속 실패 N회 이상이면 구조적 결함(외부 1회 장애 제외)
A4_CADENCE_MULT=15  # A4: mtime 정지 임계 = 주기 × 1.5 (정수연산 위해 ×10 스케일: 15/10)
A6_DUP_MAX=1        # A6: 동일 잡 하루 발신 이 값 초과(≥2)면 중복 의심

# 결함 누적: 한 줄 = "CODE|SEV|target|설명"
FINDINGS=""
add_finding(){ FINDINGS="${FINDINGS}$1"$'\n'; }

# ══════════════════════════════════════════════════════════════
# A1. 죽은 잡 탐지 — KeepAlive 상주 PID 없음(즉시) + 예약잡 연속 실패 N회
# ══════════════════════════════════════════════════════════════
# 상주(KeepAlive) 서비스: PID 없으면 죽음. (monitor·gpu-agent은 상주 아님 → 제외)
RESIDENT="com.rentailor.claude-broker com.cadam.erp com.cadam.clipserver com.rentailor.md-viewer com.cadam.naver ai.openclaw.gateway homebrew.mxcl.postgresql@18"
for L in $RESIDENT; do
  LINE=$(launchctl list 2>/dev/null | awk -v l="$L" '$3==l{print $1}')
  if [ -z "$LINE" ]; then
    add_finding "A1|high|$L|상주 서비스 LaunchAgent 미적재(launchctl 목록에 없음)"
  elif [ "$LINE" = "-" ]; then
    add_finding "A1|high|$L|상주(KeepAlive) 서비스인데 PID 없음 — 프로세스 죽음 의심"
  fi
done

# 예약잡: 마지막 종료코드 ≠0 이 연속 A1_STREAK_N 회 이상 → 구조적 실패
# (외부 일시장애 1회는 제외. 상태파일에 잡별 연속 실패수 영속)
SCHEDULED="com.cadam.gwp1-pipeline com.rentailor.recall-collect com.user.secondbrain.ingest com.cadam.kosis com.cadam.encar-crawler-v2 com.cadam.api-hub.ev-chargers com.cadam.api-hub.car-sales com.cadam.terms-monitor com.cadam.wp-sync"
read_streak(){ [ -f "$STREAK" ] && awk -v l="$1" '$1==l{print $2}' "$STREAK" | head -1 || true; }
NEW_STREAK=""
for L in $SCHEDULED; do
  ST=$(launchctl list 2>/dev/null | awk -v l="$L" '$3==l{print $2}')
  [ -z "$ST" ] && continue
  PREV=$(read_streak "$L"); PREV=${PREV:-0}
  # -15/143(SIGTERM)·0 은 성공/정상종료로 간주, 그 외 비영(1 등)은 실패
  if [ "$ST" = "0" ] || [ "$ST" = "-15" ] || [ "$ST" = "143" ]; then
    CUR=0
  else
    CUR=$((PREV + 1))
  fi
  NEW_STREAK="${NEW_STREAK}${L} ${CUR}"$'\n'
  if [ "$CUR" -ge "$A1_STREAK_N" ]; then
    add_finding "A1|med|$L|예약잡 연속 실패 ${CUR}회(종료코드 $ST) — 구조적 실패 의심"
  fi
done

# ══════════════════════════════════════════════════════════════
# A2. 거짓성공 탐지 — 성공 문자열 O 그러나 산출물 없음/mtime 안바뀜
# ══════════════════════════════════════════════════════════════
# 잡별 성공 기준선(성공 문자열 + 기대 산출물). 산출물 mtime이 오늘이 아니면 거짓성공.
# 형식: label|로그경로|성공정규식|산출물경로(mtime 오늘이어야)
mtime_epoch(){ [ -e "$1" ] && stat -f %m "$1" 2>/dev/null || echo 0; }
is_today(){ [ "$(date -r "$1" '+%Y-%m-%d' 2>/dev/null)" = "$TODAY" ]; }
check_false_success(){
  local label="$1" log="$2" ok_re="$3" artifact="$4"
  [ -f "$log" ] || return 0
  # 오늘 로그에 성공 문자열이 있는지(없으면 A2 대상 아님 — A3/A4가 다룸)
  if tail -60 "$log" 2>/dev/null | grep -Eq "$ok_re"; then
    if [ -n "$artifact" ] && [ -e "$artifact" ]; then
      if ! is_today "$artifact"; then
        add_finding "A2|high|$label|로그엔 성공인데 산출물 mtime이 오늘 아님($(date -r "$artifact" '+%m-%d %H:%M' 2>/dev/null)) — 거짓성공 의심"
      fi
    elif [ -n "$artifact" ]; then
      add_finding "A2|high|$label|로그엔 성공인데 기대 산출물 없음($artifact) — 거짓성공 의심"
    fi
  fi
}
BK="$HOME/projects/cadam/backups/$TODAY"
check_false_success "backup-cadam" "$HOME/projects/cadam/backups/backup.log" "백업 완료|백업 성공" "$BK"
# 주의(v1 한계): secondbrain.ingest 는 "처리할 파일 없음"도 정상 완료라 산출물 mtime 기준선이 불안정.
#   → ingest 는 A2에서 제외하고, "아예 안 돌았는지"는 A4(로그 정지)가 대신 커버한다. (성공기준선은 v2 과제)

# ══════════════════════════════════════════════════════════════
# A3. 무알림(silent) 탐지 — 잡 실패(exit≠0)인데 스크립트에 알림 발신 코드 없음
# ══════════════════════════════════════════════════════════════
# 형식: label|스크립트경로 — 종료코드≠0인데 스크립트가 notify_discord/tg_notify 미보유면 무알림 사각
check_silent(){
  local label="$1" script="$2"
  local st; st=$(launchctl list 2>/dev/null | awk -v l="$label" '$3==l{print $2}')
  [ -z "$st" ] && return 0
  [ "$st" = "0" ] || [ "$st" = "-15" ] || [ "$st" = "143" ] && return 0
  if [ -f "$script" ] && ! grep -Eq "notify_discord|tg_notify|sendDiscord|discord.com/api" "$script"; then
    add_finding "A3|med|$label|잡 실패(종료코드 $st)인데 스크립트에 알림 발신 경로 없음 — 무알림 사각"
  fi
}
check_silent "com.rentailor.recall-collect" "$HOME/projects/cadam/cadam-pipeline/scripts/recall/recall_collect.py"
check_silent "com.cadam.encar-crawler-v2" "$HOME/projects/cadam/cadam-n8n/scrape_encar.py"
check_silent "com.cadam.wp-sync" ""

# ══════════════════════════════════════════════════════════════
# A4. 로그 정지(frozen) — 로그 mtime이 주기×1.5 넘게 안 갱신
# ══════════════════════════════════════════════════════════════
# 형식: label|로그경로|주기초
check_frozen(){
  local label="$1" log="$2" cadence="$3"
  [ -f "$log" ] || { add_finding "A4|med|$label|로그 파일 없음($log) — 잡 미실행 의심"; return 0; }
  local m age limit
  m=$(mtime_epoch "$log"); age=$((NOW - m))
  limit=$(( cadence * A4_CADENCE_MULT / 10 ))
  if [ "$age" -gt "$limit" ]; then
    add_finding "A4|med|$label|로그 정지 — 마지막 갱신 $((age/3600))시간 전(임계 $((limit/3600))h 초과)"
  fi
}
check_frozen "secondbrain.ingest" "$HOME/second-brain/logs/cron.log" 86400
check_frozen "sitemap-scan"       "$HOME/projects/_meta/sitemap/scan.log" 86400
check_frozen "health-check"       "$HOME/projects/_meta/logs/health-check.log" 86400
check_frozen "secrets-drift"      "$HOME/.cadam-secrets/check-drift.log" 86400

# ══════════════════════════════════════════════════════════════
# A5. 하트비트 누락 — 당일 헬스체크 하트비트(heartbeat/ALL OK) 흔적 없음
# ══════════════════════════════════════════════════════════════
HC_LOG="$HOME/projects/_meta/logs/health-check.log"
if [ "$HOUR" -ge 8 ]; then   # 헬스체크 07:00 이후에만 판정(감사 07:30이면 통과)
  if [ -f "$HC_LOG" ] && grep -q "^\[$TODAY" "$HC_LOG" 2>/dev/null; then
    if ! grep -E "^\[$TODAY.*(heartbeat sent|ALL OK)" "$HC_LOG" >/dev/null 2>&1; then
      add_finding "A5|high|health-check|당일 헬스체크 기록은 있으나 하트비트/ALL OK 신호 없음"
    fi
  else
    add_finding "A5|high|health-check|당일($TODAY) 헬스체크 실행 흔적 없음 — 헬스체크 또는 알림 파이프라인 사망 의심"
  fi
fi

# ══════════════════════════════════════════════════════════════
# A6. 중복 알람 — 동일 잡 하루 발신 횟수 임계 초과
# ══════════════════════════════════════════════════════════════
DR_LOG="$HOME/projects/cadam/daily_report.log"
if [ -f "$DR_LOG" ]; then
  # daily_report.log 는 "요일 월 일 HH:MM:SS ... 전송 완료" 형식 → 오늘 발신 수 카운트
  DR_CNT=$(grep "$(date '+%b %e')" "$DR_LOG" 2>/dev/null | grep -c "전송 완료"); DR_CNT=${DR_CNT:-0}
  if [ "$DR_CNT" -gt "$A6_DUP_MAX" ]; then
    add_finding "A6|low|daily-report|오늘 리포트 ${DR_CNT}회 발신(임계 ${A6_DUP_MAX} 초과) — 중복/수동재실행 의심"
  fi
fi

# ══════════════════════════════════════════════════════════════
# A7. 잔재 파일 — .bak plist 잔존 (주 1회: 월요일에만 판정)
# ══════════════════════════════════════════════════════════════
if [ "$(date '+%u')" = "1" ]; then
  BAK_CNT=$(ls -1 "$HOME/Library/LaunchAgents/" 2>/dev/null | grep -c "\.bak"); BAK_CNT=${BAK_CNT:-0}
  if [ "$BAK_CNT" -gt 0 ]; then
    add_finding "A7|low|LaunchAgents|.bak plist 잔재 ${BAK_CNT}개 — 정리 필요"
  fi
fi

# ══════════════════════════════════════════════════════════════
# A8. 지도 노드 이상 — 인프라 스캔 결과 문제 노드 + 라우트 급변
# ══════════════════════════════════════════════════════════════
INFRA_JSON="$HOME/projects/_meta/sitemap/scan-infra-latest.json"
if [ -f "$INFRA_JSON" ]; then
  # summary에 strict 문제 수가 있으면 표기(설계상 판정 로직은 scan-map.js가 산출)
  PROB=$(msg="$INFRA_JSON" /usr/bin/python3 -c '
import json,os,sys
try:
    d=json.load(open(os.environ["msg"]))
except Exception:
    print(""); sys.exit()
s=d.get("summary",{})
probs=[n for n in d.get("nodes",[]) if str(n.get("judge",""))=="alert" and str(n.get("status","")) not in ("up","loaded","ok","n/a")]
print(len(probs))
' 2>/dev/null)
  if [ -n "$PROB" ] && [ "$PROB" -gt 0 ] 2>/dev/null; then
    add_finding "A8|med|sitemap-infra|인프라 지도 alert 노드 ${PROB}개 — 상태 이상"
  fi
fi
# 라우트 급변: 오늘 diff의 added+removed 합이 임계(30) 초과면 비정상 배포/삭제 의심
DIFF_JSON="$HOME/projects/_meta/sitemap/scan-diff-$(date '+%Y%m%d').json"
if [ -f "$DIFF_JSON" ]; then
  CHG=$(msg="$DIFF_JSON" /usr/bin/python3 -c 'import json,os;d=json.load(open(os.environ["msg"]));print(len(d.get("added",[]))+len(d.get("removed",[])))' 2>/dev/null)
  if [ -n "$CHG" ] && [ "$CHG" -gt 30 ] 2>/dev/null; then
    add_finding "A8|low|sitemap-route|오늘 라우트 변경 ${CHG}건(임계 30 초과) — 대량 배포/삭제 확인"
  fi
fi

# ══════════════════════════════════════════════════════════════
# A9. 미커밋 산출물 누적 (주 1회: 월요일) — 리마인드용, 알람 아님
# ══════════════════════════════════════════════════════════════
if [ "$(date '+%u')" = "1" ]; then
  UNCOMMITTED=$(git -C "$HOME/projects/_meta" status --short 2>/dev/null | grep -vc "^$"); UNCOMMITTED=${UNCOMMITTED:-0}
  if [ "$UNCOMMITTED" -gt 15 ]; then
    add_finding "A9|low|_meta|미커밋/미추적 파일 ${UNCOMMITTED}개 누적 — 커밋 여부 검토(리마인드)"
  fi
fi

# ══════════════════════════════════════════════════════════════
# 결과 처리
# ══════════════════════════════════════════════════════════════
FINDINGS=$(printf '%s' "$FINDINGS" | grep -v '^$' || true)
FCOUNT=$(printf '%s\n' "$FINDINGS" | grep -c '|'); FCOUNT=${FCOUNT:-0}

# 카드 생성 대상(조치필요): A1(high/med)·A2·A3·A4·A5. A6/A7/A8/A9는 요약만(리마인드).
actionable_line(){ echo "$1" | grep -Eq '^A1\||^A2\||^A3\||^A4\||^A5\|'; }

# 채널·토큰
SECRETS="$HOME/.cadam-secrets/secrets.env"
DASH_TOKEN=$(grep '^DASHBOARD_AUTH_TOKEN=' "$SECRETS" 2>/dev/null | head -1 | cut -d= -f2 | tr -d "\"' ")
ERP_URL="http://localhost:3001/api/tasks"

# ── 2단계: 요약 리포트 문구 작성 (결함 있으면 claude, 없으면 정형문) ──
if [ "$FCOUNT" -eq 0 ]; then
  SUMMARY="🔎 [감사] 이상 없음 (A1~A9 통과) — $TS"
else
  # 결함 목록 텍스트
  FLIST=$(printf '%s\n' "$FINDINGS" | awk -F'|' '{printf "  [%s/%s] %s: %s\n",$1,$2,$3,$4}')
  CLAUDE_BIN="/Users/kim/.local/bin/claude"
  ANALYSIS=""
  if [ "$DRY_RUN" = false ] && [ -x "$CLAUDE_BIN" ]; then
    PROMPT="너는 1인 기업 서버 감사팀장이다. 아래 시스템 감사 결함을 대표에게 보고하는 형식으로 2000자 이내 한국어로 요약하라. 형식: 한줄 종합판단(심각도) → 항목별(무엇을 놓쳤나→영향→권고). 감사 시각 $TS.
결함 목록:
$FLIST"
    ANALYSIS=$("$CLAUDE_BIN" -p "$PROMPT" --dangerously-skip-permissions --model sonnet 2>/dev/null | sed 's/\x1b\[[0-9;]*m//g')
  fi
  if [ -n "$ANALYSIS" ]; then
    SUMMARY="🔎 [감사] 결함 ${FCOUNT}건 — $TS"$'\n'"$ANALYSIS"
  else
    SUMMARY="🔎 [감사] 결함 ${FCOUNT}건 감지 — $TS"$'\n'"$FLIST"
  fi
fi

# ── dry-run: 출력만 ──
if [ "$DRY_RUN" = true ]; then
  echo "════════ 감사 에이전트 DRY-RUN ($TS) ════════"
  echo "[1단계 결정론 판정] 결함 ${FCOUNT}건"
  if [ "$FCOUNT" -gt 0 ]; then printf '%s\n' "$FINDINGS" | awk -F'|' '{printf "  - [%s/%s] %s: %s\n",$1,$2,$3,$4}'; else echo "  (없음 — A1~A9 통과)"; fi
  echo
  echo "[#시스템알림 발송 예정 문구]"
  echo "----------------------------------------"
  printf '%s\n' "$SUMMARY"
  echo "----------------------------------------"
  echo
  echo "[ERP 카드 생성 예정(조치필요 결함만, source=스팟·agent=관리팀장·status=배분대기)]"
  CARD_N=0
  while IFS= read -r f; do
    [ -z "$f" ] && continue
    if actionable_line "$f"; then
      CARD_N=$((CARD_N+1))
      code=$(echo "$f"|cut -d'|' -f1); tgt=$(echo "$f"|cut -d'|' -f3); desc=$(echo "$f"|cut -d'|' -f4)
      echo "  카드$CARD_N: title=[감사 $code] $tgt / instruction=$desc"
    fi
  done <<< "$FINDINGS"
  [ "$CARD_N" -eq 0 ] && echo "  (조치필요 결함 없음 → 카드 생성 안 함)"
  echo
  echo "[검증] dry-run: 실발송·카드생성·상태기록 모두 생략됨"
  exit 0
fi

# ── 실운영: 상태기록 + 요약발송 + 카드생성 ──
# A1 streak 영속
printf '%s' "$NEW_STREAK" > "$STREAK"

# (항상) 요약 1줄 발송 = 감사 생존 하트비트 겸용
source "$SECRETS" 2>/dev/null
source "$HOME/.cadam-secrets/notify_discord.sh"
notify_discord "$SUMMARY"

# (조치필요 결함만) 카드 생성 + dedup
touch "$SEEN"
NEW_SEEN=""
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if actionable_line "$f"; then
    code=$(echo "$f"|cut -d'|' -f1); tgt=$(echo "$f"|cut -d'|' -f3); desc=$(echo "$f"|cut -d'|' -f4)
    key="${code}:${tgt}"
    NEW_SEEN="${NEW_SEEN}${key}"$'\n'
    if grep -qxF "$key" "$SEEN" 2>/dev/null; then
      echo "[$TS] dedup skip $key (미해결 재카드 방지)" >> "$LOG"
      continue
    fi
    TITLE="[감사 $code] $tgt"
    TITLE=$(echo "$TITLE" | cut -c1-60)
    INSTR="[시스템 감사 자동생성] $desc  (근거: audit-agent.sh $code, $TS. 조치 후 결재 상신 요망.)"
    PAYLOAD=$(t="$TITLE" i="$INSTR" /usr/bin/python3 -c 'import json,os;print(json.dumps({"title":os.environ["t"],"agent":"관리팀장","source":"스팟","status":"배분대기","instruction":os.environ["i"]}))')
    HTTP=$(/usr/bin/curl -s -o /dev/null -w '%{http_code}' -X POST -H "x-dashboard-token: $DASH_TOKEN" -H "Content-Type: application/json" -d "$PAYLOAD" "$ERP_URL")
    echo "[$TS] card create $key → HTTP $HTTP" >> "$LOG"
  fi
done <<< "$FINDINGS"
# 해소된 결함은 seen에서 자동 제거(이번에 안 잡힌 키는 NEW_SEEN에 없음)
printf '%s' "$NEW_SEEN" | grep -v '^$' > "$SEEN" || true

echo "[$TS] audit done — findings=$FCOUNT" >> "$LOG"
