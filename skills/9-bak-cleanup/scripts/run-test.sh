#!/bin/bash
# 9-bak-cleanup self-test: uses a throwaway folder under the system temp dir only.
# Real ~/projects and ~/projects/_archive are never touched (roots overridden by env).
# The temp folder is left for the OS to clean (no rm -rf, global rule).
set -uo pipefail
cd "$(dirname "$0")"

TMP="$(mktemp -d)"
P="$TMP/projects"; A="$P/_archive"; L="$TMP/LaunchAgents"
mkdir -p "$P/demo/sub" "$P/_data/rentailor/backups" "$L"
export BAK_PROJECTS_ROOT="$P" BAK_ARCHIVE_ROOT="$A" BAK_LAUNCH_DIR="$L"

touch "$P/demo/real.txt" "$P/demo/real.txt.bak.20260101"          # original exists → move
touch "$P/demo/sub/a.py" "$P/demo/sub/a.py.bak"                    # nested → move, path kept
touch "$P/demo/orphan.txt.bak.20260101"                            # no original → keep
touch "$P/demo/config.json" "$P/demo/config.json.bak.20261105"     # secret-like → keep
touch "$P/demo/com.user.secondbrain.rss.plist" "$P/demo/com.user.secondbrain.rss.plist.bak.1"  # protected
touch "$P/demo/svc.sh" "$P/demo/svc.sh.bak"; echo "$P/demo/svc.sh.bak" > "$L/x.plist"           # launchd ref → keep
touch "$P/_data/rentailor/backups/db.sql" "$P/_data/rentailor/backups/db.sql.bak"               # data backups → keep

pass=0; fail=0
ok() { if eval "$2"; then echo "PASS: $1"; pass=$((pass+1)); else echo "FAIL: $1"; fail=$((fail+1)); fi; }

OUT="$(./cleanup.sh 2>&1)";            ok "인자 없음 거부" 'echo "$OUT" | grep -q 사용법'
OUT="$(./cleanup.sh "$HOME" 2>&1)";    ok "홈 거부" 'echo "$OUT" | grep -q 거부'
OUT="$(./cleanup.sh "$P" 2>&1)";       ok "projects 전체 거부" 'echo "$OUT" | grep -q 거부'
OUT="$(./cleanup.sh "$A" 2>&1)";       ok "보관함 안 거부" 'echo "$OUT" | grep -q 거부'

OUT="$(./cleanup.sh "$P/demo" 2>&1)"
ok "dry-run 표시" 'echo "$OUT" | grep -q DRY-RUN'
ok "dry-run은 아무것도 안 옮김" '[ -f "$P/demo/real.txt.bak.20260101" ] && [ ! -d "$A/$(date +%F)" ]'

OUT="$(./cleanup.sh "$P/demo" --run 2>&1)"
D="$A/$(date +%F)"
ok "원본 있는 .bak → 보관함으로 이동" '[ ! -e "$P/demo/real.txt.bak.20260101" ] && [ -f "$D/demo/real.txt.bak.20260101" ]'
ok "하위 경로 유지" '[ -f "$D/demo/sub/a.py.bak" ]'
ok "MOVED.txt에 2줄" '[ "$(wc -l < "$D/MOVED.txt" | tr -d " ")" = 2 ]'
ok "고아 .bak 보존" '[ -f "$P/demo/orphan.txt.bak.20260101" ]'
ok "config.json 백업 보존(비밀 가능)" '[ -f "$P/demo/config.json.bak.20261105" ]'
ok "secondbrain 보존" '[ -f "$P/demo/com.user.secondbrain.rss.plist.bak.1" ]'
ok "launchd가 가리키는 파일 보존" '[ -f "$P/demo/svc.sh.bak" ]'
ok "원본 파일 무손상" '[ -f "$P/demo/real.txt" ] && [ -f "$P/demo/sub/a.py" ]'
ok "rm 사용 안 함" '! grep -qE "^[^#]*\brm " cleanup.sh'

OUT="$(./cleanup.sh "$P/_data" --run 2>&1)"
ok "데이터 창고 backups 보존" '[ -f "$P/_data/rentailor/backups/db.sql.bak" ]'

echo ""
echo "=== 결과: PASS $pass / FAIL $fail (임시 폴더: $TMP, 실제 폴더 무손상) ==="
[ "$fail" = 0 ]
