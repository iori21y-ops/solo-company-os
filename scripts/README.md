# scripts/

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
