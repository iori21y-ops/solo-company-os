# 포스트모템 — 봇 간 "종료" 무한 루프

- 작성: 관리팀장
- 일자: 2026-06-02
- 심각도: 중 (채널 도배 + Claude 호출 한도/타임아웃 소진)
- 상태: 수정 적용·재시작 완료, 검증됨

## 증상
관리팀장 ↔ 데이터 등 봇끼리 `<@봇ID> 종료` 메시지를 무한 핑퐁.
broker.error.log에 turns 초과·300s 타임아웃 다수 발생.

## 근본 원인
`agent.js` 응답 처리에서 봇 발신 메시지에는 무조건 발신자 멘션을 접두로 붙임:
`const mentionPrefix = message.author.bot ? '<@author> ' : ''`
→ "종료"(terminal) 답변에도 멘션이 붙음
→ 상대 봇의 extractPrompt가 그 멘션을 매칭해 prompt를 추출·재처리
→ 재트리거 무한 반복.

## 조치 (적용 완료)
1. terminal(종료·무응답·무액션) 답변에는 멘션 미부착:
   `mentionPrefix = (message.author.bot && !terminal) ? '<@author> ' : ''`
   → 멘션 없으면 상대 extractPrompt 미매칭 → 재트리거 안 됨.
2. 봇 발신 + terminal 프롬프트(`종료`/`응답 없음`/`무응답`) 조기 SKIP 가드 추가.
3. 인라인 role-mention 파싱 보강(멘션이 줄 중간에 있어도 인식).
- 파일: `~/.openclaw/workspace/claude-broker/src/agent.js` (10:07:18 수정)
- 백업: `agent.js.bak-endloop-1003`

## 검증
- 브로커 PID 65810, 10:07:30 재시작 → 패치 코드 구동 중. LaunchAgent state=running/keepalive.
- 10:11 기획팀장 수신 테스트: 5개 에이전트 각 1회 "수신 OK/종료" 회신, 재차 캐스케이드 없음. 종료 핑퐁 소멸 확인.
- broker.error.log 10:07:31 이후 신규 에러 없음(과거 에러는 루프 시절 잔여).

## 잔여/주의
- [CALL:]/[ESCALATE]/[APPROVAL] 등 실제 위임은 의도적으로 role-mention을 발송하므로 정상 재트리거됨(루프 아님).
- 비-terminal 봇 간 응답은 설계상 멘션이 붙음 → "모든 루프 불가"는 아님. terminal 핑퐁만 차단됨.
