---
type: fact-block
title: 제네시스 Electrified GV70 팩트블록 (quantitative · 2026년형 · 전기)
topic: gv70ev-factblock-quant
subject: 제네시스 Electrified GV70 (2026년형 · 중형 전기 SUV · AWD · 19"/20")
date: 2026-06-24
data_source:
  - data/outputs/approved/verdict-gv70ev-20260611.md (quantitative/referential GREEN)
created: 2026-06-24
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-019-factblock-batch-20260624]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-gv70ev-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='gv70ev' (쿼리 2026-06-24, 2행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='gv70ev' (쿼리 2026-06-24, 1행)
data_gate: verdict-gv70ev-20260611 GREEN · DB == PDF 원문 일치 (pdf_cache 재파싱 전수 대조)
certified_scope: 전비(복합/도심/고속)·주행거리(복합/도심/고속)·공차중량·구동방식·휠
uncertified: 가격·이미지·배터리 용량 상세·에너지등급(전기차 별도 고시)·2WD 제원
flags:
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.body_type/segment/category null — DB 미입력. 데이터팀 보완 권고."
  - "vehicle_powertrains에 AWD 2행만 수집(19\"/20\") — 2WD 제원 미수집. 2WD 존재 여부 미확인."
  - "vehicle_trims 1건만 수집(ELECTRIFIED GV70, drive_type='2WD' 기재) — 실제 powertrains는 AWD만 존재. 트림 drive_type 데이터팀 확인 권고."
  - "raw_line 내 '697 / 120.6' 단위 불명확 → 배터리 용량 수치 사용 금지. 전비·주행거리만 사용."
  - "energy_grade null — 전기차 에너지소비효율 등급은 별도 고시(환경부). DB 미입력 정상."
  - "co2_emission null — 전기차 직접 배출 없음."
  - "vehicle_trims.base_price 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# Electrified GV70 팩트 블록 — quantitative (2026년형 · 전기 SUV)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-gv70ev-20260611 GREEN · pdf_cache 전수 대조 확정).  
> 인증 범위: 전비(복합/도심/고속)·주행거리(복합/도심/고속)·공차중량·구동방식·휠.  
> ⚠️ 배터리 용량 수치(raw_line "697 / 120.6") 단위 불명확 → 인용 금지. 전비·주행거리만 사용.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| model_code | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| body_type / segment / category | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| 2WD 제원 | ⚠️ 미수집 | AWD 2행만 수집. 2WD 존재 여부·제원 미확인. |
| vehicle_trims drive_type | ⚠️ 불일치 | 트림표에 '2WD' 기재 / powertrains는 AWD만 존재 — 데이터팀 확인 권고. |
| 배터리 수치 | 🚫 사용 금지 | raw_line "697 / 120.6" 단위 불명확. 전비·주행거리만 사용. |
| energy_grade | ℹ️ null | 전기차 등급 별도 고시(환경부). DB 미입력 정상. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 제네시스 | vehicles.brand |
| 모델명 | Electrified GV70 | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | — (null) | vehicles.segment |
| 카테고리 | — (null) | vehicles.category |
| 엔진 라인업 | 전기 (EV) | vehicle_powertrains.fuel_kind |
| 구동방식 | AWD (수집분) | vehicle_powertrains.drive_type |
| 휠 | 19" / 20" | vehicle_powertrains.wheel |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 전기 EV — AWD (공차중량 2,275~2,295 kg)

| 행 | 구동 | 휠 | 전비(복합) | 전비(도심) | 전비(고속) | 주행거리(복합) | 주행거리(도심) | 주행거리(고속) | 공차중량 |
|---|---|---|---|---|---|---|---|---|---|
| A | **AWD** | **19"** | **4.5 km/kWh** | 4.8 | 4.2 | **423 km** | 448 | 393 | **2,275 kg** |
| B | **AWD** | **20"** | **4.2 km/kWh** | 4.5 | 3.9 | **400 km** | 427 | 367 | **2,295 kg** |

> ※ 2WD 제원 미수집 — 존재 여부 및 성능 수치 미확인.  
> ※ 에너지등급 미기재(전기차 별도 고시 — 본 팩트블록 범위 外).

---

## 휠별 핵심 비교

| 항목 | 19" AWD | 20" AWD |
|------|---------|---------|
| 복합 전비 | **4.5 km/kWh** | 4.2 km/kWh |
| 복합 주행거리 | **423 km** | 400 km |
| 공차중량 | 2,275 kg | 2,295 kg |

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.  
> ⚠️ 1건만 수집(Genesis EV 파서 제한). 트림 drive_type 불일치(2WD 기재 ↔ powertrains AWD) — 데이터팀 확인 권고.

| 트림명 | 출고가 참고 | 세제혜택가 참고 |
|--------|-----------|--------------|
| ELECTRIFIED GV70 | 79,840,000원 | 78,630,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
제네시스 Electrified GV70 2026 · 전기 SUV · AWD 19" 최대 4.5km/kWh · 423km
```

### ② 블로그 소개 단락용 (2~3문장)
```
제네시스 Electrified GV70 2026년형은 AWD 전기 SUV입니다.
19" 기준 복합 전비 4.5 km/kWh, 복합 주행거리 423 km이며,
20" 선택 시 전비 4.2 km/kWh, 주행거리 400 km입니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 제네시스
모델: Electrified GV70 2026년형
연료: 전기 (EV)
구동: AWD (수집분)

[AWD 19"]
복합 전비: 4.5 km/kWh (도심 4.8 / 고속 4.2)
복합 주행거리: 423 km (도심 448 / 고속 393)
공차중량: 2,275 kg

[AWD 20"]
복합 전비: 4.2 km/kWh (도심 4.5 / 고속 3.9)
복합 주행거리: 400 km (도심 427 / 고속 367)
공차중량: 2,295 kg
```

### ④ 인포그래픽·카드 수치 스니펫
```
[AWD 19"]  4.5km/kWh | 423km | 2,275kg  ← 최고 효율
[AWD 20"]  4.2km/kWh | 400km | 2,295kg
※ 전비·주행거리 기준 / 2WD 제원 미수집 / 배터리 용량 수치 사용 금지
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 外) |
| 2WD 제원 | powertrains 미수집 |
| 배터리 용량 (kWh) | raw_line 단위 불명확 — 사용 금지 |
| 에너지등급 | 전기차 별도 고시 (환경부) |
| 안전 등급 | 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-24_  
_data gate: verdict-gv70ev-20260611.md (GREEN · pdf_cache 전수 대조) · commit 8877504_
