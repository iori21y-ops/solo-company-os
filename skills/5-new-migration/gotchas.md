# new-migration gotchas

- 2026-11-15: 옛 버전의 "003_*.sql 패턴"은 기준 파일이 어디인지 불분명했다(현재 003은 `import-lease/db/migrations/003_lease_source_view.sql`뿐). 기준 파일 하나 대신 "그 폴더의 이름 방식 + 머리말 틀"로 바꿈.
- 옛 버전은 "사람이 SQL Editor로 적용"이라 했지만, 2026-11 규칙은 "승인 받은 쓰기만 MCP·Management API"다. 적용은 이 스킬 밖의 승인 단계.
- `find.sh`는 파일 이름순으로 최근을 고른다. 번호형(`006_`)과 날짜형(`2026…`)이 섞이면 날짜형이 위로 온다 — 같은 표가 두 사업 DB에 다 있으면 결과 목록을 보고 판단한다.
- `_wt-*`(작업 사본)·`_archive` 폴더는 찾기·만들기 대상에서 뺀다.
- 롤백에 DROP TABLE을 쓰지 않는다(security.md §5.1 금지). 기존 마이그레이션도 롤백 DROP은 주석 처리돼 있다(`cadam/docs/schema.md` 참고).
