# 문서 규칙 (DOCS_RULES)

> 무엇을 정하는 파일: 어떤 문서가 원본인지, 노션 동기화, "docs 반영해줘"·세션 종료 절차, 위키 규칙 요약, 구조 변경 후 문서 정리.
> 마지막 갱신: 2026-11-11 (사장님 결정 2 반영) · **이 파일이 원본 — 다른 문서는 여기를 가리킨다.** 지도: [RULES_MAP.md](RULES_MAP.md)

## 1. 문서 원본 위치 (사장님 결정 6, 2026-11-11)
| 무엇 | 원본 | 다른 곳은 |
|---|---|---|
| 규칙 (모든 프로젝트 공통) | `~/projects/_meta/governance/` (지도 `RULES_MAP.md`) | CLAUDE.md 등은 핵심 몇 줄 + 링크 |
| 운영 사실 (경로·명령·절차) | `~/projects/cadam/docs/` — 노션에 자동 복사 | 위키는 링크만 |
| 개념·결정 이유·연결 관계 | second-brain 위키 `wiki/system/` | 상세는 cadam/docs로 링크 |
| 지금 켜짐/꺼짐 같은 **상태** | 문서에 쓰지 않는다 → **엔진 대시보드**가 보여 준다 (`python3 ~/projects/_meta/dashboard/build.py --open`) | 문서에는 구조·위치·사용법만 |

- 위키 `system/`에 겹쳐 적힌 운영 사실은 문서 점검(§6)이 걸러낼 때 차례로 줄인다.
- 문서 본문은 한국어. 거버넌스·문서 파일명은 한국어 허용, 코드·스크립트·데이터 파일명은 영어 ([FOLDER_RULES.md](FOLDER_RULES.md)).

## 2. 노션 동기화 (cadam/docs)
- `~/projects/cadam/docs/*.md`를 고쳐 `cadam-doc` 리포에 push → GitHub Actions(`.github/workflows/sync-notion.yml`)가 **바뀐 파일만** 노션 위키에 복사.
- push는 승인 후 ([GIT_DEPLOY_RULES.md](GIT_DEPLOY_RULES.md) §4).
- 수동 재실행: `gh workflow run sync-notion.yml -R iori21y-ops/cadam-doc -f files=<파일>`
- 로컬에서 직접 실행: `NOTION_TOKEN=<토큰> python3 ~/projects/cadam/scripts/sync_notion.py [파일명]` (토큰 값은 화면에 남기지 않는다). 동기화 스크립트 `cadam/scripts/sync_notion.py`.
- 노션 위키: https://www.notion.so/Wiki-3529fc8f3ff28026a166e678ef75adf7

## 3. "docs 반영해줘" 절차
("문서 업데이트해줘", "노션 업데이트해줘"도 같다)
1. 이번 세션에서 바꾼 파일을 정리한다.
2. 아래 표대로 해당 docs 파일의 **그 섹션만** 고친다 (통째 재작성 금지). 여러 영역에 걸치면 해당 파일 모두.
3. `cadam-doc`에서 커밋 → 승인 후 push → 노션 반영.
4. `cadam-web`에 안 올린 커밋이 있으면 **승인 후** push (= 즉시 배포).

| 바뀐 것 | 고칠 docs 파일 |
|---|---|
| 서버·서비스 구조, 포트, 인프라 | `architecture.md` + `system-diagram.html` |
| 환경변수, API 키, 인증, RLS | `security.md` |
| 서버 시작·중지, 장애 대응, 모니터링 | `runbook.md` |
| Vercel·배포 설정, 도메인 | `deploy.md` |
| 수집·콘텐츠 자동화 파이프라인 | `pipeline.md` |
| Supabase 표·컬럼·RLS | `schema.md` |
| 데이터 수집·처리·저장 흐름 | `data-flow.md` |
| 웹 페이지 추가·삭제·라우팅 | `_PAGE_MAP.md` |
| 버그·미해결 문제 | `known-issues.md` |
| 협업자용 설명 | `onboarding.md` |
| 마일스톤 완료·단계 전환 | `PROGRESS.md` |
| 진행 중 이슈 | `ISSUES.md` |
| 수집기 추가·중단, 표·API·페이지 연결 | `data-registry.md` (행 수는 자동 생성 — 직접 고치지 않음) |

