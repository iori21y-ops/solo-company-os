---
type: fact-block
title: 현대 아반떼 하이브리드 팩트블록 (quantitative · CN7)
topic: avante-hybrid-factblock-quant
subject: 현대 아반떼 하이브리드 (CN7 2026년형)
date: 2026-06-15
data_source:
  - data/outputs/approved/verdict-avante-hybrid-20260611.md (quantitative/referential GREEN)
created: 2026-06-15
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-008-factblock-batch-20260615]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-avante-hybrid-20260611.md
  - DB: vehicle_powertrains WHERE slug='avante-hybrid' (쿼리 2026-06-15)
  - DB: vehicles WHERE slug='avante-hybrid' (메타)
data_gate: verdict-avante-hybrid-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·배기량·CO2·공차중량·휠·에너지등급·변속기
uncertified: 가격·이미지·vehicles 메타(body_type·drive_type 등)
flags:
  - "vehicles 테이블 body_type = 'SUV' → 명백 오류(아반떼 하이브리드는 준중형 세단). 팩트블록 미채택, 데이터팀 수정 필요."
  - "vehicle_powertrains drive_type 전 행 null → 구동방식 기재 불가. 원문 PDF 확인 후 데이터팀 보완 권고."
---

# 아반떼 하이브리드 팩트 블록 — quantitative (CN7)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-avante-hybrid-20260611 GREEN).  
> 인증 범위: 연비·배기량·CO2·공차중량·휠·에너지등급·변속기. 가격·이미지·구동방식 미포함.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| vehicles 메타 오류 | ⚠️ 요확인 | body_type = 'SUV' 기재 — 실제는 준중형 하이브리드 세단(CN7). 데이터팀 수정 권고. |
| drive_type | ⚠️ null | 전 행 null — 구동방식(FWD 추정) DB 미기재. 콘텐츠 출력 시 생략 처리. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (HYUNDAI) | vehicles.brand |
| 모델명 | 아반떼 하이브리드 (AVANTE HYBRID) | vehicles.name |
| 모델코드 | CN7 | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 카테고리 | 세단 (준중형) | vehicles.category 참조 / body_type 오류 제외 |
| 연료 유형 | 하이브리드 (가솔린+모터) | vehicle_powertrains.fuel_kind = hybrid |
| 엔진 | 가솔린 1.6 하이브리드엔진 | vehicle_powertrains.engine |
| 배기량 | 1,580 cc | vehicles.displacement_cc |
| 변속기 | 6단 DCT | vehicles.transmission |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 가솔린 1.6 하이브리드 (1,580 cc · 6단 DCT)

| 휠 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 | 에너지등급 |
|----|---------|------|------|-----|---------|-----------|
| 16" | **21.1 km/L** | 21.4 | 20.7 | 74 g/km | 1,335 kg | **1등급** |
| 17" | 19.5 km/L | 20.3 | 18.6 | 81 g/km | 1,350 kg | **1등급** |

> 전 트림 에너지등급 1등급.  
> 16" → 17" 전환 시 복합연비 1.6 km/L 감소, CO2 7 g/km 증가, 공차중량 15 kg 증가.  
> drive_type DB 미기재 (null) — 일반적으로 FWD(전륜구동) 세단이나 원문 재확인 권고.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 아반떼 하이브리드 CN7 2026년형 · 1.6 HEV · 6단 DCT · 16" 기준 21.1 km/L(1등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 아반떼 하이브리드(AVANTE HYBRID) CN7 2026년형은 가솔린 1.6 하이브리드엔진(1,580 cc)과
6단 DCT를 탑재한 준중형 세단입니다.
16인치 기준 복합연비 21.1 km/L(1등급)로, CO2 배출량 74 g/km · 공차중량 1,335 kg를 달성합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대(HYUNDAI)
모델: 아반떼 하이브리드(AVANTE HYBRID) CN7
연식: 2026년형
파워트레인: 1.6 가솔린 하이브리드
배기량: 1,580 cc
변속기: 6단 DCT
연비(대표): 21.1 km/L (16" · 1등급)
연비(17"): 19.5 km/L (1등급)
CO2(대표): 74 g/km (16")
공차중량: 1,335 kg (16") / 1,350 kg (17")
```

### ④ 인포그래픽·카드 수치 스니펫
```
[HEV 16"] 1,580cc | 21.1 km/L | CO2 74g/km | 1,335kg | 1등급
[HEV 17"] 1,580cc | 19.5 km/L | CO2 81g/km | 1,350kg | 1등급
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 구동방식 | vehicle_powertrains.drive_type 전 행 null |
| 바디타입 | vehicles 메타 오류(SUV 기재) → 데이터팀 수정 후 채택 |
| 트림별 정보 | vehicle_trims 미조회 (제원 위주 팩트블록 범위) |

---

_작성: 컨텐츠_  
_작성일: 2026-06-15_  
_data gate: verdict-avante-hybrid-20260611.md (GREEN) · commit 8877504_
