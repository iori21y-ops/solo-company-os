# 자동 작업 전수 조사 · 개선안 (2026-11-13)

> 조사만 했고 아무것도 바꾸지 않았다. 아래 개선안은 사장님 승인 후 진행.
> 표시: **확인됨** = 파일·로그로 직접 확인 / **추정** = 정황상 그럴 가능성이 높지만 확인 못 함 / **미확인** = 볼 수 없었음

## 진행 상황 (2026-11-13 저녁, 사장님과 하나씩 진행 중)
- ① **완료** — audit-agent가 켜진 작업 95개를 자동 감시(주기 2배·강제 종료=실패·바로 알림·ERP 카드 제거). `_meta a5a3d4e`, 첫 실운영 11-14 07:30
- ② **예약됨** — 11-14 14:00 이 세션에서 재등록 82개 첫 실행 점검(목록 `reloaded-20261113.txt`)
- ③ **이미 해결** — 다른 세션이 고침(`cadam c3265dc`, REN-179)
- ④ **정리됨** — 10·11월 로그가 없던 건 고장이 아님(10/27 중단 → 11/5 창고 전용 재개). 진짜 문제는 API 403 → REN-191(사장님 포털 확인). 실패 알림에 API 키가 찍히던 문제는 모든 수집기 공통으로 가림(`cadam 5d9db3a`)
- ⑤ **완료** — gpu-agent·gpu-queue-runner 정지+사용 안 함 표시(11-13 18:10, 승인). 재개 명령은 메모리 project_gpu_server_hold
- ⑥ **완료** — pipeline-api 정지+사용 안 함 표시, ERP `.env.local`의 CRAWLER_BASE_URL 주석 처리 후 ERP 재시작(11-13 18:08, 승인). ERP /login 200, 모니터 경보 0건. 되돌리기: 주석 해제 + `launchctl enable`·`bootstrap` + ERP 재시작
- ⑦ **결정: 그대로 계속**(재개 대비). 11-13 07:09 강제 종료는 fbref-reports(ego 브라우저) 단계에서 외부 신호로 끝남 — 원인 미확인, 2회 연속이면 감사가 알림
- ⑧ **미룸** → REN-192 (호출량 측정 후 통합 검토)
- ⑨ **완료** — 폰 보기 서버 UTF-8(`_shared 4b6024a`, 재시작 확인) · 꺼진 서비스 문서 표기(`cadam 498957f`, `cadam-erp 4733785` — ERP 화면은 다음 배포 때 반영) · 끝난 클라우드 예약 "엔카 W45" 삭제 · 파이썬 경고 → REN-193
- **추가 개선(11-13 밤)**
  - C 완료: audit-agent·헬스체크의 요약용 Claude를 "모든 권한 허용" → "도구 없음"으로 (`_meta 2a5e315`, 실제 호출 시험 OK)
  - B: Ollama는 앱 설정 "Expose Ollama to the network"가 켜져 있어 모든 네트워크에 열림(외부 접속 기록 0건) → **사장님이 앱에서 끄기**. ERP는 Tailscale로 쓰므로 그대로
  - A 완료: claude-bridge(n8n 전용, 11-10 이후 사용 0) 정지+사용 안 함 (`cadam 57755bb` 문서)
  - D 완료: caffeinate에서 화면 꺼짐 막기(-d) 제거(백업 `_data/shared/backups/manual/com.rentailor.caffeinate-welfare.plist_20261113.bak`). 화면은 Amphetamine 세션(151시간째)이 아직 막는 중 → 사장님이 앱에서 끄기
  - E 확인: Supabase 두 프로젝트 모두 pg_cron 없음 = DB 안 예약 작업 0개
- **push 대기(승인 필요)**: `_meta a5a3d4e·2a5e315`, `_shared aaa4e41·4b6024a`, `cadam 5d9db3a·498957f·57755bb`(수집 코드 리포 — 따로 승인), `cadam-erp 4733785`

## 1. 한눈에 보기

