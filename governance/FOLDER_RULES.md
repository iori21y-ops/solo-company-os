# ~/projects 폴더 규칙 (v1.1, 2026-11-10)

> 목적: 블로그 엔진·데이터 창고·수집 인프라를 사업(브랜드)별로 같은 모양으로 두고, 새 형식(브랜드)을 폴더 하나 추가로 붙인다.
> 근거 조사: 2026-11-10 전체 인벤토리 (`~/projects/cadam/docs/strategy/blog-engine-and-folders-20261110.md` §1).

## 1. 최상위 구조

```
~/projects/
  _meta/          공통 운영 OS: 규칙(governance/), 핸드오프(handoff/), 감사·점검 스크립트
  _shared/        공용 파이썬 라이브러리 패키지 `solo_common` (discord, notify, claude 호출, ego_browser, polite, config 로더,
                  창고 DB 접속, LLM 호출, 기사 본문 추출 — 두 프로젝트 이상이 쓰는 도구만)
  _archive/       삭제 대기 보관함: _archive/<YYYY-MM-DD>/<원래 경로> — 7일간 문제 없으면 비운다
  blog-engine/    글쓰기 엔진 (모든 브랜드 공용, §3)
  <사업>/          사업별 서비스 + 그 사업의 수집기·데이터 (cadam = 렌테일러, football-blog = 해외파 리포트, …)
  my-shorts/ 등   영상·기타 독립 프로젝트
```

## 2. 사업(브랜드) 프로젝트 안의 모양

```
<사업>/
  collectors/     그 사업의 수집기 전부 (한 곳). 수집기 하나 = 폴더 하나 또는 파일 하나
  data/           원본·캐시·내보내기 (git 제외). 숫자 데이터의 원본은 로컬 PostgreSQL(§4)
  services/ 또는 각 앱 폴더   웹·ERP·API 서버 (cadam-web, cadam-erp …는 지금 이름 유지)
  launchd/        이 사업의 launchd plist 원본 사본 (설치본과 동일하게 유지)
  docs/           운영 문서
```
- 수집기 출력 규칙은 `cadam/collectors/COLLECTOR_CONVENTION.md`를 따른다: 숫자 → PostgreSQL, 맥락 → second-brain, 사이트 노출값 → Supabase.
- 다른 프로젝트 폴더를 `sys.path`에 넣지 않는다(다른 프로젝트의 코드를 import하지 않는다). 공용 코드는 `_shared/solo_common`만.
- 다른 사업의 데이터가 필요하면 아래 **세 가지 길**로만 읽는다:
  1. DB (Supabase, 로컬 PostgreSQL schema)
  2. 내보내기 파일 (그 사업의 `data/` 아래 JSON 등 — 읽기만)
  3. **데이터 창구 명령** — 그 사업이 내놓는 명령 하나를 실행해 JSON 답만 받는다. 계산 규칙은 그 사업 코드에 그대로 둔다.
     예: `cadam-pipeline/scripts/content/facts_cli.py <함수이름>` ← `blog-engine/brands/rentailor/sources.py`가 부름.
     창구의 함수 이름·반환 모양을 바꾸면 부르는 쪽도 같이 고친다. 진행 기록은 stderr, 답(JSON)은 stdout 한 줄.
- 실시간 외부 조회(API 호출)처럼 "데이터"가 아닌 작은 도우미 코드가 양쪽에 필요하면 `solo_common`으로 옮긴다. 당장 못 옮겨 사본을 만들면 §6 목록에 적는다.

## 3. 블로그 엔진

