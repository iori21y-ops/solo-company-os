---
type: fact-block
title: 제네시스 GV80 쿠페 팩트블록 (quantitative · 2026년형 · 가솔린)
topic: gv80-coupe-factblock-quant
subject: 제네시스 GV80 쿠페 (2026년형 · 대형 가솔린 SUV 쿠페 · 2.5T · AWD · 20"/22")
date: 2026-06-24
data_source:
  - data/outputs/approved/verdict-gv80-coupe-20260611.md (quantitative/referential GREEN)
created: 2026-06-24
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-019-factblock-batch-20260624]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-gv80-coupe-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='gv80-coupe' (쿼리 2026-06-24, 3행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='gv80-coupe' (쿼리 2026-06-24, 2행)
data_gate: verdict-gv80-coupe-20260611 GREEN · DB == PDF 원문 일치 (수동 3자 대조 확정)
certified_scope: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠·구동방식
uncertified: 가격·이미지·트림별 스펙 매핑·안전등급
flags:
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.body_type null — DB 미입력. 데이터팀 보완 권고."
  - "제네시스 ICE 파서(_gs_parse_ice_fuel) 불안정 — 수동 PDF 3자 대조로 GREEN 확정. 파서 출력 자동 재INSERT 차단(GENESIS_ICE_AUTO_INSERT_BLOCKED=True). 콘텐츠 작성에는 영향 없음."
  - "2.5T AWD 20\" 2행 존재(id 525·526): 525(8.2/2,160 kg)·526(7.8/2,220 kg) — 공차중량 60 kg 차이. 트림(일반/BLACK) 또는 옵션 차이 추정. 단일 수치 사용 지양."
  - "vehicle_trims 2건만 수집(GV80 COUPE·GV80 COUPE BLACK) — Genesis ICE 파서 제한. 트림별 스펙 그룹 매핑 불가."
  - "vehicle_trims.base_price 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
  - "전 라인업 AWD 전용 — 2WD 미존재(쿠페 모델 특성)."
---

# GV80 쿠페 팩트 블록 — quantitative (2026년형 · 대형 가솔린 SUV 쿠페)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-gv80-coupe-20260611 GREEN · 수동 3자 대조 확정).  
> 인증 범위: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠·구동방식.  
> ⚠️ 제네시스 ICE 파서 불안정 → 수동 확정값. 수치 인용 시 원문 PDF 병행 확인 권장.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| model_code | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| body_type | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| Genesis ICE 파서 | ⚠️ 불안정 | 수동 PDF 3자 대조로 GREEN 확정. 파서 자동 re-INSERT 차단 중. |
| AWD 20" 2행 | ⚠️ 확인 권고 | 공차중량 60 kg 차이(2,160/2,220 kg) — 트림·옵션 차이 추정. 단일 수치 사용 지양. |
| vehicle_trims | ℹ️ 2건 | Genesis ICE 파서 제한 — 전체 트림 미반영 가능성. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 제네시스 | vehicles.brand |
| 모델명 | GV80 쿠페 | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 대형 | vehicles.segment |
| 카테고리 | SUV | vehicles.category |
| 엔진 라인업 | 2.5T (I4 2,497cc) | vehicle_powertrains |
| 연료 | 가솔린 | vehicle_powertrains.fuel_kind |
| 구동방식 | AWD 전용 | vehicle_powertrains.drive_type |
| 휠 | 20" / 22" | vehicle_powertrains.wheel |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 2.5T I4 — 2,497cc · AWD 전용 (공차중량 2,160~2,280 kg)

| 행 | 구동 | 휠 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|
| A | **AWD** | **20"** | **8.2 km/ℓ** | 7.3 | 9.5 | 209 g/km | **2,160 kg** | **5등급** |
| B | **AWD** | **20"** | **7.8 km/ℓ** | 6.8 | 9.3 | 220 g/km | **2,220 kg** | **5등급** |
| C | **AWD** | **22"** | **8.1 km/ℓ** | 7.3 | 9.3 | 212 g/km | **2,280 kg** | **5등급** |

> ※ 행 A·B: 동일 AWD 20"에 2행 존재. 공차중량 60 kg 차이(2,160 kg vs 2,220 kg), 연비 0.4 km/ℓ 차이 — 트림(일반/BLACK) 또는 옵션 차이 추정. 단일 수치 발행 지양.  
> ※ 행 C: AWD 22"(2,280 kg)가 행 B(20"·2,220 kg)보다 무겁고 효율은 행 B보다 높음(8.1 vs 7.8) — 발행 전 원문 확인 권장.

---

## 휠별 핵심 비교

| 항목 | 20" AWD 최고 | 20" AWD 최저 | 22" AWD |
|------|------------|------------|---------|
| 복합연비 | **8.2 km/ℓ** (행A) | 7.8 km/ℓ (행B) | 8.1 km/ℓ (행C) |
| CO2 | 209 g/km | 220 g/km | 212 g/km |
| 공차중량 | 2,160 kg | 2,220 kg | 2,280 kg |
| 에너지등급 | 5등급 | 5등급 | 5등급 |

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.  
> ⚠️ Genesis ICE 파서 제한으로 2건만 수집 — 전체 트림 미반영 가능성.

| 트림명 | 출고가 참고 | 세제혜택가 참고 |
|--------|-----------|--------------|
| GV80 COUPE | 81,400,000원 | 80,160,000원 |
| GV80 COUPE BLACK | 101,100,000원 | 99,670,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
제네시스 GV80 쿠페 2026 · 대형 가솔린 SUV 쿠페 · AWD · 최대 8.2km/ℓ (5등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
제네시스 GV80 쿠페 2026년형은 I4 2.5T(2,497cc) 가솔린 엔진에 AWD 전용 구성을 갖춘 대형 SUV 쿠페입니다.
20" 기준 최대 복합연비 8.2 km/ℓ(5등급)이며 22" 선택 시 8.1 km/ℓ입니다.
전 라인업이 AWD 전용으로 구성됩니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 제네시스
모델: GV80 쿠페 2026년형
세그먼트: 대형 SUV 쿠페
연료: 가솔린 (2.5T I4 2,497cc)
구동: AWD 전용

[AWD 20" — 기준 행(경량)]
복합연비: 8.2 km/ℓ (도심 7.3 / 고속 9.5)
CO2: 209 g/km
공차중량: 2,160 kg
에너지등급: 5등급

[AWD 22"]
복합연비: 8.1 km/ℓ (도심 7.3 / 고속 9.3)
CO2: 212 g/km
공차중량: 2,280 kg
에너지등급: 5등급
```

### ④ 인포그래픽·카드 수치 스니펫
```
[AWD 20" 최고]  8.2km/ℓ | CO2 209g | 2,160kg | 5등급  ← 최고 효율
[AWD 22"]       8.1km/ℓ | CO2 212g | 2,280kg | 5등급
[AWD 20" 중량]  7.8km/ℓ | CO2 220g | 2,220kg | 5등급
※ 복합연비 기준 / 제네시스 ICE 파서 불안정 → 수동 확정값, 발행 전 원문 확인 권장
※ AWD 20"에 2행 존재 — 단일 수치 발행 시 원문 확인 필수
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 外) |
| 트림별 스펙 매핑 | Genesis ICE 파서 제한 — 트림 2건만 수집 |
| 2WD 제원 | 쿠페 모델 미존재 (AWD 전용) |
| 안전 등급 | 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-24_  
_data gate: verdict-gv80-coupe-20260611.md (GREEN · 수동 3자 대조) · commit 8877504_
