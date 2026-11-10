# 인계: 블로그 엔진 분리 + 폴더 통합·정리 (2026-11-10)

두 세션을 **동시에** 연다. 각 세션 첫 메시지로 아래 블록을 통째로 붙여넣는다.
기준 문서: `~/projects/_meta/governance/FOLDER_RULES.md`, `~/projects/cadam/docs/strategy/blog-engine-and-folders-20261110.md`

현재 상태(공통): n8n 글쓰기 → Python `cadam-pipeline/scripts/writer/wp_writer.py` 전환 완료, Docker·n8n 제거됨(앱 본체 `/Applications/Docker.app`만 남음 — 사장님이 휴지통으로). 렌테일러 글쓰기 보류 `cadam-pipeline/data/WRITING_PAUSE`, 해외파 발행 보류 `football-blog/data/PUBLISH_PAUSE` — 해제하지 말 것. CRM 시트 동기화는 Python(`scripts/sync/crm_sheet_sync.py`, 30분)으로 이관·Sheets API 확인 완료. 모든 커밋 로컬(push 안 함: cadam-doc, cadam-pipeline, cadam-erp, football-blog, _meta).

---

## 세션 A 붙여넣기용

```
세션 A — 블로그 엔진 구축. ~/projects/_meta/handoff/20261110_blog_engine_and_folders.md 와
~/projects/cadam/docs/strategy/blog-engine-and-folders-20261110.md §2 "세션 A", ~/projects/_meta/governance/FOLDER_RULES.md §1·§3,
~/projects/cadam/docs/strategy/writing-integration-20261110.md 를 읽고 세션 A 범위만 진행해.
순서: ① ~/projects/_shared/solo_common (cadam-pipeline/scripts/common의 discord_client·notify·claude·ego_browser·polite·config_loader 이동 + 옛 자리 re-export 호환층)
② ~/projects/blog-engine 뼈대 + brands/rentailor·football brand.yaml ③ 렌테일러 WP writer+rules 이전(dry-run 비교 후 launchd com.cadam.wp-writer 교체)
④ cadam-naver 발행 서버 → blog-engine/publishers/naver (launchd com.cadam.naver, football 하드코딩 경로 수정, config.json·쿠키는 비밀) ⑤ 렌테일러 네이버·blog_images·topic_* 이전
⑥ 해외파 글쓰기(draft/review/series/records/preview/leaguepost/matchreview) → brands/football, football config.py의 cadam-pipeline sys.path → solo_common ⑦ 통합 주간 성과 보고.
보류 유지, 세션 B 범위(수집기·백업·worktree·캐시) 손대지 말 것. 단계마다 checkpoint 커밋, push 금지.
```

## 세션 B 붙여넣기용

```
세션 B — 폴더 통합·정리. ~/projects/_meta/handoff/20261110_blog_engine_and_folders.md 와
~/projects/cadam/docs/strategy/blog-engine-and-folders-20261110.md §1·§2 "세션 B", ~/projects/_meta/governance/FOLDER_RULES.md 를 읽고 세션 B 범위만 진행해.
① 바로 삭제(재생성 가능): 병합된 cadam-web worktree 9개 git worktree remove(_wt-consult-steps는 미병합 a53c9ed — 남기고 보고), .next·__pycache__
② ~/projects/_archive/2026-11-10/원래경로 로 이동: backups/n8n(최종 백업 backups-manual/n8n_final_20261110 확인 후), cadam-n8n/n8n_data·prompt-bff·workflows-*·vehicle_images,
   test-logs, _scratch, explainer, cadam-data/backup, gpu-setup-*, cadam/_meta/erp-sources, 옛 SQLite 창고(PG 반영 확인 후), football 루트 _scratch_*·shorts-lab *.out·시험 mp4, .bak, 빈 폴더, 끊긴 disabled plist
③ com.cadam.monitor WorkingDirectory → cadam-erp 후 cadam-dashboard 보관
④ 수집기 통합: cadam-n8n/price_crawler·terms_crawler·supabase/wp_sync.py·lib·claude_bridge·telegram_clipper → 규칙 위치(cadam/collectors 등), launchd 경로 동시 수정·재시작, warehouse_backup.sh의 lib.section7 import 수정, 다 옮긴 뒤 cadam-n8n 보관
⑤ PG 백업 하나로(실패 중 warehouse-backup 정리), backup_cadam.sh n8n 코드 제거 ⑥ cadam-doc의 cadam-gpu-agent·cadam-naver 이중 추적 정리(git rm --cached).
세션 A 범위(글쓰기·발행·공용 라이브러리·cadam-naver, 관련 launchd) 손대지 말 것. 실제 삭제(보관함 비우기)는 7일 뒤 목록 보여주고. 단계마다 checkpoint 커밋, push 금지.
```

---

## 이 세션에서 남은 확인
- Docker 앱 본체 휴지통 이동(사장님 수동, 관리자 비밀번호) 후 `com.docker.helper` 등록 남았는지 확인.
- CRM 다음 실제 상담 1건이 시트에 `010-xxxx-xxxx`·날짜 형식으로 들어가는지 확인. 옛 n8n 시절 0 빠진 전화번호 19건은 그대로 둠(수정은 별도 결정).
- 보류 해제 후 첫 실제 발행(렌테일러 WP·네이버, 해외파) 지켜보기.
- ERP/웹 상태 화면의 n8n 표시 정리, 문서 push, Linear 이슈 등록(/mcp 인증 필요).