| 구분 | 개수 |
|---|---|
| 맥 예약 작업(launchd, 맥이 정해진 시각에 자동 실행하는 작업) 파일 | 102개 |
| └ 실제 켜져 있는 것 | 93개 (상주 서비스 11 · 예약 실행 82) |
| └ 꺼진 것 | 9개 (축구 4 · 옛 대시보드·gwp1·data-freshness·shorts-stats·rag-proxy) |
| 클라우드 예약 작업(Claude) | 2개 (켜짐 1: 내일 08:41 "11-13 알림 수정 결과 확인" 1회 · 꺼짐 1: 엔카 W45, 세션 없어 실패) |
| Vercel 예약 작업 | 1개 (cadam-web `/api/sync-wp`, 매일 06:00 한국시간) |
| GitHub 자동 작업 | 1개 (cadam `sync-notion.yml`, 수동 실행 방식) |
| Supabase 내부 예약(cron) | 0개 (두 프로젝트 모두 pg_cron 없음, 11-13 밤 확인) |
| GPU 서버 자체 예약 작업 | **미확인** (서버 꺼짐) |

**전체 판단:** 수집·알림 작업 대부분은 정상으로 돌고 있다. 문제는 개별 작업보다 **"점검을 점검하는 장치"(audit-agent)가 93개 중 약 12개만 보고 있다**는 점이다. 그래서 작업이 조용히 멈춰도 알림이 안 올 수 있는 사각지대가 넓다.

## 2. 개선안 (중요한 순서)

### ① audit-agent 감시 대상을 자동으로 만들기 — 가장 중요
- **문제(확인됨):** `_meta/scripts/audit-agent.sh`는 감시할 작업 이름을 손으로 적어 둔 목록을 쓴다.
  - 예약 작업 9개 · 상주 서비스 3개 · 로그 4개만 본다 (전체 93개 중).
  - 목록에 이미 꺼진 작업 2개가 남아 있다: `gwp1-pipeline`(꺼짐), `api-hub.ev-chargers`(disabled 폴더로 이동).
  - 상주 서비스 중 `car-db-postgrest`·`car-db-proxy`(차량 DB)·`erp-tunnel`(ERP 외부 연결)·`phone-view`·`claude-bridge`가 빠져 있다. 이것들이 죽어도 알림이 없다.
  - 종료 코드 -15·143(강제 종료됨)을 "성공"으로 친다. 축구 data 작업이 -15로 끝나고 로그가 중간에 끊겼는데도 정상으로 보인다.
- **개선안:** 감시 목록을 손으로 적지 말고 `~/Library/LaunchAgents`의 plist(작업 설정 파일)에서 매일 자동으로 읽는다. 작업마다 "주기의 1.5배가 넘도록 실제 로그가 안 바뀌면 경고", 상주 서비스는 "프로세스 없으면 경고". 오늘 조사에 쓴 목록 스크립트를 그대로 발전시키면 된다.
  - 새 점검 작업을 추가로 만들지 않는다. 데이터 신선도는 이미 data-health(235개 점검)가 맡고 있으니, audit-agent는 **작업이 돌았는지**만 본다.
  - 자체 로그를 따로 쓰는 작업(키워드 스캔·second-brain 인제스트 등)은 "진짜 로그 위치"를 표에 한 번 적어 둔다.
- **승인:** 코드 수정·커밋은 승인 없이 가능하다. 다만 매일 알림 내용이 바뀌므로 먼저 보고한다.
- **되돌리기:** `git revert`.

### ② 오늘 경로가 바뀐 작업 약 60개의 "첫 실행" 확인
- **사실(확인됨):** 오늘 13:27~14:35 폴더 이동 때 plist 약 60개가 새 경로로 다시 등록됐다. 그래서 아직 한 번도 새 경로로 실행되지 않았다(실행 횟수 0). 고장은 아니다.
- **위험(추정):** 스크립트 안에 옛 경로가 남아 있으면 내일 아침부터 하나씩 실패할 수 있다.
- **개선안:** 내일(11-14) 오후, 다시 등록된 작업마다 "등록 뒤 로그가 새로 써졌는지 + 오류(Traceback) 없는지"를 한 번에 확인한다. 내일 08:41 예약된 클라우드 확인 작업은 RSS·다나와·GPU 알림만 보므로 이것은 따로 필요하다. 원하시면 1회성 확인 예약을 걸어 둔다(승인 없이 가능).

