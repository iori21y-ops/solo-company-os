#!/usr/bin/env bash
# 신규 핸드오프 영역 자동 생성
# Usage: ./scripts/new-handoff.sh <category> <name> <description>
# Example: ./scripts/new-handoff.sh scratch test-area "테스트용"
# Example: ./scripts/new-handoff.sh projects newproject "새 프로젝트"
# Example: ./scripts/new-handoff.sh meta ops "운영 에이전트 정비"

set -euo pipefail

CATEGORY="${1:-}"
NAME="${2:-}"
DESC="${3:-(설명 없음)}"
DATE=$(date +%Y-%m-%d)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
AREA_DIR="$BASE_DIR/handoff/$CATEGORY/$NAME"

if [[ -z "$CATEGORY" || -z "$NAME" ]]; then
  echo "사용법: $0 <category> <name> [description]"
  echo "  category: projects | meta | scratch"
  echo "  name:     영역 이름 (영문, 하이픈 허용)"
  echo "  description: 영역 설명 (따옴표로 묶기)"
  exit 1
fi

if [[ -d "$AREA_DIR" ]]; then
  echo "❌ 이미 존재합니다: handoff/$CATEGORY/$NAME/"
  exit 1
fi

mkdir -p "$AREA_DIR"
echo "✅ 디렉토리 생성: handoff/$CATEGORY/$NAME/"

# init 파일 생성
cat > "$AREA_DIR/${DATE}-init.md" << MDEOF
---
area: $CATEGORY/$NAME
created: $DATE
description: $DESC
---

# $NAME 핸드오프 초기화

$DESC

## 첫 작업 후보
- (작업 시작 시 갱신)
MDEOF
echo "✅ ${DATE}-init.md 생성"

# handoff-latest.md 생성 (init 복사)
cp "$AREA_DIR/${DATE}-init.md" "$AREA_DIR/handoff-latest.md"
echo "✅ handoff-latest.md 생성"

# projects 카테고리: DECISIONS·current-state 추가 생성 (gitignore 차단)
if [[ "$CATEGORY" == "projects" ]]; then
  cat > "$AREA_DIR/DECISIONS.md" << MDEOF
---
area: $CATEGORY/$NAME
---
# $NAME 결정사항 누적

MDEOF
  cat > "$AREA_DIR/current-state.md" << MDEOF
---
area: $CATEGORY/$NAME
---
# $NAME 현재 상태

MDEOF
  echo "✅ DECISIONS.md 생성 (로컬 전용 — gitignore)"
  echo "✅ current-state.md 생성 (로컬 전용 — gitignore)"
fi

echo ""
echo "README 자동 갱신 중..."
"$SCRIPT_DIR/refresh-readme.sh"
echo ""
echo "✅ 완료: handoff/$CATEGORY/$NAME/"
