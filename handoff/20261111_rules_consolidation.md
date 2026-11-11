# 규칙 정리 + 문서 추적 절차 (2026-11-11, REN-152)

사장님 결정(2026-11-11):
1. 규칙 원본 = `_meta/governance/`에 종류별 파일 1개씩 + 맨 앞 규칙 지도 `RULES_MAP.md`(무엇이 어디 있고 누가 참조하는지). 렌테일러 전용 상세(보안·배포 등)는 `cadam/docs/`에 남기고 지도에서 연결.
2. CLAUDE.md = 꼭 지킬 핵심 몇 줄만 그대로 + 나머지는 규칙 지도 참조표.
3. 추적 = 자동 점검(주 1회, 대시보드 표시, 걸리면 Linear) + 구조 변경 작업 끝 수동 절차.
4. 코드 사본(collectors/lib 3개)은 기존 기한(12/15, REN-135). 이번엔 `cadam-pipeline/scripts/common/writing_pause.py`만 보관함으로.
5. 개선 제안 8개 전부 시행 (아래 체크리스트).

## 체크리스트
- [ ] A. 규칙 전수 조사(어느 파일에 어떤 규칙, 겹침·충돌) → 충돌은 사장님께 질문
- [ ] B. `_meta/governance/` 종류별 규칙 파일 + `RULES_MAP.md`
- [ ] C. CLAUDE.md 슬림화(전역 `~/.claude/CLAUDE.md`, cadam, cadam-pipeline, football-blog 등) + 참조표. 전역의 ego_browser 경로 정정(제안 5)
- [ ] D. 추적 도구: `_meta/governance/doc_registry.yaml`(문서 목록·없어진 이름) + `_meta/scripts/doc_audit.py`(옛 이름·plist 사본 불일치(제안 2)·상태 중복) + 주간 launchd + 대시보드 표시 + Linear
- [ ] E. 상태는 한 곳(제안 1): 해외파·엔진 운영 상태 원본 1곳, 나머지 문서는 링크
- [ ] F. AGENTS.md → CLAUDE.md 가리키는 한 줄(제안 3; my-shorts 영상 폴더별 자동 생성분은 제외)
- [ ] G. cadam 세션 종료 규칙 → `docs/PROGRESS.md`(제안 4)
- [ ] H. 노션에 블로그 엔진 페이지(제안 6): docs/blog-engine.md + sync_notion 매핑(노션에 빈 페이지 먼저 필요 — 스크립트는 페이지를 만들지 않음)
- [ ] I. writing_pause.py 보관함(제안 7)
- [ ] J. n8n 시절 섹션 재작성(제안 8): architecture 그림·data-flow·security, 위키 crm-sheets·알람 인벤토리 확인
- [ ] K. push(사장님 확인) → 노션 동기화 확인 → REN-152 기록

주의: `_meta/dashboard/build.py`에 다른 세션의 미커밋 변경(11/11)이 있음 — 건드릴 땐 그 변경과 섞지 말 것(커밋은 `git commit -- <경로>`).
미push 커밋(11/11 오전 점검분): cadam `5111291`, cadam-pipeline `2e2c07c`, football-blog `2a7a580 5e7362a`, _shared `89ec49d`, _meta `4b624b4`, blog-engine `07ab4cb`(다른 세션 커밋과 섞임).