### ③ data-health의 "iCloud 파일 권한 오류"
- **문제(확인됨):** data-health의 "콘텐츠 규칙 전제" 점검이 `~/second-brain/scripts/scrape_encar.py`를 읽다가 `Operation not permitted`로 실패한다. `~/second-brain`은 iCloud 폴더로 연결돼 있는데, 맥이 예약 작업에는 iCloud 폴더 접근을 막는다.
- 엔카 크롤러 자체는 `~/second-brain-git` 사본으로 돌고 있어 정상이다(오늘 04:28 수집 확인).
- **개선안:** 이 점검이 iCloud 원본 대신 `~/second-brain-git` 사본을 읽게 바꾼다. 메모리 기록상 코드 원본은 iCloud이고 git 사본은 밤마다 덮어쓴다. 그래서 읽기 전용 점검에는 사본이 맞다.
- **승인:** 코드 수정만 해당한다(승인 불필요, 보고).

### ④ 정비업체(repair-shops) 수집이 10월·11월에 안 돈 흔적
- **사실(확인됨):** 매월 1일 09:30 작업인데, 로그는 9/1에서 멈춰 있다. 그날 기록은 "전체 0건인데 ✅ 완료"였다(가짜 성공). 10/1·11/1에는 로그가 아예 없다. 다만 창고 테이블에는 34,071행이 남아 있다(옛 데이터).
- **원인:** 미확인. 그 사이 plist가 빠져 있었을 수도 있다(추정).
- **개선안:** (a) 0건이면 "실패"로 처리하고 알림을 보내게 수정한다. (b) 12/1 실행을 ②의 확인 대상에 넣는다. (c) 필요하면 지금 수동으로 1회 실행한다. 수동 실행은 외부 API 호출과 창고 쓰기라서 **승인이 필요**하다.

### ⑤ GPU 서버가 꺼져 있는데 GPU 관련 작업 2개가 계속 돎
- **사실(확인됨):** `gpu-queue-runner`가 60초마다 "할 일 없음" 줄을 **파일 2개에 똑같이** 쓴다(각 약 5MB, 하루 약 1,440줄). `gpu-agent`도 계속 켜져 있다. 서버 끄기 명령은 접속 시간 초과로 실패 중이다.
- **개선안:** GPU 보류 기간에는 두 작업을 잠시 멈추거나, 할 일이 없을 때는 로그를 안 쓰게 바꾼다. 같은 내용이 두 파일에 쌓이는 것도 하나로 줄인다.
- **승인:** 작업 멈추기는 실행 중인 서비스 변경이라 **승인 필요**. 되돌리기는 `launchctl bootstrap`.

### ⑥ 쓰는 곳이 안 보이는 상주 서비스 `pipeline-api`
- **사실(확인됨):** 포트 9721에서 **모든 네트워크(같은 와이파이 포함)**에 열려 있다. 로그는 0바이트이고 248시간째 변화가 없다. 코드에서 이 포트를 부르는 곳을 찾았지만 문서에만 나온다.
- **판단(추정):** 안 쓰는 서비스일 가능성이 높다.
- **개선안:** 1주일 동안 접속 기록을 보고, 없으면 끈다. 계속 쓴다면 내 컴퓨터 안(127.0.0.1)에서만 열리게 바꾼다. ERP(3001)·gpu-agent(3199)도 모든 네트워크에 열려 있으니 같은 기준으로 점검한다.
- **승인:** 서비스 끄기·설정 변경 모두 **승인 필요**.

### ⑦ 축구 작업 3개는 보류 중인데 계속 돎 — 의도 확인
- `football-data`(매일)·`football-brain`(주간)·`football-backup`(주간)이 켜져 있다. 글쓰기 4개만 꺼져 있다.
- 데이터를 계속 쌓으려는 의도라면 그대로 둔다. 그렇지 않다면 끈다. **사장님 결정 사항.**
- 참고: `football-data`가 최근 강제 종료(-15)로 끝났고 로그가 중간에 끊겨 있다(확인됨). ①이 적용되면 이런 경우 알림이 온다.

