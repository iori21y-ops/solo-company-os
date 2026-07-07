---
type: fact-block
title: 기아 니로 EV 팩트블록 (quantitative · 2025 · 전기)
topic: niro-ev-factblock-quant
subject: 기아 니로 EV (전기 · 2025)
date: 2026-06-28
data_source:
  - data/outputs/approved/verdict-niro-ev-20260611.md (quantitative/referential GREEN)
created: 2026-06-28
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-023-factblock-batch-20260628]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-niro-ev-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='niro-ev' (쿼리 2026-06-28, 1행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='niro-ev' (쿼리 2026-06-28, 3건)
  - DB: vehicles WHERE slug='niro-ev' (메타)
data_gate: verdict-niro-ev-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 전비(km/kWh)·주행거리(km)·에너지등급·공차중량
uncertified: 가격·이미지·구동방식(drive_type null)·휠(null)·배터리용량(raw_line 단위 불명확)
flags:
  - "drive_type null — 2WD(FWD 또는 RWD) 추정. 발행 전 원문 확인 권고."
  - "wheel null — DB 미수집. 원문 확인 권고."
  - "raw_line '358/180.9' 단위 불명확 → 배터리 수치(kWh·Wh/km 등) 사용 금지."
  - "vehicles.year = 2025 (2026 아님). 현행 연식 갱신 여부 데이터팀 확인 권고."
  - "segment='소형SUV' · category='EV' DB 확인."
  - "1행만 수집 — 휠·구동 변형 행 미수집. EV 단일 파워트레인 구성 추정."
  - "vehicle_trims 3건(익스클루시브·프레스티지·캘리그래피) — fuel_type·drive_type·wheel_size·fuel_eff 전 null."
  - "niro(HEV)·niro-ev(전기) 분리 slug. 본 팩트블록은 전기(EV) 전용."
---

# 니로 EV 팩트 블록 — quantitative (기아 · 전기 · 2025)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-niro-ev-20260611 GREEN).  
> 인증 범위: 전비(km/kWh)·주행거리(km)·에너지등급·공차중량.  
> ※ drive_type null(2WD 추정), wheel null. vehicles.year=2025. 배터리 수치 raw_line 단위 불명확 → 사용 금지.  
> ※ niro HEV는 별도 팩트블록(factblock-niro-quant-20260627.md) 참조.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| drive_type | ⚠️ null | 2WD 추정. 발행 전 원문 확인 권고. |
| wheel | ⚠️ null | DB 미수집. 원문 확인 권고. |
| 배터리 수치 | ⚠️ 사용 금지 | raw_line "358/180.9" 단위 불명확 (kWh·Wh/km 등 미확인) |
| vehicles.year | ⚠️ 2025 | 2026년형 여부 데이터팀 확인 권고. |
| 1행 단일 | ℹ️ | 휠·구동 변형 미수집. 단일 EV 파워트레인 구성 추정. |
| vehicle_trims | ℹ️ null 전 행 | 트림별 제원 매핑 불가. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 기아 (Kia) | vehicles.brand |
| 모델명 | 니로 EV | vehicles.name |
| 모델코드 | null (미수집) | vehicles.model_code |
| 연식 | 2025 ⚠️ | vehicles.year |
| 세그먼트 | 소형 SUV | vehicles.segment |
| 차체 형태 | null (소형 SUV 추정) | vehicles.body_type |
| 카테고리 | EV | vehicles.category |
| 연료 | 전기 (EV) | vehicle_powertrains.fuel_kind |
| 구동 | null (2WD 추정) | vehicle_powertrains.drive_type |
| 휠 | null (미수집) | vehicle_powertrains.wheel |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 니로 EV (전기 · 단일 구성)

| 행 | 전비(복합) | 전비(도심) | 전비(고속) | 주행거리(복합) | 주행거리(도심) | 주행거리(고속) | 에너지등급 | 공차중량 |
|---|---|---|---|---|---|---|---|---|
| A | **5.3 km/kWh** | 5.9 | 4.8 | **401 km** | 436 km | 358 km | **2등급** | **1,705 kg** |

> raw_line 원문: "니로 EV 401 436 358 5.3 5.9 4.8 2 358/180.9 1,705"  
> ⚠️ "358/180.9" 항목은 단위 미확인 → 배터리 관련 수치 발행 금지.  
> ⚠️ drive_type null(2WD 추정), wheel null. 원문 확인 후 발행 권고.

---

## 연비·전비 요약

| 항목 | 수치 | 근거 |
|------|------|------|
| 전비 (복합) | **5.3 km/kWh** | electric_eff |
| 전비 (도심) | 5.9 km/kWh | raw_line |
| 전비 (고속) | 4.8 km/kWh | raw_line |
| 주행거리 (복합) | **401 km** | driving_range |
| 주행거리 (도심) | 436 km | raw_line |
| 주행거리 (고속) | 358 km | raw_line |
| 에너지등급 | **2등급** | energy_grade |
| 공차중량 | **1,705 kg** | curb_weight_kg |

---

## 트림 라인업 (vehicle_trims · 가격 미인증)

| 트림 | 출고가(참고) |
|------|------------|
| 익스클루시브 | 49,820,000원 |
| 프레스티지 | 55,360,000원 |
| 캘리그래피 | 61,860,000원 |

> ⚠️ 가격은 verdict 인증 범위 외 — 참고값. 발행 전 최신가 확인 필수.  
> ⚠️ fuel_type·drive_type·wheel_size·fuel_eff 전 null — 트림별 제원 매핑 불가.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
기아 니로 EV 2025 · 전비 5.3km/kWh · 주행거리 401km · 에너지 2등급
```

### ② 블로그 소개 단락용 (2~3문장)
```
기아 니로 EV(2025)는 소형 SUV 형태의 순수 전기차로, 복합 전비 5.3 km/kWh·1회 충전 주행거리 401 km(복합 기준)·에너지 2등급을 달성합니다.
도심 전비 5.9 km/kWh로 도심 주행 효율이 특히 높으며, 공차중량은 1,705 kg입니다.
배터리 용량 수치는 DB 원문 단위가 미확인 상태로, 발행 전 별도 확인이 필요합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 기아(Kia)
모델: 니로 EV (2025) ※ 현행 연식 확인 권고
세그먼트: 소형 SUV (EV)
연료: 전기(EV)
구동방식: null (2WD 추정 — 원문 확인 필요)
휠: null (DB 미수집)
전비(복합): 5.3 km/kWh | 도심 5.9 | 고속 4.8
주행거리(복합): 401 km | 도심 436 km | 고속 358 km
에너지등급: 2등급
공차중량: 1,705 kg
배터리 용량: DB 미확인 → 발행 금지
트림: 익스클루시브 / 프레스티지 / 캘리그래피
```

### ④ 인포그래픽·카드 수치 스니펫
```
[니로 EV 2025 · 단일 구성]
전비 5.3 km/kWh (도심 5.9 · 고속 4.8)
주행거리 401 km (도심 436 · 고속 358)
에너지 2등급 | 공차중량 1,705 kg
※ 배터리 수치 발행 금지 / drive_type null(2WD 추정) / wheel null
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 배터리 용량 | raw_line 단위 불명확 → 사용 금지 |
| 구동방식 확정 | drive_type null — 원문 확인 권고 |
| 휠 사이즈 | DB 미수집 |
| 트림별 제원 상세 | vehicle_trims null 전 행 |
| HEV 니로 | niro 별도 팩트블록(factblock-niro-quant-20260627.md) |

---

_작성: 컨텐츠_  
_작성일: 2026-06-28_  
_data gate: verdict-niro-ev-20260611.md (GREEN) · commit 8877504_
