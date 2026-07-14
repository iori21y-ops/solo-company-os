---
title: "audit 작업 노트"
type: audit-working-notes
status: draft
created: 2026-06-09
---

# audit 작업 노트

audit 규칙 확정 과정에서 결정된 사항을 시간순 한 줄로 누적. 정식 규칙은 audit-rules-*.md 로 승격.

## cross-source

- 2026-06-09 — brand 매칭 규칙: price_sources.brand 와 vehicles.brand 직접 문자열 비교. 예외 1건 'hyundai'='현대'. BRAND_MAP(generate-pricing) 미사용 — 죽은 매핑 4개(kia/genesis/kgm/renault) 포함, audit엔 부적합.

## semantic / freshness — 2026-07-14 대표 결정 (6주 반복 AMBER 종결)

- **B-2 (COV-2/SEM-2)** — 파워트레인별 실가격은 다르다(확정). 그러나 pricing은 모델 단위 저장이라 "K5 하이브리드 미수집"은 오탐 → 커버리지 매칭을 **모델 단위(파워트레인 접미사 제거)**로 완화. → audit-rules-semantic.md S1. 크롤러 파워트레인 세분화 수집은 **P2 설계 이관**. 진짜 미수집 = **테슬라 Model Y L**(별도 목록, 정보성).
- **B-3 (SEM-1)** — pricing.method NULL 정상(downstream은 conditions.product_type 사용, method 컬럼 미참조 확인). flag 금지. → S2.
- **B-4 (FRESH-3)** — finance_rates 갱신 기준 **분기(90일)** 채택·명문화. → freshness-thresholds.md v1.1.
- **FRESH-1 (vehicle_msrp)** — 소스통합 완료(commit 21ace25, vehicle_msrp→vehicle_trims, 소비처 0). verdict 표기를 "ops 크롤러 재실행"에서 "소스 통합 완료(vehicle_trims 정본)"로 정정. RED 해제.
- 위 반영 시 DATA-01 잔여 RED/AMBER 소거 → 다음 사이클 GREEN 복귀 기대.
