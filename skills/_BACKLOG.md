# 스킬 라이브러리 백로그 (9분류 점검표)

원칙: 폴더(빈 그릇)는 먼저 만든다. 내용은 그 작업을 실제로 하며 채운다.
type 기준: 정답이 하나로 정해지나? YES→script / NO→rule

| # | 스킬 | type | 상태 | 비고 |
|---|------|------|------|------|
| 1 | broker-api | rule | ✅완료 | 본문+포인터 |
| 2 | verify-distribute | script ⭐ | ✅완료 | 라이브 실증(부모71 PASS) |
| 3 | supabase-query | script | ✅완료 | 가드 7/7 PASS, 실제 쓰기 0 |
| 4 | handoff-writer | rule | ✅완료 | — |
| 5 | new-migration | script | ✅완료 | 003 패턴, 적용은 사람 수동 |
| 6 | code-before-acting | rule | ✅완료 | — |
| 7 | launchd-restart | script | ✅완료 | 테스트 PASS |
| 8 | databot-alert-debug | script ⭐ | ✅완료 | SKILL 런북+diagnose.sh, 라이브 실증 |
| 9 | bak-cleanup | script | ✅완료 | 테스트 PASS |

⭐ = Anthropic 문서가 효과 최대로 꼽은 2개(검증·런북). 둘 다 script형.

## Claude Code 연결 상태 (2026-11-15 점검)
연결 = `~/.claude/skills/<이름>` → `~/projects/_meta/skills/<번호-이름>` 바로가기(심볼릭 링크). 모든 세션에서 자동으로 쓰인다. 끊으려면 그 바로가기 하나만 지운다(원본은 그대로).

| 스킬 | 연결 | 이유 |
|---|---|---|
| supabase-query | ✅ 연결 | 읽기 전용 가드 + Management API(규칙 허용 경로). `.env` 경로 문구 갱신 |
| handoff-writer | ✅ 연결 | "인수인계 작성해줘" 명시 지시 때만 작동 |
| code-before-acting | ✅ 연결 | 추측 금지 4단계. 옛 예시(broker) 문구 갱신 |
| bak-cleanup | ✅ 연결 | 2026-11-15 개정: `rm` → `_archive/<날짜>/` 이동 + `MOVED.txt`, `~/projects` 안만, 비밀 가능 백업·데이터 창고 백업·git 추적·launchd 참조 보존. 테스트 16/16 PASS |
| launchd-restart | ⏸ 보류 | 예시 라벨(`com.cadam.md-dashboard`·`com.rentailor.claude-broker`)과 plist 경로가 없어짐. 재시작은 승인 대상(SAFETY_RULES §1)이라 문구도 함께 고친 뒤 연결 |
| new-migration | ⏸ 보류 | 기준 "003 패턴" 파일이 어디인지 불분명(현재 `import-lease/db/migrations/003_*`만 있음). 기준 파일·백업 절차 확정 후 연결 |
| broker-api · verify-distribute · databot-alert-debug | — | 표에는 완료로 적혀 있으나 이 폴더에 없음(옛 위치 미확인) |
