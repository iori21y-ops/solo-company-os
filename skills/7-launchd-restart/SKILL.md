---
name: launchd-restart
description: 맥미니 launchd 서비스(ERP·네이버 발행 서버·예약 작업)를 안전하게 재시작하거나 지금 한 번 실행한다. 재시작은 사장님 승인 대상 — 먼저 미리보기(dry-run)로 종류와 명령을 보여 주고 승인 후 실행. "재시작", "서비스 멈춤", "kickstart" 트리거.
type: script
---

# launchd 서비스 재시작

> 2026-11-15 개정: 옛 서비스(md-dashboard·claude-broker) 예시 삭제, 정확한 라벨만 허용, 상시 서비스와 예약형 작업 구분, 승인 규칙 반영.
> 근거: 전역 `~/.claude/CLAUDE.md`·`governance/SAFETY_RULES.md` §1(서비스 재시작 = 승인 필요), `cadam/docs/security.md` §5.2(kickstart = 승인 후, plist 삭제 금지).

## 목적
명령을 기억으로 다시 짜지 않고 검증된 `scripts/restart.sh`를 쓴다. 라벨 오타·비슷한 이름(`com.cadam.naver` vs `naver-perf-*`)·예약 작업을 실수로 돌리는 사고를 막는다.

## 꼭 알아야 할 것: 두 종류
| 종류 | 예 | `kickstart -k`가 하는 일 |
|---|---|---|
| 상시 서비스 (plist에 `KeepAlive`) | `com.cadam.erp`, `com.cadam.naver`(발행 서버), `com.cadam.car-db-postgrest` | 끄고 다시 켬. 하는 일은 같음 |
| 예약형 작업 (정해진 시각·N초마다·파일 감시) | `com.cadam.wp-writer`(10분마다 글쓰기), 수집기, 리포트 | **지금 한 번 실행** — 글 발행·알림·DB 쓰기가 실제로 일어남 |

예약형은 보통 재시작이 필요 없다. 코드를 고치면 다음 예약 시각에 새 코드로 돈다.

## 순서
1. 미리보기: `scripts/restart.sh <정확한 라벨>` → 종류·설정 파일·PID·실행될 명령이 나온다. 아무것도 바꾸지 않는다.
2. 그 결과를 사장님께 보여 주고 **승인을 받는다** (재시작은 승인 필요 목록).
3. 승인 후
   - 상시 서비스: `scripts/restart.sh <라벨> --run`
   - 예약형을 지금 한 번 돌려야 할 때: `scripts/restart.sh <라벨> --run-scheduled-now` (`--run`은 거부됨)
4. 실행 후 출력의 `state`·`pid`·`last exit code`로 확인해 보고한다.

## 하지 않는 것
- ERP 코드 변경 반영 → 재시작이 아니라 `~/projects/web-engine/cadam-erp/scripts/deploy.sh` (빌드 포함, 승인 필요).
- `unload`·`load`·`bootout`·plist 고치기·`.disabled` 이름 바꾸기 → 이 스킬 범위 밖. 예약 작업 끄기·실행 시각 바꾸기는 승인 대상이고, plist를 고칠 때는 SAFETY_RULES §6 백업 규칙을 따른다.
- 권한 600 plist(민감정보 가능)는 `chmod`하지 않는다.
- `com.apple.*` 등 우리 것이 아닌 라벨은 스크립트가 거부한다.

## 참고
- 라벨 목록: `launchctl list | grep -E 'com\.(cadam|blogengine|kim|rentailor|solo)|secondbrain'`
- PID가 없거나 마지막 종료 코드가 음수(-15 등)여도 예약형이면 정상일 수 있다.

## 검증
`scripts/run-test.sh` — 미리보기와 거부 경로만 11개 확인(실제 재시작 0회). 스크립트를 고치면 다시 돌린다.
