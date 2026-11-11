# 인계: 차량 DB 남은 빈칸 정리 (REN-155 후속) — 2026-11-12

사용자 지시: "위에서 체크한 모든 내용을 수정 진행해. 개선 방법을 찾아봐."
이전 작업 전체: ~/projects/_meta/handoff/20261111_car_data_full_alignment.md (§1~13, REN-155 완료분)
빈칸 목록(행 단위): ~/projects/cadam/docs/reports/car_db_gaps_20261112.json (2026-11-12 로컬 DB 조회, 활성 107차종)

## 0. 먼저 알아야 할 환경 (11/12 바뀜)
- 차량 표 원본 = Mac 로컬 DB(스키마 car). 스위치 `collectors/price_crawler/data/car_db/LOCAL`. 쓰기는 반드시 공용 경로
  `trim_spec_parser._sb()`/`patch_grouped()`(로컬 게이트웨이 :54330). `requests`로 SUPABASE_URL 직접 쓰지 말 것
  (직접 써야 하면 `car_db.supabase_url(os.environ["SUPABASE_URL"])`). 상세: cadam-doc docs/strategy/car-data-local-source-plan-20261112.md §10
- 사이트 반영 = `python3 collectors/price_crawler/car_publish.py kick "설명"` → 10분 조용하면 자동 배포(가드 걸리면 보류+디스코드). 매일 12:30 정기 실행
- 사진 업로드(Storage)는 아직 Supabase — Log Ingestion 0.85/1GB(11/21 초기화). 11/21 전엔 하루 수백 장 이내
- ERP는 11/12 07:44부터 로컬 DB 읽고 씀(ERP_LOCAL). ERP 4칸(노출·순서·대표사진·360)은 로컬에서 직접 고치지 말 것
- car_export.py·car_publish.py는 '차량 데이터 로컬 원본' 세션이 관리 — 고칠 땐 그 세션에 먼저 알림
- DB 쓰기 전 백업(backups-manual/), 브랜드·차종 단위로 dry-run → 확인 → 반영
- 월간 가격 수집은 11/21로 보류 중(data/monthly_hold_until). 월간 수집은 trim_options·vehicle_trims를 지우고 다시 넣음 →
  손으로 넣은 값은 사라짐. **고칠 땐 파서/고정 목록(코드)에 넣어 매달 재현되게** 할 것

## 1. 할 일 (점검 결과 → 개선 방법 후보)
| # | 항목 | 수 | 개선 방법 후보 (확인 필요) |
|---|---|---|---|
| 1 | 아반떼 N 옵션 0개 | 1차종 | pdf_cache/hyundai_avante-n_*.pdf 에 옵션 표(빌트인 캠 등) 있는지 확인 → HyundaiParser가 왜 0개인지(N 전용 표 형식?) 파서 수정. 테슬라·BYD 옵션 0은 결정 G(현행 유지) |
| 2 | 트림 기본사양 빈칸 | 52트림 | 대부분 기아 EV 롱레인지(EV3~EV9)·K9·K8 시그니처 블랙·카니발 X-Line·싼타페HEV AWD·아이오닉6·쏘나타 N라인·그랑 콜레오스. 원인 후보: ① 스탠다드/롱레인지가 같은 사양 블록인데 가격이 달라 match_trims(가격 매칭) 실패 → 이름 유사도·sibling_fill 확장 ② 상위 트림 '대비 추가' 블록 ③ 그랑 콜레오스는 trim_specs_renault. trim_spec_parser.plan()으로 차종별 미매칭 사유 확인 |
| 3 | 옵션 0원 | 337행(option 204·package 133, 모두 트림행) | 성격 분류: '기본 포함'(사양에 있는 걸 옵션표가 ● 표시) / 무상 선택(KGM '무상선택', 블랙 퀼팅 등) / 파싱 실패(가격 칸 못 읽음). 사이트는 0원을 추천 카드에서 이미 제외. 파싱 실패만 고치고, 기본 포함은 axis 구분 또는 condition_note '무상 선택' 표기 검토 |
| 4 | 옵션 설명 없음 | 930행(현대 378·기아 318·KGM 92·제네시스 75·르노 43·쉐보레 15·폴스타 9) | option_desc_enrich.plan()의 unmatched_names로 차종별 원인 확인. 가격표에 설명이 없는 단품(선루프·HUD 등)은 ① 같은 이름 옵션의 다른 차종 설명 재사용(같은 브랜드 한정) ② 제조사 견적 API 옵션 설명(현대 product API·기아 configurator·KGM getCar*Option) 수집. 근거 없는 문장 생성 금지 |
| 5 | 옵션 사진 없음 | 98종(이름 기준) | 이미 시도: 수동 확인 연결·같은 계열 재사용·쉐보레 구성기(option_media_manual.json). 남은 것: 현대 configurator 옵션 이미지 API, KGM getCarOptionList 썸네일(일부 'Package' 아이콘은 제외 규칙), 기아 option 이미지. 업로드는 Storage → 11/21 이후 또는 소량 |
| 6 | 색상 칩 없음 | 87행(르노 24·테슬라 22·폴스타 19·기아 10·KGM 7) | color_config 매칭 실패분: 르노 구성기 칩 URL(asset/color/{code}.webp)·테슬라 tesla_colors·폴스타 configurator. color_config_plan의 db_unmatched 확인. 업로드 Storage 주의 |
| 7 | 공차중량 빈칸 | 17행(카니발·카니발HEV·K5·K5HEV·K9·니로·레이·트레일블레이저) | 기아 가격표 제원표/카탈로그(hyundai_catalog.kia_fetch 류) 공차중량 열, 쉐보레는 portal_spec_fills 규칙(다나와·네이버 일치) |
| 8 | 출력·토크 빈칸 | 출력 20·토크 27행(GV80·넥쏘·스타리아 일렉트릭·테슬라) | GV80: brand_specs 제네시스 제원표(하이브리드 신규행 13개가 비었을 가능성). 넥쏘: 현대 카탈로그 제원. 스타리아EV 토크: 카탈로그(US39/40/41 catalog pdf). 테슬라: 공식 미공개 → 빈칸 유지(근거 없으면 넣지 않음) |
| 9 | 연비 빈칸 | 1행(tesla-model-3 Premium RWD) | ev.or.kr 보조금 대상 차종(상온 주행거리만 있음) 또는 테슬라 공식 페이지. 전비 공식값 없으면 유지 |

## 2. 원칙
- 숨김 > 틀린 정보. 근거(가격표·카탈로그·제조사 웹·환경부) 없는 값은 넣지 않음. 출처는 portal_spec_fills.py 같은 코드 표에 기록
- 매달 재삽입되는 표(trim_options·vehicle_trims)는 파서/고정 목록으로 고칠 것. vehicle_powertrains·vehicle_colors는 월간이 빈칸만 채움/upsert
- 사이트 반영은 car_publish kick. cadam-web 코드 push는 사장님 승인 필요(push = 배포)
- 커밋 전 `checkpoint:` 커밋, 다른 세션 미커밋 변경 있으면 먼저 보고. push 전 `git log origin/main..HEAD` 따로 확인, 남의 커밋 섞이면 멈추고 확인

## 3. 끝나면
- REN-155에 댓글(또는 새 이슈로 분리), 이 문서와 메모리 갱신, car_publish kick 후 사이트 확인
