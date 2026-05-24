---
title: Strategy Agent
status: 최소 정의됨 (쌍5 확정 — 멀티에이전트 자율화 전 확장 예정)
last-updated: 2026-05-25
---

# Strategy Agent

<!-- SECTION:START name=definition -->
## 한 줄 정의
사업 방향 판단, 에이전트 간 우선순위 조율, 리소스 배분.
현 단계에서는 파운더(경년)가 직접 수행. 멀티에이전트 자율 실행 시점에 확장 예정.
<!-- SECTION:END name=definition -->

<!-- SECTION:START name=intervention_conditions -->
## 개입 조건

아래 조건을 충족할 때만 strategy 소관. 그 외는 해당 에이전트가 자율 수행.

1. **복수 에이전트 간 우선순위 충돌** — 두 에이전트가 같은 리소스를 놓고 경합할 때
2. **신규 사업 방향·기능 도입 여부 판단** — "이걸 해야 하나?" 수준의 의사결정
3. **리소스(시간·비용) 배분 결정** — 어느 에이전트에 얼마를 투입할지
4. **분기·월간 목표 설정 및 리뷰** — 전체 우선순위 재조정
<!-- SECTION:END name=intervention_conditions -->

<!-- SECTION:START name=boundaries -->
## 경계

단일 에이전트 소관 실무에는 개입하지 않음.
이미 경계가 확정된 영역의 실무 판단은 해당 에이전트가 자율 수행.

경계 판정 기준:
- 단일 에이전트 소관 → 해당 에이전트가 처리
- 복수 에이전트에 걸치거나 사업 방향 판단 → strategy

상세는 boundary-rules.md 쌍5 참조.
<!-- SECTION:END name=boundaries -->

<!-- SECTION:START name=delegation_grade -->
## 위임 등급

**현 단계 위임 불가 — 파운더 직접 판단 영역.**

멀티에이전트 자율 실행 체계 구축 후 재정의 예정.
<!-- SECTION:END name=delegation_grade -->
