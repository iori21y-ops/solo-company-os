---
type: card-image-spec
topic: avante-spec-card-square
subject: 현대 아반떼 (1:1 정방형)
data_source: speccard-avante-visual-20260601.md (visual/referential green)
created: 2026-06-02
expires: null
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-006-avante-square]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-hyundai-avante-20260601.md
  - content/outputs/approved/speccard-avante-visual-20260601.md
  - content/outputs/approved/speccard-avante-visual-20260601.png
asset_file: speccard-avante-square-20260602.png
canvas: 1080x1080px (1:1, 정방형)
data_gate: visual/referential green only
note: |
  ⚠️ 이 파일은 레이아웃 규격 정의서(소스 .md)입니다. 렌더 PNG는 cadam-image 파이프라인 실행 후 생성.
  기존 speccard-avante-visual-20260601.png (4:5, 1080×1350) 기반 정방형 파생본.
  수치·가격·렌탈료 전면 미포함 (visual/referential 범위 유지).
---

# 아반떼 비주얼 카드 — 1:1 정방형 규격 소스

> **제공물**: 렌더 지시 소스(.md). 실제 PNG는 cadam-image 파이프라인 실행 필요.
> 기반: `speccard-avante-visual-20260601.png` (4:5 세로형 approved 버전)
> 목적: 카카오채널·Instagram 1:1 정방형 채널 대응

---

## 규격

| 항목 | 값 |
|------|-----|
| 캔버스 | 1080 × 1080 px (1:1) |
| 포맷 | PNG |
| 기반 에셋 | `speccard-avante-visual-20260601.png` |
| 변환 방식 | 정방형 크롭 또는 여백 추가 (아래 레이아웃 참조) |

---

## 레이아웃 조정 지시 (4:5 → 1:1)

```
원본 (1080×1350) → 정방형 (1080×1080)
조정 방식: 상단 크롭 방식

─────────────────────────────
[헤더 존] HYUNDAI / AVANTE 배지    ← 유지
─────────────────────────────
[차량 이미지 존] 측면 3/4 컷       ← 중앙 기준 크롭
  · 이미지 종횡비 유지
  · 좌우 여백 균등
─────────────────────────────
[정보 존] 모델명·카테고리 태그      ← 유지
  현대 아반떼 / SEDAN · 2024
  가솔린  하이브리드  IVT  FWD  5인승
─────────────────────────────
[CADAM 브랜딩 푸터]               ← 유지 (압축 허용)
─────────────────────────────
```

---

## 포함 요소 (원본 동일)

| 요소 | 내용 | 근거 |
|------|------|------|
| 브랜드 배지 | HYUNDAI / AVANTE | speccard-avante-visual 포함 요소 |
| 모델명 | 현대 아반떼 / SEDAN · 2024 | speccard-avante-visual 포함 요소 |
| 카테고리 태그 | 가솔린, 하이브리드, IVT, FWD, 5인승 | speccard-avante-visual 포함 요소 |
| 차량 이미지 | 측면 3/4 컷 (원본 재사용) | speccard-avante-visual 포함 요소 |
| CADAM 브랜딩 | 풋터 | speccard-avante-visual 포함 요소 |

## 제외 요소 (원본 동일 유지)
- 수치 스펙 (배기량, 출력, 연비 등) — spec-data 미확보
- 가격, 렌탈료 — spec-data 미확보

---

## cadam-image 파이프라인 실행 지시

승인 후 cadam-image 에이전트에 아래 지시로 PNG 생성 요청:

```
기반 파일: speccard-avante-visual-20260601.png (1080×1350)
출력 규격: 1080×1080 (1:1 정방형)
크롭 기준: 상단 크롭 (헤더 포함), 정보존·푸터 유지
출력 파일명: speccard-avante-square-20260602.png
```
