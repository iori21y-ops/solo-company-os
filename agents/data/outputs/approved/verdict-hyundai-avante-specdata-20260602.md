---
subject: hyundai-avante
data_type: spec-data
audit_kind: partial-integrity
verdict: yellow
checked: 2026-06-02
source_cycle: null
---

# verdict — hyundai-avante (spec-data / partial)

**종합 판정: YELLOW** — 10개 슬롯 중 5개 green, 5개 소스 없음 (green 불가)

---

## 검증 대상

콘텐츠 차단 파일:
- `content/outputs/pending/speccard-avante-design-20260601.md` (스펙카드 수치 슬롯)
- `content/outputs/pending/아반떼-장기렌트-20260531.md` (블로그)

---

## 슬롯별 판정

### GREEN (출처 확인, 사용 가능)

| 슬롯 | 값 | 출처 |
|------|----|------|
| `{연료유형}` | 가솔린 | avante-2026-price.pdf |
| `{배기량}` | 1598 cc | avante-2026-price.pdf |
| `{변속기명}` | 스마트스트림 IVT | avante-2026-price.pdf |
| `{연비}` | 15.0 km/L (복합) | avante-2026-price.pdf |
| `{연식}` | 2026 | avante-2026-price.pdf |

**출처 상세:**
- URL: `https://www.hyundai.com/contents/repn-car/catalog/avante-2026-price.pdf`
- PDF hash: `4dbb156ee827533b4f984673c608e56066cd6b1d5cb8a4550fdeb09ae5dae578`
- 수집일: 2026-05-31T17:01:26 (크롤러 자동 수집)

### MISSING — green 불가 (소스 없음)

| 슬롯 | DB 상태 | 사유 |
|------|---------|------|
| `{출력}` (max_power_ps) | null | 공식 가격표 미포함. 제원 별도 소스 필요 |
| `{구동방식}` (drive_type) | null | 공식 가격표 미포함. 제원 별도 소스 필요 |
| `{전장}` (length_mm) | DB 컬럼 없음 | vehicles 테이블에 전장 필드 미존재. 소스 없음 |
| `{승차정원}` (seating) | null | 공식 가격표 미포함. 제원 별도 소스 필요 |
| `{트림명}` (trim_name) | DB 미연동 | pricing 테이블 트림 데이터 아반떼 미수록 |

> 규칙 적용: "출처 없는 수치는 green 금지" — 5개 슬롯은 기억·추론 기반 입력 불가.

---

## 현재 차단 상태

- **콘텐츠 스팟C**: 유지. 누락 5개 슬롯 해소 전까지 수치 채우기 금지.
- **부분 활용 가능**: green 5개 슬롯(연료·배기량·변속기·연비·연식)은 스펙카드에 선사용 가능 — 단, 나머지 4개 수치 슬롯은 공란 처리 필요.

---

## 결재·에스컬레이션 필요 사항

아래 두 갈래 중 대표 결정이 필요합니다:

**갈래 A — 스팟 수집 승인**
- 현대 공식 제원 페이지(hyundai.com) 스팟 크롤링 권한 요청
- 수집 대상: 출력(ps), 구동방식, 전장(mm), 승차정원
- 완료 시 full green verdict 재발행 → 스팟C 전면 해제 가능
- 해당 사항: "스팟 수집 / 소스 추가" → 대표 결재 게이트

**갈래 B — 축소 카드 승인**
- 현재 green 5개 슬롯만으로 스펙카드 제작 허용
- 수치 미확보 슬롯(출력·구동·전장·승차정원) 카드에서 제거
- 트림명 슬롯도 데이터 미연동으로 제외

---

_verdict 발행자: 데이터_
_발행일: 2026-06-02_
