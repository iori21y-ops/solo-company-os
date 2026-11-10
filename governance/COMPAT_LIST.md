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
| `blog-engine/graphics/` blog_graphics·explainer `.py` | `_shared/solo_common/` 같은 이름 | 호환 파일 | 엔진 1곳 (naver_rewrite) | 해외파 글쓰기가 엔진으로 온 뒤 실제 파일을 `graphics/`로 되돌림 | 해외파 이전 때 |

## B. 사본 (원본을 고치면 같이 고쳐야 하는 것)

| 사본 | 원본 | 내용 | 하나로 합치는 방법 | 기한 |
|---|---|---|---|---|
| `blog-engine/brands/rentailor/trend_api.py` | `cadam-pipeline/scripts/trends/trend_collector.py` | norm·strip_tags·apihub_headers·fetch_news_evidence·CAR_TERMS·searchad_related | 6개를 `solo_common`으로 옮기고 양쪽이 거기서 가져다 씀 | 2026-12-15 |
| `cadam/collectors/lib/` ego_browser.py·ego_bridge.js·polite.py | `_shared/solo_common/` 같은 이름 | 수집기용 브라우저·예절 대기 (ego_browser는 이미 내용이 다름) | 차이를 합친 뒤 lib 쪽을 호환 파일로 | 2026-12-15 |

## C. 아직 규칙을 어기는 곳 (다른 프로젝트 코드를 직접 불러 씀)

| 어디 | 무엇을 | 고치는 방법 | 기한 |
|---|---|---|---|
| `my-shorts/datashorts/run.py` notify() | cadam-pipeline `common.telegram_notifier` | 알림을 `solo_common.notify`로 (my-shorts에 다른 작업의 미커밋 변경이 많아 11/10엔 손대지 않음) | my-shorts 다음 작업 때 |
| `import-lease/crawler/` fetch_official_pdfs·encar_used_prices·lease_fallback·run_daily.sh | cadam `collectors/lib`(ego_browser·notify), `price_crawler` 코드, `linear_alert.py` | lib → `solo_common`, price_crawler 재사용분은 사본 정리 또는 데이터 창구 | 2026-12-15 |
| `football-blog/tools/upgrade_posts.py` | 렌테일러 브랜드 코드 `naver_rewrite.naver_markup` (수동 일회용 도구) | 다음에 쓸 일이 생기면 blog-engine으로 옮김 | 쓸 때 |
| `football-blog/football/` 글쓰기 7개 파일 | (위반은 아님) 아직 엔진으로 못 옴 | `blog-engine/brands/football/README.md`의 3단계 | 별도 세션 |

## D. 끝난 것 (참고)
- 2026-11-10: football-blog·keyword-scan의 `cadam-pipeline/scripts` sys.path 제거 → `solo_common`.
- 2026-11-10: 렌테일러 글쓰기 작업 파일(글감 후보·네이버 초안·사진 작업)과 실행 기록을 `blog-engine`으로 이동.
