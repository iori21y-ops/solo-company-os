# 임시 연결·사본·남은 위반 목록 (FOLDER_RULES §6)

> 이사하면서 남긴 "옛 주소 → 새 주소" 연결, 어쩔 수 없이 만든 사본, 아직 규칙을 어기는 곳을 한곳에 적는다.
> 새로 만들면 여기에 한 줄 추가, 없애면 줄을 지운다. **점검일마다 "쓰는 곳 수"를 다시 세고 0이면 없앤다**(삭제 전 사장님 확인).
> 마지막 점검: 2026-11-10 · 다음 점검: 2026-11-24

## A. 임시 연결 (옛 주소로 와도 새 주소로 이어 주는 것)

| 옛 자리 | 새 자리 | 종류 | 쓰는 곳 (11/10) | 없애는 조건 | 기한 |
|---|---|---|---|---|---|
| `cadam/cadam-naver` | `blog-engine/publishers/naver` | 폴더 링크 | 코드 0곳 (문서 언급만) | 1주일간 발행·백업 오류 없음 | 2026-11-17 |
| `cadam/cadam-n8n` | `cadam/collectors` | 폴더 링크 | 코드 46곳 (`_meta/handoff/cadam-n8n-references-20261110.txt`) | 46곳을 `collectors` 또는 `solo_common`으로 고친 뒤 | 2026-12-15 |
| `cadam-pipeline/scripts/common/` discord_client·notify·claude·ego_browser·polite·warehouse·llm_client·content_extractor `.py` | `_shared/solo_common/` 같은 이름 | 호환 파일(같은 모듈을 가리킴) | cadam 코드 65개 파일 | 65곳의 `from common…`을 `from solo_common…`으로 바꾼 뒤 | 2027-01-31 |
| `cadam-pipeline/scripts/content/evidence_body.py` | `_shared/solo_common/evidence_body.py` | 호환 파일 | 1곳 (shorts_scripts) | 그 1곳을 고친 뒤 | 2026-12-15 |
| `football-blog/data/posts` | `blog-engine/brands/football/outbox/posts` | 폴더 링크 | football-blog 코드 6곳: `poststate`(videoflow가 영상 상태를 읽고 씀), `insta._used_on`(사진 14일 중복 검사), `topics.recent_entities`, `run.py` video 명령, `tools/` 2개 | 영상 상태를 football-blog 쪽 파일로 떼고, 사진 중복 검사·최근 글감은 엔진이 창구 인자로 넘기게 바꾼 뒤 | 2026-12-15 |
| `football-blog/data/cards` | `blog-engine/brands/football/outbox/cards` | 폴더 링크 | `insta.HEADERS`(썸네일 크롭을 `cards/headers/`에 씀) + 11/10 이전 글 18편 본문에 적힌 옛 카드 경로 | 크롭 저장 위치를 football-blog 사진 창고로 옮기고(`_orig`·`recheck_photos`의 `/cards/headers/` 판별 같이 수정), 옛 글 경로가 더 필요 없을 때 | 2026-12-15 |

## B. 사본 (원본을 고치면 같이 고쳐야 하는 것)

| 사본 | 원본 | 내용 | 하나로 합치는 방법 | 기한 |
|---|---|---|---|---|
| `blog-engine/brands/rentailor/trend_api.py` | `cadam-pipeline/scripts/trends/trend_collector.py` | norm·strip_tags·apihub_headers·fetch_news_evidence·CAR_TERMS·searchad_related | 6개를 `solo_common`으로 옮기고 양쪽이 거기서 가져다 씀 | 2026-12-15 |
| `blog-engine/brands/football/` llmutil.py·discordutil.py·poststate.py | `football-blog/football/` 같은 이름 | Claude 호출·JSON 파싱·로그 / 디스코드 채널·반응 확인 / 글 상태 파일 읽기·저장 (import 한 줄만 다름, 양쪽이 같이 씀: 엔진=글, football-blog=영상·쇼츠·수집) | 엔진 공용 단계(인계 ③)로 합치거나 `solo_common`으로 옮김. 영상 상태를 글 상태 파일에서 떼면 poststate 사본은 없어짐 | 2026-12-15 |
| `cadam/collectors/lib/` ego_browser.py·polite.py·notify.py | `_shared/solo_common/` 같은 이름 | 수집기용 브라우저·예절 대기·알림 (세 파일 모두 내용이 다름, 2026-11-11 확인. ego_bridge.js는 같음) | 차이를 합친 뒤 lib 쪽을 호환 파일로 | 2026-12-15 |

