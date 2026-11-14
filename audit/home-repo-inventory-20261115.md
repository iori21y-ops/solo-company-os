# 홈 레포 공유 자료 전수 조사 (2026-11-15)

> 맷 포콕 "홈 레포(Home Repo)" 방식 2단계(공유 자료 분류)를 사장님 구조에 적용한 결과. 사장님 승인: 2026-11-15 "추천안대로".
> 범위: `~/projects` 전 저장소 + `~/second-brain-git` + `~/.claude/skills`. 제외: `node_modules`·`_archive`·`_data`·`_wt-*`·`.git`.

## 조사 규모
규칙 파일(CLAUDE.md·AGENTS.md·.cursorrules) 17개 · 스킬(SKILL.md) 43개 · AI용 문서(규칙·규약·보안·온보딩) 20개.

## 분류
| 분류 | 무엇 | 조치 |
|---|---|---|
| 공용 (본사에 이미 있음) | `_meta/governance` 규칙 7개, `_meta/skills` 6개, `~/projects/CLAUDE.md`, 전역 `~/.claude/CLAUDE.md` | 없음 |
| 저장소 전용 | 각 프로젝트 CLAUDE.md 12개, cadam 스킬 4개(`cadam/.claude/skills`), 쇼츠 `shorts` 스킬, `cadam/docs/security.md`(“다르면 governance 우선” 명시), `COLLECTOR_CONVENTION.md`, `cadam/docs/onboarding.md`, 브랜드 글쓰기 규칙 | 제자리 |
| 설치형 | `content-engine/video/.claude/skills` 30개(출처 `skills-lock.json`: greensock/gsap-skills, remotion-dev/skills, higgsfield-ai/skills, LottieFiles/motion-design-skill, hypit-ai/hypit), `~/.claude/skills`의 ego-browser·graphify·motion-prompt·synced, hyperframes 플러그인 v0.8.186 | 제자리 |
| 중복·오래됨 → 정리함 | 아래 "한 일" | 정리 |
| 중복이지만 의도됨 | 쇼츠 폴더 2곳 CLAUDE.md=AGENTS.md(HyperFrames 도구가 생성) · `~/second-brain-git/CLAUDE.md`(볼트 밤마다 미러) · `_shared/phone-view/` 인계 문서 사본(폰 보기용) · `~/.codex/AGENTS.md`(전역 규칙 옛 사본, Codex 보류) | 그대로 |

## 한 일
1. **cadam `/p`·`/progress`·`/ps` 명령어 은퇴** — 없어진 `rentailor-plan/`을 읽고 썼음. 세션 종료는 `DOCS_RULES.md` §4. → `~/projects/_archive/2026-11-15/cadam/.claude/commands/` (cadam 커밋 `0295494`).
2. **문서 점검 범위 확대** — `doc_registry.yaml`에 `~/projects/CLAUDE.md`, `*/.claude/commands/*.md`, `*/.claude/skills/*/SKILL.md`, `_meta/skills/*/SKILL.md` 추가 (_meta 커밋 `5d9f368`).
3. **hyperframes 직접 설치본 4개 은퇴** — `~/.claude/skills/{hyperframes,hyperframes-cli,hyperframes-registry,media-use}`(10-31)가 플러그인과 두 벌로 동시에 읽혔음. 플러그인 쪽만 남김 → `~/projects/_archive/2026-11-15/home-claude-skills/`. 새 세션 확인: `hyperframes:*` 7개만 보임.
4. **cadam-web 옛 Cursor 규칙 3개 은퇴(브랜치만)** — `.cursorrules`·`cursor_rules.md`·`CURSORRULES-ADDITION.md`(3월, 없어진 `price_ranges` 표 기준). main push = 배포이고 월 렌트료 자동화가 main을 push하므로, main·작업 폴더는 그대로 두고 브랜치 `chore/retire-cursor-rules`(커밋 `ea81fb7`)에만 기록. **다음 배포 승인 때 합친다.**

보관함 기록: `~/projects/_archive/2026-11-15/MOVED.txt` — 2026-11-22 이후 사장님 확인 후 비움.

## 남은 것
- ~~cadam 전용 스킬·명령어 안 옛 경로 11건~~ → 2026-11-15 고침(사장님 승인): `cadam-stats` 일일 보고 `ops/`·디스코드, `cadam-crawl` 약관 결과 = Supabase `terms_documents`·크롤러 `collect/crawl/`, `cadam-image` 360° = 휴면 표시(원본은 GPU 콜드 아카이브), `/test` 기록 = `_data/rentailor/work/test-logs/`. 같은 옛 경로가 있던 `docs/runbook.md`·`docs/architecture.md`도 함께. 점검 결과 0건.
- `cadam/docs/architecture.md` "cadam-pipeline" 표의 데이터 입출력·로그·Git(`cadam-auto.git`) 줄은 옛 내용일 가능성 — 이번엔 확인 안 함.
- Codex용 `~/projects/AGENTS.md` 연결 — 보류(사장님).
- 공통 코딩 기준 문서 없음 — 필요 시 별도.
