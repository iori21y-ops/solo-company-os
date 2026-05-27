# CLAUDE.md — 에이전트 학습 vault 운영 규칙

이 파일은 에이전트 학습 vault의 운영 규칙을 정의한다.
모든 학습 작업(사이클 기록, 인사이트 추출, 승격, 린트)은 이 스키마를 따른다.

최종 업데이트: 2026-05-26

---

# ⚠️ 최우선 규칙

## 0.1 모든 질문은 wiki/index.md 먼저

에이전트가 어떤 작업을 시작하든 — 사이클 시작, 인사이트 추출, 종합 분석, 질의 응답 — 웹서치나 자체 추론으로 바로 답하지 말고, 반드시 아래 순서를 따른다:

1. `{에이전트}/wiki/index.md` 읽기 → 관련 페이지 확인
2. 관련 페이지가 있으면 해당 페이지를 읽고 학습 데이터 기준으로 답변
3. 학습 데이터에 없는 경우만 웹서치/추론 사용 (사용 시 "학습 데이터에 없어 외부 정보로 답변" 명시)

위키 파일 검색 시 glob 패턴은 반드시 한글 포함 전체 목록을 커버해야 한다.
이 규칙을 어기면 학습 누적이 무의미해진다.

## 0.2 자가수정 금지

에이전트는 다음을 절대 자기 손으로 수정하지 않는다:

- 자신의 시스템 프롬프트
- 자신의 SKILL.md 본문
- 다른 에이전트의 wiki, raw, SKILL.md
- CLAUDE.md (이 파일)
- _shared/ 하위

위 항목은 모두 **사람(경년님) 또는 추후 strategy 에이전트의 승인** 후에만 수정 가능.
에이전트는 자기 wiki 안에서 신규 페이지 생성·수정만 허용된다.

---

# 1. 역할 정의

## 1.1 에이전트의 역할

- **위키 관리자**: 자기 vault 내 wiki 페이지를 생성·수정·교차참조한다.
- **사이클 실행자**: 트리거 받은 작업을 raw/cycles/에 사실대로 기록한다.
- **인사이트 추출자**: 사이클 종료 시 §6 "학습 추출 가이드"에 따라 인사이트 후보를 만든다.
- **참조자**: 사이클 시작 시 §5 "워크플로우"의 로드 순서에 따라 학습 데이터를 먼저 읽는다.

에이전트는 자기 vault 안에서만 권한이 있다. 다른 에이전트 vault는 **읽기 전용**.
다른 에이전트 인사이트 참조 시 §7 규칙 준수.

## 1.2 사용자(경년님)의 역할

- **큐레이터**: 사이클 결과를 검토하고 인사이트 후보를 승격(confirmed/rejected) 한다.
- **승격 게이트키퍼**: 프로젝트→직무 승격, Tier 상향, 플레이북 박제의 최종 승인.
- **방향 설정자**: 직무 정의(SKILL.md), 경계(boundary-rules.md), 위임 등급의 결정.

사용자는 비개발자이므로 모든 설명은 한국어로, 쉽게 작성한다.

## 1.3 추후 위임 (strategy 에이전트)

strategy 에이전트가 정의 완료되고 위임 5질문을 50회 누적 통과하면,
사용자의 "승격 게이트키퍼" 역할 중 일부를 strategy로 위임한다.
위임 시점은 별도 결정. 현재(2026-05)는 모든 승격을 사람이 직접 한다.

---

# 2. 디렉토리 구조

