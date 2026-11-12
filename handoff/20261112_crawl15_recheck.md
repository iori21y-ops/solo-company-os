# 인계: 15일 정기 가격수집 앞당겨 실행 + 빈칸 재점검 — 2026-11-12

사용자 지시(11/12): "15일 하는 정기수집을 지금 진행하고 빠진 부분을 다시 점검하자"
이전 작업: ~/projects/_meta/handoff/20261112_car_db_gaps.md (§4), 결과 ~/projects/cadam/docs/reports/car_db_gaps_result_20261112.md

## 0. 실행 전 확인 (먼저 사용자에게 한 줄 확인받을 것)
- 수집 스크립트: `collectors/price_crawler/run_monthly.sh` (launchd 매일 02:00, 1~14일·15일~ 각 1회). 지금은
  `data/monthly_hold_until` = 2026-11-21 로 **보류 중** → 수동 실행은 `run_monthly.sh --force` (보류·완료표시 무시).
- 보류 이유 = Supabase 무료 한도(Log Ingestion 0.85/1GB, 11/21 초기화). 차량 표는 11/12부터 로컬 DB라 수집 자체는 괜찮음.
- 색상 단계 `color_config.py --monthly`: 예전엔 매번 약 1,700장을 Supabase Storage에 다시 올렸으나, 11/12 수정(collectors 커밋
  "perf(colors): reuse Storage paths…")으로 이미 올린 사진은 건너뜀 → 11/12 계획 기준 133장만 업로드. **전체 그대로 실행해도 됨.**
  (차량 표는 로컬 DB, 사진 파일만 Supabase Storage. `option_media_sync.py --apply` 도 새 파일만 올림)
- 11/12에 --force 실행하면 완료표시가 `2026-11-1`로 남아 11/21 보류 해제 뒤 15일분(`2026-11-2`)이 또 돈다 → 정상(가격 재확인). 원치 않으면 끝난 뒤 `data/monthly_last_success` 를 `2026-11-2` 로(사용자 확인 후).
- 끝나면 `car_publish.py kick` 이 스크립트 안에서 자동 실행 → 10분 조용하면 cadam-web main에 데이터 자동 push(=배포).
  가드(트림·옵션 30%↓, 가격 ±20%)에 걸리면 보류+디스코드 → `car_publish.py status` 로 확인, 승인은 사용자.
- 실행 시간이 길다(수십 분). Bash `run_in_background` 로 돌리고 `crawler.log` 를 본다. 잠금: `data/.monthly.lock`.

## 1. 수집 후 재점검 (11/12 고친 것이 월간 재삽입 후에도 재현되는지)
기준 목록: `docs/reports/car_db_gaps_20261112_after.json` · 재측정: `cd collectors/price_crawler && python3 car_db_gaps.py --json <새파일>`
(환경: `set -a; source /Users/kim/projects/cadam/cadam-n8n/price_crawler/.env; set +a`)
| 확인 | 기대값 (11/12 오전 기준) |
|---|---|
| 아반떼 N 옵션 | 10개(선루프·N DCT 패키지·빌트인 캠(조건)·버켓 시트·단조 휠·스마트센스Ⅰ/Ⅱ(axis package)·N 컴포트(버켓 시트와 배제)·시티/트랙 팩(구성 설명)) |
| 니로 EV 옵션 | 16개 + 설명 15행, 사진 4종(HUD·스마트 커넥트·선루프·하만카돈, 수동 목록) |
| 아이오닉 6 N | **가격표 옵션 4개로 바뀜**(빌트인 캠 2 Plus 포함), '제조사 견적 화면 기준' 행은 사라짐 = 정상 |
| 사양 빈 트림(사이트 기준) | trims_no_spec_site = 0 (쏘나타 N라인·카니발HEV X-Line·그랑 콜레오스 4·코나EV 모던 플러스) |
| 0원 옵션 | 전부 '기본'/'무상선택' (파싱 실패 0) |
| 공차중량·출력·토크 | vehicle_powertrains 는 월간이 빈칸만 채움 → 유지. `python3 portal_spec_fills.py` 미리보기 0행이면 정상(행이 교체됐으면 --apply) |
| 옵션 0개 차종 | 7 (테슬라 3·BYD 4 = 결정 G) — 늘었으면 그 차종 파서 확인 |
| 색상 칩 | 86 (①로 color_config를 뺐다면 새 색상 행은 칩 없음 → 11/21 이후 color_config --monthly) |
새로 생긴 빈칸은 원인(가격표 형식 변경·새 차종·파서) 확인 후 코드로 고칠 것(손으로 넣은 값은 다음 수집에 사라짐).
`reports/verify_prices` 결과(가격표 vs DB)와 디스코드 가격 변동 요약도 함께 본다.

## 2. 원칙 (그대로)
근거 없는 값 금지(숨김 > 틀린 정보) · 쓰기는 ts._sb/patch_grouped(로컬 게이트웨이) · dry-run → 백업(backups-manual/) → 반영 ·
월간 재삽입 표는 파서/고정 목록 · cadam-web 코드 push는 승인 · 커밋 전 checkpoint · push 전 `git log @{u}..HEAD` 따로 확인

## 3. 열린 일
- collectors 미push: 내 a305460(색상 별칭) + 다른 세션 1456294·f2d3e53·d05c1f4·aa0dccd·f29f18b(약관 창고 이전).
  사용자 결정(11/12): **보류** — 약관 이전 세션이 끝나고 push할 때 함께 나감. 이 세션이 임의로 push하지 말 것
- 아반떼 N 옵션 사진: 현대 견적 화면에 차종 없음 → 공식 출처 없음(유지)
- 색상 칩: 테슬라·폴스타 소스 없음, 쉐보레 구성기 403(11/12)
- 남긴 빈칸(근거 없음): 카니발 19" 캠 무게 2·레이 1·트레일블레이저 2, 테슬라 출력·전비, 넥쏘 토크
- 끝나면 REN-155 댓글·이 문서·메모리(project_car_db_gaps_20261112) 갱신
