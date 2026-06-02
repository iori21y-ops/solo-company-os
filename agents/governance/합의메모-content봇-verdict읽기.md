# 합의메모 — content봇 verdict 읽기 게이트 (구현·검증 완료)

- area: meta/agents (디스코드 구현 트랙)
- date: 2026-06-01
- 선행: 합의메모-verdict형식.md (스키마 확정)

## 확정 설계 — 방법 B (코드 스캔)
content봇이 초안 전 verdict를 읽는 방식을 LLM 지시(방법 A)가 아닌 코드 주입(방법 B)으로 확정.
이유: broker가 --no-session-persistence라 매 메시지 새 세션 → "파일 읽어라" SKILL 지시가 매번 실행된다는 보장 없음(비결정론). 코드가 결정론적으로 읽어 userPrompt에 주입.

## 구현 (agent.js askClaude, 314줄 userPrompt 조립부)
- name === '콘텐츠'일 때만 approved/ 스캔.
- 경로: ${process.env.HOME}/projects/_meta/agents/data/outputs/approved (AGENTS_ROOT는 askClaude 클로저 밖이라 HOME 직접 사용).
- verdict-*.md frontmatter 정규식 파싱(subject/verdict/data_type/checked), verdict===green만 수집.
- userPrompt 앞에 verdict 블록 주입 + 게이트 문구 동봉:
  - green 있음: "위 목록 차종만 초안 가능, 없는 차종은 거부+ESCALATE"
  - green 없음: "green 없음, SKILL 규칙대로 거부+데이터검증요청+ESCALATE"
- readdirSync/readFileSync 기존 import 재사용, 추가 import 없음.

## 검증 (디스코드 실테스트, 2026-06-01)
- verdict 파일: data/outputs/approved/verdict-hyundai-avante-20260601.md (subject:hyundai-avante, data_type:visual, audit_kind:referential, verdict:green, checked:2026-06-01).
- 게이트 닫힘 ✅: "카니발 글" 요청 → 봇이 주입목록에서 kia-carnival 없음 확인 → 거부+ESCALATE. 코드 주입 데이터 기반 결정론적 차단 확인.
- 게이트 열림 ✅: "아반떼" 요청 → visual green 통과 → CLI 도달. 단순 호출은 정상 응답.
- 유형 분리 작동 ✅: "아반떼 장기렌트(가격)글" 요청 시 봇이 "visual green은 맞으나 가격=quantitative 미검증"이라 거부. 유형 다르면 상호 보증 안 함(핸드오프 5절 원칙) 정상 작동.

## 미해결 (다음 파트)
- 타임아웃: 복잡 작업(이미지 스펙카드 등 도구 사용)에서 Claude CLI 호출이 .env CLAUDE_TIMEOUT_MS=300000(5분) 꽉 채우고 행. CLI 단독은 3.2초, 단순 broker 호출도 정상 → broker 버그 아닌 복잡작업 한정 인프라 문제. 게이트와 무관, 별도 파트.
- _config audit-rules 5종 실내용(무엇이 green인가) 미작성 — visual/referential만 wf_vi 실물 존재, 나머지 4종 draft.
- cycle 1바퀴 실발행(초안→저장→승인→wp_publish.py): 타임아웃 해결 후.
