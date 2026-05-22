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

<!-- SECTION:START name=mobile_index -->
## 📱 모바일 새 세션용 인덱스

모바일에서 새 Claude 세션을 시작할 때, 핸드오프에 박힌 인덱스 URL이 이 README입니다.
새 세션은 이 인덱스를 보고 필요한 파일만 추가 페치하세요.

### 핵심 진입점 (필요한 것만 페치)

| 영역 | 인덱스 (1차) | 핵심 파일 (2차) |
|------|------------|---------------|
| **에이전트 정의** | [agents/README.md](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/README.md) | [agents/_shared/boundary-rules.md](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/boundary-rules.md) — 경계 규칙 모음 |
| **핸드오프 시스템** | [handoff/README.md](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/handoff/README.md) | [handoff/templates/self-contained.md](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/handoff/templates/self-contained.md) — 자급자족 템플릿 |
| **위임 프레임워크** | (예정) | — |

### 사용법

1. 모바일 새 세션 시작 시 핸드오프 붙여넣기 (자급자족 맥락 포함)
2. 더 깊은 맥락 필요시 위 표의 1차 인덱스 페치
3. 1차 인덱스에서 특정 파일 위치 파악 후 2차 페치

### 페치 명령 예시 (새 세션에 줄 말)

**예시 1 — 가벼운 확인용:**
```
agents/README.md를 읽어서 9개 에이전트가 뭔지 정리해줘:
https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/README.md
```

**예시 2 — 작업 시작용:**
```
agents/_shared/boundary-rules.md를 페치해서 지난 작업의 경계 규칙 패턴을 파악해줘:
https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/boundary-rules.md
```
<!-- SECTION:END name=mobile_index -->
