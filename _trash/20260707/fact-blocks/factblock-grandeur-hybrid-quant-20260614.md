---
type: fact-block
title: 현대 그랜저 하이브리드 팩트블록 (quantitative · GN7)
topic: grandeur-hybrid-factblock-quant
subject: 현대 그랜저 하이브리드 (GN7 2026년형)
date: 2026-06-14
data_source:
  - data/outputs/approved/verdict-grandeur-hybrid-20260611.md (quantitative/referential GREEN)
created: 2026-06-14
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-007-factblock-batch-20260614]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-grandeur-hybrid-20260611.md
  - DB: vehicle_powertrains WHERE slug='grandeur-hybrid' (쿼리 2026-06-14)
  - DB: vehicle_trims WHERE slug='grandeur-hybrid' (트림명·가격)
data_gate: verdict-grandeur-hybrid-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·배기량·CO2·공차중량·구동방식·휠·에너지등급
uncertified: 가격·이미지·vehicles 메타(body_type 등)
flags:
  - "vehicles 테이블 body_type = 'SUV' → 명백 오류(그랜저 하이브리드는 준대형 하이브리드 세단). 팩트블록 미채택, 데이터팀 수정 필요."
  - "vehicle_trims 수치(연비·drive_type·wheel_size 등) null → 트림명만 기재. 가격은 인증 범위 외."
---

# 그랜저 하이브리드 팩트 블록 — quantitative (GN7)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-grandeur-hybrid-20260611 GREEN).  
> 인증 범위: 연비·배기량·CO2·공차중량·구동방식·휠·에너지등급. 가격·이미지 미포함.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| vehicles 메타 오류 | ⚠️ 요확인 | body_type = 'SUV' 기재 — 실제는 준대형 하이브리드 세단. 데이터팀 수정 권고. |
| vehicle_trims 수치 | ℹ️ null | 트림별 연비·구동·휠 수치 DB 미연동. 트림명 참조 전용. |
| 그랜저 (일반) 연관 | 📌 별도 | grandeur(비하이브리드) 팩트블록 별도 생산 완료 (factblock-grandeur-quant-20260612.md). |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (HYUNDAI) | vehicles.brand |
| 모델명 | 그랜저 하이브리드 (GRANDEUR HYBRID) | vehicles.name |
| 모델코드 | GN7 | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 준대형 | vehicles.segment |
| 연료 유형 | 하이브리드 (gasoline + motor) | vehicle_powertrains.fuel_kind |
| 엔진 | 스마트스트림 가솔린 1.6 터보 하이브리드 | vehicle_powertrains.engine |
| 배기량 | 1,598 cc | vehicle_powertrains.displacement_cc |
| 변속기 (공통) | 6단 자동변속기 | vehicle_powertrains.raw_line |
| 구동방식 | 2WD (전 트림 동일) | vehicle_powertrains.drive_type |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 스마트스트림 가솔린 1.6 터보 하이브리드 (1,598 cc · 6단 자동 · 2WD)

| 휠 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 | 에너지등급 |
|----|---------|------|------|-----|---------|-----------|
| 18" | **18.0 km/L** | 18.0 | 17.9 | 88 g/km | 1,700 kg | **1등급** |
| 19" | 16.7 km/L | 16.6 | 16.8 | 96 g/km | 1,715 kg | 1등급 |
| 20" | 15.7 km/L | 15.4 | 15.9 | 103 g/km | 1,735 kg | 2등급 |

> 구동방식 전 행 2WD. AWD 없음.  
> 18" → 19" → 20" 순으로 연비 감소 / CO2 증가 / 공차중량 증가.  
> 18" 기준 국산 준대형 최상위 연비 구간.

---

## 트림 라인업 (vehicle_trims · 트림명 참조)

> 수치(연비·가격 등) null — 트림별 수치 DB 미연동. 트림명만 인증 범위 외.  
> 가격은 uncertified — 참고값으로만 표기.

| 트림명 | 참고가(원, 미인증) |
|--------|----------|
| 프리미엄 | 45,230,000 |
| 익스클루시브 | 50,190,000 |
| 어너스 | 52,490,000 |
| 캘리그래피 | 54,490,000 |
| 블랙 잉크 | 54,490,000 |
| 블랙 익스테리어 | 55,780,000 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 그랜저 하이브리드 GN7 2026년형 · 1.6 터보 HEV · 2WD · 6단 자동 · 18" 기준 18.0 km/L(1등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 그랜저 하이브리드(GRANDEUR HYBRID) GN7 2026년형은 스마트스트림 가솔린 1.6 터보 하이브리드(1,598 cc)와
6단 자동변속기를 탑재한 준대형 하이브리드 세단입니다.
18인치 기준 복합연비 18.0 km/L(1등급)로, CO2 배출량 88 g/km · 공차중량 1,700 kg를 달성합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대(HYUNDAI)
모델: 그랜저 하이브리드(GRANDEUR HYBRID) GN7
연식: 2026년형
세그먼트: 준대형
파워트레인: 1.6 터보 가솔린 하이브리드
배기량: 1,598 cc
변속기: 6단 자동변속기
구동방식: 2WD
연비(대표): 18.0 km/L (18" 2WD · 1등급)
CO2(대표): 88 g/km (18" 2WD)
공차중량: 1,700 kg (18" 2WD)
트림: 프리미엄·익스클루시브·어너스·캘리그래피·블랙 잉크·블랙 익스테리어
```

### ④ 인포그래픽·카드 수치 스니펫
```
[HEV 18"] 1,598cc | 18.0 km/L | CO2 88g/km | 1,700kg | 1등급
[HEV 19"] 1,598cc | 16.7 km/L | CO2 96g/km | 1,715kg | 1등급
[HEV 20"] 1,598cc | 15.7 km/L | CO2 103g/km | 1,735kg | 2등급
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 그랜저 (일반) 가솔린·LPG 제원 | grandeur 별도 slug · 별도 팩트블록 기생산 |
| 트림별 제원 수치 | vehicle_trims 수치 null (DB 미연동) |
| 바디타입·카테고리 | vehicles 메타 오류(SUV 기재) → 데이터팀 수정 후 채택 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-14_  
_data gate: verdict-grandeur-hybrid-20260611.md (GREEN) · commit 8877504_
