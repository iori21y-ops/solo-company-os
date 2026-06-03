---
title: "마케팅 업무 목록 + 직접 실행·보고 프로세스 (제안서)"
type: process-proposal
status: pending
created: 2026-06-02
author: admin
approver: 대표님
target_agent: marketing
project: cadam
---

# 마케팅 업무 목록 + 직접 실행·보고 프로세스 (제안서)

> 작성: 관리팀장 / 결재: 대표님
> 원칙: 새 분류·새 보고양식을 발명하지 않는다. 기존 SKILL.md(주기A/B)·cycle 템플릿·결재카드 표준에 **앵커링**한다.
> 이 문서는 제안서다. 승인 시 marketing/SKILL.md에 반영한다(아래 §5).

---

## 1. 업무 목록 — 주기(Cycle) vs 스팟(Spot)

### 1-A. 주기 업무 (정기·반복 / `cycle_kind: regular`)

| # | 업무 | 정의 | 트리거 | trigger_source | 결재 게이트 |
|---|------|------|--------|----------------|------------|
| 주기A | **확정 발행계획 실행** | content approved 소스 + data 합본 → 최종물 제작 → 발행 → `_shared/final` 복사 | 발행계획 확정 | content / self | **게이트2(발행 직전, 필수)** — 채널별 차등 |
| 주기B | **신규 주제 발굴·선정** | content 스카우트 후보 + sales conversion-report + 트렌드 → 5질문 Tier 판정 → 확정 발행계획 산출 | 트렌드·캘린더·스카우트 | self / schedule / content | **게이트1(Tier 판정 사람 승인)** + 발행계획 확정 |
| 주기C | **발행 7일 후 노출 측정·환류** | 발행물 노출지표 측정 → sales 전환분석(§7.4)으로 연결 → 다음 주기B Tier Q4 환류 | 발행 D+7 | schedule | 없음(측정·보고) |

### 1-B. 스팟 업무 (일회성·임시 / `cycle_kind: adhoc`)

| # | 업무 | 정의 | 트리거 | trigger_source | 결재 게이트 |
|---|------|------|--------|----------------|------------|
| 스팟1 | **트렌드·이슈 즉응 콘텐츠** | 급상승 키워드·시즌·뉴스 반응형 카피/카드/쇼츠 | 외부 이슈 | self / human | 게이트2(채널별 차등) |
| 스팟2 | **대표님 직접 지시 발행물** | 사장님이 주제·채널을 콕 집어 지시 | human 요청 | human | 게이트2(채널별 차등) |
| 스팟3 | **시즌 캠페인 소재** | 명절·연말·신차 출시 등 일정성 캠페인 | 캘린더 이벤트 | human / self | 게이트2(채널별 차등) |
| 스팟4 | **광고/랜딩 카피 단건** | 특정 광고·랜딩페이지 카피 요청 | human / sales | human | 게이트2(자사 < 광고집행) |

> **스팟 요청 적재 위치:** data의 `_inbox/adhoc-queue.md` 패턴을 마케팅에 동일 적용 →
> `marketing/_inbox/adhoc-queue.md` 신설(승인 시). 사장님·타 에이전트의 스팟 요청을 여기 줄단위로 쌓고, 마케팅이 자기 주기에 pull.

---

## 2. 결재·보고 프로세스 — **이미 구축됨 (재사용)**

새로 만들 것 없음. 아래 3개가 이미 작동하는 보고·결재 인프라다.

### 2-A. 결재 = Discord 결재 카드 (`_shared/approval-card-policy.md`)
- 마케팅 → 관리팀장: `[APPROVAL:관리팀장] 제목 | 요약 | /절대경로/파일`
- 카드 컨트롤 필수: `승인` `수정` `반려` `코멘트`(모달)
- 대표 결재가 필요한 채널은 관리팀장이 `[APPROVAL:대표님]`으로 승급

### 2-B. 보고 = cycle 템플릿의 측정·학습 단계 (`templates/cycle-marketing.md`)
- **§5 노출 측정** — 발행 직후 조회·도달·노출 기록 (전환은 sales 영역)
- **§6 학습 추출(5질문)** → `wiki/{프로젝트}/insights/`
- **status 전이** = 진행상황 보고: `started → in-progress → completed → measured → archived`
- 완료 시 Discord 완료 통지(채널 알림). **별도 보고양식 신설 안 함.**

