---
type: fact-block
title: 기아 모닝 팩트블록 (quantitative · JA · 2026)
topic: morning-factblock-quant
subject: 기아 모닝 (1.0 가솔린 4단 자동 · 경차)
date: 2026-06-26
data_source:
  - data/outputs/approved/verdict-morning-20260611.md (quantitative/referential GREEN)
created: 2026-06-26
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-021-factblock-batch-20260626]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-morning-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='morning' (쿼리 2026-06-26, 3행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='morning' (쿼리 2026-06-26, 4행)
data_gate: verdict-morning-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·공차중량·휠·에너지등급
uncertified: 가격·이미지·CO2(경형 별도 고시)·구동방식(drive_type null)
flags:
  - "vehicles.body_type null — 경형 해치백(5도어) 추정. 데이터팀 보완 권고."
  - "co2_emission 전 행 null — 경차 에너지등급 별도 고시 방식(정상). CO2 수치 사용 불가."
  - "drive_type 전 행 null — FWD(전륜) 추정."
  - "Row A(14\" 일반) · Row B(14\" 밴) 연비 동일(14.7km/L) — 동일 기계 스펙, 바디 타입 차이."
  - "vehicle_trims.wheel_size·fuel_eff null 전 행 — 트림-휠 매핑 불가."
---

# 모닝 팩트 블록 — quantitative (JA · 2026 · 1.0 가솔린)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-morning-20260611 GREEN).  
> 인증 범위: 연비(km/L)·공차중량·휠·에너지등급.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| body_type | ℹ️ null | DB 미입력. 경형 해치백 추정. 데이터팀 보완 권고. |
| CO2 | ℹ️ null 전 행 | 경차 에너지등급 별도 고시 방식 — 정상. CO2 수치 사용 불가. |
| drive_type | ℹ️ null 전 행 | FWD 추정. |
| 14" 일반/밴 | ℹ️ 참고 | 연비 동일(14.7km/L). 일반승용·밴 바디 구분이나 기계 스펙 동일. |
| vehicle_trims | ℹ️ null | wheel_size·fuel_eff null — 트림-휠 매핑 불가. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 기아 (KIA) | vehicles.brand |
| 모델명 | 모닝 | vehicles.name |
| 모델코드 | JA | vehicles.model_code |
| 연식 | 2026 | vehicles.year |
| 세그먼트 | 경차 | vehicles.segment |
| 차체 형태 | null (경형 해치백 추정) | vehicles.body_type |
| 연료 | 가솔린 | vehicle_powertrains.fuel_kind |
| 엔진 | 1.0 가솔린 4단 자동 (998cc) | vehicle_powertrains.engine |
| 구동 | null (FWD 추정) | vehicle_powertrains.drive_type |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> CO2 전 행 null (경형 별도 고시 — 표에서 제외).  
> drive_type 전 행 null (FWD 추정).  
> 에너지등급: 경형등급(경차 전용 기준).

### 1.0 가솔린 4단 자동 (998cc · FWD 추정)

| 행 | 휠 | 비고 | 연비(복합) | 연비(도심) | 연비(고속) | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|
| A | 14" | 일반승용 | **14.7 km/L** | 13.5 | 16.3 | 975 kg | **경형등급** |
| B | 14" | 밴 | **14.7 km/L** | 13.5 | 16.3 | 975 kg | **경형등급** |
| C | 16" | 표준 | **14.7 km/L** | 13.5 | 16.3 | 1,010 kg | **경형등급** |

> **핵심 포인트:**
> - **전 조합 연비 동일 14.7 km/L** — 휠 크기·바디 무관
> - 16" 휠 (행C): 공차중량 +35 kg (975→1,010 kg), 연비 유지
> - 14" 일반/밴(행A·B): 기계 스펙 동일, 바디 타입만 상이
> - CO2 수치 미제공 (경형 별도 고시)

---

## 연비 요약

| 휠 | 구동 | 바디 | 연비(복합) | 에너지등급 |
|----|------|------|-----------|-----------|
| 14" | FWD 추정 | 일반 | **14.7 km/L** | **경형등급** |
| 14" | FWD 추정 | 밴 | **14.7 km/L** | **경형등급** |
| 16" | FWD 추정 | 표준 | **14.7 km/L** | **경형등급** |

---

## 트림 라인업 (vehicle_trims)

| 트림 | 비고 |
|------|------|
| 트렌디 | — |
| 프레스티지 | — |
| 시그니처 | — |
| GT-Line | — |

> ⚠️ wheel_size·drive_type·fuel_eff null 전 행 — 트림별 제원 매핑 불가.  
> 트림 가격은 verdict 인증 범위 외 → 미포함.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
기아 모닝 2026 · 1.0 가솔린 · 복합 연비 14.7km/L(경형등급) · 공차중량 975kg~
```

### ② 블로그 소개 단락용 (2~3문장)
```
기아 모닝(JA, 2026년형)은 998cc 1.0 가솔린 4단 자동을 탑재한 경차입니다.
14인치·16인치 전 휠 조합에서 복합 연비 14.7 km/L(경형등급)로 동일하며,
공차중량은 14" 975 kg에서 16" 1,010 kg 수준입니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 기아(KIA)
모델: 모닝 (JA · 2026년형)
세그먼트: 경차
연료: 가솔린
엔진: 1.0 가솔린 4단 자동 (998cc)
구동방식: FWD 추정 (drive_type DB null)
연비(전 조합): 14.7 km/L | 경형등급
연비(도심): 13.5 km/L | 연비(고속): 16.3 km/L
공차중량: 975 kg(14") / 1,010 kg(16")
트림: 트렌디 / 프레스티지 / 시그니처 / GT-Line
```

### ④ 인포그래픽·카드 수치 스니펫
```
[14" FWD추정 일반]  14.7km/L | 975kg  | 경형등급
[14" FWD추정 밴  ]  14.7km/L | 975kg  | 경형등급
[16" FWD추정     ]  14.7km/L | 1,010kg | 경형등급
※ CO2 미제공 (경형 별도 고시) / 도심 13.5·고속 16.3 공통
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| CO2 배출량 | 경차 별도 고시 방식 — DB null (정상) |
| 구동방식 확정값 | drive_type null — FWD 추정 |
| 트림별 제원 상세 | vehicle_trims wheel_size·fuel_eff null |
| 최고출력·토크 | vehicle_powertrains 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-26_  
_data gate: verdict-morning-20260611.md (GREEN) · commit 8877504_
