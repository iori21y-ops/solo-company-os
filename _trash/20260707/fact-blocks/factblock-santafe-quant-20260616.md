---
type: fact-block
title: 현대 싼타페 팩트블록 (quantitative · MX5 2026년형)
topic: santafe-factblock-quant
subject: 현대 싼타페 (MX5 2026년형 · 가솔린 2.5터보)
date: 2026-06-16
data_source:
  - data/outputs/approved/verdict-santafe-20260611.md (quantitative/referential GREEN)
created: 2026-06-16
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-009-factblock-batch-20260616]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-santafe-20260611.md
  - DB: vehicle_powertrains WHERE slug='santafe' (쿼리 2026-06-16, 12행)
  - DB: vehicle_trims WHERE slug='santafe' (쿼리 2026-06-16, 6행)
data_gate: verdict-santafe-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·배기량·CO2·공차중량·구동방식·휠·에너지등급·변속기
uncertified: 가격·이미지
flags:
  - "전 행 에너지등급 4등급 — 2.5T AWD SUV 특성상 연비 효율 낮음. 콘텐츠 사용 시 등급 표기 주의."
  - "인승(5/6/7인승) 선택에 따라 공차중량 최대 60 kg 차이 — raw_line에 인승별 중량 명시. DB curb_weight_kg는 대표값(최중량)."
  - "빌트인 캠 적용 시 연비 약 0.2~0.4 km/L 감소."
  - "vehicle_trims.base_price는 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
  - "santafe-hybrid(MX5 하이브리드)는 별도 slug — 이 팩트블록에 미포함."
---

# 싼타페 팩트 블록 — quantitative (MX5 · 가솔린 2.5터보)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-santafe-20260611 GREEN).  
> 인증 범위: 연비·배기량·CO2·공차중량·구동방식·휠·에너지등급·변속기. 가격·이미지 미포함.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| 에너지등급 | ℹ️ 전 행 4등급 | 2.5T AWD SUV. 연비 효율 낮은 편 — 콘텐츠 표기 시 주의. |
| 인승별 공차중량 차이 | ℹ️ 확인 | 5/6/7인승 선택에 따라 최대 60 kg 차이. raw_line에 인승별 중량 기재. |
| 빌트인 캠 영향 | ℹ️ | 빌트인 캠 적용 시 연비 0.2~0.4 km/L 하락. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |
| 싼타페 하이브리드 | ℹ️ 별도 | santafe-hybrid slug — 이 블록 미포함. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (HYUNDAI) | vehicles.brand |
| 모델명 | 싼타페 (SANTA FE) | vehicles.name |
| 모델코드 | MX5 | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 중형 | vehicles.segment |
| 바디타입 | SUV | vehicles.body_type |
| 연료 | 가솔린 | vehicle_powertrains.fuel_kind |
| 엔진 | 스마트스트림 가솔린 2.5터보 | vehicle_powertrains.engine |
| 배기량 | 2,497 cc | vehicle_powertrains.displacement_cc |
| 변속기 | 8단 DCT | raw_line |
| 구동방식 | 2WD / AWD | vehicle_powertrains.drive_type (GREEN) |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> 공차중량: DB 저장값(대표 인승 기준). raw_line에 5/6/7인승별 중량 명시됨.

### A. 2WD — 스마트스트림 가솔린 2.5터보 · 8단 DCT

| 휠 | 인승 | 옵션 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 (대표) | 에너지등급 |
|----|------|------|---------|------|------|-----|----------------|-----------|
| 18" | 5/6인승 | 기본 | **11.0 km/L** | 9.6 | 13.4 | 152 g/km | 1,835 kg | **4등급** |
| 18" | 5/6인승 | 빌트인 캠 | 10.8 km/L | 9.4 | 13.2 | 156 g/km | 1,835 kg | 4등급 |
| 18" | 7인승 | 기본 | 10.6 km/L | 9.3 | 12.9 | 158 g/km | 1,850 kg | 4등급 |
| 18" | 7인승 | 빌트인 캠 | 10.4 km/L | 9.1 | 12.8 | 162 g/km | 1,850 kg | 4등급 |
| 20" | 5인승 | 기본 | 10.4 km/L | 9.2 | 12.5 | 162 g/km | 1,835 kg | 4등급 |
| 20" | 6/7인승 | 기본 | 10.0 km/L | 8.8 | 12.0 | 168 g/km | 1,890 kg | 4등급 |
| 21" | 5/6/7인승 | 기본 | 10.0 km/L | 8.8 | 12.0 | 168 g/km | 1,920 kg | 4등급 |

