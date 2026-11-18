# content-engine 동시 작업 나눔 (2026-11-17~)

> 같은 리포(`~/projects/content-engine`)를 두 세션이 함께 고치는 동안의 약속. 사장님 지시(11-17): "겹치는 게 없도록".
> 끝나면 이 파일 맨 위에 "종료" 날짜를 적는다.

## 두 세션이 맡은 것

| 세션 | 맡은 일 | 주로 고치는 곳 |
|---|---|---|
| 제목·사진 세션 | 모든 글의 제목 생성, 사진 넣기 규칙 | 제목·사진 규칙 문서(`rules/**`, `brands/rentailor/rules/**`의 제목·이미지), 프롬프트, 제목을 만드는 코드, 사진 고르기·넣기 코드(`blog_images.py`, `deep_photos.py`, `tracker_photos.py`, `cover_card.py`, `wp_cover.py`, `blog_cards.py`, `naver_rewrite.py`의 사진 넣기·제목 부분, `naver_digest.py`의 제목·프롬프트) |
| 자동 발행 세션 | 무승인 자동 운영(실패 재시도, 알림, 감시, 보류·재개, 데이터 자동 채움) | `naver_rewrite.py`의 발행·대기열·마감·알림 부분(`publish`, `check_queued`, `check_stuck`, `check_digest_deadlines`, `digest_run`의 예외 처리, `main`의 poll 순서), `car_news.py`의 `daily`·`poll`·`make_draft` 저장 순서, `tips.py`의 `prepare` 반복문, `topic_selector.py`의 `hold_command`, `daily_stop.py`, `publish_slots.py`, `channel_check.py`, `brand.yaml`의 `auto_mode`·`publish_slots`, `publishers/wordpress/client.py`의 재시도, cadam `check/monitoring/*` |

자동 발행 세션은 **제목 문구·제목 규칙·사진 고르기·사진 개수·사진 위치를 건드리지 않는다.** 사진이 0장일 때 "알림에 표시"만 하고, 사진을 고르는 방식은 바꾸지 않는다.

## 같은 파일을 고칠 때 (특히 `naver_rewrite.py`, `car_news.py`, `brand.yaml`)

1. 고치기 직전에 `git status`와 `git log --oneline -5`를 본다. 상대 세션의 미커밋 변경이 그 파일에 있으면 **그 파일은 고치지 않고** 다른 항목부터 한다.
2. 한 번에 작게 고치고 바로 커밋한다 (`git add <내 파일>` → `git commit -- <내 파일>`). 미커밋 상태로 오래 두지 않는다.
3. 함수 이름·인자·상태 파일의 칸 이름(`title`, `photos`, `cover`, `body` 등)을 바꿔야 하면 여기에 먼저 적는다.
4. `brand.yaml`은 고친 뒤 `python3 run.py rentailor`로 읽히는지 확인한다(한 글자 오류로 글쓰기 전체가 멈춘다).
5. push는 사장님 승인 후. 상대 세션의 커밋이 섞여 올라가면 보고한다.

## 서로 알아야 할 변경 (생기면 아래에 한 줄씩)

