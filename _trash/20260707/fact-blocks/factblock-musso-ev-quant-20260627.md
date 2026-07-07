---
type: fact-block
title: KGM 무쏘 EV 팩트블록 (quantitative · 2026)
topic: musso-ev-factblock-quant
subject: KGM 무쏘 EV (전기 픽업트럭 · 2026)
date: 2026-06-27
data_source:
  - data/outputs/approved/verdict-musso-ev-20260611.md (quantitative/referential GREEN)
created: 2026-06-27
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-022-factblock-batch-20260627]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-musso-ev-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='musso-ev' (쿼리 2026-06-27, 2행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='musso-ev' (쿼리 2026-06-27, 2행)
data_gate: verdict-musso-ev-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 전비·1회충전주행거리·공차중량·배터리 정격전압·용량(raw_line)
uncertified: 가격·이미지·모터출력·에너지등급·휠·구동방식(drive_type raw_line 기반)
flags:
  - "body_type null — 픽업트럭 추정. 데이터팀 확인 권고."
  - "wheel null 전 행 — DB·raw_line 미기재. 발행 금지."
  - "energy_grade null — 전기차 별도 고시(정상). 발행 자제."
  - "배터리 수치(371V·217Ah)는 raw_line 기반 — kWh 환산값 발행 금지(표준 환산식 미확인)."
  - "vehicle_trims MX·T2 전 필드 null — 트림별 제원 매핑 불가."
  - "drive_type은 raw_line 기반(2WD·AWD) — DB fuel_eff_combined/city/highway null, electric_eff만 수집."
---

# 무쏘 EV 팩트 블록 — quantitative (KGM · 2026 · 전기)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-musso-ev-20260611 GREEN).  
> 인증 범위: 전비(km/kWh)·1회충전주행거리(km)·공차중량(kg)·배터리 정격전압/용량(raw_line).  
> ※ fuel_eff_combined/city/highway DB null — electric_eff·driving_range 필드에서 추출.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| body_type | ⚠️ null | 픽업트럭 추정. 데이터팀 확인 권고. |
| wheel | ⚠️ null 전 행 | DB·raw_line 미기재. 발행 금지. |
| energy_grade | ℹ️ null | 전기차 별도 고시(정상). 발행 자제. |
| 배터리 kWh | ⚠️ raw_line 한정 | 371V·217Ah 기재 — kWh 환산 발행 금지. |
| vehicle_trims | ℹ️ null 전 행 | 트림별 제원 매핑 불가. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | KGM | vehicles.brand |
| 모델명 | 무쏘 EV | vehicles.name |
| 모델코드 | null (미수집) | vehicles.model_code |
| 연식 | 2026 | vehicles.year |
| 세그먼트 | null (미수집) | vehicles.segment |
| 차체 형태 | null (픽업트럭 추정) | vehicles.body_type |
| 연료 | 전기 (EV) | vehicle_powertrains.fuel_kind |
| 구동 | 2WD / AWD (raw_line 기반) | vehicle_powertrains.raw_line |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> drive_type DB 필드 기재(2WD·AWD)는 raw_line 기반 파싱값.  
> fuel_eff_combined/city/highway null — electric_eff·driving_range 필드에서 전비·주행거리 추출.

### 전기 (EV)

| 행 | 구동 | 전비(복합) | 전비(도심) | 전비(고속) | 1회충전(복합) | 1회충전(도심) | 1회충전(고속) | 공차중량 | 배터리 |
|---|---|---|---|---|---|---|---|---|---|
| A | **2WD** | **4.2 km/kWh** | 4.6 | 3.8 | **400 km** | 434 km | 358 km | 2,155 kg | 371V · 217Ah |
| B | **AWD** | **3.4 km/kWh** | 3.7 | 3.2 | **340 km** | 361 km | 313 km | 2,275 kg | 371V · 217Ah |

> **핵심 포인트:**
> - 2WD 대비 AWD: 전비 −0.8 km/kWh, 1회충전 −60 km, 공차중량 +120 kg
> - 배터리 정격전압·용량 동일(371V·217Ah) — raw_line 기반 표기, kWh 환산값 발행 금지
> - 2WD 복합 400km: 전기 픽업트럭 기준 중거리 주행 가능

---

## 전비·주행거리 요약

| 구동 | 전비(복합) | 1회충전(복합) | 공차중량 | 에너지등급 |
|------|-----------|-------------|---------|-----------|
| 2WD | **4.2 km/kWh** | **400 km** | 2,155 kg | 별도 고시 |
| AWD | 3.4 km/kWh | 340 km | 2,275 kg | 별도 고시 |

---

## 트림 라인업 (vehicle_trims)

| 트림 | 비고 |
|------|------|
| MX | — |
| T2 | — |

> ⚠️ fuel_type·drive_type·wheel_size·fuel_eff 전 필드 null — 트림별 제원 매핑 불가.  
> 트림 가격은 verdict 인증 범위 외 → 미포함.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
KGM 무쏘 EV · 2WD 전비 4.2km/kWh · 1회충전 400km · 전기 픽업트럭 2026
```

### ② 블로그 소개 단락용 (2~3문장)
```
KGM 무쏘 EV(2026)는 국내 대표 전기 픽업트럭으로, 2WD 기준 복합 전비 4.2 km/kWh·1회충전 400 km(복합)를 달성합니다.
AWD 모델은 전비 3.4 km/kWh·1회충전 340 km이며, 공차중량은 2WD 2,155 kg / AWD 2,275 kg입니다.
배터리는 정격 371V·217Ah로 두 구동계 동일 구성입니다(kWh 환산값 별도 확인 필요).
```

### ③ 상담 자료용 (항목형)
```
브랜드: KGM
모델: 무쏘 EV (2026)
차체: 픽업트럭 추정 (body_type null, 원문 확인 권고)
연료: 전기(EV)
배터리: 371V · 217Ah (raw_line 기준, kWh 환산 미확인)
전비(2WD): 복합 4.2 km/kWh | 도심 4.6 | 고속 3.8
전비(AWD): 복합 3.4 km/kWh | 도심 3.7 | 고속 3.2
1회충전(2WD): 복합 400 km | 도심 434 | 고속 358
1회충전(AWD): 복합 340 km | 도심 361 | 고속 313
공차중량: 2WD 2,155 kg / AWD 2,275 kg
트림: MX / T2 (트림별 제원 매핑 불가)
```

### ④ 인포그래픽·카드 수치 스니펫
```
[2WD] 전비 4.2km/kWh | 1회충전 400km | 2,155kg
[AWD] 전비 3.4km/kWh | 1회충전 340km | 2,275kg
배터리: 371V·217Ah (kWh 환산 발행 금지)
※ 에너지등급·휠 미수집 — 발행 전 확인 필수
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 에너지등급 | 전기차 별도 고시 (DB null 정상) |
| 휠 | DB·raw_line 미기재 |
| 모터 출력 | vehicle_powertrains 미수집 |
| 트림별 제원 | vehicle_trims null 전 행 |
| 배터리 kWh | 환산 기준 미확인 — 발행 금지 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-27_  
_data gate: verdict-musso-ev-20260611.md (GREEN) · commit 8877504_
