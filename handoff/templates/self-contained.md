# 자급자족 핸드오프 템플릿

모바일 새 세션이 파일 읽기 없이도 즉시 작업 시작 가능하도록 설계.

## 사용법
세션 마무리 시 클코가 이 템플릿 채워서 pbcopy → 모바일 새 채팅에 ⌘V.

---

## 템플릿 (아래부터 복사)

[작업 이어가기: {프로젝트명} - {파트명}]

## 직전 맥락 (자급자족 - 페치 없이 작업 가능)
- 무엇을 하고 있나: {한 줄}
- 어디까지 했나: {3줄 이내}
- 이번에 할 일: {한 줄}

## 핵심 규칙·패턴 (이 세션에서 따라야 할 것)
- {규칙 1}
- {규칙 2}
- {규칙 3}

## 결정 박제 위치
- 메인: ~/projects/_meta/{경로}
- 클코 박제 패턴: {예: 섹션 마커 str_replace}

## 필요 시 페치 (선택적 — 인덱스 한 줄 방식)

맥락이 더 필요하면 새 세션에 아래 중 하나를 한 줄로 전달:

```
# 에이전트 구조 확인용
agents/README.md를 읽어서 9개 에이전트가 뭔지 정리해줘:
https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/README.md
```

```
# 경계 규칙 작업 시작용
agents/_shared/boundary-rules.md를 페치해서 지난 작업의 경계 규칙 패턴을 파악해줘:
https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/agents/_shared/boundary-rules.md
```

전체 인덱스: https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/README.md

## 첫 작업
{구체적으로 무엇부터 시작할지}
