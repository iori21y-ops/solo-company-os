---
type: fact-block
title: 기아 레이 팩트블록 (quantitative · 2026)
topic: ray-factblock-quant
subject: 기아 레이 JA (경형 해치백/밴 · 2026 · 가솔린)
date: 2026-06-29
data_source:
  - data/outputs/approved/verdict-ray-20260611.md (quantitative/referential GREEN)
created: 2026-06-29
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-024-factblock-batch-20260629]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-ray-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='ray' (쿼리 2026-06-29, 3행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='ray' (쿼리 2026-06-29, 4행)
data_gate: verdict-ray-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비(복합·도심·고속)·배기량·공차중량·에너지등급(경형)
uncertified: 가격·이미지·CO2(경형 별도 고시)·구동방식·최고출력
flags:
  - "body_type null — 경형 해치백/밴 추정. 데이터팀 확인 권고."
  - "model_code null — 데이터팀 확인 권고."
  - "drive_type null 전 행 — FWD 추정. 발행 전 원문 확인 권고."
  - "co2_emission null 전 행 — 경형차 별도 고시(정상)."
  - "행B(밴): displacement_cc 미명시(raw_line)이나 DB=998cc. 승용(행A)과 연비 동일."
  - "raw_line '127'·'130' → 최고출력(PS) 추정 — 인증 범위 외, 발행 금지."
  - "vehicle_trims 트렌디·프레스티지·시그니처·시그니처 X-Line 전 필드 null — 트림별 제원 매핑 불가."
---

# 레이 팩트 블록 — quantitative (기아 · 2026 · 경형)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-ray-20260611 GREEN).  
> 인증 범위: 연비(km/L)·배기량(cc)·공차중량(kg)·에너지등급(경형).  
> ※ 3행 구성: 14"(승용) / 14"(밴) / 15". CO2 null — 경형차 별도 고시 정상.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| body_type | ⚠️ null | 경형 해치백/밴 추정. 데이터팀 확인 권고. |
| model_code | ℹ️ null | 미수집. |
| drive_type | ⚠️ null 전 행 | FWD 추정. 발행 전 원문 확인 권고. |
| co2_emission | ℹ️ null 전 행 | 경형차 별도 고시(정상). 발행 자제. |
| 최고출력 | ⚠️ raw_line 한정 | '127'/'130'(PS 추정) — 인증 범위 외, 발행 금지. |
| vehicle_trims | ℹ️ null 전 행 | 트림별 제원 매핑 불가. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 기아 | vehicles.brand |
| 모델명 | 레이 | vehicles.name |
| 모델코드 | null (미수집) | vehicles.model_code |
| 연식 | 2026 | vehicles.year |
| 세그먼트 | 경차 | vehicles.segment |
| 차체 형태 | null (경형 해치백/밴 추정) | vehicles.body_type |
| 연료 | 가솔린 1.0 | vehicle_powertrains.fuel_kind |
| 배기량 | 998 cc | vehicle_powertrains.displacement_cc |
| 구동 | null (FWD 추정) | vehicle_powertrains.drive_type |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> 3행 구성. drive_type null 전 행(FWD 추정). CO2 null — 경형차 별도 고시.

### 가솔린 1.0 (4단 자동)

| 행 | 구분 | 휠 | 배기량 | 연비(복합) | 연비(도심) | 연비(고속) | 에너지등급 | 공차중량 |
|---|---|---|---|---|---|---|---|---|
| A | **승용** | **14"** | 998 cc | **12.9 km/L** | 12.2 | 13.8 | 경형등급 | 1,085 kg |
| B | **밴** | **14"** | 998 cc | **12.9 km/L** | 12.2 | 13.8 | 경형등급 | 1,075 kg |
| C | **승용** | **15"** | 998 cc | **12.6 km/L** | 11.9 | 13.5 | 경형등급 | 1,090 kg |

> **행 구분 근거:**
> - 행A raw_line: "1.0 가솔린 14인치 타이어 ... 4단 자동 경형 1,085 127" (승용 14")
> - 행B raw_line: "14인치 타이어(밴) ... 1,075 127" (밴 14" — 밴 공차중량 10 kg 경량)
> - 행C raw_line: "15인치 타이어 ... 1,090 130" (승용 15" — 연비 소폭 하락, 공차중량 최대)

> **핵심 포인트:**
> - 14" 승용 vs 밴: 연비 동일(12.9 km/L), 밴이 10 kg 경량(1,075 kg)
> - 15" 장착 시: 연비 −0.3 km/L(복합), 공차중량 +5 kg(승용 대비)
> - 경형차 에너지등급 별도 고시 — "경형등급" 표기 (숫자 등급 없음)
> - CO2 null — 경형차 별도 인증 체계(정상)

---

## 연비 요약

| 구분 | 휠 | 연비(복합) | 연비(도심) | 연비(고속) | 에너지등급 | 공차중량 |
|------|-----|-----------|-----------|-----------|-----------|---------|
| 승용 | 14" | **12.9 km/L** | 12.2 | 13.8 | 경형등급 | 1,085 kg |
| 밴 | 14" | 12.9 km/L | 12.2 | 13.8 | 경형등급 | 1,075 kg |
| 승용 | 15" | 12.6 km/L | 11.9 | 13.5 | 경형등급 | 1,090 kg |

---

## 트림 라인업 (vehicle_trims)

| 트림 | 비고 |
|------|------|
| 트렌디 | — |
| 프레스티지 | — |
| 시그니처 | — |
| 시그니처 X-Line | — |

> ⚠️ fuel_type·drive_type·wheel_size·fuel_eff·curb_weight null 전 행 — 트림별 제원 매핑 불가.  
> 트림 가격은 verdict 인증 범위 외 → 미포함.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
기아 레이 2026 · 경형 · 연비 12.9km/L(14") · 4단자동 · 4트림
```

### ② 블로그 소개 단락용 (2~3문장)
```
기아 레이(2026)는 1.0 가솔린 4단 자동 경형차로, 14인치 타이어 기준 복합 연비 12.9 km/L(도심 12.2 / 고속 13.8)를 기록합니다.
15인치 타이어 장착 시 복합 연비 12.6 km/L로 소폭 낮아지며, 공차중량은 승용 1,085~1,090 kg · 밴 1,075 kg입니다.
트림은 트렌디·프레스티지·시그니처·시그니처 X-Line 4종이며, 에너지등급은 경형차 별도 고시 기준 적용입니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 기아
모델: 레이 (2026, 경형)
연료: 가솔린 1.0 · 4단 자동
배기량: 998 cc
구동: FWD 추정 (drive_type null)
연비(14" 승용): 복합 12.9 / 도심 12.2 / 고속 13.8 km/L
연비(14" 밴): 복합 12.9 / 도심 12.2 / 고속 13.8 km/L
연비(15" 승용): 복합 12.6 / 도심 11.9 / 고속 13.5 km/L
공차중량: 승용14" 1,085 kg / 밴14" 1,075 kg / 승용15" 1,090 kg
에너지등급: 경형등급 (별도 고시)
트림: 트렌디 / 프레스티지 / 시그니처 / 시그니처 X-Line
```

### ④ 인포그래픽·카드 수치 스니펫
```
[14" 승용] 연비 12.9km/L(복합) | 1,085kg
[14" 밴] 연비 12.9km/L(복합) | 1,075kg
[15" 승용] 연비 12.6km/L(복합) | 1,090kg
가솔린 1.0 · 4단자동 · 경형등급
※ CO2 경형 별도 고시 · 구동방식 미확인
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| CO2 배출량 | 경형차 별도 고시 (DB null 정상) |
| 에너지등급 수치 | 경형차 별도 고시 체계 |
| 최고출력 | raw_line 추정값 (인증 범위 외) |
| 트림별 제원 | vehicle_trims null 전 행 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-29_  
_data gate: verdict-ray-20260611.md (GREEN) · commit 8877504_
