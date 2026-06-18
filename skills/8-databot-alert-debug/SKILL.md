---
name: databot-alert-debug
description: 데이터봇/에이전트 알림(디스코드 멘션·결과 통보)이 안 올 때 원인을 순서대로 짚는 런북. broker 로그와 ledger를 직접 확인한다.
type: script
---

# 데이터봇 알림 디버그 런북

## 목적
"알림이 안 왔다 / 멘션이 안 갔다 / 자식 업무가 안 생겼다" 증상이 나올 때,
추측하지 말고 broker 로그·ledger를 정해진 순서로 확인해 원인을 좁힌다.
verify-distribute(2번)가 "카드가 제대로 생겼나"를 본다면, 이 런북은
"알림/멘션이 실제로 나갔나"를 본다.

## 언제 쓰나
- 배분/CALL 후 담당 에이전트에게 알림(멘션)이 안 간 것 같을 때
- 작업 시작(▶️)·결과(✅) 통보가 채널에 안 뜰 때
- 결재/에스컬레이션 알림이 대표님께 안 갈 때

## 사용법 (확인 순서)

### 0. 로그 위치
- 표준: `~/.openclaw/workspace/claude-broker/broker.log`
- 에러: `~/.openclaw/workspace/claude-broker/broker.error.log`

### 1. originChannelId 비었는지 (1순위, 가장 흔함)
알림은 `task.originChannelId`로 채널을 fetch해서 보낸다(agent.js:893).
이게 비면 channel=null → 시작/결과 통보가 아예 안 나가고, CALL은 멘션 대신
ledger 폴백으로 빠진다.
```
grep "CALL→PING-FAIL" ~/.openclaw/workspace/claude-broker/broker.log | tail
```
→ `channel null (originChannelId 누락)` 이 보이면 원인 확정.
   배분 체인은 #대표이사실(1510170922005565470)을 주입하게 돼 있다(distributePoll).
   그 경로를 안 탄 task면 originChannelId가 빈 채로 들어왔을 수 있다.

### 2. 로그 마커로 분기 판정
```
grep -E "\[CALL→OPENCLAW-PING\]|\[CALL→TASK\]|\[CALL→PING-FAIL\]|\[CALL→FAIL\]|\[CALL-DEDUP\]" \
  ~/.openclaw/workspace/claude-broker/broker.log | tail -30
```
- `[CALL→OPENCLAW-PING]` = 기획팀장(OpenClaw)에 멘션 ping 성공
- `[CALL→TASK]` = 일반 에이전트에 ledger 카드로 위임됨(정상). 일반 에이전트는
  멘션 ping이 아니라 **카드+폴러** 경로다. "멘션이 안 왔다"가 정상일 수 있음.
- `[CALL→PING-FAIL]` = 채널 없음 → ledger 폴백 (1번 확인)
- `[CALL→FAIL]` = 예외 발생. 메시지 확인 필요
- `[CALL-DEDUP]` = 같은 대상 5분내 중복이라 건너뜀. "안 온 게" 아니라 "안 보낸 것"

### 3. 에스컬레이션(결재) 알림
대표님 결정 요청은 `raiseApprovalCard`로 가고 mention은 1471821518672756879.
```
grep -E "\[ESCALATE→APPROVAL\]|\[ESCALATE-FAIL\]" ~/.openclaw/workspace/claude-broker/broker.log | tail
```
`ESCALATE-FAIL`이면 결재 알림 발송 실패 → 폴백 동작 확인.

### 4. broker 살아있는지
```
launchctl list | grep claude-broker      # PID 있어야 함
tail -50 ~/.openclaw/workspace/claude-broker/broker.error.log
```

## Gotchas
→ gotchas.md 참고 (originChannelId 1순위 / CALL→PING 변환)

## 스크립트
→ scripts/diagnose.sh (위 1~4를 한 번에 돌려 요약). 읽기 전용.
