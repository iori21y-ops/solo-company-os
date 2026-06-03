---
title: 9개 에이전트 시스템 인덱스
status: in-progress (경계 점검 진행 중)
last-updated: 2026-06-01
---

# 9개 에이전트 시스템

온라인 비즈니스 법인 운영을 위한 직무별 에이전트 분류.
랜테일러뿐 아니라 다른 온라인 사업 프로젝트에도 공통 적용.

<!-- SECTION:START name=agent_list -->
## 에이전트 목록

| # | 이름 | 한 줄 정의 | 상태 |
|---|------|----------|------|
| 1 | 마케팅 | 외부 발행 콘텐츠 제작·발행. 트래픽·전환 유도 | 정의됨 |
| 2 | 컨텐츠 | 데이터를 사람이 보는 에셋으로 가공·비축 | 정의됨 |
| 3 | 데이터 | 사실 수집·검증·정합성 유지. DB와 사이트 표시 자산 책임 | 정의됨 |
| 4 | sales | 리드·전환 데이터 분석·룰화. CRM 정합성·딜러 성과·채널 ROI 측정 | 정의됨 |
| 5 | cs | 고객·딜러 직접 대화. 1차 응대~체결 직전까지. 체결 후는 딜러 책임 | 정의됨 |
| 6 | ops | 파이프라인·서버·인프라 실행·스케줄·장애복구. 현장 엔지니어 | 정의됨 |
| 7 | finance | 돈의 흐름 추적·집계·정산. 수수료·매출·세금 자료 | 최소 정의됨 |
| 8 | legal | 약관·계약·컴플라이언스. 금소법·개인정보·딜러 계약 | 최소 정의됨 |
| 9 | strategy | 복수 에이전트 조율·사업 방향 판단. 현 단계 파운더 직접 수행 | 최소 정의됨 |
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
- ops ↔ data (쌍4)
- strategy ↔ 전체 (쌍5)
- legal ↔ finance (쌍6)

✅ **기본 6/6 경계 확정 완료**

추가 경계 (기본 쌍 외):
- sales ↔ marketing (쌍7)

상세는 `_shared/boundary-rules.md` 참조.
<!-- SECTION:END name=boundary_status -->

## 파일 운영 원칙

- 신규 생성만 자동화 (덮어쓰기 가드)
- 수정은 섹션 마커 기반 str_replace로만
- 매 수정 시 `_shared/modification-checklist.md` 따라 누락 확인
- 경계 규칙은 양쪽 SKILL.md에 중복 기록 (누락 방지)
- 결재는 `_shared/approval-card-policy.md` 기준. **(2026-06-03 개편)** 인터랙티브 버튼 카드 폐지 → **평문 알림 + 모바일 뷰어 링크**, 전용 `#결재함`(1510170922005565470) 단일 집결.
- 결재 결정은 결재함에서 카드에 **답글 `승인`/`반려 [사유]`** → 브로커가 파일 이동(pending→approved/rejected) + 원채널 담당 에이전트에 통보 → 이어받아 진행. (관리팀장 봇 순수 코드 처리, LLM 0)
- 결과물은 알림에서 확인 가능해야 한다: vault 파일은 자동으로 md-viewer 링크(`http://macmini.tail466d13.ts.net:9724`)로 변환, 웹/문서는 `--link`. 파일 없이 경로만 올리면 자동 반려.
- 결재물 자동점검(린트, 0턴) + 로컬AI(qwen3:14b) 요약이 카드에 부가됨.

<!-- SECTION:START name=files_in_this_area -->
## 이 영역의 파일 지도

| 파일 | raw URL | 용도 |
|------|---------|------|
| `agents/README.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/README.md) | 인덱스 — 여기 |
| `agents/_shared/boundary-rules.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/boundary-rules.md) | 에이전트 간 경계 규칙 (쌍1·쌍2 확정) |
| `agents/_shared/scout-territories.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/scout-territories.md) | 에이전트별 자율 발굴 영역 매트릭스 (B-J 위탁 흐름) |
| `agents/_shared/modification-checklist.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/modification-checklist.md) | 수정 시 누락 방지 체크리스트 |
| `agents/_shared/approval-card-policy.md` | — | 결재 표준 (평문 알림+모바일 링크+답글 승인/반려, 버튼 폐지) |
| `agents/marketing/SKILL.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/marketing/SKILL.md) | 마케팅 정의 |
| `agents/content/SKILL.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/content/SKILL.md) | 컨텐츠 정의 |
| `agents/data/SKILL.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/data/SKILL.md) | 데이터 정의 |
| `agents/{sales,cs,ops,finance,legal,strategy}/SKILL.md` | — | 스텁 (정의 대기) |
<!-- SECTION:END name=files_in_this_area -->

<!-- SECTION:START name=vault_assets -->
## vault 운영 자산

에이전트 실제 운영 시 사용하는 자산 (cycle 양식, 사이클 카운터, 정본 참조 stub).
정의/규칙 파일은 위 `files_in_this_area` 섹션 참조.

| 파일 | raw URL | 용도 |
|------|---------|------|
| `_shared/templates/cycle-marketing.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/templates/cycle-marketing.md) | marketing 에이전트 cycle 양식 |
| `_shared/templates/cycle-content.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/templates/cycle-content.md) | content 에이전트 cycle 양식 |
| `_shared/templates/cycle-data.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/templates/cycle-data.md) | data 에이전트 cycle 양식 |
| `_shared/counters/README.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/counters/README.md) | 사이클 카운터 디렉토리 안내 |
| `_shared/counters/cadam.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/counters/cadam.md) | cadam 프로젝트 사이클 카운터 |
| `_shared/refs/cadam/_index.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/refs/cadam/_index.md) | cadam 정본(second-brain) 참조 stub 인덱스 |
<!-- SECTION:END name=vault_assets -->
