---
title: "합의메모 — 9에이전트 협업·결재·학습 모델 (파트C)"
type: agreement-memo
area: meta/agents
date: 2026-05-31
status: 확정 (#4는 사장님 OK 대기 표시)
---

# 합의메모 — 9에이전트 협업·결재·학습 모델 (파트C)

이 문서는 파트C 세션에서 확정한 협업 워크플로우·결재/보고·추적성 설계의 단일 기록이다.
후속 파일 박제(governance / CLAUDE.md / _shared/templates / 각 SKILL.md)는 이 문서를 출처로 한다.

---

## 0. 대전제 — cycle이 모든 것의 공통 기록부

새 상위 엔티티(job_id 등)를 만들지 않는다. 협업·결재·보고·학습·인사이트가 모두 **cycle 프론트매터 하나**에 매달린다.

큰 고리:
```
[트리거] → cycle(작업) → 산출물 → [결재판 pending → 승인/수정/반려]
                                          ↓ (최종물이면 _shared/final 복사)
 playbook ← synthesis ← insight ← [학습] ←┘
   └──────────(지난 학습이 다음 cycle 트리거·판정에 재투입)──────────┘
```

---

## 1. 작업 단위 (#1) — 확정

- **원자 단위 = cycle.** 트리거·결재·보고·건별학습이 매달리는 단위.
- **협업 단위 = `triggered_by`로 이어진 cycle 체인.** 저장 엔티티가 아니라 프론트매터에서 재구성. 별도 job 개념 없음.
- **최종물 = 체인의 마지막 cycle + `_shared/final` 복사.** 이 복사 사건이 연쇄학습 발화점.
- 학습 2종: 건별(§6 5질문, 각 cycle 자기완결) / 연쇄(final 떨어지면 체인 역추적해 기여자 호출).

## 2. 트리거 모델 (#2) — 확정

- **schedule 기본 + manual 우회.** pull은 예약 스캔에 흡수, push 배제.
- push 배제 근거: 앞이 뒤의 작업을 결정 = 자율성 위반 / 결합도 / 옵션라 모순 / self-scout 충돌.
- 연결: schedule 트리거 = 정기 → 관리팀장 승인 / manual 트리거 = 스팟 → 대표 승인.

## 3. 핸드오프 (#3) — 확정

- 다운스트림이 업스트림 `outputs/approved/`를 자기 주기에 스캔(= pull).
- 미처리 판별 = 다운스트림 cycle의 `inputs` 필드 (cross-agent write 0, vault 소유권 보존).
- approved/만 스캔 → 미승인 데이터가 다운스트림으로 못 넘어감(오염 차단의 물리적 강제).
- 디스코드 push 방식 배제.

### 3-스팟. 긴급 경로 (옵션 다′) — 확정

- **조율 주체 = 관리팀장(실무자 아님).** 실무자가 동료를 지휘하면 push 권한 문제 재발 → 금지.
- 흐름:
  1. 대표 → 스팟 발행 지시 (스팟 = 대표 결재 진입)
  2. 기획팀장 + 관리팀장 협의 (기획=전략·우선순위 / 관리=실행 판단)
  3. 관리팀장이 approved/ 확인 → 빠진 것 판별 → **빠진 것 기준으로 순서 결정**(고정 아님) → data/content/marketing에 긴급 작업지시(요청 아티팩트) 배분
  4. 실무봇 각자 실행 — **각자 게이트(data 검증/content 정확성) 거쳐 approved/로**
  5. 관리팀장 상태 모니터링 + 결재집행(pending→approved) → 마케팅 발행
- 주기 vs 스팟 조율: 주기 = 조율자 불필요(자율 스캔) / 스팟 = 관리팀장 조율.
- **스팟이라도 게이트 건너뛰기 금지.** 빠르게 통과시킬 뿐, 없애지 않음. 승인 주체만 대표로 상향.
- 메커니즘은 평소와 동일(요청 아티팩트 + 스캔 체인 + 게이트). 바뀐 건 조율 주체뿐.

## 4. 추적성 (#4) — [사장님 OK 대기]

- **output 프론트매터: `source_cycle`** — 그 납품물을 만든 cycle 링크. `[[{에이전트}/raw/cycles/{프로젝트}/cycle-NNN-슬러그]]`
- **cycle 프론트매터: `inputs`** — 이 cycle이 쓴 상류 approved 납품물 링크 리스트. 풀(Supabase/폴더)일 땐 정합성 verdict + 슬라이스(테이블/폴더) 지정.
- 학습루프 역추적: final → source_cycle → inputs → (상류 output) → source_cycle → … → data.
- §7 공급조항 신설: §7.2 금지 대상 = `raw/cycles/insights`(내부 학습물)만. `outputs/approved`(공개 납품물)는 공급관계로 직접 읽기 허용. 참조관계(synthesis/playbook) vs 공급관계(approved 직접)를 §7에서 분리.

## 5. data — 업무·결재·보고 (확정)

- **산출 이중경로:** ① 단발 납품(리포트/스냅샷/점검결과 → approved/) ② 유지되는 풀(Supabase 테이블 + 로컬 폴더). 풀의 핸드오프 = **정합성 verdict("수확 허가")**. content는 풀을 직접 읽되 verdict가 green인 구역만.
- 업무 흐름: 주기 수집+정합성 / 스팟 수집 → 프로세스 확정 → 주기 승격.
- 폴더 대응(실존): `_inbox`(스팟 인테이크) / `builders/cadam`(확정 프로세스=스팟→주기 승격물) / `initiatives/wf-vi`(대형 작업) / `_config`(소스 레지스트리 추정).
- 결재 게이트(진짜): 정합성 verdict(이슈 시) / 스팟 수집(대표) / 스팟→주기 승격(대표, 고위험) / 풀 범위 변경(대표) / 사이트 표시 자산 변경(대표, 더 엄격).
- 보고 중심: 일상 수집(건수·이상치). 이상 無=조용히, 有=알림.

## 6. content — 업무·결재·보고 (확정)

- 주기1: 마케팅 **확정 발행계획**에 따른 소스 생산.
- 주기2: 데이터 스카우팅 → 랜덤 소스 생산(마케팅 신규 주제 선정 입력). 후보 → **관리팀장 승인** → 생산.
- 결재 게이트: 사전(주기2 후보 선택, 관리팀장) / 사후(정확성 검증 = 데이터 풀 대조, 관리팀장) → approved/.
- 전제조건: 해당 데이터 구역의 최신 정합성 verdict green.
- 보완 4: ①정확성 게이트 필수(데이터 틀리면 소스 통째 틀림) ②integrity verdict 의존 ③자산 만료/폐기 보고(데이터 갱신 시 stale) ④재사용 등록(보고 수준).

## 7. marketing — 업무·결재·보고 (확정)

- 주기A: 확정 발행계획 실행 — content job1 소스(approved) + data(approved) 합본 → 최종물(카드뉴스/글/쇼츠) → 발행 → `_shared/final` 복사. (합치는 주체 = marketing)
- 주기B: 신규 주제 발굴·선정 — content job2 후보 + sales conversion-report(§7.4) + 트렌드 → 5질문 Tier 판정 → **확정 발행계획** 산출(주기A·content job1의 시작 조건).
- 스팟: 시즌/긴급 → 대표 결재(위 3-스팟 경로).
- 결재 게이트: 주기B 게이트1(Tier 사람 승인, Q1·Q5 사람/Discord) / 주기A 발행 직전 게이트2(필수, 채널별 강도 차등: 자사블로그<네이버·인스타·쇼츠).
- 쌍7 경계: marketing은 노출까지, 클릭 이후 전환은 sales.
- 보완 5: ①발행=외부 노출=회수 불가에 가까움 → 발행 직전 결재 생략 불가 ②`_shared/final` 복사 = 학습루프 발화 → 복사 시 source_cycle·inputs 채워져 있어야 함 ③결과 측정(7일) → sales → conversion-report → 다시 Tier Q4(피드백 고리) ④발행계획 확정 = 명시적 결재 지점(현재 미정의) ⑤stale 자산 차단.

## 8. 공통 결재 골격

실무봇 산출 → `outputs/pending/` → 관리팀장 1차 품질검토 → 정기·저위험=관리팀장 승인 / 스팟·고위험=대표 결재(`[ESCALATE]`) → `approved/`. 이동 집행 = 파트B 결재판 코드.
- 관리팀장 = opus(조율·판단·업무분배·품질검토·결재집행·모니터링). 실무봇 = sonnet(실행).

## 9. 점검에서 나온 수정/확인 사항

- **수정 1 (완료/명령 발행):** §4.1 cycle 경로 모순 → `{에이전트}/raw/cycles/{프로젝트}/cycle-NNN-{슬러그}.md`로 통일.
- **수정 2 (#4에 포함):** §7 공급조항 신설.
- **수정 3 (#4에 포함):** inputs/source_cycle 템플릿 추가.
- **확인 필요:** §7.6 미완(sales `synthesis-conversion-report` 정기 산출물 정의, boundary-rules marketing↔sales). marketing 주기B가 이 리포트를 참조하므로 sales 측 정의 확인 필요.

## 10. 박제 위치 맵 (후속 작업)

| 대상 파일 | 박는 내용 |
|---|---|
| `governance/` | 이 합의메모 + (결재·보고 규정 REG-002 후보) |
| `CLAUDE.md` §4.1 | 경로 수정 (완료) |
| `CLAUDE.md` §7 | 공급조항 신설(참조 vs 공급 분리) |
| `_shared/templates/cycle-*.md` | 프론트매터에 `inputs`, 납품물에 `source_cycle` |
| `data/SKILL.md` | 산출 이중경로, 결재 게이트, 정합성 verdict |
| `content/SKILL.md` | 주기1·2 정의, 정확성/후보 게이트, 만료 보고 |
| `marketing/SKILL.md` | 주기A·B 정의, 발행 결재(채널 차등), 피드백 고리 |
| `admin/SKILL.md` | 스팟 조율(업무분배) 절차 = 옵션 다′ |
