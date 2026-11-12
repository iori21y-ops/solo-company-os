# 인계: 15일 정기 가격수집 앞당겨 실행 + 빈칸 재점검 — 2026-11-12

사용자 지시(11/12): "15일 하는 정기수집을 지금 진행하고 빠진 부분을 다시 점검하자"
이전 작업: ~/projects/_meta/handoff/20261112_car_db_gaps.md (§4), 결과 ~/projects/cadam/docs/reports/car_db_gaps_result_20261112.md

## 00. 수집 전에 먼저 만들 것 (사용자 결정 11/12: "새 세션에서 1·2 먼저")
배경: color_config 가 이미 올린 사진은 건너뛰게 바뀜(collectors 02fb9bd). 그 대가로 "제조사가 같은 주소의 사진을 바꾼 경우·
업로드가 깨진 경우"가 다시 올라가지 않음. 또 매칭 실수·처리 실수(배경 제거 실패 등)는 예전에도 아무도 확인하지 않았음.
1. **원본 변경 감지** (color_config.py, 가능하면 option_media_sync 도 같은 방식): 제조사 사진 주소에 HEAD 요청 →
   ETag/Last-Modified/Content-Length 를 로컬 색인(data/ 아래 json, git 제외 여부 확인)에 기록. 지난 값과 다르면 그 사진만
   다시 받아 올림(같은 경로 x-upsert). HEAD 는 제조사 서버로만 가니 Supabase 사용량 없음. 첫 실행은 색인만 채우고 재업로드 0.
   HEAD 를 안 주는 서버는 건너뛰고 보고(무작정 재업로드 금지).
2. **눈으로 보는 확인표**: 정기수집 뒤 '이번에 새로 올라가거나 바뀐' 칩·색상 사진·옵션 사진만 차종별로 한 장(PNG 접촉 시트:
   사진 + DB 색/옵션 이름 + 구성기 이름)으로 → docs/reports/ 에 저장, SendUserFile 로 사용자에게 보여줌. run_monthly.sh 끝에
   자동 생성 단계로 넣는 것까지(실패해도 수집은 성공 처리). 매칭·처리 실수는 코드가 못 알아채니 이것이 유일한 검사.
1·2 dry-run 확인 → 커밋(collectors push는 보류 결정 유지) → 그다음 §0 정기수집.

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

## 진행 (11/12 세션 2, 사용량 한도로 중단)
- §00 완료·커밋 collectors 4599518 (push 안 함): image_watch.py(HEAD 지문 색인 data/image_fingerprints/, git 제외),
  color_config `--review-dry`·변경분만 재업로드, option_media_sync 원본 변경 시 재다운로드, image_review_sheet.py, run_monthly.sh 끝에 확인표 단계.
- dry-run: 색상 이미 올린 1,623장 색인 기록(HEAD 미지원 0), 업로드 예정 121장, 확인표 128장(빨간 테두리 44) →
  docs/reports/image_review_dry_20261112/. 옵션 원본 3,553개 HEAD 2회 연속 변경 0(안정). **색상 HEAD 2회차 안정성 검사는 아직** —
  `python3 -c "import image_watch as iw;print(iw.summary(iw.check(list(iw.load('colors')),'colors')[0]))"` 로 changed≈0 확인 후 수집.
- 남은 일: 빨간 테두리 44장 확인 → run_monthly.sh --force(→car_publish 자동 배포 주의) → 확인표 사용자에게 → car_db_gaps §1 비교 → REN-155·메모리.

## 완료 (11/12 세션 2 이어서, 12:30)
- 색상 HEAD 2회차: 1,621 same, 쉐보레 2장만 서버마다 값이 달라 HEAD_SKIP(20a0bf7). 옵션 3,553 same.
- `run_monthly.sh --force` 완료(가격 변경 56건·트림 가격 10건). 색상 단계 409 실패 → vehicle_colors 순번 수정 후 재실행.
- 확인표 docs/reports/image_review_monthly_20261112_1103/ (사용자에게 전송). 제네시스 매트 오류 발견·수정, 운영 사이트 GV80 '마테호른 화이트 매트' 확인.
- 결과 표: docs/reports/car_db_gaps_result_20261112.md 맨 아래. collectors 커밋 4599518~85e812c (push 보류 유지).
- 완료표시 monthly_last_success = 2026-11-1 → 11/21 보류 해제 뒤 15일분 다시 돎(정상, 원치 않으면 사용자 확인 후 2026-11-2로).
## 남은 일
- GV70 마테호른 화이트: 구성기는 매트(FT7), 가격표엔 매트 이름 없음 → 유광으로 둠(사용자 판단 필요)
- 스타리아 일렉트릭: 새 내장색 칩 없음(구성기 0개 반환) · 가격표 대조 불일치 4트림(도구 한계 추정, 미확인)
- 아이오닉 6 N 가격표 옵션 2개 사진·설명 없음
- 추가 수정 a0c2768: color_config가 로컬 게이트웨이 1,000행 상한 때문에 색상 115행의 경로를 못 보고 재업로드·'연결 변경' 오기록 → 페이지 단위 읽기. 이 세션 Storage 업로드 약 280장 중 약 160장은 재실행·이 버그로 인한 같은 경로 재업로드.
- 사용자 결정 11/12: GV70 마테호른 화이트 → 매트 +70만(d00f904, 운영 반영), monthly_last_success = 2026-11-2 (11/21 이후 15일분 재수집 안 함, 다음은 12월 1회차)
- 11/12 오후 추가: 스타리아 일렉트릭 구성기 US39·US40·US41 추가 → 새 내장색 칩 반영(a4ffa53) · 아이오닉 6 N 스포츠 디자인 패키지 사진(구성기 N퍼포먼스파츠, 전용 매트) + 설명 3건 가격표 근거 고정(f5deba2, cadam-doc b12f686·923975c) · 가격표 대조 스타리아 불일치는 다른 세션 96423b0로 해결, 재실행 불일치 0종
- 11/12 오후: 공식 근거 출처 조사 → 한국에너지공단 수송통합운영시스템(min24.energy.or.kr, 차량 상세 '자동차 기본제원' = 공차중량·출력·토크·전비, 브라우저로만 조회됨, 테슬라 토크 칸은 출력 복사 오류) · 넥쏘 토크 350Nm(현대 디 올 뉴 넥쏘 카탈로그). portal_spec_fills 8행 반영(02695ba), power_note 칸 신설(로컬 DB·car_export), 사이트 표시 코드 cadam-web 99073a3 로컬 커밋(push 승인 대기). 보류: 레이(승용 1,090/밴 1,080), 카니발 19"(7/9인승 혼합 행), 트레일블레이저 18" FWD(연비 불일치). 테슬라·폴스타 색상 칩 = ego-browser 필요(미착수)
- 11/12 오후: 테슬라·폴스타 색상 칩 39행 반영(ego-browser 수집 → swatch_import.py, collectors 6ce7441 미push — push가 자동 권한 검사에서 막힘, 사용자 확인 필요). 폴스타 3 Midnight·Storm은 구성기에 없어 빈칸. 확인표 docs/reports/image_review_swatch_20261112/
