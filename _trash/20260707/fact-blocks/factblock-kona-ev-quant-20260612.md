---
type: fact-block
title: 현대 코나 일렉트릭 팩트블록 (quantitative)
topic: kona-ev-factblock-quant
subject: 현대 코나 일렉트릭 (2024년형)
date: 2026-06-12
data_source:
  - data/outputs/approved/verdict-kona-ev-20260611.md (quantitative/referential GREEN)
created: 2026-06-12
expires: 2026-09-11
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-005-factblock-batch-20260612]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-kona-ev-20260611.md
  - DB: vehicle_powertrains WHERE slug='kona-ev' (쿼리 2026-06-12)
  - DB: vehicle_trims WHERE slug='kona-ev' (트림명만, 수치 null)
data_gate: verdict-kona-ev-20260611 GREEN · vehicle_powertrains DB == PDF 원문 일치
certified_scope: 전비·주행거리·공차중량·휠
uncertified: 가격·이미지·구동방식(kona-ev drive_type null)
flags:
  - "vehicle_powertrains.drive_type = null (전체). 구동방식 미기재 — 팩트블록 미채택."
  - "vehicles.year = 2024. 2026년형 데이터 갱신 여부 데이터팀 확인 권고."
---

# 코나 일렉트릭 팩트 블록 — quantitative

> 수치 출처: `vehicle_powertrains` 테이블 (DB == PDF 원문 일치, verdict-kona-ev-20260611 GREEN).  
> 인증 범위: 전비(km/kWh)·복합주행거리·공차중량·휠. 가격·이미지 미포함.

---

## 주의 플래그

| 항목 | 상태 | 내용 |
|------|------|------|
| 구동방식 | ⚠️ 미기재 | vehicle_powertrains.drive_type 전 행 null. 구동방식 팩트블록 미채택. |
| 연식 | ⚠️ 확인 권고 | vehicles.year = 2024 — 2025/2026년형 데이터 갱신 여부 데이터팀 확인 권고. |

---

## 기본 정보

| 항목 | 내용 | 근거 |
|------|------|------|
| 브랜드 | 현대 (HYUNDAI) | vehicles.brand |
| 모델명 | 코나 일렉트릭 (KONA Electric) | vehicles.name |
| 연식 | 2024년형 (DB 기준) | vehicles.year |
| 연료 | 전기 (BEV) | vehicle_powertrains.fuel_kind |

---

## 제원 매트릭스 (vehicle_powertrains · GREEN 인증)

> 전비(km/kWh): 도심·고속·복합 순. 주행거리: 복합 기준(km).

| 구분 | 휠 | 전비(도심) | 전비(고속) | 전비(복합) | 복합주행거리 | 공차중량 |
|------|-----|-----------|-----------|-----------|------------|---------|
| Standard | 17" | 6.1 | 4.8 | 5.5 km/kWh | 311 km | 1,630 kg |
| Long Range | 17" | 6.1 | 5.0 | 5.5 km/kWh | **417 km** | 1,720 kg |
| Long Range + 빌트인 캠 | 17" | 6.1 | 5.0 | 5.5 km/kWh | 415 km | 1,725 kg |
| Long Range | 19" | 5.2 | 4.4 | 4.8 km/kWh | 368 km | 1,740 kg |
| N Line (Long Range) | 19" | 5.1 | 4.3 | 4.7 km/kWh | 364 km | 1,740 kg |

> **최장 주행거리**: Long Range 17" — **417 km** (복합 기준)  
> **최고 전비**: Long Range 17" / Standard 17" — **5.5 km/kWh** (복합 기준)

---

## 트림 라인업 (vehicle_trims · 트림명만)

> 수치 null — 트림별 수치 DB 미연동. 트림명만 참고.

| 트림명 |
|--------|
| 롱레인지 |
| 프리미엄 |
| N라인 |
| 인스퍼레이션 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 코나 일렉트릭 2024년형 · 최대 417km · 전비 5.5km/kWh · 롱레인지/N라인
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 코나 일렉트릭(KONA Electric) 2024년형은 소형 SUV 세그먼트의 전기차입니다.
Long Range 17인치 기준 복합 전비 5.5 km/kWh, 복합 주행거리 417 km를 달성하며,
Standard·Long Range·N Line 등 5가지 파워트레인 구성을 갖추고 있습니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대(HYUNDAI)
모델: 코나 일렉트릭(KONA Electric)
연식: 2024년형 (DB 기준)
연료: 전기(BEV)
주행거리(대표): 417 km (Long Range 17" · 복합)
전비(대표): 5.5 km/kWh (Long Range 17" · 복합)
공차중량: 1,630~1,740 kg (파워트레인·휠별)
트림: 롱레인지·프리미엄·N라인·인스퍼레이션
```

### ④ 인포그래픽·카드 수치 스니펫
```
[Standard 17"]   311km | 5.5km/kWh | 1,630kg
[LR 17"]         417km | 5.5km/kWh | 1,720kg  ← 최장
[LR 19"]         368km | 4.8km/kWh | 1,740kg
[N Line 19"]     364km | 4.7km/kWh | 1,740kg
```

---

## 미포함 항목

| 항목 | 사유 |
|------|------|
| 출고가 / 렌탈료 | 가격 데이터 미인증 (verdict 범위 외) |
| 구동방식 | vehicle_powertrains.drive_type null (전 행) |
| 배터리 용량(kWh) | vehicle_powertrains 수집값 없음 |
| 트림별 수치 | vehicle_trims 수치 null (DB 미연동) |

---

_작성: 컨텐츠_  
_작성일: 2026-06-12_  
_data gate: verdict-kona-ev-20260611.md (GREEN) · commit 8877504_
