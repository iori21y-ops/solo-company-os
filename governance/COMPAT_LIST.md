# 임시 연결·사본·남은 위반 목록 (FOLDER_RULES §6)

> 이사하면서 남긴 "옛 주소 → 새 주소" 연결, 어쩔 수 없이 만든 사본, 아직 규칙을 어기는 곳을 한곳에 적는다.
> 새로 만들면 여기에 한 줄 추가, 없애면 줄을 지운다. **점검일마다 "쓰는 곳 수"를 다시 세고 0이면 없앤다**(삭제 전 사장님 확인).
> 마지막 점검: 2026-11-13 · 다음 점검: 2026-11-27

## A. 임시 연결 (옛 주소로 와도 새 주소로 이어 주는 것)

없음 (2026-11-13 점검: 폴더 링크·별칭 파일 모두 없앰 — 아래 D).

## B. 사본 (원본을 고치면 같이 고쳐야 하는 것)

| 사본 | 원본 | 내용 | 하나로 합치는 방법 | 기한 |
|---|---|---|---|---|
| `content-engine/brands/rentailor/trend_api.py` | `cadam/collect/trends/trend_collector.py` | norm·strip_tags·apihub_headers·fetch_news_evidence·CAR_TERMS·searchad_related | 6개를 `solo_common`으로 옮기고 양쪽이 거기서 가져다 씀 | 2026-12-15 |
| `cadam/collect/lib/` ego_browser.py·polite.py·notify.py | `_shared/solo_common/` 같은 이름 | 수집기용 브라우저·예절 대기·알림 (세 파일 모두 내용이 다름, 2026-11-13 다시 확인. ego_bridge.js는 같음). 쓰는 곳 61개 파일(`sys.path`에 `cadam/collect` 넣고 `from lib…`, 임포리스 포함) | 차이를 합친 뒤 lib 쪽을 호환 파일로 → 부르는 쪽을 `solo_common`으로. 새 패키지 이름은 `lib` 말고 겹치지 않는 이름 | 2026-12-15 |

## C. 아직 규칙을 어기는 곳 (다른 프로젝트 코드를 직접 불러 씀)

| 어디 | 무엇을 | 고치는 방법 | 기한 |
|---|---|---|---|
| `content-engine/brands/rentailor/video/run.py` notify() | cadam `core/scripts/common/telegram_notifier` (`python3 -c "from common.telegram_notifier …"`) | 알림을 `solo_common.notify`로 | 쇼츠 과정 재설계 때 |
| `import-lease/collect/encar_used_prices.py`·`collect/fetch_official_pdfs.py`·`process/lease_fallback.py`·`check/db_size_check.py`·`ops/run_daily.sh` | cadam `collect/lib`(ego_browser·notify)·`collect/price_crawler` 코드·`collect/.env`·`core/scripts/common/linear_alert.py` | lib → `solo_common`, linear_alert → `solo_common`(두 사업이 씀), price_crawler 재사용분은 사본 정리 또는 데이터 창구 | 2026-12-15 |
| `content-engine/brands/football/video/*` (11개 파일) | `sys.path`에 `football-blog` 넣고 `football.*` 패키지를 직접 import | 쇼츠 과정 재설계 때 `football/content/`와 함께 정리 | 쇼츠 재설계 때 |
| `football-blog/ops/tools/upgrade_posts.py` | 렌테일러 브랜드 코드 `naver_rewrite.naver_markup` (수동 일회용 도구, `football.draft`가 없어 **지금은 실행 안 됨**) | 다음에 쓸 일이 생기면 `content-engine/brands/football/tools/`로 옮김 | 쓸 때 |

## D. 끝난 것 (참고)
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
