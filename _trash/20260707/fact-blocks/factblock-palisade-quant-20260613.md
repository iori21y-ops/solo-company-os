---
type: fact-block
title: 현대 팰리세이드 팩트블록 (quantitative · LX2)
topic: palisade-factblock-quant
subject: 현대 팰리세이드 (LX2 2026년형)
date: 2026-06-13
data_source:
  - data/outputs/approved/verdict-palisade-20260611.md (quantitative/referential GREEN)
created: 2026-06-13
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-006-factblock-batch-20260613]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-palisade-20260611.md
  - DB: vehicle_powertrains WHERE slug='palisade' (쿼리 2026-06-13)
  - DB: vehicle_trims WHERE slug='palisade' (트림명·가격)
data_gate: verdict-palisade-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·CO2·배기량·공차중량·에너지등급·구동방식·휠
uncertified: 가격·이미지
flags:
  - "vehicle_powertrains에 가솔린·하이브리드 행이 모두 slug='palisade'에 귀속. palisade-hev는 별도 slug·별도 verdict 존재(vehicles 테이블에 팰리세이드 하이브리드 별도 항목). 본 팩트블록은 palisade verdict GREEN 범위 내에서 가솔린·하이브리드 행 모두 포함."
  - "7인승/9인승 공차중량이 동일 raw_line에 병기(예: 1,985kg_7인승 / 2,020kg_9인승). 단일 DB 행이 두 값 대표. 팩트블록에 병기 표기."
  - "vehicles.body_type='SUV' — 팰리세이드는 대형 SUV이므로 올바름(그랜저 오류와 다름). 정상."
  - "vehicle_trims.base_price는 가격 verdict 미인증 범위 — 참고용으로만 기재, 발행 시 별도 가격 인증 필요."
---

# 팰리세이드 팩트 블록 — quantitative (LX2 · 가솔린·하이브리드)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-palisade-20260611 GREEN).  
> 인증 범위: 연비·CO2·배기량·공차중량·에너지등급·구동방식. 가격·이미지 미포함.  
> ※ 하이브리드 행도 slug='palisade' 귀속으로 본 블록에 포함. palisade-hev는 별도 처리 예정.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| 하이브리드 행 포함 | 📌 참고 | palisade slug에 가솔린·하이브리드 혼재. palisade-hev 별도 처리 예정. |
| 인승별 공차중량 | ℹ️ 병기 | 7인승·9인승 동일 raw_line 내 병기. 실제 차이 최대 35kg. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (HYUNDAI) | vehicles.brand |
| 모델명 | 팰리세이드 (PALISADE) | vehicles.name |
| 모델코드 | LX2 | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 대형 | vehicles.segment |
| 바디타입 | SUV | vehicles.body_type |
| 파워트레인 | 2.5 가솔린 / 2.5 하이브리드 | vehicle_powertrains.fuel_kind |
| 구동방식 | 2WD / AWD | vehicle_powertrains.drive_type (GREEN) |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### ■ 가솔린 2.5 (스마트스트림 2,497 cc · 8단 자동)

| 휠 | 옵션 | 구동 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 (7/9인승) | 에너지등급 |
|----|------|------|---------|------|------|-----|------------------|-----------|
| 18" | 기본 | 2WD | 9.7 km/L | 8.5 | 11.6 | 174 g/km | 1,985 / 2,020 kg | 4등급 |
| 18" | 빌트인 캠 | 2WD | 9.4 km/L | 8.2 | 11.4 | 180 g/km | 1,985 / 2,020 kg | 4등급 |
| 18" | 기본 | AWD (7인승) | 8.7 km/L | 7.7 | 10.4 | 193 g/km | 2,055 kg | 5등급 |
| 18" | 기본 | AWD (9인승) | 8.6 km/L | 7.6 | 10.3 | 197 g/km | 2,090 kg | 5등급 |
| 20" | 기본 | 2WD | 9.0 km/L | 7.9 | 10.8 | 188 g/km | 2,015 / 2,050 kg | 5등급 |
| 20" | 기본 | AWD | 8.2 km/L | 7.2 | 9.8 | 207 g/km | 2,085 / 2,120 kg | 5등급 |
| 21" | 기본 | 2WD | 8.7 km/L | 7.6 | 10.6 | 195 g/km | 2,070 / 2,095 kg | 5등급 |
| 21" | 기본 | AWD | 8.2 km/L | 7.2 | 9.8 | 207 g/km | 2,140 / 2,165 kg | 5등급 |

