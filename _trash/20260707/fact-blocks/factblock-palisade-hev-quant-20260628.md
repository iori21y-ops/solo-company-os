---
type: fact-block
title: 현대 팰리세이드 하이브리드 팩트블록 (quantitative · 2026 · 2.5 HEV)
topic: palisade-hev-factblock-quant
subject: 현대 팰리세이드 하이브리드 (2.5T HEV · 2026)
date: 2026-06-28
data_source:
  - data/outputs/approved/verdict-palisade-hev-20260611.md (quantitative/referential GREEN)
created: 2026-06-28
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-023-factblock-batch-20260628]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-palisade-hev-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='palisade-hev' (쿼리 2026-06-28, 15행 — 가솔린 8 + 하이브리드 7)
  - DB: vehicle_trims JOIN vehicles WHERE slug='palisade-hev' (쿼리 2026-06-28, 0건)
  - DB: vehicles WHERE slug='palisade-hev' (메타)
data_gate: verdict-palisade-hev-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비(km/L)·배기량·CO2·공차중량·구동방식·휠·에너지등급 (하이브리드 행)
uncertified: 가격·이미지·vehicles 메타(model_code null·segment null)
flags:
  - "vehicle_powertrains에 가솔린 행 8건 혼재(palisade 가솔린은 factblock-palisade-quant-20260613.md 참조). 본 블록은 hybrid 행(7건)만 수록."
  - "공차중량 7인승/9인승 이원화 — raw_line '2,080kg_7인승 / 2,115kg_9인승' 형식. DB curb_weight_kg는 7인승 기준값."
  - "model_code null, segment null — 대형 SUV 추정."
  - "vehicle_trims 0건 — 트림명·가격 미수집."
  - "2WD 21\" 행(id 170) 도심·고속 연비 동일(12.5/12.5 km/L) — raw_line 확인 권고."
  - "AWD 20\"·21\" 행 복합/도심/고속 동일(11.4/11.4/11.3) — 인치별 수치 동일 원문 그대로 보존."
---

# 팰리세이드 하이브리드 팩트 블록 — quantitative (현대 · 2026 · 2.5 HEV)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-palisade-hev-20260611 GREEN).  
> 인증 범위: 연비(km/L)·배기량·CO2·공차중량·구동방식·휠·에너지등급 (하이브리드 행).  
> ※ 가솔린 행(8건)은 factblock-palisade-quant-20260613.md 참조.  
> ※ 공차중량은 7인승 기준 DB값. 9인승은 raw_line 참고(+35~55 kg).

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| 가솔린 행 혼재 | ⚠️ 주의 | palisade-hev slug에 가솔린 8행 포함. 본 블록 HEV 7행만 사용. |
| 공차중량 이원화 | ⚠️ 확인 | 7인승 DB값 / 9인승 raw_line. 9인승: +35~55 kg. |
| 2WD 21" 연비 | ⚠️ 확인 | 도심·고속 동일(12.5/12.5) — raw_line 재확인 권고. |
| AWD 20"·21" | ℹ️ 동일 수치 | 복합·도심·고속·CO2 동일 — 원문 그대로 보존. |
| vehicle_trims | ℹ️ 미수집 | 트림명·가격 DB 없음. |
| model_code | ℹ️ null | 대형 SUV 추정. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (Hyundai) | vehicles.brand |
| 모델명 | 팰리세이드 하이브리드 | vehicles.name |
| 모델코드 | null (미수집) | vehicles.model_code |
| 연식 | 2026 | vehicles.year |
| 세그먼트 | null (대형 SUV 추정) | vehicles.segment |
| 차체 형태 | SUV | vehicles.body_type |
| 연료 | 하이브리드 (HEV) | vehicle_powertrains.fuel_kind |
| 엔진 | 2.5T (2,497 cc) · 자동 6단 | vehicle_powertrains.engine / displacement_cc |
| 인승 | 7인승 / 9인승 | vehicle_powertrains.engine 텍스트 |

---

## 제원 매트릭스 (vehicle_powertrains · 하이브리드 행만 · GREEN 인증)

> ※ 공차중량 DB값 = 7인승 기준. 9인승 공차중량은 raw_line 참고값 별기.

### 2.5T HEV · 자동 6단 · 2WD

| 행 | 휠 | 비고 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량(7인승) | (9인승 raw) | 에너지등급 |
|---|---|---|---|---|---|---|---|---|---|
| A | 18" | 표준 | **14.1 km/L** | 14.5 | 13.6 | 114 g/km | **2,080 kg** | 2,115 kg | **2등급** |
| B | 18" | 빌트인 캠 | 13.9 km/L | 14.0 | 13.7 | 116 g/km | 2,080 kg | 2,115 kg | 2등급 |
| C | 20" | 표준 | 12.7 km/L | 12.9 | 12.4 | 129 g/km | 2,110 kg | 2,145 kg | 3등급 |
| D | 21" | 표준 | 12.5 km/L | 12.5 ⚠️ | 12.5 ⚠️ | 131 g/km | 2,165 kg | 2,190 kg | 3등급 |

### 2.5T HEV · 자동 6단 · AWD

