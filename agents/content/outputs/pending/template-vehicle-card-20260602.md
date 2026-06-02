---
type: template-definition
topic: vehicle-card-template
subject: 차종 비주얼 카드 표준 템플릿
data_source: null
created: 2026-06-02
expires: null
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-005-template-vehicle-card]]
trigger_type: schedule
inputs:
  - content/outputs/approved/speccard-avante-visual-20260601.md
  - content/outputs/approved/speccard-avante-visual-20260601.png
note: |
  speccard-avante-visual 제작 경험 기반 일반화. 데이터 무관 템플릿 문서.
  향후 신차종 green verdict 발행 시 즉시 카드 생산 가능하도록 규격 표준화.
---

# 차종 비주얼 카드 표준 템플릿 정의서

> 기반: `speccard-avante-visual-20260601.png` 제작 경험 일반화
> 목적: 신차종 green verdict 발행 즉시 카드 생산 착수 가능한 표준 규격

---

## 1. 규격 표준

| 항목 | 값 | 비고 |
|------|-----|------|
| 기본 규격 | 1080 × 1350 px (4:5) | Instagram 피드 표준 |
| 정방형 규격 | 1080 × 1080 px (1:1) | 카카오채널·인스타 정방형 |
| 포맷 | PNG (투명도 없음) | WebP 변환은 cadam-image 파이프라인 사용 |
| 해상도 | 72 dpi (디지털 전용) | 인쇄 필요 시 300 dpi 별도 요청 |
| 색상 공간 | sRGB | |

---

## 2. 레이아웃 구조

```
┌─────────────────────────────────┐
│  [헤더 존] 브랜드 로고 / 모델 배지    │  상단 15%
│  HYUNDAI · AVANTE (예시)          │
├─────────────────────────────────┤
│                                   │
│     [차량 이미지 존]                │  중앙 55%
│     측면 3/4 앵글                   │
│     (미러 반사 효과 권장)             │
│                                   │
├─────────────────────────────────┤
│  [정보 존] 모델명 / 연식 / 카테고리   │  하단 상 20%
│  예: 현대 아반떼 / SEDAN · 2024    │
│      가솔린  하이브리드  IVT  FWD   │
├─────────────────────────────────┤
│  [CADAM 브랜딩 푸터]               │  최하단 10%
└─────────────────────────────────┘
```

---

## 3. 존별 콘텐츠 규격

### 3-1. 헤더 존
| 슬롯 | 내용 | 데이터 게이트 |
|------|------|--------------|
| `{brand_logo}` | OEM 브랜드 로고 | visual/referential green |
| `{model_badge}` | 영문 모델명 배지 | visual/referential green |

### 3-2. 차량 이미지 존
| 슬롯 | 내용 | 데이터 게이트 |
|------|------|--------------|
| `{vehicle_image}` | 차량 측면 3/4 컷 | visual green (이미지 완전성 확인) |
| 이미지 배경 제거 | cadam-image 파이프라인 처리 | — |
| 미러 반사 | 선택 효과 | — |

### 3-3. 정보 존 (visual/referential 전용)
| 슬롯 | 내용 | 데이터 게이트 |
|------|------|--------------|
| `{brand_kr}` | 한글 브랜드명 | visual/referential green |
| `{model_kr}` | 한글 모델명 | visual/referential green |
| `{body_type}` | 바디타입 (세단/SUV 등) | visual/referential green |
| `{model_year}` | 연식 | visual/referential green |
| `{powertrain}` | 파워트레인 태그 | visual/referential green |
| `{transmission}` | 변속기 태그 | visual/referential green |
| `{drive_type}` | 구동방식 태그 | visual/referential green |
| `{seating}` | 승차정원 태그 | visual/referential green |

### 3-4. 스펙 수치 존 (spec-data 전용, 별도 버전)
| 슬롯 | 내용 | 데이터 게이트 |
|------|------|--------------|
| `{displacement}` | 배기량 (cc) | spec-data green 필요 |
| `{max_power}` | 최고출력 (ps/rpm) | spec-data green 필요 |
| `{fuel_efficiency}` | 복합연비 (km/L) | spec-data green 필요 |
| `{length_mm}` | 전장 (mm) | spec-data green 필요 |
| `{trim_name}` | 트림명 | spec-data green 필요 |
| `{rental_price}` | 렌탈료 (월) | spec-data + price green 필요 |

> ⚠️ 스펙 수치 존이 포함된 카드는 spec-data green verdict 확보 전 생산 금지

### 3-5. CADAM 브랜딩 푸터
| 슬롯 | 내용 |
|------|------|
| CADAM 로고 | 고정 (브랜딩 에셋) |
| 슬로건 | 선택 |

---

## 4. 제작 절차 (신차종 투입 시)

```
1. data 에이전트 green verdict 확인
   ├─ visual green → 3-2 + 3-3 슬롯만 채운 visual 전용 카드 제작 가능
   └─ spec-data green → 3-4 슬롯 추가 (수치 버전 카드 가능)

2. content 에이전트: 팩트 블록 → 카드 소스(.md) 생산 → pending/

3. cadam-image 파이프라인: PNG 렌더 (배경 제거 + 규격 변환)

4. 정확성 검증 → [APPROVAL:관리팀장] 결재 카드 발송

5. 승인 → approved/ 이동 → assets/cadam/cards/ 복사 → index.md 등록
```

---

## 5. 파일명 규칙

```
speccard-{brand}-{model}-{type}-{YYYYMMDD}.md   # 소스 정의
speccard-{brand}-{model}-{type}-{YYYYMMDD}.png   # 렌더 결과물

type 값:
  visual   = visual/referential 전용 (수치 없음)
  design   = spec-data 포함 (수치 있음)
  square   = 1:1 정방형 파생
```

---

## 6. 기반 레퍼런스

- 레퍼런스: `speccard-avante-visual-20260601.{md,png}` (approved)
- 적용 사례: 현대 아반떼 (아반떼 visual → 이 정의서 기준 소급 정합)
