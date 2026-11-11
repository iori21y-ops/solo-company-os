# 인계: 차량 데이터 전수 정합 (REN-155) — 2026-11-11 정리본

사용자 지시: "모든 차종의 옵션·색상·이미지·가격 등 전체 데이터를 다 맞춰야 한다. 끝까지 분석해서."
점검 보고서: ~/projects/cadam/docs/reports/car_data_full_audit_20261111.md ('수정 계획' 1~6)

## 1. 현재 상태 한눈에

| 수정 계획 | 상태 |
|---|---|
| 1 가격표 파서 (제네시스·기아·KGM·르노·현대·세제가·CO₂) | ✅ DB 반영 완료 |
| 2 색상 (추가금·누락색·코드·투톤) | ✅ DB 반영 완료 (color_config 963행 포함) |
| 3 제원 (GV80 재구성·하이브리드, GV70) | ✅ DB 반영 완료 |
| 4 옵션 설명 | ◑ KGM·쉐보레 123행 완료 / 르노 3건 남음 |
| 4 옵션 사진 | ◑ 이름 정규화 재연결 3행 / 약 40종 남음 |
| 5 사이트 코드 (cadam-web) | ⬜ 미착수 |
| 6 판단 항목 | ✅ 결정 받음(§2 '6번 판단 결과') → 실행은 ⬜ 미착수 |
| collectors push | ✅ 완료 (11/11, origin/main = 0209900, 다른 세션 렌트료 커밋 3개 포함) |
| REN-155 Linear 댓글 | ⬜ 마무리 때 |

DB 수치(작업 전 → 후): 옵션 2865→2932, 옵션 사진 2318→2360, 옵션 설명 1611→1759, 트림 487→488, 제원 548→560, 색상 1063→1068.
기준점 저장: option_change_log --baseline → collectors/price_crawler/data/option_snapshots/snapshot_20261111.json (이번 교정분은 '제조사 변경'으로 기록되지 않음).

## 2. 사용자 결정 (이미 확정, 2026-11-11)
1. 특수 판매형(장애인용·렌터카 LPG·운전교습·영업용·키즈/휠체어/구급·밴·도너) — 넣지 않는다. → 현대 파서가 자동 제외(`_SPECIAL_SALE`)
2. 투톤 추가금 — 색상(vehicle_colors.extra_price)에만 둔다. → 셀토스·베뉴·KGM 5종·EV5 GT 투톤 옵션 행 삭제, 색상 행에 합침
3. 제네시스 가격 — 가격표 기준 (G90 파노라마 200만/LWB 250만·빌트인 캠 80만 = DB 일치)
4. 캐스퍼 일렉트릭 대표 사진 — 전용 사진으로 교체 (5번 사이트 작업에서, 소스 후보: 현대 vr360 AX07 프레임)

### 6번 판단 결과 (2026-11-11, §4 표 기준)
- A 웹 전용 색: **추가**(웹 견적 화면 기준, 추가금은 웹 표시값). DB 쓰기 전 백업
- B 팰리세이드 인승별 추가금: 현행 유지(10만 + 비고 9인승 9만)
- C 무쏘 EV·EVX 밴 세제가: 빈칸 유지
- D 코나·EV5 투톤: **A에서 투톤 색상 행을 만들고 '투톤 루프' 옵션 행은 삭제**(결정 2와 통일). 색상 행 금액에 투톤 가격 포함
- E 베뉴 실내 블랙 중복: 하나로 합침
- F EV4 블랙&화이트: **기아 웹 견적 화면 확인 후** 있으면 추가, 없으면 삭제
- G 테슬라·BYD 옵션: 현행 유지
- H 근거 없는 제원(렉스턴 써밋, 스타리아 일렉트릭 라운지·리무진 4트림, 테슬라·N 일부 배터리·토크): **다른 출처로 채움**(제조사 웹 제원표·카탈로그 우선, 출처 기록)
- I 구동방식 빈칸 23종: '전륜'으로 채움(전륜 전용 차만, 확인 후)
- J ERP 잔존율: 트림 최저가 기준으로 변경(cadam-erp, 운영 반영은 재시작 승인 필요)
- K 무쏘·무쏘 EV 대표 사진: **같은 사진인지 확인**, 같으면 전용 사진 교체(cadam-web push 승인 필요)

