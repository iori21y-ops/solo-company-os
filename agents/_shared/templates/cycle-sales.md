---
title: "sales cycle 양식"
type: template
target_agent: sales
status: confirmed
created: 2026-05-30
---

# sales cycle 양식

sales 에이전트의 사이클은 다음 양식을 따른다.
파일명: `raw/cycles/{프로젝트}/cycle-NNN-{슬러그}.md`

## 프론트매터

```yaml
---
title: "사이클 제목 (한국어)"
type: cycle
status: started | in-progress | completed | measured | archived | cancelled
created: YYYY-MM-DD
cycle_id: NNN
agent: sales
project: cadam
cycle_kind: regular | batch | adhoc | scout
trigger_source: human | cs | marketing | self | schedule
analysis_target: lead-scoring | channel-roi | dealer-performance | crm-integrity | kpi-report
triggered_by: []
parallel_with: []
follow_up_to: []
related_assets: []
related_scouts: []
---
```

## 1. 배경

이 사이클을 왜 시작했는가? 어떤 신호가 트리거했는가?

- 트리거 출처: (human 요청 / cs 피드백 / marketing 요청 / 자체 발견 / 정기 스케줄)
- 직전 사이클·인사이트와 어떤 관련이 있는가
- 기대하는 분석 결과 한 줄

## 2. 입력

분석 시작 시 참조한 데이터·자산·외부 정보.

- 참조 wiki 페이지: `[[]]` (insights / playbooks / syntheses)
- 참조 데이터: Supabase 테이블, CRM, Google Sheets
- 참조 cs 피드백: cs가 공급한 고객 반응·컴플레인 패턴

## 3. 분석 범위

이번 사이클에서 분석할 대상을 명시한다.

| 대상 | 이번 사이클 해당 여부 |
|------|----------------------|
| 리드 스코어링 룰 갱신 | yes / no |
| 채널별 ROI 계산 | yes / no |
| 딜러별 성과 분석 | yes / no |
| CRM 정합성 점검 | yes / no |
| 주간/월간 KPI 집계 | yes / no |

분석 범위 선정 근거 한 줄.

## 4. 산출물

분석 결과물. 내부 의사결정용(외부 발송 아님).

- 산출물 종류: (룰 갱신 / 리포트 / 대시보드 갱신 / 이상탐지 결과)
- 파일 경로: `wiki/{프로젝트}/syntheses/...` 또는 `wiki/{프로젝트}/playbooks/...`
- cs·marketing에 공급할 인사이트 요약

## 5. 분석 결과

핵심 수치와 발견.

- 주요 지표 변화 (전환율, 응답률, ROI 등)
- 룰 변경사항 (변경 전 → 변경 후)
- 이상치·특이사항

## 6. 학습 추출 (5질문)

§6 학습 추출 가이드의 5질문에 답한다.

1. 이번 사이클에서 처음 알게 된 것이 있는가?
2. 예상과 다른 결과가 나온 부분이 있는가?
3. 다음 사이클에서 다르게 할 점이 있는가?
4. 다른 프로젝트에서도 적용될 가능성이 있는가?
5. 절대 다시 하지 말아야 할 패턴이 있는가?

→ 인사이트 후보 박제 위치: `wiki/{프로젝트}/insights/insight-{슬러그}.md` (status: pending-review)

## 7. 참조 cs 피드백

cs가 공급한 고객 반응·컴플레인 패턴을 이번 분석에 반영했는지 기록.

- 반영한 cs 피드백: `[[]]`
- 미반영 사유 (있을 경우):

## 관련 페이지

- 트리거 사이클: `[[]]`
- 산출 인사이트: `[[]]`
- 공급 대상 (cs/marketing): `[[]]`
