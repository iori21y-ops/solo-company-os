---
type: fact-block
title: 르노코리아 그랑 콜레오스 가솔린 팩트블록 (quantitative · 26MY · 2.0 터보)
topic: grand-koleos-factblock-quant
subject: 르노코리아 그랑 콜레오스 가솔린 2.0 터보 (26MY · 중형 SUV · 2WD/4WD · 19"/20")
date: 2026-06-23
data_source:
  - data/outputs/approved/verdict-grand-koleos-20260611.md (quantitative/referential GREEN)
created: 2026-06-23
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-016-factblock-batch-20260623]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-grand-koleos-20260611.md
  - PDF: cadam-n8n/price_crawler/pdf_cache/renault_koleos_20260611.pdf (p.7 제원표 · 정부 공인 표준연비 및 등급)
data_gate: verdict-grand-koleos-20260611 GREEN · DB == PDF 원문 일치 (pdf_cache 전수 대조)
certified_scope: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠·구동방식
uncertified: 가격·이미지·트림별 스펙 매핑·안전등급
flags:
  - "DB 접근 불가(SUPABASE_ACCESS_TOKEN 미제공) — PDF 원문 직접 추출. verdict GREEN으로 DB==PDF 일치 확인된 수치 그대로 사용."
  - "19"/20" 동일 트림 내 연비 동일값으로 PDF에 묶어 표기 — 휠별 분리 수치 미제공."
  - "2WD: 7단 DCT(습식) / 4WD: 8AT — 변속기 다름."
  - "4WD iconic만 제공(techno·esprit Alpine 4WD 없음)."
  - "가격(base_price) 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# 그랑 콜레오스 가솔린 2.0 터보 팩트 블록 — quantitative (26MY · 중형 가솔린 SUV)

> 수치 출처: `renault_koleos_20260611.pdf` p.7 정부 공인 표준연비 및 등급표  
> 인증 범위: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠·구동방식.  
> ⚠️ DB 직접 조회 대신 PDF 원문 사용 — verdict GREEN(DB==PDF 일치) 확인 기준.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| DB 접근 | ⚠️ 불가 | SUPABASE_ACCESS_TOKEN 미제공 — PDF 원문 수치 사용 (verdict GREEN 기준) |
| 휠별 분리 | ℹ️ 미제공 | 19"/20" 연비 동일값으로 묶어 표기 |
| 4WD 트림 | ℹ️ iconic 전용 | 4WD는 iconic 트림만 선택 가능 (techno·esprit Alpine 미적용) |
| 가격 데이터 | 📌 참고용 | 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 르노코리아 | PDF 표지 |
| 모델명 | 그랑 콜레오스 가솔린 2.0 터보 | PDF p.4 |
| 연식 | 26MY (2026년형) | PDF 표지 |
| 세그먼트 | 중형 SUV | PDF 제원 |
| 연료 | 가솔린 (터보 직분사) | PDF p.7 |
| 엔진 | 2.0 터보 가솔린 (211ps/5,000rpm) | PDF p.7 |
| 최대 토크 | 33.2 kg·m / 2,000~4,500 rpm | PDF p.7 |
| 변속기 | 7단 DCT(습식) — 2WD / 8AT — 4WD | PDF p.4·p.7 |
| 배기량 | 1,969cc | PDF p.7 |
| 전장×전폭×전고 | 4,780mm × 1,880mm × 1,680mm (1,705mm w/ 안테나) | PDF p.7 |
| 축거 | 2,820mm | PDF p.7 |

---

## 제원 매트릭스 (정부 공인 표준연비 · GREEN 인증)

| 행 | 구동 | 변속기 | 휠 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|------|------|---|-----------|-----------|-----------|-----|---------|---------|
| A | **2WD** | 7단 DCT | **19" / 20"** | **11.1 km/ℓ** | 9.8 | 13.1 | 150 g/km | **1,655 kg** | **4등급** |
| B | **4WD** | 8AT | **19" / 20"** | **9.8 km/ℓ** | 8.5 | 11.9 | 172 g/km | **1,765 kg** | **4등급** |

> ※ 타이어: techno·iconic 2WD = 235/50 R19 넥센타이어, iconic 20"·esprit Alpine = 245/45 R20 금호타이어  
> ※ 4WD는 iconic 트림 전용. 도로 오프로드 모드(Snow/Off Road) 포함.

---

## 핵심 비교

