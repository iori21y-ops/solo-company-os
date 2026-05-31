# 핸드오프 — 에이전트 실제 업무 인벤토리 (착수)

- area: meta/agents
- date: 2026-05-31

## 1. 이어가는 중
9-에이전트 OS 트랙. 직전 파트C에서 협업·결재·학습 모델 설계·박제 완료(커밋·푸시까지). 이번은 그 틀에 채울 "현재 실제 하고 있는 업무" 인벤토리 착수. 새 작업이 아니라 연속.
받으면 먼저: ① conversation_search로 파트C 검토 ② 추측 기반 반박부터 하지 말 것.

## 2. 마스터플랜 — 왜 이걸 하나
파트C에서 업무가 흐르는 틀(cycle 단위 / schedule·manual 트리거 / 결재·보고 게이트 / outputs/approved 핸드오프)을 만들었다. 그런데 틀만 있고 내용물(각 에이전트가 실제로 뭘 하는지)이 비어 있다. 이 인벤토리가 채워져야 cycle이 실제로 돌기 시작한다.
원칙: 추측으로 업무를 지어내지 말고, 실재하는 것에서 끌어낸다.

## 3. 기존 자산 (파트C 박제물 — 전체 설계는 governance 메모 참조)
- governance/합의메모-파트C-협업결재학습모델.md — 전체 설계 단일 기록 (이거 먼저 읽기)
- CLAUDE.md §4(4계층 학습) · §7(참조 vs 공급 분리) · §9(사이클 생애주기)
- _shared/templates/cycle-{data,content,marketing}.md — inputs 필드 추가됨, output엔 source_cycle
- data/content/marketing/admin SKILL.md — "결재·보고·업무 흐름" 섹션 박제됨
- 폴더: {agent}/raw/cycles · /outputs/{pending,approved,rejected} · /wiki, data/{_inbox,builders,initiatives,_config}, _shared/{templates,counters}
- 결재 골격: 실무봇→pending→관리팀장 품질검토→정기=관리팀장 / 스팟=대표→approved
- 트리거: schedule 기본 + manual 우회(push 배제). 스팟 협업 = 관리팀장 조율([CALL:]+기획팀장 협의, 게이트 유지)

## 4. 이번 미션 — 방법론 (직전 세션 합의)
현재 업무는 두 부류:
- (1) 이미 자동/스크립트로 도는 것 → 기계가 알려줌(열거). n8n 활성 워크플로, launchd/cron, 스크립트(~/cadam-data/scripts, data/builders), Flask(9722 크롤 / 9724 인포그래픽).
- (2) 아직 경년님이 손으로 하는 것 → 경년님 회상으로만. 상담 후 처리, 발행, 데이터 갱신 등 매일/매주/매월 루틴.

분류 4칸(= cycle 정의): 에이전트(data/content/marketing) / 주기·스팟 / 현재상태(수동·자동) / 트리거·결재게이트.
기록: {agent}/_tasks.md 평면 목록으로 먼저 → 검증되면 주기 업무는 playbook+스케줄로, data 수집 프로세스는 builders/로 승격.

## 5. 판단 (바뀐 것 없음, 신규 트랙)
파트C = 메타(틀), 이번 = 오브젝트(내용물). 순서 역전 아님 — 틀이 먼저 있어야 업무를 어디에 넣을지 정해진다.

## 6. 우선순위 / 범위
- 범위: data/content/marketing 3개 활성 에이전트의 현재 업무만. 미활성 6개(sales/cs/ops/finance/legal/strategy) 제외.
- (1) 자동화 열거부터(추측 0) → 그다음 (2) 수동 회상.
- 한 번에 한 에이전트씩 분류 권장(과부하 방지).

## 7. 첫 지시 (순서대로)
1. 자동화된 현재 업무 열거 — 클코로 한 번에: ls ~/Library/LaunchAgents/ + launchctl list | grep -i rentailor, crontab -l, ls -la ~/cadam-data/scripts/, ls -la data/builders/cadam/ data/initiatives/, n8n 활성 워크플로 목록(UI 또는 API — 접근법부터 확인). 결과 원문 출력.
2. 결과를 data/content/marketing × 주기/스팟 4칸으로 1차 분류(Claude가 제안 1개씩).
3. 그다음 경년님 수동 routine 회상 → 누락분 보완.
4. 합의된 분류만 {agent}/_tasks.md로 박제(신규 생성 또는 str_replace, 합의메모 먼저).

## 제약
- 클코 자체 진행 금지 — 명령어 문서로만 / 통째 덮어쓰기 금지 — str_replace·신규생성만
- 한 세션 = 한 파트 / 합의메모 없으면 박제 안 함 / git 자동 커밋·푸시 금지(명시 지시 시만)
- second-brain vault 읽기만 / 모름은 추측 금지 — "확인하려면 [명령어]" 형식
- 추측으로 업무 목록 지어내지 말 것 — 실재(자동화 열거 / 경년님 회상)에서만

## 환경
- 경로: ~/projects/_meta (= git repo, github.com/iori21y-ops/solo-company-os, 파트C 푸시 완료)
- 모델: 클코 기본 Sonnet, Opus 어드바이저. 관리팀장=opus, 실무봇=sonnet
- n8n = Docker(downloads-n8n-1). Flask 9722(크롤)/9724(인포그래픽)
