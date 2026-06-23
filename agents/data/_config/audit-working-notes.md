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
