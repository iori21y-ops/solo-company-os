# scripts/

운영 자동화 스크립트 모음.

## server-health-check.sh

서버 상태 자동 점검 스크립트. 매일 07:00 launchd(`com.rentailor.health-check`)가 실행.

**점검 항목 (12개):** 디스크·메모리·claude-broker·OpenClaw·n8n Docker·Ollama·Tailscale·포트(5678/9722)·LaunchAgent·broker 에러로그·rentailor.co.kr·Docker 디스크·대용량 로그

**동작:**
- 문제 감지 → Claude sonnet이 분석 보고서 생성 → 관리팀장 봇으로 디스코드 전송
- 각 항목에 복구 명령어 포함 (`→ 복구: ...`)
- 자동 복구 가능 명령어는 `~/projects/_meta/logs/health-check-fixes.sh`에 별도 저장
- 디스코드에서 `복구 승인` 입력 시 fixes.sh 자동 실행
- Claude/봇 실패 시 디스코드 웹훅으로 fallback

**관련 파일:**
- `~/Library/LaunchAgents/com.rentailor.health-check.plist` — launchd 등록
- `~/projects/_meta/logs/health-check.log` — 실행 이력
- `~/projects/_meta/logs/health-check-fixes.sh` — 복구 명령어 목록

---

핸드오프 시스템 자동화 스크립트.

## new-handoff.sh

신규 핸드오프 영역을 생성합니다.

```bash
./scripts/new-handoff.sh <category> <name> [description]
```

| 인자 | 설명 | 예시 |
|------|------|------|
| category | 영역 분류 | `projects` / `meta` / `scratch` |
| name | 영역 이름 (영문·하이픈) | `rentailor` / `agents` |
| description | 영역 설명 (선택, 따옴표) | `"랜테일러 프로젝트"` |

**생성되는 파일:**
- `handoff/{category}/{name}/{DATE}-init.md` — 초기 핸드오프 내용
- `handoff/{category}/{name}/handoff-latest.md` — init 복사본 (공개)
- (category=projects인 경우만) `DECISIONS.md`, `current-state.md` — 로컬 전용

**실행 예시:**
```bash
# 일회성 작업
./scripts/new-handoff.sh scratch test-area "스크립트 테스트"

# 새 프로젝트
./scripts/new-handoff.sh projects myproject "새 사업 프로젝트"

# 메타 작업
./scripts/new-handoff.sh meta ops "운영 에이전트 정비"
```

실행 후 `refresh-readme.sh`가 자동 호출되어 루트 README가 갱신됩니다.

---

## refresh-readme.sh

루트 `README.md`의 "🚀 활성 핸드오프 영역" 섹션을 자동 갱신합니다.

```bash
./scripts/refresh-readme.sh
```

`handoff/` 디렉토리를 스캔해 `handoff-latest.md`가 있는 모든 영역을 표로 생성합니다.
`AUTO-GENERATED:START/END active_areas` 마커 사이 내용을 덮어씁니다.
마커가 없으면 README 맨 끝에 섹션을 추가합니다.

## save-handoff.sh

세션 마무리 시 핸드오프를 영역에 박제하고 push.

사용법:
  ./scripts/save-handoff.sh <태그|경로> [세션명]

태그 매핑:
  - 랜테일러 → projects/rentailor
  - 에이전트 → meta/agents
  - 일회성 → scratch/general

또는 풀 경로: projects/rentailor, meta/agents, scratch/general

본문 전달 (두 가지 방식):

방식 1 - 환경변수:
  HANDOFF_CONTENT="내용" ./scripts/save-handoff.sh 에이전트 "세션명"

방식 2 - 파이프:
  echo "내용" | ./scripts/save-handoff.sh 랜테일러 "세션명"

자동 처리:
  - 날짜 파일 생성: handoff/{area}/YYYY-MM-DD-{session}.md
  - handoff-latest.md 갱신 (날짜 파일 복사)
  - 금지 패턴 자가 점검 (IP, Supabase, 키 등)
  - README 자동 갱신 (refresh-readme.sh 호출)
  - git add/commit/push
  - raw URL 검증 (200 확인)

Claude 자연어 패턴:
  "세션 마무리 에이전트"
  "세션 마무리 meta/agents"

Claude가 자동:
  1. 영역 인지 (페치한 area 프론트매터 또는 메모리)
  2. 오늘 세션 내용 요약
  3. save-handoff.sh 호출 명령 생성
  4. 클코에 던지면 끝
