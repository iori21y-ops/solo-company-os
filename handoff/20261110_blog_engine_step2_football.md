# 인계: 블로그 엔진 2·3단계 — 해외파 글쓰기 도구 이사, 공용 도구 합치기 (2026-11-10 밤 작성)

사장님 의도: **글쓰기 규칙 / 글쓰기 도구 / 블로그별 데이터**를 구분. 순서대로 진행 지시(①규칙 꺼내기 ②해외파 도구 이사 ③공용 도구).
규칙: `~/projects/_meta/governance/FOLDER_RULES.md` v1.1 (다른 프로젝트 코드 import 금지 — DB·내보내기 파일·데이터 창구 명령만). 임시 연결 목록: `governance/COMPAT_LIST.md`.

## 끝난 것 (전부 로컬 커밋, push 안 함)
- ① 규칙 꺼내기 완료: 렌테일러 25개 파일 `blog-engine/brands/rentailor/rules/`(loader `engine/rules.py`), 해외파 7개 `blog-engine/brands/football/rules/`(football-blog `config.rule()`가 읽음). 전후 문구 동일 검증.
- 렌테일러 도구·작업 파일·로그는 blog-engine 안. 데이터는 `cadam-pipeline/scripts/content/facts_cli.py` 창구.
- 보류 유지: `cadam-pipeline/data/WRITING_PAUSE`, `football-blog/data/PUBLISH_PAUSE`. 주간 보고 launchd 미설치(승인 대기).

## ② 해외파 도구 이사 — 조사 결과 (AST로 센 실제 사용)
옮길 파일: draft·review·series·records·preview·leaguepost (6개). **matchreview는 옮기지 않는다**(shortsflow 16종·video 업로드를 쓰는 쇼츠 제작 코드).

글쓰기 → 남는 모듈(끊어야 할 것):
- draft → insta(HEADERS, INSTA_DIR, MAX_PER_POST, REVIEWED, _load, _orig, accounts, block, entities_in, face_ok, face_ratio, header_crop, image_log, index, pick, used_today), brain(OK_LICENSE, PHOTO_DIR, context, get, load), media(gather, save_media), insights(block), aiimage(generate), collect(UA)
- review → brain(add_post, update_timeline), collect(collect), insta(entities_in, screen), topics(pick_auto, rank), video(make, proposal_text, stamp, write_script), shortsflow(check_notices, check_scheduled)
- series → collect(db), insta(image_log, index), topics(entity_of)
- records → fdorg(COMPS, find_team, kst, upcoming), warehouse(LEAGUES, db, recent, standings) / preview → fdorg(COMPS, find_team), warehouse(db) / leaguepost → fdorg(find_team), warehouse(db)
남는 모듈 → 글쓰기(끊어야 할 것):
- media·official·video → draft(ask_claude, parse_json, log) / healthcheck·rosterwatch·shortsflow → review(channel, dc, owner_reacted)
- run.py → review(morning, poll, make_records/series/preview/league, make_video, propose_video, channel, dc), matchreview(run_daily)
- tools/: draft_one, draft_test, swap_insta_photos, upgrade_posts → draft/review

권장 순서(각 단계마다 dry-run: `run.py records|series|preview|league|morning --dry-run`, 그리고 5분 poll 로그 확인):
1. **football-blog 안에서 역방향 끊기**: `football/llmutil.py`(ask_claude·parse_json·log)와 `football/discordutil.py`(channel·dc·owner_reacted)를 만들고 draft·review는 거기서 가져다 쓰게(이름은 그대로 노출). media·official·video·healthcheck·rosterwatch·shortsflow·matchreview는 새 모듈을 import.
2. **draft.py의 사진 처리 부분을 football-blog 쪽 한 모듈로**(예: `football/postphotos.py`): insta·brain 사진·media·aiimage 호출을 "글 자료 → 사진 목록/헤더 블록" 함수 몇 개로 모은다. 상태 변경(image_log, used_today)도 그 안에서.
3. **review.py 나누기**: 글 승인·발행(엔진으로 갈 부분) vs 영상 제안·쇼츠 점검(video·shortsflow, football-blog에 남음). poll()이 둘을 차례로 부르는 구조 → football-blog poll은 쇼츠·영상만, 엔진 poll은 글만.
4. **football 데이터 창구** `football-blog/facts_cli.py`(렌테일러와 같은 형식: stdin JSON args → stdout JSON 한 줄): postphotos 함수들, brain.context/get/load·add_post·update_timeline, insights.block, topics.rank/pick_auto/entity_of, collect.collect, fdorg.find_team/upcoming/kst/COMPS, warehouse.standings/recent/LEAGUES, video.make 등(명령형은 반환값 최소화). sqlite 직접 조회(collect.db, warehouse.db)는 엔진에서 DB 파일을 읽기 전용으로 열어도 규칙상 허용.
5. 6개 파일을 `blog-engine/brands/football/`로(본문 그대로·import만 변경, 렌테일러 때 쓴 방식: 상수 비교 + 함수 결과 비교), `sources.py` 작성, brand.yaml 명령 추가, launchd `com.iori21y.football-poll/morning` 등을 `blog-engine/run.py football …`로 교체. football-blog/run.py의 글쓰기 명령은 엔진을 subprocess로 부르거나 제거.
6. 작업 파일(`football-blog/data/posts`, `candidates`, `cards`)을 `brands/football/outbox/`로(쇼츠가 읽는 곳 경로 수정), 로그는 `blog-engine/logs/`. COMPAT_LIST 갱신, graphics를 엔진으로 되돌림.
주의: 해외파 아침 작업 07:40, poll 5분. 파일을 지우기 전에 반드시 호출처 전환부터(11/10에 blog_graphics를 먼저 지웠다가 즉시 복구한 일이 있음).

## ③ 공용 도구 합치기 (②가 끝난 뒤)
두 브랜드가 똑같이 하는 단계를 `blog-engine/engine/`로: Claude 호출+JSON 파싱, 보류 스위치, 디스코드 승인(✅/❌·답장) 처리, 네이버 발행 호출(:3100), 중복 검사, 금액 표기·숫자 검증, 발행 간격 대기열. 먼저 겹치는 함수 목록을 만들고(렌테일러 naver_rewrite·wp_writer vs 해외파 draft·review), 가장 단순한 것(Claude 호출·JSON 파싱·발행 호출)부터 하나씩 합친다. 합칠 때마다 전후 결과 비교.
