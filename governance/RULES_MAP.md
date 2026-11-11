# 규칙 지도 (RULES_MAP)

> 무엇을 정하는 파일: 어떤 규칙이 어느 파일에 있고(원본), 누가 그 규칙을 옮겨 적거나 가리키는지(참조).
> 마지막 갱신: 2026-11-11 · **이 파일이 원본 — 다른 문서는 여기를 가리킨다.**
> 근거: 사장님 결정 2026-11-11 (`~/projects/_meta/handoff/20261111_rules_consolidation.md`, REN-152)

## 판단 순서
1. **안전 > 정확 > 속도.** 데이터 손실 방지가 먼저, 확실하지 않으면 실행하지 말고 질문.
2. 프로젝트 규칙이 공통 규칙보다 **구체적이면 프로젝트 규칙**을 따른다.
3. 단, **안전 규칙([SAFETY_RULES.md](SAFETY_RULES.md))은 항상 우선** — 어떤 프로젝트 규칙도 안전 규칙을 풀어 주지 못한다.
4. 사장님 결정(2026-11-11)이 옛 규칙 문구와 다르면 결정이 우선.

## 공통 규칙 (원본 = `~/projects/_meta/governance/`)
"참조하는 곳" = 지금 이 규칙을 옮겨 적고 있거나 가리키는 문서. 규칙이 바뀌면 이 문서들이 원본과 어긋나지 않는지 본다 (CLAUDE.md 정리 작업의 할 일 목록).

