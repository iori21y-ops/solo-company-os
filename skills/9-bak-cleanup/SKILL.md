---
name: bak-cleanup
description: 작업 중 쌓인 .bak 백업 파일을 안전하게 정리한다. 지정한 폴더 안의 .bak만, 원본 존재를 확인하고, dry-run으로 먼저 보여준 뒤에만 삭제한다.
type: script
---

# .bak 백업 파일 안전 정리

## 목적
.bak.YYYYMMDD 류 백업이 작업 폴더에 쌓이면 정리한다. 단, 일괄 rm은 절대 금지 대상(second-brain plist 백업, 민감정보)을 휩쓸 위험이 있다. 이 스킬은 화이트리스트 경로 + 배제 패턴 + dry-run으로 그 사고를 막는다.

## 언제 쓰나
- 세션 작업 후 특정 폴더에 .bak이 누적됐을 때
- 안정화가 끝나 백업을 지워도 되는 시점

## 사용법
scripts/cleanup.sh <대상폴더> [--run]
- 기본은 dry-run: 지울 후보를 나열만 한다. 실제 삭제 없음.
- 실제 삭제는 --run 을 붙인다.
- 대상폴더는 반드시 명시. 인자 없으면 거부(홈 전역 스윕 방지).
- 예: cleanup.sh ~/projects/cadam/cadam-dashboard --run

## Gotchas (절대 지킬 것)
- second-brain 백업은 삭제 금지: com.user.secondbrain.*.bak 류는 도구가 자동 관리하는 영역. 배제 패턴으로 무조건 제외한다.
- 민감정보 배제: *secondbrain*, .cadam-secrets, ~/.claude, 권한 600 plist는 건드리지 않는다.
- 홈 전역(~ 또는 /) 스윕 금지: 대상폴더를 반드시 인자로 받고, 그 하위만 처리한다.
- 원본 존재 확인: X.bak을 지우기 전에 원본 X가 살아있는지 본다. 원본이 없으면 그 .bak이 유일본일 수 있으므로 삭제하지 않고 경고만 한다.
- rm -rf 금지: 파일 단위 rm만. 디렉토리 재귀 삭제 안 한다.

## 검증
scripts/run-test.sh 로 dry-run 안전장치가 작동하는지 확인한다 (실제 삭제 0회).
