---
title: 9개 에이전트 시스템 인덱스
status: in-progress (경계 점검 진행 중)
last-updated: 2026-05-22
---

# 9개 에이전트 시스템

온라인 비즈니스 법인 운영을 위한 직무별 에이전트 분류.
랜테일러뿐 아니라 다른 온라인 사업 프로젝트에도 공통 적용.

<!-- SECTION:START name=agent_list -->
## 에이전트 목록

| # | 이름 | 한 줄 정의 | 상태 |
|---|------|----------|------|
| 1 | marketing | 외부 발행 콘텐츠 제작·발행. 트래픽·전환 유도 | 정의됨 |
| 2 | content | 데이터를 사람이 보는 에셋으로 가공·비축 (재료 공급자) | 정의됨 |
| 3 | data | 사실 수집·검증·정합성 유지. DB와 사이트 표시 자산 책임 | 정의됨 |
| 4 | sales | 리드·전환 데이터 분석·룰화. CRM 정합성·딜러 성과·채널 ROI 측정 | 정의됨 |
| 5 | cs | 고객·딜러 직접 대화. 1차 응대~체결 직전까지. 체결 후는 딜러 책임 | 정의됨 |
| 6 | ops | 서버·배포·백업·모니터링·비용 알림 | 스텁 |
| 7 | finance | 매출·지출 집계, 정산 초안, 손익 리포트 | 스텁 |
| 8 | legal | 계약·약관·세금계산서 검토·분류·요약 (보조만) | 스텁 |
| 9 | strategy | 다른 에이전트 산출물 종합. 주간 리뷰, 우선순위 제안 | 스텁 |
<!-- SECTION:END name=agent_list -->

## 구도 핵심

- **수평 1~8**: 병렬 실행
- **수직 9 (strategy)**: 다른 에이전트 감독
- **위임 정책**: `_shared/delegation-template.md`, `_shared/workflow-template.md`, `_shared/security/` 참조. 위임금지 영역은 에이전트가 보조만, 결정은 사람

<!-- SECTION:START name=boundary_status -->
## 경계 규칙 점검 현황

확정 완료:
- marketing ↔ content (쌍1)
- content ↔ data (쌍2)
- sales ↔ cs (쌍3)

확정 대기:
- ops ↔ data (쌍4)
- strategy ↔ 전체 (쌍5)
- legal ↔ finance (쌍6)

상세는 `_shared/boundary-rules.md` 참조.
<!-- SECTION:END name=boundary_status -->

## 파일 운영 원칙

- 신규 생성만 자동화 (덮어쓰기 가드)
- 수정은 섹션 마커 기반 str_replace로만
- 매 수정 시 `_shared/modification-checklist.md` 따라 누락 확인
- 경계 규칙은 양쪽 SKILL.md에 중복 기록 (누락 방지)

<!-- SECTION:START name=files_in_this_area -->
## 이 영역의 파일 지도

| 파일 | raw URL | 용도 |
|------|---------|------|
| `agents/README.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/README.md) | 인덱스 — 여기 |
| `agents/_shared/boundary-rules.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/boundary-rules.md) | 에이전트 간 경계 규칙 (쌍1·쌍2 확정) |
| `agents/_shared/modification-checklist.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/modification-checklist.md) | 수정 시 누락 방지 체크리스트 |
| `agents/marketing/SKILL.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/marketing/SKILL.md) | Marketing Agent 정의 |
| `agents/content/SKILL.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/content/SKILL.md) | Content Agent 정의 |
| `agents/data/SKILL.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/data/SKILL.md) | Data Agent 정의 |
| `agents/{sales,cs,ops,finance,legal,strategy}/SKILL.md` | — | 스텁 (정의 대기) |
<!-- SECTION:END name=files_in_this_area -->