## 2.1 전체 구조
~/projects/_meta/agents/
├── .obsidian/                            # Obsidian vault 설정
├── CLAUDE.md                             # 이 파일 (vault 공통 규칙)
├── README.md                             # vault 진입 안내
├── _shared/                              # 에이전트 공통 자산
│   ├── boundary-rules.md                 # 에이전트 간 경계 규칙
│   ├── promotion-rules.md                # 승격 게이트 규칙
│   ├── scout-territories.md              # 자율 발굴 영역 정의
│   ├── delegation-template.md            # 위임 작업 양식
│   ├── workflow-template.md              # 자율 워크플로 양식
│   ├── security/                         # 위임 권한 단계
│   │   ├── blacklist.md
│   │   ├── approval-required.md
│   │   └── auto-allowed.md
│   ├── templates/                        # cycle 양식 (별도 파일)
│   │   ├── cycle-marketing.md
│   │   ├── cycle-content.md
│   │   └── cycle-data.md
│   ├── counters/                         # 프로젝트별 사이클 카운터
│   │   ├── README.md
│   │   └── cadam.md
│   └── refs/                             # 프로젝트 정본 stub
│       └── cadam/
│           └── _index.md
│
├── marketing/                            # 에이전트별 작업·학습 공간
│   ├── SKILL.md                          # 역할·산출물·KPI·경계 정의
│   ├── raw/cycles/cadam/                 # 사이클 사실 기록
│   └── wiki/
│       ├── index.md
│       ├── log.md
│       ├── _skill/                       # 직무 학습 (모든 프로젝트 재사용)
│       │   ├── insights/
│       │   ├── syntheses/
│       │   ├── playbooks/
│       │   ├── failures/
│       │   ├── concepts/
│       │   └── entities/
│       └── cadam/                        # 프로젝트별 학습
│           ├── insights/
│           ├── syntheses/
│           ├── playbooks/
│           ├── failures/
│           └── scouts/                   # 자율 발굴 후보 카탈로그
│               ├── pending/
│               ├── approved/
│               ├── rejected/
│               └── completed/
│
├── content/                              # marketing + 다음 추가
│   └── assets/cadam/                     # 비축 자산 (wiki 밖)
│       ├── infographics/
│       ├── charts/
│       ├── cards/
│       ├── fact-blocks/
│       ├── comparisons/
│       └── reports/
│
├── data/                                 # marketing + 다음 추가
│   ├── _config/                          # 운영 설정 (audit 규칙, 임계값)
│   │   ├── source-tiers.md
│   │   ├── consistency-thresholds.md
│   │   ├── freshness-thresholds.md
│   │   └── audit-rules-{internal,referential,cross_source,temporal,semantic}.md
│   ├── _inbox/
│   │   └── adhoc-queue.md                # 사람 요청 임시 큐
│   ├── initiatives/                      # 대형 작업 단위
│   │   └── wf-vi/
│   │       ├── README.md
│   │       └── milestones.md
│   ├── builders/cadam/                   # 스크립트 자산 카탈로그
│   │   ├── README.md
│   │   ├── quantitative/
│   │   ├── visual/
│   │   ├── textual/
│   │   └── video/
│   └── wiki/cadam/
│       ├── audits/                       # 정합성 추세 (시계열)
│       │   ├── consistency-trend.md
│       │   ├── source-reliability-trend.md
│       │   └── {internal,referential,cross_source,temporal,semantic}/
│       └── initiatives/wf-vi/
│           ├── insights/
│           ├── syntheses/
│           └── playbooks/
│
├── sales/, cs/, ops/, finance/, legal/, strategy/   # 기본 구조 동일

## 2.2 각 폴더의 책임

