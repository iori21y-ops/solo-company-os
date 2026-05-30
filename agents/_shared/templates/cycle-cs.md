---
title: "cs cycle 양식"
type: template
target_agent: cs
status: confirmed
created: 2026-05-30
---

# cs cycle 양식

cs 에이전트의 사이클은 다음 양식을 따른다.
파일명: `raw/cycles/{프로젝트}/cycle-NNN-{슬러그}.md`

## 프론트매터

```yaml
---
title: "사이클 제목 (한국어)"
type: cycle
status: started | in-progress | completed | measured | archived | cancelled
created: YYYY-MM-DD
cycle_id: NNN
agent: cs
project: cadam
cycle_kind: regular | batch | adhoc | scout
trigger_source: human | customer | dealer | sales | schedule
inquiry_type: pre-delivery | post-delivery | complaint | renewal | general
urgency: high | medium | low
triggered_by: []
parallel_with: []
follow_up_to: []
related_assets: []
related_scouts: []
---
```

## 1. 배경

이 사이클을 왜 시작했는가? 어떤 신호가 트리거했는가?

- 트리거 출처: (고객 문의 유입 / 딜러 불만 전달 / 계약 만료 접근 / sales 인계 / 정기 스케줄)
- 직전 사이클·인사이트와 어떤 관련이 있는가
- 응대 목표 한 줄

## 2. 입력

응대 시작 시 참조한 데이터·자산·정보.

- 참조 wiki 페이지: `[[]]` (insights / playbooks / syntheses)
- 참조 CRM 데이터: 고객 이력, 계약 정보
- 참조 sales 룰: sales가 제공한 스코어링·우선순위 룰

## 3. 문의 분류

이번 사이클에서 처리하는 문의를 분류한다.

- 유형: 출고 전 / 출고 후 / 컴플레인 / 갱신 / 일반
- 긴급도: high / medium / low
- 에스컬레이션 필요 여부: yes / no
- 분류 근거 한 줄

## 4. 산출물

응대 결과물. 외부 발송 대상(최종 발송은 사람 승인 후).

- 산출물 종류: (응대 초안 / FAQ 갱신 / 컴플레인 분류·에스컬레이션 / 갱신 안내 / 만족도 설문)
- 발송 채널: (카카오톡 / 전화 / 이메일 / 디스코드 보고)
- 파일 경로: `content/assets/{프로젝트}/...` (해당 시)

## 5. 응대 결과

처리 결과 기록.

- 해결 여부: 해결 / 미해결 / 에스컬레이션
- 응답 시간: (첫 응답까지 소요 시간)
- 고객 반응: (만족 / 보통 / 불만)
- sales에 공급할 피드백 요약

## 6. 학습 추출 (5질문)

§6 학습 추출 가이드의 5질문에 답한다.

1. 이번 사이클에서 처음 알게 된 것이 있는가?
2. 예상과 다른 결과가 나온 부분이 있는가?
3. 다음 사이클에서 다르게 할 것이 있는가?
4. 다른 프로젝트에서도 적용될 가능성이 있는가?
5. 절대 다시 하지 말아야 할 패턴이 있는가?

→ 인사이트 후보 박제 위치: `wiki/{프로젝트}/insights/insight-{슬러그}.md` (status: pending-review)

## 7. 참조 sales 룰

sales가 제공한 스코어링 룰·응대 우선순위를 이번 응대에 적용했는지 기록.

- 적용한 sales 룰: `[[]]`
- 미적용 사유 (있을 경우):

## 관련 페이지

- 트리거 사이클: `[[]]`
- 산출 인사이트: `[[]]`
- 참조한 sales 룰: `[[]]`
- 인계 대상 (sales/marketing): `[[]]`
