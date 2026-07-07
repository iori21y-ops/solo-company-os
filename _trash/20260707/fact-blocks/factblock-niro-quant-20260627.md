---
type: fact-block
title: 기아 니로 팩트블록 (quantitative · 2026 · 1.6 HEV)
topic: niro-factblock-quant
subject: 기아 니로 (1.6 하이브리드 HEV · 2026)
date: 2026-06-27
data_source:
  - data/outputs/approved/verdict-niro-20260611.md (quantitative/referential GREEN)
created: 2026-06-27
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-022-factblock-batch-20260627]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-niro-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='niro' (쿼리 2026-06-27, 3행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='niro' (쿼리 2026-06-27, 3행)
data_gate: verdict-niro-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·CO2·공차중량·휠
uncertified: 가격·이미지·에너지등급·구동방식(drive_type null)·배기량(displacement_cc null)·모터출력
flags:
  - "drive_type null 전 행 — FWD(전륜) 추정. 발행 전 원문 확인 권고."
  - "body_type null — 소형 SUV(해치백) 추정. 데이터팀 확인 권고."
  - "model_code null — 미수집."
  - "segment null — 소형 추정."
  - "energy_grade null — 등급 DB 미수집. 연비 기준 추정 발행 금지."
  - "displacement_cc null — 1.6L HEV 추정(engine 텍스트 기반)."
  - "curb_weight_kg null — 행B(16\"/빌트인캠)·행C(18\") DB 미수집."
  - "vehicle_trims 3건(트렌디·프레스티지·시그니처) 전 필드 null — 트림별 제원 매핑 불가."
  - "niro-ev(전기)·niro(플러그인) 별도 slug 존재 여부 확인 권고 — 본 팩트블록은 HEV만."
---

# 니로 팩트 블록 — quantitative (기아 · 2026 · 1.6 HEV)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-niro-20260611 GREEN).  
> 인증 범위: 연비(km/L)·CO2·공차중량·휠.  
> ※ 에너지등급 null, 구동방식 null(FWD 추정). 본 팩트블록은 HEV(하이브리드) 전용.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| drive_type | ⚠️ null 전 행 | FWD(전륜) 추정. 발행 전 원문 확인 권고. |
| energy_grade | ⚠️ null | DB 미수집. 추정값 발행 금지. |
| body_type | ⚠️ null | 소형 SUV(해치백) 추정. 데이터팀 확인 권고. |
| curb_weight_kg | ⚠️ null(행B·C) | 16"빌트인캠·18" 공차중량 미수집. |
| displacement_cc | ℹ️ null | 1.6L HEV 추정(engine 텍스트 기반). |
| vehicle_trims | ℹ️ null 전 행 | 트림별 제원 매핑 불가. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 기아 (Kia) | vehicles.brand |
| 모델명 | 니로 | vehicles.name |
| 모델코드 | null (미수집) | vehicles.model_code |
| 연식 | 2026 | vehicles.year |
| 세그먼트 | null (소형 추정) | vehicles.segment |
| 차체 형태 | null (소형 SUV/해치백 추정) | vehicles.body_type |
| 연료 | 하이브리드 (HEV) | vehicle_powertrains.fuel_kind |
| 엔진 | 1.6 하이브리드 | vehicle_powertrains.engine |
| 구동 | null (FWD 추정) | vehicle_powertrains.drive_type |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> drive_type 전 행 null (FWD 추정).  
> curb_weight_kg null 행은 공차중량 발행 금지.

### 스마트스트림 1.6 하이브리드 (1.6 HEV)

| 행 | 휠 | 비고 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 |
|---|---|---|---|---|---|---|---|
| A | 16" | 표준 | **20.2 km/L** | 21.4 | 18.8 | 76 g/km | **1,450 kg** |
| B | 16" | 빌트인 캠 | 19.4 km/L | 20.1 | 18.6 | 80 g/km | null (미수집) |
| C | 18" | 표준 | 19.4 km/L | 20.6 | 18.1 | 80 g/km | null (미수집) |

> **핵심 포인트:**
> - 행A (16" 표준): 최고 연비 **20.2 km/L**, CO2 **76 g/km** (세 조합 중 최저)
> - 빌트인 캠(행B): 20.2→19.4 km/L (−0.8 km/L), CO2 76→80 g/km
> - 18"(행C): 연비 19.4 km/L(빌트인 캠과 동일), 도심 20.6으로 16"빌트인캠(20.1)보다 높으나 고속 18.1로 낮음
> - 에너지등급 null — DB 미수집, 추정 발행 금지

---

## 연비 요약

| 휠 | 구동 | 비고 | 연비(복합) | CO2 | 공차중량 | 에너지등급 |
|----|------|------|-----------|-----|---------|-----------|
| 16" | FWD 추정 | 표준 | **20.2 km/L** | 76 g/km | 1,450 kg | null |
| 16" | FWD 추정 | +빌트인 캠 | 19.4 km/L | 80 g/km | null | null |
| 18" | FWD 추정 | 표준 | 19.4 km/L | 80 g/km | null | null |

---

## 트림 라인업 (vehicle_trims)

| 트림 | 비고 |
|------|------|
| 트렌디 | — |
| 프레스티지 | — |
| 시그니처 | — |

> ⚠️ fuel_type·drive_type·wheel_size·fuel_eff 전 필드 null — 트림별 제원 매핑 불가.  
> 트림 가격은 verdict 인증 범위 외 → 미포함.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
기아 니로 HEV 2026 · 16" 복합 연비 20.2km/L · CO2 76g/km
```

### ② 블로그 소개 단락용 (2~3문장)
```
기아 니로(2026) 하이브리드는 1.6 HEV 파워트레인을 탑재한 소형 SUV로, 16인치 기준 복합 연비 20.2 km/L·CO2 76 g/km를 달성합니다.
빌트인 캠 장착 시 19.4 km/L(CO2 80 g/km)로 하락하며, 18인치 선택 시에도 동일하게 19.4 km/L입니다.
에너지등급은 DB 미수집으로 별도 확인이 필요합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 기아(Kia)
모델: 니로 HEV (2026)
세그먼트: 소형 (segment null, 추정)
차체: 소형 SUV/해치백 추정 (body_type null, 원문 확인 권고)
연료: 하이브리드(HEV)
엔진: 1.6 하이브리드 (displacement_cc null, 1.6L 추정)
구동방식: FWD 추정 (drive_type DB null — 원문 확인 필요)
연비(16" 표준): 복합 20.2 km/L | 도심 21.4 | 고속 18.8 | CO2 76g/km | 공차 1,450kg
연비(16" 빌트인캠): 복합 19.4 km/L | 도심 20.1 | 고속 18.6 | CO2 80g/km
연비(18"): 복합 19.4 km/L | 도심 20.6 | 고속 18.1 | CO2 80g/km
에너지등급: null (DB 미수집 — 발행 금지)
트림: 트렌디 / 프레스티지 / 시그니처
```

### ④ 인포그래픽·카드 수치 스니펫
```
[16" FWD추정·표준]       20.2km/L | CO2 76g/km | 1,450kg
[16" FWD추정·빌트인캠]   19.4km/L | CO2 80g/km | 공차 미수집
[18" FWD추정·표준]       19.4km/L | CO2 80g/km | 공차 미수집
※ 에너지등급 null — 발행 금지 / drive_type null(FWD 추정) — 원문 확인 권고
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 에너지등급 | DB null — 추정값 발행 금지 |
| 구동방식 확정값 | drive_type null — FWD 추정, 원문 확인 권고 |
| 배기량 확정값 | displacement_cc null — 1.6L HEV 추정 |
| 공차중량(행B·C) | curb_weight_kg null — 미포함 |
| 모터 출력·배터리 용량 | vehicle_powertrains 미수집 |
| 트림별 제원 상세 | vehicle_trims null 전 행 |
| 전기(EV) 모델 | niro-ev 별도 팩트블록 대상 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-27_  
_data gate: verdict-niro-20260611.md (GREEN) · commit 8877504_
