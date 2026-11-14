# bak-cleanup gotchas

- 2026-11-15: 옛 버전은 `rm`으로 바로 지웠다 → 삭제 규칙(FOLDER_RULES §5) 위반이라 보관함 이동으로 바꿈. "경로 화이트리스트"는 주석에만 있고 실제 검사가 없었다 → `~/projects` 안만 허용하도록 구현.
- 발행 서버 `content-engine/publishers/naver/config.json.bak.*`는 비밀이 들어 있을 수 있다 → 보호 목록(옮기지도 복사하지도 않음). 지울지는 사장님이 직접 판단.
- macOS 임시 폴더는 `/var/...`와 `/private/var/...` 두 경로로 보인다 → 예약 작업 참조 검사는 `~/projects` 아래 상대 경로로 비교한다.
- 테스트에서 `rm -rf`로 임시 폴더를 지우지 않는다(전역 금지) — 시스템 임시 폴더는 OS가 정리한다.
