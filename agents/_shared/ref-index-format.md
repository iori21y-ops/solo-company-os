---
title: "참조 — index.md 형식"
type: reference
status: active
source: "CLAUDE.md §11에서 분리 (2026-06-02)"
---

# index.md 형식 (CLAUDE.md §11 상세)

각 에이전트 vault의 `wiki/index.md` 는 **그 에이전트의 학습 단일 진실 소스**다.
사이클 시작 시 가장 먼저 읽고, 사이클 종료 시 갱신한다.

## 11.1 운영 원칙

- 위치: `{agent}/wiki/index.md` (9개 에이전트 각각 1개)
- 갱신 주체: 에이전트 본인 (사이클 시작·종료 시점)
- 갱신 방식: 직접 편집. 자동 생성 아님.
- 사이클 시작 시 가장 먼저 읽는 진입점 (§5 워크플로우 참조)

## 11.2 프론트매터

```yaml
---
title: "{agent} 에이전트 wiki 인덱스"
type: index
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
agent: {agent}
---
```

## 11.3 섹션 구조 (7개 섹션)

순서대로 박는다. 빈 섹션이라도 헤더는 유지한다.

### (1) 진행 중인 사이클

```markdown
## 진행 중인 사이클

| 사이클 | 프로젝트 | 상태 | 시작일 |
|--------|---------|------|--------|
| [[raw/cycles/cadam/cycle-017-슬러그]] | cadam | in-progress | 2026-05-27 |
```

진행 중(in-progress) 사이클만. 완료(completed) 사이클은 자동 제거.

### (2) Playbooks (다음 사이클 자동 적용)

```markdown
## Playbooks

### 직무 (_skill)
| 페이지 | Tier | 적용 횟수 |
|--------|------|----------|
| [[wiki/_skill/playbooks/playbook-슬러그]] | 1 | 8 |

### 프로젝트 (cadam)
| 페이지 | Tier | 적용 횟수 |
|--------|------|----------|
| [[wiki/cadam/playbooks/playbook-슬러그]] | 1 | 3 |
```

Tier 1만 자동 적용 대상. Tier 2·3은 참고 또는 후보.

### (3) Insights (검증된 가설)

```markdown
## Insights

### 직무 (_skill) — confirmed
| 페이지 | Tier | 확인 사이클 |
|--------|------|------------|
| [[wiki/_skill/insights/insight-슬러그]] | 2 | cycle-015 |

### 프로젝트 (cadam) — confirmed
| 페이지 | Tier | 확인 사이클 |
|--------|------|------------|
| [[wiki/cadam/insights/insight-슬러그]] | 2 | cycle-012 |
```

status가 confirmed인 insight만 박제. pending·rejected는 제외.

### (4) Syntheses (횡단 분석)

```markdown
## Syntheses

| 페이지 | scope | 날짜 |
|--------|-------|------|
| [[wiki/_skill/syntheses/synthesis-슬러그]] | _skill | 2026-05-20 |
| [[wiki/cadam/syntheses/synthesis-슬러그]] | cadam | 2026-05-15 |
```

scope 컬럼으로 `_skill` / `{프로젝트}` 구분.

### (5) Failures (실패 사례)

```markdown
## Failures

| 페이지 | 프로젝트 | 사이클 |
|--------|---------|--------|
| [[wiki/cadam/failures/failure-슬러그]] | cadam | cycle-012 |
```

실패 사례는 학습의 자산. 누락하지 않는다.

### (6) Entities & Concepts

```markdown
## Entities & Concepts

| 페이지 | 타입 | scope | 참조 수 |
|--------|------|-------|---------|
| [[wiki/_skill/entities/entity-슬러그]] | entity | _skill | 5 |
| [[wiki/cadam/concepts/concept-슬러그]] | concept | cadam | 3 |
```

자주 참조되는 개체·개념의 색인. 사이클에서 1회 이상 참조된 것부터.

### (7) Refs (정본 참조 stub)

```markdown
## Refs

| 페이지 | 프로젝트 | 참조 수 |
|--------|---------|---------|
| [[_shared/refs/cadam/현대-캐스퍼]] | cadam | 4 |
```

`_shared/refs/{프로젝트}/` 의 stub 목록 (§2.5 참조).

## 11.4 scope 분리 표기

- `_skill/` (직무): 모든 프로젝트에 재사용 가능한 학습
- `{프로젝트}/` (예: `cadam/`): 특정 프로젝트에서만 통하는 학습
- 한 인덱스 안에서 두 scope를 별도 하위 섹션으로 분리

## 11.5 Tier 표기

| Tier | 의미 | 운영 |
|------|------|------|
| 1 | 검증 완료, 자동 적용 | 사이클 시작 시 자동 로드 |
| 2 | 검증 완료, 참고용 | 관련 사이클에서만 로드 |
| 3 | 후보, 실험 단계 | 명시 요청 시만 로드 |

## 11.6 갱신 시점

- **사이클 시작 시**: 진행 중인 사이클 섹션에 신규 사이클 추가
- **사이클 종료 시**: 진행 중에서 제거 + 산출물(insights/syntheses/playbooks/failures) 등록
- **insight 승격 시**: pending → confirmed → 인덱스에 추가
- **playbook 승격 시**: Tier 변경 반영
- **lint 시**: 고아·누락 페이지 정리
