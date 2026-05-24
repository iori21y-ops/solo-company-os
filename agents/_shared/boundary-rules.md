---
title: 에이전트 간 경계 규칙
last-updated: 2026-05-22
---

# 경계 규칙 모음

각 쌍의 경계는 양쪽 에이전트 SKILL.md에도 중복 기록됨.

<!-- SECTION:START name=pair_1_marketing_content -->
## 쌍 1: marketing ↔ content

**비유**: content = 재료 공급자, marketing = 요리사 겸 발행인

**경계 규칙**:
- content: 데이터를 사람이 보는 에셋으로 가공·비축
- marketing: content 에셋 + 자체 카피·트렌드로 발행 콘텐츠 완성

**판정 순서**:
1. 데이터가 뼈대인가? Yes → content 거침 → marketing 마감
2. 단순 카피·트렌드 글인가? Yes → marketing 단독

**회색지대 판정**:
| 케이스 | 담당 |
|--------|------|
| "아반떼 vs K3" 비교 카드뉴스 | content가 비교표 생성 → marketing이 카피·디자인 마감 |
| 자사 블로그 SEO 글 | marketing 주도, 필요시 content 에셋 인용 |
| /info/terms-comparison 페이지 | content가 팩트블록 생성 → marketing이 페이지 카피 마감 |
| 시즌 캠페인 글 (데이터 무관) | marketing 단독 |
| 약관 개정 알림 카드뉴스 | content가 변경점 요약 → marketing이 카드뉴스 |

**한 줄 테스트**:
- "이 산출물이 발행 채널에 즉시 나갈 수 있나?" Yes = marketing 최종 담당
- "이 산출물이 재사용 가능한 에셋인가?" Yes = content 최종 담당
<!-- SECTION:END name=pair_1_marketing_content -->

<!-- SECTION:START name=pair_2_content_data -->
## 쌍 2: content ↔ data

**비유**: data = 농장, content = 재료 공급자

**경계 규칙**:
- data: 구조화된 데이터 수집·검증·정합성. 사이트 표시용 표준 자산 포함
- content: data 결과를 사람이 보는 자산으로 재가공 (별도 발행·재사용용)

**판정 순서**:
1. 사이트가 자기 데이터 표시에 필요한 표준 자산인가? Yes → data
2. 별도 발행·재사용용 자산인가? Yes → content
3. 데이터+해석이 섞인 페이지 → 주된 가치로 귀속 (해석 우세면 content)

**회색지대 판정**:
| 케이스 | 담당 | 이유 |
|--------|------|------|
| WF-VI 전체 (360수집·흰배경·홈카드·뷰어) | data | 사이트 표준 표시 자산 |
| 카드뉴스용 차량 이미지 가공 | content | 별도 발행물용 재가공 |
| /cars/[slug] 기본 스펙표 | data | 단순 표시 |
| "이 차 추천 사유" 한줄평 | content | 해석 |
| 진단 결과 페이지 | content | 해석이 주된 가치 (계산 결과는 data 입력) |
| 정책·보조금 데이터 수집 | data | 원천 수집 |
| 월간 인사이트 리포트 | content | 해석·가공 |

**한 줄 테스트**:
- "이 산출물 없으면 사이트가 차량 정보를 못 보여주나?" Yes = data
- "이 산출물 없으면 마케팅·발행물이 못 만들어지나?" Yes = content
- 둘 다 Yes면 페이지 단위 주된 가치로 판단
<!-- SECTION:END name=pair_2_content_data -->

<!-- 신규 쌍 추가 위치: 다음 세션에서 여기 아래에 pair_3, pair_4 등 추가 -->

<!-- SECTION:START name=pair_3_sales_cs -->
## 쌍 3: sales ↔ cs

**비유**: sales = 회계·분석실 (데이터로 운영 방향 잡기), cs = 매장 직원 (고객·딜러와 직접 대화)

**경계선**: 이 산출물이 **사람에게 직접 발송되는가?**
- Yes → cs (고객·딜러 직접 대화 담당)
- No, 내부 의사결정용 데이터·분석·룰인가? → sales

**관계**: 인계가 아닌 **상호 공급**
- sales → cs: 스코어링 룰·응대 우선순위·가이드 제공
- cs → sales: 실제 응대 결과·고객 반응 피드백

**사업 모델 전제**:
랜테일러는 리드-딜러 중개 플랫폼. 계약은 딜러↔고객이 체결.
계약 후 차량 운영·보험·정비는 딜러 책임 → cs는 체결 전까지만 응대.
체결 후 컴플레인은 딜러를 통해 들어오는 경우만 cs가 1차 분류.