### ■ 하이브리드 2.5 (2,497 cc · 6단 자동)

| 휠 | 옵션 | 구동 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 (7/9인승) | 에너지등급 |
|----|------|------|---------|------|------|-----|------------------|-----------|
| 18" | 기본 | 2WD | 14.1 km/L | 14.5 | 13.6 | 114 g/km | 2,080 / 2,115 kg | 2등급 |
| 18" | 빌트인 캠 | 2WD | 13.9 km/L | 14.0 | 13.7 | 116 g/km | 2,080 / 2,115 kg | 2등급 |
| 18" | 기본 | AWD | 12.5 km/L | 12.5 | 12.5 | 131 g/km | 2,150 / 2,185 kg | 3등급 |
| 20" | 기본 | 2WD | 12.7 km/L | 12.9 | 12.4 | 129 g/km | 2,110 / 2,145 kg | 3등급 |
| 20" | 기본 | AWD | 11.4 km/L | 11.4 | 11.3 | 145 g/km | 2,180 / 2,215 kg | 4등급 |
| 21" | 기본 | 2WD | 12.5 km/L | 12.5 | 12.5 | 131 g/km | 2,165 / 2,190 kg | 3등급 |
| 21" | 기본 | AWD | 11.4 km/L | 11.4 | 11.3 | 145 g/km | 2,235 / 2,260 kg | 4등급 |

---

## 트림 라인업 (vehicle_trims · 트림명·가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.  
> vehicle_trims.fuel_type = null (트림별 연료 구분 미기재).

| 트림명 | 출고가 참고 |
|--------|-----------|
| 익스클루시브 | 43,830,000원 |
| 프레스티지 | 49,360,000원 |
| 캘리그래피 | 55,860,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 팰리세이드 LX2 2026년형 · 2.5가솔린·하이브리드 · 2WD/AWD · 7/9인승
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 팰리세이드(PALISADE) LX2 2026년형은 스마트스트림 2.5 가솔린과
2.5 하이브리드 두 가지 파워트레인 옵션을 갖춘 대형 SUV입니다.
하이브리드 2WD 18" 기준 복합연비 14.1 km/L(2등급)로,
가솔린 대비 약 1.5배 향상된 연비를 제공합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대 (HYUNDAI)
모델: 팰리세이드 (PALISADE) LX2
연식: 2026년형
세그먼트: 대형 SUV
파워트레인: 가솔린 2.5 (2,497cc) / 하이브리드 2.5 (2,497cc)
변속기: 8단 자동(가솔린) / 6단 자동(하이브리드)
구동방식: 2WD / AWD
연비(대표): 9.7 km/L (가솔린 2WD 18"·4등급) / 14.1 km/L (하이브리드 2WD 18"·2등급)
탑승인원: 7인승 / 9인승
트림: 익스클루시브·프레스티지·캘리그래피
```

### ④ 인포그래픽·카드 수치 스니펫
```
[가솔린 2WD 18"] 2,497cc | 9.7km/L | CO2 174g/km | 1,985kg(7인승) | 4등급
[하이브리드 2WD 18"] 2,497cc | 14.1km/L | CO2 114g/km | 2,080kg(7인승) | 2등급
[하이브리드 vs 가솔린] 연비차 +4.4km/L / CO2차 -60g/km (동일 2WD 18" 기준)
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 트림별 연료 구분 | vehicle_trims.fuel_type = null (DB 미기재) |
| palisade-hev 전용 데이터 | 별도 slug·별도 verdict — 별도 팩트블록 처리 예정 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-13_  
_data gate: verdict-palisade-20260611.md (GREEN) · commit 8877504_
