# 임시 연결·사본·남은 위반 목록 (FOLDER_RULES §6)

> 이사하면서 남긴 "옛 주소 → 새 주소" 연결, 어쩔 수 없이 만든 사본, 아직 규칙을 어기는 곳을 한곳에 적는다.
> 새로 만들면 여기에 한 줄 추가, 없애면 줄을 지운다. **점검일마다 "쓰는 곳 수"를 다시 세고 0이면 없앤다**(삭제 전 사장님 확인).
> 마지막 점검: 2026-11-13 · 다음 점검: 2026-11-27

## A. 임시 연결 (옛 주소로 와도 새 주소로 이어 주는 것)

없음 (2026-11-13 점검: 폴더 링크·별칭 파일 모두 없앰 — 아래 D).

## B. 사본 (원본을 고치면 같이 고쳐야 하는 것)

| 사본 | 원본 | 내용 | 하나로 합치는 방법 | 기한 |
|---|---|---|---|---|
| `content-engine/brands/rentailor/video/uploader.py`·`brands/football/video/publish.py`·`upload_all.py` | `content-engine/video/pipeline/youtube.py` | 유튜브 업로드·썸네일·댓글·공개 범위 (토큰 파일 경로는 `video/pipeline/common._cred`) | 실제 게시 없이는 검증할 수 없고 두 쇼츠 라인 모두 보류 중 → 쇼츠 과정 재설계 때 `engine/`으로 하나로 | 쇼츠 재설계 때 |

## C. 아직 규칙을 어기는 곳 (다른 프로젝트 코드를 직접 불러 씀)

| 어디 | 무엇을 | 고치는 방법 | 기한 |
|---|---|---|---|
| `import-lease/shared/migrate_from_cadam.py` | 렌테일러 DB 읽기용 접속 정보를 cadam `collect/price_crawler/.env`에서 읽음(`run_monthly` 테슬라 동기화·백업/삭제 도구), 일회성 이전 `main()`은 cadam `price_crawler`를 import | 렌테일러 DB 읽기 전용 키를 `~/.cadam-secrets`에 두고 그 파일을 읽게(사장님이 키 파일 정리 시), 일회성 이전 코드는 보관함으로 | 2026-12-15 |
| `import-lease/process/normalize_images.py` | 사이트 저장소 `web-engine/cadam-web/scripts/reprocess_car_image.py`(배경 제거·배치)를 import (수동 이미지 도구) | 이미지 도구를 `solo_common` 또는 엔진으로 옮김 | 쓸 때 |
| `content-engine/brands/football/video/*` (11개 파일) | `sys.path`에 `football-blog` 넣고 `football.*` 패키지를 직접 import | 쇼츠 과정 재설계 때 `football/content/`와 함께 정리 | 쇼츠 재설계 때 |
| `football-blog/ops/tools/upgrade_posts.py` | 렌테일러 브랜드 코드 `naver_rewrite.naver_markup` (수동 일회용 도구, `football.draft`가 없어 **지금은 실행 안 됨**) | 다음에 쓸 일이 생기면 `content-engine/brands/football/tools/`로 옮김 | 쓸 때 |

