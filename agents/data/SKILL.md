---
title: Data Agent
status: 정의됨 (경계 점검 완료 — 쌍2·쌍4)
last-updated: 2026-05-25
---

# Data Agent

<!-- SECTION:START name=definition -->
## 한 줄 정의
사실 수집·검증·정합성 유지. DB와 사이트 표준 표시 자산 책임. 농장.
<!-- SECTION:END name=definition -->

<!-- SECTION:START name=outputs -->
## 주요 산출물
- 차량 스펙·가격 크롤링 결과 (Supabase 저장)
- DB 정합성 (랜테일러 4자정합성 등)
- 외부 시장조사 데이터 (정책, 보조금, 환율, 가격 동향)
- 데이터 갱신 알림
- 사이트 표준 표시 자산 (WF-VI 전체: 360 수집, 흰배경 가공, 홈카드, 뷰어)
<!-- SECTION:END name=outputs -->

<!-- SECTION:START name=triggers -->
## 트리거
- 스케줄 (가격 크롤링, 환율 갱신)
- 외부 변동 감지 (신차 발표, 정책 변경)
- 사이트 자산 갱신 필요 (신차 등록 시 이미지 수집)
<!-- SECTION:END name=triggers -->

<!-- SECTION:START name=kpi -->
## 핵심 KPI
데이터 정확성, 정합성 무결성, 갱신 적시성
<!-- SECTION:END name=kpi -->

<!-- SECTION:START name=review_burden -->
## 검토 부담
높음 (모든 하위 에이전트의 입력 — 오염 시 전체 오염)
<!-- SECTION:END name=review_burden -->

<!-- SECTION:START name=boundaries -->
## 인접 에이전트와의 경계

### vs content (쌍2)
- 구조화 데이터·DB·사이트 표준 표시 자산까지 data
- 사람이 보는 별도 발행·재사용 자산부터 content

### vs ops (쌍4) — 경계선: "실행 책임인가, 결과 책임인가?"
- ops: 파이프라인이 돌아가게 만드는 것 (실행·스케줄·장애복구·인프라)
- data: 파이프라인 결과가 맞게 나왔는지 확인하는 것 (검증·정합성·품질)
- 관계: 직렬 협력. ops가 실행 → data가 결과 검증 → 이상 시 data가 ops에 재실행 요청
- 상세는 boundary-rules.md 쌍4 참조
<!-- SECTION:END name=boundaries -->

<!-- SECTION:START name=gray_zones -->
## 회색지대 판정
boundary-rules.md 쌍2 참조.
<!-- SECTION:END name=gray_zones -->

<!-- SECTION:START name=self_test -->
## 자가검증 한 줄 테스트
"이 산출물 없으면 사이트가 차량 정보를 못 보여주나?" Yes → data 담당.
<!-- SECTION:END name=self_test -->

<!-- SECTION:START name=delegation_grade -->
## 위임 등급
위임 OK (반복·검증 가능). 단 검증 로직 자체는 사람이 설계.
<!-- SECTION:END name=delegation_grade -->
