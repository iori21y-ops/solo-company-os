# 핸드오프 — agents CLAUDE.md §7 박제 완료

area: meta/agents
date: 2026-05-28
session: 파트11 §7 에이전트 간 인사이트 참조 본문 박제

## 완료 (이번 세션, push 완료)
- 212c2a6 — §7 본문 박제(915→957줄, +42) + _shared/scout-territories.md 신규 생성
- 2 files changed, 90 insertions(+), 7 deletions(-)

## 박제된 §7 핵심
- 7.2 원칙: B의 원본(raw/cycles/insights) 직접 안 읽고 synthesis/playbook만 참조
- 7.3 예외: content가 정찰 위탁(B-J) 받을 때만 의뢰 에이전트 raw/cycles 한정 읽기. 결과는 content 본인 J 사이클에 박제, 의뢰자는 인용/링크만
- 7.4 sales conversion-report(월1회). Q4: 추천=가산/비추천=감점/언급없음=중립/부재·30일경과=중립
- 7.5 자율발굴 영역은 _shared/scout-territories.md 단일진실, 각 SKILL.md는 발췌참조
- 7.7 옵션 가/나/다 폐기, 라만 생존

## scout-territories.md 핵심
- 9개 에이전트 자율발굴 영역 매트릭스
- content만 second-brain 정찰 단독, 나머지는 content에 B-J 위탁
- 자기 영역=각자 raw/cycles/_config

## 남은 placeholder 1개
| § | 줄 | 제목 | 합의메모 |
|---|---|------|---------|
| §3.4~§3.10 | 270 | 페이지 타입별 양식 8개 | 타입 목록만 확정 (데스크탑 권장) |

## §7 후속 작업 (이번 미반영, 별도 작업)
- boundary-rules.md: marketing↔sales 경계 (노출까지/클릭이후)
- sales SKILL.md: synthesis-conversion-report-YYYYMM 정기산출물 추가 (월1회)

## 미해결
- §9 중복 9.2 (placeholder 아님, 본문 9.2가 두 번 들어감). 작은 정리 작업
- agents/.gitignore에 *.bak.* 미반영, 백업파일 untracked 노출
  (CLAUDE.md.bak.before-section7, CLAUDE.md.bak.20260527_171710)

## 다음 세션 작업 후보
1. §3.4~§3.10 페이지 타입별 양식 (데스크탑 권장, 추가 합의 필요)
2. §7 후속 — boundary-rules.md / sales SKILL.md
3. §9 중복 9.2 정리 + .gitignore *.bak.* 추가

## 절대 원칙 (유지)
1. 클코 자체 진행 금지 — 명령어 문서로만
2. CLAUDE.md 통째 덮어쓰기 금지, str_replace로만
3. 한 세션 = 한 파트
4. 합의메모 없으면 박제 안 함

## 운영 패턴 (검증됨)
- str_replace: Python + 백업 + count 검증 + 'PYEOF'
- old 블록 1번 안 나오면 즉시 중단 → 원인 진단 → 재시도
- §7 의문 해소법: conversation_search로 "파트5 학습루프" 원문 대조 (옵션 라/B-J/scout-territories 출처 전부 거기 있음)
