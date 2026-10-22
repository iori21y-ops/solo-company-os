---
title: 쏘렌토 HEV 트림별 시세 비교 — Instagram 카드뉴스 발행
cycle_kind: adhoc
channel: instagram
target_topic: "쏘렌토 HEV 트림별 시세 비교 카드뉴스 Instagram 발행 (주기A)"
created: 2026-06-10
status: cycleC-closed-20260706
tier: 1
gate1_passed: true
gate2_status: gate2-approved-20260610
publish_date: 2026-06-09
d7_measured_at: 2026-06-15
d7_verdict: yellow-closed-unmeasured
---

# cycle-004 — 쏘렌토 HEV 트림별 시세 비교 인스타 카드뉴스

## 배경

마케팅 요청 → content 에이전트가 HTML 렌더(6슬라이드, 1080×1080px) 완성.
content 결재 대기 중. 통과 시 marketing gate2(외부 발행 직전) 즉시 진행.

## 소스 자산 (content approved)

| 자산 | 경로 | 상태 |
|------|------|------|
| 카드뉴스 카피 | `content/outputs/approved/cardnews-sorento-hev-trim-20260609.md` | ✅ approved |
| 비주얼 스펙 | `content/outputs/approved/vizsrc-sorento-hev-trim-20260609.md` | ✅ approved |
| HTML 렌더 | `content/outputs/approved/cardnews-sorento-hev-trim-20260610.html` | ✅ approved |

## 데이터 게이트

`kia-sorento-hev | used_price_db_recount | green ✅`

## Marketing 산출물

| 산출물 | 경로 | 상태 |
|--------|------|------|
| Instagram 캡션 | `marketing/outputs/pending/caption-ig-sorento-hev-trim-20260610.md` | ⏳ gate2 대기 |

## Gate 2 조건

content HTML 렌더 approved/ 이동 확인 → gate2 상신 즉시 진행.

gate2 패키지:
1. 렌더 파일 경로 (approved 이동 후): `content/outputs/approved/cardnews-sorento-hev-trim-20260610.html`
2. Instagram 캡션: `marketing/outputs/pending/caption-ig-sorento-hev-trim-20260610.md`
3. 채널: Instagram 단독 (블로그 병행 승인 없음)
4. 업로드 방식: 사람이 직접 (브라우저에서 각 카드 스크린샷·크롭 → 인스타 업로드)

## 주기C (D+7 측정)

발행일 + 7일 후 노출(조회·도달·노출) 측정 → sales 전환분석 핸드오프.

---

## §5 D+7 노출 측정 결과 (2026-06-15, DATA-20260614-0009)

> 소스: `[[data/outputs/pending/conversion-sorento-hev-trim-ig-20260615]]` · verdict: 🟡 yellow

### 5-1. DB 기반 전환 (측정 완료)

| 지표 | 값 | 비고 |
|------|-----|------|
| 기간 내 총 상담 | 2건 | 쏘렌토·Instagram 무관 |
| utm_source=instagram 상담 | **0건** | CTA 직접 전환 없음 |
| 쏘렌토 HEV 상담 | **0건** | |
| 직전 기간(D-7~D-1) 상담 | 0건 | 절대치 비교 불가 |

### 5-2. Instagram Insights (수동 확인 필요 ⚠️)

| 지표 | 값 | 상태 |
|------|-----|------|
| 도달(Reach) | — | ❌ 수동 미확인 |
| 노출(Impressions) | — | ❌ 수동 미확인 |
| 저장(Saves) | — | ❌ 수동 미확인 |
| 공유(Shares) | — | ❌ 수동 미확인 |
| 좋아요+댓글(Engagement) | — | ❌ 수동 미확인 |
| 매물 페이지 클릭(CTA) | — | ❌ 인프라 없음 |

> ⚠️ **수동 확인 필요**: Instagram 앱 → 인사이트 탭에서 위 수치 직접 확인 후 이 표에 기입 바람.
> 도달 500+ 이면 동일 포맷 반복 권장. 미확인 시 주기B Tier Q4 반영 불확실.

### 5-3. 주기B Tier Q4 환류 신호

| 신호 | 판단 |
|------|------|
| DB 직접 리드 | 0건 — 전환 없음 확인 (측정 완료) |
| 포맷 효과 | 판단 불가 — Insights 미확인 |
| 반복 발행 권고 | 보류 — Insights 도달 수치 확인 후 결정 |
| 인프라 개선 필요 | Instagram API + 사이트 페이지뷰 수집 (대표님 결정 대기) |

**verdict yellow 사유**: 상담 전환 0건은 사실이나, 카드뉴스→페이지 유입 구간 미측정으로 "전환 없음"과 "측정 불가"를 구분할 수 없음. Insights 수동 확인 후 Q4 반영 판단.

*측정: 마케팅 2026-06-15 | 소스: data/outputs/pending/conversion-sorento-hev-trim-ig-20260615*

---

## §5-4. 주기C 정기 재점검 (2026-07-06, D+27)

발행(2026-06-09) 후 27일 경과. D+7 1차 측정(6-15) 이후 Instagram Insights 수동 확인이 3주+ 미이행 상태로 확인.

