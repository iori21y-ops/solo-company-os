---
type: fact-block
title: 현대 아이오닉 6 팩트블록 (quantitative · CE1)
topic: ioniq6-factblock-quant
subject: 현대 아이오닉 6 (CE1 2026년형)
date: 2026-06-12
data_source:
  - data/outputs/approved/verdict-ioniq6-20260611.md (quantitative/referential GREEN)
created: 2026-06-12
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-005-factblock-batch-20260612]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-ioniq6-20260611.md
  - DB: vehicle_powertrains WHERE slug='ioniq6' (쿼리 2026-06-12)
  - DB: vehicle_trims WHERE slug='ioniq6' (트림명만, 수치 null)
data_gate: verdict-ioniq6-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 전비·주행거리·공차중량·구동방식·휠
uncertified: 가격·이미지·배터리 용량(수집값 미포함)
---

# 아이오닉 6 팩트 블록 — quantitative (CE1)

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-ioniq6-20260611 GREEN).  
> 인증 범위: 전비(km/kWh)·복합주행거리·공차중량·구동방식·휠. 가격·이미지 미포함.

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (HYUNDAI) | vehicles.brand |
| 모델명 | 아이오닉 6 (IONIQ 6) | vehicles.name |
| 모델코드 | CE1 | vehicles.model_code |
| 연식 | 2026년형 | vehicles.year |
| 세그먼트 | 중형 | vehicles.segment |
| 연료 | 전기 (BEV) | vehicle_powertrains.fuel_kind |
| 충전규격 | 800V 초급속 지원 | vehicles.highlights (미인증, 참고용) |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> 전비(km/kWh): 도심·고속·복합 순. 주행거리: 복합 기준(km).

| 트림 구분 | 휠 | 구동 | 전비(복합) | 전비(도심) | 전비(고속) | 복합주행거리 | 공차중량 |
|----------|-----|------|-----------|-----------|-----------|------------|---------|
| Standard | 18" | 2WD | 6.3 km/kWh | 6.8 | 5.7 | 437 km | 1,825 kg |
| Long Range | 18" | 2WD | 6.0 km/kWh | 6.4 | 5.4 | **562 km** | 1,925 kg |
| Long Range | 20" | 2WD | 5.1 km/kWh | 5.5 | 4.6 | 482 km | 1,945 kg |
| Long Range | 18" | AWD | 5.7 km/kWh | 6.1 | 5.3 | 533 km | 2,035 kg |
| Long Range | 20" | AWD | 4.8 km/kWh | 5.0 | 4.5 | 440 km | 2,055 kg |
| N Line | 20" | 2WD | 5.1 km/kWh | 5.5 | 4.6 | 470 km | 1,970 kg |
| N Line | 20" | AWD | 4.6 km/kWh | 4.8 | 4.3 | 428 km | 2,080 kg |

> **최장 주행거리**: Long Range 2WD 18" — **562 km** (복합 기준)  
> **최고 전비**: Standard 2WD 18" — **6.3 km/kWh** (복합 기준)

---

## 트림 라인업 (vehicle_trims · 트림명만)

> 수치 null — 트림별 수치 DB 미연동. 트림명만 참고.

| 트림명 |
|--------|
| 이-밸류 |
| 이-라이트 |
| 익스클루시브 |
| 프레스티지 |
| N라인 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 아이오닉 6 CE1 2026년형 · 롱레인지 562km · 전비 6.0km/kWh · 2WD/AWD
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 아이오닉 6(IONIQ 6) CE1 2026년형은 공기역학 최적화 설계를 적용한 중형 전기 세단입니다.
Long Range 2WD 18인치 기준 복합 전비 6.0 km/kWh, 복합 주행거리 562 km를 달성하며,
Standard부터 N Line AWD까지 7가지 파워트레인 옵션을 제공합니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대(HYUNDAI)
모델: 아이오닉 6(IONIQ 6) CE1
연식: 2026년형
세그먼트: 중형
연료: 전기(BEV)
구동방식: 2WD / AWD
주행거리(대표): 562 km (Long Range 2WD 18" · 복합)
전비(대표): 6.0 km/kWh (Long Range 2WD 18" · 복합)
공차중량: 1,825~2,080 kg (파워트레인별)
트림: 이-밸류·이-라이트·익스클루시브·프레스티지·N라인
```

### ④ 인포그래픽·카드 수치 스니펫
```
[Standard 2WD18"] 437km | 6.3km/kWh | 1,825kg
[LR 2WD 18"]     562km | 6.0km/kWh | 1,925kg  ← 최장
[LR AWD 18"]     533km | 5.7km/kWh | 2,035kg
[N Line AWD 20"] 428km | 4.6km/kWh | 2,080kg
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 배터리 용량(kWh) | vehicle_powertrains 수집값 없음 |
| 트림별 수치 | vehicle_trims 수치 null (DB 미연동) |
| 충전속도·충전시간 | 미수집 |

---

_작성: 컨텐츠_  
_작성일: 2026-06-12_  
_data gate: verdict-ioniq6-20260611.md (GREEN) · commit 8877504_
