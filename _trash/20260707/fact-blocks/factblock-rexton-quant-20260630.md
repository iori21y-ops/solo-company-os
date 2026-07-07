---
type: fact-block
title: KGM 렉스턴 팩트블록 (quantitative · 2026년형)
topic: rexton-factblock-quant
subject: KGM 렉스턴 (2026년형 · 2.2 디젤 대형 SUV)
date: 2026-06-30
data_source:
  - data/outputs/approved/verdict-rexton-20260611.md (quantitative/referential GREEN)
created: 2026-06-30
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-025-factblock-batch-20260630]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-rexton-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='rexton' (쿼리 2026-06-30, 8행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='rexton' (쿼리 2026-06-30, 2행)
data_gate: verdict-rexton-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·ISG 적용여부
uncertified: 가격·이미지·휠사이즈·안전등급·트림별 옵션
flags:
  - "vehicles.body_type null — 대형 SUV 추정. 데이터팀 보완 권고."
  - "vehicles.model_code null — DB 미입력."
  - "vehicle_powertrains.wheel null 전 행 — 휠사이즈 미수록."
  - "2WD 5인승 2행: engine 컬럼에 ISG 구분 미명기(연비 차이로 적용/미적용 추정). 발행 시 ISG 여부 주석 권고."
  - "4WD 행 공차중량 2,170 vs 2,180 kg 2쌍: 5인승/7인승 추정. raw_line 명기 없음 — 트림 매핑 불가."
  - "vehicle_trims.drive_type·wheel_size null — 트림·구동 연결 불가."
---

# 렉스턴 팩트 블록 — quantitative (2026년형 · 2.2 디젤)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-rexton-20260611 GREEN).  
> 인증 범위: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급.  
> 휠사이즈·트림별 옵션·ISG 세부 매핑 등은 raw_line 기준 참고.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| body_type | ℹ️ null | 대형 SUV 추정. 데이터팀 보완 권고. |
| model_code | ℹ️ null | DB 미입력. |
| 휠사이즈 | ℹ️ null | vehicle_powertrains.wheel 전 행 null. |
| ISG 구분(2WD 5인승) | ⚠️ 추정 | engine 컬럼 미구분 — 연비 차이(11.4/10.8 km/ℓ)로 ISG 적용/미적용 추정. |
| 4WD 공차중량 이원화 | ⚠️ 추정 | 2,170 kg / 2,180 kg 2쌍씩 — 5인승/7인승 추정. raw_line 미명기. |
| 가격 데이터 | 📌 참고용 | 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | KGM | vehicles |
| 모델명 | 렉스턴 (Rexton) | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 대형 | vehicles.segment |
| 카테고리 | SUV | vehicles.category |
| 연료 | 디젤 | vehicle_powertrains.fuel_kind |
| 배기량 | 2,157cc (2.2L) | vehicle_powertrains.displacement_cc |
| 변속기 | 자동 8단 (전 구성) | vehicle_powertrains.engine |
| 에너지등급 | 4등급 (전 구성) | vehicle_powertrains.energy_grade |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 2WD

| 행 | 인승 | ISG | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|
| A | **5인승** | 적용(추정) | **11.4 km/ℓ** | 10.2 | 13.2 | 170 g/km | **2,060 kg** | 4등급 |
| B | **5인승** | 미적용(추정) | **10.8 km/ℓ** | 9.5 | 12.8 | 180 g/km | **2,060 kg** | 4등급 |
| C | **7인승** | 적용 | **11.4 km/ℓ** | 10.2 | 13.2 | 170 g/km | **2,070 kg** | 4등급 |
| D | **7인승** | 미적용 | **10.8 km/ℓ** | 9.5 | 12.8 | 180 g/km | **2,070 kg** | 4등급 |

### 4WD

| 행 | 공차중량 추정 | ISG | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|
| E | 5인승(추정) | 적용(추정) | **11.0 km/ℓ** | 9.8 | 12.7 | 177 g/km | **2,170 kg** | 4등급 |
| F | 5인승(추정) | 미적용(추정) | **10.5 km/ℓ** | 9.3 | 12.4 | 186 g/km | **2,170 kg** | 4등급 |
| G | 7인승(추정) | 적용(추정) | **11.0 km/ℓ** | 9.8 | 12.7 | 177 g/km | **2,180 kg** | 4등급 |
| H | 7인승(추정) | 미적용(추정) | **10.5 km/ℓ** | 9.3 | 12.4 | 186 g/km | **2,180 kg** | 4등급 |

> **핵심 포인트:**
> - ISG 적용 시 연비 향상: 2WD+0.6 km/ℓ (11.4 vs 10.8), 4WD+0.5 km/ℓ (11.0 vs 10.5)
> - ISG 적용 시 CO2 저감: 2WD −10 g/km (170 vs 180), 4WD −9 g/km (177 vs 186)
> - 2WD → 4WD 전환 시 최고 연비 기준 0.4 km/ℓ 하락 (11.4→11.0, ISG 적용 기준)
> - 공차중량: 2WD 5인승 2,060 kg → 4WD 7인승(추정) 2,180 kg (최대 120 kg 차이)
> - 전 구성 4등급 — 대형 디젤 SUV 수준

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | drive_type | wheel_size |
|--------|-----------|-----------|
| T1 | null | null |
| T2 | null | null |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
KGM 렉스턴 2026 · 2.2 디젤 대형 SUV · 2WD(ISG) 복합 11.4km/ℓ (4등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
KGM 렉스턴 2026년형은 2.2L 디젤 터보 엔진에 자동 8단 변속기를 탑재한 대형 SUV입니다.
2WD ISG 적용 기준 복합 연비 11.4 km/ℓ(도심 10.2 / 고속 13.2)이며, 4WD ISG 기준 11.0 km/ℓ입니다.
5인승·7인승 두 가지 구성으로 제공되며, ISG 적용 시 연비와 CO2 배출량이 개선됩니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: KGM
모델: 렉스턴 2026년형
연료: 디젤
배기량: 2,157cc (2.2L)
변속기: 자동 8단
구동방식: 2WD / 4WD
인승: 5인승 / 7인승
에너지등급: 4등급 (전 구성)

연비 — 2WD ISG 적용(최고): 복합 11.4 / 도심 10.2 / 고속 13.2 km/ℓ · CO2 170g/km
연비 — 2WD ISG 미적용:    복합 10.8 / 도심  9.5 / 고속 12.8 km/ℓ · CO2 180g/km
연비 — 4WD ISG 적용:     복합 11.0 / 도심  9.8 / 고속 12.7 km/ℓ · CO2 177g/km
연비 — 4WD ISG 미적용:   복합 10.5 / 도심  9.3 / 고속 12.4 km/ℓ · CO2 186g/km

공차중량: 2,060~2,180 kg (구성별 상이)
트림: T1, T2
```

### ④ 인포그래픽·카드 수치 스니펫
```
[렉스턴 2026 · 2.2 디젤]
2WD(ISG)  11.4km/ℓ | CO2 170g | 2,060kg | 4등급  ← 최고 연비 구성
4WD(ISG)  11.0km/ℓ | CO2 177g | 2,170kg | 4등급
※ 복합연비 기준 / ISG 적용 기준 수치
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 verdict 미인증 |
| 휠사이즈 | vehicle_powertrains.wheel null |
| 트림별 옵션 | 미수집 |
| 안전 등급 | 미수집 |
| ISG 세부 적용 트림 | DB 트림 매핑 불가 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-30_  
_data gate: verdict-rexton-20260611.md (GREEN) · commit 8877504_