## C. 아직 규칙을 어기는 곳 (다른 프로젝트 코드를 직접 불러 씀)

| 어디 | 무엇을 | 고치는 방법 | 기한 |
|---|---|---|---|
| `my-shorts/datashorts/run.py` notify() | cadam-pipeline `common.telegram_notifier` | 알림을 `solo_common.notify`로 (my-shorts에 다른 작업의 미커밋 변경이 많아 11/10엔 손대지 않음) | my-shorts 다음 작업 때 |
| `import-lease/crawler/` fetch_official_pdfs·encar_used_prices·lease_fallback·run_daily.sh | cadam `collectors/lib`(ego_browser·notify), `price_crawler` 코드, `linear_alert.py` | lib → `solo_common`, price_crawler 재사용분은 사본 정리 또는 데이터 창구 | 2026-12-15 |
| `football-blog/tools/upgrade_posts.py` | 렌테일러 브랜드 코드 `naver_rewrite.naver_markup` (수동 일회용 도구). 2026-11-10부터 `football.draft`도 없어 **지금은 실행 안 됨** | 다음에 쓸 일이 생기면 blog-engine으로 옮김 | 쓸 때 |
| `football-blog/tools/swap_insta_photos.py` | (위반은 아님) `football.draft`를 불러 쓰는데 그 파일이 2026-11-10 엔진으로 이사해 **지금은 실행 안 됨**(수동 일회용 도구) | 다시 쓸 일이 생기면 `draft.header_block` → `postphotos.header_block`으로 고침 | 쓸 때 |
| `football-blog` → `blog-engine/brands/football/outbox/` | (위반은 아님) football-blog 코드가 엔진 작업 파일에 **쓴다**: videoflow가 글 상태 파일의 `video` 항목, `insta.header_crop`이 `cards/headers/` (위 A의 링크 두 줄과 같은 일) | A의 두 링크를 없앨 때 같이 해결 | 2026-12-15 |
| `cadam-pipeline/scripts/common/writing_pause.py` | `blog-engine/brands/rentailor/writing_pause.py` | 글쓰기 보류 스위치 도우미. 내용이 다르고 cadam 안에서 부르는 곳이 없음(2026-11-11 확인) | 부르는 곳이 정말 없는지 한 번 더 본 뒤 보관함으로 | 2026-12-15 |
| 해외파 글쓰기 실행 기록 | (위반은 아님) 엔진 작업인데 기록이 `football-blog/logs/morning.log`·`poll.log`에 남는다(launchd가 football-blog/run.py를 실행하므로) | launchd 교체 때 `blog-engine/logs/`로 | 2026-11-24 |
| launchd `com.iori21y.football-morning`·`-poll` | (위반은 아님) **2026-11-11부터 운영 보류로 내려 둠** — 다시 켜기 전까지 기한 보류. 켜지면 `football-blog/run.py`를 실행하고, 그 안에서 엔진(`blog-engine/run.py football …`)을 부른다 | 며칠 안정 확인 뒤 사장님 확인을 받아 엔진 직접 실행으로 교체(자동 점검·잠금·영상 poll을 어떻게 나눌지 같이 결정) | 2026-11-24 |

## D. 끝난 것 (참고)
- 2026-11-10: football-blog·keyword-scan의 `cadam-pipeline/scripts` sys.path 제거 → `solo_common`.
- 2026-11-10: 해외파 글쓰기 6개 파일(draft·review·series·records·preview·leaguepost)을 `blog-engine/brands/football/`로 이동, 데이터는 `football-blog/facts_cli.py` 창구. 옛 파일은 `_archive/2026-11-10/football-blog/`(11/17 이후 사장님 확인 후 비움).
- 2026-11-10: 해외파 글쓰기 작업 파일(초안 상태·후보·카드·주간 스냅샷·evergreen·hold_cursor)을 `blog-engine/brands/football/outbox/`로 이동(보류 파일 `PUBLISH_PAUSE`는 제자리).
- 2026-11-10: `blog_graphics`·`explainer` 실제 파일을 `_shared/solo_common`에서 `blog-engine/graphics/`로 되돌림(쓰는 곳이 엔진뿐).
- 2026-11-10: 렌테일러 글쓰기 작업 파일(글감 후보·네이버 초안·사진 작업)과 실행 기록을 `blog-engine`으로 이동.
