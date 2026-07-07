---
type: fact-block
title: 제네시스 G70 Shooting Brake 팩트블록 (quantitative · 2026년형 · 가솔린)
topic: g70-sb-factblock-quant
subject: 제네시스 G70 Shooting Brake (2026년형 · I4 2.5T 가솔린 · 2WD/AWD · 18"/19")
date: 2026-06-21
data_source:
  - data/outputs/approved/verdict-g70-sb-20260611.md (quantitative/referential GREEN)
created: 2026-06-21
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-014-factblock-batch-20260621]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-g70-sb-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='g70-sb' (쿼리 2026-06-21, 6행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='g70-sb' (쿼리 2026-06-21, 1행)
data_gate: verdict-g70-sb-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치 (수동 3자 대조 확정)
certified_scope: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠·구동방식
uncertified: 가격·이미지·V6 3.3T 존재 여부·트림별 스펙 분리·안전등급
flags:
  - "vehicles.segment null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.category null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.body_type null — DB 미입력. 데이터팀 보완 권고."
  - "제네시스 ICE 파서(_gs_parse_ice_fuel) 불안정 — 수동 PDF 3자 대조로 GREEN 확정. 파서 출력 자동 재INSERT 차단(GENESIS_ICE_AUTO_INSERT_BLOCKED=True). 콘텐츠 작성에는 영향 없음."
  - "V6 3.3T 행 미수집 — G70 SB에 3.3T 미제공이거나 파서 미수집. 데이터팀 확인 권고."
  - "18\" 2WD 2행(id 517·518): 공차중량 1,705·1,710 kg, 연비 10.9·10.8 — 스펙 그룹 미분리. 원문 확인 권고."
  - "18\" AWD 2행(id 520·521): 공차중량 1,770·1,775 kg, 연비 10.1·10.0 — 스펙 그룹 미분리. 원문 확인 권고."
  - "vehicle_trims 1건만 수집 — Genesis ICE 파서 제한."
  - "vehicle_trims.base_price 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# G70 Shooting Brake 팩트 블록 — quantitative (2026년형 · 2.5T 가솔린)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-g70-sb-20260611 GREEN · 수동 3자 대조 확정).  
> 인증 범위: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠·구동방식.  
> ⚠️ 제네시스 ICE 파서 불안정 → 수동 확정값. 수치 인용 시 원문 PDF 병행 확인 권장.  
> V6 3.3T 행 미수집 — DB에 2.5T만 존재. G70 SB의 3.3T 제공 여부 원문 확인 필요.  
> 동일 휠·구동 조합에 2행씩 존재 (18" 2WD·18" AWD) — 스펙 그룹 분리 미확인.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| segment / category | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| model_code | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| body_type | ℹ️ null | DB 미입력. (슈팅브레이크 왜건형) |
| Genesis ICE 파서 | ⚠️ 불안정 | 수동 PDF 3자 대조로 GREEN 확정. 파서 자동 re-INSERT 차단 중. |
| V6 3.3T | ⚠️ 미수집 | G70 SB 3.3T 미제공 또는 파서 누락. 데이터팀 확인 권고. |
| 18" 2WD 2행 | ⚠️ 미분리 | 공차중량 1,705·1,710 kg — 스펙 그룹 트림 매핑 미확인. |
| 18" AWD 2행 | ⚠️ 미분리 | 공차중량 1,770·1,775 kg — 스펙 그룹 트림 매핑 미확인. |
| vehicle_trims | ℹ️ 1건 | Genesis ICE 파서 제한 — 트림별 수치 매핑 불가. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 제네시스 | vehicles.brand |
| 모델명 | G70 Shooting Brake | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | — (null) | vehicles.segment |
| 카테고리 | — (null) | vehicles.category |
| 엔진 | I4 2.5 T-GDi | vehicle_powertrains.engine |
| 연료 | 가솔린 | vehicle_powertrains.fuel_kind |
| 배기량 | 2,497cc (2.5) | vehicle_powertrains.displacement_cc |
| 구동방식 | 2WD / AWD | vehicle_powertrains.drive_type |
| 휠 | 18" / 19" | vehicle_powertrains.wheel |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 2.5T I4 — 2WD

| 행 | 구동 | 휠 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|
| A | **2WD** | **18"** | **10.9 km/ℓ** | 9.7 | 12.7 | 154 g/km | **1,705 kg** | **4등급** |
| B | **2WD** | **18"** | **10.8 km/ℓ** | 9.6 | 12.6 | 156 g/km | **1,710 kg** | **4등급** |
| C | **2WD** | **19"** | **10.7 km/ℓ** | 9.5 | 12.5 | 157 g/km | **1,720 kg** | **4등급** |

> ※ Row A·B 동일 18" 2WD에서 연비 차이(10.9 vs 10.8) / 중량 차이(1,705 vs 1,710 kg) — 스펙 그룹 분리 미확인.

### 2.5T I4 — AWD

| 행 | 구동 | 휠 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|
| D | **AWD** | **18"** | **10.1 km/ℓ** | 9.1 | 11.7 | 166 g/km | **1,770 kg** | **4등급** |
| E | **AWD** | **18"** | **10.0 km/ℓ** | 9.0 | 11.6 | 168 g/km | **1,775 kg** | **4등급** |
| F | **AWD** | **19"** | **9.9 km/ℓ** | 8.9 | 11.5 | 171 g/km | **1,785 kg** | **4등급** |

> ※ Row D·E 동일 18" AWD에서 연비 차이(10.1 vs 10.0) / 중량 차이(1,770 vs 1,775 kg) — 스펙 그룹 분리 미확인.

---

## 핵심 비교 요약

| 항목 | 2WD 최고 | AWD 최고 | 차이 |
|------|---------|---------|------|
| 최대 복합연비 | 10.9 km/ℓ (18" Row A) | 10.1 km/ℓ (18" Row D) | −0.8 km/ℓ |
| 최저 CO2 | 154 g/km | 166 g/km | +12 g/km |
| 최저 공차중량 | 1,705 kg | 1,770 kg | +65 kg |
| 에너지등급 | 4등급 | 4등급 | — |

> **핵심 포인트:**
> - 전 라인업 4등급 — G70 세단(4등급)과 동급
> - 2WD 18" 최고 연비 10.9 km/ℓ (G70 세단 경량 11.2 대비 −0.3 — SB 중량 증가 영향)
> - 19" 선택 시 AWD 기준 9.9 km/ℓ (2WD 10.7 대비 −0.8)
> - AWD 선택 시 2WD 대비 공차중량 약 +65 kg, 연비 약 −0.8 km/ℓ

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.  
> ⚠️ Genesis ICE 파서 제한으로 1건만 수집 — 전체 트림 미반영 가능성.

| 트림명 | 출고가 참고 |
|--------|-----------|
| G70 SHOOTING BRAKE | 47,040,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
제네시스 G70 SB 2026 · 슈팅브레이크 · 2.5T · 최대 10.9km/ℓ (4등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
제네시스 G70 Shooting Brake 2026년형은 I4 2.5T-GDi 가솔린 엔진을 탑재한 왜건형 파생 모델입니다.
2WD 18" 기준 최대 복합연비 10.9 km/ℓ(4등급), AWD 19" 기준 9.9 km/ℓ이며,
공차중량은 2WD 1,705 kg~1,720 kg, AWD 1,770 kg~1,785 kg입니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 제네시스
모델: G70 Shooting Brake 2026년형
엔진: I4 2.5 T-GDi (2,497cc) 가솔린
구동방식: 2WD / AWD

[2WD]
최대 복합연비: 10.9 km/ℓ (18")
CO2: 154 g/km (18" 최저)
공차중량: 1,705 kg (18" 최저)
에너지등급: 4등급

[AWD]
최대 복합연비: 10.1 km/ℓ (18")
CO2: 166 g/km (18" 최저)
공차중량: 1,770 kg (18" 최저)
에너지등급: 4등급
```

### ④ 인포그래픽·카드 수치 스니펫
```
[2WD 18" Row A]  10.9km/ℓ | CO2 154g | 1,705kg | 4등급  ← 최고 효율
[2WD 19"]        10.7km/ℓ | CO2 157g | 1,720kg | 4등급
[AWD 18" Row D]  10.1km/ℓ | CO2 166g | 1,770kg | 4등급
[AWD 19"]         9.9km/ℓ | CO2 171g | 1,785kg | 4등급
※ 복합연비 기준 / 18" 동일 구동 2행 존재 — 스펙 그룹 분리 미확인
※ V6 3.3T 미수집 — 2.5T 전용 수치
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| V6 3.3T 제원 | DB 미수집 — G70 SB 3.3T 존재 여부 불명 |
| 스펙 그룹별 트림 매핑 | Genesis ICE 파서 제한 — 트림 1건만 수집 |
| 안전 등급 | 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-21_  
_data gate: verdict-g70-sb-20260611.md (GREEN · 수동 3자 대조) · commit 8877504_
