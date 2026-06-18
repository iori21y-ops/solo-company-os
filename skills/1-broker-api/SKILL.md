---
name: broker-api
description: broker(agent.js)가 대시보드 erp_tasks를 REST로 호출하는 표준 방식. 작업 카드 생성/조회/상태변경 코드를 쓰거나 고칠 때 이 규칙을 따른다.
type: rule
---

# broker → erp_tasks API 호출 규칙

## 목적
broker는 Supabase에 직접 붙지 않는다. 대시보드의 `/api/tasks` REST 엔드포인트만 호출한다. 카드 생성/조회/상태변경을 추가하거나 고칠 때, 매번 새 fetch 패턴을 즉흥으로 짜지 말고 이 규칙을 그대로 쓴다.

## 언제 쓰나
- broker에서 작업 카드를 새로 만들 때 (POST)
- 배분대기/특정 status 카드를 조회할 때 (GET)
- 카드 상태를 바꿀 때, 예: 배분대기→진행중 (PATCH)
- agent.js의 erp_tasks 호출부를 수정할 때

## 사용법

### 공통
- 엔드포인트는 상수 `ERP_TASKS_URL` 하나만 쓴다 (기본 `http://localhost:3101/api/tasks`). URL 하드코딩 금지.
- 헤더는 항상 이 패턴:
  - `'content-type': 'application/json'`
  - `DASHBOARD_AUTH_TOKEN` 있으면 `'x-dashboard-token'` 동봉 (대시보드 proxy.ts 토큰 인증 통과용)
- 모든 호출은 try/catch로 감싼다. 대시보드 연결 실패가 협의/작업 자체를 막으면 안 된다. 실패 시 broker.log에 경고만 남기고 흐름은 계속.

### POST (카드 생성)
body는 4필드만:
- agent: 담당자 (normalizedOwner 형태로 정규화)
- title: 작업 지시문
- status: '대기'
- parentId: 부모 ledger task의 dashboardId(정수). 부모 없으면 null(최상위)

### GET (조회)
status로 거른다 (예: 배분대기 수집). 응답은 카드 배열.

### PATCH (상태 변경)
대상 카드 id + 바꿀 status. 멱등하게 — 같은 카드를 두 번 진행중으로 PATCH해도 안전해야 함.

## Gotchas
- originChannelId는 POST body에 없다. broker 로컬 ledger에만 있고 erp_tasks 테이블엔 안 들어간다. 디스코드 알림이 originChannelId를 요구하면 호출 쪽(createLedgerTask)에서 주입해야지, API body로는 안 넘어간다.
- DASHBOARD_AUTH_TOKEN은 broker .env에 있다. Supabase 키는 .env에 없다 — broker는 Supabase 직접 접근 수단이 없으므로 erp_tasks를 Supabase로 직접 치려 하지 말 것.
- 연결 실패를 throw로 터뜨리면 배분/협의 루프가 멈춘다. 반드시 try/catch 격리.

## 포인터
- 호출부: ~/.openclaw/workspace/claude-broker/src/agent.js
  - 57행 ERP_TASKS_URL 상수
  - 135행 createLedgerTask POST
  - 1045행 GET / 1055행 PATCH (sync 동기화 전용)
  - 1680행 distributePoll GET 조회 (조회 대표) / 1687행 distributePoll PATCH 상태변경 (대표)
