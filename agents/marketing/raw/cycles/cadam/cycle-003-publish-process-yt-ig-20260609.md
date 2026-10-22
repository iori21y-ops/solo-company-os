---
title: "유튜브 Shorts + 인스타그램 발행 프로세스 구현"
type: cycle
status: in-progress
created: 2026-06-09
cycle_id: "003"
agent: marketing
project: cadam
cycle_kind: adhoc
trigger_source: human
channel: [youtube-shorts, instagram]
target_topic: "유튜브·인스타그램 발행 파이프라인 SOP + 체크리스트 완성"
estimated_tier: 1
triggered_by: [대표님]
parallel_with: []
follow_up_to: [cycle-002-topic-scout-20260602]
inputs:
  - marketing/scripts/ig_publish.py (기존 스캐폴드)
  - marketing/scripts/youtube_publish.py (기존 스캐폴드)
related_assets: []
related_scouts: []
---

# cycle-003 — 유튜브 Shorts + 인스타그램 발행 프로세스 구현

## 1. 배경

- **트리거 출처:** 대표님 직접 지시 (스팟2) — "4번 자료를 활용할 수 있게 유튜브, 인스타그램 발행 프로세스부터 구현하자"
- **기존 현황 파악:** ig_publish.py / youtube_publish.py 스캐폴드 이미 존재. PUBLISH-SOP.md·체크리스트 미생성.
- **기대 결과:** 두 채널 발행 파이프라인 완성 → 이후 모든 콘텐츠(4번 자료 포함)를 이 프로세스로 발행 가능.

## 2. 입력 자산

- `marketing/scripts/ig_publish.py` — Instagram Graph API 2단계 플로우 구현 완료 (자격증명 미발급)
- `marketing/scripts/youtube_publish.py` — YouTube Data API v3 OAuth 업로드 구현 완료 (자격증명 미발급)
- 기존 발행 이력: cycle-001(인스타 카드뉴스), 이후 쏘렌토HEV 인스타 게시 경험

## 3. Tier 판정

- 사업적합도 (Q1): yes — 발행 파이프라인은 모든 마케팅 콘텐츠의 인프라
- 전환력 (Q4): yes — 프로세스 완성 없이는 외부 발행 자체가 불가
- 타깃일치 (Q5): yes — 전 채널 공통 인프라

→ **Tier 1** (인프라 작업이므로 Tier 판정 형식 그대로 적용).

## 4. 산출물

### 4-1. 완성된 파일 목록

| 파일 | 유형 | 상태 |
|------|------|------|
| `marketing/scripts/ig_publish.py` | 스크립트 | 기존 완성 |
| `marketing/scripts/youtube_publish.py` | 스크립트 | 기존 완성 |
| `marketing/scripts/PUBLISH-SOP.md` | SOP 문서 | ✅ 신규 생성 (2026-06-09) |
| `marketing/outputs/pending/checklist-yt-ig-publish-process-20260609.md` | 체크리스트 | ✅ 신규 생성 → 결재 대기 |

### 4-2. 프로세스 요약

```
콘텐츠 준비
  └─ content/approved 소스 확인
  └─ data/verdict green 확인
  └─ 표시광고법 게이트 통과

발행 실행 (채널별)
  ├─ [인스타] ig_publish.py → 컨테이너 생성 → 결재 → --publish
  └─ [유튜브] youtube_publish.py → private 업로드 → Studio 확인 → 결재 → --publish

발행 완료
  └─ cycle §4 URL 기록
  └─ _shared/final 복사
  └─ D+7 주기C 스케줄
```

### 4-3. 자격증명 현황 (2026-06-09 기준)

| 채널 | 상태 | 다음 단계 |
|------|------|----------|
| 인스타그램 | ⚠️ META_ACCESS_TOKEN, IG_USER_ID 미발급 | PUBLISH-SOP.md §1-A 프로비저닝 실행 |
| 유튜브 | ⚠️ YT_OAUTH_TOKEN 미발급 | PUBLISH-SOP.md §1-B OAuth 발급 실행 |

> **자격증명 발급 = 사람이 직접 실행해야 하는 작업 (OAuth 브라우저 인증 포함)**
> → 대표님 또는 담당자가 §1 체크리스트 완료 후 마케팅에 완료 통보 필요.

## 5. 노출 측정

해당 없음 (인프라 사이클 — 발행물 없음).

## 6. 학습 추출

1. 스캐폴드(스크립트)만 있어도 SOP+체크리스트 없이는 운용 불가 → 셋트로 관리해야 함.
2. Meta API는 이미지 직접 업로드 불가(공개 URL 필요) → 이미지 호스팅 인프라 선결 필요.
3. YT 쿼터(일 10,000 units) 제약 → 하루 최대 6건, 예약 발행 전략 필요.
4. OAuth 토큰은 최초 1회 브라우저 인증 → 자동화 파이프라인에 refresh_token 갱신 로직 추가 필요(v2).

## 7. 참조 sales 산출물

없음.