### ⑧ 1~10분마다 도는 작업이 많음 (선택)
- **현황(확인됨):** 60초마다 2개(`discord-clipper`, `shorts-picks`), 5분마다 3개(`monitor`, `linear-approval`, `topic-selector`), 10분마다 7개(`blog-images`, `car-publish-tick`, `growth-approve`, `shorts-scripts`, `terms-approve`, `vehicle-approve`, `wp-writer`)가 돈다.
- 디스코드 반응을 기다리는 작업(`*-approve` 4개)은 지금 쓰는 기능이다. 11-13에 폐지된 결재 체계(claude-broker)와는 다르다.
- **개선안:** 디스코드 반응을 읽는 작업 4개를 하나로 합친다. Supabase나 외부 사이트를 부르는 작업은 무료 한도에 맞춰 주기를 다시 정한다. 급하지 않다.

### ⑨ 정리 거리 (작은 것)
- 대부분의 수집기가 맥 기본 파이썬(3.9)으로 돌아서, 로그마다 SSL 경고 2줄이 반복된다. 진짜 오류가 묻힌다. 파이썬 3.11로 통일하거나 경고를 끈다.
- launchd 로그와 자체 로그가 따로 있는 작업이 많아, 사람이 볼 때 "멈춘 것처럼" 보인다(키워드 스캔·second-brain 인제스트·약관 모니터). ①의 "진짜 로그 위치" 표로 해결한다.
- 꺼진 클라우드 예약 "엔카 W45 수집 확인"은 끝난 일이다. 지우기는 **승인 필요**.
- 약관 모니터 경고("이번 달 성공 표시 없음"): 표시 파일에는 `2026-11`이 들어 있고, 점검 경로도 오늘 고쳐졌다. 내일 11:10 점검에서 저절로 사라질 것으로 보인다(추정).

## 3. 정상으로 확인한 것 (오해 방지)
- 키워드 스캔: 매일 09:01 자체 로그 기록(11-10~11-13) → 정상
- second-brain 인제스트: `cron.log` 오늘 01:04 갱신 → 정상 (`launchd.log`의 권한 오류는 6월 기록)
- 백업·헬스체크: 매일 07:00 "ALL OK" + 하트비트 정상. audit-agent는 매일 07:30 실행(최근 9일 문제 0건 — 다만 ①의 사각지대 때문에 0건으로 나오는 면이 있음)
- data-registry: 결과 파일 오늘 11:38 갱신 → 정상
- 주간·월간 작업(kosis·약관·프로모션·월간 정리·전기차 보조금 등): 로그 나이가 주기 안 → 정상

## 4. 사장님이 정해 주실 것
1. ① audit-agent 개편 진행 여부
2. ⑤ GPU 작업 2개 일시 정지 여부
3. ⑥ pipeline-api: 1주 관찰 후 끄기 여부
4. ⑦ 축구 데이터 수집 계속 여부
5. ④ 정비업체 수동 1회 실행 여부

## 5. 직접 확인하는 방법
- 터미널에서 지금 켜진 작업 보기: `launchctl list | grep -E "cadam|kim|solo|importlease|iori21y|blogengine|rentailor"`
- 오늘 데이터 점검 결과: `open ~/projects/_data/rentailor/work/pipeline/health/latest.md`
- audit-agent 최근 결과: `tail -20 ~/projects/_meta/audit/audit.log`

---
## 부록 A. 전체 자동 작업 목록 (2026-11-13 17시 기준, 맥 launchd)

> 주기: cal=정해진 시각(H시 M분, W요일 0=일, D=일자) · every Ns=N초마다 · keepalive=항상 켜진 서비스. 로그 나이=launchd 로그 파일이 마지막으로 바뀐 뒤 지난 시간(자체 로그를 따로 쓰는 작업은 여기 숫자가 오래돼도 정상일 수 있음).

### 렌테일러(cadam) 수집 (27개)

