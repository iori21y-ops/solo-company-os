---
type: fact-block
title: 기아 K5 팩트블록 (quantitative · 2026년형)
topic: k5-factblock-quant
subject: 기아 K5 (2026년형)
date: 2026-06-15
data_source:
  - data/outputs/approved/verdict-k5-20260611.md (quantitative/referential GREEN)
created: 2026-06-15
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-008-factblock-batch-20260615]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-k5-20260611.md
  - DB: vehicle_powertrains WHERE slug='k5' (쿼리 2026-06-15)
  - DB: vehicles WHERE slug='k5' (메타)
data_gate: verdict-k5-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·CO2·공차중량·휠·에너지등급
uncertified: 가격·이미지·배기량(1.6T null)·구동방식·변속기 메타
flags:
  - "vehicle_powertrains 혼재: '2.0 가솔린 자동 6단' engine 레이블 아래 연비 18~20 km/L 행 4개 존재 — 가솔린 2.0 수준(12.X km/L)과 현저히 다름. 해당 행은 PDF K5 HEV(2.0 HEV) 섹션에서 파싱된 것으로 추정. fuel_kind='gasoline'으로 기재돼 있으나 실제는 HEV 파워트레인. 데이터팀 engine/fuel_kind 재분류 권고."
  - "vehicles 테이블 displacement_cc null, body_type null, model_code='' — 기본 메타 미완. 데이터팀 보완 권고."
  - "vehicle_powertrains 전 행 displacement_cc null, drive_type null — 제원표 누락."
---

# K5 팩트 블록 — quantitative (2026년형)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-k5-20260611 GREEN).  
> 인증 범위: 연비·CO2·공차중량·휠·에너지등급. 가격·구동방식·배기량 미포함.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| HEV 행 engine 레이블 오류 | ⚠️ 요확인 | '2.0 가솔린 자동 6단' engine 아래 18~20 km/L 행 4개 — PDF K5 HEV 섹션 파싱 행 추정. fuel_kind='gasoline' 잘못 기재. 콘텐츠 출력 시 2.0 HEV로 별도 표기. |
| 배기량 | ⚠️ null | vehicle_powertrains 전 행 displacement_cc null. 1.6T는 약 1,591cc, 2.0은 1,999cc(추정). 원문 확인 필요. |
| body_type / drive_type | ℹ️ null | 세단 추정(vehicles.category='세단'), 전 행 drive_type null. |
| vehicles 메타 | ℹ️ 미완 | model_code 공백, body_type null. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 기아 (KIA) | vehicles.brand |
| 모델명 | K5 | vehicles.name |
| 연식 | 2026년형 | vehicles.year |
| 카테고리 | 세단 (중형) | vehicles.category |
| 파워트레인 구성 | 1.6 가솔린 터보 + 2.0 가솔린 + 2.0 HEV(추정) + 2.0 LPG | vehicle_powertrains 통합 |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### ① 1.6 가솔린 터보 · 자동 8단 (fuel_kind=gasoline)

| 휠 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 | 에너지등급 |
|----|---------|------|------|-----|---------|-----------|
| 17" | **13.7 km/L** | 12.1 | 16.1 | 121 g/km | 1,450 kg | **3등급** |
| 17" (빌트인 캠) | 13.5 km/L | 11.9 | 16.0 | 123 g/km | — | 3등급 |
| 18" (빌트인 캠) | 13.0 km/L | 11.5 | 15.4 | 128 g/km | 1,485 kg | 3등급 |
| 19" (빌트인 캠) | 12.3 km/L | 10.8 | 14.9 | 135 g/km | 1,480 kg | 3등급 |

> 배기량 DB null. 1.6T 추정 약 1,591 cc.  
> 빌트인 캠 옵션 적용 시 연비 소폭 감소(동일 휠 기준 ~0.2 km/L).

---

### ② 2.0 가솔린 · 자동 6단 (fuel_kind=gasoline)

| 휠 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 | 에너지등급 |
|----|---------|------|------|-----|---------|-----------|
| 16" | **12.6 km/L** | 11.2 | 14.7 | 132 g/km | 1,425 kg | **3등급** |
| 17" | 12.6 km/L | 11.2 | 14.7 | 132 g/km | 1,435 kg | 3등급 |
| 17" (빌트인 캠) | 12.3 km/L | 10.9 | 14.5 | 135 g/km | — | 3등급 |
| 18" (빌트인 캠) | 12.2 km/L | 10.9 | 14.1 | 137 g/km | 1,455 kg | 3등급 |