## 3. 남은 작업 (순서대로)

### 3-1. 옵션 사진 약 40종 (4번)
- option_media 자체에 사진 출처가 없는 것: KGM 로마숫자 패키지(Ⅰ/Ⅱ), 투싼 익스테리어 디자인 Ⅱ/II, 스포티지 '스타일', 제네시스 휠 9종, 쉐보레 페이지 사진, g70-sb 스포츠 패키지(AWD/2WD), 코나·코나HEV '클러스터(12.3인치 컬러 LCD)', 투싼 하이브리드 '익스테리어 디자인I'
- 방법: option_media_build의 출처 이름 매칭 보강 → option_media_sync --apply. 반영 전 백업.
### 3-2. 르노 옵션 설명 3건 (4번)
- option_desc_anchor.py에 르노 구간 추가 또는 수동 3행. 근거: 르노 가격표 PDF 구성 문구.
### 3-3. 사이트 코드 (5번, cadam-web — push = 즉시 배포, 승인 필요)
- 찜·마이페이지 사진이 대표 사진과 다른 옛 버전 10종(avante·avante-hybrid·tucson·tucson-hybrid·grandeur-hybrid·kona-hybrid·k5-hybrid·k8-hybrid·sorento-hybrid·sportage-hybrid·tasman)
- 넥쏘: DB의 수소 연비를 화면이 안 읽어 연비 빈칸
- 현대 공통행(trim_id 없음)과 트림행 겹침 58행 → 화면 중복 표시 방지
- 캐스퍼 일렉트릭 전용 대표 사진 (결정 4)
- 시작 전 `git status --short`로 다른 세션 변경 확인 → checkpoint 커밋 → 수정 → `npm run build` → 로컬 커밋 → push는 승인 후 (`git pull --rebase origin main` 먼저, market-rent-*.json 직접 커밋 금지)
### 3-4. 마무리
- REN-155 댓글(완료 내역·남은 것), collectors push(승인 시), 인계 문서·메모리 갱신

## 4. 사용자 판단이 필요한 것 (6번)

| # | 항목 | 현재 상태 | 선택지 (권장 ★) |
|---|---|---|---|
| A | 가격표에 없고 웹 견적 화면에만 있는 색 — 렉스턴 실키화이트펄, 티볼리 아이언메탈(+투톤), 코나 투톤 3종·실내 패키지 색, G90 4색, GV70 세레스 블루 매트, 제네시스 레드 투톤 실내, 베뉴 초크화이트 투톤 2 | DB에 없음 | ★웹 견적 화면 기준으로 추가(추가금은 웹 표시값) / 가격표에 나올 때까지 보류 |
| B | 팰리세이드(·HEV) 크리미 화이트 펄 추가금 — 7인승 10만, 9인승 9만 | 10만으로 저장, 9인승 9만은 비고에만 | ★현행 유지(비고로 안내) / 인승별로 행 분리 |
| C | 무쏘 EV·토레스 EVX 밴 세제혜택 후 가격 | 가격표에 값이 없어 빈칸 | ★빈칸 유지(사이트는 값 있을 때만 표시) / 웹에서 따로 확인해 수동 입력 |
| D | 코나·EV5(일반) 투톤 — 가격표에 투톤 색상 행이 없어 '투톤 루프' 옵션으로만 존재 | 옵션 행 유지 | ★옵션으로 유지(결정 2의 예외) / A와 함께 색상 행 만들고 옵션 삭제 |
| E | 베뉴 실내 '블랙'·'블랙 모노톤' 중복 같은 색 | 둘 다 있음 | ★하나로 합침 / 유지 |
| F | EV4 '블랙&화이트' 칩 | 확인 못 함 | 웹 견적 화면 확인 후 결정 |
| G | 테슬라·BYD 옵션 없음 | 옵션 0개 | ★현행 유지(가격표 형식 없음) / 웹 구성기에서 수집 |
| H | 근거 없는 제원 — 렉스턴 써밋, 스타리아 일렉트릭 라운지·리무진 4트림, 테슬라·N 일부 배터리·토크 | 빈칸 | ★빈칸 유지 / 다른 출처로 채움 |
| I | 구동방식 빈칸 23종(대부분 전륜 전용) | 사이트는 대체값 표시 | ★'전륜'으로 채움 / 유지 |
| J | ERP 잔존율 계산이 옛 손입력 vehicles.base_price(51종 불일치) 사용 | 미수정 | ★트림 최저가 기준으로 바꿈(ERP 작업) / 유지 |
| K | 무쏘·무쏘 EV 대표 사진이 같은지 | 미확인 | 캐스퍼 일렉트릭처럼 전용 사진 필요 여부 |

