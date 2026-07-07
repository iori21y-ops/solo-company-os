---
type: fact-block
title: 기아 K8 하이브리드 팩트블록 (quantitative · 연식 미확인)
topic: k8-hybrid-factblock-quant
subject: 기아 K8 하이브리드 (1.6 터보 하이브리드 · AWD 준대형 세단)
date: 2026-06-25
data_source:
  - data/outputs/approved/verdict-k8-hybrid-20260611.md (quantitative/referential GREEN)
created: 2026-06-25
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-018-factblock-batch-20260625]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-k8-hybrid-20260611.md
  - DB: vehicle_powertrains JOIN vehicles WHERE slug='k8-hybrid' (쿼리 2026-06-25, 4행)
  - DB: vehicle_trims JOIN vehicles WHERE slug='k8-hybrid' (쿼리 2026-06-25, 0행 — 미등록)
data_gate: verdict-k8-hybrid-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 연비·공차중량·구동방식·휠·에너지등급
uncertified: 가격·이미지·CO2·모터 출력·배터리 용량
flags:
  - "vehicles.year null — 연식 미입력(2026년형 추정). 데이터팀 보완 권고."
  - "vehicles.model_code null — DB 미입력. 데이터팀 보완 권고."
  - "drive_type 전 행 AWD — 2WD/FWD 행 없음. AWD 전용 라인업으로 추정하나 데이터팀 확인 권고."
  - "co2_emission 전 행 null — 하이브리드 CO2 미수집. CO2 수치 콘텐츠 사용 금지."
  - "18인치 빌트인 캠 행(16.7 km/L)과 표준 행(17.2 km/L) 공존 — curb_weight 동일(1,655 kg). 빌트인 캠 장착 시 연비 0.5 km/L 하락."
  - "vehicle_trims 미등록 — k8(가솔린) 트림 테이블에 HEV 트림 혼재 가능성. 데이터팀 확인 권고."
---

# K8 하이브리드 팩트 블록 — quantitative (연식 미확인 · 1.6 터보 HEV)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-k8-hybrid-20260611 GREEN).  
> 인증 범위: 연비(km/L)·공차중량·구동방식·휠·에너지등급.  
> ※ 가솔린(K8) 제원은 slug='k8' 별도 팩트블록(factblock-k8-quant-20260617) 참조.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| year | ⚠️ null | 연식 미입력 (2026년형 추정). 데이터팀 보완 권고. |
| model_code | ℹ️ null | DB 미입력. 데이터팀 보완 권고. |
| drive_type | ⚠️ 요확인 | 전 행 AWD — 2WD 미존재. AWD 전용 라인업 추정. |
| CO2 | ⚠️ null 전 행 | 하이브리드 CO2 미수집. 수치 사용 금지. |
| 빌트인 캠 연비 | ℹ️ 참고 | 18" 빌트인 캠 장착 시 연비 17.2→16.7 km/L (−0.5 km/L). |
| vehicle_trims | ℹ️ 미등록 | HEV 트림 정보 별도 조회 필요. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 기아 (KIA) | vehicles.brand |
| 모델명 | K8 하이브리드 | vehicles.name |
| 모델코드 | — (null) | vehicles.model_code |
| 연식 | — (null, 2026년형 추정) | vehicles.year |
| 세그먼트 | 준대형 | vehicles.segment |
| 카테고리 | 세단 | vehicles.category |
| 연료 | 하이브리드 (HEV) | vehicle_powertrains.fuel_kind |
| 엔진 | 1.6 터보 하이브리드 자동 6단 (1,598cc) | vehicle_powertrains.engine |
| 구동 | AWD 전용 (전 행) | vehicle_powertrains.drive_type |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> CO2 전 행 null — 표에서 제외.  
> drive_type 전 행 AWD (2WD 행 없음).

### 1.6 터보 하이브리드 자동 6단 (1,598cc · AWD)

| 행 | 휠 | 비고 | 연비(복합) | 연비(도심) | 연비(고속) | 공차중량 | 에너지등급 |
|---|---|---|---|---|---|---|---|
| A | 17" | 표준 | **18.1 km/L** | 17.9 | 18.2 | 1,635 kg | **1등급** |
| B | 18" | 표준 | **17.2 km/L** | 17.2 | 17.2 | 1,655 kg | **1등급** |
| C | 18" | 빌트인 캠 | 16.7 km/L | 16.3 | 17.1 | 1,655 kg | **1등급** |
| D | 19" | 표준 | **16.1 km/L** | 15.8 | 16.4 | 1,695 kg | **1등급** |

> **핵심 포인트:**
> - **전 조합 1등급** 달성 — 준대형 세단 최상위 효율 등급
> - 최고 연비: 행A (17" AWD) — **18.1 km/L**
> - 빌트인 캠 장착 시 (행C): 17.2→16.7 km/L (−0.5 km/L), 등급 유지(1등급)
> - 공차중량: 휠 대형화에 따라 1,635→1,695 kg 증가

---

## 연비 요약

| 휠 | 구동 | 연비(복합) | 에너지등급 |
|----|------|-----------|-----------|
| 17" | AWD | **18.1 km/L** | **1등급** |
| 18" (표준) | AWD | **17.2 km/L** | **1등급** |
| 18" (빌트인 캠) | AWD | 16.7 km/L | **1등급** |
| 19" | AWD | 16.1 km/L | **1등급** |

---

## 트림 라인업 (vehicle_trims)

> ⚠️ vehicle_trims 미등록 — DB에 k8-hybrid 트림 정보 없음. k8(가솔린) 트림 테이블에서 HEV 트림 확인 필요.  
> ※ 실제 트림명·가격은 데이터팀 확인 후 별도 보완 필요.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
기아 K8 하이브리드 · 1.6T HEV AWD · 17" 기준 연비 18.1km/L(1등급) · 준대형 세단
```

### ② 블로그 소개 단락용 (2~3문장)
```
기아 K8 하이브리드는 1.6 터보 HEV 자동 6단 AWD를 탑재한 준대형 세단입니다.
17인치 기준 복합 연비 18.1 km/L(1등급)을 달성하며, 전 휠 조합에서 에너지 1등급을 유지합니다.
가솔린·LPG 라인업은 별도 K8 팩트블록을 참조하세요.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 기아(KIA)
모델: K8 하이브리드 (연식 미확인, 2026년형 추정)
세그먼트: 준대형 세단
연료: 하이브리드(HEV)
엔진: 1.6 터보 하이브리드 자동 6단 (1,598cc)
구동방식: AWD (전용)
연비(대표·17"): 18.1 km/L (1등급)
연비(대표·18"): 17.2 km/L (1등급)
연비(대표·19"): 16.1 km/L (1등급)
공차중량: 1,635~1,695 kg (휠 조합별)
※ 전 조합 에너지 1등급
```

### ④ 인포그래픽·카드 수치 스니펫
```
[17" AWD]  18.1km/L | 1,635kg | 1등급  ← 최고연비
[18" AWD]  17.2km/L | 1,655kg | 1등급
[18" AWD+빌트인캠]  16.7km/L | 1,655kg | 1등급
[19" AWD]  16.1km/L | 1,695kg | 1등급
※ CO2 미수집(DB null) / 전 조합 AWD
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| CO2 배출량 | DB 미수집 (전 행 null) |
| 모터 출력·배터리 용량 | vehicle_powertrains 미수집 |
| 트림 상세 | vehicle_trims 미등록 — 데이터팀 확인 필요 |
| 최고출력·토크 | vehicle_powertrains 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-25_  
_data gate: verdict-k8-hybrid-20260611.md (GREEN) · commit 8877504_
