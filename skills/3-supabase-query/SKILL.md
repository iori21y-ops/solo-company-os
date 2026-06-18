---
name: supabase-query
description: Supabase DB를 읽기 전용으로 직접 조회. "테이블 조회", "컬럼 확인", "스키마 확인", "SELECT" 트리거.
type: script
---

## 목적
Supabase를 SELECT로 직접 조회한다. 대시보드 API로 안 되는 임의 테이블·스키마 확인용.
쓰기는 절대 안 됨. 정답이 query.py 가드로 고정됨 → script.

## 언제 쓰나 (트리거)
- "erp_tasks에 X 컬럼 있나?", "이 테이블 행 수는?"
- 마이그레이션 전후 스키마 확인 (5-new-migration과 연계)

## 사용법
python3 scripts/query.py "SELECT * FROM erp_tasks LIMIT 5"
- SELECT/WITH만 허용. 쓰기 키워드·다중문은 자동 거부.
- 결과 50행 상한.

## 🚫 절대 금지
- 토큰 하드코딩 금지. cadam-n8n/.env에서만 읽는다 (gitignore 필수).
- 쓰기/스키마 변경은 이 스킬로 하지 않는다 → 5-new-migration.
- requests 쓰지 말 것 (LibreSSL 경고) → curl.

## Gotchas
→ gotchas.md

## 스크립트
→ scripts/query.py (SELECT 가드 내장), scripts/run-test.sh (가드 검증)