- **`docs/ISSUES.md` 표 컬럼(칸) 구조 변경 금지** — 이유: cadam-erp 모니터 화면이 이 파일의 '활성 이슈' 표를 읽는다 (`cadam-erp/src/app/api/monitoring/issues/route.ts`, `…/alerts/promote/route.ts`, 2026-11-11 확인).

## 4. 세션 종료 절차 (cadam 작업)
"끝", "종료", "마무리해줘", "오늘 여기까지" 등을 들으면 종료 전에 4단계:
1. **docs 반영** — §3 표대로. 수집기·표·API·페이지 연결이 바뀌었으면 `data-registry.md`도.
2. **진행 기록** — `~/projects/cadam/docs/PROGRESS.md` 맨 위에 `## 📅 YYYY-MM-DD` 로 오늘 작업 추가.
3. **cadam-doc 커밋 → push** (노션 동기화). "마무리해줘" 요청이 문서·규칙 리포 push 승인이다(결정 10).
4. **cadam-web** 안 올린 커밋이 있으면 **따로 승인** 받은 뒤 push (= 배포).

함께: Linear 기록 ([WORK_RULES.md](WORK_RULES.md) §6). docs 반영 없이 닫았으면 다음 세션에서 "최근 커밋 내용 확인해서 docs에 반영해줘"로 복구 (git log/diff 기반).

## 5. 위키 (second-brain) 요약
- 위치: `~/second-brain/` (iCloud 볼트). 상세 스키마는 볼트의 `CLAUDE.md` — 위키 작업 전 먼저 읽는다.
- 질문은 **`wiki/index.md` 먼저** → 관련 페이지 → 없을 때만 웹 검색("위키에 없어 웹서치로 확인" 명시).
- `raw/`는 **읽기 전용** (인제스트 후 `raw/ingested/`로 옮기는 것만 허용).
- `wiki/` 페이지를 만들거나 고치면 `index.md`·`log.md`도 같이 갱신. 고치기 전 이유를 한국어로.
- 5개 이상 파일을 바꾸면 계획을 먼저 공유. 내용 삭제는 이유를 log에. 대량 삭제·통째 덮어쓰기는 사전 확인.
- 숫자 덤프는 위키에 넣지 않는다 (데이터 창고 대상).
- 명령: "인제스트해줘"·"린트해줘"·질문 → 볼트 CLAUDE.md 절차. 커밋 메시지 `ingest:`/`query:`/`lint:`.
- git 기록: 볼트(iCloud)는 git이 아니다. `~/second-brain-git` 미러가 밤마다 볼트를 rsync한 뒤 커밋·push한다.

## 6. 구조 변경 후 문서 정리
폴더 이동·이름 변경·서비스 폐기를 했으면 그 작업 끝에:
1. `~/projects/_meta/governance/doc_registry.yaml`의 `retired:`에 옛 이름 → 새 이름 한 줄 추가.
2. `python3 ~/projects/_meta/scripts/doc_audit.py` 실행.
3. 결과 `~/projects/_meta/logs/doc_audit.md` 목록을 **원본 문서부터** 고친다. 규칙은 [RULES_MAP.md](RULES_MAP.md)의 원본 파일만 고치고, 다른 문서는 원본을 가리키게.
4. **0건이 될 때까지** 2~3을 반복. 기록으로 남길 문단은 `> ⚠️ … 폐기 — 기록용` 으로 표시하면 점검이 넘어간다.
5. 자동 점검: **매주 월 09:05** 예약 작업(`com.solo.doc-audit`)이 남은 것을 Linear 이슈(키 `doc-audit:*`)로 알리고, 고쳐지면 자동으로 닫는다. 엔진 대시보드 '문서 점검' 탭에서도 보인다.