## 5. 작업 방법 (다음 세션용)
- DB 재반영은 브랜드 단위: 백업 → `python3 price_crawler.py --recrawl-brands <hyundai|기아|KGM|제네시스|르노코리아|쉐보레> --from-cache` → option_conflict_fix --apply --monthly → option_span_fill --apply → option_desc_enrich --apply --monthly → config_options_fill --apply → option_media_sync --apply → 백업 대비 검증.
- option_change_log --apply는 파서 교정을 제조사 변경으로 기록하므로 교정 작업 중엔 돌리지 말고 끝에 --baseline만.
- powertrain_refresh --apply는 66차종 전체 교체라 배터리·출력·인승 보강값 유실 위험 → 행 id 단위 PATCH로 대신.
- 파서 수정은 저장된 PDF 전체로 수정 전/후 비교(트림 수·기본가 불변) 후 반영. 도구(임시): /private/tmp/claude-501/-Users-kim-projects-cadam/5ff00df0-678b-4d47-a6c6-736dd35856fe/scratchpad/ 의 snap.py·diff.py·dbdump.py·verify.py·chain.sh
- 백업(~/projects/cadam/backups-manual/): car_data_before_REN155_alignment_20261111.json(전체), car_data_before_{genesis,kia,kgm,renault,hyundai}_reapply_20261111.json, car_data_before_color_fix_20261111.json, vehicle_powertrains_before_co2_fill_20261111.json, vehicle_powertrains_before_genesis_refresh_20261111.json

## 6. 완료 상세 (참고)
- 제네시스: 필수 선택 사양 전 페이지 열 단위 읽기(AWD·디자인 셀렉션·VIP/인승·Black 엔진·MAGMA·GV60 액세서리), g70-sb '2WD(후륜)'→스포츠 패키지 2종, EV 세제혜택 후 가격 3종
- 기아: 쏘렌토·스포티지 가솔린 블랙 에디션, 카니발 듀얼 선루프·BOSE·아웃도어, K8 스마트 커넥트, '스타일*', 사양 글 옵션표 섞임 11트림·EV6 제어문자
- KGM: 로마숫자 뒤로('딥 컨트롤 패키지 Ⅱ'), 티볼리 마이너스 옵션 -36만, 세제혜택 후 5트림
- 르노: 아르카나 파워 테일게이트 95만→80만, 하이브리드 8트림 세제혜택 후 가격
- 현대: 깨진 옵션명 4건, 영업용·구급 옵션 제거, 세제혜택 후 가격 11차종 58트림, 스타리아 일렉트릭 카고 5인승 모던 추가
- CO₂ 37행·K9 도심연비
- 색상: 팰리세이드·베뉴·아이오닉5·EV3-GT·EV6·트레일블레이저 추가금, EV5 다크 오션 블루 0·아이스버그 매트 그린 추가, EV4 모닝 헤이즈, K5 HEV 가솔린 전용색 제거, 액티언 스칼렛 그로브, G70 본드 실버 매트 69만·마칼루 그레이 NCM(유광)/매트 MPE 69만
- 제원: GV80 29행 재구성(하이브리드 13행 신규), GV70 18인치 2행 삭제·무게 수정
- KGM·쉐보레 옵션 설명 123행

