#!/bin/bash
# launchd 서비스 재시작. 기본 dry-run, --run 붙여야 실제 실행.
set -euo pipefail

LABEL="${1:-}"
MODE="${2:-}"

if [ -z "$LABEL" ]; then
  echo "사용법: restart.sh <라벨> [--run]"
  echo "예: restart.sh com.cadam.md-dashboard --run"
  exit 1
fi

# 라벨이 실제로 로드돼 있는지 확인
if ! launchctl list | grep -q "$LABEL"; then
  echo "⚠️  '$LABEL' 라벨이 launchctl list에 없습니다. 라벨을 확인하세요."
  echo "현재 cadam/rentailor 라벨:"
  launchctl list | grep -iE "cadam|rentailor" || true
  exit 1
fi

CMD="launchctl kickstart -k gui/$(id -u)/$LABEL"

if [ "$MODE" = "--run" ]; then
  echo "▶ 재시작 실행: $CMD"
  eval "$CMD"
  sleep 2
  echo "▶ 재시작 후 상태:"
  launchctl list | grep "$LABEL"
else
  echo "[DRY-RUN] 실행될 명령: $CMD"
  echo "[DRY-RUN] 실제 재시작하려면 끝에 --run 을 붙이세요."
  echo "현재 상태:"
  launchctl list | grep "$LABEL"
fi