| 작업 이름 | 주기 | 로그 나이 | 실행 파일 |
|---|---|---|---|
| com.cadam.api-hub.blog-stats | cal:W1,H6,M40 | nofile nofile | run_blog_stats_weekly.sh |
| com.cadam.api-hub.car-sales | cal:H9,M10 | 9h 9h | check_and_fetch_car_sales.py |
| com.cadam.api-hub.gas-stations | cal:H4,M10 | 13h 13h | fetch_gas_stations_warehouse.py |
| com.cadam.api-hub.insurance | cal:H9,M0 | 9h 9h | check_and_fetch_insurance.py |
| com.cadam.api-hub.kidi | cal:D3,H6,M40,M1;D3,H6,M40,M4;D3,H6,M40, | nofile nofile | fetch_model_grade.py |
| com.cadam.api-hub.kncap | cal:D2,H6,M30 | nofile nofile | fetch_kncap.py |
| com.cadam.api-hub.opinet | cal:H10,M0 | 8h 8h | fetch_fuel_prices.py |
| com.cadam.api-hub.repair-shops | cal:D1,H9,M30 | 1760h 1760h | fetch_repair_shops.py |
| com.cadam.api-hub.succession | cal:H7,M40 | 10h 10h | fetch_eacar.py |
| com.cadam.api-hub.used-rent | cal:H7,M20 | 10h 10h | fetch_used_rent.py |
| com.cadam.chazm-monthly | cal:H2,M30 | 15h 15h | run_chazm_monthly.sh |
| com.cadam.crm-sheet-sync | every 1800s | 0h 0h | crm_sheet_sync.py |
| com.cadam.delivery-wait | cal:D2,H13,M17;D5,H13,M17 | nofile nofile | delivery_wait_collect.py |
| com.cadam.encar-crawler-v2 | cal:H3,M0,W2;H3,M0,W5 | 13h 13h | scrape_encar.py --v2 --daily-mode --per-run=3 |
| com.cadam.ev-subsidy | cal:W1,H5,M40 | 108h 108h | run_weekly.sh |
| com.cadam.kb-used-compare | cal:D15,H1,M40;D16,H1,M40;D17,H1,M40;D18 | 194h 194h | kb_used_compare.py |
| com.cadam.kosis | cal:D8,H4,M30 | 133h 133h | kosis_collect.py |
| com.cadam.price-crawler | cal:H2,M0 | 15h 15h | run_monthly.sh |
| com.cadam.promo-collector | cal:D1,H10,M20;D3,H10,M20;D16,H10,M20 | 227h 227h | promo_collector.py |
| com.cadam.terms-approve | every 600s | 27h 27h | terms_approve.py --poll |
| com.cadam.trend-collector | cal:H8,M10;H13,M10;H18,M10 | 5h 5h | trend_collector.py |
| com.cadam.used-prices-prune | cal:W2,H4,M17 | 85h 85h | archive_rows.py --used-prices-keep-weeks 4 --delete |
| com.cadam.vehicle-approve | every 600s | 0h 0h | vehicle_actions.py --poll |
| com.cadam.vehicle-check | cal:H4,M30,W1 | 108h 108h | weekly_vehicle_check.py |
| com.cadam.vehicle-newcar | cal:H11,M13 | 6h 6h | weekly_vehicle_check.py --daily-new |
| com.cadam.warehouse-import | cal:H5,M20 | 12h 12h | warehouse_import.py |
| com.rentailor.recall-collect | cal:H6,M0 | 12h 12h | recall_collect.py |

### 렌테일러 콘텐츠·블로그·쇼츠 (23개)

