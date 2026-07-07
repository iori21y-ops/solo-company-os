---
type: fact-block
title: 기아 카니발 하이브리드 팩트블록 (quantitative · KA4)
topic: carnival-hybrid-factblock-quant
subject: 기아 카니발 하이브리드 (KA4 · 1.6T 터보 HEV 대형 다목적)
date: 2026-06-18
data_source:
  - data/outputs/approved/verdict-carnival-hybrid-20260611.md (quantitative/referential GREEN)
created: 2026-06-18
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-011-factblock-batch-20260618]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-carnival-hybrid-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='carnival-hybrid' (쿼리 2026-06-18, 3행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='carnival-hybrid' (쿼리 2026-06-18, 0행)
data_gate: verdict-carnival-hybrid-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠·인승·빌트인캠 연비 영향
uncertified: 가격·이미지·구동방식·안전등급·연식·트림별 옵션
flags:
  - "vehicles.year null — DB 미입력. 연식 미확인. 데이터팀 보완 권고."
  - "vehicles.body_type null — DB 미입력. 데이터팀 보완 권고."
  - "vehicle_powertrains.drive_type null 전 행 — FWD(전륜) 추정(대형 미니밴 전형). 데이터팀 확인 권고."
  - "Row B curb_weight_kg null — 빌트인 캠 적용 행. 원문 확인 권고."
  - "vehicle_trims 미등록 — 트림·가격 참고 불가. 데이터팀 수집 필요."
---

# 카니발 하이브리드 팩트 블록 — quantitative (KA4 · 1.6T 터보 HEV)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-carnival-hybrid-20260611 GREEN).  
> 인증 범위: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠·인승 구분·빌트인캠 연비 영향.  
> 구동방식·연식·트림 정보는 DB 미입력 — 참고 불가.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| year | ⚠️ null | DB 미입력. 연식 미확인 — 데이터팀 보완 권고. |
| body_type | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| drive_type | ⚠️ null 전 행 | 전 행 FWD(전륜구동) 추정. 데이터팀 확인 권고. |
| Row B 공차중량 | ⚠️ null | 빌트인 캠 행 미수록. 원문 확인 권고. |
| vehicle_trims | ⚠️ 미등록 | 트림·가격 데이터 없음. 데이터팀 수집 필요. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 기아 (KIA) | vehicles.brand |
| 모델명 | 카니발 하이브리드 (Carnival Hybrid) | vehicles.name |
| 모델코드 | KA4 | vehicles.model_code |
| 연식 | — (null) | vehicles.year |
| 세그먼트 | 대형 | vehicles.segment |
| 카테고리 | 다목적 (MPV/미니밴) | vehicles.category |
| 연료 | 하이브리드 (HEV) | vehicle_powertrains.fuel_kind |
| 배기량 | 1,598cc (1.6T 터보) | vehicle_powertrains.displacement_cc |
| 변속기 | 6단 자동 | vehicle_powertrains.engine |
| 인승 | 7인승 / 9인승 | raw_line |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> 구동방식 전 행 null — FWD(전륜구동) 추정. 데이터팀 확인 권고.  
> Row B 공차중량 DB null — 원문 확인 필요.

| 행 | 휠 | 인승 | 빌트인캠 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|---|
| A | 18" | 9인승 | — | **14.0 km/ℓ** | 14.6 | 13.3 | 116 g/km | **2,155 kg** | **2등급** |
| B | 18" | — | ✓ 포함 | **13.7 km/ℓ** | 14.0 | 13.4 | 118 g/km | — (null) | **3등급** |
| C | 19" | 7/9인승 | — | **13.5 km/ℓ** | 14.0 | 12.9 | 121 g/km | **2,165 kg** | **3등급** |

> **핵심 포인트:**
> - 최고 연비: Row A (18" 9인승) — 복합 **14.0 km/ℓ**, **2등급**
> - 빌트인 캠(Row B) 적용 시 연비 0.3 km/ℓ 하락 (14.0→13.7), 에너지등급 2→3등급 하락
> - 19인치(Row C) 선택 시 18인치 대비 복합 0.5 km/ℓ 하락, CO2 5 g/km 증가
> - 공차중량: 18"(2,155 kg) vs 19"(2,165 kg) — 10 kg 차이
> - 카니발 가솔린(KA4, 동급) 대비 하이브리드 연비 대폭 향상 — 가솔린 별도 팩트블록 참조

---

## 빌트인 캠 연비 영향 요약

| 옵션 | 연비(복합) | 에너지등급 |
|------|-----------|-----------|
| 기본 (18" · Row A 기준) | 14.0 km/ℓ | 2등급 |
| 빌트인 캠 포함 (18" · Row B) | 13.7 km/ℓ | 3등급 |
| **차이** | **−0.3 km/ℓ** | **등급 하락** |

> ⚠️ 빌트인 캠 선택 시 에너지등급이 2→3등급으로 하락함. 장기렌트·리스 상담 시 중요 포인트.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
기아 카니발 하이브리드 KA4 · 1.6T HEV · 18" 9인승 복합 14.0km/ℓ (2등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
기아 카니발 하이브리드(KA4)는 1.6T 터보 하이브리드 + 6단 자동변속기를 탑재한 대형 다목적 차량입니다.
18인치 9인승 기준 복합 14.0 km/ℓ(도심 14.6 / 고속 13.3), CO2 116 g/km으로 에너지소비효율 2등급을 달성하며,
빌트인 캠 선택 시 연비가 13.7 km/ℓ(3등급)로 소폭 하락합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 기아(KIA)
모델: 카니발 하이브리드 (KA4)
연료: 하이브리드 (HEV)
배기량: 1,598cc (1.6T 터보)
변속기: 6단 자동
인승: 7인승 / 9인승
구동방식: FWD 추정 (DB 미기재)
연비 (18" 9인승): 복합 14.0 / 도심 14.6 / 고속 13.3 km/ℓ  → 2등급
연비 (18" 빌트인캠): 복합 13.7 / 도심 14.0 / 고속 13.4 km/ℓ → 3등급
연비 (19" 7/9인승): 복합 13.5 / 도심 14.0 / 고속 12.9 km/ℓ → 3등급
CO2: 116~121 g/km (조합별)
공차중량: 2,155 kg (18") / 2,165 kg (19") — Row B null
```

### ④ 인포그래픽·카드 수치 스니펫
```
[18"·9인승]       14.0km/ℓ | CO2 116g | 2,155kg | 2등급  ← 최고 효율
[18"·빌트인캠]    13.7km/ℓ | CO2 118g |  — kg   | 3등급  ← 캠 적용
[19"·7·9인승]     13.5km/ℓ | CO2 121g | 2,165kg | 3등급
※ 구동방식 FWD 추정 / 복합연비 기준
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | vehicle_trims 미등록 + 가격 verdict 미인증 |
| 연식 | vehicles.year null — 데이터팀 확인 필요 |
| 구동방식 | drive_type null 전 행 — 데이터팀 확인 필요 |
| Row B 공차중량 | curb_weight null — 원문 확인 필요 |
| 전기 모터 출력 | 미수집 |
| EV 주행거리 | HEV (순수 전기 주행 해당 없음) |

---

_작성: 컨텐츠_  
_작성일: 2026-06-18_  
_data gate: verdict-carnival-hybrid-20260611.md (GREEN) · commit 8877504_
