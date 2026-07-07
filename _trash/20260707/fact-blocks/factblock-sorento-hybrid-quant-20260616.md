---
type: fact-block
title: 기아 쏘렌토 하이브리드 팩트블록 (quantitative · MQ4)
topic: sorento-hybrid-factblock-quant
subject: 기아 쏘렌토 하이브리드 (MQ4 · 1.6T HEV)
date: 2026-06-16
data_source:
  - data/outputs/approved/verdict-sorento-hybrid-20260611.md (quantitative/referential GREEN)
created: 2026-06-16
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-009-factblock-batch-20260616]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-sorento-hybrid-20260611.md
  - DB: vehicle_powertrains WHERE slug='sorento-hybrid' (쿼리 2026-06-16, 10행)
  - DB: vehicle_trims WHERE slug='sorento-hybrid' (쿼리 2026-06-16, 0행)
data_gate: verdict-sorento-hybrid-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·배기량·CO2·공차중량·구동방식·휠·에너지등급·변속기
uncertified: 가격·이미지·연식
flags:
  - "vehicles.year = null — 연식 미입력. MQ4 연식(2023~2025년형 혼재 가능성). 데이터팀 확인 권고."
  - "vehicles.body_type = null — 중형 SUV 추정(vehicles.category='SUV'). 데이터팀 보완 권고."
  - "vehicle_trims 데이터 없음 — 트림·가격 정보 미조회."
  - "5/6/7인승 선택에 따라 공차중량 차이 — raw_line에 인승별 중량 명시."
  - "4WD 전 행 연비 동일(13.8 km/L) — 휠 크기 무관."
  - "주의: 쏘렌토(가솔린·디젤, slug=sorento)와 별도 관리. 혼동 금지."
---

# 쏘렌토 하이브리드 팩트 블록 — quantitative (MQ4 · 1.6T HEV)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-sorento-hybrid-20260611 GREEN).  
> 인증 범위: 연비·배기량·CO2·공차중량·구동방식·휠·에너지등급·변속기. 가격·이미지 미포함.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| 연식 | ⚠️ null | vehicles.year 미입력. MQ4 기준 2023~2025년형 혼재 가능. 데이터팀 확인 권고. |
| body_type | ℹ️ null | SUV 추정(category='SUV'). 데이터팀 보완 권고. |
| 트림·가격 | ℹ️ 없음 | vehicle_trims 미등록. 가격 정보 별도 확인 필요. |
| 인승별 공차중량 | ℹ️ 확인 | 5/6/7인승 선택에 따라 최대 40 kg 차이. raw_line에 인승별 중량 기재. |
| 쏘렌토(ICE)와 구분 | ⚠️ | slug=sorento(가솔린·디젤)와 별도. 혼동 금지. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 기아 (KIA) | vehicles.brand |
| 모델명 | 쏘렌토 하이브리드 (SORENTO HYBRID) | vehicles.name |
| 모델코드 | MQ4 | vehicles.model_code |
| 연식 | — (null · 데이터팀 확인 권고) | vehicles.year |
| 세그먼트 | 중형 | vehicles.segment |
| 카테고리 | SUV | vehicles.category |
| 연료 | 하이브리드 (가솔린+모터) | vehicle_powertrains.fuel_kind |
| 엔진 | 1.6 터보 하이브리드 | vehicle_powertrains.engine |
| 배기량 | 1,598 cc | vehicle_powertrains.displacement_cc |
| 변속기 | 6단 자동 | vehicle_powertrains.engine 파생 |
| 구동방식 | 2WD / 4WD | vehicle_powertrains.drive_type (GREEN) |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> 공차중량: DB 저장값(대표 인승 기준). raw_line에 5/6/7인승별 중량 명시됨.

### A. 2WD — 1.6 터보 하이브리드 · 자동 6단 · 1,598 cc

| 휠 | 인승 | 옵션 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 (대표) | 에너지등급 |
|----|------|------|---------|------|------|-----|----------------|-----------|
| 17" | 5인승 | 기본 | **15.7 km/L** | 16.6 | 14.6 | 102 g/km | 1,820 kg | **2등급** |
| 17" | 5인승 | 빌트인 캠 | 15.3 km/L | 15.8 | 14.7 | 105 g/km | 1,820 kg | 2등급 |
| 17" | 6/7인승 | 기본 | 14.8 km/L | 15.2 | 14.3 | 109 g/km | 1,850 kg | 2등급 |
| 18" | 5인승 | 기본 | **15.7 km/L** | 16.6 | 14.6 | 102 g/km | 1,835 kg | **2등급** |
| 18" | 5인승 | 빌트인 캠 | 15.3 km/L | 15.8 | 14.7 | 105 g/km | 1,835 kg | 2등급 |
| 18" | 6/7인승 | 기본 | 14.8 km/L | 15.2 | 14.3 | 109 g/km | 1,865 kg | 2등급 |
| 19" | 5/6/7인승 | 빌트인 캠 | 14.8 km/L | 15.2 | 14.3 | 109 g/km | 1,850 kg | 2등급 |

