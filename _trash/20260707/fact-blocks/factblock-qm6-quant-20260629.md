---
type: fact-block
title: 르노코리아 QM6 팩트블록 (quantitative · 2026)
topic: qm6-factblock-quant
subject: 르노코리아 QM6 (중형 SUV · 2026 · 가솔린/LPG)
date: 2026-06-29
data_source:
  - data/outputs/approved/verdict-qm6-20260611.md (quantitative/referential GREEN)
created: 2026-06-29
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-024-factblock-batch-20260629]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-qm6-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='qm6' (쿼리 2026-06-29, 2행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='qm6' (쿼리 2026-06-29, 2행)
data_gate: verdict-qm6-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비(복합·도심·고속)·CO2배출량·배기량·공차중량·에너지등급
uncertified: 가격·이미지·변속기·구동방식(LPG행 raw_line 기반)·휠(LPG행 raw_line 기반)
flags:
  - "body_type null — 중형 SUV 추정. 데이터팀 확인 권고."
  - "model_code null — 데이터팀 확인 권고."
  - "LPG 행: drive_type null (2WD, raw_line 기반), wheel null (17\"/18\" raw_line 기반)."
  - "가솔린 트림 vehicle_trims 미등록 — LE·RE는 LPG 트림만 확인."
  - "vehicle_trims wheel_size·fuel_eff null 전 행 — 트림별 상세 제원 매핑 불가."
---

# QM6 팩트 블록 — quantitative (르노코리아 · 2026 · 중형 SUV)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-qm6-20260611 GREEN).  
> 인증 범위: 연비(km/L)·CO2배출량(g/km)·배기량(cc)·공차중량(kg)·에너지등급.  
> ※ 가솔린 2행(2WD·18") 수집, LPG 1행(2WD·17"/18" raw_line) 수집.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| body_type | ⚠️ null | 중형 SUV 추정. 데이터팀 확인 권고. |
| model_code | ℹ️ null | 미수집. |
| LPG drive_type | ⚠️ null | 2WD, raw_line 기반. |
| LPG wheel | ⚠️ null | 17"/18" 병기, raw_line 기반. |
| 가솔린 트림 | ℹ️ 미등록 | vehicle_trims에 LPG 트림(LE·RE)만 확인됨. |
| vehicle_trims 상세 | ℹ️ null 전 행 | 트림별 제원 매핑 불가. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 르노코리아 | vehicles.brand |
| 모델명 | QM6 | vehicles.name |
| 모델코드 | null (미수집) | vehicles.model_code |
| 연식 | 2026 | vehicles.year |
| 세그먼트 | 중형 | vehicles.segment |
| 차체 형태 | null (중형 SUV 추정) | vehicles.body_type |
| 연료 | 가솔린 2.0 GDe / LPG 2.0 LPe | vehicle_powertrains.fuel_kind |
| 구동 | 가솔린 2WD / LPG 2WD (raw_line 기반) | vehicle_powertrains |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 가솔린 (2.0 GDe · 무단변속기)

| 행 | 구동 | 휠 | 배기량 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 에너지등급 | 공차중량 |
|---|---|---|---|---|---|---|---|---|---|
| A | **2WD** | **18"** | 1,997 cc | **12.0 km/L** | 11.1 | 13.5 | 140 g/km | **3등급** | 1,535 kg |

### LPG (2.0 LPe · 무단변속기)

| 행 | 구동 | 휠 | 배기량 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 에너지등급 | 공차중량 |
|---|---|---|---|---|---|---|---|---|---|
| B | **2WD*** | **17"/18"*** | 1,998 cc | **8.9 km/L** | 8.1 | 10.2 | 147 g/km | **5등급** | 1,575 kg |

> \* raw_line 기반 (drive_type/wheel DB null). "2.0 LPe 2WD(17\"/18\")" raw_line 명시.  
> ※ LPG 연비(km/L)는 가솔린 환산 단위. 실제 LPG 충전량 기준 환산 필요(마케팅 주의).

> **핵심 포인트:**
> - 가솔린: 복합 12.0 km/L · CO2 140 g/km · **3등급** (2WD 18" 기준)
> - LPG: 복합 8.9 km/L · CO2 147 g/km · **5등급** (2WD 기준)
> - 가솔린 대비 LPG: 연비 −3.1 km/L, 공차중량 +40 kg, CO2 +7 g/km
> - 가솔린·LPG 배기량 동일(1,997/1,998 cc, 차이 1 cc — 인증 규격 차이 추정)

---

## 연비 요약

| 연료 | 구동 | 휠 | 연비(복합) | CO2 | 에너지등급 | 공차중량 |
|------|------|----|-----------|-----|-----------|---------|
| 가솔린 2.0 GDe | 2WD | 18" | **12.0 km/L** | 140 g/km | **3등급** | 1,535 kg |
| LPG 2.0 LPe | 2WD* | 17"/18"* | 8.9 km/L | 147 g/km | 5등급 | 1,575 kg |

> \* raw_line 기반

---

## 트림 라인업 (vehicle_trims)

| 트림 | 연료 | 구동 | 비고 |
|------|------|------|------|
| LE | LPG | 2WD | 제원 null (트림 매핑 불가) |
| RE | LPG | 2WD | 제원 null (트림 매핑 불가) |

> ⚠️ wheel_size·fuel_eff·curb_weight null 전 행 — 트림별 제원 매핑 불가.  
> 가솔린 트림 vehicle_trims 미등록. 트림 가격은 verdict 인증 범위 외 → 미포함.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
르노코리아 QM6 2026 · 가솔린 12.0km/L 3등급 · LPG 8.9km/L · 중형 SUV
```

### ② 블로그 소개 단락용 (2~3문장)
```
르노코리아 QM6(2026)는 중형 SUV로 가솔린 2.0 GDe(2WD·18")와 LPG 2.0 LPe(2WD) 두 파워트레인을 제공합니다.
가솔린 기준 복합 연비 12.0 km/L · CO2 140 g/km · 에너지등급 3등급이며, 공차중량 1,535 kg입니다.
LPG 모델은 복합 8.9 km/L · CO2 147 g/km · 5등급, 공차중량 1,575 kg으로 유지비 측면에서 LPG 연료비 절감 효과를 고려해야 합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 르노코리아
모델: QM6 (2026, 중형 SUV)
연료①: 가솔린 2.0 GDe · 무단변속기
  - 구동: 2WD · 휠: 18"
  - 연비: 복합 12.0 / 도심 11.1 / 고속 13.5 km/L
  - CO2: 140 g/km · 에너지등급: 3등급
  - 공차중량: 1,535 kg · 배기량: 1,997 cc
연료②: LPG 2.0 LPe · 무단변속기
  - 구동: 2WD(raw_line) · 휠: 17"/18"(raw_line)
  - 연비: 복합 8.9 / 도심 8.1 / 고속 10.2 km/L
  - CO2: 147 g/km · 에너지등급: 5등급
  - 공차중량: 1,575 kg · 배기량: 1,998 cc
트림(LPG): LE / RE (제원 매핑 불가)
```

### ④ 인포그래픽·카드 수치 스니펫
```
[가솔린 2.0 GDe · 2WD · 18"] 연비 12.0km/L | CO2 140g/km | 3등급 | 1,535kg
[LPG 2.0 LPe · 2WD · 17"/18"*] 연비 8.9km/L | CO2 147g/km | 5등급 | 1,575kg
※ LPG 구동/휠 raw_line 기반 · 가솔린 트림 미등록
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 가솔린 트림 구분 | vehicle_trims 미등록 |
| LPG 휠 구분 (17"/18") | raw_line 병기, 분리 수치 미제공 |
| 트림별 제원 | vehicle_trims null 전 행 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-29_  
_data gate: verdict-qm6-20260611.md (GREEN) · commit 8877504_
