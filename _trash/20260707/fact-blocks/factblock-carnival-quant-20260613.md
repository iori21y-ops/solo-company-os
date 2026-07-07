---
type: fact-block
title: 기아 카니발 팩트블록 (quantitative · KA4)
topic: carnival-factblock-quant
subject: 기아 카니발 (KA4 2026년형)
date: 2026-06-13
data_source:
  - data/outputs/approved/verdict-carnival-20260611.md (quantitative/referential GREEN)
created: 2026-06-13
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-006-factblock-batch-20260613]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-carnival-20260611.md
  - DB: vehicle_powertrains WHERE slug='carnival' (쿼리 2026-06-13)
  - DB: vehicle_trims WHERE slug='carnival' (트림명·가격)
data_gate: verdict-carnival-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·CO2·배기량·공차중량·에너지등급·휠
uncertified: 가격·이미지·drive_type(DB null)
flags:
  - "vehicle_powertrains.drive_type = null (전 행) — 카니발 전 파워트레인 구동방식 DB 미기재. 가솔린 MPV 특성상 2WD(FWD) 추정이나 DB 미인증. 팩트블록에서 '미기재'로 표기."
  - "curb_weight_kg null 행 2건(18\" 빌트인 캠, 19\" 빌트인 캠) 존재 — 해당 행 공차중량 미포함 표기."
  - "vehicle_trims.base_price는 가격 verdict 미인증 범위 — 참고용으로만 기재, 발행 시 별도 가격 인증 필요."
---

# 카니발 팩트 블록 — quantitative (KA4 · 3.5 가솔린)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-carnival-20260611 GREEN).  
> 인증 범위: 연비·CO2·배기량·공차중량·에너지등급. 가격·이미지 미포함.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| drive_type | ⚠️ 미기재 | 전 행 DB null. FWD 추정이나 미인증. |
| 공차중량 일부 null | ℹ️ 확인 | 빌트인 캠 옵션 2행 curb_weight null. 해당 수치 팩트블록 미채택. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 기아 (KIA) | vehicles.brand |
| 모델명 | 카니발 (CARNIVAL) | vehicles.name |
| 모델코드 | KA4 | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 대형 | vehicles.segment |
| 카테고리 | 다목적 (MPV) | vehicles.category |
| 파워트레인 | 3.5 가솔린 (스마트스트림 V6 3,470 cc) | vehicle_powertrains.engine |
| 변속기 | 8단 자동변속기 | vehicle_powertrains.engine (raw_line) |
| 구동방식 | 미기재 (DB null) | — |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 3.5 가솔린 (3,470 cc · 8단 자동)

| 휠 | 옵션 | 탑승 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 | 에너지등급 |
|----|------|------|---------|------|------|-----|---------|-----------|
| 18" | 기본 | 9인승 | 9.0 km/L | 7.8 | 10.9 | 189 g/km | 2,080 kg | 5등급 |
| 18" | 빌트인 캠 | — | 8.9 km/L | 7.7 | 10.9 | 192 g/km | — (null) | 5등급 |
| 19" | 기본 (9인승) | 9인승 | 9.0 km/L | 7.8 | 10.9 | 189 g/km | 2,090 kg | 5등급 |
| 19" | 기본 (7인승) | 7인승 | 9.0 km/L | 7.8 | 10.9 | 189 g/km | 2,115 kg | 5등급 |
| 19" | 빌트인 캠 | — | 8.9 km/L | 7.7 | 10.9 | 192 g/km | — (null) | 5등급 |

> 공차중량 null 행: 빌트인 캠 장착 사양은 DB curb_weight_kg 미기재.  
> 인승별 공차중량: 7인승 > 9인승 경향 (19" 기준 7인승 2,115 kg / 9인승 2,090 kg).

---

## 트림 라인업 (vehicle_trims · 트림명·가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | 출고가 참고 |
|--------|-----------|
| 3.5 가솔린 9인승 프레스티지 | 36,360,000원 |
| 3.5 가솔린 9인승 노블레스 | 40,710,000원 |
| 3.5 가솔린 7인승 노블레스 아웃도어 | 42,320,000원 |
| 3.5 가솔린 7인승 노블레스 | 43,310,000원 |
| 3.5 가솔린 9인승 시그니처 | 44,260,000원 |
| 3.5 가솔린 9인승 시그니처 X-Line | 45,020,000원 |
| 3.5 가솔린 7인승 시그니처 | 47,080,000원 |
| 3.5 가솔린 7인승 시그니처 X-Line | 47,610,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
기아 카니발 KA4 2026년형 · 3.5가솔린 V6 · 8단 자동 · 7인승/9인승
```

### ② 블로그 소개 단락용 (2~3문장)
```
기아 카니발(CARNIVAL) KA4 2026년형은 스마트스트림 V6 3.5 가솔린(3,470 cc) 엔진에
8단 자동변속기를 탑재한 대형 다목적 차량(MPV)입니다.
19인치 9인승 기준 복합연비 9.0 km/L, 7인승 기준 공차중량 2,115 kg입니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 기아 (KIA)
모델: 카니발 (CARNIVAL) KA4
연식: 2026년형
세그먼트: 대형 / 다목적 (MPV)
파워트레인: 3.5 가솔린 (V6 3,470 cc)
변속기: 8단 자동변속기
구동방식: 미기재 (DB null)
연비(대표): 9.0 km/L (19" 기준 · 5등급)
CO2: 189 g/km (기본 사양)
탑승인원: 7인승 / 9인승 선택
트림: 프레스티지·노블레스·노블레스 아웃도어·시그니처·시그니처 X-Line
```

### ④ 인포그래픽·카드 수치 스니펫
```
[3.5가솔린 9인승 18"] 3,470cc | 9.0km/L | CO2 189g/km | 2,080kg | 5등급
[3.5가솔린 7인승 19"] 3,470cc | 9.0km/L | CO2 189g/km | 2,115kg | 5등급
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 구동방식 | DB null — 미인증 |
| 빌트인 캠 사양 공차중량 | DB curb_weight_kg null (2행) |
| 카니발 하이브리드 | carnival-hybrid 별도 slug·별도 verdict 존재 → 별도 팩트블록 처리 예정 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-13_  
_data gate: verdict-carnival-20260611.md (GREEN) · commit 8877504_