> **raw_line 기준 인승별 공차중량 예시 (2WD 17" 기본·6/7인승):**  
> 6인승 1,850 kg / 7인승 1,860 kg  
> **raw_line 기준 인승별 공차중량 예시 (2WD 19" 캠O):**  
> 5인승 1,850 kg / 6인승 1,880 kg / 7인승 1,890 kg

### B. 4WD — 1.6 터보 하이브리드 · 자동 6단 · 1,598 cc

| 휠 | 옵션 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 (대표) | 에너지등급 |
|----|------|---------|------|------|-----|----------------|-----------|
| 17" | — | **13.8 km/L** | 14.0 | 13.4 | 118 g/km | 1,880 kg | **2등급** |
| 18" | — | 13.8 km/L | 14.0 | 13.4 | 118 g/km | 1,895 kg | 2등급 |
| 19" | 빌트인 캠 | 13.8 km/L | 14.0 | 13.4 | 118 g/km | 1,910 kg | 2등급 |

> 4WD 전 행 복합연비 13.8 km/L 동일 — 휠 크기에 따른 연비 차이 없음(DB 기준).  
> **raw_line 기준 인승별 공차중량 예시 (4WD 17"):**  
> 5인승 1,880 kg / 6인승 1,910 kg / 7인승 1,920 kg

---

## 2WD vs 4WD 요약 비교

| 구분 | 최고 연비 | 최저 연비 | CO2 범위 | 공차중량 범위 | 에너지등급 |
|------|---------|---------|---------|------------|-----------|
| 2WD | 15.7 km/L (17"/18"·5인승·기본) | 14.8 km/L (17"/18"·6/7인승 또는 19") | 102~109 g/km | 1,820~1,890 kg | 2등급 |
| 4WD | 13.8 km/L (17"/18"/19" 동일) | — | 118 g/km | 1,880~1,950 kg | 2등급 |

> 2WD → 4WD 전환 시 연비 약 1.9~2.0 km/L 감소, CO2 약 9~16 g/km 증가.  
> 전 조합 **2등급** 유지 — 하이브리드 우수 효율.

---

## 트림 라인업

> ℹ️ vehicle_trims 데이터 미등록. 가격 정보 별도 확인 필요.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
기아 쏘렌토 하이브리드 MQ4 · 1.6T HEV · 2WD 17" 기준 최대 15.7 km/L (2등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
기아 쏘렌토 하이브리드(SORENTO HYBRID) MQ4는 1.6 터보 하이브리드(1,598 cc)와
6단 자동변속기를 탑재한 중형 SUV입니다.
2WD 17인치/18인치 5인승 기준 복합연비 15.7 km/L(2등급 · CO2 102g/km)을 기록하며,
4WD 선택 시 13.8 km/L(2등급)가 유지됩니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 기아(KIA)
모델: 쏘렌토 하이브리드(SORENTO HYBRID) MQ4
파워트레인: 1.6 터보 가솔린 하이브리드
배기량: 1,598 cc
변속기: 6단 자동
구동: 2WD / 4WD
연비(대표·2WD 17"·5인승): 15.7 km/L (2등급)
연비(대표·4WD): 13.8 km/L (2등급)
CO2(2WD·5인승 최저): 102 g/km
공차중량: 1,820~1,950 kg (구동·인승·휠 조합별)
※ 트림 가격 정보 별도 확인 필요
```

### ④ 인포그래픽·카드 수치 스니펫
```
[HEV 2WD 17"·5인승·기본] 1,598cc | 15.7 km/L | CO2 102g/km | 1,820kg | 2등급
[HEV 2WD 17"·5인승·캠O] 1,598cc | 15.3 km/L | CO2 105g/km | 1,820kg | 2등급
[HEV 2WD 17"·6/7인승] 1,598cc | 14.8 km/L | CO2 109g/km | 1,850kg | 2등급
[HEV 4WD 17"] 1,598cc | 13.8 km/L | CO2 118g/km | 1,880kg | 2등급
[HEV 4WD 19"·캠O] 1,598cc | 13.8 km/L | CO2 118g/km | 1,910kg | 2등급
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | vehicle_trims 미등록 + 가격 verdict 범위 외 |
| 연식 구분 | vehicles.year null — 데이터팀 확인 후 반영 |
| 쏘렌토(가솔린·디젤) | slug=sorento 별도 팩트블록(factblock-sorento-quant-20260614.md) |

---

_작성: 컨텐츠_  
_작성일: 2026-06-16_  
_data gate: verdict-sorento-hybrid-20260611.md (GREEN) · commit 8877504_
