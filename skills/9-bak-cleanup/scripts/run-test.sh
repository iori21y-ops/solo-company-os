#!/bin/bash
# 9-bak-cleanup 검증: 실제 삭제 없이 가드 동작 확인
set -uo pipefail
cd "$(dirname "$0")"

# 임시 테스트 폴더 구성
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

touch "$TMP/real.txt"                          # 원본
touch "$TMP/real.txt.bak.20260101"             # 원본 있는 .bak (삭제 대상)
touch "$TMP/orphan.txt.bak.20260101"           # 원본 없는 .bak (보존)
touch "$TMP/com.user.secondbrain.rss.plist.bak.20260101"  # 보호 대상

echo "=== TEST 1: 인자 없이 → 거부 ==="
OUT="$(./cleanup.sh 2>&1 || true)"
echo "$OUT" | grep -q "사용법" && echo "PASS: 인자없음 거부" || echo "FAIL"

echo ""
echo "=== TEST 2: 홈 전역 → 거부 ==="
OUT="$(./cleanup.sh "$HOME" 2>&1 || true)"
echo "$OUT" | grep -q "거부" && echo "PASS: 홈 전역 거부" || echo "FAIL"

echo ""
echo "=== TEST 3: dry-run → 삭제 0회, 보호 동작 ==="
OUT="$(./cleanup.sh "$TMP" 2>&1 || true)"
echo "$OUT" | grep -q "DRY-RUN" && echo "PASS: dry-run 모드" || echo "FAIL"
echo "$OUT" | grep -q "배제(보호).*secondbrain" && echo "PASS: secondbrain 보호" || echo "FAIL"
echo "$OUT" | grep -q "원본없음(보존).*orphan" && echo "PASS: 고아 .bak 보존" || echo "FAIL"
[ -f "$TMP/real.txt.bak.20260101" ] && echo "PASS: dry-run이 실제삭제 안함" || echo "FAIL"

echo ""
echo "=== TEST 4: --run → 원본있는 .bak만 삭제, 나머지 보존 ==="
OUT="$(./cleanup.sh "$TMP" --run 2>&1 || true)"
[ ! -f "$TMP/real.txt.bak.20260101" ] && echo "PASS: 원본있는 .bak 삭제됨" || echo "FAIL"
[ -f "$TMP/com.user.secondbrain.rss.plist.bak.20260101" ] && echo "PASS: secondbrain 보존됨" || echo "FAIL"
[ -f "$TMP/orphan.txt.bak.20260101" ] && echo "PASS: 고아 .bak 보존됨" || echo "FAIL"

echo ""
echo "=== 검증 끝 (실제 대상폴더 무손상, 임시폴더만 사용) ==="