| 항목 | 2WD (7단 DCT) | 4WD (8AT) | 차이 |
|------|--------------|-----------|------|
| 복합연비 | **11.1 km/ℓ** | 9.8 km/ℓ | △1.3 km/ℓ |
| 도심연비 | 9.8 km/ℓ | 8.5 km/ℓ | △1.3 km/ℓ |
| 고속연비 | 13.1 km/ℓ | 11.9 km/ℓ | △1.2 km/ℓ |
| CO2 | 150 g/km | 172 g/km | △22 g/km |
| 공차중량 | 1,655 kg | 1,765 kg | △110 kg |
| 에너지등급 | 4등급 | 4등급 | 동일 |

---

## 하이브리드 vs 가솔린 연비 간 비교 (참고)

| 파워트레인 | 최고 복합연비 | CO2 최소 | 에너지등급 |
|-----------|------------|---------|---------|
| HEV 1.5T (techno 19") | **15.7 km/ℓ** | 102 g/km | 2등급 |
| 가솔린 2.0T 2WD | 11.1 km/ℓ | 150 g/km | 4등급 |
| 가솔린 2.0T 4WD | 9.8 km/ℓ | 172 g/km | 4등급 |

> ※ HEV vs 가솔린 비교는 별도 verdict(grand-koleos-hybrid/grand-koleos 각각) 기반. 동일 pdf_cache 원문.

---

## 트림 라인업 (가격 참고용 · 가격 verdict 미인증)

| 트림 | 구동 | 판매가 (개소세 5%) | 개소세 인하 후 | 주요 특징 |
|------|------|-----------------|-------------|---------|
| techno | 2WD | 35,500,000원 | 34,970,000원 | 19" 넥센 · 7단 DCT |
| iconic | 2WD | 39,400,000원 | 38,810,000원 | 19"/20" · 7단 DCT · FULL 오토 파킹 보조 |
| esprit Alpine | 2WD | 41,550,000원 | 40,920,000원 | 20" 금호 · 7단 DCT · Alpine 디자인 |
| iconic 4WD | 4WD | 42,100,000원 | 41,470,000원 | 19"/20" · 8AT · 오프로드 모드 |

> ⚠️ 가격 출처: PDF p.4. 가격 verdict 미인증 — 참고용. 발행 전 별도 인증 필수.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
르노 그랑 콜레오스 2.0 터보 26MY · 2WD 11.1km/ℓ · 4WD 9.8km/ℓ · 4등급
```

### ② 블로그 소개 단락용 (2~3문장)
```
르노코리아 그랑 콜레오스 가솔린 2.0 터보 26MY는 211ps 터보 직분사 엔진을 탑재한
중형 SUV로, 2WD(7단 DCT) 기준 복합연비 11.1 km/ℓ, 4WD(8AT) 기준 9.8 km/ℓ이며,
두 구성 모두 에너지 4등급입니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 르노코리아
모델: 그랑 콜레오스 가솔린 2.0 터보 26MY
세그먼트: 중형 SUV
연료: 가솔린 터보 · 배기량 1,969cc · 211ps

[2WD · 7단 DCT(습식) · 19"/20"]
복합연비: 11.1 km/ℓ (도심 9.8 / 고속 13.1)
CO2: 150 g/km | 공차중량: 1,655 kg | 에너지등급: 4등급

[4WD · 8AT · 19"/20"] (iconic 전용)
복합연비: 9.8 km/ℓ (도심 8.5 / 고속 11.9)
CO2: 172 g/km | 공차중량: 1,765 kg | 에너지등급: 4등급
```

### ④ 인포그래픽·카드 수치 스니펫
```
[가솔린 2WD 7DCT 19"/20"]  11.1km/ℓ | CO2 150g | 1,655kg | 4등급
[가솔린 4WD 8AT  19"/20"]   9.8km/ℓ | CO2 172g | 1,765kg | 4등급
※ 복합연비 기준 · PDF 정부 공인 표준연비 표 원문 · 2.0T 가솔린 직분사 터보
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 19" vs 20" 개별 연비 | PDF에서 동일값으로 묶어 표기 — 분리 수치 미제공 |
| techno·esprit Alpine 4WD | 해당 조합 미존재 |
| 안전 등급 | 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-23_  
_data gate: verdict-grand-koleos-20260611.md (GREEN · DB==PDF 일치) · PDF 원문: renault_koleos_20260611.pdf p.7_
