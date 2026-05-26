# 핸드오프 — agents vault 박제 단계 4~7 대기

area: meta/agents
date: 2026-05-26
session: 파트5 학습루프 + vault 박제 (단계 1~3 + cycle 양식 + push 완료)

## 완료
로컬 커밋 9개, origin/main에 push 완료:
- .gitignore 백업 패턴 추가
- save-handoff.sh v2.2 본문 박기
- rentailor 핸드오프 박제
- agents vault 디렉토리 골격 158개 (2b2cdb6)
- agents Obsidian vault 인식 설정 (61c51b1)
- CLAUDE.md 본문 박제
- 앞 세션 핸드오프 박제
- cycle 양식 3종 박제 (1732eac)
- 핸드오프 갱신 (8aec8a7)

## 박제 완료된 핵심 자산
- agents/CLAUDE.md (444줄, 합의 섹션 + 미완성 헤더 11개)
- agents/_shared/templates/cycle-marketing.md (75줄)
- agents/_shared/templates/cycle-content.md (80줄)
- agents/_shared/templates/cycle-data.md (150줄)
- vault 디렉토리 골격 233개
- Obsidian vault 인식 설정

## 중요: 앞 세션 사고 사실 (단계 4 시작 시 주의)

agents/README.md는 박제 작업 이전부터 존재하는 정본 인덱스 (8개 커밋 이력).
앞 세션에서 클코가 단계 4 자체 진행 시도하다가 사고 발생:
- README 자체 발견 → 자체 판단으로 vault_assets 섹션 추가 시도
- 존재하지 않는 파일(counters/cadam.md, refs/cadam/_index.md)을 인덱스에 박음
- 사용자가 발견 → 롤백 (git checkout)
- 클코가 임의로 만들었던 untracked 두 파일도 삭제

현재 git status clean.

## 절대 원칙 (위반 시 사고)

1. 클코 자체 진행 금지 — 모든 파일 작업은 사용자가 박는 명령어 문서로만
2. agents/README.md는 정본 — 통째 덮어쓰기 금지, 섹션 마커 str_replace로만
3. 박제 순서 — 존재하지 않는 파일을 인덱스에 박지 않음

## 남은 작업 (단계 4~7)

단계 4 (두 단계 분리 권장):
- (4-a) counters/cadam.md + refs/cadam/_index.md 신규 생성 → 커밋
- (4-b) README.md에 vault_assets 섹션 str_replace로 추가 → 커밋

단계 5: data/_config/*.md 8개 (헤더만) + data/initiatives/wf-vi/README.md + data/_inbox/adhoc-queue.md
단계 6: 9개 에이전트 wiki/index.md + wiki/log.md 초기화
단계 7: 최종 git push origin main

## 미완성 (CLAUDE.md 헤더로만 박제, 추후 작성)
- §3.4~§3.10 페이지 타입별 양식
- §4 4계층 학습 흐름 본문
- §5 워크플로우 본문
- §6 학습 추출 가이드 본문
- §7~§14 보조 규칙 본문
- sales cycle, cs cycle 양식 (TBD)
- ops/finance/legal/strategy SKILL.md

## 메모
- 한 세션 = 한 파트 원칙 (파트5 안에서 마이크로 분할)
- heredoc 시작 토큰은 작은따옴표로 ('XXX_EOF')
- 모바일 디렉토리 트리 깨짐 → 첨부 파일 방식 사용
