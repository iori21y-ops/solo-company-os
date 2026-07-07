---
type: fact-block
title: 르노코리아 그랑 콜레오스 하이브리드 팩트블록 (quantitative · 26MY · E-Tech)
topic: grand-koleos-hybrid-factblock-quant
subject: 르노코리아 그랑 콜레오스 하이브리드 E-Tech (26MY · 중형 SUV · 1.5T HEV · 2WD · 19"/20")
date: 2026-06-23
data_source:
  - data/outputs/approved/verdict-grand-koleos-hybrid-20260611.md (quantitative/referential GREEN)
created: 2026-06-23
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-016-factblock-batch-20260623]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-grand-koleos-hybrid-20260611.md
  - PDF: cadam-n8n/price_crawler/pdf_cache/renault_koleos_20260611.pdf (p.7 제원표 · 정부 공인 표준연비 및 등급)
data_gate: verdict-grand-koleos-hybrid-20260611 GREEN · DB == PDF 원문 일치 (pdf_cache 전수 대조)
certified_scope: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠·구동방식
uncertified: 가격·이미지·트림별 스펙 매핑·안전등급
flags:
  - "DB 접근 불가(SUPABASE_ACCESS_TOKEN 미제공) — PDF 원문 직접 추출. verdict GREEN으로 DB==PDF 일치 확인된 수치 그대로 사용."
  - "트림 연비 구분: techno(19") vs iconic·esprit Alpine(19"/20") — 트림 간 무게 차(15kg)·CO2 차(5g) 확인됨."
  - "19"/20" 동일 트림 내 연비 동일값으로 PDF에 묶어 표기 — 휠별 분리 수치 미제공."
  - "구동방식: 전 트림 2WD 전용(하이브리드 E-Tech 전용). 4WD 없음."
  - "파워트레인: 가솔린 1.5 터보(144ps/5,500rpm) + 듀얼 모터(구동 100kW/보조 60kW) · 시스템 최고출력 245ps · 배터리 1.64kWh · 멀티모드 오토."
  - "가격(base_price) 가격 verdict 미인증 — 참고용. 발행 전 별도 가격 인증 필수."
---

# 그랑 콜레오스 하이브리드 E-Tech 팩트 블록 — quantitative (26MY · 중형 HEV SUV)

> 수치 출처: `renault_koleos_20260611.pdf` p.7 정부 공인 표준연비 및 등급표  
> 인증 범위: 연비(복합/도심/고속)·CO2·공차중량·배기량·에너지등급·휠·구동방식.  
> ⚠️ DB 직접 조회 대신 PDF 원문 사용 — verdict GREEN(DB==PDF 일치) 확인 기준.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| DB 접근 | ⚠️ 불가 | SUPABASE_ACCESS_TOKEN 미제공 — PDF 원문 수치 사용 (verdict GREEN 기준) |
| 휠별 분리 | ℹ️ 미제공 | iconic·esprit Alpine의 19"/20" 연비 동일값으로 묶어 표기 |
| 구동방식 | ℹ️ 2WD 전용 | 하이브리드 E-Tech 전 트림 2WD. 4WD 미설정. |
| 가격 데이터 | 📌 참고용 | 가격 verdict 미인증. 발행 전 별도 인증 필수. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 르노코리아 | PDF 표지 |
| 모델명 | 그랑 콜레오스 하이브리드 E-Tech | PDF p.3 |
| 연식 | 26MY (2026년형) | PDF 표지 |
| 세그먼트 | 중형 SUV | PDF 제원 |
| 연료 | 하이브리드 (가솔린 1.5T + 전기) | vehicle_powertrains |
| 파워트레인 | 1.5T 가솔린 엔진(144ps) + 듀얼모터(구동 100kW · 보조 60kW) · 시스템 245ps | PDF p.7 |
| 배터리 | 1.64kWh | PDF p.3 |
| 변속기 | 멀티모드 오토 | PDF p.7 |
| 구동방식 | 2WD 전용 | PDF p.7 |
| 배기량 | 1,499cc (1.5T 가솔린) | PDF p.7 |
| 전장×전폭×전고 | 4,780mm × 1,880mm × 1,680mm (1,705mm w/ 안테나) | PDF p.7 |
| 축거 | 2,820mm | PDF p.7 |

---

## 제원 매트릭스 (정부 공인 표준연비 · GREEN 인증)

