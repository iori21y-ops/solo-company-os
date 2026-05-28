#!/bin/bash
set -e

if [ "$#" -lt 1 ]; then
  echo "사용법: $0 <태그|경로> [세션명]"
  echo ""
  echo "지원 태그: 랜테일러 / 에이전트 / 일회성"
  echo "또는 풀 경로: projects/rentailor, meta/agents, scratch/general"
  exit 1
fi

TAG=$1
SESSION_NAME=${2:-"session"}

case "$TAG" in
  랜테일러|rentailor|projects/rentailor) AREA="projects/rentailor" ;;
  에이전트|agents|meta/agents) AREA="meta/agents" ;;
  일회성|general|scratch|scratch/general) AREA="scratch/general" ;;
  *)
    if [[ "$TAG" =~ ^(projects|meta|scratch)/.+ ]]; then
      AREA="$TAG"
      if [ ! -d "$HOME/projects/_meta/handoff/$AREA" ]; then
        echo "영역 없음: handoff/$AREA"
        exit 1
      fi
    else
      echo "알 수 없는 태그: $TAG"
      exit 1
    fi
    ;;
esac

REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
TARGET_DIR="$REPO_ROOT/handoff/$AREA"
TODAY=$(date +%Y-%m-%d)
SESSION_SLUG=$(echo "$SESSION_NAME" | tr ' ' '-' | tr -cd '[:alnum:]-가-힣')
DATE_FILE="$TARGET_DIR/$TODAY-$SESSION_SLUG.md"

if [ -e "$DATE_FILE" ]; then
  SUFFIX=2
  while [ -e "$TARGET_DIR/$TODAY-$SESSION_SLUG-$SUFFIX.md" ]; do
    SUFFIX=$((SUFFIX + 1))
  done
  DATE_FILE="$TARGET_DIR/$TODAY-$SESSION_SLUG-$SUFFIX.md"
fi

echo "영역: $AREA"
echo "날짜 파일: $DATE_FILE"

if [ -n "$HANDOFF_CONTENT" ]; then
  echo "$HANDOFF_CONTENT" > "$DATE_FILE"
else
  echo "본문 없음. HANDOFF_CONTENT 환경변수에 본문을 넣고 실행하세요."
  exit 1
fi

VIOLATION=0
if grep -qE '\b(100|192\.168|10)\.[0-9]{1,3}\.[0-9]{1,3}' "$DATE_FILE"; then
  echo "IP 검출"
  VIOLATION=1
fi
if grep -qE '[a-z]{15,}\.supabase\.co' "$DATE_FILE"; then
  echo "Supabase 검출"
  VIOLATION=1
fi
if grep -qiE '(api[_-]?key|secret|password|bearer)' "$DATE_FILE"; then
  echo "키/시크릿 단어 검출 (확인 필요)"
fi
if [ $VIOLATION -eq 1 ]; then
  echo "푸시 중단"
  exit 1
fi

cp "$DATE_FILE" "$TARGET_DIR/handoff-latest.md"
echo "handoff-latest.md 갱신"

if [ -x "$REPO_ROOT/scripts/refresh-readme.sh" ]; then
  "$REPO_ROOT/scripts/refresh-readme.sh"
fi

cd "$REPO_ROOT"
git add "handoff/$AREA/" README.md
git commit -m "Session: $AREA - $SESSION_NAME"
git push

sleep 3
URL="https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/handoff/$AREA/handoff-latest.md"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL")
if [ "$STATUS" = "200" ]; then
  echo "200 OK"
else
  echo "FAIL: $STATUS"
fi

# 클립보드 자동 복사 — 본문 직접 박기 (다음 세션 즉시 시작 가능)
if command -v pbcopy > /dev/null 2>&1; then
  { cat "$TARGET_DIR/handoff-latest.md"; printf '\n\n위 내용이 직전 세션 마무리야. "# 완료" 섹션은 끝난 작업이고, "# 다음" 섹션이 이번 세션에서 할 일이야. 완료된 작업을 다시 하지 마.'; } | pbcopy
  echo "✅ 본문이 클립보드에 복사됨 — 새 Claude 채팅에 ⌘V"
fi

echo ""
echo "완료. 영역: $AREA"
echo "URL: $URL"
