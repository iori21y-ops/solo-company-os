---
title: "verdict 파일 형식 + content 해금 연결 (MVP)"
type: 합의메모
status: confirmed
date: 2026-06-01
area: meta/agents
관련: content↔data 정합성 verdict 배관 (디스코드 구현 트랙 A안)
---

# 합의 — verdict 파일 형식과 content 해금 연결

## 배경
content SKILL.md 106줄 "정합성 verdict가 green일 때만 초안" 규칙은 있으나,
verdict의 실제 파일 형식·경로·해금 로직이 미정의(_config 5종 audit-rules 전부 draft).
이번 파트는 그 배관을 정의하고, 점검 실물이 이미 있는 1유형(이미지=referential/wf_vi)으로
cycle 1바퀴를 돌려 배관을 검증한다. 나머지 유형 규칙은 후속 파트.

## 데이터 5유형 (기존 박제 재확인)
data/builders/cadam/{quantitative,visual,textual,video}/ + adhoc.
정합성 점검 방식 5종 = _config/audit-rules-{cross-source,internal,referential,semantic,temporal}.md
유형마다 정합성의 본질이 다름:
- 숫자(quantitative): 다중 소스 교차검증 (cross_source/temporal)
- 이미지(visual): 완전성·규격 (referential = 4자정합성 wf_vi)
- 텍스트(textual): 출처 간 의미 일치 (semantic)
- 영상(video): 메타데이터+자막→텍스트화 후 semantic
- 즉석(adhoc): 점검이 아니라 수집·검증 스크립트 신설(builder)

## verdict 파일 스키마 (확정)
경로: data/outputs/pending/ → 관리팀장 경량 승인 → data/outputs/approved/
(SKILL.md 92·96줄 그대로. content는 approved/만 스캔 = SKILL 109줄)
파일명: verdict-{차종슬러그}-{YYYYMMDD}.md

frontmatter:
---
type: verdict
agent: data
subject: hyundai-avante      # 차종 슬러그 = content 매칭 키 (파일명 아님)
data_type: visual            # quantitative|visual|textual|video|mixed
audit_kind: referential      # _config audit-rules 5종과 동일 명칭
verdict: green               # green|yellow|red
checked: 2026-06-01
expires: 2026-07-01          # 기록용. MVP는 검사 안 함(v2)
issues: []                   # yellow/red 시 이슈 목록
source_cycle: null           # TODO: cycle 구현 후 링크 (다음 파트)
---

## 확정 결정
1. content 해금 조건 = verdict: green 단일 검사 (MVP). expires/issues는 기록만.
2. 차종 매칭 = frontmatter subject 필드값 (파일명 한글 깨짐 회피, 저장입구 콘텐츠/컨텐츠 버그 교훈).
3. data_type+audit_kind 필수. content는 자기가 쓸 유형의 green을 봐야 함
   (가격글=quantitative green / 이미지=visual green. 유형 다르면 상호 보증 안 함).
4. source_cycle은 MVP에서 null. 배관 검증 후 cycle 파트에서 채움(학습루프 역추적용, 해금 판정과 무관).

## MVP 범위
1유형(visual/referential=wf_vi) · 1차종(아반떼)으로:
verdict green 산출 → pending → 관리팀장 승인 → approved → content봇이 읽고 초안 1편 → 저장 → 승인 → wp_publish.py 발행.
숫자/텍스트/영상 audit-rules는 후속 파트에서 하나씩.

## 미결 (후속 파트)
- _config 5종 audit-rules 실내용 (무엇이 green/yellow/red인가)
- cycle 템플릿 + source_cycle 실연결
- content봇이 approved/ verdict를 읽어 green 판정하는 코드 (다음 단계 구현 대상)
