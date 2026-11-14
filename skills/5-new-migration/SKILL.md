---
name: new-migration
description: DB 스키마 변경(컬럼 추가·인덱스·정책 등) 마이그레이션 SQL 파일과 롤백 파일을 만든다. 파일만 만들고 DB에는 적용하지 않는다(적용은 사장님 승인 후 별도). "마이그레이션", "컬럼 추가", "스키마 변경", "ALTER TABLE" 트리거.
type: script
---

# 마이그레이션 SQL 만들기

> 2026-11-15 개정: 옛 "003 패턴"(기준 파일 불명확)·broker 언급 삭제. 폴더는 "그 표를 마지막으로 다룬 곳"을 따르고, 롤백 파일·백업·승인 칸을 필수로.
> 근거: `governance/SAFETY_RULES.md` §2(백업 없는 스키마 변경 금지)·§3(DB 쓰기 절차)·§6(백업 위치), `cadam/docs/security.md` §5.1(ALTER = 승인 후, DROP TABLE·TRUNCATE 금지).

## 목적
스키마 변경을 매번 같은 모양으로, 되돌릴 수 있게 만든다. **이 스킬은 파일만 만든다. DB에 적용하지 않는다.**

## 순서
1. **어느 폴더?** `scripts/find.sh <표 이름>` → 그 표를 다룬 마이그레이션을 최근 기록 순으로 보여 주고 따를 폴더를 알려 준다.
   - **렌테일러 DB는 항상 `~/projects/cadam/db` (2026-11-15 사장님 결정)** — 옛 기록이 다른 폴더에 있어도 새 파일은 여기.
   - 같은 이름 표가 여러 사업 DB에 있으면(예: `brands` = 임포리스·렌테일러) 폴더를 정하지 않고 경고한다 → 어느 사업 DB인지 확인 후 진행.
   - "(없음)"이면 처음 다루는 표 → 렌테일러면 `cadam/db`, 그 밖은 **사장님께 어느 폴더인지 묻는다** (추측 금지).
2. **커밋 준비:** 그 폴더의 저장소에서 `git status` → 다른 세션의 미커밋 변경이 있으면 멈추고 보고(내 파일만 커밋할 것). 그다음 `checkpoint:` 커밋.
3. **파일 만들기:** `scripts/new.sh <그 폴더> <동사_대상>` → 폴더의 이름 방식(번호 `007_` / 날짜 `YYYYMMDD_` / 14자리 타임스탬프)에 맞춰 본파일 + `_rollback.sql`을 만든다.
4. **채우기:** 머리말의 `<...>` 칸(목적·대상 DB·승인·백업·롤백·적용)과 SQL 본문.
   - `begin; … commit;`으로 감싼다.
   - 멱등: `add column if not exists`, `create index if not exists`, `drop policy if exists` 후 `create policy`.
   - 비파괴: 기존 컬럼·데이터를 지우거나 바꾸지 않는다. 새 컬럼은 NULL 허용 또는 DEFAULT.
   - 롤백 파일의 DROP TABLE·TRUNCATE는 금지 → 주석으로만. DROP COLUMN은 데이터 삭제 경고를 붙인다.
5. **보여 주기:** 사장님께 SQL, 영향받는 표·행 수, 롤백 방법을 보여 주고, 만든 두 파일만 커밋한다. 여기서 이 스킬은 끝.

## 적용은 별도 단계 (이 스킬 밖, 승인 필요)
SAFETY_RULES §3 순서: 지금 상태 조회 → 바뀌는 점 요약 → 백업(`~/projects/_data/<사업>/backups/manual/`에 바뀌는 표 내보내기) → **사장님 승인** → MCP 또는 Management API로 적용 → 다시 조회해서 확인 → 머리말 "승인·백업" 칸 채우고 커밋.
- 운영 DB에 `psql` 직접 접속 금지. Supabase SQL Editor 수동 실행은 사장님이 원할 때만.

## 마이그레이션 폴더 (2026-11-15 확인)
| 폴더 | 이름 방식 | 무엇 | 비고 |
|---|---|---|---|
| `~/projects/cadam/db` (폴더 바로 아래) | `YYYYMMDD_` + `_rollback` | **렌테일러 DB(운영 Supabase 포함) — 새 마이그레이션은 여기 한 곳** | 2026-11-15 사장님 결정. 덤프(`db_backup_*`)·이름 없는 create 스크립트는 마이그레이션으로 치지 않음 |
| `~/projects/import-lease/db/migrations` | `00N_` | 임포리스 | 11-14까지 쓰임 |
| `~/projects/cadam/db/migrations` · `web-engine/cadam-web/supabase/migrations` · `cadam/collect/supabase/migrations` · `collect/terms_crawler/migrations` · `web-engine/cadam-erp/migrations` | 제각각 | 렌테일러 옛 폴더 | **새 파일 금지**(`new.sh`가 거부). 옛 파일은 문서·코드가 경로로 가리켜서 옮기지 않음 |

기록: `~/projects/cadam/CLAUDE.md` 폴더 지도 `db/` 줄.

## 검증
`scripts/run-test.sh` — 임시 폴더에서 26개 확인(DB·실제 폴더 무손상). 스크립트를 고치면 다시 돌린다.
