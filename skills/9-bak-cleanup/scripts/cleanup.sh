#!/bin/bash
# Safe .bak cleanup: never deletes. Moves backups into the archive box
# _archive/<YYYY-MM-DD>/<original path under ~/projects> and logs each move in MOVED.txt
# (FOLDER_RULES section 5). Default is dry-run; pass --run to actually move.
# Guards: target must be inside ~/projects, protected/secret patterns skipped,
# original must exist, git-tracked files skipped, launchd-referenced files skipped.
set -uo pipefail

TARGET="${1:-}"
MODE="${2:-}"

# Overridable only for tests.
PROJECTS_ROOT="${BAK_PROJECTS_ROOT:-$HOME/projects}"
ARCHIVE_ROOT="${BAK_ARCHIVE_ROOT:-$PROJECTS_ROOT/_archive}"
LAUNCH_DIR="${BAK_LAUNCH_DIR:-$HOME/Library/LaunchAgents}"

if [ -z "$TARGET" ]; then
  echo "사용법: cleanup.sh <대상폴더> [--run]"
  echo "예: cleanup.sh ~/projects/content-engine/publishers/naver"
  echo "(대상폴더 필수 — ~/projects 안만 가능. 지우지 않고 _archive/<날짜>/로 옮긴다)"
  exit 2
fi

TARGET="${TARGET/#\~/$HOME}"
if [ ! -d "$TARGET" ]; then
  echo "⛔ 거부: '$TARGET' 폴더가 없습니다."
  exit 1
fi
TARGET="$(cd "$TARGET" && pwd -P)"
ROOT_REAL="$(cd "$PROJECTS_ROOT" && pwd -P)"
ARCHIVE_REAL="$(mkdir -p "$ARCHIVE_ROOT" 2>/dev/null; cd "$ARCHIVE_ROOT" 2>/dev/null && pwd -P || echo "$ARCHIVE_ROOT")"

case "$TARGET/" in
  "$ROOT_REAL"/*/) ;;
  *) echo "⛔ 거부: '$TARGET'는 $ROOT_REAL 안이 아닙니다 (홈·루트·바깥 폴더 금지)."; exit 1 ;;
esac
if [ "$TARGET" = "$ROOT_REAL" ]; then
  echo "⛔ 거부: ~/projects 전체는 대상이 될 수 없습니다. 프로젝트 폴더를 지정하세요."
  exit 1
fi
case "$TARGET/" in
  "$ARCHIVE_REAL"/*) echo "⛔ 거부: 보관함(_archive) 안은 대상이 아닙니다."; exit 1 ;;
esac

# Never touch: secrets, tool-managed areas, intentional backups in the data warehouse.
# config.json / cookies backups of the publisher may hold secrets → do not move or copy (rule 4).
PROTECT='secondbrain|second-brain|cadam-secrets|/\.claude/|/\.git/|/node_modules/|\.env|config\.json|cookie|secret|token|credential|/_data/[^/]+/backups/'

TODAY="$(date +%F)"
EMPTY_ON="$(date -v+7d +%F 2>/dev/null || date -d '+7 days' +%F)"
DAY_DIR="$ARCHIVE_REAL/$TODAY"

echo "=== 대상: $TARGET ==="
echo "=== 모드: ${MODE:-dry-run} (지우지 않음 → $DAY_DIR 로 옮김) ==="
echo ""

MOVED=0
SKIPPED=0

while IFS= read -r f; do
  if echo "$f" | grep -qiE "$PROTECT"; then
    echo "🛡  보호(손대지 않음): $f"
    SKIPPED=$((SKIPPED+1)); continue
  fi
  ORIG="${f%%.bak*}"
  if [ ! -e "$ORIG" ]; then
    echo "⚠  원본없음(보존): $f  → 원본 '$ORIG' 없어 유일본 가능"
    SKIPPED=$((SKIPPED+1)); continue
  fi
  dir="$(dirname "$f")"
  if git -C "$dir" rev-parse --is-inside-work-tree >/dev/null 2>&1 \
     && git -C "$dir" ls-files --error-unmatch "$f" >/dev/null 2>&1; then
    echo "⚠  git이 추적 중(보존): $f  → 커밋과 함께 따로 정리"
    SKIPPED=$((SKIPPED+1)); continue
  fi
  rel="${f#$ROOT_REAL/}"
  # Match on the path under ~/projects so /var vs /private/var or ~ spellings all hit.
  if [ -d "$LAUNCH_DIR" ] && grep -rqF "$rel" "$LAUNCH_DIR" 2>/dev/null; then
    echo "⚠  예약 작업(launchd)이 가리킴(보존): $f"
    SKIPPED=$((SKIPPED+1)); continue
  fi
  dest="$DAY_DIR/$rel"
  if [ -e "$dest" ]; then
    echo "⚠  보관함에 같은 이름 있음(보존): $f"
    SKIPPED=$((SKIPPED+1)); continue
  fi
  if [ "$MODE" = "--run" ]; then
    mkdir -p "$(dirname "$dest")"
    if mv -n "$f" "$dest" && [ -e "$dest" ] && [ ! -e "$f" ]; then
      printf '%s | 무엇: %s | 어디서: %s | 왜: .bak 정리(원본 있음, bak-cleanup 스킬) | 비울 날: %s 이후 사장님 확인\n' \
        "$(date '+%F %T')" "$rel" "$f" "$EMPTY_ON" >> "$DAY_DIR/MOVED.txt"
      echo "📦 옮김: $f → $dest"
      MOVED=$((MOVED+1))
    else
      echo "❌ 옮기기 실패(그대로 둠): $f"
      SKIPPED=$((SKIPPED+1))
    fi
  else
    echo "[DRY-RUN] 옮길 예정: $f → $dest"
    MOVED=$((MOVED+1))
  fi
done < <(find "$TARGET" -type f -name "*.bak*" 2>/dev/null)

echo ""
if [ "$MODE" = "--run" ]; then
  echo "=== 완료: ${MOVED}개 보관함으로 옮김, ${SKIPPED}개 보존. 기록: $DAY_DIR/MOVED.txt ==="
  echo "=== 7일 뒤($EMPTY_ON) 목록을 사장님께 보여 주고 승인 받은 뒤 비운다 (FOLDER_RULES §5) ==="
else
  echo "=== [DRY-RUN] ${MOVED}개 옮길 예정, ${SKIPPED}개 보존. 실제로 옮기려면 --run ==="
fi