```
blog-engine/
  engine/         공통 단계: 대기열·상태, 자료 묶음, 초안, 검수, 재작성, 숫자 검증, 금액 표기, 중복 검사, 보류 스위치, 알림
  rules/          공통 규칙(common/)과 발행처별 형식 규칙(sites/<발행처>/) — 블로그별 규칙은 brands/<브랜드>/rules/ (지도: rules/README.md)
  publishers/     발행처: wordpress/, naver/ (cadam-naver 발행 서버를 여기로), youtube/(추후)
  graphics/       표·그래프·카드 (blog_graphics), 설명 애니메이션 (explainer) — 실제 파일이 여기 있다(2026-11-10 `_shared`에서 되돌림)
  brands/
    <브랜드>/
      brand.yaml  채널(디스코드 채널·발행처·블로그 ID·카테고리), 일정, 보류 플래그 위치, 사용할 데이터 연결
      rules/      글쓰기·검수·재작성 규칙(브랜드 원본), kind/ 글 유형별 규칙, <발행처>/ 그 브랜드×발행처 전용 규칙, CHANGELOG.md
      sources.py  그 사업의 데이터 읽기(어댑터) — 데이터는 사업 프로젝트에 그대로 두고 읽기만
      topics.py   (선택) 글감 찾기
      outbox/     글쓰기 작업 파일: 글감 후보, 초안·승인 상태, 사진 작업 (git 제외). 사업이 수집한 데이터는 여기 두지 않는다
  logs/           엔진 작업의 실행 기록 (git 제외)
  launchd/        엔진 작업의 launchd plist 원본 사본
  run.py          `run.py <brand> <command>` 하나로 실행
```
- 새 형식 추가 = `brands/<새이름>/` 폴더 하나(brand.yaml + rules/ + sources.py). 새 발행처 = `rules/sites/<발행처>/` + `publishers/<발행처>/`.
- 규칙 층: 두 블로그 이상이 글자 그대로 같이 쓰는 규칙만 공통·발행처 층으로 올린다. 층은 자동으로 합치지 않고, 지시문을 만드는 코드가 고른다.
- 브랜드마다 디스코드 채널을 하나 정해 그 브랜드의 글쓰기 알림은 전부 거기로(렌테일러 #콘텐츠기획, 해외파 #축구블로그).
- **무엇이 엔진 것이고 무엇이 사업 것인가**: 글쓰기만 쓰는 파일(후보·초안·발행 상태·사진 작업)은 엔진 `outbox/`. 홈페이지·ERP·영상·수집기도 쓰는 자료(가격·시세·경기 기록·사진 원본·조회수 수집분)는 사업 프로젝트 `data/`에 그대로 두고 §2의 세 가지 길로 읽는다.
- 실행 기록(로그)은 그 작업의 코드가 있는 프로젝트의 `logs/`에 둔다. 5MB 넘으면 주간 정리(`cadam/cleanup_logs.sh`)가 줄인다.
- 공용 코드와 엔진 코드는 launchd가 쓰는 `/usr/bin/python3`(3.9)에서 돌아야 한다.

## 4. 데이터 창고

> 데이터 한 건을 어떻게 적고(카테고리·이용 등급·쓰는 곳), 언제 늘리고 줄이는지는 `DATA_RULES.md`(v0.1 초안). 현황 화면은 `_meta/dashboard`.

- 숫자 데이터: 로컬 PostgreSQL 하나(현재 DB `cadam`). 사업마다 schema를 나눈다(`warehouse`=렌테일러, `data`=KOSIS, 해외파는 추후 `football`).
- 백업은 한 경로로: `_meta` 백업 스크립트 → `<사업>/backups/postgres/` 30일 + iCloud 사본. 겹치는 백업은 없앤다.
- SQLite 등 옛 저장소는 이전이 확인되면 `_archive`로.

## 5. 정리·삭제 규칙

1. 다시 만들 수 있는 것(빌드 캐시 `.next`, `__pycache__`, 병합된 git worktree)은 바로 지운다. worktree는 `git worktree remove`.
2. 그 밖의 파일·폴더는 바로 지우지 않고 `_archive/<날짜>/원래경로`로 옮긴다 → launchd·코드 참조가 없는지 확인 → 7일 뒤 목록을 사장님께 보여 주고 비운다.
3. 실행 중인 launchd가 가리키는 파일을 옮기면 같은 작업에서 plist도 고치고 다시 불러온다.
4. `rm -rf` 금지(전역 규칙). 비밀 파일(`.env`, `~/.cadam-secrets`, 발행 서버 `config.json`·쿠키)은 **옮기지도 복사하지도 않는다. 제자리에서 읽기만** 한다(읽는 쪽 코드에 그 경로를 적는다). 값은 화면·로그·git에 남기지 않는다.
5. 이동 전 해당 저장소에서 `checkpoint:` 커밋, 다른 세션의 미커밋 변경이 있으면 멈추고 보고.

## 6. 임시 연결·사본·남은 위반

- 이사할 때 남기는 임시 연결(폴더 링크, 옛 자리의 호환 파일), 어쩔 수 없이 만든 코드 사본, 아직 규칙을 어기는 곳은 전부 `~/projects/_meta/governance/COMPAT_LIST.md`에 적는다. 적지 않은 임시 연결은 만들지 않는다.
- 줄마다 **없애는 조건과 기한**을 적는다. 기한이 된 줄은 쓰는 곳 수를 다시 세어 0이면 없애고(삭제는 사장님 확인 후), 남아 있으면 기한을 새로 정한다.
- 2주마다 목록을 점검한다(다음 점검일은 목록 맨 위).

