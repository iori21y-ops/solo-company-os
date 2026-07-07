---
type: fact-block
title: KGM 액티언 하이브리드 팩트블록 (quantitative · 2026년형)
topic: actyon-hybrid-factblock-quant
subject: KGM 액티언 하이브리드 (2026년형 · 1.5T e-DHT 하이브리드 SUV)
date: 2026-06-18
data_source:
  - data/outputs/approved/verdict-actyon-hybrid-20260611.md (quantitative/referential GREEN)
created: 2026-06-18
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-011-factblock-batch-20260618]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-actyon-hybrid-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='actyon-hybrid' (쿼리 2026-06-18, 2행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='actyon-hybrid' (쿼리 2026-06-18, 1행)
data_gate: verdict-actyon-hybrid-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠(20인치)·타이어 구분
uncertified: 가격·이미지·구동방식(Row B)·안전등급·segment·category
flags:
  - "vehicles.segment null — DB 미입력. 액티언 동급(준중형 SUV) 추정. 데이터팀 보완 권고."
  - "vehicles.category null — DB 미입력. SUV 추정. 데이터팀 보완 권고."
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.body_type null — DB 미입력. 데이터팀 보완 권고."
  - "vehicle_powertrains Row B drive_type null — 미쉐린 타이어 행, 2WD 추정. 데이터팀 확인 권고."
  - "vehicle_trims.base_price 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# 액티언 하이브리드 팩트 블록 — quantitative (2026년형 · 1.5T e-DHT HEV)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-actyon-hybrid-20260611 GREEN).  
> 인증 범위: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠(20인치)·타이어 구분.  
> segment·category·Row B 구동방식은 DB 미입력 — 참고용.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| segment | ℹ️ null | DB 미입력. 준중형 SUV(액티언 동급) 추정. |
| category | ℹ️ null | DB 미입력. SUV 추정. |
| model_code | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| body_type | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| Row B drive_type | ⚠️ null | 미쉐린 타이어 행. 2WD 추정이나 DB 미기재 — 데이터팀 확인 권고. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | KGM | vehicles.brand |
| 모델명 | 액티언 하이브리드 (Actyon Hybrid) | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | — (null, 준중형 SUV 추정) | vehicles.segment |
| 카테고리 | — (null, SUV 추정) | vehicles.category |
| 연료 | 하이브리드 (HEV) | vehicle_powertrains.fuel_kind |
| 배기량 | 1,498cc (1.5T) | vehicle_powertrains.displacement_cc |
| 변속기 | e-DHT 하이브리드 변속기 | vehicle_powertrains.engine |
| 휠 | 20인치 (넥센 / 미쉐린 선택) | vehicle_powertrains.wheel |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> Row A: 20인치 넥센 타이어 / Row B: 20인치 미쉐린 타이어 (타이어 옵션 차이).  
> Row B drive_type DB null — 2WD 추정. 데이터팀 확인 권고.

| 행 | 휠 | 타이어 | 구동 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|---|
| A | 20" | 넥센 | 2WD | **15.0 km/ℓ** | 15.6 | 14.2 | 107 g/km | **1,730 kg** | **2등급** |
| B | 20" | 미쉐린 | 2WD(추정) | **14.9 km/ℓ** | 15.8 | 13.9 | 107 g/km | **1,730 kg** | **2등급** |

> **핵심 포인트:**
> - 타이어 옵션에 따른 복합연비 차이 0.1 km/ℓ (넥센 15.0 > 미쉐린 14.9)
> - 도심 연비는 미쉐린 행이 소폭 우위 (15.8 > 15.6), 고속은 넥센 행 우위 (14.2 > 13.9)
> - CO2·공차중량 동일 (107 g/km, 1,730 kg) — 두 행 모두 2등급
> - 액티언 가솔린(2WD 10.8 km/ℓ) 대비 연비 약 39% 개선, CO2 30% 절감
> - 저공해 인증 여부: raw_line에 명시 없음 — 발행 전 확인 권고

---

## 액티언 vs 액티언 하이브리드 비교 (2WD 기준)

| 구분 | 액티언 (2WD) | 액티언 하이브리드 (2WD·넥센) | 차이 |
|------|-------------|---------------------------|------|
| 연비(복합) | 10.8 km/ℓ | 15.0 km/ℓ | **+4.2 (+39%)** |
| CO2 | 152 g/km | 107 g/km | **−45 (−30%)** |
| 공차중량 | 1,590 kg | 1,730 kg | +140 kg |
| 에너지등급 | 4등급 | **2등급** | — |

> ※ 비교 수치는 인증 범위 내 제원. 가격 차이는 별도 가격 verdict 인증 필요.

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | 출고가 참고 |
|--------|-----------|
| S8 | 38,900,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
KGM 액티언 하이브리드 2026 · 1.5T e-DHT · 2WD 복합 15.0km/ℓ (2등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
KGM 액티언 하이브리드 2026년형은 1.5T e-DHT 하이브리드 시스템을 탑재한 준중형 SUV입니다.
20인치 타이어(넥센) 기준 복합 15.0 km/ℓ(도심 15.6 / 고속 14.2), CO2 107 g/km으로
에너지소비효율 2등급을 달성했습니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: KGM
모델: 액티언 하이브리드 2026년형
연료: 하이브리드 (HEV)
배기량: 1,498cc (1.5T)
변속기: e-DHT 하이브리드 변속기
구동방식: 2WD
휠: 20인치
연비 (넥센): 복합 15.0 / 도심 15.6 / 고속 14.2 km/ℓ
연비 (미쉐린): 복합 14.9 / 도심 15.8 / 고속 13.9 km/ℓ
CO2: 107 g/km
공차중량: 1,730 kg
에너지등급: 2등급
```

### ④ 인포그래픽·카드 수치 스니펫
```
[2WD·넥센]   15.0km/ℓ | CO2 107g | 1,730kg | 2등급  ← 추천
[2WD·미쉐린] 14.9km/ℓ | CO2 107g | 1,730kg | 2등급
※ 복합연비 기준 / 20인치
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 전기 모터 출력 | vehicle_powertrains 미수집 |
| EV 주행거리 | HEV (순수 전기 주행거리 해당 없음) |
| 안전 등급 | 미수집 |
| 저공해 등급 | raw_line 미명시 — 발행 전 확인 권고 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-18_  
_data gate: verdict-actyon-hybrid-20260611.md (GREEN) · commit 8877504_
