---
type: fact-block
title: 현대 코나 하이브리드 팩트블록 (quantitative · SX2 · 2024)
topic: kona-hybrid-factblock-quant
subject: 현대 코나 하이브리드 (1.6 HEV 6단 DCT · 소형 SUV)
date: 2026-06-26
data_source:
  - data/outputs/approved/verdict-kona-hybrid-20260611.md (quantitative/referential GREEN)
created: 2026-06-26
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-021-factblock-batch-20260626]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-kona-hybrid-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='kona-hybrid' (쿼리 2026-06-26, 3행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='kona-hybrid' (쿼리 2026-06-26, 4행)
data_gate: verdict-kona-hybrid-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·CO2·공차중량·휠·에너지등급
uncertified: 가격·이미지·모터 출력·배터리 용량·구동방식(drive_type null)
flags:
  - "vehicles.year=2024 — 현행 연식 갱신 미확인(코나 가솔린과 동일 이슈). 데이터팀 확인 권고."
  - "drive_type 전 행 null — FWD(전륜) 추정. 발행 전 원문 확인 권고."
  - "vehicle_trims.wheel_size null 전 행 — 트림-휠 조합 매핑 불가."
  - "18" 이상 휠 추가 구성 존재 여부 미확인 (DB 행=3, 17\"/18\" 2종만 수집)."
---

# 코나 하이브리드 팩트 블록 — quantitative (SX2 · 2024 · 1.6 HEV)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-kona-hybrid-20260611 GREEN).  
> 인증 범위: 연비(km/L)·CO2·공차중량·휠·에너지등급.  
> ※ 가솔린·전기 라인업은 slug='kona'·'kona-ev' 별도 팩트블록 참조.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| year | ⚠️ 2024 | 현행 연식 갱신 미확인. 데이터팀 확인 권고. |
| drive_type | ⚠️ null 전 행 | FWD(전륜) 추정. 4WD 행 없음. 발행 전 원문 확인 권고. |
| vehicle_trims | ℹ️ wheel_size null | 트림-휠 매핑 불가. 트림 가격은 미인증(verdict 범위 외). |
| 수집 행 수 | ℹ️ 3행 | 17"/18" 2종. 추가 휠 구성 존재 여부 미확인. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (Hyundai) | vehicles.brand |
| 모델명 | 코나 하이브리드 | vehicles.name |
| 모델코드 | SX2 | vehicles.model_code |
| 연식 | 2024 (현행 갱신 미확인) | vehicles.year |
| 세그먼트 | 소형 | vehicles.segment |
| 차체 형태 | SUV | vehicles.body_type |
| 연료 | 하이브리드 (HEV) | vehicle_powertrains.fuel_kind |
| 엔진 | 스마트스트림 가솔린 1.6 하이브리드 6단 DCT (1,580cc) | vehicle_powertrains.engine · raw_line |
| 구동 | null (FWD 추정) | vehicle_powertrains.drive_type |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> drive_type 전 행 null (FWD 추정).  
> 구동방식은 발행 전 원문(PDF) 확인 필요.

### 스마트스트림 가솔린 1.6 하이브리드 6단 DCT (1,580cc)

| 행 | 휠 | 비고 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|---|
| A | 17" | 표준 | **19.8 km/L** | 20.8 | 18.6 | 79 g/km | 1,435 kg | **1등급** |
| B | 17" | 빌트인 캠 | 18.9 km/L | 19.4 | 18.2 | 83 g/km | 1,435 kg | **1등급** |
| C | 18" | 표준 | 18.1 km/L | 18.6 | 17.5 | 87 g/km | 1,450 kg | **1등급** |

> **핵심 포인트:**
> - **전 조합 1등급** 달성 — 소형 SUV 최상위 효율
> - 최고 연비: 행A (17" 표준) — **19.8 km/L**, CO2 **79 g/km**
> - 빌트인 캠 장착 시 (행B): 19.8→18.9 km/L (−0.9 km/L), CO2 79→83 g/km, 등급 유지
> - 18" 휠 (행C): 17" 표준 대비 연비 −1.7 km/L, 공차중량 +15 kg

---

## 연비 요약

| 휠 | 구동 | 비고 | 연비(복합) | CO2 | 에너지등급 |
|----|------|------|-----------|-----|-----------|
| 17" | FWD 추정 | 표준 | **19.8 km/L** | 79 g/km | **1등급** |
| 17" | FWD 추정 | +빌트인 캠 | 18.9 km/L | 83 g/km | **1등급** |
| 18" | FWD 추정 | 표준 | 18.1 km/L | 87 g/km | **1등급** |

---

## 트림 라인업 (vehicle_trims)

| 트림 | 비고 |
|------|------|
| 모던 | — |
| 프리미엄 | — |
| N라인 | — |
| 인스퍼레이션 | — |

> ⚠️ wheel_size·drive_type·fuel_eff null 전 행 — 트림별 제원 매핑 불가.  
> 트림 가격은 verdict 인증 범위 외 → 미포함.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 코나 하이브리드 · 1.6 HEV · 17" 복합 연비 19.8km/L(1등급) · 소형 SUV
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 코나 하이브리드(SX2)는 스마트스트림 1.6 하이브리드 6단 DCT를 탑재한 소형 SUV입니다.
17인치 기준 복합 연비 19.8 km/L(CO2 79g/km, 1등급)로 소형 SUV 최상위 효율을 달성하며,
빌트인 캠 장착 시 18.9 km/L, 18인치 휠 선택 시 18.1 km/L로 전 조합 1등급을 유지합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대(Hyundai)
모델: 코나 하이브리드 (SX2 · 2024, 연식 갱신 미확인)
세그먼트: 소형 SUV
연료: 하이브리드(HEV)
엔진: 스마트스트림 1.6 HEV 6단 DCT (1,580cc)
구동방식: FWD 추정 (drive_type DB null — 원문 확인 필요)
연비(대표·17" 표준): 19.8 km/L | CO2 79g/km | 1등급
연비(17" +빌트인캠): 18.9 km/L | CO2 83g/km | 1등급
연비(18" 표준): 18.1 km/L | CO2 87g/km | 1등급
공차중량: 1,435~1,450 kg (휠 조합별)
트림: 모던 / 프리미엄 / N라인 / 인스퍼레이션
```

### ④ 인포그래픽·카드 수치 스니펫
```
[17" FWD추정]          19.8km/L | CO2 79g/km | 1,435kg | 1등급  ← 최고연비
[17" FWD추정+빌트인캠] 18.9km/L | CO2 83g/km | 1,435kg | 1등급
[18" FWD추정]          18.1km/L | CO2 87g/km | 1,450kg | 1등급
※ drive_type null(FWD 추정) — 원문 확인 권고
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 구동방식 확정값 | drive_type null — FWD 추정, 원문 확인 권고 |
| 모터 출력·배터리 용량 | vehicle_powertrains 미수집 |
| 트림별 제원 상세 | vehicle_trims wheel_size·fuel_eff null |
| 최고출력·토크 | vehicle_powertrains 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-26_  
_data gate: verdict-kona-hybrid-20260611.md (GREEN) · commit 8877504_
