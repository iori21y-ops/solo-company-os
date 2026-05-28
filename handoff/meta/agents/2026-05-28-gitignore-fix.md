# 핸드오프 — agents .gitignore 정리 완료
area: meta/agents
date: 2026-05-28
session: 파트12 §9 진단 + .gitignore 백업패턴 추가

## 완료 (이번 세션)
- §9 중복 진단 → 중복 없음 확인. 핸드오프의 "§9 중복 9.2"는 오기재였음 (9.1~9.6 정상)
- .gitignore에 *.bak.* 추가 (기존 *.md.bak-* 하이픈 패턴은 점 형식 백업 미매칭이었음)
- 백업 2개 git check-ignore 무시 확인, 원래 untracked라 rm 불필요
- commit + push 완료

## 다음 세션 작업 후보
1. §7 후속 — boundary-rules.md(marketing↔sales 경계) + sales SKILL.md(월1회 conversion-report 정기산출물). ※새 파일 2개, §7이 이미 이 둘을 전제로 참조 중이라 안 만들면 빈 참조
2. §3.4~§3.10 페이지 타입별 양식 8개 (270줄, 타입목록만 확정 / 양식 본문 추가 합의 필요)

## 절대 원칙
1. 클코 자체 진행 금지 — 명령어 문서로만
2. CLAUDE.md 통째 덮어쓰기 금지, str_replace로만
3. 한 세션 = 한 파트
4. 합의메모 없으면 박제 안 함
