---
type: fact-block
title: 현대 싼타페 하이브리드 팩트블록 (quantitative · 2026년형)
topic: santafe-hybrid-factblock-quant
subject: 현대 싼타페 하이브리드 (2026년형 · 1.6T HEV 중형 SUV)
date: 2026-06-30
data_source:
  - data/outputs/approved/verdict-santafe-hybrid-20260611.md (quantitative/referential GREEN)
created: 2026-06-30
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-025-factblock-batch-20260630]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-santafe-hybrid-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='santafe-hybrid' (쿼리 2026-06-30, 6행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='santafe-hybrid' (쿼리 2026-06-30, 6행)
data_gate: verdict-santafe-hybrid-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·구동방식·휠사이즈·빌트인캠 적용여부
uncertified: 가격·이미지·안전등급·트림별 옵션·인승별 공차중량(raw_line 참고)
flags:
  - "vehicles.segment null — DB 미입력."
  - "vehicles.model_code null — DB 미입력."
  - "인승별 공차중량: raw_line에만 명시(7인승/6인승/5인승 상이) — DB curb_weight_kg는 대표값 1개만 수록."
  - "AWD 18\" 2행: 5인승(1,930kg·2등급·14.0) vs 7/6인승(1,985kg·3등급·13.6) — 인승별 제원 상이."
  - "빌트인캠 적용 시 연비 하락: 2WD 18\" 기준 15.5→15.0 km/ℓ (−0.5 km/ℓ), CO2 104→108 g/km."
  - "vehicle_trims.drive_type·wheel_size null — 트림·구동·휠 연결 불가."
---

# 싼타페 하이브리드 팩트 블록 — quantitative (2026년형 · 1.6T HEV)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-santafe-hybrid-20260611 GREEN).  
> 인증 범위: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·구동방식·휠사이즈·빌트인캠 여부.  
> 인승별 공차중량 세부 수치는 raw_line 기반 참고값.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| segment | ℹ️ null | DB 미입력. |
| model_code | ℹ️ null | DB 미입력. |
| 인승별 공차중량 | ⚠️ raw_line | DB curb_weight_kg는 대표값(최대 인승 기준). 인승별 상세는 raw_line 참고. |
| AWD 18\" 인승 이원화 | ⚠️ 주의 | 5인승(1,930kg·2등급)과 7/6인승(1,985kg·3등급) 제원 상이. |
| 빌트인캠 연비 영향 | ℹ️ 정상 | 장착 시 복합연비 −0.5 km/ℓ, CO2 +4 g/km (2WD 18\" 기준). |
| 가격 데이터 | 📌 참고용 | 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (Hyundai) | vehicles |
| 모델명 | 싼타페 하이브리드 | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 카테고리 | SUV | vehicles.category |
| 연료 | 하이브리드 (HEV) | vehicle_powertrains.fuel_kind |
| 배기량 | 1,598cc (1.6T) | vehicle_powertrains.displacement_cc |
| 변속기 | 6단 자동 (전 구성) | raw_line |
| 구동방식 | 2WD / AWD | vehicle_powertrains.drive_type |
| 휠 | 18\" / 20\" | vehicle_powertrains.wheel |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

| 행 | 구동 | 휠 | 빌트인캠 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량(대표) | 에너지등급 |
|---|---|---|---|---|---|---|---|---|---|
| A | **2WD** | **18\"** | — | **15.5 km/ℓ** | 16.3 | 14.6 | 104 g/km | **1,920 kg** | **2등급** |
| B | **2WD** | **18\"** | ✅ | **15.0 km/ℓ** | 15.7 | 14.2 | 108 g/km | **1,920 kg** | **2등급** |
| C | **AWD** | **18\"** | — | **14.0 km/ℓ** | 14.1 | 13.8 | 117 g/km | **1,930 kg** | **2등급** |
| D | **AWD** | **18\"** | — | **13.6 km/ℓ** | 13.7 | 13.4 | 120 g/km | **1,985 kg** | **3등급** |
| E | **2WD** | **20\"** | — | **14.4 km/ℓ** | 14.9 | 13.8 | 112 g/km | **1,950 kg** | **2등급** |
| F | **AWD** | **20\"** | — | **13.0 km/ℓ** | 13.3 | 12.6 | 126 g/km | **2,025 kg** | **3등급** |

> ※ 행 C: AWD 18" **5인승** (공차중량 1,930 kg · **2등급**)  
> ※ 행 D: AWD 18" **7인승/6인승** (공차중량 1,985 kg · **3등급**) — 인승별 등급 상이

### raw_line 인승별 공차중량 참고 (발행 시 DB 공차중량과 병기 권고)

| 구분 | 7인승 | 6인승 | 5인승 |
|------|------|------|------|
| 2WD 18" | 1,920 kg | 1,905 kg | 1,865 kg |
| AWD 18" (5인승 행 C) | — | — | 1,930 kg |
| AWD 18" (7/6인승 행 D) | 1,985 kg | 1,970 kg | — |
| 2WD 20" | 1,950 kg | 1,935 kg | 1,895 kg |
| AWD 20" | 2,025 kg | 2,010 kg | 1,970 kg |

> **핵심 포인트:**
> - 2WD 18" 표준이 최고 연비: 복합 15.5 km/ℓ, 에너지 2등급
> - 빌트인캠 적용 시 연비 0.5 km/ℓ 하락 (2WD 18" 기준: 15.5→15.0 km/ℓ)
> - AWD 18" **인승에 따라 에너지등급 분리**: 5인승 2등급(14.0) vs 7/6인승 3등급(13.6)
> - 20" 휠 선택 시 연비 추가 하락: 2WD 15.5→14.4 (−1.1), AWD 14.0→13.0 (−1.0 · 5인승 기준)
> - AWD 20" 최대 공차중량 2,025 kg (7인승 기준)

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | drive_type | wheel_size |
|--------|-----------|-----------|
| 익스클루시브 | null | null |
| 프레스티지 | null | null |
| 블랙 잉크 | null | null |
| 블랙 익스테리어 | null | null |
| 캘리그래피 | null | null |
| H-Pick | null | null |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 싼타페 하이브리드 2026 · 1.6T HEV SUV · 2WD 복합 15.5km/ℓ (2등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 싼타페 하이브리드 2026년형은 1.6T 가솔린 터보 하이브리드 엔진과 6단 자동변속기를 탑재한 중형 SUV입니다.
2WD 18" 표준 기준 복합 연비 15.5 km/ℓ(도심 16.3 / 고속 14.6), 에너지 2등급 인증으로
하이브리드 중형 SUV 중 높은 효율을 갖추고 있습니다.
AWD와 20" 휠 옵션도 제공되며, 빌트인캠 장착 시 연비는 15.0 km/ℓ로 소폭 하락합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대
모델: 싼타페 하이브리드 2026년형
연료: 하이브리드 (1.6T HEV)
배기량: 1,598cc
변속기: 6단 자동
구동방식: 2WD / AWD
휠: 18" / 20"
에너지등급: 2등급(2WD·AWD5인승) / 3등급(AWD 7/6인승·AWD20")
트림: 익스클루시브, 프레스티지, 블랙잉크, 블랙익스테리어, 캘리그래피, H-Pick

연비 — 2WD 18" 표준:     복합 15.5 / 도심 16.3 / 고속 14.6 km/ℓ · CO2 104g · 2등급
연비 — 2WD 18" + 빌트인캠: 복합 15.0 / 도심 15.7 / 고속 14.2 km/ℓ · CO2 108g · 2등급
연비 — AWD 18" (5인승):   복합 14.0 / 도심 14.1 / 고속 13.8 km/ℓ · CO2 117g · 2등급
연비 — AWD 18" (7/6인승): 복합 13.6 / 도심 13.7 / 고속 13.4 km/ℓ · CO2 120g · 3등급
연비 — 2WD 20":          복합 14.4 / 도심 14.9 / 고속 13.8 km/ℓ · CO2 112g · 2등급
연비 — AWD 20":          복합 13.0 / 도심 13.3 / 고속 12.6 km/ℓ · CO2 126g · 3등급

공차중량: 1,865 ~ 2,025 kg (인승·구동·휠 구성별 상이)
```

### ④ 인포그래픽·카드 수치 스니펫
```
[싼타페 하이브리드 2026 · 1.6T HEV]
2WD 18"        15.5km/ℓ | CO2 104g | 1,920kg | 2등급  ← 최고 연비
2WD 18" + 캠   15.0km/ℓ | CO2 108g | 1,920kg | 2등급
AWD 18" (5인승) 14.0km/ℓ | CO2 117g | 1,930kg | 2등급
AWD 20"        13.0km/ℓ | CO2 126g | 2,025kg | 3등급
※ 복합연비 기준
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 verdict 미인증 |
| 트림별 옵션 | 미수집 |
| 안전 등급 | 미수집 |
| 트림별 구동·휠 매핑 | vehicle_trims null — 매핑 불가 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-30_  
_data gate: verdict-santafe-hybrid-20260611.md (GREEN) · commit 8877504_