| 규칙 종류 | 원본 파일 | 한 줄 요약 | 이 규칙을 가리키는(참조하는) 곳 |
|---|---|---|---|
| 소통·작업 방식 | [WORK_RULES.md](WORK_RULES.md) §1 | 되돌릴 수 있으면 한 줄 설명 후 바로 실행, 아니면 먼저 질문 | `~/.claude/CLAUDE.md` 소통 방식, `cadam/CLAUDE.md` 작업 스타일, `cadam/docs/security.md` 보고·의사결정 |
| 추측 금지 | WORK_RULES §2 | 코드 먼저 읽고 실행, 모르면 확인 명령과 함께 보고 | `cadam/CLAUDE.md` 추론/추측 금지 원칙 |
| 완료 보고 | WORK_RULES §3 | "완료"는 도구 결과로 근거 | `cadam/CLAUDE.md` 작업 스타일, `security.md` 보고 규칙 |
| 동시 세션 | WORK_RULES §4 | 한 리포 한 세션, 시작 전 `git status`, 남의 변경 보고 | `cadam/cadam-web/CLAUDE.md`, `cadam/cadam-erp/CLAUDE.md`, 메모리 `feedback_check_parallel_sessions.md` |
| 세션 관리 | WORK_RULES §5 | `/advisor`, 용량 과다 시 메모리 저장·인계 | `~/.claude/CLAUDE.md`, `cadam/CLAUDE.md` |
| 작업 기록 (Linear) | WORK_RULES §6 | REN 이슈 댓글·완료, 남은 일은 새 이슈, 커밋에 `Refs/Fixes REN-N` | `~/.claude/CLAUDE.md`, 메모리 `project_linear.md` |
| 비용 | WORK_RULES §7 | Supabase 무료 한도, Vercel Hobby 주의, HyperFrames, API 예산 | 메모리 `feedback_supabase_free_plan.md`·`project_netlify_standby.md`, `my-shorts/CLAUDE.md` |
| 실행 환경 | WORK_RULES §8 | launchd·공용·엔진 = `/usr/bin/python3` 3.9, my-shorts = `.venv`, GPU = `ssh gpu-server` | `cadam/cadam-pipeline/CLAUDE.md`, `my-shorts/CLAUDE.md`, `FOLDER_RULES.md` §3, `security.md` |
| 승인 범위 | [SAFETY_RULES.md](SAFETY_RULES.md) §1 | 되돌릴 수 없는 것만 승인(DB 쓰기·push·재시작·삭제·예약 작업 끄기) | `~/.claude/CLAUDE.md` 전역 안전 규칙, `cadam/CLAUDE.md` 최우선 규칙, `security.md` 작업 전 절차·도구 규칙, `_meta/agents/CLAUDE.md` §13 |
| 절대 금지 | SAFETY §2 | DROP·TRUNCATE·조건 없는 DELETE/UPDATE·비밀 커밋·`rm -rf`·강제 push 등 | `~/.claude/CLAUDE.md`, `cadam/CLAUDE.md`, `cadam-pipeline/CLAUDE.md`, `cadam-web/CLAUDE.md`, `security.md` 절대 금지 |
| DB 쓰기 절차 | SAFETY §3 | 지금 상태 → 요약 → 되돌리는 법 → 승인, 10행+ 나눠서 | `security.md` Supabase 데이터 변경, `cadam/CLAUDE.md` |
| 오류 시 | SAFETY §4 | 멈추고 전문 보고, 재시도 2회까지, 자동 되돌리기 없음 | `security.md` 에러 처리 |
| 정리·삭제 | SAFETY §5 + [FOLDER_RULES.md](FOLDER_RULES.md) §5 | 캐시는 바로 삭제, 나머지는 보관함 7일 후 승인 받고 비움 | `~/.claude/CLAUDE.md` (`rm -rf` 금지), `security.md` 파일 삭제 |
| 백업 | SAFETY §6 | 새 백업은 `<사업>/backups`(자동)·`backups-manual`(일회성), `~/backups`는 읽기 전용 | `security.md` 백업 정책, `FOLDER_RULES.md` §4, `cadam/CLAUDE.md` 저장 위치 |
| 비밀 파일 | SAFETY §7 | `~/.cadam-secrets/`·`.env`는 제자리에서 읽기만, 값 출력 금지 | `~/.claude/CLAUDE.md`, `security.md`, `FOLDER_RULES.md` §5, `_meta/agents/CLAUDE.md` §10, `my-shorts/CLAUDE.md` 키 |
| 커밋·리포 | [GIT_DEPLOY_RULES.md](GIT_DEPLOY_RULES.md) §1~4 | 영어 메시지, 고치기 전 `checkpoint:`, 내 파일만 커밋, push는 승인 | `~/.claude/CLAUDE.md`, `cadam/CLAUDE.md` Git 리포, `cadam-pipeline/CLAUDE.md`, `cadam-web/CLAUDE.md`, `security.md` Git 작업 |
| 배포 | GIT_DEPLOY_RULES §5 | 승인 → 로컬 빌드 → Claude가 push(cadam-web = 즉시 배포) → `npx vercel ls` | `cadam/CLAUDE.md`, `cadam-web/CLAUDE.md`, `cadam/docs/deploy.md` |
| 수집·웹 도구 | [COLLECT_RULES.md](COLLECT_RULES.md) | ego-browser 기본, 예절 수집, 약관 금지 사이트는 승인 예외 표만 | `~/.claude/CLAUDE.md` 웹 자료 수집, `cadam/collectors/COLLECTOR_CONVENTION.md`, `football-blog/CLAUDE.md` 데이터 창고 표, `cadam/cadam-data/CLAUDE.md` 주의, 메모리 `project_polite_crawl.md`·`project_encar_crawler_copies.md` |
| 데이터 창고 | [DATA_RULES.md](DATA_RULES.md) (초안, 사장님 확인 전) | 쓰이는 것만 남긴다, 데이터 명세·카테고리·늘리고 줄이는 기준 | `FOLDER_RULES.md` §4, `COLLECTOR_CONVENTION.md` §1 |
| 저장 위치·폴더 | [FOLDER_RULES.md](FOLDER_RULES.md) | 산출물은 `~/projects/<프로젝트>/`, 사업별 같은 모양, 다른 프로젝트 import 금지 | `~/.claude/CLAUDE.md` 저장 위치, `cadam/CLAUDE.md` 저장 위치 |
| 임시 연결·사본 | [COMPAT_LIST.md](COMPAT_LIST.md) | 옛 주소 연결·코드 사본·남은 위반과 없애는 기한 | `FOLDER_RULES.md` §6 |
| 문서·노션·세션 종료 | [DOCS_RULES.md](DOCS_RULES.md) §1~4 | 운영 사실은 cadam/docs, 상태는 대시보드, 종료 4단계 | `cadam/CLAUDE.md` docs 업데이트·세션 종료 규칙 |
| 위키 | DOCS_RULES §5 (요약) — 원본은 볼트 `CLAUDE.md` | index 먼저, raw 읽기 전용, index·log 갱신 | `~/.claude/CLAUDE.md` Second Brain, `cadam/CLAUDE.md` 볼트 |
| 구조 변경 후 문서 정리 | DOCS_RULES §6 | `retired:` 추가 → `doc_audit.py` → 0건까지 | `doc_registry.yaml` |
| 결재·보고 (에이전트) | [REG-001-결재보고프로세스.md](REG-001-결재보고프로세스.md) | 에이전트 산출물 승인·수정·반려 절차 | `_meta/agents/CLAUDE.md` |

