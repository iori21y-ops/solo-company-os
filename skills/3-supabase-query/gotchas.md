# 함정 (Gotchas) — Supabase 직접 조회

- Management/service_role 토큰은 RLS 우회 = 최고 권한.
  읽기 가드 없으면 쓰기·삭제도 됨 → SELECT 가드 필수.
- 토큰 하드코딩 절대 금지 (2026-06-18 실제 유출 사고 발생).
  코드에 박으면 git→GitHub로 샌다. 반드시 .env에서, .env는 gitignore.
- .bak·백업 파일에도 토큰 평문 남기지 말 것 (사고 때 .bak에서 또 나옴).
- SELECT 시작만 보면 "SELECT 1; DROP TABLE" 다중문이 뚫림.
  세미콜론으로 쪼개 각 조각을 검사해야 함.
- requests는 이 환경에서 LibreSSL 경고 → curl 사용.
