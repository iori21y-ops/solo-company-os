# ~/projects 폴더 규칙 (v1, 2026-11-10)

> 목적: 블로그 엔진·데이터 창고·수집 인프라를 사업(브랜드)별로 같은 모양으로 두고, 새 형식(브랜드)을 폴더 하나 추가로 붙인다.
> 근거 조사: 2026-11-10 전체 인벤토리 (`~/projects/cadam/docs/strategy/blog-engine-and-folders-20261110.md` §1).

## 1. 최상위 구조

```
~/projects/
  _meta/          공통 운영 OS: 규칙(governance/), 핸드오프(handoff/), 감사·점검 스크립트
  _shared/        공용 파이썬 라이브러리 패키지 `solo_common` (discord, notify, claude 호출, ego_browser, polite, config 로더)
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
- 수집기 출력 규칙은 `cadam-n8n/COLLECTOR_CONVENTION.md`(→ 이전 후 `<사업>/collectors/CONVENTION.md`)를 따른다: 숫자 → PostgreSQL, 맥락 → second-brain, 사이트 노출값 → Supabase.
- 다른 프로젝트 폴더를 `sys.path`에 넣지 않는다. 공용 코드는 `_shared/solo_common`, 다른 사업의 데이터가 필요하면 그 데이터의 공개 경로(DB 스키마·내보내기 파일)로 읽는다.

## 3. 블로그 엔진

```
blog-engine/
  engine/         공통 단계: 대기열·상태, 자료 묶음, 초안, 검수, 재작성, 숫자 검증, 금액 표기, 중복 검사, 보류 스위치, 알림
  publishers/     발행처: wordpress/, naver/ (cadam-naver 발행 서버를 여기로), youtube/(추후)
  graphics/       표·그래프·카드 (blog_graphics), 폰트
  brands/
    <브랜드>/
      brand.yaml  채널(디스코드 채널·발행처·블로그 ID·카테고리), 일정, 보류 플래그 위치, 사용할 데이터 연결
      rules/      글쓰기·검수·재작성 규칙(브랜드 원본), kind/ 글 유형별 규칙, CHANGELOG.md
      sources.py  그 사업의 데이터 읽기(어댑터) — 데이터는 사업 프로젝트에 그대로 두고 읽기만
      topics.py   (선택) 글감 찾기
      outbox/     초안·결과 (git 제외)
  run.py          `run.py <brand> <command>` 하나로 실행
```
- 새 형식 추가 = `brands/<새이름>/` 폴더 하나(brand.yaml + rules/ + sources.py).
- 브랜드마다 디스코드 채널을 하나 정해 그 브랜드의 글쓰기 알림은 전부 거기로(렌테일러 #콘텐츠기획, 해외파 #축구블로그).

## 4. 데이터 창고

- 숫자 데이터: 로컬 PostgreSQL 하나(현재 DB `cadam`). 사업마다 schema를 나눈다(`warehouse`=렌테일러, `data`=KOSIS, 해외파는 추후 `football`).
- 백업은 한 경로로: `_meta` 백업 스크립트 → `<사업>/backups/postgres/` 30일 + iCloud 사본. 겹치는 백업은 없앤다.
- SQLite 등 옛 저장소는 이전이 확인되면 `_archive`로.

## 5. 정리·삭제 규칙

1. 다시 만들 수 있는 것(빌드 캐시 `.next`, `__pycache__`, 병합된 git worktree)은 바로 지운다. worktree는 `git worktree remove`.
2. 그 밖의 파일·폴더는 바로 지우지 않고 `_archive/<날짜>/원래경로`로 옮긴다 → launchd·코드 참조가 없는지 확인 → 7일 뒤 목록을 사장님께 보여 주고 비운다.
3. 실행 중인 launchd가 가리키는 파일을 옮기면 같은 작업에서 plist도 고치고 다시 불러온다.
4. `rm -rf` 금지(전역 규칙). 비밀 파일(`.env`, `~/.cadam-secrets`)은 옮기지 않는다.
5. 이동 전 해당 저장소에서 `checkpoint:` 커밋, 다른 세션의 미커밋 변경이 있으면 멈추고 보고.
