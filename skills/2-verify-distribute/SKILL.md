---
name: verify-distribute
description: 자동배분 실행 후 부모-자식 카드가 올바르게 생성·연결·상속됐는지 검증
type: script
---

## 목적
관리팀장봇 자동배분이 돈 뒤, 결과가 의도대로인지 사람 눈이 아니라
스크립트로 결정론적으로 판정한다. 매번 칸반 눈으로 확인하는 실수를 없앤다.

## 언제 쓰나 (트리거)
- 대시보드에 '배분요청'을 넣고 자동배분이 돈 직후
- 배분 로직(broker distributePoll / createLedgerTask)을 고친 뒤 회귀 확인
- "자식 카드가 안 보인다 / 알림이 안 왔다" 증상이 나올 때

## 사용법
scripts/run-test.sh <부모카드_dashboardId>
예: scripts/run-test.sh 58
→ 부모 id를 주면 그 부모의 자식들을 PASS/FAIL로 판정.

## Gotchas (함정)
→ gotchas.md 참고

## 스크립트
→ scripts/run-test.sh 참고
- 대시보드 API(localhost:3101/api/tasks) 경유로 읽는다 (broker와 동일 경로).
- 읽기 전용. 어떤 변경도 하지 않는다.
