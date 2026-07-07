---
type: fact-block
title: KGM 액티언 팩트블록 (quantitative · 2026년형)
topic: actyon-factblock-quant
subject: KGM 액티언 (2026년형 · 1.5T 가솔린 준중형 SUV)
date: 2026-06-18
data_source:
  - data/outputs/approved/verdict-actyon-20260611.md (quantitative/referential GREEN)
created: 2026-06-18
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-011-factblock-batch-20260618]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-actyon-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='actyon' (쿼리 2026-06-18, 2행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='actyon' (쿼리 2026-06-18, 1행)
data_gate: verdict-actyon-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비(복합/도심/고속)·CO2·공차중량·구동방식·배기량·에너지등급
uncertified: 가격·이미지·휠사이즈·안전등급·트림별 옵션
flags:
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.body_type null — DB 미입력. 데이터팀 보완 권고."
  - "vehicle_powertrains.wheel null 전 행 — 휠사이즈 미수록. 원문 확인 권고."
  - "vehicle_trims.base_price 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# 액티언 팩트 블록 — quantitative (2026년형 · 1.5T 가솔린)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-actyon-20260611 GREEN).  
> 인증 범위: 연비(복합/도심/고속)·CO2·공차중량·구동방식·배기량·에너지등급.  
> 휠사이즈·트림별 옵션 등은 인증 범위 외.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| model_code | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| body_type | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| 휠사이즈 | ℹ️ null | vehicle_powertrains.wheel 전 행 null — 원문 확인 권고. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | KGM | vehicles.brand |
| 모델명 | 액티언 (Actyon) | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 준중형 | vehicles.segment |
| 카테고리 | SUV | vehicles.category |
| 연료 | 가솔린 | vehicle_powertrains.fuel_kind |
| 배기량 | 1,497cc (1.5T) | vehicle_powertrains.displacement_cc |
| 변속기 | 자동 8단 | vehicle_powertrains.engine |
| 저공해 | 3종 | raw_line |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

| 행 | 구동 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|
| A | **2WD** | **10.8 km/ℓ** | 9.8 | 12.2 | 152 g/km | **1,590 kg** | **4등급** |
| B | **4WD** | **10.2 km/ℓ** | 9.1 | 11.8 | 164 g/km | **1,680 kg** | **4등급** |

> **핵심 포인트:**
> - 2WD → 4WD 전환 시 복합연비 0.6 km/ℓ 하락 (10.8→10.2), CO2 12 g/km 증가
> - 공차중량 차이: 4WD가 90 kg 무거움 (1,590→1,680 kg)
> - 전 구동 조합 4등급 — 저공해 3종 인증 (환경부 인증 차종)

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | 출고가 참고 |
|--------|-----------|
| S8 | 35,170,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
KGM 액티언 2026 · 1.5T 가솔린 SUV · 2WD 복합 10.8km/ℓ (4등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
KGM 액티언 2026년형은 1.5T 가솔린 터보 엔진에 자동 8단 변속기를 탑재한 준중형 SUV입니다.
2WD 기준 복합 연비 10.8 km/ℓ(도심 9.8 / 고속 12.2), 공차중량 1,590 kg으로
저공해 3종 인증을 획득했으며, 4WD 선택 시 복합 10.2 km/ℓ입니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: KGM
모델: 액티언 2026년형
연료: 가솔린
배기량: 1,497cc (1.5T 터보)
변속기: 자동 8단
구동방식: 2WD / 4WD
연비 (2WD): 복합 10.8 / 도심 9.8 / 고속 12.2 km/ℓ
연비 (4WD): 복합 10.2 / 도심 9.1 / 고속 11.8 km/ℓ
CO2: 152 g/km (2WD) / 164 g/km (4WD)
공차중량: 1,590 kg (2WD) / 1,680 kg (4WD)
에너지등급: 4등급
저공해: 3종
```

### ④ 인포그래픽·카드 수치 스니펫
```
[2WD]  10.8km/ℓ | CO2 152g | 1,590kg | 4등급  ← 기본 구동
[4WD]  10.2km/ℓ | CO2 164g | 1,680kg | 4등급
※ 복합연비 기준 / 저공해 3종
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 휠사이즈 | vehicle_powertrains.wheel null — 원문 확인 필요 |
| 트림별 옵션 스펙 | 미수집 |
| 안전 등급 | 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-18_  
_data gate: verdict-actyon-20260611.md (GREEN) · commit 8877504_
