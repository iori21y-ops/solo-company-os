---
type: fact-block
title: 제네시스 GV70 팩트블록 (quantitative · 2026년형)
topic: gv70-factblock-quant
subject: 제네시스 GV70 (2026년형 · 가솔린 중형 SUV)
date: 2026-06-17
data_source:
  - data/outputs/approved/verdict-gv70-20260611.md (quantitative/referential GREEN)
created: 2026-06-17
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-010-factblock-batch-20260617]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-gv70-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='gv70' (쿼리 2026-06-17, 10행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='gv70' (쿼리 2026-06-17, 1행)
data_gate: verdict-gv70-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·CO2·공차중량·구동방식·휠·에너지등급
uncertified: 가격·이미지·트림 상세 (Genesis ICE 파서 제한)
flags:
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.body_type null — 중형 SUV 추정. 데이터팀 보완 권고."
  - "vehicle_trims 1건만 존재(54,000,000원) — Genesis ICE 파서 불안정으로 트림 데이터 수집 제한. 참고 불가 수준."
  - "Genesis ICE 파서 자동 재INSERT 차단 중 (verify_powertrains.py GENESIS_ICE_AUTO_INSERT_BLOCKED=True) — 콘텐츠 작성에는 무관."
  - "gv70ev(전기버전)은 별도 slug로 관리 — 본 팩트블록은 가솔린 한정."
  - "vehicle_trims.base_price는 가격 verdict 미인증 — 참고 불가. 발행 전 별도 가격 인증 필수."
---

# GV70 팩트 블록 — quantitative (2026년형 · 가솔린)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-gv70-20260611 GREEN).  
> 인증 범위: 연비(km/L)·CO2 배출량·공차중량·구동방식·휠·에너지등급.  
> ※ 본 팩트블록은 가솔린 GV70 한정. 전동화 모델(GV70 전동화)은 slug='gv70ev' 별도 처리.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| model_code | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| body_type | ℹ️ null | 중형 SUV 추정. |
| 트림 데이터 | ⚠️ 불완전 | vehicle_trims 1건만 수집 — Genesis ICE 파서 제한. 트림 수치·상세 사용 금지. |
| Genesis ICE 파서 | ℹ️ 내부 이슈 | 파서 출력 자동 재INSERT 차단 중 — 수동 PDF 검증 완료(DB == PDF). 콘텐츠 사용 안전. |
| gv70ev | ℹ️ 별도 | 전동화(전기) 버전은 slug='gv70ev'로 별도 관리. |
| 가격 데이터 | 📌 참고 불가 | 트림 데이터 불완전. 발행 전 별도 가격 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 제네시스 (Genesis) | vehicles.brand |
| 모델명 | GV70 | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 중형 | vehicles.segment |
| 카테고리 | SUV | vehicles.category |
| 연료 | 가솔린 | vehicle_powertrains.fuel_kind |
| 엔진 라인업 | 2.5 T-GDi (I4) / 3.5 T-GDi (V6) | vehicle_powertrains.engine |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 2.5 T-GDi (I4 · 2,497cc)

| 휠 | 구동 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|----|------|-----------|-----------|-----------|-----|---------|-----------|
| 18" | 2WD | **10.2 km/L** | 8.9 | 12.5 | 164 g/km | 1,865 kg | **4등급** |
| 18" | AWD | 9.7 km/L | 8.4 | 11.8 | 174 g/km | 1,930 kg | 4등급 |
| 19" | 2WD | 9.8 km/L | 8.5 | 11.8 | 172 g/km | 1,875 kg | 4등급 |
| 19" | AWD | 9.4 km/L | 8.2 | 11.4 | 180 g/km | 1,940 kg | 4등급 |
| 21" | 2WD | 9.7 km/L | 8.5 | 11.6 | 174 g/km | 1,895 kg | 4등급 |
| 21" | AWD | 9.0 km/L | 7.9 | 10.8 | 187 g/km | 1,960 kg | **5등급** |

### 3.5 T-GDi (V6 · 3,470cc)

| 휠 | 구동 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|----|------|-----------|-----------|-----------|-----|---------|-----------|
| 19" | 2WD | 8.9 km/L | 7.8 | 10.9 | 189 g/km | 1,950 kg | **5등급** |
| 19" | AWD | 8.5 km/L | 7.5 | 10.2 | 199 g/km | 2,015 kg | 5등급 |
| 21" | 2WD | 8.5 km/L | 7.5 | 10.1 | 199 g/km | 1,970 kg | 5등급 |
| 21" | AWD | 8.3 km/L | 7.3 | 9.8 | 205 g/km | 2,035 kg | 5등급 |

> **핵심 포인트:**
> - 최고 연비: 2.5T 18" 2WD — **10.2 km/L (4등급)**
> - 2.5T 전 조합 4등급 (단, 21" AWD는 5등급)
> - 3.5T 전 조합 5등급
> - 2WD→AWD 전환 시 공차중량 약 65~80 kg 증가, CO2 약 6~18 g/km 증가
> - 18" 기준 최저 CO2: 2.5T 2WD 164 g/km

---

## 등급별 요약

| 엔진 | 최고연비 조합 | 연비(복합) | CO2 | 에너지등급 |
|------|-------------|-----------|-----|-----------|
| 2.5 T-GDi | 18" 2WD | **10.2 km/L** | 164 g/km | **4등급** |
| 2.5 T-GDi | 21" AWD | 9.0 km/L | 187 g/km | 5등급 |
| 3.5 T-GDi | 19" 2WD | 8.9 km/L | 189 g/km | 5등급 |
| 3.5 T-GDi | 21" AWD | 8.3 km/L | 205 g/km | 5등급 |

---

## 트림 라인업 (vehicle_trims · 참고 불가)

> ⚠️ Genesis ICE 파서 제한으로 1건만 수집. 트림 상세·가격 사용 금지.

| 트림명 | 참고가 |
|--------|--------|
| GV70 | 54,000,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
제네시스 GV70 2026 · 2.5T 가솔린 18" 2WD 기준 연비 10.2km/L(4등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
제네시스 GV70 2026년형은 2.5 터보 GDi(I4)와 3.5 터보 GDi(V6) 두 가지 가솔린 엔진을 제공하는 중형 럭셔리 SUV입니다.
2.5T 18인치 2WD 기준 복합 연비 10.2 km/L(4등급)을 달성하며, 2WD와 AWD를 선택할 수 있습니다.
3.5T 모델은 전 조합 5등급이며, 최저 복합 연비는 V6 21" AWD 기준 8.3 km/L입니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 제네시스(Genesis)
모델: GV70 (2026년형)
연료: 가솔린
엔진: 2.5 T-GDi(I4) / 3.5 T-GDi(V6)
구동방식: 2WD / AWD
연비(대표·2.5T 18" 2WD): 10.2 km/L (4등급)
연비(대표·3.5T 19" 2WD): 8.9 km/L (5등급)
CO2(대표·2.5T 18" 2WD): 164 g/km
공차중량: 1,865~2,035 kg (엔진·구동·휠 조합별)
※ 전동화 버전(GV70 전동화)은 별도 문의
```

### ④ 인포그래픽·카드 수치 스니펫
```
[2.5T 18" 2WD] 10.2km/L | CO2 164g | 1,865kg | 4등급  ← 최고연비
[2.5T 19" 2WD] 9.8km/L  | CO2 172g | 1,875kg | 4등급
[2.5T 21" AWD] 9.0km/L  | CO2 187g | 1,960kg | 5등급
[3.5T 19" 2WD] 8.9km/L  | CO2 189g | 1,950kg | 5등급
[3.5T 21" AWD] 8.3km/L  | CO2 205g | 2,035kg | 5등급
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 트림 데이터 불완전 + 가격 verdict 미인증 |
| 트림 상세 스펙 | Genesis ICE 파서 제한으로 수집 불가 |
| 최고출력·토크 | vehicle_powertrains 미수집 |
| 변속기 | vehicle_powertrains 미수집 (8단 자동 추정) |

---

_작성: 컨텐츠_  
_작성일: 2026-06-17_  
_data gate: verdict-gv70-20260611.md (GREEN) · commit 8877504_
