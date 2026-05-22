---
title: 수정 시 누락 방지 체크리스트
last-updated: 2026-05-22
---

# 수정 체크리스트

새로운 결정이 나왔을 때 어디를 업데이트해야 하는지 추적용.

<!-- SECTION:START name=case_a -->
## 케이스 A: 새로운 경계 쌍 확정 (예: sales↔cs)

다음 4곳 모두 업데이트 필요:
- [ ] `_shared/boundary-rules.md` — 새 SECTION으로 쌍 내용 추가
- [ ] `{왼쪽 에이전트}/SKILL.md` — "인접 에이전트와의 경계" 섹션에 추가
- [ ] `{오른쪽 에이전트}/SKILL.md` — "인접 에이전트와의 경계" 섹션에 추가
- [ ] `README.md` — "경계 규칙 점검 현황" 섹션의 "확정 완료"로 이동
<!-- SECTION:END name=case_a -->

<!-- SECTION:START name=case_b -->
## 케이스 B: 스텁 에이전트 정의 완료 (예: sales 스텁 → 정의됨)

다음 3곳 모두 업데이트 필요:
- [ ] `{에이전트}/SKILL.md` — 스텁 내용을 전체 8개 섹션으로 교체
- [ ] `README.md` "agent_list" 섹션 — 해당 행의 상태 "스텁" → "정의됨"
- [ ] 관련 쌍이 있다면 케이스 A도 함께
<!-- SECTION:END name=case_b -->

<!-- SECTION:START name=case_c -->
## 케이스 C: 기존 정의 수정

- [ ] 해당 SKILL.md의 해당 섹션만 str_replace
- [ ] 다른 SKILL.md에 동일 내용이 중복 기록되어 있다면 그쪽도 동기화
- [ ] `last-updated` 날짜 갱신
<!-- SECTION:END name=case_c -->

<!-- SECTION:START name=case_d -->
## 케이스 D: 새 에이전트 추가 (10번째 등)

- [ ] `{새이름}/SKILL.md` 신규 생성
- [ ] `README.md` "agent_list" 표에 새 행 추가
- [ ] 인접 에이전트와의 경계 쌍 점검 → 케이스 A 적용
<!-- SECTION:END name=case_d -->
