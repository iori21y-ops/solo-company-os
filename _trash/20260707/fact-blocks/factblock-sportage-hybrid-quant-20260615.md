---
type: fact-block
title: 기아 스포티지 하이브리드 팩트블록 (quantitative · NQ5)
topic: sportage-hybrid-factblock-quant
subject: 기아 스포티지 하이브리드 (NQ5)
date: 2026-06-15
data_source:
  - data/outputs/approved/verdict-sportage-hybrid-20260611.md (quantitative/referential GREEN)
created: 2026-06-15
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-008-factblock-batch-20260615]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-sportage-hybrid-20260611.md
  - DB: vehicle_powertrains WHERE slug='sportage-hybrid' (쿼리 2026-06-15)
  - DB: vehicles WHERE slug='sportage-hybrid' (메타)
data_gate: verdict-sportage-hybrid-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·배기량·CO2·공차중량·구동방식·휠·에너지등급
uncertified: 가격·이미지·vehicles 메타(body_type null 등)
flags:
  - "vehicles 테이블 body_type null — 실제 SUV(중형). 데이터팀 보완 권고."
  - "연식 혼재: 1등급 행(16.3 km/L)과 2등급 행(15.8 km/L)이 동일 slug 내 공존 — 신형/구형 연식 차이로 추정(raw_line 구조 차이). 연식 구분 없이 DB 통합 기재됨. 콘텐츠 출력 시 등급 기준 행을 명시할 것."
---

# 스포티지 하이브리드 팩트 블록 — quantitative (NQ5)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-sportage-hybrid-20260611 GREEN).  
> 인증 범위: 연비·배기량·CO2·공차중량·구동방식·휠·에너지등급. 가격·이미지 미포함.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| 연식 혼재 | ⚠️ 요확인 | 1등급(16.3 km/L)과 2등급(15.8 km/L) 행 동일 slug 내 공존. 신형/구형 연식 혼합 추정. 콘텐츠 사용 시 등급·연식 명시 필수. |
| vehicles body_type | ℹ️ null | SUV 추정(vehicles.category='SUV'). 메타 보완 권고. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 기아 (KIA) | vehicles.brand |
| 모델명 | 스포티지 하이브리드 (SPORTAGE HYBRID) | vehicles.name |
| 모델코드 | NQ5 | vehicles.model_code |
| 카테고리 | SUV (중형) | vehicles.category |
| 연료 유형 | 하이브리드 (가솔린+모터) | vehicle_powertrains.fuel_kind = hybrid |
| 엔진 | 1.6 터보 하이브리드 | vehicle_powertrains.engine |
| 배기량 | 1,598 cc | vehicle_powertrains.displacement_cc |
| 변속기 | 6단 자동 | vehicle_powertrains.engine 파생 |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 1.6 터보 하이브리드 · 자동 6단 · 1,598 cc

#### A. 2WD

| 휠 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 | 에너지등급 | 비고 |
|----|---------|------|------|-----|---------|-----------|------|
| 17" | **16.3 km/L** | 16.9 | 15.5 | 98 g/km | 1,650 kg | **1등급** | 신형 |
| 18" | 16.3 km/L | 16.9 | 15.5 | 98 g/km | 1,660 kg | **1등급** | 신형 |
| 17" (빌트인 캠) | 15.8 km/L | 16.2 | 15.3 | 101 g/km | 1,650 kg | 2등급 | 구형 추정 |
| 18" (빌트인 캠) | 15.8 km/L | 16.2 | 15.3 | 101 g/km | 1,660 kg | 2등급 | 구형 추정 |
| 19" (빌트인 캠) | 15.6 km/L | 16.2 | 14.8 | 102 g/km | 1,685 kg | 2등급 | 구형 추정 |

> 신형 2WD(1등급) 17"·18" 복합연비 동일(16.3 km/L).  
> 19"는 2등급(구형 추정) 데이터만 있음.

#### B. 4WD

| 휠 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 | 에너지등급 |
|----|---------|------|------|-----|---------|-----------|
| 17" (빌트인 캠) | **14.7 km/L** | 15.0 | 14.2 | 110 g/km | 1,710 kg | **2등급** |
| 18" (빌트인 캠) | 14.7 km/L | 15.0 | 14.2 | 110 g/km | 1,720 kg | 2등급 |
| 19" (빌트인 캠) | 14.3 km/L | 14.4 | 14.1 | 113 g/km | 1,745 kg | 2등급 |

> 4WD 전 행 에너지등급 2등급.  
> 2WD → 4WD 전환 시 복합연비 약 1.5~1.6 km/L 감소, 공차중량 약 60 kg 증가.  
> 19" 4WD 최중량 1,745 kg.

---

## 2WD vs 4WD 요약 비교

| 구분 | 최고 연비 | 대표 CO2 | 공차중량 범위 | 에너지등급 |
|------|---------|---------|------------|-----------|
| 2WD (신형·17") | 16.3 km/L | 98 g/km | 1,650~1,685 kg | 1등급~2등급 |
| 4WD (17") | 14.7 km/L | 110 g/km | 1,710~1,745 kg | 2등급 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
기아 스포티지 하이브리드 NQ5 · 1.6T HEV · 2WD 17" 기준 16.3 km/L(1등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
기아 스포티지 하이브리드(SPORTAGE HYBRID) NQ5는 1.6 터보 하이브리드(1,598 cc)와
6단 자동변속기를 탑재한 중형 SUV입니다.
2WD 17인치 기준 복합연비 16.3 km/L(1등급)로, CO2 배출량 98 g/km · 공차중량 1,650 kg를 달성하며,
4WD 선택 시 복합연비 14.7 km/L(2등급)가 적용됩니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 기아(KIA)
모델: 스포티지 하이브리드(SPORTAGE HYBRID) NQ5
파워트레인: 1.6 터보 가솔린 하이브리드
배기량: 1,598 cc
변속기: 6단 자동
구동: 2WD / 4WD 선택
연비(대표·2WD 17"): 16.3 km/L (1등급)
연비(4WD 17"): 14.7 km/L (2등급)
CO2(2WD 17"): 98 g/km
공차중량: 1,650 kg (2WD 17") / 1,710 kg (4WD 17")
```

### ④ 인포그래픽·카드 수치 스니펫
```
[HEV 2WD 17"·신형] 1,598cc | 16.3 km/L | CO2 98g/km | 1,650kg | 1등급
[HEV 2WD 18"·신형] 1,598cc | 16.3 km/L | CO2 98g/km | 1,660kg | 1등급
[HEV 4WD 17"] 1,598cc | 14.7 km/L | CO2 110g/km | 1,710kg | 2등급
[HEV 4WD 19"] 1,598cc | 14.3 km/L | CO2 113g/km | 1,745kg | 2등급
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 연식 구분 | DB 연식 미분리 — 1등급/2등급 행 연식 데이터팀 확인 권고 |
| 바디타입 | vehicles 메타 null → 데이터팀 보완 후 채택 |
| 트림별 정보 | vehicle_trims 미조회 |
| 스포티지(가솔린·디젤) | sportage 별도 slug |

---

_작성: 컨텐츠_  
_작성일: 2026-06-15_  
_data gate: verdict-sportage-hybrid-20260611.md (GREEN) · commit 8877504_
