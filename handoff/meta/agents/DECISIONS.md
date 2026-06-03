# 멀티에이전트 시스템 — 설계 결정 기록

## 파트1~3 (2026-05-22) — 마케팅 에이전트 워크플로

상세 내용은 `handoff/projects/rentailor/DECISIONS.md` 참조.
- 파트1: 시드 키워드 발굴 사이클 (트리거)
- 파트2: research.md 생성 (리서치)
- 파트3: Tier 판정 → 디스코드 버튼 → 제안서 생성

## 파트4 (2026-05-30) — 디스코드 봇 설계

### 아키텍처: 봇 = 결재판 (승인 게이트)
- 봇은 Claude API를 호출하지 않음 (비용 0)
- vault의 pending/ 감시 → 디스코드 임베드 카드 → [승인][반려] 버튼 → 파일 이동(pending→approved/rejected)
- 무거운 작업(리서치·제안서)은 클코가 별도 실행 (수동 또는 스케줄)
- 근거: "클코=유료·사람감독, 로컬AI·n8n=무료·자율" 원칙 유지

### 구현 스택
- 언어: discord.js (Node.js) — 기존 Next.js 스택 일치
- 상주: 맥미니 LaunchAgent
- 인증: 사장님 디스코드 ID 화이트리스트 + 비공개 서버

### 메시지 형식
- 임베드 카드 (제목/타깃/구성안 + 어드바이저 반박·우려 별도 필드)
- [승인] [반려] 버튼

### 실행 흐름
- 초기(사이클 1~10회): 수동 시동 → 봇 결재 → 발행
- 검증 후: cron 자동 승격
- 봇 보조 명령(후순위): /status, /사이클 [에이전트] [키워드]

### 미결 (운영 후 결정)
- (B)안 봇 자동 호출 = 헤드리스 = API 과금, 검증 후 승격
- 비평 게이트 정식 박제 = 별도 파트

## 2026-06-03 — 결재 시스템 전면 개편 + 로컬LLM 단일화

> 파트4의 **인터랙티브 버튼 카드 설계는 폐기**. 버튼이 게이트웨이 재시작 시 "expired"로 죽고 컨텍스트·턴 비용이 컸음. 결재판=파일이동 게이트 원칙(봇 LLM 0)은 유지·강화.

### 결재 흐름 (신)
- **버튼 폐지 → 평문 알림 + 결재물 링크.** 결정은 결재함에서 카드에 **답글 `승인`/`반려 [사유]`** (관리팀장 봇 순수 코드 처리, LLM 0).
- **전용 `#결재함`(1510170922005565470) 단일 집결** — [APPROVAL]·[ESCALATE] 모두. `send-approval-card.mjs`가 `--target` 무관하게 강제 라우팅.
- 답글 승인 시: 카드 `-# [ref] agent|origin|path` 마커 파싱 → 파일이면 pending→approved/rejected 이동 + **원채널 담당 에이전트에 역할멘션 통보 → 이어받아 진행**(round-trip). 의사결정 결재(파일無)는 `decision-*.md` 자동 박제.
- **자동점검 린트(0턴)**: 파일없음/빈파일=자동반려, frontmatter누락·중복·고위험(.ts/DB/배포)=카드 태그.
- **로컬AI 요약(비차단)**: 카드 즉시 게시 후 요약을 답글로 첨부. Opus 미사용.

### 모바일 결재물 뷰어 (신규 서비스)
- `~/projects/_meta/md-viewer/server.mjs` (의존성0 Node http, 포트 9724), launchd `com.rentailor.md-viewer`. Tailscale 전용: `http://macmini.tail466d13.ts.net:9724/`. GitHub(미푸시 404)·PDF(도구없음) 대비 채택.

### 로컬 LLM 단일화
- 시스템(sysadmin)·결재요약 모두 **`ollama/qwen3:14b`** 단일 → VRAM 스왑 없음. 30b-a3b·8b 삭제(디스크 ~24GB 확보). 32GB라 30b와 14b 공존 불가가 결정 근거.

### SSOT·관련 파일
- 표준: `_shared/approval-card-policy.md`. 코드: `~/.openclaw/workspace/{tools/send-approval-card.mjs, claude-broker/src/agent.js}`, `~/.openclaw/openclaw.json`(sysadmin model). 워커 SKILL(data/content/marketing)·admin SKILL에 round-trip 계약 반영.