## 7. 3차 세션 진행 기록 (2026-11-11 밤 ~23:40)
백업: backups-manual/car_data_before_REN155_decisions_20261111.json(차량 5표), option_media_features_before_REN155_photos_20261111.json

| 항목 | 결과 |
|---|---|
| A·D 웹 전용 색 | ✅ DB 43행 추가(견적 API 표시 추가금). color_parser `WEB_ONLY_COLORS`에 고정 → 월간 수집에도 유지. 코나·코나HEV·코나EV 투톤 6/6/7색(30만 포함)+실내 패키지 3색, EV5 GT-Line 투톤 3색(40만), 베뉴 초크화이트 투톤 2(40만), 렉스턴 실키 화이트 펄(10만·노블레스), 티볼리 아이언 메탈(+투톤 41만·V7), G90 한라산 그린·베르비에 화이트 매트(79만), GV70 세레스 블루 매트(70만), G70·G70SB·G80·GV70 세비야 레드 투톤 실내. 투톤 루프 옵션 8행 삭제(코나2·코나HEV1·코나EV3·EV5 2). 칩·사진·트림 color_config로 연결 완료 |
| E 베뉴 실내 블랙 | ✅ '블랙'(1549) 삭제 → '블랙 모노톤'에 합침(MERGE_COLORS) |
| F EV4 블랙&화이트 | ✅ 기아 견적 화면(GT-Line)에 있음, DB·사진 이미 있음 → 유지(변경 없음) |
| H 제원 | ◑ portal_spec_fills: 아이오닉5N 609PS·740Nm, 아이오닉6N 448kW/609PS·740Nm(카탈로그 기본값, 부스트 770), 아반떼N 휠 19", 렉스턴 써밋 엔진명. ⬜ 못 채움: 써밋 공차중량(KGM 상세 제원 페이지 없어짐, 네이버는 일반 렉스턴 값), 스타리아 일렉트릭 라운지·리무진 4트림(현 가격표 4쪽에 라운지 없음, 견적 API 코드 US36=어린이 통학), 테슬라 배터리(공식 미공개·출처 불일치) |
| I 구동 '전륜' | ✅ 23종 99행 (4WD 옵션·근거 없음 확인) |
| 4 옵션 사진 | ◑ 15개 눈으로 확인 후 수동 연결(제네시스 스포츠·그래파이트 패키지·AWD, 투싼HEV 익스테리어 디자인 I, 무쏘 12.3 내비) → option_media 862→911. 나머지 미연결 156종은 출처 사진 없음/애매(KGM 컴포트Ⅱ 3색, G90 컴포트 I/II 등) |
| 4 르노 설명 | ✅ 3행(아르카나·아르카나 가솔린 카멜 브라운 패키지, 필랑트 시그니처 패키지), 근거 문구 있을 때만 월간 유지 |
| 5 cadam-web | ✅ 로컬 커밋 0b42f69 (찜 사진 카탈로그 기준, 넥쏘 km/kg, 공통행 중복 제거, 캐스퍼EV·무쏘 전용 사진 v3), npm run build 통과·로컬 화면 확인. ⏸ push 승인 대기 |
| K 무쏘/무쏘EV | 같은 파일이었음 → 무쏘(내연) 전용 옆모습(KGM 360 1번) 새로 만듦. 캐스퍼EV는 공식 옆모습 없어 앞 대각선(AX07) |
| J ERP 잔존율 | ✅ 로컬 커밋 65b134b (트림 최저가 기준). ⏸ push·ERP 재시작 승인 대기 |
| 커밋 | collectors 7171072·7164dcb·d696753, cadam-doc 33a14ed (모두 미push) |

남은 질문: 렉스턴 써밋·티볼리 터보에 실키 화이트 펄·아이언 메탈을 넣을지(견적 화면 공유라 근거 약함), 베뉴 썬더 옐로우(운전교습용 전용) 삭제 여부(결정 1 특수 판매형).

