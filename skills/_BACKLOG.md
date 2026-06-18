# 스킬 라이브러리 백로그 (9분류 점검표)

원칙: 폴더(빈 그릇)는 먼저 만든다. 내용은 그 작업을 실제로 하며 채운다.
type 기준: 정답이 하나로 정해지나? YES→script / NO→rule

| # | 스킬 | type | 상태 | 비고 |
|---|------|------|------|------|
| 1 | broker-api | rule | ✅완료 | 본문+포인터 |
| 2 | verify-distribute | script ⭐ | ✅완료 | 라이브 실증(부모71 PASS) |
| 3 | supabase-query | script | ⬜미작성 | 키 출처 불명, 보류 |
| 4 | handoff-writer | rule | ✅완료 | — |
| 5 | new-migration | script | ⬜미작성 | DB 스키마 변경, 신중 |
| 6 | code-before-acting | rule | ✅완료 | — |
| 7 | launchd-restart | script | ✅완료 | 테스트 PASS |
| 8 | databot-alert-debug | script ⭐ | ✅완료 | SKILL 런북+diagnose.sh, 라이브 실증 |
| 9 | bak-cleanup | script | ✅완료 | 테스트 PASS |

⭐ = Anthropic 문서가 효과 최대로 꼽은 2개(검증·런북). 둘 다 script형.
