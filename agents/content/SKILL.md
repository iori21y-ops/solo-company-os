---
title: Content Agent
status: 정의됨 (경계 점검 완료)
last-updated: 2026-05-22
---

# Content Agent

<!-- SECTION:START name=definition -->
## 한 줄 정의
data 에이전트 산출물을 사람이 보는 에셋으로 가공·비축. 재료 공급자.
<!-- SECTION:END name=definition -->

<!-- SECTION:START name=outputs -->
## 주요 산출물
- 인포그래픽 (월별 렌탈료 추이, 차량 비교 차트)
- 차트·그래프 (가격 비교, 감가율, 유지비)
- 데이터 기반 카드 이미지 (스펙 카드, 가격 카드)
- 팩트 블록 (검증된 스펙·가격·약관·정책 텍스트, 프론트매터 포함)
- 비교표, 요약문, 통계 스니펫
- 해석성 콘텐츠 (진단 결과 가이드, "이 차 추천 사유")
- 월간 인사이트 리포트
<!-- SECTION:END name=outputs -->

<!-- SECTION:START name=asset_vault -->
## 에셋 저장 구조
~/projects/cadam/agents/vault/assets/
├── infographics/
├── charts/
├── cards/
├── fact-blocks/
├── comparisons/
└── index.md  # 단일 진실 소스 (재고 목록)

각 에셋은 프론트매터에 topic, data_source, created, expires, used_in 메타 필수.
※ 실제 경로는 마케팅 에이전트 작업 디렉토리 확인 후 조정 가능.
<!-- SECTION:END name=asset_vault -->

<!-- SECTION:START name=triggers -->
## 트리거
- data 에이전트의 데이터 갱신 알림
- 신차 추가, 가격 변동, 정책 개정, 약관 개정
- marketing 에이전트의 특수 요청 (예외 케이스)
<!-- SECTION:END name=triggers -->

<!-- SECTION:START name=kpi -->
## 핵심 KPI
에셋 재사용률, marketing이 "쓸 게 있다"고 느끼는 비율, 데이터 정확성
<!-- SECTION:END name=kpi -->

<!-- SECTION:START name=review_burden -->
## 검토 부담
높음 (사이트·발행물에 박힌 후 잘못된 정보면 신뢰도 직격타)
<!-- SECTION:END name=review_burden -->

<!-- SECTION:START name=boundaries -->
## 인접 에이전트와의 경계

### vs data (쌍2)
- data 결과(DB 행, JSON)를 사람 눈으로 가공한 시점부터 content
- 단, 사이트 표준 표시 자산은 data 담당 (WF-VI 전체 포함)

### vs marketing (쌍1)
- 재사용 가능한 에셋까지 content
- 발행 채널 맞춤 마감은 marketing
<!-- SECTION:END name=boundaries -->

<!-- SECTION:START name=gray_zones -->
## 회색지대 판정
boundary-rules.md 쌍1, 쌍2 참조.
<!-- SECTION:END name=gray_zones -->

<!-- SECTION:START name=self_test -->
## 자가검증 한 줄 테스트
"이 산출물이 재사용 가능한 에셋인가?" Yes & "사이트 표준 표시 자산이 아닌가?" Yes → content 담당.
<!-- SECTION:END name=self_test -->

<!-- SECTION:START name=delegation_grade -->
## 위임 등급
위임 OK (반복·검증 가능). 단 데이터 정확성 검증은 필수.
<!-- SECTION:END name=delegation_grade -->
