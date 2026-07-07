---
type: fact-block
title: 르노코리아 필란테 팩트블록 (quantitative · 2026년형 · HEV)
topic: filante-factblock-quant
subject: 르노코리아 필란테 하이브리드 E-Tech (2026년형 · 1.5 E-Tech · 19"/20")
date: 2026-06-21
data_source:
  - data/outputs/approved/verdict-filante-20260611.md (quantitative/referential GREEN)
created: 2026-06-21
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-014-factblock-batch-20260621]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-filante-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='filante' (쿼리 2026-06-21, 1행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='filante' (쿼리 2026-06-21, 4행)
data_gate: verdict-filante-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠
uncertified: 가격·이미지·구동방식(drive_type)·안전등급·19"/20" 휠별 수치 분리
flags:
  - "vehicles.segment null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.category null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.body_type null — DB 미입력. 데이터팀 보완 권고."
  - "vehicle_powertrains.drive_type null — 르노 필란테 HEV는 FWD 전용으로 알려짐. 원문 확인 권고."
  - "engine 필드 '(19\"/20\")' 명시 — 19인치·20인치 수치가 단일 행으로 통합 기재. 휠별 수치 미분리. 데이터팀 확인 권고."
  - "vehicle_trims.base_price 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# 필란테 팩트 블록 — quantitative (2026년형 · 1.5 E-Tech HEV)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-filante-20260611 GREEN).  
> 인증 범위: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠.  
> 구동방식(drive_type) null — 르노 필란테 HEV는 FWD 전용으로 알려지나 DB 미기재, 발행 전 원문 확인 권고.  
> 19"/20" 단일 행 수집 — DB engine 필드에 "(19\"/20\")" 통합 기재. 휠 크기별 수치 분리 미확인.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| segment / category | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| model_code | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| body_type | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| drive_type | ⚠️ null | FWD 전용 추정. 원문 확인 필요. |
| 19"/20" 수치 분리 | ⚠️ 미분리 | engine 필드에 "(19\"/20\")" 통합 기재 — 휠 크기별 별도 수치 없음. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 르노코리아 | vehicles.brand |
| 모델명 | 필란테 하이브리드 E-Tech | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | — (null) | vehicles.segment |
| 카테고리 | — (null) | vehicles.category |
| 연료 | 하이브리드 (E-Tech) | vehicle_powertrains.fuel_kind |
| 배기량 | 1,499cc (1.5) | vehicle_powertrains.displacement_cc |
| 변속기 | 멀티모드 오토 | vehicle_powertrains.engine |
| 구동방식 | — (null, FWD 추정) | vehicle_powertrains.drive_type |
| 휠 | 19" / 20" (단일 행 수집) | vehicle_powertrains.wheel + engine |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

| 행 | 휠 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|
| A | **19" / 20"** | **15.1 km/ℓ** | 14.7 | 15.5 | **106 g/km** | **1,820 kg** | **2등급** |

> **핵심 포인트:**
> - 복합연비 15.1 km/ℓ — 고속(15.5) > 도심(14.7). E-Tech 하이브리드임에도 고속 우위 특이.
> - CO2 106 g/km — 준중형 세단급 HEV 기준 낮은 배출량
> - 에너지 2등급 인증 (국내 공인 기준)
> - 19인치·20인치 휠 크기별 수치 분리 미수집 — 단일 통합값. 휠별 차이 발행 시 원문 확인 필수.

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | 출고가 참고 |
|--------|-----------|
| 테크노 | 45,000,000원 |
| 아이코닉 | 48,700,000원 |
| SE | 51,500,000원 |
| 에스프리 알핀 | 54,000,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
르노 필란테 2026 · E-Tech HEV · 복합 15.1km/ℓ (2등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
르노코리아 필란테 하이브리드 E-Tech 2026년형은 1.5 E-Tech 하이브리드 시스템을 탑재한 세단입니다.
복합연비 15.1 km/ℓ(도심 14.7 / 고속 15.5), CO2 106 g/km으로
에너지소비효율 2등급을 획득했으며, 공차중량은 1,820 kg입니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 르노코리아
모델: 필란테 하이브리드 E-Tech 2026년형
연료: 하이브리드 (E-Tech)
배기량: 1,499cc (1.5)
변속기: 멀티모드 오토
구동방식: FWD 추정 (DB null)
연비 (복합): 15.1 km/ℓ
연비 (도심): 14.7 km/ℓ
연비 (고속): 15.5 km/ℓ
CO2: 106 g/km
공차중량: 1,820 kg
에너지등급: 2등급
휠: 19" / 20" (수치 동일 공인)
```

### ④ 인포그래픽·카드 수치 스니펫
```
[HEV 19"/20"(공통)]  15.1km/ℓ | CO2 106g | 1,820kg | 2등급
※ 복합연비 기준 / 고속>도심 특성 / 휠 크기별 수치 분리 미수집
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 구동방식 | vehicle_powertrains.drive_type null — 원문 확인 필요 |
| 휠 크기별 연비 분리 | DB 단일 행 수집 — 19"·20" 통합 처리 |
| 트림별 옵션 스펙 | 미수집 |
| 안전 등급 | 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-21_  
_data gate: verdict-filante-20260611.md (GREEN) · commit 8877504_
