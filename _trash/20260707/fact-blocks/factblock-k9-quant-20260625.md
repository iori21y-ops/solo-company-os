---
type: fact-block
title: 기아 K9 팩트블록 (quantitative · 2026년형)
topic: k9-factblock-quant
subject: 기아 K9 (2026년형 · 3.8가솔린/3.3터보가솔린 대형 세단)
date: 2026-06-25
data_source:
  - data/outputs/approved/verdict-k9-20260611.md (quantitative/referential GREEN)
created: 2026-06-25
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-018-factblock-batch-20260625]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-k9-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='k9' (쿼리 2026-06-25, 10행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='k9' (쿼리 2026-06-25, 8행)
data_gate: verdict-k9-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·공차중량·구동방식·휠·에너지등급
uncertified: 가격·이미지·CO2
flags:
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "co2_emission 전 행 null — 미수집. CO2 수치 콘텐츠 사용 금지."
  - "3.3T AWD 19\" 행 2건 존재 (빌트인 캠/표준) — 빌트인 캠 행 curb_weight null, fuel_eff_city null. 표준 행(8.1 km/L, 2,075 kg) 우선 사용."
  - "3.8 2WD 18\" 행 2건 존재 (빌트인 캠/표준) — 빌트인 캠 행 curb_weight null."
  - "3.8 2WD 19\" 행 2건 존재 (빌트인 캠/표준) — 빌트인 캠 행 curb_weight null."
  - "3.8 AWD(18\"/19\") fuel_eff_city/highway null — raw_line 파싱 오류(\"7. 3\" 형식). 복합 연비만 확인 가능. 데이터팀 재파싱 권고."
  - "vehicle_trims.drive_type 전 행 null — 가격 참고용으로만 사용."
  - "vehicle_trims.base_price 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# K9 팩트 블록 — quantitative (2026년형 · 가솔린)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-k9-20260611 GREEN).  
> 인증 범위: 연비(km/L)·공차중량·구동방식·휠·에너지등급.  
> CO2 배출량: DB 미수집 — 콘텐츠 사용 금지.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| model_code | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| CO2 | ⚠️ null 전 행 | 미수집. 콘텐츠 사용 금지. |
| 3.3T AWD 19" 중복 행 | ⚠️ 요확인 | 빌트인 캠(8.0, curb null) / 표준(8.1, 2,075 kg) 2건 공존. |
| 3.8 AWD 도심·고속 연비 | ⚠️ 파싱오류 | fuel_eff_city/highway null (raw_line "7. 3" 파싱 오류). 복합 연비만 유효. |
| 빌트인 캠 행 공차중량 | ℹ️ null | 빌트인 캠 장착 행은 curb_weight 전 null — 표준 행 공차중량 참조. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 기아 (KIA) | vehicles.brand |
| 모델명 | K9 | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 대형 | vehicles.segment |
| 카테고리 | 세단 | vehicles.category |
| 연료 | 가솔린 | vehicle_powertrains.fuel_kind |
| 엔진 라인업 | 3.8 가솔린 8단 자동 / 3.3 가솔린 터보 8단 자동 | vehicle_powertrains.engine |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> CO2 전 행 null — 표에서 제외.  
> 빌트인 캠 행은 별도 표시, 공차중량 null인 경우 "—" 표기.

### 3.8 가솔린 8단 자동 (3,778cc)

| 행 | 휠 | 구동 | 비고 | 연비(복합) | 연비(도심) | 연비(고속) | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|
| A | 18" | 2WD | 표준 | **9.0 km/L** | 7.8 | 11.0 | 1,930 kg | **5등급** |
| B | 18" | 2WD | 빌트인 캠 | 8.8 km/L | 7.6 | 10.8 | — | **5등급** |
| C | 18" | AWD | 표준 | 8.4 km/L | — ⚠️ | — ⚠️ | 2,000 kg | **5등급** |
| D | 19" | 2WD | 표준 | **8.8 km/L** | 7.6 | 10.7 | 1,940 kg | **5등급** |
| E | 19" | 2WD | 빌트인 캠 | 8.6 km/L | 7.5 | 10.5 | — | **5등급** |
| F | 19" | AWD | 표준 | 8.3 km/L | — ⚠️ | — ⚠️ | 2,010 kg | **5등급** |

> ⚠️ 행C·F AWD: fuel_eff_city/highway DB null (raw_line 파싱 오류). 복합 연비만 유효.

### 3.3 가솔린 터보 8단 자동 (3,342cc)

| 행 | 휠 | 구동 | 비고 | 연비(복합) | 연비(도심) | 연비(고속) | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|
| G | 19" | 2WD | 빌트인 캠 | 8.6 km/L | — | 10.6 | — | **5등급** |
| H | 19" | AWD | 빌트인 캠 | 8.0 km/L | 6.8 | 10.0 | — | **5등급** |
| I | 19" | AWD | 표준 | **8.1 km/L** | 7.0 | 10.1 | 2,075 kg | **5등급** |

> ※ 3.3T 표준 행 공차중량: AWD 2,075 kg (2WD 표준 행 미수집 — DB 없음).

> **핵심 포인트:**
> - **전 조합 5등급** — 대형 가솔린 세단 특성상 고연비 대안 없음
> - 3.8 가솔린 최고 연비: 18" 2WD 표준 — **9.0 km/L**
> - 3.3T 최고 연비: 19" 2WD 빌트인 캠 — **8.6 km/L** (표준 2WD 행 미수집)
> - 빌트인 캠 장착 시 연비 0.2~0.3 km/L 하락 (3.8 기준)
> - AWD vs 2WD: 복합 연비 약 0.5~0.7 km/L 차이

---

## 연비 요약

| 엔진 | 최고연비 조합 | 연비(복합) | 에너지등급 |
|------|-------------|-----------|-----------|
| 3.8 가솔린 | 18" 2WD (표준) | **9.0 km/L** | **5등급** |
| 3.3T 가솔린 | 19" 2WD (빌트인 캠) | 8.6 km/L | **5등급** |

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.  
> ⚠️ drive_type 전 행 null — 트림별 구동방식 미분리.

| 트림명 | 출고가 참고 |
|--------|-----------|
| 3.8 가솔린 플래티넘 | 60,410,000원 |
| 3.3 가솔린 터보 플래티넘 | 66,960,000원 |
| 3.8 가솔린 플래티넘 베스트 셀렉션 Ⅰ | 69,080,000원 |
| 3.3 가솔린 터보 플래티넘 베스트 셀렉션 Ⅰ | 74,840,000원 |
| 3.8 가솔린 마스터즈 | 75,290,000원 |
| 3.3 가솔린 터보 마스터즈 | 80,040,000원 |
| 3.8 가솔린 마스터즈 베스트 셀렉션 Ⅱ | 82,390,000원 |
| 3.3 가솔린 터보 마스터즈 베스트 셀렉션 Ⅱ | 87,140,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
기아 K9 2026 · 대형 세단 · 3.8가솔린 18" 2WD 기준 연비 9.0km/L(5등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
기아 K9 2026년형은 3.8 가솔린과 3.3 가솔린 터보 두 가지 파워트레인을 갖춘 플래그십 대형 세단입니다.
3.8 가솔린 18인치 2WD 기준 복합 연비 9.0 km/L(5등급), 3.3 터보는 19인치 기준 8.6 km/L(5등급)을 기록합니다.
트림은 플래티넘·마스터즈 두 단계로 구성되며, 출고가는 6,000만 원대부터 시작합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 기아(KIA)
모델: K9 (2026년형)
세그먼트: 대형 세단
연료: 가솔린
엔진: 3.8 가솔린 자동 8단 / 3.3 가솔린 터보 자동 8단
구동방식: 2WD / AWD (엔진별 상이)
연비(대표·3.8가솔린 18" 2WD): 9.0 km/L (5등급)
연비(대표·3.8가솔린 18" AWD): 8.4 km/L (5등급, 도심·고속 미확인)
연비(대표·3.3T 19" AWD): 8.1 km/L (5등급)
공차중량: 1,930~2,075 kg (엔진·구동·휠 조합별, 빌트인 캠 행 제외)
트림: 플래티넘·마스터즈 (가격 미인증, 참고용)
```

### ④ 인포그래픽·카드 수치 스니펫
```
[3.8가솔린 18" 2WD]  9.0km/L | 1,930kg | 5등급  ← 최고연비(3.8)
[3.8가솔린 18" AWD]  8.4km/L | 2,000kg | 5등급  ※ 도심·고속 미확인
[3.8가솔린 19" 2WD]  8.8km/L | 1,940kg | 5등급
[3.8가솔린 19" AWD]  8.3km/L | 2,010kg | 5등급  ※ 도심·고속 미확인
[3.3T 19" AWD]       8.1km/L | 2,075kg | 5등급
※ CO2 미수집(DB null)
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| CO2 배출량 | DB 미수집 (전 행 null) |
| 3.8 AWD 도심·고속 연비 | raw_line 파싱 오류 — 데이터팀 재파싱 권고 |
| 최고출력·토크 | vehicle_powertrains 미수집 |
| 트림별 구동방식 | vehicle_trims.drive_type null |

---

_작성: 컨텐츠_  
_작성일: 2026-06-25_  
_data gate: verdict-k9-20260611.md (GREEN) · commit 8877504_
