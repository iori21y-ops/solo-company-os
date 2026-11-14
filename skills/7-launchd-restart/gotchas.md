# launchd-restart gotchas

- 2026-11-15: 옛 버전은 `launchctl list | grep -q 라벨`로 확인해서 부분 일치도 통과했다(`com.cadam.naver` → `naver-perf-collect`도 맞음). 지금은 `launchctl print gui/<uid>/<라벨>`로 정확히 일치만.
- 예약형 작업에 `kickstart -k`를 쓰면 지금 한 번 실행된다(wp-writer면 글 발행). 그래서 예약형은 `--run`을 거부하고 `--run-scheduled-now`를 따로 둔다.
- 옛 예시 `com.cadam.md-dashboard`·`com.rentailor.claude-broker`는 2026-11 기준 없음.
- 테스트는 미리보기만 한다. 실제 재시작 테스트는 하지 않는다(승인 대상).
