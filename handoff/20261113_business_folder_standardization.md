# 사업 폴더 표준화 — 11-13 작업 요약·남은 일·폴더 구조

작성: 2026-11-13 (사장님 요청). 상세 기록: `cadam/docs/strategy/engines-and-business-folders-20261113.md` §8, 확인표: `cadam/docs/strategy/data-management-20261112.md` §6, 남은 위반 목록: `_meta/governance/COMPAT_LIST.md`.

## 1. 한 일 (11-13 하루)

### 큰 구조 — 3층
- **데이터 창고** `~/projects/_data/<사업>/<collected|media|work|backups>/` — 모든 사업의 수집 원본·사진·작업 파일·백업을 코드 폴더에서 빼서 한곳에. 창고 git(비공개 GitHub) + 매일 iCloud 백업.
- **엔진** — `content-engine/`(글·영상, 옛 blog-engine), `web-engine/`(사이트 cadam-web·ERP cadam-erp).
- **사업 폴더** — 그 사업의 데이터를 만드는 코드만. 폴더 이름은 그대로(cadam=렌테일러, import-lease=임포리스, football-blog=해외파, keyword-scan=공용 키워드).

### 사업 폴더 안 표준 틀
`collect/`(수집) · `process/`(가공·DB 반영) · `check/`(점검·감시) · `facts/`(엔진에 숫자를 주는 창구) · `db/` · `knowledge/` · `services/`(상시 서버) · `ops/`(운영 스크립트·예약 작업 사본) · `docs/` · `logs/`
- 렌테일러: 옛 `collectors/`·`cadam-pipeline/`을 표준 틀로 나누고 git 하나로 합침. 남은 예외 `core/`(실행 설정·렌테일러 공용 모듈)
- 임포리스: 옛 `crawler/` 한 폴더(57개 파일)를 collect/process/check/shared로 나눔
- 해외파: `football/{collect,process,check,content}` + facts/ops
- 키워드: collect/ + ops/

