---
type: fact-block
title: KGM 무쏘 팩트블록 (quantitative · 2026 · 디젤/가솔린 픽업트럭)
topic: musso-factblock-quant
subject: KGM 무쏘 (2,157cc 디젤 · 1,998cc 가솔린 · 픽업트럭 추정)
date: 2026-06-26
data_source:
  - data/outputs/approved/verdict-musso-20260611.md (quantitative/referential GREEN)
created: 2026-06-26
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-021-factblock-batch-20260626]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-musso-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='musso' (쿼리 2026-06-26, 17행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='musso' (쿼리 2026-06-26, 3행: M5/M9/T3)
data_gate: verdict-musso-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·CO2·공차중량·휠·에너지등급
uncertified: 가격·이미지·구동방식(일부 null)·트림-바리에이션 매핑
flags:
  - "vehicles.body_type null — 픽업트럭 추정(스탠다드/롱/XL/그랜드 스타일 variant). 데이터팀 보완 권고."
  - "vehicles.segment null — 데이터팀 보완 권고."
  - "vehicles.model_code null — 데이터팀 보완 권고."
  - "engine 컬럼 파싱 오류 심각 — variant명·휠 정보 혼입(예: engine='롱 18/', '무쏘 17/18/'). raw_line이 신뢰 소스."
  - "drive_type null 일부 행 — 2WD 추정. 발행 전 원문 확인 권고."
  - "17\" 기본 디젤 2행 수치 상이 (복합 9.8 vs 10.1, 공차 2,175 vs 2,055 kg) — 별도 구성 추정. 데이터팀 확인 필요."
  - "롱 4WD 디젤 2행 수치 상이 (복합 9.6/9.8, CO2 204/200, 공차 2,180/2,175 kg) — 중복 또는 별도 구성. 데이터팀 확인 필요."
  - "vehicle_trims(M5/M9/T3) ↔ variant(스탠다드/롱/XL/그랜드 스타일) 매핑 미확인."
---

# 무쏘 팩트 블록 — quantitative (2026 · 디젤/가솔린 픽업)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-musso-20260611 GREEN).  
> 인증 범위: 연비(km/L)·CO2·공차중량·휠·에너지등급.  
> ⚠️ engine 컬럼 파싱 오류 — 이 팩트블록은 raw_line 기준으로 정리.  
> ※ 무쏘 EV(전기)는 slug='musso-ev' 별도 팩트블록 참조.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| body_type | ⚠️ null | 픽업트럭 추정 (스탠다드/롱/XL/그랜드 스타일). 데이터팀 보완 권고. |
| segment | ⚠️ null | 데이터팀 보완 권고. |
| model_code | ℹ️ null | 데이터팀 보완 권고. |
| engine 컬럼 | ⚠️ 파싱 오류 | variant명·휠 정보 혼입. raw_line 기준 정리 필수. |
| drive_type | ⚠️ 일부 null | null 행은 2WD 추정. 원문 확인 권고. |
| 17" 디젤 2행 | ⚠️ 수치 상이 | 복합 9.8 vs 10.1 km/L, 공차 2,175 vs 2,055 kg — 별도 구성 추정. 데이터팀 확인 필요. |
| 롱 4WD 디젤 2행 | ⚠️ 중복 의심 | 복합 9.6/9.8 km/L — 중복 또는 별도 구성. 데이터팀 확인 필요. |
| 트림↔variant 매핑 | ⚠️ 미확인 | M5/M9/T3 ↔ 스탠다드/롱/XL/그랜드 스타일 연결 불명확. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | KGM (쌍용 → KGM) | vehicles.brand |
| 모델명 | 무쏘 | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | 2026 | vehicles.year |
| 세그먼트 | — (null, 픽업트럭 추정) | vehicles.segment |
| 차체 형태 | — (null, 픽업트럭 추정) | vehicles.body_type |
| 연료 | 디젤 (2,157cc) / 가솔린 (1,998cc) | vehicle_powertrains.fuel_kind |

---

## 제원 매트릭스 — 17" 구성 (vehicle_powertrains · GREEN 인증)

> raw_line 기준 정리. engine 컬럼 신뢰 불가.  
> drive_type 전 행 null (2WD 추정 — 원문 확인 필요).

### 디젤 2,157cc (17")

| 행 | 휠 | variant | 구동 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|---|
| A | 17" | 기본형 | null(2WD추정) | **9.8 km/L** | 9.2 | 10.5 | 200 g/km | 2,175 kg | **4등급** |
| B | 17" | 기본형 (별도구성 추정) | null(2WD추정) | **10.1 km/L** | 9.2 | 11.3 | 194 g/km | 2,055 kg | **4등급** |
| C | 17" | XL | null(2WD추정) | 9.5 km/L | 9.0 | 10.1 | 206 g/km | 2,290 kg | **4등급** |

> ⚠️ 행A·B 동일 variant로 보이나 수치 상이(연비 9.8 vs 10.1, 공차중량 2,175 vs 2,055 kg) — 별도 구성 추정. 데이터팀 확인 필요.

### 가솔린 1,998cc (17")

| 행 | 휠 | variant | 구동 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|---|
| D | 17" | XL | null(2WD추정) | **7.6 km/L** | 6.9 | 8.7 | 225 g/km | 2,230 kg | **5등급** |
| E | 17" | 기본형 (null) | null(2WD추정) | **8.6 km/L** | 7.7 | 9.9 | 195 g/km | 1,955 kg | **5등급** |

---

## 제원 매트릭스 — 18/20" 구성 (vehicle_powertrains · GREEN 인증)

> raw_line 내 "18/20인치" 병기 → DB wheel 컬럼에 "20\"" 로 파싱됨.

### 디젤 2,157cc (18/20")

| 행 | 휠 | variant | 구동 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|---|
| F | 18/20" | 무쏘 기본 2WD | 2WD | **10.0 km/L** | 9.1 | 11.2 | 196 g/km | 2,055 kg | **4등급** |
| G | 18/20" | 스탠다드 | null(2WD추정) | **9.8 km/L** | 9.0 | 10.8 | 200 g/km | 2,060 kg | **4등급** |
| H | 17/18/20" | 무쏘 4WD | 4WD | **9.8 km/L** | 9.3 | 10.4 | 199 g/km | 2,160 kg | **4등급** |
| I | 18/20" | 그랜드 스타일 4WD | 4WD | **10.0 km/L** | 9.4 | 10.8 | 195 g/km | 2,160 kg | **4등급** |
| J① | 18/20" | 롱 4WD | 4WD | 9.6 km/L | 9.1 | 10.2 | 204 g/km | 2,180 kg | **4등급** |
| J② | 18/20" | 롱 4WD (중복의심) | 4WD | 9.8 km/L | 9.2 | 10.6 | 200 g/km | 2,175 kg | **4등급** |

> ⚠️ 행J①·J② 동일 raw_line prefix(롱 4WD 18/20") 수치 상이 — 중복 또는 별도 구성. 발행 전 데이터팀 확인 필수.

### 가솔린 1,998cc (18/20")

| 행 | 휠 | variant | 구동 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|---|
| K | 18/20" | 무쏘 기본 2WD | 2WD | **8.3 km/L** | 7.5 | 9.5 | 206 g/km | 1,955 kg | **5등급** |
| L | 18/20" | 스탠다드 | null(2WD추정) | **8.2 km/L** | 7.4 | 9.3 | 204 g/km | 1,960 kg | **5등급** |
| M | 17/18/20" | 4WD (기본) | 4WD | **7.9 km/L** | 7.1 | 9.1 | 212 g/km | 2,070 kg | **5등급** |
| N | 17/18/20" | (별도, drive null) | null(2WD추정) | **7.7 km/L** | 7.1 | 8.6 | 218 g/km | 2,120 kg | **5등급** |
| O | 18/20" | 그랜드 스타일 4WD | 4WD | **8.1 km/L** | 7.3 | 9.2 | 211 g/km | 2,070 kg | **5등급** |
| P | 18/20" | 롱 4WD | 4WD | **7.8 km/L** | 7.1 | 8.9 | 215 g/km | 2,120 kg | **5등급** |

> ⚠️ 행M(4WD 17/18/20")·행N(drive null 17/18/20") 연비 상이(7.9 vs 7.7) — 4WD vs 2WD 구성 추정.

---

## 연비 요약 (디젤 vs 가솔린 · 대표값)

| 연료 | variant | 구동 | 최고 연비 | 최저 연비 | 에너지등급 |
|------|---------|------|----------|----------|-----------|
| 디젤 2,157cc | 그랜드 스타일 4WD(18/20") | 4WD | 10.0 km/L | — | 4등급 |
| 디젤 2,157cc | 기본형(17") 추정 | 2WD추정 | 10.1 km/L | 9.5 km/L | 4등급 |
| 가솔린 1,998cc | 기본형(17") | 2WD추정 | 8.6 km/L | — | 5등급 |
| 가솔린 1,998cc | 기본형 2WD(18/20") | 2WD | 8.3 km/L | — | 5등급 |
| 가솔린 1,998cc | 롱 4WD | 4WD | 7.8 km/L | — | 5등급 |

> 디젤이 가솔린 대비 연비 약 1.5~2.0 km/L 우세.  
> ⚠️ variant별 확정 매핑 전 단일 수치 발행 금지.

---

## 트림 라인업 (vehicle_trims)

| 트림 | 비고 |
|------|------|
| M5 | — |
| M9 | — |
| T3 | — |

> ⚠️ drive_type·wheel_size·fuel_eff null 전 행 — 트림별 제원 매핑 불가.  
> M5/M9/T3 ↔ 스탠다드/롱/XL/그랜드 스타일 연결 미확인.  
> 트림 가격은 verdict 인증 범위 외 → 미포함.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
KGM 무쏘 2026 · 디젤 2.2L / 가솔린 2.0L · 픽업트럭 · 디젤 복합 최대 10.1km/L(4등급)
```

### ② 블로그 소개 단락용 (2~3문장)
```
KGM 무쏘(2026년형)는 2,157cc 디젤과 1,998cc 가솔린 두 가지 엔진을 제공하는 픽업트럭입니다.
스탠다드·롱·XL·그랜드 스타일 variant와 2WD/4WD 조합으로 운용되며,
디젤 기준 복합 연비 최대 10.1 km/L(4등급), 가솔린 기준 최대 8.6 km/L(5등급) 수준입니다.
※ variant-트림 매핑 미확인으로 단일 수치 인용 시 데이터팀 확인 필요.
```

### ③ 상담 자료용 (항목형)
```
브랜드: KGM
모델: 무쏘 (2026년형)
차체: 픽업트럭 추정 (body_type DB null)
연료: 디젤(2,157cc) / 가솔린(1,998cc)
variant: 스탠다드 / 롱 / XL / 그랜드 스타일
구동: 2WD / 4WD (drive_type null 행 일부 → 2WD 추정)
디젤 연비(대표·2WD): 9.8~10.1 km/L | CO2 194~200 g/km | 4등급
디젤 연비(대표·4WD): 9.6~10.0 km/L | CO2 195~204 g/km | 4등급
가솔린 연비(대표·2WD): 8.2~8.6 km/L | CO2 195~206 g/km | 5등급
가솔린 연비(대표·4WD): 7.8~8.1 km/L | CO2 211~215 g/km | 5등급
트림: M5 / M9 / T3
※ variant-트림 매핑 미확인. 단일 수치 인용 전 데이터팀 확인 필수.
```

### ④ 인포그래픽·카드 수치 스니펫
```
[디젤 2WD 17"] 기본 9.8~10.1km/L | CO2 194~200g/km | 4등급  ※ 2행 수치 상이, 확인 필요
[디젤 2WD 18/20"] 스탠다드 9.8 / 기본 10.0 km/L | 4등급
[디젤 4WD 18/20"] 무쏘 9.8 / 롱 9.6~9.8 / 그랜드 10.0 km/L | 4등급
[가솔린 2WD 17"] 기본 8.6 / XL 7.6 km/L | 5등급
[가솔린 2WD 18/20"] 기본 8.3 / 스탠다드 8.2 km/L | 5등급
[가솔린 4WD 18/20"] 롱 7.8 / 그랜드 8.1 km/L | 5등급
※ variant-트림 매핑 미확인. 발행 전 데이터팀 확인 필수.
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 차체 형태 확정 | body_type null |
| 구동방식 확정 (일부) | drive_type null 행 존재 |
| 트림-variant 매핑 | M5/M9/T3 ↔ 스탠다드/롱/XL/그랜드 스타일 미확인 |
| 최고출력·토크 | vehicle_powertrains 미수집 |
| 변속기 정보 | vehicle_powertrains 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-26_  
_data gate: verdict-musso-20260611.md (GREEN) · commit 8877504_
