---
type: fact-block
title: 현대 아반떼 팩트블록 (quantitative · 2026년형 · 가솔린/LPG)
topic: avante-factblock-quant
subject: 현대 아반떼 (2026년형 CN7 · 준중형 세단 · 가솔린 1.6 / LPG 1.6)
date: 2026-06-20
data_source:
  - data/outputs/approved/verdict-avante-20260611.md (quantitative/referential GREEN)
created: 2026-06-20
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-013-factblock-batch-20260620]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-avante-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='avante' (쿼리 2026-06-20, 11행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='avante' (쿼리 2026-06-20, 4행)
data_gate: verdict-avante-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠
uncertified: 가격·이미지·구동방식(drive_type)·안전등급·트림별 옵션
flags:
  - "vehicles.body_type='SUV' — 오류. 아반떼는 준중형 세단. 데이터팀 수정 권고."
  - "vehicles.category='SUV' — 오류. 세단으로 수정 권고."
  - "vehicle_powertrains.drive_type null 전 행 — FWD(FF) 추정. 원문 확인 권고."
  - "curb_weight_kg null (가솔린 16\"+빌트인캠·17\"·18\" N Line) — raw_line에 '(C)' 표기값 있으나 DB 미파싱. 발행 전 확인 권고."
  - "LPG rows 중복 적재 — 3개 구성(15\"/16\"/17\") 행이 vehicle_powertrains에 2회씩 적재(총 6행, 유효 3행). 데이터팀 중복 정리 권고."
  - "vehicle_trims.base_price 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# 아반떼 팩트 블록 — quantitative (2026년형 · CN7 · 가솔린/LPG)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-avante-20260611 GREEN).  
> 인증 범위: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠.  
> drive_type null 전 행 — 아반떼는 FF(앞바퀴 굴림) 세단이나 DB 미기재, 발행 전 원문 확인 권고.  
> 가솔린 일부 행 curb_weight_kg null — raw_line "(C)" 표기 파싱 미처리. 수치 사용 전 확인 필요.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| body_type | ⚠️ 오류 | DB='SUV' → 아반떼는 준중형 세단. 데이터팀 수정 권고. |
| category | ⚠️ 오류 | DB='SUV' → 세단 수정 권고. |
| drive_type | ⚠️ null | FWD(FF) 추정. 원문 확인 필요. |
| curb_weight (일부) | ℹ️ null | 가솔린 16"+빌트인캠·17"·18" — raw_line "(C)" 표기값 DB 미파싱. |
| LPG 중복 적재 | ⚠️ 주의 | 3개 구성 각각 2행씩 적재(총 6행=유효 3행). 데이터팀 정리 권고. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 | vehicles.brand |
| 모델명 | 아반떼 | vehicles.name |
| 모델코드 | CN7 | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 준중형 | vehicles.segment |
| 카테고리 | 세단 (DB='SUV' 오류) | — |
| 연료 | 가솔린 1.6 / LPG 1.6 | vehicle_powertrains.fuel_kind |
| 배기량 | 가솔린 1,598cc / LPG 1,591cc | vehicle_powertrains.displacement_cc |
| 변속기 | 가솔린: 스마트스트림 IVT / LPG: 자동 6단 | vehicle_powertrains.engine (raw) |
| 구동방식 | — (null, FWD 추정) | vehicle_powertrains.drive_type |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 가솔린 1.6 · 스마트스트림 IVT

| 행 | 휠 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 | 비고 |
|---|---|---|---|---|---|---|---|---|
| A | **15"** | **15.0 km/ℓ** | 13.4 | 17.4 | 108 g/km | **1,260 kg** | **2등급** | — |
| B | **16"** | **14.8 km/ℓ** | 13.3 | 17.0 | 111 g/km | **1,265 kg** | **2등급** | — |
| C | **16"** | **14.6 km/ℓ** | 13.1 | 16.9 | 112 g/km | — (null) | **2등급** | 빌트인캠 적용 |
| D | **17"** | **14.3 km/ℓ** | 12.9 | 16.4 | 115 g/km | — (null) | **2등급** | — |
| E | **18"** | **13.8 km/ℓ** | 12.4 | 15.9 | 119 g/km | — (null) | **2등급** | N Line |

> ※ 공차중량 null(C·D·E행): raw_line에 1,265(C)/1,270(C)/1,320(C)kg 표기 있으나 DB 파싱 미처리. 수치 사용 전 데이터팀 확인 권고.

### LPG 1.6 · 자동 6단

| 행 | 휠 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|
| F | **15"** | **10.5 km/ℓ** | 9.3 | 12.4 | 124 g/km | **1,260 kg** | **4등급** |
| G | **16"** | **10.3 km/ℓ** | 9.1 | 12.1 | 126 g/km | **1,275 kg** | **4등급** |
| H | **17"** | **10.2 km/ℓ** | 9.0 | 12.0 | 127 g/km | **1,280 kg** | **4등급** |

> ※ LPG 3행이 DB에 각 2회씩 중복 적재(총 6행). 위 수치는 중복 제거 후 유효값. 데이터팀 정리 권고.

---

> **핵심 포인트:**
> - 가솔린 최고 연비: 15" 기준 복합 15.0 km/ℓ (2등급)
> - 가솔린 N Line 18": 복합 13.8 km/ℓ — 타 트림 대비 고속 위주 세팅
> - 빌트인캠 적용(16") 시 연비 0.2 km/ℓ 하락(14.8→14.6), CO2 1 g/km 증가
> - LPG: 전 휠 사이즈 4등급 / 도심(9.0~9.3) vs 고속(12.0~12.4) — 고속 주행 시 상대적 유리
> - 가솔린 vs LPG: 복합연비 기준 가솔린이 4~5 km/ℓ 우위, LPG는 연료비 단가 고려 필요

---

## 가솔린 연비 추이 (휠 사이즈별)

| 휠 | 복합 | 고속 | CO2 |
|---|---|---|---|
| 15" | 15.0 | 17.4 | 108 |
| 16" | 14.8 | 17.0 | 111 |
| 16"+빌트인캠 | 14.6 | 16.9 | 112 |
| 17" | 14.3 | 16.4 | 115 |
| 18" (N Line) | 13.8 | 15.9 | 119 |

> 15"→18" 전환 시 복합연비 1.2 km/ℓ 하락, CO2 11 g/km 증가.

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | 출고가 참고 |
|--------|-----------|
| 스마트 | 20,650,000원 |
| 모던 | 23,910,000원 |
| 인스퍼레이션 | 27,590,000원 |
| N라인 | 28,490,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 아반떼 2026 CN7 · 가솔린 1.6 · 복합 최대 15.0km/ℓ (2등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 아반떼 2026년형(CN7)은 1.6 가솔린과 1.6 LPG 두 가지 파워트레인을 제공하는 준중형 세단입니다.
가솔린 기준 최고 복합연비 15.0 km/ℓ(15" 기준, 도심 13.4 / 고속 17.4)로 에너지소비효율 2등급을 획득했으며,
LPG는 복합 10.2~10.5 km/ℓ(4등급)로 연료비 절감형 선택지를 제공합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대
모델: 아반떼 2026년형 (CN7)
세그먼트: 준중형 세단

[가솔린 1.6 · 스마트스트림 IVT]
배기량: 1,598cc
구동방식: FWD 추정 (DB null)
연비 (복합/도심/고속):
  15": 15.0 / 13.4 / 17.4 km/ℓ | CO2 108 | 1,260kg | 2등급
  16": 14.8 / 13.3 / 17.0 km/ℓ | CO2 111 | 1,265kg | 2등급
  16"+빌트인캠: 14.6 / 13.1 / 16.9 km/ℓ | CO2 112 | 2등급
  17": 14.3 / 12.9 / 16.4 km/ℓ | CO2 115 | 2등급
  18" (N Line): 13.8 / 12.4 / 15.9 km/ℓ | CO2 119 | 2등급

[LPG 1.6 · 자동 6단]
배기량: 1,591cc
연비 (복합/도심/고속):
  15": 10.5 / 9.3 / 12.4 km/ℓ | CO2 124 | 1,260kg | 4등급
  16": 10.3 / 9.1 / 12.1 km/ℓ | CO2 126 | 1,275kg | 4등급
  17": 10.2 / 9.0 / 12.0 km/ℓ | CO2 127 | 1,280kg | 4등급
```

### ④ 인포그래픽·카드 수치 스니펫
```
[가솔린 15"]  15.0km/ℓ | CO2 108g | 1,260kg | 2등급  ← 최고연비
[가솔린 16"]  14.8km/ℓ | CO2 111g | 1,265kg | 2등급
[가솔린 18" N Line]  13.8km/ℓ | CO2 119g | 2등급
[LPG 15"]  10.5km/ℓ | CO2 124g | 1,260kg | 4등급
※ 복합연비 기준 / drive_type DB null(FWD 추정)
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 구동방식 | vehicle_powertrains.drive_type null — 원문 확인 필요 |
| 공차중량 일부 | 가솔린 C·D·E행 curb_weight_kg null (raw_line "(C)" 파싱 미처리) |
| 트림별 옵션 스펙 | 미수집 |
| 안전 등급 | 미수집 |
| 하이브리드 모델 | avante-hybrid 별도 팩트블록 참조 (factblock-avante-hybrid-quant-20260615.md) |

---

_작성: 컨텐츠_  
_작성일: 2026-06-20_  
_data gate: verdict-avante-20260611.md (GREEN) · commit 8877504_