> **raw_line 기준 인승별 공차중량 예시 (2WD 18" 기본):**  
> 5인승 1,795 kg / 6인승 1,835 kg / 7인승 1,850 kg

### B. AWD — 스마트스트림 가솔린 2.5터보 · 8단 DCT

| 휠 | 인승 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 (대표) | 에너지등급 |
|----|------|---------|------|------|-----|----------------|-----------|
| 18" | 5/6/7인승 | **10.1 km/L** | 8.8 | 12.2 | 168 g/km | 1,915 kg | **4등급** |
| 20" | 5/6인승 | 9.7 km/L | 8.5 | 11.6 | 175 g/km | 1,940 kg | 4등급 |
| 20" | 7인승 | 9.4 km/L | 8.2 | 11.3 | 181 g/km | 1,955 kg | 4등급 |
| 21" | 5인승 | 9.7 km/L | 8.5 | 11.6 | 175 g/km | 1,930 kg | 4등급 |
| 21" | 6/7인승 | 9.4 km/L | 8.2 | 11.3 | 181 g/km | 1,985 kg | 4등급 |

> **raw_line 기준 인승별 공차중량 예시 (AWD 18"):**  
> 5인승 1,860 kg / 6인승 1,900 kg / 7인승 1,915 kg

---

## 2WD vs AWD 요약 비교

| 구분 | 최고 연비 | 최저 연비 | CO2 범위 | 공차중량 범위 | 에너지등급 |
|------|---------|---------|---------|------------|-----------|
| 2WD | 11.0 km/L (18"·5/6인승·기본) | 10.0 km/L (20"/21"·6/7인승) | 152~168 g/km | 1,795~1,920 kg | 4등급 |
| AWD | 10.1 km/L (18") | 9.4 km/L (20"/21"·7인승) | 168~181 g/km | 1,860~1,985 kg | 4등급 |

> 2WD → AWD 전환 시 연비 약 0.9~1.0 km/L 감소, CO2 약 16~13 g/km 증가.

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | 출고가 참고 |
|--------|-----------|
| 익스클루시브 | 36,620,000원 |
| 프레스티지 | 39,490,000원 |
| H-Pick | 42,140,000원 |
| 블랙 익스테리어 | 42,490,000원 |
| 캘리그래피 | 45,530,000원 |
| 블랙 잉크 | 45,530,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 싼타페 MX5 2026 · 2.5T · 2WD 18" 기준 최대 11.0 km/L (4등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 싼타페(SANTA FE) MX5 2026년형은 스마트스트림 2.5 터보 가솔린(2,497 cc)과
8단 DCT를 탑재한 중형 SUV입니다.
2WD 18인치 기준 복합연비 최대 11.0 km/L(CO2 152g/km · 4등급),
AWD 18인치 기준 10.1 km/L(CO2 168g/km · 4등급)가 적용됩니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대(HYUNDAI)
모델: 싼타페(SANTA FE) MX5
파워트레인: 스마트스트림 가솔린 2.5터보
배기량: 2,497 cc
변속기: 8단 DCT
구동: 2WD / AWD
연비(대표·2WD 18"·5/6인승): 11.0 km/L (4등급)
연비(대표·AWD 18"): 10.1 km/L (4등급)
CO2(2WD 18"·기본): 152 g/km
공차중량: 1,795~1,985 kg (구동·인승·휠 조합별)
트림: 익스클루시브·프레스티지·H-Pick·블랙 익스테리어·캘리그래피·블랙 잉크
```

### ④ 인포그래픽·카드 수치 스니펫
```
[2WD 18"·5/6인승·기본] 2,497cc | 11.0 km/L | CO2 152g/km | 1,835kg | 4등급
[2WD 18"·5/6인승·캠O] 2,497cc | 10.8 km/L | CO2 156g/km | 1,835kg | 4등급
[2WD 18"·7인승·기본] 2,497cc | 10.6 km/L | CO2 158g/km | 1,850kg | 4등급
[AWD 18"] 2,497cc | 10.1 km/L | CO2 168g/km | 1,915kg | 4등급
[AWD 20"·7인승] 2,497cc | 9.4 km/L | CO2 181g/km | 1,955kg | 4등급
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 싼타페 하이브리드 | santafe-hybrid 별도 slug — 별도 팩트블록 필요 |
| 옵션별 상세 트림 가격 차이 | 가격 verdict 미인증 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-16_  
_data gate: verdict-santafe-20260611.md (GREEN) · commit 8877504_
