---
type: fact-block
title: 제네시스 G80 팩트블록 (quantitative · 2026년형 · 가솔린)
topic: g80-factblock-quant
subject: 제네시스 G80 (2026년형 · 대형 세단 · 2.5T/3.5T 가솔린 · 2WD/AWD · 18"~20")
date: 2026-06-22
data_source:
  - data/outputs/approved/verdict-g80-20260611.md (quantitative/referential GREEN)
created: 2026-06-22
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-015-factblock-batch-20260622]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-g80-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='g80' (쿼리 2026-06-22, 10행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='g80' (쿼리 2026-06-22, 2행)
data_gate: verdict-g80-20260611 GREEN · DB == PDF 원문 일치 (수동 3자 대조 확정)
certified_scope: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠·구동방식
uncertified: 가격·이미지·트림별 스펙 매핑·안전등급
flags:
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.body_type null — DB 미입력. 데이터팀 보완 권고."
  - "제네시스 ICE 파서(_gs_parse_ice_fuel) 불안정 — 수동 PDF 3자 대조로 GREEN 확정. 파서 출력 자동 재INSERT 차단(GENESIS_ICE_AUTO_INSERT_BLOCKED=True). 콘텐츠 작성에는 영향 없음."
  - "vehicle_powertrains에 spec_idx 별도 컬럼 없음 — raw_line 내 '_spec_idx' 값 참조(2.5T=0, 3.5T=1)."
  - "3.5T 2WD 19\"/20\": 연비·CO2 동일(8.8·193)이나 공차중량 5 kg 차이(1930/1935) — spec 그룹 내 미세 차이, 타이어 사이즈별 정상 범위 내."
  - "3.5T AWD 19\"/20\": 연비·CO2 동일(8.2·209)이나 공차중량 5 kg 차이(2000/2005) — 동상."
  - "vehicle_trims 2건만 수집(G80·G80 Black) — Genesis ICE 파서 제한. 트림별 스펙 그룹 매핑 불가."
  - "vehicle_trims.base_price 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# G80 팩트 블록 — quantitative (2026년형 · 대형 가솔린 세단)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-g80-20260611 GREEN · 수동 3자 대조 확정).  
> 인증 범위: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠·구동방식.  
> ⚠️ 제네시스 ICE 파서 불안정 → 수동 확정값. 수치 인용 시 원문 PDF 병행 확인 권장.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| model_code | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| body_type | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| Genesis ICE 파서 | ⚠️ 불안정 | 수동 PDF 3자 대조로 GREEN 확정. 파서 자동 re-INSERT 차단 중. |
| 3.5T 동일 휠 2행 | ℹ️ 미세 중량 차 | 2WD·AWD 각 19"/20"에 공차중량 5 kg 차이 2행 존재 — 정상 범위. |
| vehicle_trims | ℹ️ 2건 | Genesis ICE 파서 제한 — 전체 트림 미반영 가능성. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 제네시스 | vehicles.brand |
| 모델명 | G80 | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 대형 | vehicles.segment |
| 카테고리 | 세단 | vehicles.category |
| 엔진 라인업 | 2.5T (I4 2,497cc) / 3.5T (V6 3,470cc) | vehicle_powertrains |
| 연료 | 가솔린 | vehicle_powertrains.fuel_kind |
| 구동방식 | 2WD / AWD | vehicle_powertrains.drive_type |
| 휠 | 18" / 19" / 20" | vehicle_powertrains.wheel |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 2.5T I4 — 2,497cc (공차중량 1,830~1,920 kg)

| 행 | 구동 | 휠 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|
| A | **2WD** | **18"** | **10.5 km/ℓ** | 9.1 | 13.2 | 159 g/km | **1,830 kg** | **4등급** |
| B | **2WD** | **19"** | **10.1 km/ℓ** | 8.7 | 12.6 | 166 g/km | **1,845 kg** | **4등급** |
| C | **2WD** | **20"** | **9.9 km/ℓ** | 8.6 | 12.2 | 169 g/km | **1,850 kg** | **4등급** |
| D | **AWD** | **18"** | **9.8 km/ℓ** | 8.4 | 12.4 | 171 g/km | **1,900 kg** | **4등급** |
| E | **AWD** | **19"** | **9.5 km/ℓ** | 8.1 | 11.9 | 177 g/km | **1,915 kg** | **4등급** |
| F | **AWD** | **20"** | **9.4 km/ℓ** | 8.1 | 11.7 | 179 g/km | **1,920 kg** | **4등급** |

---

### 3.5T V6 — 3,470cc (공차중량 1,930~2,005 kg)

| 행 | 구동 | 휠 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|
| G | **2WD** | **19"** | **8.8 km/ℓ** | 7.6 | 11.0 | 193 g/km | **1,930 kg** | **5등급** |
| H | **2WD** | **20"** | **8.8 km/ℓ** | 7.6 | 11.0 | 193 g/km | **1,935 kg** | **5등급** |
| I | **AWD** | **19"** | **8.2 km/ℓ** | 7.1 | 10.2 | 209 g/km | **2,000 kg** | **5등급** |
| J | **AWD** | **20"** | **8.2 km/ℓ** | 7.1 | 10.2 | 209 g/km | **2,005 kg** | **5등급** |

> ※ 3.5T는 19" 전용 / 20" 옵션만 수집 — 18" 미수집 (파서 제한 가능성).

---

## 엔진별 핵심 비교

| 항목 | 2.5T 최고 | 2.5T 최저 | 3.5T 최고 | 3.5T 최저 |
|------|-----------|-----------|-----------|-----------|
| 복합연비 | 10.5 km/ℓ (18" 2WD) | 9.4 km/ℓ (20" AWD) | 8.8 km/ℓ (19"/20" 2WD) | 8.2 km/ℓ (19"/20" AWD) |
| 최저 CO2 | 159 g/km | 179 g/km | 193 g/km | 209 g/km |
| 공차중량 범위 | 1,830~1,850 kg (2WD) | 1,900~1,920 kg (AWD) | 1,930~1,935 kg (2WD) | 2,000~2,005 kg (AWD) |
| 에너지등급 | 4등급 | 4등급 | 5등급 | 5등급 |

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.  
> ⚠️ Genesis ICE 파서 제한으로 2건만 수집 — 전체 트림 미반영 가능성.

| 트림명 | 출고가 참고 |
|--------|-----------|
| G80 | 60,700,000원 |
| G80 Black | 83,700,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
제네시스 G80 2026 · 대형 가솔린 세단 · 2.5T 최대 10.5km/ℓ (4등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
제네시스 G80 2026년형은 I4 2.5T와 V6 3.5T 두 가지 가솔린 엔진을 갖춘 대형 세단입니다.
2.5T(2,497cc) 기준 최대 복합연비 10.5 km/ℓ(4등급), 3.5T(3,470cc) 기준 최대 8.8 km/ℓ(5등급)이며,
2WD·AWD와 18"~20" 휠 선택이 가능합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 제네시스
모델: G80 2026년형
세그먼트: 대형 세단
연료: 가솔린 (2.5T / 3.5T)

[2.5T I4 2,497cc]
최대 복합연비: 10.5 km/ℓ (18" 2WD)
CO2 범위: 159~179 g/km
공차중량: 1,830~1,920 kg
에너지등급: 4등급
구동·휠: 2WD 18"/19"/20", AWD 18"/19"/20"

[3.5T V6 3,470cc]
최대 복합연비: 8.8 km/ℓ (19"/20" 2WD)
CO2 범위: 193~209 g/km
공차중량: 1,930~2,005 kg
에너지등급: 5등급
구동·휠: 2WD 19"/20", AWD 19"/20"
```

### ④ 인포그래픽·카드 수치 스니펫
```
[2.5T 18" 2WD]  10.5km/ℓ | CO2 159g | 1,830kg | 4등급  ← 최고 효율
[2.5T 19" 2WD]  10.1km/ℓ | CO2 166g | 1,845kg | 4등급
[2.5T 20" 2WD]   9.9km/ℓ | CO2 169g | 1,850kg | 4등급
[2.5T 18" AWD]   9.8km/ℓ | CO2 171g | 1,900kg | 4등급
[2.5T 19" AWD]   9.5km/ℓ | CO2 177g | 1,915kg | 4등급
[2.5T 20" AWD]   9.4km/ℓ | CO2 179g | 1,920kg | 4등급
[3.5T 19" 2WD]   8.8km/ℓ | CO2 193g | 1,930kg | 5등급
[3.5T 20" 2WD]   8.8km/ℓ | CO2 193g | 1,935kg | 5등급
[3.5T 19" AWD]   8.2km/ℓ | CO2 209g | 2,000kg | 5등급
[3.5T 20" AWD]   8.2km/ℓ | CO2 209g | 2,005kg | 5등급
※ 복합연비 기준 / 제네시스 ICE 파서 불안정 → 수동 확정값, 발행 전 원문 확인 권장
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 트림별 스펙 매핑 | Genesis ICE 파서 제한 — 트림 2건만 수집 |
| 3.5T 18" 데이터 | 파서 미수집 (존재 여부 불명) |
| 안전 등급 | 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-22_  
_data gate: verdict-g80-20260611.md (GREEN · 수동 3자 대조) · commit 8877504_
