---
title: 결재 카드 표준
status: active
last-updated: 2026-06-02
---

# 결재 카드 표준

## 원칙

- 모든 결재 요청은 Discord 결재 카드로 올린다.
- 카드에는 반드시 `승인`, `수정`, `반려`, `코멘트` 컨트롤이 있어야 한다.
- 코멘트는 가능한 경우 모달로 받는다.
- 산출물 파일이나 이미지는 카드에 첨부한다.
- 채팅 공지만으로는 적용된 것으로 보지 않는다. 각 에이전트 지침과 결재 도구에 이 규칙이 있어야 한다.

## 결재자

- 실무자 `마케팅`, `컨텐츠`, `데이터`가 관리팀장에게 결재를 올릴 때: 결재자 `관리팀장`
- 관리팀장이 대표님 결정을 받아야 할 때: 결재자 `대표님`
- 기획팀장/OpenClaw 산출물 결재: 기본 결재자 `대표님`, 실무 검토가 먼저 필요한 경우 `관리팀장`

## Claude 브로커 프로토콜

Claude 브로커 소속 에이전트는 결재 요청을 일반 텍스트로 끝내지 말고, 응답 마지막에 아래 한 줄을 붙인다.

```text
[APPROVAL:관리팀장] 제목 | 요청 요약 | /절대/경로/파일명
```

예시:

```text
[APPROVAL:관리팀장] 데이터 검증 리포트 결재 요청 | 아반떼 가격 데이터 정합성 리포트 검토 요청 | /Users/kim/projects/_meta/agents/data/outputs/pending/verdict-avante-20260602.md
```

파일 첨부가 없으면 세 번째 칸은 생략할 수 있다.

```text
[APPROVAL:관리팀장] 발행 후보 승인 요청 | 이번 주 네이버 블로그 후보 3건 중 1건 선택 요청
```

브로커는 이 프로토콜을 감지하면 `tools/send-approval-card.mjs`를 호출해 동일 채널에 결재 카드를 생성한다.

## OpenClaw 도구

OpenClaw/Codex 쪽은 다음 스크립트를 사용한다.

```bash
node /Users/kim/.openclaw/workspace/tools/send-approval-card.mjs \
  --target channel:1510181005330350100 \
  --approver 관리팀장 \
  --title "결재 요청 제목" \
  --summary "요청 요약" \
  --file "/절대/경로/파일명"
```

`--approver`는 `대표님`, `관리팀장`, Discord 사용자 ID를 지원한다.
