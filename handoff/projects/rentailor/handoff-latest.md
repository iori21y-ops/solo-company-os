---
project: rentailor (solo-company-os 메타)
session: 디렉토리 재구조화 + 자동화 완료 → 쌍3 sales↔cs로
date: 2026-05-24
status: 완료
---

# 핸드오프: 인프라 정비 완료 → 쌍3 sales↔cs로

## 직전 세션 (자급자족)

**무엇을 했나**: 핸드오프 시스템 디렉토리 재구조화 + 자동화 스크립트 구축.

**완료된 것**:
1. GitHub 공개 저장소 구조 정비 (`meta/agents`, `scratch/general` 영역 신설)
2. `scripts/new-handoff.sh` — 신규 영역 자동 생성
3. `scripts/refresh-readme.sh` — README 활성 영역 표 자동 갱신
4. 루트 README에 "🚀 활성 핸드오프 영역" 섹션 자동 생성
5. `.gitignore` 보강 (`notes-private.md` 추가)
6. 공개 9개 URL 200, 차단 2개 URL 404 확인 완료

## 이번 세션에서 할 일

**쌍3: sales ↔ cs 경계 정의**

지금까지 확정된 경계:
- 쌍1 marketing↔content: 요리사 ↔ 재료 공급자
- 쌍2 content↔data: 재료 공급자 ↔ 농장

남은 4쌍 중 쌍3부터:
- 쌍3: sales ↔ cs (이번)
- 쌍4: ops ↔ data
- 쌍5: strategy ↔ 전체
- 쌍6: legal ↔ finance

## 작업 패턴 (반드시 따를 것)

1. **비유부터 정하기** (쌍1·2처럼 직관적으로)
2. **경계 규칙 본문 작성** (4~6줄)
3. **회색지대 표** (3~5건의 구체 사례 + 어디 담당인지)
4. **한 줄 테스트** (자가 검증용)
5. **클코로 박제**:
   - `agents/_shared/boundary-rules.md`에 새 SECTION 추가
   - `agents/sales/SKILL.md`, `agents/cs/SKILL.md` 스텁→정의됨 교체
   - `agents/README.md` 상태 갱신
6. 박제 시 `_shared/modification-checklist.md` 케이스 A 따라 4곳 누락 확인

## 핵심 페치 URL (필요 시)

- 전체 인덱스: https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/README.md
- 에이전트 목록: https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/README.md
- 기존 경계 규칙 (쌍1·2 참고): https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/boundary-rules.md
- 잘 정의된 SKILL.md 예시: https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/marketing/SKILL.md

## 첫 질문

sales와 cs의 핵심 차이는 무엇인가? (둘 다 "고객과 대화"이지만 어디서 갈리는가)

- 가설1: 리드(잠재고객) ↔ 기존고객
- 가설2: 구매 전 ↔ 구매 후
- 가설3: 능동적 추적 ↔ 수동적 응대
