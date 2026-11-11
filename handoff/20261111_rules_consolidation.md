# 규칙 정리 + 문서 추적 절차 (2026-11-11, REN-152)

사장님 결정(2026-11-11):
1. 규칙 원본 = `_meta/governance/`에 종류별 파일 1개씩 + 맨 앞 규칙 지도 `RULES_MAP.md`(무엇이 어디 있고 누가 참조하는지). 렌테일러 전용 상세(보안·배포 등)는 `cadam/docs/`에 남기고 지도에서 연결.
2. CLAUDE.md = 꼭 지킬 핵심 몇 줄만 그대로 + 나머지는 규칙 지도 참조표.
3. 추적 = 자동 점검(주 1회, 대시보드 표시, 걸리면 Linear) + 구조 변경 작업 끝 수동 절차.
4. 코드 사본(collectors/lib 3개)은 기존 기한(12/15, REN-135). 이번엔 `cadam-pipeline/scripts/common/writing_pause.py`만 보관함으로.
5. 개선 제안 8개 전부 시행 (아래 체크리스트).

## 체크리스트
- [x] A. 규칙 전수 조사(어느 파일에 어떤 규칙, 겹침·충돌) → 충돌은 사장님께 질문
- [ ] B. `_meta/governance/` 종류별 규칙 파일 + `RULES_MAP.md`
- [ ] C. CLAUDE.md 슬림화(전역 `~/.claude/CLAUDE.md`, cadam, cadam-pipeline, football-blog 등) + 참조표. 전역의 ego_browser 경로 정정(제안 5)
- [x] D. (62f6755: doc_audit.py·doc_registry.yaml·launchd com.solo.doc-audit 월 09:05 설치·대시보드 '문서 점검' 탭. DOCS_RULES.md 절차 문서는 B에서) 추적 도구: `_meta/governance/doc_registry.yaml`(문서 목록·없어진 이름) + `_meta/scripts/doc_audit.py`(옛 이름·plist 사본 불일치(제안 2)·상태 중복) + 주간 launchd + 대시보드 표시 + Linear
- [ ] E. 상태는 한 곳(제안 1): 해외파·엔진 운영 상태 원본 1곳, 나머지 문서는 링크
- [x] F. (cadam·cadam-pipeline AGENTS.md(미추적)·football-blog f9e2fc0, 옛 본 _archive/2026-11-11/agents-md) AGENTS.md → CLAUDE.md 가리키는 한 줄(제안 3; my-shorts 영상 폴더별 자동 생성분은 제외)
- [ ] G. cadam 세션 종료 규칙 → `docs/PROGRESS.md`(제안 4)
- [x] H. (cadam 커밋: docs/blog-engine.md + sync_notion이 없는 페이지 생성 — push 후 노션에 생김) 노션에 블로그 엔진 페이지(제안 6): docs/blog-engine.md + sync_notion 매핑(노션에 빈 페이지 먼저 필요 — 스크립트는 페이지를 만들지 않음)
- [x] I. (cadam-pipeline fe12cb8, _archive/2026-11-11/MOVED.txt) writing_pause.py 보관함(제안 7)
- [x] J. (cadam 87aeb9f·89d44c2 재작성, security c38a8c8·deploy 7aa6a06 결정 반영. 확인 필요: GPU Ollama 사용처, 상담 KPI 화면, 키워드 규칙 편집 화면) n8n 시절 섹션 재작성(제안 8): architecture 그림·data-flow·security, 위키 crm-sheets·알람 인벤토리 확인
- [ ] K. push(사장님 확인) → 노션 동기화 확인 → REN-152 기록

주의: `_meta/dashboard/build.py`에 다른 세션의 미커밋 변경(11/11)이 있음 — 건드릴 땐 그 변경과 섞지 말 것(커밋은 `git commit -- <경로>`).
미push 커밋(11/11 오전 점검분): cadam `5111291`, cadam-pipeline `2e2c07c`, football-blog `2a7a580 5e7362a`, _shared `89ec49d`, _meta `4b624b4`, blog-engine `07ab4cb`(다른 세션 커밋과 섞임).

