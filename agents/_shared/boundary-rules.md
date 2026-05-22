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
