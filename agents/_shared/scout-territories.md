# 자율 발굴 영역 매트릭스

## 목적

각 에이전트가 자율 발굴(트리거 J) 권한을 어디까지 갖는지, 영역을 벗어난 정찰이 필요할 때 어떻게 처리할지 정한다.

## 영역 매트릭스

| 에이전트 | 자기 영역 자율 발굴 | second-brain 정찰 | 타 에이전트 영역 정찰 |
|---------|-------------------|------------------|-------------------|
| content | ✓ | ✓ (단독) | 위탁 받으면 |
| data | ✓ | ✗ | 위탁 받으면 (드묾) |
| marketing | ✓ | content에 위탁 | content에 위탁 |
| sales | ✓ | content에 위탁 | content에 위탁 |
| cs | ✓ | content에 위탁 | content에 위탁 |
| ops | (정의 후) | content에 위탁 | content에 위탁 |
| finance | (정의 후) | content에 위탁 | content에 위탁 |
| legal | (정의 후) | content에 위탁 | content에 위탁 |
| strategy | (정의 후) | content에 위탁 | content에 위탁 |

## 핵심 규칙

1. 자기 영역: 각 에이전트의 raw/, cycles/, 자기 _config/
2. second-brain: 외부 자료(웹, 문서, 공개 데이터) — content만 정찰 단독
3. 타 에이전트 영역 정찰이 필요하면: content에 B-J 위탁

## B-J 위탁 흐름

[의뢰 에이전트] → 트리거 B로 content에 정찰 의뢰
              → [content] 트리거 J로 위탁 정찰 사이클 시작
              → 의뢰 에이전트의 raw/cycles 한정 권한 읽기
              → 정찰 결과를 content/cycles/ 에 박제
[의뢰 에이전트] → content 결과 페이지를 인용/링크만

## 인접 영역 참조 (§7.2 원칙 적용)

marketing은 sales의 conversion-report(synthesis)를, sales는 marketing의 attribution synthesis를 참조한다. 이는 예외가 아니라 §7.2(synthesis만 참조) 원칙의 정상 적용이다. 원본을 직접 읽는 것이 아니다.

## 미정 영역

ops/finance/legal/strategy는 자율 발굴 영역 정의가 아직 안 됐다. 각 에이전트 SKILL.md 작성 시 매트릭스에 채운다.