### 오후~저녁 정리
- 실행 기록 `cadam/core/logs` → `cadam/logs` (예약 작업 30개 재등록, ERP 재배포)
- 공용 도구 정리: 별칭 파일 8개·수집기 도구 사본 3개 없앰 → `_shared/solo_common` 직접 사용. 새 공용 모듈 `naver_api`(네이버 검색), `linear_alert`(Linear 알림)
- 임포리스가 렌테일러 코드를 빌려 쓰던 것: 알림(#데이터 그대로)·Linear·렌트 비교 계산(렌테일러 데이터 창구로) 정리
- 렌테일러 자동 쇼츠 알림: 텔레그램 → 디스코드 #콘텐츠기획
- gwp1(뉴스 수집·점수) 예약 작업 **끔** (사장님 지시)

### 하다가 찾아서 고친 고장
- 다나와 월간 동기화가 옮긴 옛 폴더를 찾아 실패할 상태 → 고침
- 임포리스 월간 가격 갱신(테슬라)이 없앤 옛 폴더를 가리켜 실패할 상태 → 고침
- GPU 이미지 동기화 스크립트가 창고 폴더만 비우고 멈출 상태 → 원본 확인 후 비우게
- 성장 지표의 쇼츠 로그인 예비 경로 → 새 위치로

## 2. 남은 일

### 확인 (실제 실행을 봐야 함)
| 언제 | 무엇 | 보는 곳 |
|---|---|---|
| 11-13 18:07 | 렌테일러 자동 쇼츠(보류 중) | `_data/rentailor/work/datashorts/run.log` 마지막 줄 `paused — nothing done` |
| 11-13 18:10 | 트렌드 수집 (naver_api 첫 실행) | `cadam/logs/trend_collector.log` |
| 11-14 02:00 | 약관 감시 | `cadam/collect/terms_crawler/monitor.log` |
| 11-14 03:40 | 임포리스 수집 (폴더 나눈 뒤 첫 실행) | `import-lease/logs/collector.log` |
| 11-14 09:00 | 키워드 수집 | `_data/shared/collected/keyword-scan/logs/<날짜>.log` |
| 11-14 11:10 | 데이터 건강 점검 (기록 위치 바뀐 뒤) | `cadam/logs/data_health.log` |
전체 목록은 확인표 §6.

### 미뤄 둔 것 (기한 있음)
- 유튜브 업로드 코드 3벌 하나로 · 해외파 영상이 football-blog 코드 직접 사용 — **쇼츠 과정 재설계 때**
- 임포리스가 렌테일러 DB 읽을 때 렌테일러 `.env` 사용 — 사장님 비밀 키 정리 때 (12-15)
- 임포리스 수동 이미지 도구가 사이트 스크립트 사용 — 쓸 때
- 폴더 이름 바꾸기(cadam→rentailor 등) — 사장님 제외
- gwp1 다시 켤지 — 네이버 다이제스트·WP 글쓰기 재개 때 결정

### 다른 세션 몫 (참고)
- ERP 저장소에 다른 세션 커밋 2개 push 안 됨(디스코드 토큰 경로)
- `_data/scripts/md_to_phone_html.py` — 창고에 코드가 있음(규칙상 코드 폴더로 옮겨야 함, 다른 세션이 만든 것)

## 3. 지금 폴더 구조 (괄호 = 스크립트 수)

```
~/projects/
├── _archive/
├── _data/
├── _meta/
├── _shared/
├── cadam/
├── content-engine/
├── football-blog/
├── import-lease/
├── keyword-scan/
└── web-engine/

### cadam (렌테일러)
cadam/
├── check/
│   ├── analysis/  (2 scripts)
│   ├── growth/  (8 scripts)
│   └── monitoring/  (11 scripts)
├── collect/
│   ├── api-hub/  (1 scripts)
│   ├── claude_bridge/  (1 scripts)
│   ├── crawl/  (5 scripts)
│   ├── delivery/  (1 scripts)
│   ├── docs/
│   ├── extract/  (1 scripts)
│   ├── kosis/  (4 scripts)
│   ├── lib/  (4 scripts)
│   ├── price_crawler/  (101 scripts)
│   ├── promo/  (2 scripts)
│   ├── recall/  (1 scripts)
│   ├── rentailor/
│   ├── supabase/  (1 scripts)
│   ├── telegram_clipper/  (5 scripts)
│   ├── terms_crawler/  (18 scripts)
│   ├── trends/  (1 scripts)
│   └── vehicle_images/  (9 scripts)
├── core/
│   ├── config/
│   ├── docs/
│   └── scripts/  (3 scripts)
├── db/
│   └── migrations/
├── docs/
│   ├── archive/
│   ├── kakao-login-review/
│   ├── notes/
│   ├── partnerships/
│   ├── reports/
│   ├── screenshots/
│   ├── seo/
│   ├── strategy/
│   └── wf-vi/
├── facts/  (7 scripts)
├── knowledge/
│   ├── eval/
│   ├── models/
│   └── prompt-changes/
├── logs/
│   ├── agents/
│   └── api-usage/
├── ops/  (8 scripts)
│   ├── launchd/
│   └── oneoff/  (1 scripts)
├── process/
│   ├── curation/  (2 scripts)
│   ├── maintenance/  (8 scripts)
│   └── sync/  (3 scripts)
└── services/
    ├── gpu-agent/
    ├── infographic/  (1 scripts)
    └── pipeline-api/  (1 scripts)

### import-lease (임포리스)
import-lease/
├── check/  (3 scripts)
├── collect/  (32 scripts)
├── db/
├── docs/
├── logs/
├── ops/  (1 scripts)
├── process/  (19 scripts)
├── public/
└── shared/  (3 scripts)

### football-blog (해외파)
football-blog/
├── docs/
│   └── revamp/
├── facts/  (1 scripts)
├── football/  (4 scripts)
│   ├── check/  (4 scripts)
│   ├── collect/  (23 scripts)
│   ├── content/  (10 scripts)
│   └── process/  (8 scripts)
├── logs/
└── ops/  (1 scripts)
    ├── launchd/
    └── tools/  (8 scripts)

### keyword-scan (키워드)
keyword-scan/
├── collect/  (13 scripts)
└── ops/  (1 scripts)

### content-engine (글·영상 엔진)
content-engine/
├── brands/  (1 scripts)
│   ├── football/  (14 scripts)
│   └── rentailor/  (37 scripts)
├── engine/  (11 scripts)
├── graphics/  (3 scripts)
├── launchd/
├── logs/
├── publishers/  (1 scripts)
│   ├── naver/
│   └── wordpress/  (2 scripts)
├── rules/
│   ├── common/
│   └── sites/
└── video/
    ├── brand/
    ├── docs/
    ├── pipeline/  (13 scripts)
    └── tools/  (5 scripts)

### web-engine (사이트·ERP)
web-engine/
├── _wt-car-publish/
├── _wt-rent-publish/
├── cadam-erp/
└── cadam-web/

### _data (데이터 창고)
_data/
├── football/
│   ├── backups/
│   ├── media/
│   └── work/
├── imporis/
│   ├── backups/
│   ├── collected/
│   ├── media/
│   └── work/
├── rentailor/
│   ├── backups/
│   ├── collected/
│   ├── media/
│   └── work/
├── scripts/  (1 scripts)
└── shared/
    ├── backups/
    ├── collected/
    └── work/

### _shared
_shared/
├── phone-view/
├── phone-view-server/  (1 scripts)
└── solo_common/  (15 scripts)
```
