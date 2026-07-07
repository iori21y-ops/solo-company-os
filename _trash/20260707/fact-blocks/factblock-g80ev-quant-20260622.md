---
type: fact-block
title: 제네시스 G80 전동화 팩트블록 (quantitative · 2026년형 · 전기)
topic: g80ev-factblock-quant
subject: 제네시스 Electrified G80 (2026년형 · 전기 · AWD · 19")
date: 2026-06-22
data_source:
  - data/outputs/approved/verdict-g80ev-20260611.md (quantitative/referential GREEN)
created: 2026-06-22
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-015-factblock-batch-20260622]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-g80ev-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='g80ev' (쿼리 2026-06-22, 1행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='g80ev' (쿼리 2026-06-22, 1행)
data_gate: verdict-g80ev-20260611 GREEN · DB == PDF 원문 일치 (pdf_cache 재파싱 전수 대조)
certified_scope: 전비(복합)·복합주행거리·공차중량·구동방식·휠
uncertified: 에너지등급·도심/고속 전비·도심/고속 주행거리·배터리 수치·가격·이미지·세그먼트·카테고리
flags:
  - "vehicles.category null, segment null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.body_type null — DB 미입력. 데이터팀 보완 권고."
  - "energy_grade null — vehicle_powertrains 미입력. 에너지 등급 발행 불가."
  - "1행만 수집 (AWD·19" 단일 구성) — 2WD 또는 다른 휠 사이즈 존재 여부 불명. 데이터팀 확인 권고."
  - "raw_line '523 / 180.9' 단위 불명확 → 배터리/출력 관련 수치 사용 금지."
  - "도심/고속 전비(4.6/4.3 km/kWh)·주행거리(492/454 km)는 raw_line에만 존재, vehicle_powertrains 별도 컬럼 미분리 — 복합 수치만 인증."
  - "vehicle_trims 1건만 수집(ELECTRIFIED G80) — 가격 verdict 미인증."
---

# G80 전동화 팩트 블록 — quantitative (2026년형 · 전기)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-g80ev-20260611 GREEN).  
> 인증 범위: **전비(복합)·복합주행거리·공차중량·구동방식·휠**.  
> ⚠️ 1행 단일 구성 (AWD·19" 전용). 에너지등급·배터리 수치 미인증.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| category / segment | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| model_code / body_type | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| energy_grade | ⚠️ null | DB 미입력 — 에너지등급 발행 불가. |
| 수집 행수 | ⚠️ 1행 | AWD·19" 단일 구성만 수집. 2WD 또는 다른 휠 존재 여부 미확인. |
| raw_line 수치 | 🚫 사용 금지 | "523 / 180.9" 단위 불명확. 배터리 관련 수치 미검증. |
| 도심/고속 전비·거리 | 📌 참고 불가 | raw_line 내 4.6/4.3 km/kWh, 492/454 km — 별도 컬럼 미분리, 인증 범위 外. |
| 가격 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 제네시스 | vehicles.brand |
| 모델명 | Electrified G80 | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | — (null) | vehicles.segment |
| 카테고리 | — (null) | vehicles.category |
| 엔진 | 전기 | vehicle_powertrains.engine |
| 연료 | EV | vehicle_powertrains.fuel_kind |
| 구동방식 | AWD | vehicle_powertrains.drive_type |
| 휠 | 19" | vehicle_powertrains.wheel |

---

## 제원 (vehicle_powertrains · GREEN 인증)

| 항목 | 수치 | 단위 | 비고 |
|------|------|------|------|
| 전비 (복합) | **4.4** | km/kWh | ✅ 인증 (vehicle_powertrains.electric_eff) |
| 복합 주행거리 | **475** | km | ✅ 인증 (vehicle_powertrains.driving_range) |
| 공차중량 | **2,355** | kg | ✅ 인증 (vehicle_powertrains.curb_weight_kg) |
| 에너지등급 | — (null) | — | ❌ DB 미입력, 발행 불가 |

> ⚠️ 도심 전비 4.6 km/kWh, 고속 전비 4.3 km/kWh는 raw_line 참고값 — **인증 범위 外, 발행 금지**.  
> ⚠️ 도심 주행거리 492 km, 고속 454 km는 raw_line 참고값 — **인증 범위 外, 발행 금지**.

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | 출고가 참고 |
|--------|-----------|
| ELECTRIFIED G80 | 89,190,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
제네시스 Electrified G80 2026 · 전기 AWD · 복합 4.4km/kWh · 항속 475km
```

### ② 블로그 소개 단락용 (2~3문장)
```
제네시스 Electrified G80 2026년형은 전기 AWD 구동의 대형 전기 세단입니다.
복합 전비 4.4 km/kWh, 복합 주행거리 475 km를 제공하며, 공차중량 2,355 kg입니다.
현재 19" 단일 휠·AWD 전용 구성으로 수집되었습니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 제네시스
모델: Electrified G80 2026년형
연료: 전기
구동: AWD
휠: 19"

[인증 수치]
복합 전비: 4.4 km/kWh
복합 주행거리: 475 km
공차중량: 2,355 kg
에너지등급: 미확인 (DB null)
```

### ④ 인포그래픽·카드 수치 스니펫
```
[전기 AWD 19"]  4.4km/kWh | 475km | 2,355kg
※ 복합 기준 / 에너지등급 미확인 / 배터리 수치 발행 금지
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 에너지등급 | vehicle_powertrains.energy_grade = null (DB 미입력) |
| 배터리 용량·충전 출력 | raw_line "523/180.9" 단위 불명확 → 사용 금지 |
| 도심/고속 전비·주행거리 | raw_line 참고값, 별도 컬럼 미분리 → 인증 범위 外 |
| 2WD / 다른 휠 구성 | 미수집 (단일 AWD·19" 행만 존재) |
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 안전 등급 | 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-22_  
_data gate: verdict-g80ev-20260611.md (GREEN) · commit 8877504_
