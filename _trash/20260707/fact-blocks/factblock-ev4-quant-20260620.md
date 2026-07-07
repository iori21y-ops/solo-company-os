---
type: fact-block
title: 기아 EV4 팩트블록 (quantitative · 2026년형 · 전기)
topic: ev4-factblock-quant
subject: 기아 EV4 (2026년형 · 소형 전기 세단 · 스탠다드/롱레인지 · 2WD/4WD)
date: 2026-06-20
data_source:
  - data/outputs/approved/verdict-ev4-20260611.md (quantitative/referential GREEN)
created: 2026-06-20
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-013-factblock-batch-20260620]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-ev4-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='ev4' (쿼리 2026-06-20, 6행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='ev4' (쿼리 2026-06-20, 6행)
data_gate: verdict-ev4-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 전비(복합)·주행거리(복합)·공차중량·에너지등급·구동방식·휠
uncertified: 가격·이미지·CO2(전기차 해당없음)·배터리용량(단위불명)·도심/고속 전비·도심/고속 주행거리·안전등급
flags:
  - "vehicles.body_type null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.segment null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.category null — DB 미입력. 데이터팀 보완 권고."
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "CO2 null — 전기차 해당 없음(정상)."
  - "displacement_cc null — 전기차 해당 없음(정상)."
  - "fuel_eff_combined/city/highway null — 전기차 전비(electric_eff)로 대체. DB 컬럼 구분 정상."
  - "raw_line 내 '369/158.2'(스탠다드)·'343/237.3'(롱레인지) 수치 단위 불명확 — 배터리 관련 수치 추정. 발행 시 사용 금지, 데이터팀 확인 권고."
  - "롱레인지 2WD 19\" 2행 존재(일반 19\": 502km/5.5효율 vs GT-Line 19\": 495km/5.4효율) — 타이어/세팅 차이로 추정."
  - "도심/고속 전비·주행거리: DB 컬럼 미추출, raw_line에서 확인. 이 팩트블록 raw_line 파생 수치는 '참고용'으로만 표기."
  - "vehicle_trims.base_price 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# EV4 팩트 블록 — quantitative (2026년형 · 소형 전기)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-ev4-20260611 GREEN).  
> 인증 범위(DB): 전비(복합)·주행거리(복합)·공차중량·에너지등급·구동방식·휠.  
> CO2·displacement_cc null — 전기차이므로 정상. raw_line 내 배터리 관련 수치(369/158.2, 343/237.3) 단위 불명확 → 발행 시 배터리 용량 수치 사용 금지.  
> 도심/고속 전비·주행거리는 DB 컬럼 미추출 — raw_line 참조값이므로 '참고용' 표기.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| body_type / segment / category | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| model_code | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| CO2 | ℹ️ null | 전기차 해당 없음 (정상). |
| 배터리 용량 수치 | ⚠️ 단위 불명확 | raw_line '369/158.2'(스탠다드)·'343/237.3'(롱레인지). 사용 금지. |
| 롱레인지 2WD 19" 2행 | ℹ️ 참고 | 일반 19"(502km·5.5효율)과 GT-Line 19"(495km·5.4효율) 별도 행. |
| 가격 데이터 | 📌 참고용 | vehicle_trims.base_price 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 기아 | vehicles.brand |
| 모델명 | EV4 | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | — (null, 소형 추정) | vehicles.segment |
| 카테고리 | — (null, EV) | vehicles.category |
| 연료 | 전기 | vehicle_powertrains.fuel_kind |
| 배기량 | — (전기차) | vehicle_powertrains.displacement_cc |
| 배터리 구성 | 스탠다드 / 롱레인지 | 2종 |
| 구동 | 2WD (스탠다드·롱레인지) / 4WD (롱레인지) | — |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> 전비(복합)·주행거리(복합)·공차중량·에너지등급: **DB 인증값**.  
> 도심/고속 전비·주행거리: **raw_line 파생 참고값** (별도 표기).

### 스탠다드 배터리

| 행 | 구동 | 휠 | 주행거리(복합) | 전비(복합) | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|
| A | **2WD** | **17"** | **382 km** | **5.8 km/kWh** | **1,745 kg** | **1등급** |
| B | **2WD** | **19"** | **354 km** | **5.4 km/kWh** | **1,760 kg** | **2등급** |

<details>
<summary>스탠다드 도심/고속 상세 (raw_line 참고값)</summary>

| 행 | 구동 | 휠 | 주행거리(도심) | 주행거리(고속) | 전비(도심) | 전비(고속) |
|---|---|---|---|---|---|---|
| A | 2WD | 17" | 404 km | 354 km | 6.2 km/kWh | 5.3 km/kWh |
| B | 2WD | 19" | 373 km | 330 km | 5.7 km/kWh | 5.0 km/kWh |

</details>

### 롱레인지 배터리

| 행 | 구동 | 휠 | 주행거리(복합) | 전비(복합) | 공차중량 | 에너지등급 | 비고 |
|---|---|---|---|---|---|---|---|
| C | **2WD** | **17"** | **533 km** | **5.8 km/kWh** | **1,835 kg** | **1등급** | — |
| D | **2WD** | **19"** | **502 km** | **5.5 km/kWh** | **1,850 kg** | **2등급** | — |
| E | **2WD** | **19"** | **495 km** | **5.4 km/kWh** | **1,850 kg** | **2등급** | GT-Line |
| F | **4WD** | **19"** | **475 km** | **5.1 km/kWh** | **1,940 kg** | **2등급** | — |

<details>
<summary>롱레인지 도심/고속 상세 (raw_line 참고값)</summary>

| 행 | 구동 | 휠 | 주행거리(도심) | 주행거리(고속) | 전비(도심) | 전비(고속) |
|---|---|---|---|---|---|---|
| C | 2WD | 17" | 567 km | 491 km | 6.2 km/kWh | 5.3 km/kWh |
| D | 2WD | 19" | 537 km | 458 km | 5.9 km/kWh | 5.0 km/kWh |
| E | 2WD | 19" (GT-Line) | 527 km | 455 km | 5.8 km/kWh | 4.9 km/kWh |
| F | 4WD | 19" | 497 km | 448 km | 5.3 km/kWh | 4.8 km/kWh |

</details>

> **핵심 포인트:**
> - 롱레인지 2WD 17" 최대 주행거리 533km (1등급) — 기아 소형 EV 라인업 중 최장
> - 스탠다드 17"(1등급) vs 19"(2등급): 주행거리 28km 차이, 전비 0.4 하락
> - 롱레인지 19" GT-Line: 일반 19" 대비 7km 단축, 전비 0.1 하락 (타이어/세팅 차이 추정)
> - 롱레인지 4WD 선택 시 주행거리 475km(2WD 19" 대비 -27km), 공차중량 90kg 증가

---

## 배터리별 핵심 비교

| 항목 | 스탠다드 최고 | 롱레인지 최고 | 차이 |
|------|------------|-------------|------|
| 최대 주행거리 | 382 km (2WD 17") | 533 km (2WD 17") | +151 km |
| 최대 전비 | 5.8 km/kWh | 5.8 km/kWh | 동일 |
| 에너지등급 (최고) | 1등급 | 1등급 | 동일 |
| 공차중량(최저) | 1,745 kg | 1,835 kg | +90 kg |

---

## 트림 라인업 (vehicle_trims · 가격 참고용)

> ⚠️ 가격(base_price)은 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수.

| 트림명 | 출고가 참고 |
|--------|-----------|
| 에어 스탠다드 | 42,570,000원 |
| 어스 스탠다드 | 47,410,000원 |
| GT-Line 스탠다드 | 48,570,000원 |
| 에어 롱레인지 | 47,000,000원 |
| 어스 롱레인지 | 51,830,000원 |
| GT-Line 롱레인지 | 52,990,000원 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
기아 EV4 2026 · 전기 · 롱레인지 최대 533km (1등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
기아 EV4 2026년형은 스탠다드·롱레인지 2종 배터리를 제공하는 소형 전기차입니다.
롱레인지 2WD 17" 기준 최대 주행거리 533km(전비 5.8km/kWh, 1등급),
스탠다드 2WD 17" 기준 382km(전비 5.8km/kWh, 1등급)이며, 4WD는 롱레인지에서만 제공됩니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 기아
모델: EV4 2026년형
연료: 전기
배터리: 스탠다드 / 롱레인지

[스탠다드]
주행거리: 최대 382km (2WD 17" 기준)
전비: 5.8km/kWh (복합, 17") / 5.4km/kWh (복합, 19")
에너지등급: 1등급(17") / 2등급(19")
공차중량: 1,745kg (17") / 1,760kg (19")

[롱레인지 2WD]
주행거리: 최대 533km (17" 기준)
전비: 5.8km/kWh (복합, 17") / 5.5km/kWh (복합, 19")
에너지등급: 1등급(17") / 2등급(19")
공차중량: 1,835kg (17") / 1,850kg (19")
※ GT-Line 19": 주행거리 495km, 전비 5.4km/kWh

[롱레인지 4WD]
주행거리: 475km (19" 기준)
전비: 5.1km/kWh (복합)
에너지등급: 2등급
공차중량: 1,940kg
```

### ④ 인포그래픽·카드 수치 스니펫
```
[스탠다드 2WD 17"]  382km | 5.8km/kWh | 1,745kg | 1등급
[스탠다드 2WD 19"]  354km | 5.4km/kWh | 1,760kg | 2등급
[롱레인지 2WD 17"]  533km | 5.8km/kWh | 1,835kg | 1등급  ← 최장 주행거리
[롱레인지 2WD 19"]  502km | 5.5km/kWh | 1,850kg | 2등급
[롱레인지 4WD 19"]  475km | 5.1km/kWh | 1,940kg | 2등급
※ 주행거리·전비 복합 기준 / 배터리 용량 수치 사용 금지(단위 미확인)
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 배터리 용량 (kWh) | raw_line 내 수치 단위 불명확 — 데이터팀 확인 권고 |
| 모터 출력 (kW) | 미수집 |
| 충전 시간 | 미수집 |
| 안전 등급 | 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-20_  
_data gate: verdict-ev4-20260611.md (GREEN) · commit 8877504_