## 프로젝트별 규칙 (그 프로젝트에 남는 원본)
| 규칙 | 원본 위치 |
|---|---|
| 렌테일러 월 렌탈료 표기·계산식 폐기, 차량 상세 서버 조회, 이미지·성능 기준 | `~/projects/cadam/cadam-web/CLAUDE.md` |
| cadam 보안 상세 (Supabase 단계별 확인, RLS, 도구별 허용 표, 오류별 대응) | `~/projects/cadam/docs/security.md` |
| 배포 상세 (Vercel 설정·환경변수·도메인·브랜치) | `~/projects/cadam/docs/deploy.md` |
| 수집기 상세 (저장·등록·실패·알림·인벤토리) | `~/projects/cadam/collectors/COLLECTOR_CONVENTION.md` |
| 글쓰기 규칙 (공통·발행처·블로그 층) | `~/projects/blog-engine/rules/README.md` |
| 해외파 콘텐츠·사진·데이터 규칙 | `~/projects/football-blog/CLAUDE.md` |
| 쇼츠 제작 규칙 | `~/projects/my-shorts/CLAUDE.md` |
| 위키 스키마 (인제스트·린트·볼트 업데이트) | `~/second-brain/CLAUDE.md` (iCloud 볼트) |
| 에이전트 학습 vault 운영 | `~/projects/_meta/agents/CLAUDE.md` |
| 에이전트 결재·보고 | `REG-001-결재보고프로세스.md` |

## 규칙을 바꿀 때
1. **원본 파일만** 고친다 (위 표의 원본 파일). 다른 문서에는 내용을 옮겨 적지 말고 원본을 가리킨다.
2. 원본 파일 맨 위 "마지막 갱신" 날짜를 바꾼다.
3. `python3 ~/projects/_meta/scripts/doc_audit.py` 실행 → `~/projects/_meta/logs/doc_audit.md`에 걸린 곳을 고친다 ([DOCS_RULES.md](DOCS_RULES.md) §6).

## 후속 확인 (Linear) — 수집 예외 미확인 6건
사장님 결정 2(2026-11-11): 아래는 Linear 후속 이슈로 확인한다. 확인 전까지 [COLLECT_RULES.md](COLLECT_RULES.md) 예외 표에 넣지 않는다.
1. **Transfermarkt 감독 이력**(`tm_managers`) 수집 승인일이 기록에 없음.
2. **Capology** 연봉 수집(사용자 결정 2026-11-10, robots `use=reference` 준수) — 약관상 자동 수집 금지인지 기록이 없음.
3. **리그 공식 사이트**: `football-blog/CLAUDE.md`에 "보류(premierleague.com 약관이 DB 생성 금지)"와 "추가 수집 `official.py`(2026-11-09 사용자 지시)"가 함께 있음.
4. **엔카 웹 시세**(`scrape_encar.py`): 수집기 규약은 "엔카 API 금지"만 적혀 있고 웹 페이지 약관 상태는 기록이 없음.
5. **인스타그램** 공식 계정 사진 수집(2026-11-06 사용자 결정, 수집 전용 계정) — 약관 상태 기록 없음.
6. **무공해차 통합누리집 충전요금**(ego 수집): 규약에 "약관 미확인 → 노출 전 확인".

## 알려진 불일치 (원본이 맞고, 다른 문서를 고칠 차례)
- `cadam/collectors/COLLECTOR_CONVENTION.md` 2.2는 창고 백업을 `warehouse_backup.sh`(로컬 4개 + iCloud 8개)로 적었으나, 그 예약 작업 plist가 `~/Library/LaunchAgents`에 없다(2026-11-11 확인). 실제 DB 백업은 `cadam/backup_cadam.sh`(로컬 30개 + iCloud 주 1회 8개). 원본: [SAFETY_RULES.md](SAFETY_RULES.md) §6.
