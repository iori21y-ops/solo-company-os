---
title: "marketing cycle 양식"
type: template
target_agent: marketing
status: confirmed
created: 2026-05-26
---

# marketing cycle 양식

marketing 에이전트의 사이클은 다음 양식을 따른다.
파일명: `raw/cycles/{프로젝트}/cycle-NNN-{슬러그}.md`

## 프론트매터

```yaml
---
title: "사이클 제목 (한국어)"
type: cycle
status: started | in-progress | completed | measured | archived | cancelled
created: YYYY-MM-DD
cycle_id: NNN
agent: marketing
project: cadam
cycle_kind: regular | batch | adhoc | scout
trigger_source: human | content | sales | self | schedule
channel: blog | naver-blog | youtube-shorts | instagram | cardnews | infographic
target_topic: "주제 한 줄"
estimated_tier: 1 | 2 | 3
triggered_by: []
parallel_with: []
follow_up_to: []
related_assets: []
related_scouts: []
---
```

## 1. 배경

이 사이클을 왜 시작했는가? 어떤 신호가 트리거했는가?

- 트리거 출처: (human 요청 / content 위탁 / sales 데이터 / 자체 발굴 / 정기 스케줄)
- 직전 사이클·인사이트와 어떤 관련이 있는가
- 기대하는 결과 한 줄

## 2. 입력

작업 시작 시 참조한 학습 데이터·자산·외부 정보.

- 참조 wiki 페이지: `[[]]` (insights / playbooks / syntheses)
- 참조 자산: `[[]]` (content/assets/, builders/)
- 참조 외부 자료: second-brain 페이지, URL, Supabase 쿼리

## 3. Tier 판정

- 사업적합도 (Q1): yes / no
- 전환력 (Q4): yes / no
- 타깃일치 (Q5): yes / no

Q1+Q4+Q5 모두 yes → Tier 1 (풀제안서)
2개 yes → Tier 2 (간이 제안)
1개 이하 → Tier 3 (스킵 또는 보류)

판정 근거 한 줄.

## 4. 산출물

채널별 결과물. 발행처와 링크.

- 채널: (블로그/네이버블로그/Shorts대본/카드뉴스/인포그래픽 등)
- 발행 위치: URL 또는 경로
- 파일 경로: `content/assets/{프로젝트}/...`
- 발행 일시: YYYY-MM-DD HH:MM

## 5. 노출 측정 (사이클 종료 시점)

발행 직후 측정 가능한 노출 지표만. 전환·매출은 sales 영역.

- 조회수, 도달, 노출
- 채널별 KPI에 따라 다름

## 6. 학습 추출 (5질문)

§6 학습 추출 가이드의 5질문에 답한다.

1. 이번 사이클에서 처음 알게 된 것이 있는가?
2. 예상과 다른 결과가 나온 부분이 있는가?
3. 다음 사이클에서 다르게 할 점이 있는가?
4. 다른 프로젝트에서도 적용될 가능성이 있는가?
5. 절대 다시 하지 말아야 할 패턴이 있는가?

→ 인사이트 후보 박제 위치: `wiki/{프로젝트}/insights/insight-{슬러그}.md` (status: pending-review)

## 7. 참조 sales 산출물

전환·매출 측정은 sales가 별도 박제하는 `synthesis-conversion-report-YYYYMM.md`를 참조한다.
이 사이클에서 직접 sales 데이터를 끌어오지 않는다.

## 관련 페이지

- 트리거 사이클: `[[]]`
- 산출 인사이트: `[[]]`
- 참조한 sales 산출물: `[[]]`