| 행 | 휠 | 비고 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량(7인승) | (9인승 raw) | 에너지등급 |
|---|---|---|---|---|---|---|---|---|---|
| E | 18" | 표준 | 12.5 km/L | 12.5 | 12.5 | 131 g/km | **2,150 kg** | 2,185 kg | **3등급** |
| F | 20" | 표준 | 11.4 km/L | 11.4 | 11.3 | 145 g/km | 2,180 kg | 2,215 kg | 4등급 |
| G | 21" | 표준 | 11.4 km/L | 11.4 | 11.3 | 145 g/km | 2,235 kg | 2,260 kg | 4등급 |

> **핵심 포인트 (HEV):**
> - 최고 연비: 2WD 18" 표준 **14.1 km/L** (도심 14.5 — 도심이 고속보다 효율적, HEV 특성)
> - 빌트인 캠 장착 시: 14.1 → 13.9 km/L (−0.2 km/L), CO2 114 → 116 g/km
> - 2WD→AWD 18": 12.5 km/L (−1.6 km/L)
> - 2WD 18"·AWD 18" 모두 자동 6단 (가솔린은 자동 8단과 구분)
> - AWD 20"·21" 수치 동일(11.4/11.4/11.3) — 원문 그대로 보존

---

## 연비 요약 (HEV · 전 조합)

| 구동 | 휠 | 비고 | 연비(복합) | CO2 | 공차중량(7인승) | 에너지등급 |
|------|----|----|-----------|-----|----------------|-----------|
| 2WD | 18" | 표준 | **14.1 km/L** | 114 g/km | 2,080 kg | **2등급** |
| 2WD | 18" | +빌트인캠 | 13.9 km/L | 116 g/km | 2,080 kg | 2등급 |
| 2WD | 20" | 표준 | 12.7 km/L | 129 g/km | 2,110 kg | 3등급 |
| 2WD | 21" | 표준 | 12.5 km/L | 131 g/km | 2,165 kg | 3등급 |
| AWD | 18" | 표준 | 12.5 km/L | 131 g/km | 2,150 kg | 3등급 |
| AWD | 20" | 표준 | 11.4 km/L | 145 g/km | 2,180 kg | 4등급 |
| AWD | 21" | 표준 | 11.4 km/L | 145 g/km | 2,235 kg | 4등급 |

---

## 트림 라인업 (vehicle_trims)

> ⚠️ vehicle_trims 0건 — 트림명·가격 DB 미수집. 별도 확인 필요.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 팰리세이드 HEV 2026 · 2WD 18" 복합 14.1km/L · CO2 114g/km · 2등급
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 팰리세이드 하이브리드(2026)는 2.5T HEV 파워트레인(자동 6단)을 탑재한 대형 SUV로, 2WD 18인치 기준 복합 연비 14.1 km/L·CO2 114 g/km·에너지 2등급을 달성합니다.
도심 연비(14.5 km/L)가 고속도로(13.6 km/L)보다 높아 하이브리드 특성이 잘 나타납니다.
AWD 선택 시 18인치 기준 12.5 km/L(3등급)으로 하락하며, 공차중량은 7인승 기준 2,080~2,235 kg(구성에 따라 상이)입니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대(Hyundai)
모델: 팰리세이드 하이브리드 (2026)
세그먼트: 대형 SUV (HEV) — segment null, 추정
파워트레인: 2.5T HEV 자동 6단
인승: 7인승 / 9인승
─ 2WD HEV ─
  연비(18" 표준): 복합 14.1 km/L | 도심 14.5 | 고속 13.6 | CO2 114g/km | 공차 2,080kg(7인)/2,115kg(9인) | 2등급
  연비(18" 빌트인캠): 복합 13.9 km/L | CO2 116g/km | 2등급
  연비(20"): 복합 12.7 km/L | CO2 129g/km | 3등급 | 공차 2,110/2,145kg
  연비(21"): 복합 12.5 km/L | CO2 131g/km | 3등급 | 공차 2,165/2,190kg
─ AWD HEV ─
  연비(18"): 복합 12.5 km/L | CO2 131g/km | 3등급 | 공차 2,150/2,185kg
  연비(20"): 복합 11.4 km/L | CO2 145g/km | 4등급 | 공차 2,180/2,215kg
  연비(21"): 복합 11.4 km/L | CO2 145g/km | 4등급 | 공차 2,235/2,260kg
가솔린: factblock-palisade-quant-20260613.md 참조
```

### ④ 인포그래픽·카드 수치 스니펫
```
[팰리세이드 HEV 2WD 18" 표준]   14.1km/L | CO2 114g/km | 2등급 | 2,080kg(7인)
[팰리세이드 HEV 2WD 18" 빌트인캠] 13.9km/L | CO2 116g/km | 2등급
[팰리세이드 HEV AWD 18"]         12.5km/L | CO2 131g/km | 3등급 | 2,150kg(7인)
[팰리세이드 HEV AWD 20-21"]      11.4km/L | CO2 145g/km | 4등급
※ 가격·트림명 미수집 / 9인승 공차중량은 raw_line 참고 (+35~55kg)
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 가솔린 제원 | factblock-palisade-quant-20260613.md 별도 참조 |
| 트림명 · 트림별 제원 | vehicle_trims 0건 — DB 미수집 |
| model_code / segment | DB null — 추정값 발행 금지 |
| 9인승 공차중량 DB값 | curb_weight_kg 7인승 기준 — 9인승은 raw_line 참고 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-28_  
_data gate: verdict-palisade-hev-20260611.md (GREEN) · commit 8877504_