**판정 순서**:
1. 외부(고객·딜러)로 나가는 메시지·콘텐츠인가? → cs
2. 내부 분석·룰·리포트·대시보드인가? → sales
3. 양쪽 모두 해당? → 산출물을 분리 (예: cs는 메시지 초안, sales는 그 메시지의 효과 측정)

**회색지대 판정**:
| 케이스 | 담당 | 이유 |
|--------|------|------|
| 새 리드 1차 응대 메시지 | cs | 고객 직접 대화 |
| 리드 스코어링 룰 설계 | sales | 데이터 분석 |
| "이 리드 우량 여부" 판정 | sales | 룰 적용 |
| 우량 리드 우선 응대 메시지 | cs (sales 룰 활용) | 응대는 cs, 룰은 sales |
| CRM에 새 리드 추가 | cs | 응대 흐름 중 발생 |
| CRM 데이터 정합성 점검 | sales | 데이터 관리 |
| 진단 결과 → 고객 안내 | cs | 고객 메시지 |
| 진단 결과 통계 집계 | sales | 데이터 |
| 딜러 핸드오프 메시지 | cs | 딜러와 직접 대화 |
| 딜러별 응답률 분석 | sales | 성과 분석 |
| 채널별 ROI 계산 | sales | 분석 |
| 1차 컴플레인 응대 | cs | 직접 대화 |
| 컴플레인 패턴 분석 | sales | 데이터 |
| 주간 KPI 리포트 | sales | 내부 의사결정 |

**한 줄 테스트**:
- "이 산출물이 사람(고객·딜러)에게 직접 발송되는가?" Yes → cs
- "이 산출물이 사람에게 보이지 않고 내부 의사결정용인가?" Yes → sales

**위임 정책 참조**:
- cs 산출물(외부 발송) → `_shared/security/approval-required.md` 따름 (텔레그램 승인 필수)
- sales 산출물(내부 분석) → 대부분 `_shared/security/auto-allowed.md` 가능 (읽기·분석)
- 단, sales의 룰·스코어링이 cs 응대 우선순위를 바꾸는 경우 → approval-required
<!-- SECTION:END name=pair_3_sales_cs -->

<!-- SECTION:START name=pair_4_ops_data -->
## 쌍 4: ops ↔ data

**비유**: ops = 현장 엔지니어 (기계가 돌아가게), data = 품질 검사관 (결과가 맞는지 확인)

**경계선**: "실행 책임인가, 결과 책임인가?"
- ops: 파이프라인이 돌아가게 만드는 것 (실행·스케줄·장애복구·인프라)
- data: 파이프라인 결과가 맞게 나왔는지 확인하는 것 (검증·정합성·품질)

**관계**: 직렬 협력
- ops → data: 실행 완료 신호 전달
- data → ops: 결과 이상 감지 시 재실행 요청

**판정 순서**:
1. 파이프라인·서버·스케줄을 돌리거나 유지하는 행위인가? → ops
2. 파이프라인 결과물의 정확성·정합성을 확인하는 행위인가? → data
3. 양쪽 모두 필요한 작업? → 분리 실행 (ops가 먼저, data가 검증)

**회색지대 판정**:
| 케이스 | 담당 | 이유 |
|--------|------|------|
| 파서 스크립트 실행 | ops | 실행 행위 |
| 파서 결과 검증 (레코드 수·값 범위) | data | 결과 품질 확인 |
| GWP n8n 워크플로 실행 | ops | n8n 실행·스케줄 |
| GWP 글 품질 검증 | data → content | 내용 품질은 content까지 |
| Supabase Storage 버킷 생성·정리 | ops | 인프라 운영 |
| Supabase 데이터 정합성 점검 | data | 데이터 품질 |
| 서버 CPU·메모리·디스크 모니터링 | ops | 인프라 상태 |
| 데이터 이상치 감지 (레코드 누락·불일치) | data | 데이터 품질 |
| DB 마이그레이션 스키마 설계 | data | 데이터 구조 정의 |
| DB 마이그레이션 실행·롤백 | ops | 실행 행위 |
| Vercel 배포 실행 | ops | 실행 행위 |
| 배포 후 사이트 표시 데이터 확인 | data | 결과 검증 |
| n8n 워크플로 신규 구축 | ops | 실행 인프라 구성 |
| 워크플로 입출력 데이터 스펙 정의 | data | 데이터 품질 기준 |
| 서버 에러 로그 분석 | ops | 인프라 상태 |
| 비즈니스 로그 분석 (전환율·유입) | data → sales | 비즈니스 데이터 |

