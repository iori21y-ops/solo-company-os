---
title: 외부 발행 SOP — 유튜브 Shorts · 인스타그램
type: sop
owner: marketing
status: active
version: 1.0
created: 2026-06-09
last-updated: 2026-06-09
applies-to: [youtube-shorts, instagram]
---

# 외부 발행 SOP — 유튜브 Shorts + 인스타그램

> **불변 원칙**: 외부 노출은 회수 불가. 발행 직전 게이트(§4)는 긴급해도 생략 금지.

---

## §1. 전제 조건 — 자격증명 프로비저닝

### 1-A. 인스타그램 (Meta Graph API)

| 항목 | 설명 | .env 키 |
|------|------|---------|
| Meta 개발자 앱 | business.facebook.com → 앱 생성 | — |
| 페이스북 페이지 연결 | CADAM 인스타 계정을 FB Page에 연결 | — |
| instagram_content_publish 권한 | 앱 심사 신청 (수일~수주) | — |
| 장기 사용자 액세스 토큰 | 60일 유효. 만료 30일 전 갱신 스케줄링 | `META_ACCESS_TOKEN` |
| 인스타 비즈니스 계정 ID | Graph API `/me?fields=id` 로 확인 | `IG_USER_ID` |

**프로비저닝 체크리스트 (최초 1회)**
- [ ] Meta 개발자 계정 생성 / 앱 등록 (앱 유형: Business)
- [ ] CADAM 인스타 → 전문가 계정(비즈니스/크리에이터) 전환
- [ ] FB 페이지에 인스타 계정 연결
- [ ] `instagram_content_publish` 권한 앱 심사 통과
- [ ] 장기 토큰 발급 → `.env` 에 `META_ACCESS_TOKEN=...` 등록
- [ ] `IG_USER_ID` 확인 → `.env` 에 등록
- [ ] `python3 ig_publish.py --image-url {테스트URL} --caption-file test.txt` 로 컨테이너 생성 테스트 (--publish 없이)

### 1-B. 유튜브 (YouTube Data API v3)

| 항목 | 설명 | .env 키 |
|------|------|---------|
| Google Cloud 프로젝트 | console.cloud.google.com | — |
| YouTube Data API v3 활성화 | API 라이브러리에서 사용 설정 | — |
| OAuth 동의화면 설정 | 스코프: `youtube.upload` | — |
| OAuth 2.0 클라이언트 ID | 앱 유형: 데스크톱 앱 | — |
| 액세스 토큰 발급 | 첫 발급 시 브라우저 인증 필요 (1회) | `YT_OAUTH_TOKEN` |
| 리프레시 토큰 관리 | 액세스 토큰 만료(1h) → refresh_token으로 갱신 | `YT_REFRESH_TOKEN` (선택) |

**프로비저닝 체크리스트 (최초 1회)**
- [ ] Google Cloud 프로젝트 생성
- [ ] YouTube Data API v3 활성화
- [ ] OAuth 동의화면 구성 (테스트 사용자에 CADAM 계정 추가)
- [ ] OAuth 2.0 클라이언트 ID 생성 → `client_secrets.json` 다운로드
- [ ] 최초 인증 실행:
  ```bash
  python3 -c "
  from google_auth_oauthlib.flow import InstalledAppFlow
  flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', ['https://www.googleapis.com/auth/youtube.upload'])
  creds = flow.run_local_server(port=0)
  print('ACCESS:', creds.token)
  print('REFRESH:', creds.refresh_token)
  "
  ```
- [ ] 발급된 토큰 → `.env` 에 `YT_OAUTH_TOKEN=...` 등록
- [ ] `python3 youtube_publish.py --video test.mp4 --title "테스트"` (--publish 없이 private 업로드 확인)

> ⚠️ 일 쿼터: videos.insert = 약 1,600 units/건, 기본 일일 한도 10,000 units → 하루 최대 6건

---

## §2. 콘텐츠 준비 규격

### 2-A. 유튜브 Shorts

| 항목 | 규격 |
|------|------|
| 영상 파일 | MP4, H.264, 최대 60초, 세로(9:16 권장) |
| 해상도 | 1080×1920 (최소 720×1280) |
| 대본 | `shorts-{슬러그}-{날짜}.md` (마케팅 approved/) |
| 제목 | 20자 내외, `#Shorts` 포함 |
| 설명 | 150자 이내, 해시태그 5개 이하, CTA 링크 포함 |
| 파일 저장 위치 | `~/projects/cadam/media/shorts/{슬러그}.mp4` |

### 2-B. 인스타그램

| 콘텐츠 유형 | 규격 |
|------------|------|
| 카드뉴스(캐러셀) | JPEG/PNG, 1:1 또는 4:5, 최대 10장, 각 10MB 이하 |
| Reels(숏폼) | MP4, 최대 90초, 9:16, 최대 1GB |
| 단일 이미지 | JPEG/PNG, 1:1~4:5 |
| 이미지 호스팅 | Meta API는 공개 URL fetch → S3/Cloudflare/GitHub Raw 등에 선호스팅 필요 |
| 캡션 | 2,200자 이하, 해시태그 30개 이하, CTA 명시 |

---

## §3. 발행 직전 게이트 체크리스트

