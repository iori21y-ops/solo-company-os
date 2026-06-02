---
title: "참조 — 페이지 형식 규칙"
type: reference
status: active
source: "CLAUDE.md §3에서 분리 (2026-06-02)"
---

# 페이지 형식 규칙 (CLAUDE.md §3 상세)

## 3.1 공통 프론트매터

모든 wiki 페이지는 YAML 프론트매터로 시작한다.

### 필수 (4개)

```yaml
---
title: "한국어 제목"
type: index | log | cycle | insight | synthesis | playbook | failure | concept | entity | project-ref | scout-candidate
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

- [[_shared/templates/cycle-sales]]
- [[_shared/templates/cycle-cs]]

ops/finance/legal/strategy cycle 양식은 각 에이전트 스텝 정의 완료 후 추가.

cycle 페이지는 raw/cycles/{프로젝트}/ 에 저장. 사이클 진행 사실 기록이며 불변.

## 3.4 insight 페이지
검증된 깨달음 한 조각. 필수 섹션:
- **요지**: 한 줄 핵심
- **근거**: 어떤 사이클·소스에서 나왔나 (링크)
- **적용 범위**: 이 프로젝트 한정인가, 일반화 가능한가
- **반증 조건**: 언제 이 깨달음이 틀리게 되나

## 3.5 synthesis 페이지
여러 인사이트·소스를 묶은 종합 결론. 필수 섹션:
- **결론**: 종합 판단
- **근거 링크**: 묶은 인사이트·소스 목록
- **종합 논리**: 왜 이 결론에 도달했나
- **남은 불확실성**: 아직 확인 안 된 부분

## 3.6 playbook 페이지
반복 작업 실행 매뉴얼. 필수 섹션:
- **목적**: 언제 이 플레이북을 쓰나
- **사전 조건**: 시작 전 갖춰야 할 것
- **단계**: 순서대로 실행 절차
- **성공 기준**: 무엇으로 완료를 판단하나
- **실패 시 대처**: 막혔을 때 행동

## 3.7 failure 페이지
안 된 것 기록. 필수 섹션:
- **시도**: 무엇을 했나
- **결과**: 어떻게 실패했나
- **원인 분석**: 왜 실패했나
- **교훈**: 다음에 무엇을 다르게
- **재시도 조건**: 언제 다시 시도할 가치가 있나

## 3.8 concept 페이지
추상 개념. 필수 섹션:
- **정의**: 개념 설명
- **중요성**: 왜 중요한가
- **관련 링크**: 연결된 엔티티·개념
- 모순되는 정보는 `> [!warning]` 콜아웃으로 표시

## 3.9 entity 페이지
구체적 대상(차량·브랜드·도구). 필수 섹션:
- **정의**: 대상 설명
- **핵심 속성**: 주요 스펙·특징
- **교차참조**: 관련 소스·페이지 링크
- **변경 이력**: 스펙·가격 변경 시 갱신 기록

## 3.10 project-ref / scout-candidate 페이지

### project-ref
프로젝트 현황 참조 카드. 상태 상세는 핸드오프 문서가 source of truth이고 이 카드는 위키 내 연결용 stub만. 필수 섹션:
- **정의**: 프로젝트 한 줄 설명
- **현재 상태**: 한 줄 요약
- **핸드오프 링크**: 상세 문서 위치
- **담당 범위**: 이 에이전트가 맡는 부분

### scout-candidate
검토 후보 메모. 필수 섹션:
- **후보**: 무엇을 검토하나 (한 줄)
- **발견 경위**: 어디서 나왔나
- **우선순위**: 검토 시급도
- **판정일**: status가 confirmed/rejected로 바뀐 날짜

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
