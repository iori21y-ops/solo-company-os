---
type: fact-block
title: 현대 포터 II 일렉트릭 팩트블록 (quantitative · 2024)
topic: porter2-electric-factblock-quant
subject: 현대 포터 II 일렉트릭 (전기 소형 화물차 · 2024)
date: 2026-06-29
data_source:
  - data/outputs/approved/verdict-porter2-electric-20260611.md (quantitative/referential GREEN)
created: 2026-06-29
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-024-factblock-batch-20260629]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-porter2-electric-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='porter2-electric' (쿼리 2026-06-29, 1행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='porter2-electric' (쿼리 2026-06-29, 2행)
data_gate: verdict-porter2-electric-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 전비(복합·도심·고속)·1회충전주행거리(복합·도심·고속)·공차중량
uncertified: 가격·이미지·모터출력·배터리kWh·에너지등급·휠·구동(raw_line 기반 참고)
flags:
  - "body_type/category 'SUV' 오류 — 소형 전기 화물트럭. 데이터팀 수정 권고."
  - "wheel null 전 행 — DB 미기재. 발행 금지."
  - "energy_grade null — 전기차 별도 고시(정상). 발행 자제."
  - "year=2024 — 현행 연식 갱신 미확인(2026년형 출시 여부 불명). 데이터팀 확인 권고."
  - "raw_line '58.8' → 배터리 kWh 추정(raw_line 기반). 단독 발행 전 원문 확인 필수."
  - "raw_line '327/180' 단위 불명확 — 발행 금지."
  - "vehicle_trims 스마트·프리미엄 전 필드 null — 트림별 제원 매핑 불가."
---

# 포터 II 일렉트릭 팩트 블록 — quantitative (현대 · 2024 · 전기 화물차)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-porter2-electric-20260611 GREEN).  
> 인증 범위: 전비(km/kWh)·1회충전주행거리(km)·공차중량(kg).  
> ※ DB electric_eff·driving_range 필드 추출. fuel_eff_combined/city/highway null (전기차 정상).

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| body_type | ⚠️ 'SUV' 오류 | 소형 전기 화물트럭. 데이터팀 수정 권고. |
| wheel | ⚠️ null 전 행 | DB 미기재. 발행 금지. |
| energy_grade | ℹ️ null | 전기차 별도 고시(정상). 발행 자제. |
| year | ⚠️ 2024 | 현행 연식 갱신 미확인. 데이터팀 확인 권고. |
| 배터리 58.8 | ⚠️ raw_line 한정 | kWh 추정값. 원문 확인 전 단독 발행 금지. |
| 327/180 | ⚠️ raw_line 단위 불명 | 발행 금지. |
| vehicle_trims | ℹ️ null 전 행 | 트림별 제원 매핑 불가. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 | vehicles.brand |
| 모델명 | 포터 II 일렉트릭 | vehicles.name |
| 모델코드 | null (미수집) | vehicles.model_code |
| 연식 | 2024 (현행 갱신 미확인) | vehicles.year |
| 세그먼트 | null (미수집) | vehicles.segment |
| 차체 형태 | 소형 전기 화물트럭 추정 (DB 'SUV' 오류) | vehicles.body_type |
| 연료 | 전기 (EV) | vehicle_powertrains.fuel_kind |
| 구동 | 2WD | vehicle_powertrains.drive_type |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> 1행 구성 (2WD 단일). fuel_eff_combined/city/highway null — electric_eff·driving_range 필드 추출.  
> 도심·고속 전비 및 주행거리는 raw_line 기반 참고값.

### 전기 (EV)

| 행 | 구동 | 전비(복합) | 전비(도심)* | 전비(고속)* | 1회충전(복합) | 1회충전(도심)* | 1회충전(고속)* | 공차중량 | 배터리* |
|---|---|---|---|---|---|---|---|---|---|
| A | **2WD** | **3.1 km/kWh** | 3.6 | 2.7 | **211 km** | 238 km | 177 km | 1,940 kg | 58.8 kWh 추정 |

> \* raw_line 기반 참고값. DB electric_eff(복합 3.1)·driving_range(복합 211)만 인증 필드.  
> 배터리 58.8 kWh는 raw_line 추정값 — 원문 확인 전 발행 금지.

> **핵심 포인트:**
> - 전기 소형 화물트럭 기준 복합 전비 3.1 km/kWh · 1회충전 211 km (복합)
> - 도심 전비(3.6) > 고속 전비(2.7) — 전형적 전기차 특성, 시내 배달 효율 우위
> - 공차중량 1,940 kg — 화물 적재 전 차체 중량

---

## 전비·주행거리 요약

| 구동 | 전비(복합) | 전비(도심)* | 전비(고속)* | 1회충전(복합) | 공차중량 | 에너지등급 |
|------|-----------|------------|------------|-------------|---------|-----------|
| 2WD | **3.1 km/kWh** | 3.6* | 2.7* | **211 km** | 1,940 kg | 별도 고시 |

> \* raw_line 기반 참고값

---

## 트림 라인업 (vehicle_trims)

| 트림 | 비고 |
|------|------|
| 스마트 | — |
| 프리미엄 | — |

> ⚠️ fuel_type·drive_type·wheel_size·fuel_eff 전 필드 null — 트림별 제원 매핑 불가.  
> 트림 가격은 verdict 인증 범위 외 → 미포함.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 포터 II 일렉트릭 · 전기 화물차 · 전비 3.1km/kWh · 1회충전 211km · 2024
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 포터 II 일렉트릭(2024)은 국내 대표 전기 소형 화물트럭으로, 복합 전비 3.1 km/kWh · 1회충전 주행거리 211 km(복합 인증)를 제공합니다.
도심 전비는 3.6 km/kWh로 시내 배달·상업 용도에서 효율이 더욱 높아집니다.
공차중량 1,940 kg이며 트림은 스마트·프리미엄 2종입니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대
모델: 포터 II 일렉트릭 (2024, 연식 갱신 미확인)
차체: 소형 전기 화물트럭 (body_type DB 오류 — 원문 참조)
연료: 전기(EV)
구동: 2WD
전비(복합): 3.1 km/kWh (인증)
전비(도심/고속): 3.6 / 2.7 km/kWh (raw_line 참고)
1회충전(복합): 211 km (인증)
1회충전(도심/고속): 238 / 177 km (raw_line 참고)
공차중량: 1,940 kg
배터리: 58.8 kWh 추정 (raw_line — 발행 전 확인 필수)
트림: 스마트 / 프리미엄 (트림별 제원 매핑 불가)
```

### ④ 인포그래픽·카드 수치 스니펫
```
[2WD] 전비 3.1km/kWh(복합) | 1회충전 211km(복합) | 공차중량 1,940kg
도심 3.6km/kWh | 238km (raw_line 참고)
※ 배터리 용량·에너지등급 미수집 — 발행 전 확인 필수
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 에너지등급 | 전기차 별도 고시 (DB null 정상) |
| 휠 | DB 미기재 |
| 배터리 kWh (확정) | raw_line 추정값 — 원문 확인 후 사용 |
| 모터 출력 | 단위 불명확 (raw_line '327/180') |
| 트림별 제원 | vehicle_trims null 전 행 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-29_  
_data gate: verdict-porter2-electric-20260611.md (GREEN) · commit 8877504_
