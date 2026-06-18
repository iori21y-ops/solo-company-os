---
name: new-migration
description: erp_tasks 등 DB 스키마 변경(컬럼 추가 등) 마이그레이션 SQL 작성. "마이그레이션", "컬럼 추가", "스키마 변경", "ALTER TABLE" 트리거.
type: script
---

## 목적
DB 스키마를 안전하게 바꾸는 마이그레이션 SQL을 003 패턴 그대로 찍어낸다.
정답이 003_*.sql로 고정돼 있으므로 script. 흔들리면 안 됨.

## 언제 쓰나 (트리거)
- erp_tasks 등에 컬럼 추가/변경이 필요할 때
- "마이그레이션 만들어줘", "스키마 바꿔줘"

## 사용법 (절대 순서)
1. migrations/ 의 최신 번호 확인 → 다음 번호로 파일명: 00N_동사_대상.sql (snake_case)
   예: 004_add_skill_id.sql
2. 003_*.sql 을 참조 템플릿으로 복사해서 시작
3. 헤더 주석 4항목 필수 작성: 목적 / 승인 / 실행 / 안전성
4. SQL 본문 규칙:
   - BEGIN; ... COMMIT; 트랜잭션으로 감싼다
   - 멱등: ADD COLUMN IF NOT EXISTS (재실행 안전)
   - 비파괴: 기존 컬럼·제약 안 건드림. 기존 행은 NULL 허용 또는 DEFAULT
   - snake_case 준수
5. 파일만 만든다. 여기서 끝.

## 🚫 절대 금지 (가드)
- 클로드코드가 DB에 직접 적용 금지. SQL 파일 생성까지만.
- 실제 적용은 사람이: 백업 → Supabase SQL Editor 수동 실행.
- broker처럼 자동 적용 경로 없음 (.env.local 키는 있으나 쓰지 않는다).
- 최대 가능 작업 = dry-run (SQL 문법·영향범위 설명 출력)까지.

## Gotchas (함정)
→ gotchas.md 참고

## 스크립트
→ scripts/ (현재 없음. 작성은 파일 생성이라 코드 불요)