### 2-C. 결재 게이트 = SKILL.md §결재 게이트 (그대로 유지)
- 주기B 게이트1: Tier 판정 사람 승인(Q1·Q5)
- 발행계획 확정: 명시적 결재 지점
- 주기A 게이트2(발행 직전, 필수): 채널별 강도 차등
  - 자사블로그 < 네이버·인스타·쇼츠 → **후자 3종은 대표 결재**
- 발행 전 stale 자산 차단(만료 content 자산 발행 금지)

---

## 3. "마케팅 직접 실행 → 결과 보고" 표준 루프

> ⚠️ **직접 실행 ≠ 무결재 자동발행.** 외부 노출은 회수 불가하므로 발행 직전 게이트는 *필수*다.
> 마케팅은 **게이트 직전까지 자율 실행**하고, 승인 후 발행한다.

```
1. 트리거 수신        (주기 캘린더 / 스팟 adhoc-queue / 사장님 지시)
2. cycle 파일 개설     raw/cycles/cadam/cycle-NNN-{슬러그}.md  (status: started)
3. 입력 수집·자율 제작  content approved + data approved 합본 → 최종물  (in-progress)
4. pending 저장        outputs/pending/{유형}-{주제}-{YYYYMMDD}.md  (completed)
5. 결재 카드 상신      [APPROVAL:관리팀장] …  → (대표 결재 채널이면 승급)
6. 승인 후 발행        approved/ 이동 → 채널 발행 → _shared/final 복사
7. 결과 보고           cycle §5 노출측정 기록(measured) → Discord 완료통지 → archived
8. 환류(D+7)          주기C로 노출측정 → 다음 주기B Tier Q4 입력
```

---

## 4. 채널별 자가실행 능력 — **정직한 현황** (배선 점검 결과)

"직접 실행"은 실행 능력 전제. 일부 채널은 아직 미배선이므로 구분해 표기한다.

| 채널 | 자가실행 | 비고 |
|------|---------|------|
| 자사 블로그(WordPress) | ⚠️ 부분 | `marketing/scripts/wp_publish.py` 존재. 워크플로우-스크립트 **연결 미검증** |
| 네이버 블로그 | ⚠️ 부분 | `cadam-naver`(post-blog.js, 쿠키인증) 존재. 에이전트-스크립트 **미배선** |
| n8n 파이프라인 | ⚠️ 부분 | GWP/VWP 발행 파이프라인 가동 중이나 에이전트 워크플로우와 **미연결** |
| 인스타/쇼츠/카드뉴스 | ❌ 수동 | 자동 발행 경로 없음. 소재 제작까지만 자가 가능, 발행은 수동 |

> **결론:** 현재는 *제작·결재 상신까지* 완전 자가실행 가능. *발행 단계*는 채널별로 수동 또는 미배선.
> 완전 자동 루프를 그리려면 별도 "발행 배선" 작업(스크립트↔에이전트 연결)이 선행 필요 → 별건 제안.

---

## 5. 승인 후 반영(다음 단계)

- 본 제안서는 마케팅 **업무 정의** 영역이므로 최종 거처는 `marketing/SKILL.md`.
- 관리팀장이 타 에이전트 정의를 무단 개정하지 않는다. **대표 승인 후** SKILL.md §결재·보고·업무흐름에 반영:
  1. 주기C(D+7 노출측정 환류) 명문화
  2. 스팟1~4 + `marketing/_inbox/adhoc-queue.md` 신설
  3. §4 채널 배선 현황을 별건 "발행 자동화" 과제로 등록
- 기존 주기A/B 명칭·게이트는 **변경 없이 유지**(충돌 방지).

---

## 부록: 근거 파일
- `marketing/SKILL.md` §결재·보고·업무흐름 (주기A/B, 게이트)
- `_shared/templates/cycle-marketing.md` (보고 = §5·§6·status)
- `_shared/approval-card-policy.md` (결재 카드 표준)
- `CLAUDE.md` §9.4 cycle_kind / §데이터 `_inbox/adhoc-queue.md`
