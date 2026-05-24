---
area: meta/agents
created: 2026-05-24
description: 9개 에이전트 시스템 정비 영역
---

# meta/agents 핸드오프 초기화

9개 직무 에이전트(marketing, content, data, sales, cs, ops, finance, legal, strategy) 설계 및 경계 정의 작업 영역.

## 현재 상태

- 정의됨 3/9: marketing, content, data
- 스텁 6/9: sales, cs, ops, finance, legal, strategy
- boundary-rules.md에 쌍1(marketing↔content), 쌍2(content↔data) 완료

## 다음 작업 후보

- **쌍3 sales↔cs 경계 정의** ← 다음
- 쌍4 ops↔data
- 쌍5 strategy↔전체
- 쌍6 legal↔finance

## 핵심 페치 URL

- 에이전트 목록: https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/README.md
- 기존 경계 규칙: https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/boundary-rules.md
