---
title: "content cycle 양식"
type: template
target_agent: content
status: confirmed
created: 2026-05-26
---

# content cycle 양식

content 에이전트의 사이클은 다음 양식을 따른다.
content는 재료 공급자 역할. 자율 발굴(J)을 단독으로 수행.

파일명: `raw/cycles/{프로젝트}/cycle-NNN-{슬러그}.md`
정찰 사이클은 `cycle-NNN-scout-{슬러그}.md`

## 프론트매터

```yaml
---
title: "사이클 제목 (한국어)"
type: cycle
status: started | in-progress | completed | measured | archived | cancelled
created: YYYY-MM-DD
cycle_id: NNN
agent: content
project: cadam
cycle_kind: regular | batch | adhoc | scout
trigger_source: human | marketing | sales | strategy | self-scout | schedule
asset_type: infographic | chart | card | fact-block | comparison | report
target_topic: "주제 한 줄"
target_consumer: marketing | sales | strategy | direct-publish
triggered_by: []
parallel_with: []
follow_up_to: []
inputs: []
parent_scout_cycle: []
related_candidates: []
---
```

## 1. 배경

이 사이클을 왜 시작했는가?

- 트리거 출처
- 위탁받았다면 의뢰자와 의뢰 사유
- 자율 발굴이면 어떤 신호로 발굴했는가

## 2. 입력 (정찰)

second-brain 또는 자기 과거 사이클에서 어떤 페이지·데이터를 정찰했는가?

- 정찰 범위
- 발견한 단서들 (인용 또는 링크)
- 자율 발굴 사이클이면 이 섹션이 핵심

## 3. 가설 (제작 전)

만들려는 자산이 다음 조건을 만족하는가?

- **사실 정합성**: 정찰한 데이터가 정확한가
- **활용 가능성**: 누가, 어디서, 어떻게 쓸까
- **재사용성**: 다른 프로젝트·사이클에도 쓰일 가치가 있는가

## 4. 제작

산출물 제작 과정.

- 사용 도구 (Figma / Canva / Playwright / Python 등)
- 제작 단계
- 검토 (사실 검증)

## 5. 산출물

- 자산 파일 경로: `content/assets/{프로젝트}/{유형}/...`
- 자산 메타: 크기, 포맷, 해상도, 사용 가능 범위
- 정합성 검증: data 에이전트에 검증 의뢰 여부

## 6. 비축

자산은 wiki 밖 `assets/{프로젝트}/{유형}/` 에 저장.
재사용 가능하도록 index.md에 등록.

- 등록 위치: `wiki/{프로젝트}/index.md` 또는 `assets/{프로젝트}/{유형}/README.md`
- 태그 부여 (검색용)

## 7. 발견된 후보 (자율 발굴 사이클 한정)

정찰 결과 발굴된 후보들. 각 후보를 `wiki/{프로젝트}/scouts/pending/` 에 페이지로 생성.

- 후보 1: `[[wiki/{프로젝트}/scouts/pending/J-NNN-01-{슬러그}]]`
- 후보 2: ...
- 사람 결정 대기 상태로 박제

## 8. 학습 추출 (5질문)

§6 학습 추출 가이드의 5질문에 답한다.

→ 인사이트 후보 박제 위치: `wiki/{프로젝트}/insights/insight-{슬러그}.md`

## 관련 페이지

- 트리거: `[[]]`
- 산출물: `[[]]`
- 발굴 후보들: `[[]]`
- 산출 인사이트: `[[]]`
