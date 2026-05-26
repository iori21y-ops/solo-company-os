---
area: meta/agents
date: 2026-05-26
session: 핸드오프 시스템 v2.2 - 본문 박기 방식 전환
---
# 완료
1. web_fetch 캐시 문제 진단: GitHub raw URL이 클로드 web_fetch에서 5분 캐시에 걸려 옛 버전 반환되는 사고 확인
2. 1차 우회 시도 실패: ?t=timestamp 쿼리스트링이 web_fetch에서 정규화돼 무효
3. 방안 전환: URL 박기 → 본문 직접 박기 (web_fetch 자체를 안 함)
4. save-handoff.sh 수정: pbcopy 대상이 URL → handoff-latest.md 본문+지시문
5. iOS 단축어 "이어받기" 3분기 재구성 완료
6. 3분기 전체 실측 검증: 렌테일러/에이전트/일회성 정상
7. 메모리 #23 v2.1→v2.2 갱신

# 현황
PC/모바일 양쪽 캐시 문제 영구 해결. 클로드는 web_fetch 없이 본문 즉시 읽음.

# 다음
파트5 학습루프 설계 → 파트4 디스코드봇 → 클코 실제 구현

# 메모
한 세션=한 파트 원칙. 다음 세션은 파트5 단독.
