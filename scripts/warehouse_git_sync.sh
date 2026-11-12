#!/bin/bash
# Weekly snapshot of the data warehouse git (~/projects/_data -> private GitHub iori21y-ops/data-warehouse).
# Only the hand-made small files allowed by ~/projects/_data/.gitignore are tracked (configs, manual link tables,
# promotions, brand kit) — photos, PDFs, databases and logs never are. Owner-approved 2026-11-13.
# launchd: com.solo.warehouse-git (Sundays 04:20). Alerts only when something fails.
export LANG=en_US.UTF-8
HOME=/Users/kim
WH="$HOME/projects/_data"
LOG="$WH/shared/work/warehouse-git/sync.log"
mkdir -p "$(dirname "$LOG")"
GIT=/usr/bin/git
log() { echo "$(date '+%F %T') $*" >> "$LOG"; }
fail() {
  log "FAIL: $*"
  source "$HOME/.cadam-secrets/notify_discord.sh"
  notify_discord "❌ 데이터 창고 git 주간 기록 실패: $* (로그 $LOG)"
  exit 1
}

cd "$WH" || fail "창고 폴더 없음"
$GIT rev-parse --git-dir >/dev/null 2>&1 || fail "창고 git 없음"
NAME=$($GIT -C "$HOME/projects/cadam" config user.name)
EMAIL=$($GIT -C "$HOME/projects/cadam" config user.email)

$GIT add -A || fail "git add"
if $GIT diff --cached --quiet; then
  log "no changes"
else
  N=$($GIT diff --cached --name-only | wc -l | tr -d ' ')
  $GIT -c user.name="$NAME" -c user.email="$EMAIL" commit -q -m "chore: weekly snapshot $(date +%F) ($N files)" || fail "git commit"
  log "committed $N files"
fi

# push (also retries anything an earlier failed run left behind)
if [ -n "$($GIT log origin/main..HEAD --oneline 2>/dev/null)" ]; then
  for i in 1 2 3 4; do
    $GIT push -q origin main 2>>"$LOG" && { log "pushed"; exit 0; }
    sleep $((i * 30))
  done
  fail "git push (4번 재시도)"
fi
log "up to date"