## 8. 4차 (2026-11-11 밤, 사용자 지시: 못 한 것 다시·결정 1~3)
백업: backups-manual/car_data_before_REN155_round4_20261111.json, option_media_before_REN155_{wheels,chevrolet,siblings}_20261111.json
- 결정: 렉스턴 써밋 실키 화이트 펄·티볼리 터보 아이언 메탈(+투톤) 추가 / 베뉴 썬더 옐로우 삭제(DROP_COLORS) / G90 베르비에 화이트 매트 80만(가격표 매트 기준) — collectors b9e0563
- 캐스퍼 일렉트릭 옆모습: 현대 카탈로그 PDF '제원' 면 측면 사진(_hcat/casper-ev) → cadam-web dc5da1e
- 스타리아 일렉트릭 라운지·리무진: 별도 가격표 US40/US41(the-new-staria-lounge-electric_price.pdf, …limousine…) 발견 → 4트림 사양 PATCH, 제원 3행 INSERT(id 1001~1003). ⚠️ 월간 수집기는 이 두 PDF를 아직 안 받음(값은 유지되지만 갱신 안 됨)
- 테슬라 배터리 6행: ev.or.kr 보조금 지급대상 차종 / 렉스턴 써밋 공차중량 2,255: 2025.10 취급설명서(4WD 5인승 선택사양 포함, 구조변경 전) — collectors f995759
- 옵션 사진 911→932: 제네시스 휠 9, 쉐보레 견적 화면 2(파일은 cadam-data에 있으나 gitignore), 같은 계열 차 동일 옵션 11 — cadam-doc be09746·66f8bb7·28ade59, collectors 94a39f4. 남은 135종은 출처 사진 없음
- 테슬라 출력·토크는 공식 미공개로 빈칸 유지

## 9. ⏸ 보류 (사장님 결정, 2026-11-12 전달) — 11/21까지
Supabase 무료 플랜 Log Ingestion 0.85/1GB(11/21 초기화). REN-155 일괄 작업이 11/11 하루 약 90MB 사용.
- Supabase 직접 쓰기 일괄 실행 금지(--apply·색상/제원/옵션 일괄·Storage 업로드). dry-run·로컬 커밋·코드 수정은 가능
- cadam-web push 보류 → 11/21 이후 한 번에 (5d86e5d·0b42f69·dc5da1e 대기)
- 앞으로 일괄 쓰기 코드는 trim_spec_parser.patch_grouped(id=in.(...) 60개 묶음, collectors 8e77b8f) 사용
- 남은 일(11/21 이후): 스타리아 라운지·리무진 일렉트릭 가격표 월간 수집기 등록, ERP 65b134b push·재시작, 각 저장소 push

## 10. 로컬 원본 전환 후 정리 (2026-11-12)
- 차량 원본이 Mac 로컬 DB(car 스키마)로 전환됨. 11/11 반영분(스타리아 1001~1003, 썬더 옐로우 삭제, G90 80만, 테슬라 배터리, 써밋 무게, option_media 932) 로컬에 모두 있음 확인
- collectors d8aaf95: car_export가 vehicle_powertrains.hydrogen_eff 내보냄(넥쏘 km/kg). 다음 car_publish 때 powertrains.json에 칸 추가됨
- cadam-web: 로컬 브랜치 alimtalk-quote-button을 origin/main(3720882, JSON 원본) 위로 rebase. 커밋 c956fac·9b94081·7df1442·c9ee2b1 + 다른 세션 eabaf35. 충돌 2곳(car-insight·catalog-specs)은 JSON 경로 유지+hydrogen_eff 추가. 타입 검사 통과(빌드는 Supabase 조회라 생략). 이전 상태: backup/ren155-site-before-rebase-20261112
- ERP 65b134b(잔존율)는 아직 Supabase vehicle_trims(동결본)를 읽음 — 로컬 원본 전환 3단계 때 함께 확인
- 보류(§9) 유지: push·Storage 업로드는 11/21 이후
