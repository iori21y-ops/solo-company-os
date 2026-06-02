---
title: 콘텐츠 에셋 재고 목록 (단일 진실 소스)
updated: 2026-06-02
---

<!-- 마지막 갱신: 2026-06-02 주기3 정기 갱신 — 스팟A·B approved 반영, 주기2 3건 pending 등록, stale 점검 -->

# CADAM 콘텐츠 에셋 인덱스

---

## 카드뉴스 문구 소스 (cards/)

| 파일명 | 주제 | 대상 | 상태 | 생성일 | 만료 | 사용처 |
|--------|------|------|------|--------|------|--------|
| cardnews-longterm-rent-benefits-20260601.md | 장기렌트 3가지 장점 (5장 문구) | 첫 상담 고객 | ✅ approved | 2026-06-01 | — | — |
| cardnews-견적비교체크리스트-20260602.md | 장기렌트 견적 비교 체크리스트 (5장 문구) | 견적 탐색 중 고객 | ✅ approved | 2026-06-02 | — | — |

> 둘 다 `outputs/approved/` — 범용, 차종·가격 미포함, 재사용 가능.
> `cardnews-견적비교체크리스트`: 2026-06-02 관리팀장 자동 승인 → approved/ 이동 완료.

---

## 스펙 카드 (cards/)

| 파일명 | 주제 | 상태 | 생성일 | 만료 | 사용처 |
|--------|------|------|--------|------|--------|
| speccard-avante-visual-20260601.{md,png} | 아반떼 visual 전용 스펙 카드 | ✅ approved | 2026-06-01 | — | — |

> 2026-06-02 관리팀장 자동 승인 → `outputs/approved/` 이동 완료.
> `assets/cadam/cards/` 물리적 이동: 결재 후 별도 처리 필요.

### 스펙 카드 pending (생산 완료, 결재 대기)

| 파일명 | 주제 | 상태 | 생성일 |
|--------|------|------|--------|
| cardspec-avante-square-20260602.md | 아반떼 1:1 정방형 카드 규격 소스 | ⏳ pending | 2026-06-02 |

> ⚠️ 규격 소스(.md)만 완성. PNG 렌더는 승인 후 cadam-image 파이프라인 필요.

---

## 팩트 블록 (fact-blocks/)

| 파일명 | 주제 | 상태 | 생성일 | 만료 | 사용처 |
|--------|------|------|--------|------|--------|
| factblock-avante-visual-20260602.md | 아반떼 visual 팩트 블록 (텍스트) | ⏳ pending | 2026-06-02 | — | — |

> 출처: speccard-avante-visual (approved) 포함 요소 직접 추적.
> 수치·가격 전면 미포함. spec-data YELLOW 판정으로 수치 슬롯 갱신 예정.

---

## 템플릿 정의서

| 파일명 | 주제 | 상태 | 생성일 |
|--------|------|------|--------|
| template-vehicle-card-20260602.md | 차종 비주얼 카드 표준 템플릿 정의서 | ⏳ pending | 2026-06-02 |

> 데이터 무관 템플릿 문서. 신차종 green verdict 발행 즉시 카드 생산 착수 가능하도록 규격 표준화.

---

## 인포그래픽 (infographics/)
_없음_

## 차트 (charts/)
_없음_

## 비교표 (comparisons/)
_없음_

## 리포트 (reports/)
_없음_

---

## 주기3 stale 점검 결과 (2026-06-02)

### stale 판정: 없음
- `cardnews-longterm-rent-benefits`: 범용 문구, 데이터 미의존 → 만료 없음 ✅
- `cardnews-견적비교체크리스트`: 범용 문구, 데이터 미의존 → 만료 없음 ✅
- `speccard-avante-visual`: visual/referential 기반, spec-data 갱신과 무관 → 만료 없음 ✅

### 주의 사항
- **spec-data YELLOW verdict 발행됨** (2026-06-02): 아반떼 spec-data green 확보 시 팩트 블록·스펙카드 수치 슬롯 갱신 필요. 갱신 시점까지 현재 에셋은 유효.
- **test-결재판-20260601.md** in `outputs/approved/`: 테스트 파일로 추정. 실제 에셋 아님 → 관리팀장 확인 후 삭제 권고.
