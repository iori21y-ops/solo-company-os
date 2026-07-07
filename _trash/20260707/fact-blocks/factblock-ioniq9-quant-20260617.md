---
type: fact-block
title: 현대 아이오닉 9 팩트블록 (quantitative · 2027년형)
topic: ioniq9-factblock-quant
subject: 현대 아이오닉 9 (2027년형 · 전기 대형 SUV)
date: 2026-06-17
data_source:
  - data/outputs/approved/verdict-ioniq9-20260611.md (quantitative/referential GREEN)
created: 2026-06-17
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-010-factblock-batch-20260617]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-ioniq9-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='ioniq9' (쿼리 2026-06-17, 6행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='ioniq9' (쿼리 2026-06-17, 3행)
data_gate: verdict-ioniq9-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 전비·주행거리·공차중량·구동방식·휠·에너지등급
uncertified: 가격·이미지·배터리 용량·모터 출력·충전속도
flags:
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.segment null — 대형 SUV(플래그십 대형 전동 MPV) 추정. 데이터팀 보완 권고."
  - "19인치 2WD 행 2건 존재 (curb_weight 2,510 vs 2,610 kg) — 배터리 구성 차이 추정. 데이터팀 확인 권고."
  - "21인치 AWD 행 2건 존재 (curb_weight 2,655 vs 2,675 kg) — 세부 구성 차이 추정. 데이터팀 확인 권고."
  - "curb_weight_kg DB값은 6인승 기준. 7인승은 5~25 kg 중량 증가 (raw_line 참조)."
  - "fuel_eff_city·fuel_eff_highway DB null — 도심·고속 전비는 raw_line 파싱값 사용."
  - "vehicle_trims.base_price는 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# 아이오닉 9 팩트 블록 — quantitative (2027년형 · 전기)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-ioniq9-20260611 GREEN).  
> 인증 범위: 전비(km/kWh)·복합주행거리·공차중량·구동방식·휠·에너지등급.  
> CO2 배출량: 전기차 해당 없음 (N/A).

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| model_code | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| segment | ℹ️ null | 대형 SUV(플래그십 전동 MPV) 추정. |
| 19" 2WD 행 중복 | ⚠️ 요확인 | curb 2,510 / 2,610 kg 행 2건 — 배터리 옵션 차이 추정. |
| 21" AWD 행 중복 | ⚠️ 요확인 | curb 2,655 / 2,675 kg 행 2건 — 세부 구성 차이 추정. |
| 인승별 공차중량 | ℹ️ 참고 | DB는 6인승 기준. 7인승 5~25 kg 추가 (raw_line 명시). |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (HYUNDAI) | vehicles.brand |
| 모델명 | 아이오닉 9 (IONIQ 9) | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2027년형 | vehicles.year |
| 세그먼트 | — (null, 대형 추정) | vehicles.segment |
| 카테고리 | SUV | vehicles.category |
| 연료 | 전기 (BEV) | vehicle_powertrains.fuel_kind |
| 배기량 | N/A (전기) | — |
| 인승 | 6인승 / 7인승 | raw_line |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> 전비 도심·고속 수치는 raw_line 파싱값. 복합 수치는 DB 직접 저장.  
> 공차중량은 6인승 기준 (7인승은 +5~25 kg, raw_line 참조).

| 행 | 휠 | 구동 | 전비(복합) | 전비(도심) | 전비(고속) | 주행거리(복합) | 주행거리(도심) | 주행거리(고속) | 공차중량(6인승) | 에너지등급 |
|---|---|---|---|---|---|---|---|---|---|---|
| A | 19" | 2WD | **4.3 km/kWh** | 4.7 | 3.9 | **532 km** | 578 | 475 | 2,510 kg | **3등급** |
| B | 19" | 2WD | 4.1 km/kWh | 4.5 | 3.7 | 503 km | 545 | 451 | 2,610 kg | 4등급 |
| C | 21" | 2WD | 4.2 km/kWh | 4.6 | 3.8 | 511 km | 553 | 460 | 2,555 kg | **3등급** |
| D | 19" | AWD | 4.1 km/kWh | 4.4 | 3.7 | 501 km | 544 | 449 | 2,630 kg | 4등급 |
| E | 21" | AWD | 4.1 km/kWh | 4.5 | 3.7 | 503 km | 545 | 451 | 2,655 kg | 4등급 |
| F | 21" | AWD | 4.1 km/kWh | 4.4 | 3.7 | 501 km | 544 | 449 | 2,675 kg | 4등급 |

> **핵심 포인트:**
> - 최대 전비: 행A (19" 2WD) — **4.3 km/kWh**, 최대 주행거리 **532 km** (3등급)
> - 3등급 달성 조합: 행A (19" 2WD, 532 km) · 행C (21" 2WD, 511 km)
> - AWD(행D~F) 및 행B 전 조합 4등급 적용
> - 2WD→AWD 전환 시 복합주행거리 약 30~40 km 감소
> - 행B/E/F: 동일 등급(4등급) 내 경쟁 조합 — 배터리·구성 구분 데이터팀 확인 필요

---

## 인승별 공차중량 참조

> raw_line 기준 (DB는 6인승만 저장).

| 행 | 휠·구동 | 6인승 | 7인승 |
|---|---|---|---|
| A | 19" 2WD | 2,510 kg | 2,505 kg |
| B | 19" 2WD | 2,610 kg | 2,605 kg |
| C | 21" 2WD | 2,555 kg | 2,560 kg |
| D | 19" AWD | 2,630 kg | 2,625 kg |
| E | 21" AWD | 2,655 kg | 2,660 kg |
| F | 21" AWD | 2,675 kg | 2,680 kg |

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | 출고가 참고 |
|--------|-----------|
| 익스클루시브 | 71,190,000원 |
| 프레스티지 | 77,150,000원 |
| 캘리그래피 | 82,270,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 아이오닉 9 2027 · 전기 대형 SUV · 19" 2WD 기준 최대 532km(3등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 아이오닉 9(IONIQ 9) 2027년형은 6/7인승 선택이 가능한 플래그십 대형 전기 SUV입니다.
19인치 2WD 기준 전비 4.3 km/kWh, 복합 주행거리 최대 532 km(3등급)를 달성하며,
익스클루시브·프레스티지·캘리그래피 세 가지 트림으로 구성됩니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대(HYUNDAI)
모델: 아이오닉 9(IONIQ 9) 2027년형
연료: 전기(BEV)
인승: 6인승 / 7인승
구동방식: 2WD / AWD
전비(대표·19" 2WD): 4.3 km/kWh (3등급)
주행거리(대표·19" 2WD): 532 km
공차중량: 2,510~2,675 kg (구동·휠·인승 조합별, 6인승 기준)
트림: 익스클루시브·프레스티지·캘리그래피
```

### ④ 인포그래픽·카드 수치 스니펫
```
[19" 2WD-A]  4.3km/kWh | 532km | 2,510kg | 3등급  ← 최대 효율·최장 주행
[21" 2WD-C]  4.2km/kWh | 511km | 2,555kg | 3등급
[19" AWD-D]  4.1km/kWh | 501km | 2,630kg | 4등급
[21" AWD-E]  4.1km/kWh | 503km | 2,655kg | 4등급
※ 공차중량 6인승 기준
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| CO2 배출량 | 전기차 해당 없음 |
| 배터리 용량(kWh) | vehicle_powertrains 미수집 |
| 모터 출력 | vehicle_powertrains 미수집 |
| 충전 속도 / 시간 | 미수집 |
| 배터리 구성 구분 | 동일 휠·구동 행 2건 — 배터리 옵션 미분리 (데이터팀 확인 필요) |

---

_작성: 컨텐츠_  
_작성일: 2026-06-17_  
_data gate: verdict-ioniq9-20260611.md (GREEN) · commit 8877504_
