---
type: scouting-report
trigger_type: schedule
cycle_kind: scout
source_cycle: [[content/raw/cycles/cadam/cycle-003-scout-1차]]
created: 2026-06-02
target_agent: 관리팀장
status: pending-preapproval
inputs:
  - data/outputs/approved/verdict-hyundai-avante-20260601.md
---

# 주기2 스카우팅 보고 — data approved 1회차 (2026-06-02)

> 사전 결재 게이트: 후보 목록 → 관리팀장 승인 → 생산 개시

---

## 1. 스캔 범위

`data/outputs/approved/` 전역 스캔 결과, 현재 green verdict 파일:

| 파일 | 차종 | 데이터 유형 | verdict | 검증일 |
|------|------|-----------|---------|--------|
| `verdict-hyundai-avante-20260601.md` | 현대 아반떼 | visual/referential | green | 2026-06-01 |

- spec-data (수치) 구역 green verdict: **0건**
- visual/referential green: **1건**

---

## 2. 기존 생산 에셋 현황

| 에셋 | 상태 | 비고 |
|------|------|------|
| `speccard-avante-visual-20260601.{md,png}` | pending-approval | 스팟A 결재 요청 중 |

→ 아반떼 visual 기반 주력 에셋 1건 이미 존재. 중복 제외 필요.

---

## 3. 신규 생산 후보 (visual/referential green 범위 내)

### 후보 1 — 아반떼 팩트 블록 (텍스트)
- **설명**: 아반떼 모델 소개용 재사용 텍스트 소스. 모델명·연식·바디형태·카테고리 구성을 팩트 블록으로 정리.
- **활용처**: 마케팅 SNS 캡션, 블로그 소개 단락, 세일즈 상담 자료 재사용 소재
- **데이터 의존**: visual/referential green ✅ (수치 미포함)
- **제작 공수**: 소 (텍스트 전용, 1~2일)
- **우선순위**: ★★★

### 후보 2 — 아반떼 비주얼 카드 1:1 정방형 규격
- **설명**: 기존 speccard-avante-visual(4:5 세로형)의 1080×1080 정방형 버전. 카카오 채널·인스타 정방형 채널 대응.
- **활용처**: 마케팅 정방형 채널 (카카오, 인스타 1:1)
- **데이터 의존**: visual/referential green ✅ (기존 PNG 이미지 재활용)
- **제작 공수**: 소 (기존 에셋 규격 변환)
- **우선순위**: ★★ (스팟A 승인 이후 순서)

### 후보 3 — 차종 소개 카드 템플릿 정의서
- **설명**: 아반떼 visual 카드 제작 경험을 기반으로, 향후 타 차종에도 재사용 가능한 비주얼 카드 레이아웃 표준 정의서.
- **활용처**: 데이터 에이전트에서 새 차종 green 나올 때마다 즉시 카드 제작 가능한 템플릿
- **데이터 의존**: 없음 (템플릿 문서, 실제 데이터 불필요)
- **제작 공수**: 중 (2~3일, speccard-avante-design blueprint 기반 일반화)
- **우선순위**: ★★

---

## 4. 차단 후보 (spec-data green 미확보)

| 후보 | 차단 사유 |
|------|---------|
| 아반떼 스펙 수치 비교 카드 (연비, 출력, 배기량) | spec-data verdict 없음 |
| 아반떼 렌탈료 인포그래픽 | spec-data + price verdict 없음 |
| 아반떼 vs 경쟁차 수치 비교표 | spec-data verdict 없음 |

---

## 5. 요청 사항

관리팀장 사전 승인 요청 (생산 시작 전):
1. **후보 1 (팩트 블록)** 생산 승인 여부
2. **후보 2 (1:1 정방형)** 생산 승인 여부 — 스팟A 승인 후 순차 진행 권장
3. **후보 3 (템플릿 정의서)** 생산 승인 여부

승인 항목만 생산 착수합니다.
