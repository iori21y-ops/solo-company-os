---
type: fact-block
title: 현대 코나 팩트블록 (quantitative · 2024년형)
topic: kona-factblock-quant
subject: 현대 코나 SX2 (2024년형 · 1.6T가솔린/2.0가솔린 소형 SUV)
date: 2026-06-25
data_source:
  - data/outputs/approved/verdict-kona-20260611.md (quantitative/referential GREEN)
created: 2026-06-25
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-018-factblock-batch-20260625]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-kona-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='kona' (쿼리 2026-06-25, 5행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='kona' (쿼리 2026-06-25, 4행)
data_gate: verdict-kona-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·CO2·공차중량·구동방식·휠·에너지등급
uncertified: 가격·이미지
flags:
  - "vehicles.year=2024 — 현행 연식 DB 미갱신 가능성. 현재 2025/2026년형 출시 여부 데이터팀 확인 권고. 수치는 2024년형 기준."
  - "1.6T 18\" 행: raw_line '18\", 19\"' 병기 — 18\"/19\" 공유 제원(구분 수치 없음). 18\"·19\" 동일 수치 처리."
  - "1.6T 4WD 18\" 행: raw_line '18\", 19\"' 병기 — 동일 처리."
  - "2.0 가솔린: 2WD 전용 (4WD 행 없음, DB 원문 반영). IVT 변속기."
  - "kona-ev(전기)·kona-hybrid(하이브리드) 별도 slug — 본 팩트블록에 미포함."
  - "vehicle_trims.drive_type 전 행 null — 가격 참고용으로만 사용."
  - "vehicle_trims.base_price 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# 코나 팩트 블록 — quantitative (2024년형 · 가솔린)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-kona-20260611 GREEN).  
> 인증 범위: 연비(km/L)·CO2 배출량·공차중량·구동방식·휠·에너지등급.  
> ※ 코나 EV는 slug='kona-ev', 코나 하이브리드는 slug='kona-hybrid' 별도 팩트블록 참조.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| vehicles.year | ⚠️ 2024 | DB 연식 2024년형. 현행 연식 갱신 여부 데이터팀 확인 권고. |
| 1.6T 18"/19" 공유 제원 | ℹ️ 참고 | raw_line에 "18\", 19\"" 병기 — 두 휠 동일 수치. 개별 분리 불가. |
| 2.0 가솔린 4WD | ℹ️ 미수집 | 2WD 전용 (DB 원문 반영). |
| EV·하이브리드 | ℹ️ 별도 | kona-ev·kona-hybrid 별도 slug. 본 팩트블록 범위 외. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (HYUNDAI) | vehicles.brand |
| 모델명 | 코나 (KONA) | vehicles.name |
| 모델코드 | SX2 | vehicles.model_code |
| 연식 | 2024년형 (DB 기준) | vehicles.year |
| 세그먼트 | 소형 | vehicles.segment |
| 카테고리 | SUV | vehicles.category |
| 연료 | 가솔린 | vehicle_powertrains.fuel_kind |
| 엔진 라인업 | 1.6 터보 자동 8단 / 2.0 가솔린 IVT | vehicle_powertrains.engine |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 스마트스트림 가솔린 1.6 터보 자동 8단 (1,598cc)

| 행 | 휠 | 구동 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|
| A | 17" | 2WD | **13.0 km/L** | 11.5 | 15.5 | 128 g/km | 1,405 kg | **3등급** |
| B | 18"/19" | 2WD | **12.2 km/L** | 10.8 | 14.3 | 137 g/km | 1,420 kg | **3등급** |
| C | 18"/19" | 4WD | **11.2 km/L** | 10.0 | 13.1 | 150 g/km | 1,495 kg | **4등급** |

> ※ 행B·C: raw_line에 18"/19" 병기. 두 휠 동일 수치.

### 스마트스트림 가솔린 2.0 IVT (1,999cc · 2WD 전용)

| 행 | 휠 | 구동 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|
| D | 17" | 2WD | **13.6 km/L** | 12.6 | 15.0 | 121 g/km | 1,360 kg | **3등급** |
| E | 18"/19" | 2WD | **13.0 km/L** | 11.8 | 14.7 | 127 g/km | 1,375 kg | **3등급** |

> **핵심 포인트:**
> - 최고 연비: 2.0 가솔린 17" 2WD — **13.6 km/L (3등급)**, CO2 121 g/km
> - 2.0 vs 1.6T: 2.0 IVT가 17" 기준 0.6 km/L 더 효율적
> - 1.6T 3등급 달성: 17" 2WD·18"/19" 2WD
> - 1.6T 4WD: 4등급 (연비 11.2 km/L, CO2 150 g/km)
> - 2.0 가솔린: 4WD 없음 (2WD 전용)

---

## 연비·CO2 요약

| 엔진 | 최고연비 조합 | 연비(복합) | CO2 | 에너지등급 |
|------|-------------|-----------|-----|-----------|
| 2.0 가솔린 (IVT) | 17" 2WD | **13.6 km/L** | **121 g/km** | **3등급** |
| 1.6T 가솔린 | 17" 2WD | 13.0 km/L | 128 g/km | **3등급** |
| 1.6T 가솔린 (4WD) | 18"/19" 4WD | 11.2 km/L | 150 g/km | 4등급 |

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.  
> ⚠️ drive_type 전 행 null.

| 트림명 | 출고가 참고 |
|--------|-----------|
| 모던 | 25,160,000원 |
| 프리미엄 | 27,790,000원 |
| N라인 | 29,420,000원 |
| 인스퍼레이션 | 31,200,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 코나 SX2 2024 · 소형 SUV · 2.0가솔린 17" 기준 연비 13.6km/L(3등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 코나(KONA) SX2는 1.6 터보 가솔린과 2.0 가솔린 두 가지 파워트레인을 갖춘 소형 SUV입니다.
2.0 가솔린 17인치 2WD 기준 복합 연비 13.6 km/L(3등급, CO2 121 g/km)로 소형 SUV 중 높은 효율을 제공하며,
1.6 터보는 4WD 선택이 가능합니다.
코나 전기·하이브리드 제원은 별도 팩트블록을 참조하세요.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대(HYUNDAI)
모델: 코나(KONA) SX2 (2024년형 DB 기준)
세그먼트: 소형 SUV
연료: 가솔린
엔진: 1.6 터보 자동 8단 / 2.0 가솔린 IVT
구동방식: 2WD(공통) / 4WD(1.6T 전용)
연비(대표·2.0가솔린 17" 2WD): 13.6 km/L (3등급), CO2 121 g/km
연비(대표·1.6T 17" 2WD): 13.0 km/L (3등급), CO2 128 g/km
연비(대표·1.6T 4WD): 11.2 km/L (4등급), CO2 150 g/km
공차중량: 1,360~1,495 kg (엔진·구동·휠 조합별)
트림: 모던·프리미엄·N라인·인스퍼레이션
※ EV·하이브리드 제원 별도 문의
```

### ④ 인포그래픽·카드 수치 스니펫
```
[2.0가솔린 17" 2WD]   13.6km/L | CO2 121g/km | 1,360kg | 3등급  ← 최고연비
[2.0가솔린 18"/19" 2WD]  13.0km/L | CO2 127g/km | 1,375kg | 3등급
[1.6T 17" 2WD]        13.0km/L | CO2 128g/km | 1,405kg | 3등급
[1.6T 18"/19" 2WD]    12.2km/L | CO2 137g/km | 1,420kg | 3등급
[1.6T 18"/19" 4WD]    11.2km/L | CO2 150g/km | 1,495kg | 4등급
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 코나 EV 제원 | kona-ev 별도 slug |
| 코나 하이브리드 제원 | kona-hybrid 별도 slug |
| 2.0 가솔린 4WD | DB 미수집 (2WD 전용 원문 반영) |
| 최고출력·토크 | vehicle_powertrains 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-25_  
_data gate: verdict-kona-20260611.md (GREEN) · commit 8877504_
