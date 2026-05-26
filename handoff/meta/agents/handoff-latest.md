# 핸드오프 — agents vault 박제 완료, 다음은 §11·§12 등 본문 작성

area: meta/agents
date: 2026-05-27
session: 파트5 학습루프 + vault 박제 단계 4~7 완료

## 완료 (이번 세션)
로컬 커밋 4개 + 원격 push 완료:
- 84c3450 — counters README/cadam + refs/cadam _index 신규 생성 (단계4-a)
- c78df47 — README.md vault_assets 섹션 추가 (단계4-b)
- b56c76b — data/_config 8개 + wf-vi README + adhoc-queue 박제 (단계5)
- 72f47a6 — 9개 에이전트 wiki/index.md + wiki/log.md 최소 초기화 (단계6)

## 박제 완료 핵심 자산 (누적)
- agents/CLAUDE.md (444줄, 합의 섹션 + 미완성 헤더 11개)
- agents/README.md (vault_assets 섹션 포함, 4개 SECTION 마커)
- agents/_shared/templates/cycle-marketing.md
- agents/_shared/templates/cycle-content.md
- agents/_shared/templates/cycle-data.md
- agents/_shared/counters/README.md + cadam.md (last_cycle: 0)
- agents/_shared/refs/cadam/_index.md (빈 stub 인덱스)
- agents/data/_config/*.md 8개 (헤더 + TBD)
- agents/data/initiatives/wf-vi/README.md
- agents/data/_inbox/adhoc-queue.md
- agents/{9에이전트}/wiki/index.md + log.md (빈 껍데기)
- vault 디렉토리 골격 233개 + Obsidian 인식

## 미완성 (다음 세션 작업 후보)
- CLAUDE.md §3.4~§3.10 페이지 타입별 양식
  (insight/synthesis/playbook/failure/concept/entity/project-ref/scout-candidate)
- CLAUDE.md §4 4계층 학습 흐름 본문
- CLAUDE.md §5 워크플로우 본문
- CLAUDE.md §6 학습 추출 가이드 본문
- CLAUDE.md §7~§14 보조 규칙 본문 (특히 §11 index.md 형식, §12 log.md 형식)
- _shared/templates/cycle-sales.md, cycle-cs.md
- ops/finance/legal/strategy SKILL.md
- data/_config/*.md 8개 본문 (현재 TBD)

## 다음 세션 진입 시
1. ~/projects/_meta/agents/CLAUDE.md 읽기
2. ~/projects/_meta/agents/README.md 읽기 (vault_assets 섹션 포함)
3. 위 "미완성" 중 하나 선택 → 한 세션 = 한 파트 원칙으로 진행

## 절대 원칙 (유지)
1. 클코 자체 진행 금지 — 명령어 문서로만
2. CLAUDE.md / README.md 통째 덮어쓰기 금지, 섹션 마커 str_replace로만
3. 존재하지 않는 파일을 인덱스에 박지 않음 (박제 순서 엄수)

## 메모
- heredoc 시작 토큰은 작은따옴표로 ('XXX_EOF')
- 모바일 디렉토리 트리 깨짐 → 첨부 파일 사용
- 한 세션 = 한 파트 원칙
