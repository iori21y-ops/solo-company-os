---
type: fact-block
title: 기아 레이 EV 팩트블록 (quantitative · 2026년형)
topic: ray-ev-factblock-quant
subject: 기아 레이 EV (2026년형 · 전기 경형)
date: 2026-06-30
data_source:
  - data/outputs/approved/verdict-ray-ev-20260611.md (quantitative/referential GREEN)
created: 2026-06-30
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-025-factblock-batch-20260630]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-ray-ev-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='ray-ev' (쿼리 2026-06-30, 2행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='ray-ev' (쿼리 2026-06-30, 2행)
data_gate: verdict-ray-ev-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 전비(복합/도심/고속)·주행거리·공차중량·에너지등급
uncertified: 가격·이미지·휠사이즈·배터리용량·안전등급·트림별 옵션
flags:
  - "vehicles.body_type null — 경형 밴/해치백 추정. 데이터팀 보완 권고."
  - "vehicles.model_code null — DB 미입력."
  - "vehicles.segment null — DB 미입력."
  - "vehicle_powertrains.drive_type null 전 행 — FWD 추정. 원문 확인 권고."
  - "vehicle_powertrains.wheel null 전 행 — 휠사이즈 미수록."
  - "raw_line '265/133.5' 단위 불명확 → 배터리 수치 발행 금지."
  - "vehicle_trims.drive_type·wheel_size 전 행 null."
---

# 레이 EV 팩트 블록 — quantitative (2026년형 · 전기)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-ray-ev-20260611 GREEN).  
> 인증 범위: 전비(복합/도심/고속)·주행거리·공차중량·에너지등급.  
> 배터리 용량·휠사이즈·트림별 옵션 등은 인증 범위 외.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| body_type | ℹ️ null | 경형 밴/해치백 추정. 데이터팀 보완 권고. |
| model_code | ℹ️ null | DB 미입력. |
| drive_type | ℹ️ null | FWD 추정. 발행 전 원문 확인 권고. |
| 휠사이즈 | ℹ️ null | vehicle_powertrains.wheel 전 행 null. |
| 배터리 수치 | 🚫 발행 금지 | raw_line '265/133.5' 단위 불명확 — 사용 금지. |
| 가격 데이터 | 📌 참고용 | 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 기아 (KIA) | vehicles |
| 모델명 | 레이 EV (Ray EV) | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 카테고리 | EV (경형 전기차) | vehicles.category |
| 연료 | 전기 | vehicle_powertrains.fuel_kind |
| 구동방식 | FWD 추정 (DB null) | raw_line |
| 에너지등급 | 2등급 (전 구성) | vehicle_powertrains.energy_grade |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

| 행 | 구분 | 전비(복합) | 전비(도심) | 전비(고속) | 주행거리(복합) | 도심 | 고속 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|---|
| A | **EV (일반)** | **5.1 km/kWh** | 6.0 | 4.4 | **205 km** | 233 km | 171 km | **1,295 kg** | **2등급** |
| B | **EV 밴 (1인승/2인승)** | **5.1 km/kWh** | 6.0 | 4.4 | **205 km** | 233 km | 171 km | **1,290 kg** | **2등급** |

> **핵심 포인트:**
> - 복합 전비 5.1 km/kWh, 주행거리 205 km — 경형 전기차 기준 준수한 수준
> - 밴 구성(1인승/2인승)이 일반 대비 5 kg 경량 (1,290 vs 1,295 kg)
> - 전비·주행거리는 동일 — 구성(승용/밴)에 따른 수치 차이 없음
> - 도심 전비(6.0 km/kWh)가 고속(4.4 km/kWh)보다 36% 높음 — 도심 주행에 유리한 경형 특성

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | drive_type | wheel_size |
|--------|-----------|-----------|
| 라이트 | null | null |
| 에어 | null | null |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
기아 레이 EV 2026 · 전기 경형 · 복합 전비 5.1km/kWh · 주행거리 205km (2등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
기아 레이 EV 2026년형은 경형 전기차로, 복합 전비 5.1 km/kWh에 인증 주행거리 205 km를 기록합니다.
도심 전비 6.0 km/kWh로 시내 주행 효율이 높으며, 에너지 효율 2등급 인증을 획득했습니다.
승용과 밴(1인승/2인승) 두 가지 구성으로 제공되며, 공차중량은 1,290~1,295 kg입니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 기아
모델: 레이 EV 2026년형
연료: 전기
구동방식: FWD 추정
에너지등급: 2등급
전비 (복합): 5.1 km/kWh
전비 (도심): 6.0 km/kWh
전비 (고속): 4.4 km/kWh
주행거리 (복합): 205 km
주행거리 (도심): 233 km
주행거리 (고속): 171 km
공차중량: 1,295 kg (승용) / 1,290 kg (밴)
구성: 승용 / EV 밴 (1인승·2인승)
트림: 라이트, 에어
```

### ④ 인포그래픽·카드 수치 스니펫
```
[레이 EV 2026]
전비 5.1km/kWh | 주행거리 205km | 공차중량 1,295kg | 2등급
※ 복합 기준 / 승용 기준 / 환경부 인증
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 verdict 미인증 |
| 배터리 용량 | raw_line 수치 단위 불명확 — 발행 금지 |
| 휠사이즈 | vehicle_powertrains.wheel null |
| 트림별 옵션 | 미수집 |
| 안전 등급 | 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-30_  
_data gate: verdict-ray-ev-20260611.md (GREEN) · commit 8877504_