**한 줄 테스트**:
- "이 산출물이 파이프라인을 돌리거나 서버를 유지하는 행위인가?" Yes → ops
- "이 산출물이 파이프라인 결과의 정확성·정합성을 확인하는 행위인가?" Yes → data

**위임 정책 참조**:
- ops 읽기·모니터링 → `_shared/security/auto-allowed.md`
- ops 실행·배포·재시작 → `_shared/security/approval-required.md` (텔레그램 승인 필수)
- data 검증·조회 → `_shared/security/auto-allowed.md`
- 운영 서버 재부팅·rm -rf → `_shared/security/delegation-blacklist.md` (절대 금지)
<!-- SECTION:END name=pair_4_ops_data -->

<!-- SECTION:START name=pair_5_strategy_all -->
## 쌍 5: strategy ↔ 전체

**경계선**: "단일 에이전트 소관이면 해당 에이전트, 복수 에이전트에 걸치거나 사업 방향 판단이면 strategy"

**strategy 개입 조건** (4가지, 이 중 하나라도 해당하면 strategy):
1. 복수 에이전트 간 우선순위 충돌
2. 신규 사업 방향·기능 도입 여부 판단
3. 리소스(시간·비용) 배분 결정
4. 분기·월간 목표 설정 및 리뷰

**원칙**: strategy는 실무에 개입하지 않는다. 경계가 확정된 영역의 실무 판단은 해당 에이전트가 자율 수행.

**회색지대 판정**:
| 케이스 | 담당 | 이유 |
|--------|------|------|
| marketing 내부 콘텐츠 우선순위 결정 | marketing | 단일 에이전트 소관 |
| marketing + content 리소스 배분 충돌 | strategy | 복수 에이전트 경합 |
| data 정합성 이슈 — data 자체 해결 가능 | data | 단일 에이전트 소관 |
| data 정합성 이슈 — ops 투입 필요 | strategy 조율 | 복수 에이전트 투입 |
| 신규 서비스(정책매칭 등) 착수 판단 | strategy | 사업 방향 판단 |
| 특정 에이전트 작업량 과부하 | strategy | 리소스 재배분 |
| 경계 미확정 영역의 업무 귀속 판단 | strategy | 에이전트 간 조율 |
| 주간 KPI 리뷰 후 다음 주 우선순위 | strategy | 전체 목표 재조정 |

**한 줄 테스트**:
- "이 판단이 단일 에이전트 내에서 끝나는가?" Yes → 해당 에이전트
- "이 판단이 복수 에이전트 또는 사업 방향에 걸치는가?" Yes → strategy

**현 단계 위임**: 불가 — 파운더 직접 판단 영역. 멀티에이전트 자율화 후 재정의.
<!-- SECTION:END name=pair_5_strategy_all -->

<!-- SECTION:START name=pair_6_legal_finance -->
## 쌍 6: legal ↔ finance

**경계선**: "돈의 흐름이면 finance, 규정·계약이면 legal"

**판정 기준**:
- "금액이 오가는 행위인가?" Yes → finance
- "규정·계약 문구를 다루는가?" Yes → legal
- 둘 다 해당하면 → 산출물 분리 (계약 구조는 legal, 금액 산정은 finance)

**회색지대 판정**:
| 케이스 | 담당 | 이유 |
|--------|------|------|
| 딜러 제휴 계약서의 계약 구조·조항 | legal | 규정·계약 |
| 딜러 제휴 계약서의 수수료 금액 산정 | finance | 돈의 흐름 |
| 세금 신고 자료 준비 | finance | 돈의 흐름 |
| 세법 해석·법적 요건 확인 | legal | 규정 해석 |
| 환불 정책 문구·약관 수립 | legal | 규정·정책 |
| 환불 금액 처리·회계 반영 | finance | 돈의 흐름 |
| 개인정보 관련 과징금 규정 위반 여부 | legal | 규정 위반 |
| 과징금 회계 처리 | finance | 돈의 흐름 |

**한 줄 테스트**:
- "이 산출물이 금액·정산·집계를 다루는가?" Yes → finance
- "이 산출물이 약관·계약·규제를 다루는가?" Yes → legal

**현 단계 위임**: 둘 다 불가 — 실거래·법적 문서는 blacklist 대상. 파운더 직접 수행.
<!-- SECTION:END name=pair_6_legal_finance -->
