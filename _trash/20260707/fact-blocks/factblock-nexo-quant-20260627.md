---
type: fact-block
title: 현대 넥쏘 팩트블록 (quantitative · 2026 · 수소전기)
topic: nexo-factblock-quant
subject: 현대 넥쏘 디 올 뉴 (수소전기 SUV · 2026)
date: 2026-06-27
data_source:
  - data/outputs/approved/verdict-nexo-20260611.md (quantitative/referential GREEN)
created: 2026-06-27
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-022-factblock-batch-20260627]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-nexo-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='nexo' (쿼리 2026-06-27, 3행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='nexo' (쿼리 2026-06-27, 2행)
data_gate: verdict-nexo-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 수소효율(km/kg)·공차중량·휠
uncertified: 가격·이미지·에너지등급·1회충전거리·구동방식(drive_type null)·모터출력
flags:
  - "drive_type null 전 행 — FWD(전륜) 추정. 발행 전 원문 확인 권고."
  - "model_code null — 모델코드 미수집."
  - "segment null — 소형 SUV 추정."
  - "energy_grade null — 수소차 별도 고시(정상). 발행 자제."
  - "driving_range null — DB·raw_line 미기재. 1회충전거리 발행 금지."
  - "vehicle_trims 2건(익스클루시브·프레스티지) 전 필드 null — 트림별 제원 매핑 불가."
  - "수소효율 도심·고속 수치는 raw_line 기반 파싱값 — DB fuel_eff_city/highway null, hydrogen_eff(복합)만 수집."
---

# 넥쏘 팩트 블록 — quantitative (현대 · 2026 · 수소전기)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-nexo-20260611 GREEN).  
> 인증 범위: 수소효율(km/kg)·공차중량(kg)·휠 인치.  
> ※ 도심·고속 수소효율은 raw_line 기반 — 참고용으로만 사용, 발행 시 "(raw_line 기반)" 병기 권고.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| drive_type | ⚠️ null 전 행 | FWD(전륜) 추정. 발행 전 원문 확인 권고. |
| energy_grade | ℹ️ null | 수소차 별도 고시(정상). 발행 자제. |
| driving_range | ⚠️ null | DB·raw_line 1회충전거리 미기재. 발행 금지. |
| model_code | ℹ️ null | 미수집. |
| vehicle_trims | ℹ️ null 전 행 | 트림별 제원 매핑 불가. |
| 도심·고속 효율 | ℹ️ raw_line | fuel_eff_city/highway null — raw_line 기반 참고값. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (Hyundai) | vehicles.brand |
| 모델명 | 넥쏘 (디 올 뉴 넥쏘) | vehicles.name |
| 모델코드 | null (미수집) | vehicles.model_code |
| 연식 | 2026 | vehicles.year |
| 세그먼트 | null (미수집) | vehicles.segment |
| 차체 형태 | SUV | vehicles.body_type |
| 연료 | 수소전기 (hydrogen) | vehicle_powertrains.fuel_kind |
| 구동 | null (FWD 추정) | vehicle_powertrains.drive_type |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> drive_type 전 행 null (FWD 추정).  
> 도심·고속 수소효율은 raw_line 기반 참고값 — 발행 시 출처 명시 권고.

### 수소전기 (hydrogen)

| 행 | 휠 | 비고 | 수소효율(복합) | 수소효율(도심) | 수소효율(고속) | 공차중량 |
|---|---|---|---|---|---|---|
| A | 18" | 익스클루시브 트림 | **107.6 km/kg** | 113.7 (raw) | 100.9 (raw) | 1,870 kg |
| B | 18" | 표준 | **104.7 km/kg** | 110.8 (raw) | 98.2 (raw) | 1,890 kg |
| C | 19" | 표준 | **95.1 km/kg** | 99.3 (raw) | 90.4 (raw) | 1,900 kg |

> **(raw)** 표시 = raw_line 기반 파싱값. fuel_eff_city/highway DB null — 참고용.  
> **핵심 포인트:**
> - 행A (18" 익스클루시브): 복합 **107.6 km/kg** — 3행 중 최고 효율
> - 18" 기본(행B) vs 익스클루시브(행A): 효율 차이 −2.9 km/kg, 공차중량 +20 kg
> - 19" (행C): 18" 기본 대비 −9.6 km/kg, 공차중량 +10 kg — 휠 인치 효율 영향 큼
> - 1회충전거리: DB null — 발행 금지

---

## 수소효율 요약

| 휠 | 구동 | 비고 | 수소효율(복합) | 공차중량 | 에너지등급 |
|----|------|------|--------------|---------|-----------|
| 18" | FWD 추정 | 익스클루시브 | **107.6 km/kg** | 1,870 kg | 별도 고시 |
| 18" | FWD 추정 | 표준 | 104.7 km/kg | 1,890 kg | 별도 고시 |
| 19" | FWD 추정 | 표준 | 95.1 km/kg | 1,900 kg | 별도 고시 |

---

## 트림 라인업 (vehicle_trims)

| 트림 | 비고 |
|------|------|
| 익스클루시브 | 18" 수소효율 107.6 km/kg 대응 추정 |
| 프레스티지 | — |

> ⚠️ fuel_type·drive_type·wheel_size·fuel_eff 전 필드 null — 트림별 제원 직접 매핑 불가.  
> 행A(익스클루시브) ↔ 트림명 대응은 raw_line 텍스트 기반 추정.  
> 트림 가격은 verdict 인증 범위 외 → 미포함.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 넥쏘 수소전기 · 18" 복합 107.6km/kg · 소형 SUV 2026
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 넥쏘(2026)는 수소연료전지 SUV로, 18인치(익스클루시브) 기준 복합 수소효율 107.6 km/kg을 달성합니다.
18인치 표준은 104.7 km/kg, 19인치는 95.1 km/kg으로 휠 인치에 따른 효율 차이가 큽니다.
공차중량은 1,870~1,900 kg 범위이며, 1회충전거리는 별도 확인이 필요합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대(Hyundai)
모델: 넥쏘 (디 올 뉴 넥쏘 · 2026)
세그먼트: SUV (segment null, 소형 추정)
연료: 수소전기
구동방식: FWD 추정 (drive_type DB null — 원문 확인 필요)
수소효율(18" 익스클루시브): 복합 107.6 km/kg | 도심 113.7(raw) | 고속 100.9(raw)
수소효율(18" 표준): 복합 104.7 km/kg | 도심 110.8(raw) | 고속 98.2(raw)
수소효율(19"): 복합 95.1 km/kg | 도심 99.3(raw) | 고속 90.4(raw)
공차중량: 1,870(18" 익스클루시브) / 1,890(18") / 1,900(19") kg
1회충전거리: DB null — 미포함
트림: 익스클루시브 / 프레스티지
```

### ④ 인포그래픽·카드 수치 스니펫
```
[18" 익스클루시브] 수소 107.6km/kg | 1,870kg
[18" 표준]         수소 104.7km/kg | 1,890kg
[19" 표준]         수소 95.1km/kg  | 1,900kg
※ drive_type null(FWD 추정) · 1회충전거리 미수집 — 발행 전 확인 필수
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 에너지등급 | 수소차 별도 고시 (DB null 정상) |
| 1회충전거리 | DB·raw_line 미기재 |
| 구동방식 확정값 | drive_type null — FWD 추정, 원문 확인 권고 |
| 모터 출력 | vehicle_powertrains 미수집 |
| 트림별 제원 상세 | vehicle_trims null 전 행 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-27_  
_data gate: verdict-nexo-20260611.md (GREEN) · commit 8877504_
