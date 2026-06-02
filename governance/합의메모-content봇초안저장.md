# 합의메모 — content봇 초안 → pending 저장 (방식 B-1)

- date: 2026-06-01
- area: meta/agents (디스코드 구현 트랙)
- 선행: 결재판 파일이동 완성·검증(합의메모-결재판파일이동.md)

## 배경
content봇은 현재 답변을 채팅 출력만 함(agent.js, 파일 저장 코드 없음 — grep으로 확정).
결재판(pending→approved 이동)은 완성됐으나, 그 앞단 "초안을 pending에 올리는 입구"가 없음. 이 메모가 그 입구를 정의.

## 방식 결정: B-1 (명시 커맨드 + 직전 봇 메시지 캡처)
A안(봇이 [SAVE] 마커 자가 부착)을 기각하고 B-1 채택.
- 기각 이유(A): 저장 시점이 봇 판단에 종속 — 마커 누락 시 저장 실패, 오부착 시 미완성본 적재.
- 채택 이유(B-1): 저장 시점을 사람이 쥠. 이미 만든 결재판과 동일 철학(봇=산출, 사장님=상태이동). 결재판 핸들러·fetch 패턴 재사용으로 코드 일관.

## 동작 정의
- 트리거: `@관리팀장 저장 content <파일명>` (관리팀장 멘션 필수 + 사장님 전용, 결재판과 동일 권한 게이트)
- 저장 대상: 커맨드 직전, 같은 채널에서 content봇(ID 2535)이 보낸 가장 최근 메시지 1건의 본문
- 캡처 방법: channel.messages.fetch (모델전환·히스토리에서 쓰던 limit10 패턴 재사용)
- 형식: md
- 파일명: `<파일명>-YYYYMMDD.md`
- 안전: 파일명에 `/`, `..` 포함 시 거부(결재판 검증 로직 재사용)
- 경로: ~/projects/_meta/agents/content/outputs/pending/
- SKILL.md 수정: 불필요(봇은 평소대로 초안 출력만)

## 구현 제약
- str_replace로만(통째 덮어쓰기 금지). 신규 핸들러는 결재판 핸들러 직후 삽입.
- node --check 통과 → broker 재기동 → 디스코드 실테스트.
- 검증 전 박제(cycle/playbook) 안 함. git은 명시 지시 시만.

## 미포함(이번 범위 밖)
- 이미지·SEO·검수·재작성·반려루프
- md→HTML 변환(발행 직전 marketing 단계에서)
- content봇이 초안을 자동으로(스케줄로) 만드는 것 — 지금은 사장님이 멘션으로 초안 요청 후 저장

## 구현·검증 완료 (2026-06-01)
- agent.js 결재판 핸들러 직후 저장 핸들러 삽입 (str_replace). import에 writeFileSync 기존 존재.
- 동작: `@관리팀장 저장 <에이전트> <파일명>` → channel.messages.fetch(limit20) → 해당 봇 마지막 메시지 캡처 → pending/<파일명>-YYYYMMDD.md 저장.
- 봇 식별 견고화: username 문자열 매칭 → author.id 매칭으로 교체. 봇ID: content=1510266422859792535, marketing=1510265704010748104, data=1510267015154106609. 닉네임 변경에 안 깨짐.
- 검증: 디스코드 실테스트 통과. pending/아반떼-장기렌트-20260531.md 생성 확인(저장 내용=content봇 ESCALATE 메시지, 봇이 SKILL 규칙대로 초안 거부한 정상 케이스).
- 미해결(다음 파트): content봇이 실제 초안을 쓰려면 데이터 검증(green verdict) 흐름 필요 — data봇 verdict → content봇 초안 해금. cycle 1바퀴 실발행은 그 후.
