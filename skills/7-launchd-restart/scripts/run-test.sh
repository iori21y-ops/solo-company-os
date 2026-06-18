#!/bin/bash
# 7-launchd-restart 검증: 실제 재시작 없이 dry-run이 정상인지 확인
# 주의: restart.sh 출력을 변수에 먼저 담아 파이프 종료코드 전파를 끊는다.
#       (grep -q + pipefail 조합이 SIGPIPE로 오탐 내는 것 방지)
set -uo pipefail
cd "$(dirname "$0")"

echo "=== TEST 1: 라벨 없이 호출 → 사용법 출력 ==="
OUT="$(./restart.sh 2>&1 || true)"
echo "$OUT" | grep -q "사용법" && echo "PASS: 사용법 안내" || echo "FAIL"

echo ""
echo "=== TEST 2: 존재하는 라벨 dry-run ==="
OUT="$(./restart.sh com.cadam.md-dashboard 2>&1 || true)"
echo "$OUT" | grep -q "DRY-RUN" && echo "PASS: dry-run 동작" || echo "FAIL"

echo ""
echo "=== TEST 3: 없는 라벨 → 경고 ==="
OUT="$(./restart.sh com.nonexistent.fake 2>&1 || true)"
echo "$OUT" | grep -q "없습니다" && echo "PASS: 없는 라벨 거부" || echo "FAIL"

echo ""
echo "=== 검증 끝 (실제 재시작 0회) ==="