> 파일: `checklist-publish-gate.md` 참조 (산출물 pending/ 저장 시 함께 제출)

**필수 확인 항목 (어느 채널이든 공통)**
- [ ] content approved 소스 유효? (`yellow/pending/hold` = 발행 금지)
- [ ] data verdict 유효? (`green` 확인)
- [ ] 표시광고법 — 가격·수익률·비교 우위 표현 없음?
- [ ] 이미지/영상 저작권 및 초상권 문제 없음?
- [ ] CTA 링크 정상 작동?
- [ ] 결재카드 승인 완료? (마케팅 → 대표님 직접 상신 경로 완료)

**채널별 추가 확인**
| 채널 | 추가 확인 |
|------|----------|
| 인스타그램 | 이미지 공개 URL 유효, 캐러셀 순서 확인 |
| 유튜브 Shorts | 영상 길이 ≤60초, `#Shorts` 제목/설명 포함 |

---

## §4. 발행 실행 절차

### 4-A. 인스타그램 발행

```bash
# 단계①: 미디어 컨테이너 생성 (--publish 없이 먼저 확인)
python3 ~/projects/_meta/agents/marketing/scripts/ig_publish.py \
  --image-url "https://..." \   # 또는 여러 장: --image-url url1 --image-url url2 --carousel
  --caption-file ~/path/to/caption.txt

# 단계②: 결과 확인 → 컨테이너 ID 기록

# 단계③: 게이트 최종 통과 확인 후 실제 발행
python3 ~/projects/_meta/agents/marketing/scripts/ig_publish.py \
  --image-url "https://..." \
  --caption-file ~/path/to/caption.txt \
  --publish   # 이 플래그가 있어야만 공개
```

**Reels(숏폼) 발행:**
```bash
python3 ~/projects/_meta/agents/marketing/scripts/ig_publish.py \
  --video-url "https://.../short.mp4" \
  --reels \
  --caption-file ~/path/to/caption.txt \
  --publish
```

### 4-B. 유튜브 Shorts 발행

```bash
# 단계①: private 업로드로 먼저 확인
python3 ~/projects/_meta/agents/marketing/scripts/youtube_publish.py \
  --video ~/projects/cadam/media/shorts/{슬러그}.mp4 \
  --title "제목 #Shorts" \
  --desc-file ~/path/to/desc.txt \
  --tags "장기렌트,렌테일러,카담" \
  --shorts

# 단계②: YouTube Studio에서 영상 확인 (섬네일·자막 등 추가 편집)

# 단계③: 게이트 통과 + 결재 완료 후 공개 발행
python3 ~/projects/_meta/agents/marketing/scripts/youtube_publish.py \
  --video ~/projects/cadam/media/shorts/{슬러그}.mp4 \
  --title "제목 #Shorts" \
  --desc-file ~/path/to/desc.txt \
  --tags "장기렌트,렌테일러,카담" \
  --shorts \
  --publish   # 이 플래그가 있어야만 public 공개
```

---

## §5. 발행 후 기록

발행 완료 즉시 해당 cycle 파일 §4(산출물)를 업데이트:

```
- 발행 위치: https://www.instagram.com/p/{미디어ID}/  또는  https://youtu.be/{영상ID}
- 발행 일시: YYYY-MM-DD HH:MM KST
- privacyStatus (YT): public
- 미디어 ID (IG): ...
```

`_shared/final/`에 최종물 복사 (source_cycle + inputs 채워야 학습루프 작동).

---

## §6. D+7 주기C 측정 트리거

발행일 기록 후 7일 뒤 주기C(노출측정) 자동 환류:

| 채널 | 측정 지표 |
|------|----------|
| 인스타 | 노출수, 도달수, 좋아요, 저장, 프로필 클릭 |
| 유튜브 Shorts | 조회수, 평균 시청 시간, 구독자 증감, 좋아요 |

측정 결과 → cycle §5 기록 → sales 전환분석 핸드오프 (§7.4 conversion-report).

---

## §7. 토큰 만료 대응

| 토큰 | 만료 | 갱신 방법 |
|------|------|----------|
| META_ACCESS_TOKEN | 60일 | Graph API `/oauth/access_token?grant_type=fb_exchange_token` 로 재발급. 만료 30일 전 갱신 권장. |
| YT_OAUTH_TOKEN | 1시간 | refresh_token으로 자동 갱신(스크립트 내 미구현 — 만료 시 §1-B 재실행). |

---

## §8. 트러블슈팅

| 에러 | 원인 | 대응 |
|------|------|------|
| `❌ 자격증명 미발급` | .env 키 누락 | §1 프로비저닝 체크리스트 실행 |
| HTTP 400 | 잘못된 media_type 또는 URL 비공개 | 이미지/영상 URL 공개 접근 가능한지 확인 |
| HTTP 190 (OAuthException) | 토큰 만료 | §7 토큰 갱신 절차 실행 |
| YT 쿼터 초과 (403) | 일일 10,000 units 소진 | 다음 날 재시도. 쿼터 증설 신청 가능(Google) |
| `status_code: ERROR` (IG Reels) | 영상 규격 불일치 | MP4/H.264, 9:16, ≤90초 확인 |
