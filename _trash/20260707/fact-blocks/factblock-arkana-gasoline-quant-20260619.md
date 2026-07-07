---
type: fact-block
title: 르노코리아 아르카나 1.6 GTe 팩트블록 (quantitative · 2027년형 · 가솔린)
topic: arkana-gasoline-factblock-quant
subject: 르노코리아 아르카나 1.6 GTe (2027년형 · 1.6 가솔린 CVT 준중형 SUV)
date: 2026-06-19
data_source:
  - data/outputs/approved/verdict-arkana-gasoline-20260611.md (quantitative/referential GREEN)
created: 2026-06-19
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-012-factblock-batch-20260619]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-arkana-gasoline-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='arkana-gasoline' (쿼리 2026-06-19, 1행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='arkana-gasoline' (쿼리 2026-06-19, 1행)
data_gate: verdict-arkana-gasoline-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠
uncertified: 가격·이미지·구동방식(drive_type)·안전등급·트림별 옵션
flags:
  - "vehicles.segment null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.category null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.body_type null — DB 미입력. 데이터팀 보완 권고."
  - "vehicle_powertrains.drive_type null — FWD 추정(1.6 GTe FWD 전용). 원문 확인 권고."
  - "vehicles.year = 2027년형 — 주의: 2027년형 기준 수치."
  - "vehicle_trims.base_price 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# 아르카나 1.6 GTe 팩트 블록 — quantitative (2027년형 · 가솔린 CVT)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-arkana-gasoline-20260611 GREEN).  
> 인증 범위: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠.  
> 구동방식(drive_type) null — 아르카나 1.6 GTe는 FWD 전용으로 알려졌으나 DB 미기재, 발행 전 원문 확인 권고.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| segment | ℹ️ null | vehicles 테이블 DB 미입력. 데이터팀 보완 권고. |
| category | ℹ️ null | vehicles 테이블 DB 미입력. 데이터팀 보완 권고. |
| model_code | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| body_type | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| drive_type | ⚠️ null | FWD 전용 추정. 원문 확인 필요. |
| 연식 | 📌 2027년형 | 수치는 2027년형 기준. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 르노코리아 | vehicles.brand |
| 모델명 | 아르카나 1.6 GTe | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2027년형 | vehicles.year |
| 세그먼트 | — (null) | vehicles.segment |
| 카테고리 | — (null) | vehicles.category |
| 연료 | 가솔린 | vehicle_powertrains.fuel_kind |
| 배기량 | 1,598cc (1.6) | vehicle_powertrains.displacement_cc |
| 변속기 | 무단(CVT) | vehicle_powertrains.engine (raw) |
| 구동방식 | — (null, FWD 추정) | vehicle_powertrains.drive_type |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

| 행 | 휠 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|
| A | **17"** | **13.6 km/ℓ** | 12.3 | 15.6 | 121 g/km | **1,300 kg** | **3등급** |

> **핵심 포인트:**
> - 복합연비 13.6 km/ℓ (3등급) — 동급 가솔린 SUV 일반 수준
> - 고속(15.6) > 도심(12.3) — 일반 가솔린 특성상 고속 주행 효율 우수
> - HEV 버전(17.4km/ℓ) 대비 복합 3.8 km/ℓ 열세, CO2 30 g/km 더 많음
> - 공차중량 1,300 kg — HEV(1,440kg) 대비 140 kg 가벼움

---

## 아르카나 HEV vs 가솔린 비교

| 항목 | 아르카나 HEV | 아르카나 1.6 GTe | 차이 |
|------|------------|----------------|------|
| 연비(복합) | 17.4 km/ℓ | 13.6 km/ℓ | HEV +3.8 |
| CO2 | 91 g/km | 121 g/km | GTe +30 |
| 공차중량 | 1,440 kg | 1,300 kg | GTe -140 |
| 에너지등급 | 1등급 | 3등급 | HEV 2단계 유리 |
| 변속기 | 자동 4+2단 | CVT | — |

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | 출고가 참고 |
|--------|-----------|
| 아이코닉 | 26,800,000원 |

> HEV 아이코닉(34,650,000) 대비 약 7,850,000원 낮음 (참고용).

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
르노 아르카나 1.6 GTe 2027 · 가솔린 CVT · 복합 13.6km/ℓ (3등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
르노코리아 아르카나 1.6 GTe 2027년형은 1.6 가솔린 CVT를 탑재한 준중형 SUV 엔트리 모델입니다.
복합연비 13.6 km/ℓ(도심 12.3 / 고속 15.6), CO2 121 g/km이며 에너지소비효율 3등급,
공차중량 1,300 kg으로 HEV 버전 대비 140 kg 가볍습니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 르노코리아
모델: 아르카나 1.6 GTe 2027년형
연료: 가솔린
배기량: 1,598cc (1.6)
변속기: 무단 CVT
구동방식: FWD 추정 (DB null)
연비 (복합): 13.6 km/ℓ
연비 (도심): 12.3 km/ℓ
연비 (고속): 15.6 km/ℓ
CO2: 121 g/km
공차중량: 1,300 kg
에너지등급: 3등급
휠: 17인치
```

### ④ 인포그래픽·카드 수치 스니펫
```
[가솔린 CVT 17"]  13.6km/ℓ | CO2 121g | 1,300kg | 3등급
※ 복합연비 기준 / HEV 대비 연비 -3.8, 공차중량 -140kg
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 구동방식 | vehicle_powertrains.drive_type null — 원문 확인 필요 |
| 트림별 옵션 스펙 | 미수집 |
| 안전 등급 | 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-19_  
_data gate: verdict-arkana-gasoline-20260611.md (GREEN) · commit 8877504_