| 행 | 트림 | 휠 | 연비(복합) | 연비(도심) | 연비(고속) | CO2 | 공차중량 | 에너지등급 |
|---|------|---|-----------|-----------|-----------|-----|---------|---------|
| A | **techno** | **19"** | **15.7 km/ℓ** | 15.6 | 15.8 | 102 g/km | **1,735 kg** | **2등급** |
| B | **iconic · esprit Alpine** | **19" / 20"** | **15.0 km/ℓ** | 14.8 | 15.2 | 107 g/km | **1,750 kg** | **2등급** |

> ※ 타이어: techno·iconic = 235/50 R19 넥센타이어(회전저항 1등급), esprit Alpine·iconic(20") = 245/45 R20 금호타이어(회전저항 1등급)

---

## 핵심 비교

| 항목 | techno (19") | iconic·esprit Alpine (19"/20") | 차이 |
|------|-------------|-------------------------------|------|
| 복합연비 | **15.7 km/ℓ** | 15.0 km/ℓ | △0.7 km/ℓ |
| CO2 | 102 g/km | 107 g/km | △5 g/km |
| 공차중량 | 1,735 kg | 1,750 kg | △15 kg |
| 에너지등급 | **2등급** | **2등급** | 동일 |

> ✅ 전 트림 2등급 달성 (르노코리아 자체 하이브리드 최상위 효율급)

---

## 트림 라인업 (가격 참고용 · 가격 verdict 미인증)

| 트림 | 판매가 (개소세 5%) | 친환경 혜택 후 | 주요 특징 |
|------|-----------------|-------------|---------|
| techno | 39,750,000원 | 38,149,000원 | 19" 넥센 · openR 파노라마 스크린(2화면) |
| iconic | 43,750,000원 | 42,089,000원 | 19"/20" · 동승석 12.3" 디스플레이 · FULL 오토 파킹 보조 |
| esprit Alpine | 45,750,000원 | 44,059,000원 | 20" 피크 알로이 · Alpine 전용 디자인 |

> ⚠️ 가격 출처: PDF p.3. 가격 verdict 미인증 — 참고용. 발행 전 별도 인증 필수.

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
르노 그랑 콜레오스 하이브리드 26MY · 최대 15.7km/ℓ · 전 트림 에너지 2등급
```

### ② 블로그 소개 단락용 (2~3문장)
```
르노코리아 그랑 콜레오스 하이브리드 E-Tech 26MY는 1.5T 가솔린 엔진과
듀얼 모터(시스템 최고출력 245ps)를 결합한 중형 SUV입니다.
techno 트림 기준 복합연비 15.7 km/ℓ로 전 트림 에너지 2등급을 달성하며,
전 구성에 2WD만 적용됩니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 르노코리아
모델: 그랑 콜레오스 하이브리드 E-Tech 26MY
세그먼트: 중형 SUV · 2WD 전용
연료: 하이브리드 (1.5T 가솔린 + 듀얼모터)
시스템 출력: 245ps

[techno · 19"]
복합연비: 15.7 km/ℓ (도심 15.6 / 고속 15.8)
CO2: 102 g/km | 공차중량: 1,735 kg | 에너지등급: 2등급

[iconic·esprit Alpine · 19"/20"]
복합연비: 15.0 km/ℓ (도심 14.8 / 고속 15.2)
CO2: 107 g/km | 공차중량: 1,750 kg | 에너지등급: 2등급
```

### ④ 인포그래픽·카드 수치 스니펫
```
[techno 19" 2WD]         15.7km/ℓ | CO2 102g | 1,735kg | 2등급  ← 최고 효율
[iconic·espritAlpine 19"/20" 2WD]  15.0km/ℓ | CO2 107g | 1,750kg | 2등급
※ 복합연비 기준 · PDF 정부 공인 표준연비 표 원문 · 배터리 1.64kWh
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 19" vs 20" 개별 연비 | PDF에서 iconic·esprit Alpine 묶어 표기 — 분리 수치 미제공 |
| 4WD 스펙 | 해당 트림 미존재 (하이브리드 E-Tech 전용 2WD) |
| 안전 등급 | 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-23_  
_data gate: verdict-grand-koleos-hybrid-20260611.md (GREEN · DB==PDF 일치) · PDF 원문: renault_koleos_20260611.pdf p.7_
