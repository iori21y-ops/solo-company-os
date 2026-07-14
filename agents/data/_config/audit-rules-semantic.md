---
title: "의미 정합성 점검 규칙"
type: audit-rules
status: draft
created: 2026-05-27
---

# 의미 정합성 점검 규칙

값 의미 무결성 (오타, 잘못된 카테고리, 의미 충돌 등).

## 운영 원칙

- 이 파일은 에이전트 운영 설정. 학습 페이지(wiki)와 분리.
- audit 사이클 누적에 따라 규칙/임계 보정 가능 (사람 승인 필요).
- 변경 시 사이클 프론트매터 `rules_applied`에 영향 명시.

## 규칙 (2026-07-14 대표 결정 반영)

### S1. 커버리지 매칭 = 모델 단위 (파워트레인 접미사 무시)
`vehicles.name`("K5 하이브리드")과 `pricing.car_model`("K5") 대조 시, **파워트레인 구분 접미사(하이브리드/일렉트릭/EV/PHEV/LPG 등)를 제거한 모델 단위로 매칭**한다.
- 근거: pricing은 **모델 단위**로만 car_model을 저장한다(파워트레인 세분화 안 함). "K5 하이브리드 pricing 미수집" 류는 **문자열 불일치 오탐**이므로 COV/SEM에서 flag 금지.
- 확정 사실(대표 2026-07-14): 파워트레인별 실가격은 **실제로 다르다**(가격표 축 조사 근거). 다만 pricing 세분화 수집은 **P2 설계로 이관**됐으므로, 그 전까지 모델 단위 pricing 존재 = 정상(GREEN)으로 판정.
- **예외(진짜 미수집, 별도 목록 유지)**: 모델 접미사 제거 후에도 car_model에 없는 신규 트림 → 실제 갭. 현재 확인분: **테슬라 `Model Y L`**(pricing에 "Model Y"만 존재). 이건 GREEN 아님 → "미수집 목록"에 별도 표기(RED 아닌 정보성).

### S2. pricing.method NULL 은 정상 (flag 금지)
`pricing.method`(장기렌트/리스/할부) 컬럼이 NULL인 것은 **결함 아님**.
- 근거: 상품 구분은 `pricing.conditions->>product_type`(jsonb)로 저장·소비된다. downstream(`cadam-web/src/lib/estimatePricing.ts`)이 `conditions.product_type==='rent'`를 읽고 **method 컬럼은 아무도 참조 안 함**(2026-07-14 확인). method 컬럼은 과거 레거시 잔재(is_active=false 11건에만 값 존재).
- 따라서 SEM에서 method-NULL 비율을 flag 하지 않는다.
