#!/bin/bash
# .bak 안전 정리. 기본 dry-run, --run 붙여야 실제 삭제.
# 가드: 경로 화이트리스트 / second-brain·민감정보 배제 / 원본 존재 확인 / rm -rf 금지
set -uo pipefail

TARGET="${1:-}"
MODE="${2:-}"

if [ -z "$TARGET" ]; then
  echo "사용법: cleanup.sh <대상폴더> [--run]"
  echo "예: cleanup.sh ~/projects/cadam/cadam-dashboard --run"
  echo "(대상폴더 필수 — 홈 전역 스윕 방지)"
  exit 2
fi

# 경로 정규화 + 위험 경로 차단
TARGET="${TARGET/#\~/$HOME}"
if [ "$TARGET" = "$HOME" ] || [ "$TARGET" = "/" ] || [ -z "$TARGET" ]; then
  echo "⛔ 거부: 홈/루트 전역은 대상이 될 수 없습니다."
  exit 1
fi
if [ ! -d "$TARGET" ]; then
  echo "⛔ 거부: '$TARGET' 폴더가 없습니다."
  exit 1
fi

# 배제 패턴 (절대 삭제 금지)
EXCLUDE='secondbrain|cadam-secrets|\.claude/'

echo "=== 대상: $TARGET ==="
echo "=== 모드: ${MODE:-dry-run} ==="
echo ""

DELETED=0
SKIPPED=0

while IFS= read -r f; do
  # 배제 패턴 매칭 → 건너뜀
  if echo "$f" | grep -qE "$EXCLUDE"; then
    echo "🛡  배제(보호): $f"
    SKIPPED=$((SKIPPED+1))
    continue
  fi
  # 원본 존재 확인 (X.bak.날짜 → X 추출)
  ORIG="${f%%.bak*}"
  if [ ! -e "$ORIG" ]; then
    echo "⚠  원본없음(보존): $f  → 원본 '$ORIG' 없어 유일본 가능, 삭제 안 함"
    SKIPPED=$((SKIPPED+1))
    continue
  fi
  if [ "$MODE" = "--run" ]; then
    rm "$f" && echo "🗑  삭제: $f"
    DELETED=$((DELETED+1))
  else
    echo "[DRY-RUN] 삭제 예정: $f"
    DELETED=$((DELETED+1))
  fi
done < <(find "$TARGET" -type f -name "*.bak*" 2>/dev/null)

echo ""
if [ "$MODE" = "--run" ]; then
  echo "=== 완료: $DELETED개 삭제, $SKIPPED개 보존 ==="
else
  echo "=== [DRY-RUN] $DELETED개 삭제 예정, $SKIPPED개 보존. 실제 삭제하려면 --run ==="
fi
