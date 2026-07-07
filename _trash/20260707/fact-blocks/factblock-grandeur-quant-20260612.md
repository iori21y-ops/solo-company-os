---
type: fact-block
title: 현대 그랜저 팩트블록 (quantitative · GN7)
topic: grandeur-factblock-quant
subject: 현대 그랜저 (GN7 2026년형)
date: 2026-06-12
data_source:
  - data/outputs/approved/verdict-grandeur-20260611.md (quantitative/referential GREEN)
created: 2026-06-12
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-005-factblock-batch-20260612]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-grandeur-20260611.md
  - DB: vehicle_powertrains WHERE slug='grandeur' (쿼리 2026-06-12)
  - DB: vehicle_trims WHERE slug='grandeur' (트림명만, 수치 null)
data_gate: verdict-grandeur-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·배기량·CO2·공차중량·구동방식·휠
uncertified: 가격·이미지·vehicles 메타(body_type 등)
flags:
  - "vehicles 테이블 body_type/category = 'SUV' → 명백 오류(그랜저는 준대형 세단). 팩트블록 미채택, 데이터팀 수정 필요."
  - "vehicles.highlights/engine 필드에 '1.6 터보·하이브리드' 기재 — vehicle_powertrains에는 2.5/3.5 가솔린·LPG만 존재. vehicles 메타 데이터팀 확인 권고."
  - "grandeur-hybrid는 별도 slug·별도 verdict 존재 → 다음 배치에서 별도 팩트블록 생산 예정."
---

# 그랜저 팩트 블록 — quantitative (GN7)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-grandeur-20260611 GREEN).  
> 인증 범위: 연비·배기량·CO2·공차중량·구동방식·휠. 가격·이미지 미포함.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| vehicles 메타 오류 | ⚠️ 요확인 | body_type = 'SUV' 기재 — 실제는 준대형 세단. 데이터팀 수정 권고. |
| vehicles.engine 불일치 | ⚠️ 요확인 | '1.6 터보·하이브리드' 기재이나 vehicle_powertrains엔 2.5/3.5만 존재. |
| 그랜저 하이브리드 | 📌 별도 | grandeur-hybrid 별도 slug·verdict 존재 → 별도 팩트블록 생산 예정. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (HYUNDAI) | vehicles.brand |
| 모델명 | 그랜저 (GRANDEUR) | vehicles.name |
| 모델코드 | GN7 | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 준대형 | vehicles.segment |
| 변속기 (공통) | 8단 자동변속기 | vehicle_powertrains.raw_line (전 파워트레인 동일) |
| 구동방식 | 2WD / AWD (엔진별 상이) | vehicle_powertrains.drive_type (GREEN) |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

### 가솔린 2.5 (스마트스트림 2,497 cc)

| 휠 | 구동 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 | 에너지등급 |
|----|------|---------|------|------|-----|---------|-----------|
| 18" | 2WD | 11.7 km/L | 10.0 | 14.5 | 143 g/km | 1,620 kg | 3등급 |
| 19" | 2WD | 11.4 km/L | 9.8 | 14.2 | 148 g/km | 1,635 kg | 4등급 |
| 20" | 2WD | 11.2 km/L | 9.6 | 13.8 | 150 g/km | 1,655 kg | 4등급 |

### 가솔린 3.5 (스마트스트림 3,470 cc)

| 휠 | 구동 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 | 에너지등급 |
|----|------|---------|------|------|-----|---------|-----------|
| 18" | 2WD | 10.4 km/L | 8.7 | 13.4 | 163 g/km | 1,695 kg | 4등급 |
| 19" | 2WD | 10.1 km/L | 8.5 | 13.0 | 168 g/km | 1,710 kg | 4등급 |
| 20" | 2WD | 9.7 km/L | 8.3 | 12.2 | 176 g/km | 1,730 kg | 4등급 |
| 18" | AWD | 9.5 km/L | 8.2 | 11.7 | 179 g/km | 1,765 kg | 4등급 |
| 19" | AWD | 9.2 km/L | 7.9 | 11.5 | 186 g/km | 1,780 kg | 5등급 |
| 20" | AWD | 9.0 km/L | 7.7 | 11.2 | 190 g/km | 1,800 kg | 5등급 |

### LPG 3.5 (3,470 cc)

| 휠 | 구동 | 복합연비 | 도심 | 고속 | CO2 | 공차중량 | 에너지등급 |
|----|------|---------|------|------|-----|---------|-----------|
| 18" | — | 7.8 km/L | 6.7 | 9.6 | 170 g/km | 1,715 kg | 5등급 |
| 19" | — | 7.4 km/L | 6.3 | 9.2 | 180 g/km | 1,730 kg | 5등급 |
| 20" | — | 7.3 km/L | 6.2 | 9.1 | 183 g/km | 1,750 kg | 5등급 |

---

## 트림 라인업 (vehicle_trims · 트림명만)

> 수치(연비·가격 등) null — 트림별 수치 DB 미연동. 트림명만 인증 범위 외.

| 트림명 |
|--------|
| 프리미엄 |
| 익스클루시브 |
| 어너스 |
| 캘리그래피 |
| 블랙 잉크 |
| 블랙 익스테리어 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 그랜저 GN7 2026년형 · 2.5/3.5 가솔린 · LPG 3.5 · 8단 자동 · 2WD/AWD
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 그랜저(GRANDEUR) GN7 2026년형은 스마트스트림 가솔린 2.5(2,497 cc)·3.5(3,470 cc)와
LPG 3.5 세 가지 파워트레인 옵션을 갖춘 국산 준대형 세단입니다.
8단 자동변속기를 탑재하며, 2.5 가솔린 2WD 18" 기준 복합연비 11.7 km/L(3등급)을 달성합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대(HYUNDAI)
모델: 그랜저(GRANDEUR) GN7
연식: 2026년형
세그먼트: 준대형
파워트레인: 가솔린 2.5 / 가솔린 3.5 / LPG 3.5
변속기: 8단 자동변속기
구동방식: 2WD / AWD (엔진별 상이)
연비(대표): 11.7 km/L (2.5 가솔린 2WD 18" · 3등급)
배기량: 2,497 cc (2.5) / 3,470 cc (3.5)
공차중량: 1,620~1,800 kg (파워트레인·구동·휠 조합별)
트림: 프리미엄·익스클루시브·어너스·캘리그래피·블랙 잉크·블랙 익스테리어
```

### ④ 인포그래픽·카드 수치 스니펫
```
[2.5가솔린] 2,497cc | 11.7km/L(2WD18") | CO2 143g/km | 1,620kg
[3.5가솔린] 3,470cc | 10.4km/L(2WD18") | CO2 163g/km | 1,695kg
[3.5LPG]   3,470cc | 7.8km/L(18")    | CO2 170g/km | 1,715kg
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 하이브리드 제원 | grandeur-hybrid는 별도 slug — 다음 배치 처리 예정 |
| 트림별 제원 수치 | vehicle_trims 수치 null (DB 미연동) |
| 바디타입·카테고리 | vehicles 메타 오류(SUV 기재) → 데이터팀 수정 후 채택 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-12_  
_data gate: verdict-grandeur-20260611.md (GREEN) · commit 8877504_