| 작업 이름 | 주기 | 로그 나이 | 실행 파일 |
|---|---|---|---|
| com.blogengine.dashboard | cal:H8,M40;H13,M40;H20,M40 | 4h 4h | build.py |
| com.blogengine.tracker-monthly | cal:H9,M20 | 8h 8h | run.py rentailor tracker-monthly |
| com.cadam.blog-images | every 600s | 0h 0h | run.py rentailor blog-images |
| com.cadam.car-publish-tick | every 600s | 5h 5h | car_publish.py tick --quiet-min 10 |
| com.cadam.car-publish | cal:H12,M30 | 5h 5h | car_publish.py run --push |
| com.cadam.discord-clipper | every 60s | 2h 2h | discord_clip_poller.py |
| com.cadam.growth-approve | every 600s | 105h 105h | approve.py |
| com.cadam.growth-collect | cal:H7,M10 | 11h 11h | collect.py |
| com.cadam.growth-weekly | cal:W1,H8,M20 | 105h 105h | weekly.py |
| com.cadam.insight-merge | cal:H6,M0 | 12h 12h | insight_merge.py |
| com.cadam.lead-attribution | cal:W1,H9,M50 | 104h 104h | lead_attribution.py |
| com.cadam.monthly-roundup | cal:D5,H9,M10 | 200h 200h | run.py rentailor monthly-roundup |
| com.cadam.naver-perf-collect | cal:H1,M10 | 17h 17h | naver_perf.py --collect |
| com.cadam.profile-fill | cal:H10,M10 | 8h 8h | profile_fill.py |
| com.cadam.shorts-auto | cal:H18,M7 | 24h 24h | run.py --auto |
| com.cadam.shorts-outliers | cal:W0,H20,M37 | 117h 117h | shorts_outliers.py |
| com.cadam.shorts-picks | every 60s | 0h 0h | shorts_scripts.py --picks |
| com.cadam.shorts-scripts | every 600s | 0h 0h | shorts_scripts.py --recent 24 |
| com.cadam.topic-candidates | cal:H7,M0 | 11h 11h | run.py rentailor topic-candidates |
| com.cadam.topic-default | cal:H10,M0 | 8h 8h | run.py rentailor topic-default |
| com.cadam.topic-selector | every 300s | 8h 8h | run.py rentailor topic-select |
| com.cadam.wp-sync | every 3600s | 1h 1h | wp_sync.py |
| com.cadam.wp-writer | every 600s | 0h 0h | run.py rentailor wp-queue |

### 점검·알림·운영 (22개)

| 작업 이름 | 주기 | 로그 나이 | 실행 파일 |
|---|---|---|---|
| com.blogengine.weekly-report | cal:H8,M50,W1 | nofile nofile | weekly_report.py --send |
| com.cadam.audit | cal:H7,M30 | 2938h 2938h | audit-agent.sh |
| com.cadam.backup-cadam | cal:H4,M0 | 6h 6h | backup_cadam.sh |
| com.cadam.cleanup-logs | cal:H3,M30,W0 | 6h 6h | cleanup_logs.sh |
| com.cadam.daily-report | cal:H9,M0 | 9h 9h | daily_report.sh |
| com.cadam.data-health | cal:H11,M10 | 7h 7h | data_health.py |
| com.cadam.data-registry | cal:H9,M20 | 413h 413h | refresh_data_registry.py |
| com.cadam.linear-approval | every 300s | 248h 248h | linear_approval.py |
| com.cadam.linear-diagnose | cal:H9,M0;H11,M0;H13,M0;H15,M0;H17,M0;H1 | 1h 1h | linear_diagnose.py |
| com.cadam.lineup-watch | cal:H9,M40 | 8h 8h | lineup_watch.py |
| com.cadam.log-ingestion-watch | cal:H9,M7 | 9h 9h | log_ingestion_watch.py |
| com.cadam.monitor | every 300s | 0h 1h | collect-tick.sh |
| com.cadam.naver-perf-report | cal:W1,H8,M40 | 17h 17h | naver_perf.py --report --send |
| com.cadam.secrets-drift | cal:H8,M30 | 9h 9h | check-drift.mjs |
| com.cadam.site-refresh-watch | every 3600s | 0h 0h | site_refresh_watch.py |
| com.cadam.sitemap-scan | cal:H6,M0 | 12h 12h | scan-map.js |
| com.cadam.supabase-write-watch | every 21600s | 7h 7h | supabase_write_watch.py |
| com.cadam.terms-monitor | cal:H2,M0 | 304h 16h | terms_monitor.py |
| com.rentailor.health-check | cal:H7,M0 | 3995h 3995h | server-health-check.sh |
| com.solo.doc-audit | cal:W1,H9,M5 | nofile nofile | doc_audit.py --linear |
| com.solo.icloud-backup | cal:H1,M30 | nofile nofile | icloud_backup.sh |
| com.solo.warehouse-git | cal:W0,H4,M20 | nofile nofile | warehouse_git_sync.sh |