- **raw/cycles/{프로젝트}/**: 사이클 진행 사실 기록. 불변(오타·포맷 제외 수정 금지).
- **wiki/_skill/**: 직무 일반 학습. 2개 이상 프로젝트 confirmed 후 승격으로만 진입.
- **wiki/{프로젝트}/**: 프로젝트 한정 학습. 사이클 인사이트 1차 박제 위치.
- **wiki/{프로젝트}/scouts/**: 자율 발굴 후보의 라이프사이클 (pending/approved/rejected/completed).
- **assets/, builders/**: wiki 밖. 실제 비축 자산·도구 (wiki는 LLM 학습 페이지 전용).
- **_shared/refs/{프로젝트}/**: 외부 정본 vault의 stub 페이지.

## 2.3 사이클 ID 채번 규칙

- 형식: `cycle-NNN` (3자리 0 패딩)
- 채번 단위: **프로젝트별 단일 카운터** (에이전트 무관)
  - 예: cadam 전체에서 cycle-001, 002, 003... 단조 증가
- 채번 위치: `_shared/counters/{프로젝트}.md` 마지막 번호 + 1
- 채번은 단조 증가, 결번 허용

## 2.4 에이전트 간 사이클 연결

같은 프로젝트의 인접 사이클이 협업 관계일 때 프론트매터로 연결:

```yaml
---
cycle_id: 008
agent: content
project: cadam
triggered_by: [[marketing/raw/cycles/cadam/cycle-007]]
parallel_with: []
follow_up_to: []
---
```

## 2.5 _shared/refs/{프로젝트}/ stub

외부 정본 vault(예: ~/second-brain)의 자주 참조되는 페이지를 에이전트 vault 안에서도
백링크 가능하게 만드는 어댑터. 본문은 정본 URI 링크 + 에이전트 관점 메모만.

- stub 생성 기준: 1회 이상 사이클에서 참조된 엔티티부터
- 정본 정보 복제 금지 (SSOT 원칙)
- 본문은 "에이전트 관점 메모" 누적만

## 2.6 vault 외부 자산 참조

vault 외부 자산은 텍스트 참조만:
- **second-brain (카담 정본)**: ~/second-brain/wiki/...
  → `_shared/refs/cadam/` stub 통해 참조
- **GitHub**: github.com/iori21y-ops/solo-company-os (vault 자체가 일부)
- **Supabase, n8n, 외부 API**: 참조 정보(테이블명, 워크플로 ID)만 기록
- **핸드오프 시스템**: ~/projects/_meta/handoff/ (별도 시스템)

---

# 3. 페이지 형식 규칙

## 3.1 공통 프론트매터

모든 wiki 페이지는 YAML 프론트매터로 시작한다.

### 필수 (4개)

```yaml
---
title: "한국어 제목"
type: cycle | insight | synthesis | playbook | failure | concept | entity | project-ref | scout-candidate
status: draft | pending-review | confirmed | rejected | archived
created: YYYY-MM-DD
---
```

### 조건부 (2개)

```yaml
project: cadam              # 폴더가 _skill/이 아닐 때만
tier: 1 | 2 | 3             # type이 insight 또는 playbook일 때만
```

### 선택 (3개)

```yaml
updated: YYYY-MM-DD         # 변경 시 갱신 (Linter 플러그인)
tags: [태그1, 태그2]         # 검색용
aliases: [별칭1]             # 옵시디언 위키링크 보조
```

### scope 판정

`scope` 필드는 사용하지 않는다. 폴더 위치(`_skill/` vs `{프로젝트}/`)로 자동 판정.
Dataview 쿼리: `file.folder.contains("_skill")` 로 직무 학습 판정.

## 3.2 내부 링크

- 모든 내부 참조는 위키링크 `[[]]` 사용
- 다른 폴더 페이지: `[[_skill/playbooks/playbook-title-clear-rules]]`
- stub 참조: `[[_shared/refs/cadam/현대-캐스퍼]]`
- 새 페이지 없으면 링크를 먼저 걸고 페이지를 생성

## 3.3 cycle 페이지

에이전트별 cycle 양식은 별도 템플릿 파일 참조:

- [[_shared/templates/cycle-marketing]]
- [[_shared/templates/cycle-content]]
- [[_shared/templates/cycle-data]]

미완성:
- sales cycle 양식 (TBD)
- cs cycle 양식 (TBD)
- ops/finance/legal/strategy (스텁 정의 완료 후)

cycle 페이지는 raw/cycles/{프로젝트}/ 에 저장. 사이클 진행 사실 기록이며 불변.

## 3.4 ~ 3.10 페이지 타입별 양식

> [!warning] 미완성
> insight, synthesis, playbook, failure, concept, entity, project-ref, scout-candidate
> 각 페이지의 필수 섹션은 다음 세션에서 작성 예정.

## 3.11 페이지 명명 규칙

- 파일명: 영문 슬러그 + 한국어 title 분리
  - 파일명: `insight-title-numbers-low-impact.md`
  - 프론트매터: `title: "제목에 숫자 넣어도 효과 미미"`
- 슬러그 규칙: 소문자 영문 + 숫자 + 하이픈, 3~6단어
- 타입 접두사:
  - `cycle-NNN-{슬러그}.md`
  - `insight-{슬러그}.md`
  - `synthesis-{슬러그}.md`
  - `playbook-{슬러그}.md`
  - `failure-{슬러그}.md`
- 예외: entities/ 의 고유명사는 한국어 허용
  - `현대-캐스퍼.md`, `네이버-블로그.md`

## 3.12 본문 작성 규칙

- 한국어로 작성 (사용자가 비개발자)
- 원본 데이터 복사 금지 — 핵심 추출 후 재구성
- 모순되는 정보 발견 시 `> [!warning]` 콜아웃으로 표시
- 가설은 `> [!note]` 콜아웃으로 표시
- 페이지 끝에 "관련 페이지" 섹션, 백링크 명시

---

# 4. 4계층 학습 흐름

학습 결과물은 4개 계층으로 구분된다. 하위 계층이 상위 계층으로 승격되며, 각 계층은 성격·승격 트리거가 다르다.

## 4.1 cycles (사실 기록)

- 성격: 불변(immutable). 한 번 작성되면 수정하지 않음
- 내용: 사이클 실행 중 발생한 사실, 관찰, 결과
- 위치: `{프로젝트}/cycles/{날짜}-{주제}.md`

## 4.2 insights (가설)

- 성격: 가변. 상태값으로 관리: `pending` → `confirmed` 또는 `rejected`
- 내용: cycles에서 도출된 가설. 검증 전이므로 단정 금지
- 승격 트리거: 동일 가설이 다른 사이클에서 재확인되면 `confirmed`
- 위치: `{프로젝트}/insights/{주제}.md` (프론트매터에 status 명시)

## 4.3 syntheses (횡단 분석)

- 성격: 여러 insights를 묶어 패턴 추출
- 승격 트리거: 다음 둘 중 하나
  - 같은 프로젝트 내 confirmed insights 3건 이상
  - 서로 다른 프로젝트 간 confirmed insights 2건 이상
- 위치: `{프로젝트}/syntheses/{패턴명}.md` 또는 `_shared/syntheses/`

## 4.4 playbooks (행동 원칙)

- 성격: 다음 사이클에 자동 적용되는 규칙
- 승격 트리거: synthesis가 행동 가능한 규칙으로 정제됨
- 내용: "X 상황에서는 Y 한다" 형식의 단언문
- 위치: `wiki/{프로젝트}/playbooks/` 또는 `_skill/playbooks/`

## 4.5 수명 정책

> [!warning] 미정
> 각 계층별 수명·아카이브 정책은 실제 사이클 운영 후 결정. 현재는 모든 계층 영구 보존.

---

# 5. 워크플로우

## 5.1 목적

§4가 4계층의 *정의*라면, §5는 *운영 절차*다. 사이클을 시작할 때 무엇을 로드하고, 끝낼 때 어떤 순서로 마무리하는지 정한다.

## 5.2 사이클 시작 시 로드 순서

새 사이클을 시작할 때 다음 순서로 컨텍스트를 로드한다:

1. `wiki/index.md` — 단일 진실 소스
2. `wiki/_skill/playbooks/` Tier 1 — 직무 공통 행동 원칙
3. `wiki/{현재 프로젝트}/playbooks/` Tier 1 — 프로젝트 행동 원칙
4. `_skill/insights/` confirmed + 관련 pending — 직무 가설
5. `{프로젝트}/insights/` confirmed + 관련 pending — 프로젝트 가설
6. `_shared/refs/{프로젝트}/` 관련 stub — 횡단 참조

playbooks가 먼저 (행동 원칙이 가설보다 우선), insights가 다음 (검증된 것 → 검증 중), refs는 마지막 (필요할 때만).

## 5.3 사이클 종료 시 절차

다음 순서로 마무리한다. 순서가 중요하다 — 앞 단계의 출력이 뒤 단계의 입력이다.

1. **결과 측정** — 에이전트별 KPI에 따라 cycles 기록 (사실부터)
2. **승격 게이트** — pending insights를 사람 승인으로 `confirmed` 또는 `rejected` 처리
3. **직무 승격** — confirmed insights 중 playbook으로 정제 가능한 것을 `{프로젝트}/playbooks/` 또는 `_skill/playbooks/`로 승격
4. **횡단 종합 트리거** — syntheses 조건 검사 (같은 프로젝트 confirmed 3건 이상, 또는 다른 프로젝트 간 confirmed 2건 이상)
5. **린트** — 모순/고아/누락/오래됨 점검 (마지막 청소)

**순서 근거:**
- 사실 없이 가설 판정 불가 → 측정이 먼저
- insights가 confirmed 돼야 playbook 후보가 됨 → 게이트 → 직무 승격
- 같은 프로젝트 내 정제가 안정돼야 횡단 입력이 깨끗함 → 직무 승격 → 횡단
- 모든 변경 끝난 뒤 청소 → 린트 마지막

## 5.4 주의

- 로드 순서·종료 절차 둘 다 운영하면서 조정 가능. 현재는 출발점.
- 5.3의 순서는 자동화 시에도 동일 (n8n 등으로 자동화하더라도 단계 순서 유지).
- 사이클 종료 절차는 §6 학습 추출 가이드(5가지 질문 답변)와 병행 — 5.3 단계 1(측정) 직후 §6 질문에 답하는 것이 자연스러움.

---

# 6. 학습 추출 가이드

## 6.1 목적

사이클이 끝날 때마다 5가지 질문에 답한다. 답변은 §4의 4계층
학습 흐름으로 들어가는 입력이다. 질문에 답하지 않으면 cycles는
사실 기록으로만 남고 학습은 일어나지 않는다.

## 6.2 5가지 질문

사이클 종료 시 다음 5가지 질문에 답한다:

1. 이번 사이클에서 처음 알게 된 것이 있는가?
2. 예상과 다른 결과가 나온 부분이 있는가?
3. 다음 사이클에서 다르게 할 점이 있는가?
4. 다른 프로젝트에서도 적용될 가능성이 있는가?
5. 절대 다시 하지 말아야 할 패턴이 있는가?

답이 "없다"여도 명시적으로 "없음"이라고 적는다. 빈칸은 질문을
건너뛴 것과 구분되지 않는다.

질문 자체는 운영하면서 다듬을 수 있다. 단 변경 시 변경 이력을
남기고, 변경 전후 사이클을 비교할 때 질문 차이를 고려해야 한다.

## 6.3 답변이 가는 곳

| 질문 | 산출물 위치 | status |
|------|-----------|--------|
| 1. 처음 알게 된 것 | `{프로젝트}/insights/{날짜}-{주제}.md` | pending |
| 2. 예상과 다른 결과 | `{프로젝트}/insights/{날짜}-{주제}.md` | pending |
| 3. 다음에 다르게 할 점 | `{프로젝트}/insights/{날짜}-{주제}.md` | pending |
| 4. 다른 프로젝트 적용 가능성 | `{프로젝트}/insights/{날짜}-{주제}.md` (프론트매터에 `cross_project: true`) | pending |
| 5. 절대 다시 하지 말 패턴 | `{프로젝트}/insights/{날짜}-{주제}.md` (failure 태그) | pending |

모든 답변은 처음에 `status: pending`으로 시작한다. confirmed/rejected
전환 규칙은 §4.2 참조.

## 6.4 운영 순서

1. 사이클 종료
2. cycles 파일 작성 완료 (사실 기록)
3. 5가지 질문에 답
4. 답변별로 insights 파일 생성 (status: pending)
5. 질문 4번 답이 "있다"면 해당 insights 프론트매터에 `cross_project: true` 추가

## 6.5 §4 승격 트리거 (재확인)

§6에서 생성된 insights는 §4 학습 흐름을 따른다:

- 같은 프로젝트 내 confirmed insights 3건 이상 → synthesis 생성
- 서로 다른 프로젝트 간 confirmed insights 2건 이상 → 횡단 synthesis 생성
- synthesis가 "X 상황에서는 Y 한다" 형태로 단언 가능 → playbook 승격

상세 규칙은 §4.3, §4.4 참조.

## 6.6 주의

- 5가지 질문에 답하지 않은 사이클은 §4 학습 흐름에 들어가지 않는다
- 답변은 추측이 아닌 사이클 중 실제 관찰한 것만 적는다
- 질문 4번에 "있다"고 답해놓고 `cross_project: true` 표시를 빠뜨리면 횡단 학습이 누락된다

---

# 7. 에이전트 간 인사이트 참조

> [!warning] 미완성
> 다음 세션에서 작성 예정.
> 합의 사항:
> - 원본 직접 안 읽고 synthesis/playbook만 참조 (옵션 라)
> - 예외: 정찰 위탁(B-J) 시 한정 권한
> - sales 정기 산출물: conversion-report-YYYYMM.md (월 1회)
> - 자율 발굴 영역 정의는 _shared/scout-territories.md 참조

---

# 8. 위임 프레임워크 적용

## 8.1 목적

에이전트의 작업을 어떤 도구에 맡길지(또는 사장님이 직접 처리할지) 정한다.
판단 기준은 5가지 질문과 위험신호다. §0.2 자가수정 금지 원칙은
위임 여부와 무관하게 유지된다.

## 8.2 5가지 질문

작업을 위임할지 결정할 때 다음 5가지를 묻는다. 각각 Yes/No로 답한다.

1. **정답 명확성** — 정답이 하나로 명확한가?
2. **안전성** — 실수해도 되돌릴 수 있는가?
3. **반복성** — 같은 작업이 반복되는가?
4. **비창의성** — 창의적 판단이 필요 없는가?
5. **검증 가능성** — 결과를 자동으로 검증할 수 있는가?

## 8.3 통과 기준

5가지 질문에 대한 Yes 개수로 위임 여부를 결정한다.

| Yes 개수 | 판단 | 검증 비율 |
|---|---|---|
| 5 | 위임 OK | 5~10% |
| 4 | 검토 후 위임 | 20~30% |
| 3 이하 | Claude 직접 | — |

**위험신호 — Yes 개수와 무관하게 위임 금지:**
- 결제
- 리드
- 고객 응대
- SEO
- 법적 영향

## 8.4 위임 대상

| 대상 | 용도 |
|---|---|
| 로컬 Ollama (Qwen3:14b) | 단순 변환·요약·분류 |
| Groq LLaMA3.3 70B | 고품질 추론·생성 |
| n8n | 트리거·스케줄·다단계 워크플로 |

> Claude Code Haiku의 위임 대상 포함 여부는 추후 확인 후 결정.

## 8.5 참조 파일

위임 작업 정의 시 다음 파일을 사용한다. 모두 `_shared/` 하위에 있다.

| 파일 | 용도 |
|---|---|
| `_shared/delegation-template.md` | 단편 작업 위임 시 복사해서 작성 |
| `_shared/workflow-template.md` | 여러 단편이 엮인 자율 워크플로 명세 |
| `_shared/security/delegation-blacklist.md` | 🔴 위임 금지 항목 |
| `_shared/security/approval-required.md` | 🟡 승인 필요 항목 |
| `_shared/security/auto-allowed.md` | 🟢 자동 허용 항목 |

**작성 순서:** delegation-template (단편) → workflow-template (자율). 역순 불가.

## 8.6 주의

- 위임된 결과물도 §0.2 보호 대상(자신의 시스템 프롬프트, SKILL.md,
  다른 에이전트의 wiki·raw·SKILL.md, CLAUDE.md, `_shared/` 하위)을
  자동으로 수정할 수 없다. 사람(경년님) 승인 후에만 반영한다.
- 위험신호 5종은 Yes 개수와 무관하게 위임 금지다. 우회 금지.
- 5가지 질문의 답은 운영하면서 다듬을 수 있다. 현재는 출발점.

---

# 9. 사이클 생애주기

## 9.1 목적

사이클이 지금 어느 단계인지 추적하고, 종료·취소·재개를 명확히 한다. 상태 라벨은 §5 워크플로우와 짝으로 움직인다(§9는 라벨, §5는 그 라벨에 도달하기 위한 작업).

## 9.2 상태 흐름

started → in-progress → completed → measured → archived
| 상태 | 의미 |
|------|------|
| `started` | 사이클 시작 선언, 목표·범위 확정 |
| `in-progress` | 본 작업 진행 중 |
| `completed` | 본 작업 산출물 완료 |
| `measured` | §5 측정 단계 완료, 결과값 기록됨 |
| `archived` | §5의 사이클 종료 절차 모두 완료, 사이클 종결 |

**각 상태 전이는 §5 워크플로우의 해당 단계 완료를 전제로 한다.** 단계별 정의·통과 조건은 §5에서 정한다.

## 9.3 중도 취소

- 어느 상태에서든 사이클을 닫아야 할 때 사용
- `status = cancelled`로 변경
- `cancel-reason` **필수** 기록 (다음 사이클이 같은 함정에 빠지지 않도록)

## 9.4 cycle_kind (사이클 종류)

| 종류 | 용도 |
|------|------|
| `regular` | 일반 정기 사이클 |
| `batch` | 다수 항목 일괄 처리 |
| `audit` | 점검·감사 사이클 |
| `adhoc` | 일회성 임시 작업 |
| `builder` | 구축·세팅 사이클 (data 한정 + scout) |

## 9.5 자율 발굴 두 층 구조

- **정찰 사이클**: 발굴 후보 탐색 자체가 목적인 사이클
- **정식 사이클**: 정찰에서 나온 후보 1건당 1개씩 진행

→ 정찰과 정식을 섞지 않는다. 정찰 결과가 곧장 작업으로 흐르면 사이클 경계가 무너진다.

## 9.6 initiative 단위

WF-VI처럼 여러 사이클이 묶이는 대형 작업은 `initiative`로 묶는다. 각 사이클은 `initiative` 안에서 자기 상태를 따로 추적한다.

---

# 10. 민감정보 처리

이 섹션은 vault에 저장해도 되는 정보와 저장해서는 안 되는 정보의 기준을 정의한다.

## 10.1 절대 저장 금지

아래 항목은 vault 어디에도 저장하지 않는다. 요약·마스킹 여부 무관.

- 비밀번호 (서비스 로그인, DB, API 게이트웨이)
- API 키 / 토큰 / 시크릿 (Supabase, OpenAI, Vercel, GitHub 등)
- 고객 개인정보 (실명, 연락처, 이메일, 차량번호 등)
- 매출 절대액 (특정 거래 단위 또는 월·연 매출 총액)

## 10.2 마스킹 후 저장 가능

아래 형태로 변환한 뒤에는 학습 노트에 포함할 수 있다.

- 가격 범위 (예: "30~50만 원대" — 구체 금액 아님)
- 트렌드 비율 (예: "전월 대비 +12%" — 절대액 미포함)
- 익명화 사례 (특정 고객 식별 불가 수준으로 가공)

## 10.3 GitHub 푸시 전 lint

vault 커밋·푸시 전 민감정보 패턴 포함 파일이 없는지 확인한다.

- 점검 대상: `*.md`, `*.yaml`, `*.json` (vault 내 모든 텍스트 파일)
- 점검 명령: `grep -r "sk-\|eyJ\|ghp_\|supabase\|password" . --include="*.md" -l`
- 위반 발견 시: 해당 파일 수정 → 재점검 → 커밋 진행

## 10.4 로컬 민감정보 보관소

vault 외부에 민감정보를 보관할 경우 `.cadam-secrets/` 디렉토리를 사용한다.

- 위치: `~/projects/_meta/agents/.cadam-secrets/` (로컬 전용)
- 현재 상태: 폴더 미생성, `agents/.gitignore` 패턴 미등록
- **별도 작업 필요**: `agents/.gitignore`에 `.cadam-secrets/` 패턴 추가 후 사용

---

# 11. index.md 형식

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

---

# 12. log.md 형식

각 에이전트 vault의 `wiki/log.md` 는 **그 에이전트의 시간순 변경 기록**이다.
append-only, 최신이 위로.

## 12.1 운영 원칙

- 위치: `{agent}/wiki/log.md` (9개 에이전트 각각 1개)
- 갱신 주체: 에이전트 본인
- 갱신 방식: append-only (기존 엔트리 수정 금지, 최신을 맨 위에 추가)
- 모든 wiki 변경은 log에 1엔트리 이상 남긴다

## 12.2 프론트매터

```yaml
---
title: "{agent} 에이전트 wiki 변경 로그"
type: log
status: active
created: YYYY-MM-DD
agent: {agent}
---
```

## 12.3 엔트리 양식

```markdown
## [YYYY-MM-DD] 타입 | 한 줄 제목
요약 2~3줄. 무엇을 왜 변경했는지.
영향받은 페이지: [[페이지1]], [[페이지2]], ...
```

- 날짜는 KST 기준
- 타입은 §12.4의 8종 중 하나
- 영향받은 페이지는 위키링크로 명시

## 12.4 타입 8종

| 타입 | 의미 |
|------|------|
| `cycle-start` | 사이클 시작 |
| `cycle-end` | 사이클 종료 (산출물 박제 포함) |
| `insight-promotion` | insight status 변경 (pending → confirmed/rejected) |
| `synthesis` | 횡단 분석 생성 |
| `playbook-promotion` | playbook Tier 승격/강등 |
| `skill-promotion` | 프로젝트 학습 → _skill 직무 학습 승격 |
| `lint` | 모순·고아·누락·오래됨 점검 |
| `update` | 기타 수정 (양식 변경, 오타 수정 등) |

## 12.5 영향받은 페이지 표기

- 위키링크 `[[]]` 사용
- 풀 경로 또는 슬러그만 (옵시디언이 해결)
- 2개 이상이면 쉼표로 구분
- 인덱스 갱신 포함 시 `[[index]]` 명시

## 12.6 보존 기간

영구 보존. 삭제 금지. 자동 정리 대상 아님.

오래된 엔트리는 별도 `log-archive-YYYY.md` 로 이관 가능 (선택사항).

---

# 13. 안전 규칙

이 섹션은 vault 운영 시 지켜야 할 **불변 원칙**과, 위임 관련 **상세 규칙 파일의 인덱스**를 제공한다.

## 13.1 vault 운영 5대 원칙

1. **raw 불변 원칙** — `data/raw/` 하위 파일은 수정·삭제 금지. 가공은 `processed/`로 복사 후.
2. **wiki 수정 전 한국어 이유 명시** — `wiki/index.md` / `wiki/log.md` 변경 전 사유를 한국어로 먼저 기록.
3. **자가수정 금지** — 에이전트는 자기 `SKILL.md` / `wiki/` / `CLAUDE.md`를 수정 못 함 (§0.2).
4. **5+ 변경 시 사전 공유** — 한 번에 5개 이상 변경 시 실행 전 변경 목록 공유 + 합의.
5. **삭제 시 로그 기록** — 모든 삭제는 `wiki/log.md`에 일자·대상·사유 기록.

## 13.2 위임 안전 규칙 (3계층)

위임 가능 여부는 아래 3개 파일에서 정의된다. 모호하면 항상 **더 보수적인 쪽**을 따른다.

| 계층 | 파일 | 줄수 | 내용 |
|------|------|------|------|
| 절대 금지 | [`_shared/security/delegation-blacklist.md`](_shared/security/delegation-blacklist.md) | 28 | DB 파괴 / 고객·리드 데이터 / 파일·환경 / 외부 실거래 |
| 사전 승인 | [`_shared/security/approval-required.md`](_shared/security/approval-required.md) | 51 | 마스터 데이터 / 차량 이미지 본 컬럼 / 콘텐츠 발행 / 대량 작업 / 버전 관리 / 승인 메시지 형식 |
| 자동 허용 | [`_shared/security/auto-allowed.md`](_shared/security/auto-allowed.md) | 26 | 데이터 수집 / 결과 저장 / 알림 / 이미지 처리 |

판단 순서:
1. blacklist 해당? → 중단
2. approval-required 해당? → 사용자 승인 대기
3. auto-allowed 해당? → 자동 실행

## 13.3 수정 체크리스트

CLAUDE.md / SKILL.md / 핵심 양식 파일을 수정할 때는 [`_shared/modification-checklist.md`](_shared/modification-checklist.md)를 따른다.

## 13.4 위반 시 처리

위 원칙 위반 (또는 위반 의심) 시: 즉시 중단 → 해당 에이전트 `wiki/log.md`에 기록 → 사용자 보고 후 복구 합의.

---

# 14. Obsidian 호환

이 vault는 Obsidian으로 직접 열어 그래프뷰·Dataview·백링크를 활용한다. 모든 페이지는 아래 4가지 양식을 준수한다.

## 14.1 링크 양식

vault 내부 참조는 **위키링크**, 운영 문서는 **마크다운 링크**로 작성한다.

- **위키링크 `[[경로]]`** — 학습 노트와 vault 내부 자산: `wiki/index.md`, `wiki/log.md`, `raw/cycles/`, `_shared/templates/` 등. 그래프뷰·백링크가 동작해야 하는 모든 페이지.
- **마크다운 링크 `[표시](경로)`** — 운영 문서: CLAUDE.md, README.md, 각 에이전트의 SKILL.md, `_shared/security/`. GitHub 웹뷰·모바일 cat에서도 동작해야 하는 페이지.
- vault 외부 자산(Supabase URL, 외부 사이트 등)은 §2.6 참조.

## 14.2 콜아웃 문법

Obsidian 콜아웃은 `> [!타입]` 문법으로 작성한다.

[!note] 메모
본문…
[!warning] 경고
본문…
지원 타입: `note` / `info` / `tip` / `warning` / `danger` / `important` / `example`.

언제 어떤 콜아웃을 쓰는지(가설은 `[!note]`, 모순은 `[!warning]` 등)는 §3.12 참조.

## 14.3 프론트매터 (YAML)

모든 페이지는 YAML 프론트매터로 시작한다. 구체 키 표준은 **§11.2(index.md)**, **§12.2(log.md)** 참조. 페이지 타입별 추가 키는 §3.4~§3.10 참조.

공통 원칙:
- 모든 키는 Dataview 쿼리에서 정렬·필터 가능해야 한다.
- 날짜는 `YYYY-MM-DD`, 리스트는 YAML 배열, 불리언은 `true`/`false`.
- 페이지 타입(`type:`)은 다음 중 하나: `index` / `log` / `cycle` / `insight` / `synthesis` / `playbook` / `failure` / `concept` / `entity` / `project-ref` / `scout-candidate`.
- 새 키·새 타입을 추가할 때는 §11.2 또는 해당 §3.X를 먼저 갱신한다.

## 14.4 이미지 참조

이미지는 vault 내 `assets/` 폴더에 저장하고 위키링크로 참조한다.

- 권장: `![[assets/diagram.png]]`
- 비권장: `![diagram](assets/diagram.png)`

대용량 이미지(>1MB)나 빈번한 업데이트가 예상되는 이미지는 vault에 박지 말고 외부 CDN(Supabase Storage 등) URL 사용 권장. 외부 자산 참조 양식은 §2.6 참조.

---

# 15. 에이전트별 특화 규칙

이 CLAUDE.md는 vault 공통 규칙이다.
에이전트별 업무 프로세스·산출물·KPI·경계는 각 `{에이전트}/SKILL.md` 참조.

자율 발굴 영역 정의는 `_shared/scout-territories.md` 참조.
에이전트 간 경계는 `_shared/boundary-rules.md` 참조.