## D. 끝난 것 (참고)
- 2026-11-13 저녁(사장님 "지금 이어서"): ① `linear_alert` → `_shared/solo_common/linear_alert.py`(렌테일러 4·임포리스 2·_meta 4곳, 옛 파일은 보관함; Linear 읽기 전용 조회로 새 경로 확인; solo-shared `a55cae5`, cadam `6a06eb4`, import-lease `b81e89f`, _meta `950cc29`) ② 임포리스 디스코드 알림 → `solo_common.notify` #데이터(같은 채널, 사장님 결정; `b81e89f`) ③ 임포리스 `lease_fallback` → 렌테일러 데이터 창구 `facts_cli chazm_source_lease`(결과 파일 단위 동일; cadam `4cbb33f`, import-lease `a079a7f`). 같이 찾아 고친 것: 임포리스 `migrate_from_cadam.CRAWLER_DIR`이 11:00에 없앤 `cadam-n8n` 링크를 가리켜 월간 테슬라 동기화가 실패할 상태(`d7eec20`), GPU 이미지 동기화 스크립트가 옛 경로라 창고 폴더만 비우고 멈출 상태(gpu-agent `2a98e2e`, 원본 확인 후 비우게), 성장 지표의 쇼츠 토큰 예비 경로(cadam `4a91b80`).
- 2026-11-13 저녁(사장님 "1·2 정리"): ① `trend_api.py` 사본 → `_shared/solo_common/naver_api.py` 하나로(키는 각자 `get_env`를 넘김, 바꾸기 전후 결과 동일; solo-shared `6227cab`, content-engine `f80db96`, cadam `d2ac0c5`) ② `cadam/collect/lib`의 ego_browser·polite·ego_bridge.js — 설명문만 다르고 코드는 solo_common과 같았음(11-11 "내용이 다름"은 잘못된 기록) → 쓰는 곳 5개 파일을 solo_common으로, 사본은 `_archive/2026-11-13-cadam-cleanup/collect-lib-copies/`(cadam `9218bf3`, import-lease `d11ca4c`). 남은 `collect/lib`(notify→#데이터·change_alert·section7)는 사본이 아니라 렌테일러 수집기 전용 라이브러리 ③ 렌테일러 자동 쇼츠 `run.py` 알림: cadam telegram_notifier(텔레그램) → `solo_common.notify` 디스코드 #콘텐츠기획(content-engine `f08363e`) ④ 임포리스 `db_size_check` → `~/.cadam-secrets/secrets.env`(같은 값 확인; `92c07d7`), `fetch_official_pdfs`의 cadam 경로 줄 제거(`2ebb59b`) ⑤ 영상 `video/pipeline`의 `_cred` 사본 → `common.py` 하나(video `b8ad144`). 함수 이름이 같은 나머지(build·main·bt·fit·josa·cover.inject)는 내용이 달라 중복 아님.
- 2026-11-13 오후 점검(이 목록 다시 셈): ① `cadam/cadam-naver`·`cadam/cadam-n8n` 폴더 링크 없음 확인 ② `core/scripts/common`의 별칭 파일 8개(claude·content_extractor·discord_client·ego_browser·llm_client·notify·polite·warehouse) — 부르는 57개 파일을 `solo_common` 직접 import로 바꾸고 별칭 파일은 `_archive/2026-11-13-cadam-cleanup/core-scripts-common-shims/`로(cadam `0b0a805`) ③ `evidence_body` — 부르는 곳 모두 `solo_common.evidence_body` ④ 계산 모듈 `sys.path` 연결 — 모듈을 `cadam/facts/`로 옮겨 해소(cadam `899a9bf`) ⑤ `writing_pause.py` 사본 — cadam 쪽 없음, 엔진 `brands/rentailor/writing_pause.py`만 남음.
- 2026-11-13: 모든 사업의 데이터(작업 파일·수집 원본·사진·백업)를 데이터 창고 `~/projects/_data/<사업>/<종류>/<이름>`으로 옮기고 코드 폴더의 바로가기를 모두 지움(`_data/README.md`). 아래 기록의 경로는 그때 기준이다.
- 2026-11-11 (REN-134): 해외파 morning·poll 예약 작업을 엔진 직접 실행으로 교체(`blog-engine/launchd/com.iori21y.football-morning|poll.plist`, 설치본 교체·**load 안 함**, 기록 `blog-engine/logs/football-*.log`). 잠금·자동 점검·미실행 알림·네이버 로그인 점검도 엔진(`brands/football/jobs.py`, 공통 `_shared/solo_common/jobhealth.py`). 영상·쇼츠 점검은 football-blog `run.py videopoll`(plist는 저장소에만, 다시 켤 때 설치). 옛 설치본 백업 `_archive/2026-11-11/football-launchd/`(2026-11-12 비움, REN-160 — 휴지통).
- 2026-11-11 (REN-135): `football-blog/data/posts`·`data/cards` 링크 제거(링크 자체는 `_archive/2026-11-11/football-links/`에 보관했다가 2026-11-12 비움, REN-160). 사진 14일 중복 검사·최근 글감은 엔진이 창구 인자로 넘김, 썸네일 크롭은 `football-blog/data/media/headers/`(2026-11-13 → `_data/football/media/football-blog/headers/`)(옛 글 18편 경로 고침, 원본은 `_archive/2026-11-11/football-outbox-posts/`에 두었다가 2026-11-12 비움, REN-160), 영상 상태는 `football-blog/data/video_jobs/`(2026-11-13 → `_data/football/work/football-blog/video_jobs/`). 남은 연결(위반 아님): 영상 제안·수동 렌더 때 `football-blog/football/videojobs.py`가 엔진 글 파일 하나를 **읽기 전용**으로 연다(엔진이 football-blog SQLite를 읽기 전용으로 여는 것과 같은 방식).
- 2026-11-11 (REN-135): 사본 `llmutil`·`discordutil` → `_shared/solo_common/claude_cli.py`·`discord_client.owner_reacted`로 하나로(엔진 `engine.llm`·`engine.discord`는 다시 내보내기만). `poststate` 사본은 football-blog에서 없어짐. `swap_insta_photos.py`는 `blog-engine/brands/football/tools/`로 옮겨 고침(창구 경유, `postphotos.header_block`).
- 2026-11-10: football-blog·keyword-scan의 `cadam-pipeline/scripts` sys.path 제거 → `solo_common`.
- 2026-11-10: 해외파 글쓰기 6개 파일(draft·review·series·records·preview·leaguepost)을 `blog-engine/brands/football/`로 이동, 데이터는 `football-blog/facts_cli.py` 창구. 옛 파일은 `_archive/2026-11-10/football-blog/`(11/17 이후 사장님 확인 후 비움).
- 2026-11-10: 해외파 글쓰기 작업 파일(초안 상태·후보·카드·주간 스냅샷·evergreen·hold_cursor)을 `blog-engine/brands/football/outbox/`로 이동(보류 파일 `PUBLISH_PAUSE`는 제자리). 2026-11-13 둘 다 창고로: `_data/football/work/blog-engine/`·`_data/football/work/football-blog/PUBLISH_PAUSE`.
- 2026-11-10: `blog_graphics`·`explainer` 실제 파일을 `_shared/solo_common`에서 `blog-engine/graphics/`로 되돌림(쓰는 곳이 엔진뿐).
- 2026-11-10: 렌테일러 글쓰기 작업 파일(글감 후보·네이버 초안·사진 작업)과 실행 기록을 `blog-engine`으로 이동.
