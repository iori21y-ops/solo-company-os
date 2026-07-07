---
type: fact-block
title: 현대 아이오닉 5 팩트블록 (quantitative · NE1)
topic: ioniq5-factblock-quant
subject: 현대 아이오닉 5 (NE1 2025년형)
date: 2026-06-13
data_source:
  - data/outputs/approved/verdict-ioniq5-20260611.md (quantitative/referential GREEN)
created: 2026-06-13
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-006-factblock-batch-20260613]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-ioniq5-20260611.md
  - DB: vehicle_powertrains WHERE slug='ioniq5' (쿼리 2026-06-13)
  - DB: vehicle_trims WHERE slug='ioniq5' (트림명·가격)
data_gate: verdict-ioniq5-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 전비·주행거리·공차중량·구동방식·휠·배터리(Wh)
uncertified: 가격·이미지·CO2(EV 미해당)
flags:
  - "Row 5 (19\" drive_type=DB에서 2WD·raw_line 239/325kW 모터→AWD 사양과 일치): DB drive_type 컬럼과 raw_line 모터 사양 불일치. 팩트블록에서 해당 행 별도 표기, 데이터팀 확인 권고."
  - "vehicle_trims.base_price는 가격 verdict 미인증 범위 — 참고용으로만 기재, 발행 시 별도 가격 인증 필요."
  - "vehicles.year=2025 (2026이 아님) — DB 현행 값. 연식 표기 주의."
---

# 아이오닉 5 팩트 블록 — quantitative (NE1 · 전기)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-ioniq5-20260611 GREEN).  
> 인증 범위: 전비·주행거리·공차중량·구동방식·휠. 가격·이미지 미포함.  
> CO2 배출량: 전기차 해당 없음 (N/A).

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| 19" Row 5 drive_type 불일치 | ⚠️ 요확인 | DB=2WD 기재이나 raw_line 모터 사양 239/325kW(AWD 사양). 데이터팀 확인 권고. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price는 가격 verdict 미인증. 발행 전 별도 인증 필수. |
| 연식 | ℹ️ 확인 | vehicles.year = 2025 (DB 기준). 표기 시 2025년형 또는 최신 연식 확인 필요. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (HYUNDAI) | vehicles.brand |
| 모델명 | 아이오닉 5 (IONIQ5) | vehicles.name |
| 모델코드 | NE1 | vehicles.model_code |
| 연식 | 2025년형 | vehicles.year |
| 세그먼트 | 중형 | vehicles.segment |
| 연료 | 전기 (EV) | vehicle_powertrains.fuel_kind |
| 변속기 | 1단 감속기 (전기차 공통) | — |
| 구동방식 | 2WD / AWD | vehicle_powertrains.drive_type (GREEN) |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 19인치 파워트레인

| 배터리 | 모터(kW) | 구동 | 전비(복합) | 전비(도심) | 전비(고속) | 주행거리 | 공차중량 |
|--------|----------|------|-----------|-----------|-----------|---------|---------|
| Standard 523 Wh | 124.9 / 170 kW | 2WD | 5.1 km/kWh | 5.7 | 4.6 | 368 km | 1,890 kg |
| Long Range 697 Wh | 168 / 229 kW | 2WD | 5.2 km/kWh | 5.8 | 4.6 | 485 km | 2,015 kg |
| Long Range 697 Wh + 캠 | 168 / 229 kW | 2WD | 5.1 km/kWh | 5.6 | 4.5 | 478 km | 2,015 kg |
| ⚠️ Long Range 697 Wh * | 239 / 325 kW | (DB:2WD) | 4.8 km/kWh | 5.2 | 4.3 | 451 km | 2,120 kg |

> ⚠️ * 4번째 행: raw_line 기준 239/325kW(AWD 모터 사양)이나 DB drive_type=2WD. 데이터팀 확인 필요. 본 블록에서는 DB 값 그대로 기재.

### 20인치 파워트레인

| 배터리 | 모터(kW) | 구동 | 전비(복합) | 전비(도심) | 전비(고속) | 주행거리 | 공차중량 |
|--------|----------|------|-----------|-----------|-----------|---------|---------|
| Long Range 697 Wh | 168 / 229 kW | 2WD | 4.9 km/kWh | 5.3 | 4.4 | 453 km | 2,025 kg |
| N Line + 캠 697 Wh | 168 / 229 kW | 2WD | 4.7 km/kWh | 5.2 | 4.1 | 441 km | 2,055 kg |
| Long Range 697 Wh | 239 / 325 kW | AWD | 4.5 km/kWh | 4.9 | 4.0 | 425 km | 2,130 kg |
| N Line AWD + 캠 697 Wh | 239 / 325 kW | AWD | 4.4 km/kWh | 4.8 | 3.9 | 411 km | 2,160 kg |

---

## 트림 라인업 (vehicle_trims · 트림명·가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | 출고가 참고 |
|--------|-----------|
| 이-밸류 | 49,930,000원 |
| 익스클루시브 | 52,980,000원 |
| 롱레인지 | 53,340,000원 |
| N라인 | 59,510,000원 |
| 프레스티지 | 62,300,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 아이오닉 5 NE1 · 전기 2WD/AWD · 19"/20" · 최대 485km 주행
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 아이오닉 5(IONIQ 5) NE1은 스탠다드(523Wh)와 롱레인지(697Wh) 두 가지
배터리 옵션을 갖춘 중형 전기 SUV입니다.
롱레인지 2WD 19" 기준 복합 전비 5.2 km/kWh, 1회 충전 주행거리 최대 485 km를 달성합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대 (HYUNDAI)
모델: 아이오닉 5 (IONIQ5) NE1
연식: 2025년형
세그먼트: 중형
연료: 전기 (EV)
배터리: 스탠다드 523Wh / 롱레인지 697Wh
구동방식: 2WD / AWD
전비(대표): 5.2 km/kWh (롱레인지 2WD 19")
주행거리(대표): 485 km (롱레인지 2WD 19")
공차중량: 1,890~2,160 kg (배터리·구동·휠 조합별)
트림: 이-밸류·익스클루시브·롱레인지·N라인·프레스티지
```

### ④ 인포그래픽·카드 수치 스니펫
```
[Standard 2WD 19"] 523Wh | 5.1km/kWh | 368km | 1,890kg
[Long Range 2WD 19"] 697Wh | 5.2km/kWh | 485km | 2,015kg
[Long Range AWD 20"] 697Wh | 4.5km/kWh | 425km | 2,130kg
[N Line AWD 20"] 697Wh | 4.4km/kWh | 411km | 2,160kg
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| CO2 배출량 | 전기차 해당 없음 |
| 충전 속도 / 충전 시간 | vehicle_powertrains 미포함 |
| 트림별 제원 수치 | vehicle_trims 수치 불완전 (DB 일부 null) |

---

_작성: 컨텐츠_  
_작성일: 2026-06-13_  
_data gate: verdict-ioniq5-20260611.md (GREEN) · commit 8877504_
