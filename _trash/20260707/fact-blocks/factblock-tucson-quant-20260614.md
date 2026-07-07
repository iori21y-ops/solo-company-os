---
type: fact-block
title: 현대 투싼 팩트블록 (quantitative · NX4 · 가솔린 1.6 터보)
topic: tucson-factblock-quant
subject: 현대 투싼 (NX4 2026년형 · 가솔린 1.6 터보)
date: 2026-06-14
data_source:
  - data/outputs/approved/verdict-tucson-20260611.md (quantitative/referential GREEN)
created: 2026-06-14
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-007-factblock-batch-20260614]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-tucson-20260611.md
  - DB: vehicle_powertrains WHERE slug='tucson' (쿼리 2026-06-14)
  - DB: vehicle_trims WHERE slug='tucson' (트림명·가격)
data_gate: verdict-tucson-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·배기량·CO2·공차중량·구동방식·휠·에너지등급
uncertified: 가격·이미지
flags:
  - "빌트인 캠 장착 행 별도 존재 (18\" 2WD) — 연비 12.3 km/L(3등급), CO2 135g/km. 기타 스펙 동일."
  - "vehicle_trims 수치(연비·drive_type·wheel_size 등) null → 트림명만 기재. 가격 미인증."
  - "tucson-hybrid는 별도 slug/verdict → 다음 배치 처리 예정."
---

# 투싼 팩트 블록 — quantitative (NX4 · 가솔린 1.6 터보)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-tucson-20260611 GREEN).  
> 인증 범위: 연비·배기량·CO2·공차중량·구동방식·휠·에너지등급. 가격·이미지 미포함.  
> **적용 파워트레인**: 가솔린 1.6 터보 (스마트스트림 7단 DCT).  
> **미적용**: 투싼 하이브리드(tucson-hybrid slug) → 별도 verdict·별도 팩트블록 예정.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| 빌트인 캠 행 | ℹ️ 별도 | 18" 2WD 빌트인 캠 장착 시: 12.3 km/L·3등급·CO2 135g/km (일반 대비 약 0.2 km/L 저하). |
| vehicle_trims 수치 | ℹ️ null | 트림별 제원 DB 미연동. 트림명만 참조. |
| 투싼 하이브리드 | 📌 별도 | tucson-hybrid 별도 slug·verdict → 다음 배치 예정. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (HYUNDAI) | vehicles.brand |
| 모델명 | 투싼 (TUCSON) | vehicles.name |
| 모델코드 | NX4 | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 준중형 | vehicles.segment |
| 바디타입 | SUV | vehicles.body_type |
| 연료 유형 | 가솔린 | vehicle_powertrains.fuel_kind |
| 엔진 | 스마트스트림 가솔린 1.6 터보엔진 | vehicle_powertrains.engine |
| 배기량 | 1,598 cc | vehicle_powertrains.displacement_cc |
| 변속기 (공통) | 스마트스트림 7단 DCT | vehicle_powertrains.raw_line |
| 구동방식 | 2WD / AWD | vehicle_powertrains.drive_type |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 스마트스트림 가솔린 1.6 터보 (1,598 cc · 7단 DCT)

| 휠 | 구동 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 | 에너지등급 |
|----|------|---------|------|------|-----|---------|-----------|
| 17" | 2WD | **12.5 km/L** | 11.5 | 13.9 | 133 g/km | 1,535 kg | **3등급** |
| 17" | AWD | 11.6 km/L | 10.7 | 12.8 | 144 g/km | 1,590 kg | 3등급 |
| 18" | 2WD | 12.5 km/L | 11.5 | 13.8 | 133 g/km | 1,555 kg | 3등급 |
| 18" | 2WD+캠 | 12.3 km/L | 11.3 | 13.7 | 135 g/km | 1,555 kg | 3등급 |
| 18" | AWD | 11.3 km/L | 10.2 | 12.9 | 148 g/km | 1,610 kg | 4등급 |
| 19" | 2WD | 12.0 km/L | 10.9 | 13.6 | 139 g/km | 1,575 kg | 3등급 |
| 19" | AWD | 11.2 km/L | 10.1 | 12.7 | 150 g/km | 1,630 kg | 4등급 |

> 2WD 기준 17"와 18"의 복합연비 동일(12.5 km/L). CO2·공차중량만 소폭 차이.  
> AWD 선택 시 연비 0.7~1.0 km/L 감소, 공차중량 약 50~55 kg 증가.  
> 19" 2WD: 12.0 km/L (17"/18" 대비 0.5 km/L 감소).

---

## 트림 라인업 (vehicle_trims · 트림명 참조)

> 수치(연비·가격 등) null — 트림명만 인증 범위 외.  
> 가격 미인증 (참고값으로만 표기).

| 트림명 | 참고가(원, 미인증) |
|--------|----------|
| 모던 | 28,480,000 |
| 프리미엄 | 31,160,000 |
| H-Pick | 32,050,000 |
| 인스퍼레이션 | 34,600,000 |
| 블랙 익스테리어 | 35,050,000 |
| N라인 | 35,450,000 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 투싼 NX4 2026년형 · 1.6 가솔린 터보 · 7단 DCT · 2WD/AWD · 17~19인치
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 투싼(TUCSON) NX4 2026년형은 스마트스트림 가솔린 1.6 터보엔진(1,598 cc)과
스마트스트림 7단 DCT를 탑재한 준중형 SUV입니다.
17·18·19인치 휠과 2WD·AWD 조합으로 구성되며, 17" 2WD 기준 복합연비 12.5 km/L(3등급)을 달성합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대(HYUNDAI)
모델: 투싼(TUCSON) NX4
연식: 2026년형
세그먼트: 준중형 SUV
파워트레인: 1.6 가솔린 터보
배기량: 1,598 cc
변속기: 7단 DCT
구동방식: 2WD / AWD
연비(대표): 12.5 km/L (17" 또는 18" 2WD · 3등급)
CO2(대표): 133 g/km (17"/18" 2WD)
공차중량: 1,535~1,630 kg (휠·구동 조합별)
트림: 모던·프리미엄·H-Pick·인스퍼레이션·블랙 익스테리어·N라인
```

### ④ 인포그래픽·카드 수치 스니펫
```
[가솔린 17" 2WD] 1,598cc | 12.5km/L | CO2 133g/km | 1,535kg | 3등급
[가솔린 18" AWD] 1,598cc | 11.3km/L | CO2 148g/km | 1,610kg | 4등급
[가솔린 19" 2WD] 1,598cc | 12.0km/L | CO2 139g/km | 1,575kg | 3등급
[가솔린 19" AWD] 1,598cc | 11.2km/L | CO2 150g/km | 1,630kg | 4등급
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 하이브리드 제원 | tucson-hybrid 별도 slug — 다음 배치 처리 예정 |
| 트림별 제원 수치 | vehicle_trims 수치 null (DB 미연동) |

---

_작성: 컨텐츠_  
_작성일: 2026-06-14_  
_data gate: verdict-tucson-20260611.md (GREEN) · commit 8877504_
