---
name: bak-cleanup
description: 작업 중 쌓인 .bak 백업 파일을 안전하게 정리한다. 지우지 않고 ~/projects/_archive/<날짜>/로 옮기고 MOVED.txt에 기록한다(7일 뒤 사장님 확인 후 비움). ~/projects 안 지정 폴더만, 원본이 있는 것만, 미리보기(dry-run) 먼저.
type: script
---

# .bak 백업 파일 안전 정리 (옮기기 방식)

> 2026-11-15 개정: `rm` 삭제 → 보관함 이동. 근거 `~/projects/_meta/governance/FOLDER_RULES.md` §5 (지울 것은 `_archive/<날짜>/원래경로`로 옮기고 `MOVED.txt`에 한 줄 → 7일 뒤 목록을 사장님께 보여 주고 비운다).

## 목적
.bak.YYYYMMDD 류 백업이 작업 폴더에 쌓이면 정리한다. 이 스킬은 **아무것도 지우지 않는다** — 보관함으로 옮길 뿐이라 언제든 되돌릴 수 있다.

## 언제 쓰나
- 작업 후 특정 프로젝트 폴더에 .bak이 쌓였을 때
- 안정화가 끝나 백업을 치워도 되는 시점

## 순서 (꼭 이 순서로)
1. 그 폴더가 속한 저장소에서 `git status` → 다른 세션의 미커밋 변경이 있으면 멈추고 보고. 없으면 `checkpoint:` 커밋.
2. 미리보기: `scripts/cleanup.sh <대상폴더>` → 옮길 목록과 보존 이유를 사장님께 보여 준다.
3. 실제 이동: `scripts/cleanup.sh <대상폴더> --run` (보관함 이동은 되돌릴 수 있어 "하고 보고" 대상).
4. 보고: 옮긴 개수, `~/projects/_archive/<날짜>/MOVED.txt` 위치, 비울 날(7일 뒤).
5. **비우기(진짜 삭제)는 이 스킬이 하지 않는다.** 7일 뒤 목록을 보여 주고 사장님 승인 후 따로 한다.

- 예: `cleanup.sh ~/projects/content-engine/publishers/naver`
- 되돌리기: `MOVED.txt`의 "어디서" 경로로 다시 옮긴다.

## 자동으로 보존하는 것 (옮기지 않음)
- `~/projects` 바깥, `~/projects` 전체, `_archive` 안 → 거부
- 원본 파일이 없는 .bak (유일본일 수 있음)
- 비밀 가능 파일: `.env`·`config.json`·쿠키·secret·token·credential 이름이 들어간 백업 (FOLDER_RULES §5-4: 옮기지도 복사하지도 않는다)
- second-brain·`.cadam-secrets`·`.claude`·`.git`·`node_modules` 안
- 데이터 창고의 의도된 백업 `_data/<사업>/backups/`
- git이 추적 중인 .bak (커밋과 함께 따로 정리)
- 예약 작업(`~/Library/LaunchAgents`)이 경로를 가리키는 파일
- 보관함에 같은 이름이 이미 있는 파일

## 검증
`scripts/run-test.sh` — 임시 폴더에서만 16개 항목 확인(실제 폴더 무손상). 스크립트를 고치면 반드시 다시 돌린다.
