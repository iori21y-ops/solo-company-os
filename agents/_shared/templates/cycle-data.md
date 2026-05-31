---
title: "data cycle 양식"
type: template
target_agent: data
status: confirmed
created: 2026-05-26
---

# data cycle 양식

data 에이전트의 사이클은 가장 복잡하다.
5종 cycle_kind, 4종 data_type, 5종 audit_kind, 5종 adhoc_subtype 분기.

파일명: `raw/cycles/{프로젝트}/cycle-NNN-{슬러그}.md`

## 프론트매터

```yaml
---
title: "사이클 제목 (한국어)"
type: cycle
status: started | in-progress | completed | measured | archived | cancelled
created: YYYY-MM-DD
cycle_id: NNN
agent: data
project: cadam
cycle_kind: regular | batch | audit | adhoc | builder | scout
data_type: quantitative | visual | textual | video | mixed
trigger_source: human | marketing | content | sales | self-scout | schedule | freshness-alert
target_topic: "주제 한 줄"
related_initiative: []
related_builder: []
linked_audit_cycles: []
audit_kind: internal | referential | cross_source | temporal | semantic
adhoc_subtype: query | scrape_existing | scrape_new | analysis | monitoring_setup
requester: human | agent-{이름}
priority: urgent | normal | low
estimated_complexity: simple | moderate | complex
needs_builder: true | false
linked_builder_cycle: []
linked_monitoring_setup: []
triggered_by: []
parallel_with: []
follow_up_to: []
inputs: []
---
```

cycle_kind에 따라 사용하는 필드가 다르다. 사용 안 하는 필드는 비워두거나 생략.

## 1. 배경

- 트리거 출처
- cycle_kind 판정 근거
- initiative에 속한 사이클이면 어느 initiative인가

## 2. cycle_kind별 본문

### 2-a. regular (정기 수집)

기존 빌더로 정기 수집. 본문 간략.

- 사용 빌더: `[[builders/{프로젝트}/{유형}/{빌더명}]]`
- 수집 범위
- 정합성 검증 결과
- 변경 사항 (전회 대비)

### 2-b. batch (대량 수집)

regular의 확장. 일일/주간 등 정해진 주기.

- 배치 범위 (기간, 대상)
- 자동화 흐름
- 실패 케이스

### 2-c. audit (정합성 점검)

audit_kind 5종 분기.

| audit_kind | 점검 대상 | 점검 방법 |
|------------|----------|----------|
| internal | 자기 vault 내 일관성 | V1~V5 규칙 |
| referential | 참조 무결성 | T1~T4 규칙 |
| cross_source | 출처 간 정합성 | 가중 다수결 |
| temporal | 시점 일관성 | R1~R3 규칙 |
| semantic | 텍스트 의미 정합성 | 로컬 Ollama Qwen3:14b |

- audit 대상 데이터
- 가중 정합률 계산 (출처 Tier 0~5 가중치)
- 임계 점검 (quantitative ≥85% / textual ≥75% / visual ≥90%)
- 임계 미달 시 자동 액션 (K 트리거 또는 builder 트리거)

### 2-d. adhoc (사용자 임시 요청)

adhoc_subtype 5종 분기.

| subtype | 처리 방식 |
|---------|----------|
| query | 기존 데이터에서 즉시 조회 (간략 박제 또는 log.md만) |
| scrape_existing | 기존 빌더로 즉시 수집 |
| scrape_new | builder cycle 분기 후 수집 |
| analysis | 기존 데이터로 분석, syntheses 박제 |
| monitoring_setup | builder + launchd/cron 등록 |

- 요청자
- 요청 내용
- 처리 결과
- 사용자 승인 (subtype=query인 경우 사이클 박제 여부 사용자 확인)

### 2-e. builder (신규 수집·검증 스크립트 작성)

새 도구를 만드는 사이클. 산출물 = 스크립트.

- 만들 도구의 목적
- 데이터 유형 (quantitative/visual/textual/video)
- 스크립트 경로: `builders/{프로젝트}/{유형}/{이름}.py`
- 정합성 검증 방식
- 카탈로그 등록: `builders/{프로젝트}/README.md`

### 2-f. scout (자율 수집 후보 발굴)

K 자율 수집. content의 J와 동일한 패턴이지만 영역이 다름.

- 정찰 영역 (자기 raw/cycles/, _config/, second-brain 검색 결과 등)
- 발견 신호 (신선도 임계 / 외부 변동 / 부재 추정)
- 발굴된 후보들 → `wiki/{프로젝트}/scouts/pending/` 에 박제

## 3. 출처 신뢰도 (cross_source / scrape 시 필수)

수집·참조한 각 출처의 Tier를 명시.

| 출처 | 카테고리 | Tier | 가중치 |
|------|---------|------|--------|
| (도메인) | (가격/판매량/정책/스펙/시장분석 등) | 0~5 | 3.0~0.0 |

판정 기준: `_config/source-tiers.md` 매트릭스 참조.

## 4. 정합성 결과

cycle_kind=audit 또는 cross-source가 있을 때.

- 일치 출처 / 불일치 출처
- 가중 정합률 점수
- 채택값 (가중 다수결 또는 Tier 0 절대 규칙)
- 출처 신뢰도 누적 갱신 (source-reliability-trend.md)

## 5. 신선도 점검

- 데이터 마지막 갱신일
- 신선도 임계값 (`_config/freshness-thresholds.md`)
- 임계 초과 시 다음 사이클 트리거 예약

## 6. 산출물

- 데이터 저장 위치 (Supabase 테이블 또는 파일 경로)
- 검증 통과 여부
- 다운스트림 소비자 알림 (marketing/content/sales)

## 7. 학습 추출 (5질문)

§6 학습 추출 가이드의 5질문에 답한다.

→ 인사이트 후보 박제 위치: `wiki/{프로젝트}/insights/insight-{슬러그}.md`
→ 정합성 인사이트는 `wiki/{프로젝트}/audits/{audit_kind}/insight-{슬러그}.md` 가능

## 관련 페이지

- 트리거: `[[]]`
- 빌더 카탈로그: `[[builders/{프로젝트}/README]]`
- audit 추세: `[[wiki/{프로젝트}/audits/consistency-trend]]`
- 출처 신뢰도 추세: `[[wiki/{프로젝트}/audits/source-reliability-trend]]`