## A 결과 요약 (규칙 전수 조사, 2026-11-11)
종류 20개: 소통·작업방식 / 사전승인 / 절대금지 / 동시 세션 / 저장위치·폴더 / 정리·삭제 / git·커밋 / 배포 / DB·Supabase·비밀 / 수집·웹도구 / 데이터 창고 / 문서·노션·세션종료 / Linear / 세션관리 / 글쓰기 / 위키 / 결재·보고 / 비용 / 실행환경 / 백업.
모순(사장님 결정 필요): ①커밋 메시지 언어(전역 영어 vs cadam-web·security 한국어) ②배포(security "가이드만" vs CLAUDE "승인 후 push=배포") ③승인 범위·launchd·삭제(security는 모든 변경 승인·launchd 금지 vs 실제 운영) ④백업 위치(~/backups vs ~/projects) ⑤약관상 금지 사이트 수집 예외(Transfermarkt·FBref·KB) ⑥시스템 문서 원본(cadam/docs vs 위키 system) ⑦소통(먼저 설명 vs 바로 실행).
제가 정함: ISSUES.md 컬럼 규칙 이유를 cadam-erp로 정정 / 거버넌스 문서 한국어 파일명 허용(코드·프로젝트 파일만 영어) / /tmp는 잠금 파일만 허용 / Playwright 금지는 수집기 한정 / 실행환경 범위 명시(my-shorts .venv, 그 외 /usr/bin/python3) / 해외파 내부 모순(자동 업로드·언론사 사진·영상 삽입)은 재개 때 정리(REN-133에 기록).
조사 원문: 이 세션 하위작업 보고(규칙 위치 file:line 전부) — 새 세션이면 다시 조사(Explore)로 재생성.

## 사장님 결정 (2026-11-11, 모순 7건 — 모두 추천안)
1. 커밋 메시지·코드 주석 = 영어 통일 (문서 본문은 한국어)
2. 배포 = 사장님 승인 후 Claude가 push(cadam-web push=즉시 배포). push 전 로컬 빌드 확인 필수
3. 승인 범위 = 되돌릴 수 없는 것만: DB 쓰기, push·배포, 서비스 재시작, 파일 삭제, 운영 중 예약작업 끄기. 승인 불필요(항상 보고): 커밋, 문서 수정, 새 예약작업 등록·경로 수정, 재생성 가능한 캐시(.next·__pycache__) 삭제
4. 백업 = 새 백업은 ~/projects/<사업>/backups(자동)·backups-manual(일회성). 기존 ~/backups는 옮기지 않고 읽기 전용 보관
5. 수집 = 원칙(약관이 자동 수집 금지면 안 씀) + 사장님 승인 예외 목록 한 표(사이트·승인일·이유·쓰임) — 표에 없으면 수집 불가
6. 문서 원본 = 운영 사실(경로·명령·절차)은 cadam/docs(노션 자동 복사)만. 위키 system/은 개념·결정 이유·연결 관계 + 상세는 링크(줄이기는 문서 점검이 걸러낼 때 차례로)
7. 작업 방식 = 정보 충분 + 되돌릴 수 있는 일은 '무엇을 왜' 한 줄 말하고 바로 실행. 확신 없거나 되돌릴 수 없는 일은 먼저 질문

## 사장님 결정 2 (2026-11-11)
8. WRITING_PAUSE: 켜기(보류)는 승인 없이 하고 보고, 끄기(재개)는 승인
9. 운영 DB: psql 직접 접속 금지, 승인 받은 쓰기만 MCP·Management API로 허용(WHERE·사전 조회)
10. "마무리해줘" = 문서·규칙 리포(cadam-doc·_meta·_shared 등) push 승인. 코드·사이트 리포는 따로 승인
11. 운영 중 예약 작업 실행 시각 변경 = 승인 필요(경로 수정은 보고만)
사실 확인: DB 백업 = 로컬 30개 + iCloud 주1회 8개(backup_cadam.sh) / Linear = productivity 플러그인 정상 / 위키 git = ~/second-brain-git(밤마다 iCloud 볼트를 rsync 후 커밋·push)
수집 예외 미확인 6건(TM 감독 이력 승인일, Capology, 리그 공식 사이트, 엔카 웹, 인스타, 충전요금) → Linear 후속 이슈
