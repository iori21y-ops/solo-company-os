# 위임 금지 목록 (Blacklist)

> 로컬 AI·n8n 자동화에 **절대 위임하지 않는** 작업 목록.
> 자동화 코드, n8n 노드, AI 에이전트 모두 이 목록에 해당하는 작업을 실행해서는 안 된다.

## DB 파괴

- `DROP TABLE` / `TRUNCATE` 실행
- `WHERE` 절 없는 `DELETE FROM` / `UPDATE`
- 운영 DB 스키마 변경 (`ALTER TABLE`, `CREATE TABLE`, `DROP COLUMN` 등)
- Supabase RLS 정책 `CREATE` / `ALTER` / `DROP`

## 고객·리드 데이터

- `consultations` 테이블 `DELETE` / `UPDATE`
- `leads` 테이블 `DELETE` / `UPDATE`
- `users` 테이블 `DELETE` / `UPDATE` / 개인정보 외부 전송

## 파일·환경

- `.env`, `.env.local`, API 키, 토큰, 비밀번호를 외부로 전송하거나 로그에 출력
- `rm -rf` 또는 `rm -r` 실행
- 운영 서버 재부팅·종료 명령

## 외부 실거래

- 결제·리드 처리 외부 API 실거래 호출 (테스트 엔드포인트 제외)
- 실 사용자에게 발송되는 이메일·SMS 발송 (알림 전용 텔레그램 제외)
