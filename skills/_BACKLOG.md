# 스킬 라이브러리 백로그 (9분류 점검표)

원칙: 폴더(빈 그릇)는 먼저 만든다. 내용은 그 작업을 실제로 하며 채운다.
type 기준: 정답이 하나로 정해지나? YES→script / NO→rule

| # | 스킬 | type | 상태 | 비고 |
|---|------|------|------|------|
| 1 | broker-api | rule | 🪦은퇴 | 2026-11-13 결재 에이전트 체계 폐지로 은퇴(커밋 `ef3ca5b`). 필요하면 `git show 9f4bf0b:skills/1-broker-api/SKILL.md`로 복원 |
| 2 | verify-distribute | script ⭐ | 🪦은퇴 | 같은 날 은퇴(카드 배분 검증 — 체계 폐지). 복원 `git show 9f4bf0b:skills/2-verify-distribute/SKILL.md` |
| 3 | supabase-query | script | ✅완료 | 가드 7/7 PASS, 실제 쓰기 0 |
| 4 | handoff-writer | rule | ✅완료 | — |
| 5 | new-migration | script | ✅완료 | 2026-11-15 개정 — 아래 연결 상태표 |
| 6 | code-before-acting | rule | ✅완료 | — |
| 7 | launchd-restart | script | ✅완료 | 2026-11-15 개정 — 아래 연결 상태표 |
| 8 | databot-alert-debug | script ⭐ | 🪦은퇴 | 같은 날 은퇴(데이터봇 알림 — 체계 폐지). 복원 `git show 9f4bf0b:skills/8-databot-alert-debug/SKILL.md` |
| 9 | bak-cleanup | script | ✅완료 | 2026-11-15 개정 — 아래 연결 상태표 |
| 10 | field-note | rule | ✅완료 | 2026-11-15 신설 — 사장님 현장 메모 → raw/ 원문 보관 → 위키 '현장 설명' 칸, 확정 사실은 확인 후. 스크립트는 `~/second-brain/scripts/field_note.py`(save·suggest·pending) 바로가기 |

⭐ = Anthropic 문서가 효과 최대로 꼽은 2개(검증·런북). 둘 다 script형.

## Claude Code 연결 상태 (2026-11-15 점검)
연결 = `~/.claude/skills/<이름>` → `~/projects/_meta/skills/<번호-이름>` 바로가기(심볼릭 링크). 모든 세션에서 자동으로 쓰인다. 끊으려면 그 바로가기 하나만 지운다(원본은 그대로).

| 스킬 | 연결 | 이유 |
|---|---|---|
| supabase-query | ✅ 연결 | 읽기 전용 가드 + Management API(규칙 허용 경로). `.env` 경로 문구 갱신 |
| handoff-writer | ✅ 연결 | "인수인계 작성해줘" 명시 지시 때만 작동 |
| code-before-acting | ✅ 연결 | 추측 금지 4단계. 옛 예시(broker) 문구 갱신 |
| bak-cleanup | ✅ 연결 | 2026-11-15 개정: `rm` → `_archive/<날짜>/` 이동 + `MOVED.txt`, `~/projects` 안만, 비밀 가능 백업·데이터 창고 백업·git 추적·launchd 참조 보존. 테스트 16/16 PASS |
| launchd-restart | ✅ 연결 | 2026-11-15 개정: 정확한 라벨만, 상시 서비스(`--run`)와 예약형(`--run-scheduled-now`, 지금 한 번 실행) 구분, 승인 후에만 실행. 테스트 11/11 PASS(재시작 0회) |
| new-migration | ✅ 연결 | 2026-11-15 개정: `find.sh`(그 표를 마지막으로 다룬 폴더) + `new.sh`(본파일+롤백, 승인·백업 칸). DB 적용 안 함. 테스트 26/26 PASS. 렌테일러 DB는 `cadam/db` 한 곳(2026-11-15 사장님 결정), 같은 이름 표가 여러 사업 DB에 있으면 묻기 |
| field-note | ✅ 연결 | 2026-11-15 신설. "현장메모:" 트리거, 밤 인제스트는 second-brain CLAUDE.md §4.1.7로 같은 절차 |
| broker-api · verify-distribute · databot-alert-debug | 🪦 은퇴 | 2026-11-13 결재 에이전트 체계 폐지로 은퇴(커밋 `ef3ca5b`). 디스크에 없음, git 이력(`9f4bf0b`)에만 남음 |
