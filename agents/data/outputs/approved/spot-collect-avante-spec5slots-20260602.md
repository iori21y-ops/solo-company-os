---
subject: hyundai-avante-cn7-fl
data_type: spec-data
audit_kind: spot-collection
verdict: green
collected: 2026-06-02
source_cycle: [[data/raw/cycles/avante-spec/cycle-001-spec5slots]]
---

# 스팟 수집 결과 — 아반떼 CN7 F/L 2026년형 제원 5슬롯

**갈래 A 실행 결과. 대표 승인 기반 스팟 수집.**

---

## 수집 슬롯 및 결과

| 슬롯 | DB 컬럼 | 수집값 | 판정 |
|------|---------|--------|------|
| 최고출력 | `max_power_ps` | 123 ps (6,300 rpm) | GREEN |
| 구동방식 | `drive_type` | FF (전륜구동) | GREEN |
| 전장 | `length_mm` | 4,710 mm | GREEN |
| 승차정원 | `seating` | 5명 | GREEN |
| 트림명 | `trim_name` | 스마트 / 모던 / 인스퍼레이션 (가솔린 1.6) | GREEN |

**전 슬롯 GREEN — 이전 YELLOW verdict 해소 가능.**

---

## 소스 상세

### 주 소스 A — chais.co.kr (CN7 F/L 2026년형 전용 페이지)
- URL: `https://chais.co.kr/Car/InfoDetail?modelId=3581`
- 수집 항목: 최고출력(123 ps), 구동방식(FF), 전장(4,710 mm), 승차정원(5명)
- 수집일: 2026-06-02

### 주 소스 B — carnoon.co.kr (더 뉴 아반떼 종합 제원)
- URL: `https://www.carnoon.co.kr/newcar/vehicle/11414`
- 수집 항목: 트림명 전체 목록, 전장, 승차정원, 최고출력 교차확인
- 수집일: 2026-06-02

### 교차 확인 — WebSearch (현대 공식 페이지 인덱싱 기반)
- 현대 공식 제원 페이지: `https://www.hyundai.com/kr/ko/e/vehicles/avante/spec`
- 현대 공식 가격 페이지: `https://www.hyundai.com/kr/ko/e/vehicles/avante/price`
- 교차 확인 항목: 123 ps, FF, 전장 4,710 mm (CN7 초기형 4,650 mm 대비 +60 mm), 5인승, 스마트/모던/인스퍼레이션 트림

> **비고**: 현대 공식 제원 페이지는 JS 렌더링으로 직접 파싱 불가. chais.co.kr + carnoon.co.kr은 공식 데이터 집계 사이트이며 두 소스 수치가 일치함. 소스 등급 → **secondary (공식 집계)**. 수치 신뢰도 HIGH.

---

## 상세 트림 라인업 (가솔린 1.6 기준)

| 트림명 | 연료 | 변속기 |
|--------|------|--------|
| 스마트 | 가솔린 1.6 | IVT (자동) |
| 모던 | 가솔린 1.6 | IVT (자동) |
| 인스퍼레이션 | 가솔린 1.6 | IVT (자동) |
| 인스퍼레이션 | 가솔린 1.6 N라인 | IVT (자동) |

> LPi(LPG) 트림도 동일 구성(스마트/모던/인스퍼레이션) 존재. 본 수집은 가솔린 기준.

---

## DB 반영 권고

| DB 컬럼 | 반영값 | 비고 |
|---------|--------|------|
| `max_power_ps` | 123 | 가솔린 1.6 기준 |
| `drive_type` | FF | 전륜구동 |
| `length_mm` | 4710 | CN7 F/L 전장 (컬럼 신규 추가 완료) |
| `seating` | 5 | |
| `trim_name` | pricing 테이블 연동 필요 | 트림 3종 확인됨. 별도 DB 연동 작업 필요 |

> `trim_name`은 pricing 테이블 아반떼 데이터 미수록 상태로 수집과 별도로 DB 연동 작업이 필요합니다. 단순 수치 반영이 아닌 테이블 구조 작업 → 대표/관리팀장 판단 후 ops 배정 권고.

---

## verdict 갱신 권고

이 수집 결과로 `verdict-hyundai-avante-specdata-20260602.md` (YELLOW)를 GREEN으로 재발행 가능합니다.
승인 시 콘텐츠팀 스팟C 차단 전면 해제됩니다.

---

_수집자: 데이터_  
_수집일: 2026-06-02_  
_관련 verdict: [[data/outputs/approved/verdict-hyundai-avante-specdata-20260602]]_