### 상주 서비스 (11개)

| 작업 이름 | 주기 | 로그 나이 | 실행 파일 |
|---|---|---|---|
| com.cadam.car-db-postgrest | keepalive | 4h 4h | car_db_postgrest.conf |
| com.cadam.car-db-proxy | keepalive | 0h 0h | car_db_proxy.py |
| com.cadam.claude-bridge | keepalive | 4h 4h | bridge.py |
| com.cadam.erp-tunnel | keepalive | - | ngrok.log |
| com.cadam.erp | keepalive | 0h 51h | next start -p 3001 |
| com.cadam.gpu-agent | keepalive | 5h 269h | server.js |
| com.cadam.gpu-queue-runner | keepalive | 0h 2759h | queue-runner.js |
| com.cadam.naver | keepalive | 9h 9h | server.js |
| com.cadam.pipeline-api | keepalive | 248h 248h | api_server.py |
| com.kim.phone-view | keepalive | 1h 1h | phone-view |
| com.rentailor.caffeinate-welfare | keepalive | 2592h 2592h | caffeinate -d -i -m -s |

### 임포리스 (2개)

| 작업 이름 | 주기 | 로그 나이 | 실행 파일 |
|---|---|---|---|
| com.importlease.collector | cal:H3,M40 | 6h 6h | run_daily.sh |
| com.importlease.encar-used | cal:H5,M30,W2;H5,M30,W5 | 0h 180h | encar_used_prices.py |

### 축구(보류 중) (3개)

| 작업 이름 | 주기 | 로그 나이 | 실행 파일 |
|---|---|---|---|
| com.iori21y.football-backup | cal:W0,H5,M20 | 6h 6h | backup_warehouse.sh |
| com.iori21y.football-brain | cal:W1,H6,M10 | 107h 107h | run.py brain |
| com.iori21y.football-data | cal:H7,M0 | 11h 11h | run.py data |

### 공통·개인 (5개)

| 작업 이름 | 주기 | 로그 나이 | 실행 파일 |
|---|---|---|---|
| com.kim.keyword-scan | cal:H9,M0 | 297h 297h | run_daily.sh |
| com.kim.ollama-env | atload | - | sh -c launchctl setenv OLLAMA_KV_CACHE_TYPE q8_0; launchctl  |
| com.user.secondbrain.ingest | cal:H1,M0 | 3857h 3857h | nightly_ingest.sh |
| com.user.secondbrain.rss | cal:H23,M30 | 18h 18h | collect_all.sh |
| com.user.secondbrain.sync | cal:H0,M0 | 18h 18h | supabase_to_raw.py |

### 꺼짐(disabled/미적재) (9개)

| 작업 이름 | 주기 | 로그 나이 | 실행 파일 |
|---|---|---|---|
| com.blogengine.dashboard-web.disabled | keepalive | 51h 51h | serve.py |
| com.cadam.data-freshness.disabled | cal:H10,M40 | 31h 31h | data_freshness.py |
| com.cadam.gwp1-pipeline.disabled | cal:H2,M0;H16,M30 | 15h 3976h | run_gwp1.sh |
| com.cadam.shorts-stats.disabled | cal:H7,M40 | nofile nofile | shorts.py stats |
| com.iori21y.football-morning | cal:H7,M40 | nofile nofile | run.py football morning |
| com.iori21y.football-poll | every 300s | nofile nofile | run.py football poll |
| com.iori21y.football-review | cal:H11,M30;H16,M30 | 73h 73h | run.py review |
| com.iori21y.football-shorts | cal:H19,M0 | 71h 71h | run.py shorts |
| com.kim.rag-proxy | keepalive | 151h 151h | rag_proxy.py |

합계 102개 (구글·Ego 업데이트·Postgres 등 외부 프로그램 제외)
