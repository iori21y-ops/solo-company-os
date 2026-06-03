---
type: fact-block
topic: avante-visual-factblock
subject: 현대 아반떼
data_source: speccard-avante-visual-20260601.md (visual/referential green)
created: 2026-06-02
expires: null
used_in: []
status: pending-approval
source_cycle: [[content/raw/cycles/cadam/cycle-004-factblock-avante]]
trigger_type: schedule
inputs:
  - data/outputs/approved/verdict-hyundai-avante-20260601.md
  - content/outputs/approved/speccard-avante-visual-20260601.md
data_gate: visual/referential green only
spec_data_excluded: true
note: |
  모든 항목이 approved speccard-avante-visual-20260601.md 포함 요소에서 직접 추적됨.
  spec-data YELLOW verdict 발행됐으나 갈래 미결정 → 수치 슬롯 전면 제외 유지.
---

# 아반떼 팩트 블록 (visual/referential 범위)

> ⚠️ 출처 한정: `speccard-avante-visual-20260601.md` (approved) 포함 요소만 사용.
> 수치 제원·가격·렌탈료 전면 미포함. 추론·지식 기반 입력 없음.

---

## 기본 정보

| 항목 | 내용 | 근거 (speccard-avante-visual 포함 요소) |
|------|------|----------------------------------------|
| 브랜드 | HYUNDAI / 현대 | 브랜드명: HYUNDAI / AVANTE 뱃지 |
| 모델명 | 아반떼 (AVANTE) | 모델명: 현대 아반떼 / SEDAN · 2024 |
| 바디타입 | 세단 (SEDAN) | 모델명: 현대 아반떼 / SEDAN · 2024 |
| 연식 | 2024 | 모델명: 현대 아반떼 / SEDAN · 2024 |
| 파워트레인 | 가솔린, 하이브리드 | 카테고리 태그: 가솔린, 하이브리드 |
| 변속기 | IVT | 카테고리 태그: IVT |
| 구동방식 | FWD (전륜구동) | 카테고리 태그: FWD |
| 승차정원 | 5인승 | 카테고리 태그: 5인승 |

---

## 재사용 문구 소스

### ① SNS 캡션용 (50자 이내)
```
현대 아반떼 세단 · 가솔린·하이브리드 · IVT · FWD · 5인승
```

### ② 블로그 소개 단락용 (2~3문장)
```
현대 아반떼(AVANTE)는 2024년식 5인승 전륜구동(FWD) 세단입니다.
가솔린과 하이브리드 두 가지 파워트레인을 제공하며, IVT 변속기를 적용했습니다.
```

### ③ 상담 자료용 (항목형)
```
브랜드: 현대(HYUNDAI)
모델: 아반떼(AVANTE)
타입: 세단
연식: 2024
파워트레인: 가솔린 / 하이브리드
변속기: IVT
구동: FWD (전륜)
정원: 5인승
```

---

## 제외 항목 (spec-data 미확보 / YELLOW verdict)

아래 항목은 spec-data 정합성 판정 결정 전까지 팩트 블록에 포함 불가:

| 슬롯 | 사유 |
|------|------|
| 배기량, 출력, 연비 | spec-data YELLOW — 갈래 A/B 미결정 |
| 전장, 구동(수치) | spec-data YELLOW — 소스 없음 |
| 렌탈료, 출고가 | spec-data YELLOW — 가격 데이터 미수록 |
| 트림명 | spec-data YELLOW — DB 미연동 |

> spec-data 갈래 A(추가 수집) 또는 갈래 B(축소 허용) 결정 후 갱신 예정.