- 11-17 자동 발행 세션: `deep_publish.prepare`는 주소만 채우고 워드 페이지 공개는 `go_live`가 한다(`tracker_publish`도 같음). `tips.preview_draft` 추가. `brand.yaml auto_mode` 추가. `daily_stop.py` 새 파일.
- 11-17 자동 발행 세션: 21:40에 글쓰기 보류가 자동으로 켜진다(시범). 보류 중에는 초안·발행이 안 돈다 — 시험 발행이 안 되면 이것부터 확인.
- 11-17 제목·사진 세션: `engine/text.py`에 `clip_sentences`(설명 문구 문장 단위 자르기)·`title_problems`(제목 검사) 추가. `deep_publish.publish_fixed`가 자료 페이지 요약 칸(`excerpt`)을 채운다. 트래커 워드 제목 맨 앞에 그달. `naver_rewrite.download`는 `blog_images.fetch_image`로 받아 항상 `.jpg`로 저장(실패하면 예전 방식). `select_images`가 고른 사진을 한 번 더 확인(`verify_picks`, 모델 호출 1번 추가). 네이버 심층·종합뉴스 사진은 `used_hashes.json`에 `naver-<key>`로 기록. 상태 파일 칸 이름은 바꾸지 않음.
- 11-17 제목·사진 세션(2차): 제목 틀 3가지(질문형 강제 검사 제거 — `deep_post.py`·`deep_series.py` 체크리스트 1번 이름이 "제목에 검색어…"로 바뀜), 종합뉴스 제목 검사 1회 다시 쓰기(`naver_digest.py`), 표지 카드 검색어+큰 숫자(`cover_card.py`), `select_images(title_cars_only=)` 추가, 큰 차량 이미지 `cover_card.hires_for`(표지·`wp_cover`·`own_car_photo`·`tracker_photos`). 성과 확인 REN-239, 차량 이미지 REN-238.
- 11-17 제목·사진 세션(3차): 트래커 상태 파일에 새 칸 `band`({kw, num} — 워드 대표 이미지 글자 띠 문구, `tracker_sales`·`tracker_rent.photo_plan` → `tracker_publish` → `wp_cover.refresh_card(slug, car, site, band)`). `wp_cover.set_photo`·`draw_photo`에 `band` 인자 추가(없으면 예전과 같음). `cards.json`에 `band:<slug>` 칸.
- 11-18 자동 발행 세션: `car_news.py` 상태 파일 새 칸 `pending_drafts`(사건별 초안 id)·`draft_retry`·`alerts`, 항목 새 칸 `publish_failed`·`publish_error`·`publish_retry_at`·`cover_failed`·`photo_done`, 새 상태값 `publish_gave_up`, 묶음 키 `"<날짜>-2"`(같은 날 재시도분). `make_draft(post, st=None, save=None)` 인자 추가. `tips.py` 새 칸 `setup_pending`. `publishers/wordpress/client.py` `update_post`·`rankmath_meta`는 5xx·연결 오류에 2회 재시도(`create_post`는 재시도 없음). 제목·사진 고르는 방식은 안 바꿈.
- 11-18 자동 발행 세션: `naver_rewrite.py` 새 상태 칸 `publish_attempts`·`retry_pending`·`last_error_tail`·`reslotted_at`·`draft_fails`·`draft_retry_at`, 새 함수 `publish_guarded`·`missed_slot`·`digest_retry_due`. 발행이 실패하면 상태가 review가 아니라 queued(10분 뒤 자동 재시도, 3번까지)로 갈 수 있다 — 재시도 때 `publish()` 앞부분(사진 추가·표지·짝 글 카드)이 다시 돈다(여러 번 돌아도 결과가 같아야 함). `brand.yaml relink_hours` [20, 22]. `daily_stop.py`·`topic_selector.hold_command` 보강.
- 11-18 자동 발행 세션(감시): 새 파일 `engine/heartbeat.py`·`brands/rentailor/watchdog.py`, `engine/naver.server_alive`. `naver_rewrite.py` poll 끝에 심박 기록(`_data/rentailor/work/content-engine/watchdog/naver_poll.json`), `publish()` 맨 앞에서 발행 서버 응답 확인 — 죽어 있으면 글이 queued로 10분 미뤄짐(새 상태 칸 `server_wait`, `publish_attempts`는 안 올림). 새 예약 작업 `com.blogengine.watchdog`(30분)·`com.blogengine.llm-check`(06:50). 제목·사진 코드는 안 건드림.
- 11-18 자동 발행 세션 → 제목·사진 세션에 알림: 11:38 `deep-G-plate` 발행 준비 중 로그 `deep hero skipped: Extra data: line 3 column 1 (char 343)` → `no photos available — publishing without`(사진 0장). 사진 고르기 응답의 JSON 뒤에 글자가 더 붙어 파싱이 실패한 것으로 보임(11-17에 추가된 사진 확인 단계 쪽 추정) — 사진 코드라 이쪽에서는 안 고침. 이 글은 그 뒤 1인칭 검사("내가 고르려는")에 걸려 발행되지 않고 카드로 되돌아가 있음(status review, ok_ignored).
- 11-18 자동 발행 세션(2순위, 워드 쪽): `car_news` 항목 새 칸 `data_warn`·`recheck`·`recheck_pending`·`refreshed`·`live_check`. 어제 이전에 만든 초안은 발행 직전에 자료를 다시 만들어 확인하고(`stale_recheck`), 가격 소식은 `build()` 결과의 제목·요약·본문이 달라졌으면 워드 초안을 그 결과로 바꾼 뒤 발행한다(제목 만드는 방식은 그대로 — `build()`가 내는 값을 씀). `tips.build` 반환값에 `data_warn`. `data_gate`에 `watch_warnings`·`warn_list`·`warn_text`·`strict_mode`(기존 `require`·`query` 그대로). `channel_check`에 8번 점검 `wp_post_pages`(최근 7일 워드 글·발행된 팁 주소가 사이트에서 열리는지).