> 배기량 DB null. 2.0 NA 추정 약 1,999 cc.

---

### ③ 2.0 HEV (추정) · 자동 6단 — DB engine 레이블 '2.0 가솔린 자동 6단' ⚠️

> **주의**: DB fuel_kind='gasoline', engine='2.0 가솔린 자동 6단'으로 기재되어 있으나  
> 연비 범위(18~20 km/L)·CO2(79~87 g/km)가 순수 가솔린 2.0과 상이 → K5 HEV 파워트레인으로 추정.  
> 콘텐츠 출력 시 반드시 "K5 HEV 추정" 명시 또는 데이터팀 재분류 확인 후 사용.

| 휠 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 | 에너지등급 |
|----|---------|------|------|-----|---------|-----------|
| 16" | **19.8 km/L** | 19.7 | 19.8 | 79 g/km | 1,515 kg | **3등급** |
| 16" (빌트인 캠) | 19.2 km/L | 18.7 | 19.7 | 82 g/km | — | 3등급 |
| 17" | 18.8 km/L | 18.7 | 18.9 | 84 g/km | 1,535 kg | 3등급 |
| 17" (빌트인 캠) | 18.2 km/L | 17.7 | 18.7 | 87 g/km | — | 3등급 |

> vehicles.engine 기재: '1.6T(12.8km/L), 2.0HEV(18.0km/L)' — 2.0HEV 확인 근거.  
> 에너지등급 3등급 기재는 DB 원문 그대로 보존. 이상치 여부 데이터팀 확인 권고.

---

### ④ 2.0 LPG · 자동 6단 (fuel_kind=lpg)

| 휠 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 | 에너지등급 |
|----|---------|------|------|-----|---------|-----------|
| 16" (빌트인 캠) | 9.7 km/ℓ | 8.5 | 11.7 | 134 g/km | 1,445 kg | 4등급 |
| 17" (빌트인 캠) | **9.8 km/ℓ** | 8.5 | 11.8 | 133 g/km | 1,465 kg | 4등급 |
| 18" (빌트인 캠) | 9.5 km/ℓ | 8.2 | 11.5 | 138 g/km | 1,500 kg | 4등급 |

> LPG 연비는 LPG ℓ 기준. 가솔린 환산 시 약 1.3배 보정 필요.

---

## 재사용 문구 소스

### ① SNS 캡션용 (파워트레인별)
```
[1.6T] 기아 K5 2026년형 · 1.6 가솔린 터보 · 8단 자동 · 17" 기준 13.7 km/L(3등급)
[2.0] 기아 K5 2026년형 · 2.0 가솔린 · 6단 자동 · 16" 기준 12.6 km/L(3등급)
[HEV] 기아 K5 2026년형 · 2.0 HEV(추정) · 6단 자동 · 16" 기준 19.8 km/L(3등급) ※DB 재분류 확인 필요
[LPG] 기아 K5 2026년형 · 2.0 LPG · 6단 자동 · 17" 기준 9.8 km/ℓ(4등급)
```

### ② 상담 자료용 (항목형 · 1.6T 대표)
```
브랜드: 기아(KIA)
모델: K5
연식: 2026년형
파워트레인(대표): 1.6 가솔린 터보
변속기: 8단 자동
연비(대표): 13.7 km/L (17" · 3등급)
CO2(대표): 121 g/km (17")
공차중량: 1,450 kg (17")
```

### ③ 인포그래픽·카드 수치 스니펫
```
[1.6T 17"] 복합 13.7 | CO2 121g | 1,450kg | 3등급
[2.0 16"] 복합 12.6 | CO2 132g | 1,425kg | 3등급
[HEV 16"·추정] 복합 19.8 | CO2 79g | 1,515kg | 3등급
[LPG 17"] 복합 9.8 | CO2 133g | 1,465kg | 4등급
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 배기량 | vehicle_powertrains 전 행 null |
| 구동방식 | 전 행 null |
| 2.0 HEV 확정 수치 | DB fuel_kind/engine 재분류 필요 — 데이터팀 확인 후 사용 |
| 트림별 정보 | vehicle_trims 미조회 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-15_  
_data gate: verdict-k5-20260611.md (GREEN) · commit 8877504_
