# Solo Company Operating OS

솔로 운영자가 AI 에이전트와 협업하여 온라인 비즈니스 법인을 운영하기 위한 메타 시스템.

## 구조

| 디렉토리 | 역할 | 상태 |
|---------|------|------|
| `agents/` | 9개 직무별 에이전트 정의 (marketing, content, data, sales, cs, ops, finance, legal, strategy) | 진행중 (3/9 정의) |
| `handoff/` | 세션 간 핸드오프 시스템 (모바일 ↔ 맥미니) | 운영중 |

## 왜 공개인가

- 모바일 새 세션이 web_fetch로 직접 페치 가능 (인증 불필요)
- 다른 솔로 운영자가 참고 가능
- 민감한 사업 정보는 `agents-private/` (gitignore)에 분리

## 운영 원칙

- 한 세션 = 한 작업 파트
- 모든 결정은 섹션 마커 기반 str_replace로 박제
- 핸드오프는 자급자족 (페치 없이도 새 세션 시작 가능)
