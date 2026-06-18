---
name: launchd-restart
description: 맥미니 launchd 서비스(대시보드·broker 등)를 안전하게 재시작한다. 서비스가 멈췄거나 코드 변경 후 반영이 필요할 때 이 스킬을 쓴다.
type: script
---

# launchd 서비스 재시작

## 목적
launchd로 도는 서비스를 재시작할 때 매번 명령을 기억으로 재구성하지 말고, 검증된 scripts/restart.sh를 실행한다. 라벨 오타·잘못된 도메인으로 엉뚱한 서비스를 건드리는 사고를 막는다.

## 언제 쓰나
- 서비스가 죽었거나 응답이 없을 때
- 코드/설정 변경 후 프로덕션 빌드를 다시 띄워야 할 때 (대시보드 등)
- plist를 바꾼 뒤 재로드가 필요할 때

## 사용법
scripts/restart.sh <라벨> [--run]
- 기본은 dry-run: 무엇을 할지 출력만 하고 실제 재시작 안 함.
- 실제 재시작은 --run 플래그를 붙인다.
- 라벨 예: com.cadam.md-dashboard, com.rentailor.claude-broker

검증된 핵심 패턴:
- 재시작: `launchctl kickstart -k gui/$(id -u)/<라벨>`  (-k = 죽이고 다시)
- 확인: `launchctl list | grep <라벨>` 로 새 PID 확인

## Gotchas
- 라벨에 두 접두어가 공존한다: com.cadam.* (인프라/크롤러/백업) 와 com.rentailor.* (에이전트 운영). 재시작 전 정확한 라벨을 launchctl list로 확인할 것.
- com.cadam.md-dashboard.plist는 심볼릭 링크(→ ~/projects/cadam/md-dashboard/launchd/). plist를 고칠 일이 있으면 링크 실체를 고쳐야 한다.
- 대시보드는 프로덕션 빌드다. 코드 변경 반영은 재시작만으로 안 되고 npm run build 후 kickstart 해야 한다. SKILL.md만 바꾼 거면 build 불필요.
- 일부 plist는 권한 600(본인만, 민감정보 포함 가능). 함부로 chmod 하지 말 것.
- PID가 음수(-15 등)면 마지막 실행이 시그널 종료/특수 상태. 스케줄/이벤트 트리거형 서비스는 상시 떠있지 않으니 PID 없음이 정상일 수 있다.

## 검증
scripts/run-test.sh 로 dry-run이 정상 동작하는지 확인한다 (실제 재시작 없이 라벨 존재·명령 조립만 검사).