### 재확인한 사실
- `.env`(`~/projects/cadam/cadam-n8n/.env`) 재확인 결과 `META_ACCESS_TOKEN`·`IG_USER_ID` 여전히 미발급 — cycle-003 이후 자동 수집 경로 없음 (2026-06-09, 06-10 결정 요청 두 건 모두 pending-approval 상태로 미종결).
- DB 기반 전환(§5-1)은 재변동 요인 없음 — utm_source=instagram·쏘렌토 HEV 상담 여전히 0건 (data 재조회 없이는 D+27 누적치 미확인, 필요 시 데이터 에이전트에 재조회 요청 가능).
- Instagram 앱 자체 포스트 인사이트는 시간 경과와 무관하게 조회 가능하므로 "기간 만료로 측정 불가"는 아님 — 단지 수동 입력 담당자가 아직 확인·기입하지 않은 상태.

### 마케팅 판단 (측정 범위 내)
- 노출 지표(도달·노출·저장 등) 없이는 "포맷 자체의 효과"를 판단할 수 없어 verdict를 yellow에서 확정하지 못함.
- DB 전환 0건은 사실로 확정 — 쏘렌토 HEV/Instagram 단일 채널·단일 CTA 구조로는 직접 리드 전환 신호가 약함 (참고 신호로 주기B Tier Q4에 반영: "가격비교형 카드뉴스+Instagram 단독 CTA는 반복 전 Insights 검증 필요").
- sales 핸드오프(§7.4): DB 전환 0건이라 분석 대상 실질 없음 — 별도 conversion-report 상신 생략. Insights 확보 후 유의미한 수치 나오면 그때 핸드오프.

### [ESCALATE] 필요 결정 (3주+ 미해결 반복 사안)
1. **Instagram Insights 수동 확인**: 대표님/담당자가 CADAM 인스타 앱 → 해당 포스트 인사이트에서 도달·노출·저장·공유 수치를 직접 확인해 본 cycle §5-2 표에 입력해 주셔야 verdict 확정 가능.
2. **자격증명 프로비저닝 재확인**: `META_ACCESS_TOKEN`/`IG_USER_ID` 발급 진행 여부 — 2026-06-09/06-10 두 차례 결정 요청이 여전히 pending. 프로비저닝 담당자 지정 또는 보류 결정 필요 (PUBLISH-SOP.md §1-A).
3. 위 두 건이 다음 주기까지도 미결이면, 마케팅은 이 cycle을 "verdict: red (측정 인프라 부재로 반복 비권장)"로 자체 종결하고 주기B Tier Q4에 반영할 예정 — 이견 있으시면 회신 바랍니다.

*재점검: 마케팅 2026-07-06 (주기C 정기)*

---

## §5-5. 결정 승인 및 cycle 종결 (2026-07-06)

`decision-결정-요청-20260706.md` (3차 재상신) 대표님 승인 확인 — `outputs/approved/`로 이동 완료.
관리팀장 전달 통보는 "승인 — 다음 단계 진행"만 명시, ①Insights 수동확인 / ②자격증명 A·B·C 중 어느 항목이 선택됐는지는 특정되지 않음.

**해석과 진행 (근거 명시, 이견 시 정정 요청)**
- 세부 옵션 미특정 상태에서 "포맷 자체가 효과 없다"는 결론을 내리는 것은 근거 초과 판단이라 판단(§5-2에서 이미 "전환없음"과 "측정불가"를 구분 불가라 명시함). 따라서 verdict는 **red(반복 비권장)로 격상하지 않음.**
- 승인을 "이 cycle을 더 이상 미결 상태로 끌지 말고 현재 확보한 근거로 종결하라"는 의미로 해석해 cycle을 종결 처리함.

**최종 verdict: yellow → 측정 미이행 종결 (gray-미측정)**
- DB 기반 전환: 0건 확정 (사실, §5-1) — 참고 신호로만 사용.
- Instagram Insights(도달·노출·저장): 끝내 미확인 — "포맷 효과"에 대한 결론은 유보. red 아님.
- sales 핸드오프: DB 전환 0건이라 conversion-report 상신 생략 (기존 판단 유지).

**주기B Tier Q4 환류 문구(확정)**: "가격비교형 카드뉴스 + Instagram 단독 CTA, cycle-004(쏘렌토 HEV): DB 직접 리드 0건(참고용, 결론 아님) / 노출 효과는 Insights 미확보로 판단 보류. 포맷 반복 여부에 대한 결론은 내리지 않음 — 향후 Insights 확보 시 재평가 필요."
- 자격증명(META_ACCESS_TOKEN/IG_USER_ID) 프로비저닝은 이번 승인으로 A/B 중 확정된 바 없어 **미해결 상태 유지** — 다음 Instagram 카드뉴스 주기(cycle-001 장기렌트 등)에서 동일 수동확인 이슈가 재발할 수 있음을 기록해 둠. 재발 시 이번처럼 반복 escalate하지 않고, 이 결정(§5-5) 기준대로 "미측정 종결"로 처리 예정.

**cycle 상태: closed (archived 대기)**

*종결: 마케팅 2026-07-06*
