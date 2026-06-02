# CLAUDE.md — 에이전트 학습 vault 운영 규칙

이 파일은 에이전트 학습 vault의 운영 규칙을 정의한다.
모든 학습 작업(사이클 기록, 인사이트 추출, 승격, 린트)은 이 스키마를 따른다.

> **참조 파일(상세 스키마는 본문에서 분리, 필요 시 읽기):**
> - §2.1 디렉토리 구조 → [_shared/ref-vault-structure.md](_shared/ref-vault-structure.md)
> - §3 페이지 형식 → [_shared/ref-page-formats.md](_shared/ref-page-formats.md)
> - §8 위임 프레임워크 → [_shared/ref-delegation.md](_shared/ref-delegation.md)
> - §9 사이클 생애주기 → [_shared/ref-cycle-lifecycle.md](_shared/ref-cycle-lifecycle.md)
> - §11 index.md 형식 → [_shared/ref-index-format.md](_shared/ref-index-format.md)
> - §12 log.md 형식 → [_shared/ref-log-format.md](_shared/ref-log-format.md)
> - §14 Obsidian 호환 → [_shared/ref-obsidian.md](_shared/ref-obsidian.md)

최종 업데이트: 2026-06-02 (상세 스키마 5개 섹션을 _shared/ref-*.md로 분리)

---

# ⚠️ 최우선 규칙

## 0.1 모든 질문은 wiki/index.md 먼저

에이전트가 어떤 작업을 시작하든 — 사이클 시작, 인사이트 추출, 종합 분석, 질의 응답 — 웹서치나 자체 추론으로 바로 답하지 말고, 반드시 아래 순서를 따른다:

1. `{에이전트}/wiki/index.md` 읽기 → 관련 페이지 확인
2. 관련 페이지가 있으면 해당 페이지를 읽고 학습 데이터 기준으로 답변
3. 학습 데이터에 없는 경우만 웹서치/추론 사용 (사용 시 "학습 데이터에 없어 외부 정보로 답변" 명시)

위키 파일 검색 시 glob 패턴은 반드시 한글 포함 전체 목록을 커버해야 한다.
이 규칙을 어기면 학습 누적이 무의미해진다.

## 0.2 자가수정 금지

에이전트는 다음을 절대 자기 손으로 수정하지 않는다:

- 자신의 시스템 프롬프트
- 자신의 SKILL.md 본문
- 다른 에이전트의 wiki, raw, SKILL.md
- CLAUDE.md (이 파일)
- _shared/ 하위

위 항목은 모두 **사람(경년님) 또는 추후 strategy 에이전트의 승인** 후에만 수정 가능.
에이전트는 자기 wiki 안에서 신규 페이지 생성·수정만 허용된다.

---

# 1. 역할 정의

## 1.1 에이전트의 역할

- **위키 관리자**: 자기 vault 내 wiki 페이지를 생성·수정·교차참조한다.
- **사이클 실행자**: 트리거 받은 작업을 raw/cycles/에 사실대로 기록한다.
- **인사이트 추출자**: 사이클 종료 시 §6 "학습 추출 가이드"에 따라 인사이트 후보를 만든다.
- **참조자**: 사이클 시작 시 §5 "워크플로우"의 로드 순서에 따라 학습 데이터를 먼저 읽는다.

에이전트는 자기 vault 안에서만 권한이 있다. 다른 에이전트 vault는 **읽기 전용**.
다른 에이전트 인사이트 참조 시 §7 규칙 준수.

## 1.2 사용자(경년님)의 역할

- **큐레이터**: 사이클 결과를 검토하고 인사이트 후보를 승격(confirmed/rejected) 한다.
- **승격 게이트키퍼**: 프로젝트→직무 승격, Tier 상향, 플레이북 박제의 최종 승인.
- **방향 설정자**: 직무 정의(SKILL.md), 경계(boundary-rules.md), 위임 등급의 결정.

사용자는 비개발자이므로 모든 설명은 한국어로, 쉽게 작성한다.

## 1.3 추후 위임 (strategy 에이전트)

strategy 에이전트가 정의 완료되고 위임 5질문을 50회 누적 통과하면,
사용자의 "승격 게이트키퍼" 역할 중 일부를 strategy로 위임한다.
위임 시점은 별도 결정. 현재(2026-05)는 모든 승격을 사람이 직접 한다.

---

# 2. 디렉토리 구조

## 2.1 전체 구조

vault 전체 디렉토리 트리(각 에이전트의 `raw/`·`wiki/_skill/`·`wiki/{프로젝트}/`·`scouts/` 구조, `_shared/` 공통 자산, data의 `_config/`·`builders/` 등) 상세는 [_shared/ref-vault-structure.md](_shared/ref-vault-structure.md) 참조. 요약: 각 에이전트 폴더 = `SKILL.md` + `raw/cycles/{프로젝트}/` + `wiki/`(index·log·_skill·{프로젝트}), 공통 자산은 `_shared/`.

## 2.2 각 폴더의 책임

- **raw/cycles/{프로젝트}/**: 사이클 진행 사실 기록. 불변(오타·포맷 제외 수정 금지).
- **wiki/_skill/**: 직무 일반 학습. 2개 이상 프로젝트 confirmed 후 승격으로만 진입.
- **wiki/{프로젝트}/**: 프로젝트 한정 학습. 사이클 인사이트 1차 박제 위치.
- **wiki/{프로젝트}/scouts/**: 자율 발굴 후보의 라이프사이클 (pending/approved/rejected/completed).
- **assets/, builders/**: wiki 밖. 실제 비축 자산·도구 (wiki는 LLM 학습 페이지 전용).
- **_shared/refs/{프로젝트}/**: 외부 정본 vault의 stub 페이지.

## 2.3 사이클 ID 채번 규칙

- 형식: `cycle-NNN` (3자리 0 패딩)
- 채번 단위: **프로젝트별 단일 카운터** (에이전트 무관)
  - 예: cadam 전체에서 cycle-001, 002, 003... 단조 증가
- 채번 위치: `_shared/counters/{프로젝트}.md` 마지막 번호 + 1
- 채번은 단조 증가, 결번 허용

## 2.4 에이전트 간 사이클 연결

같은 프로젝트의 인접 사이클이 협업 관계일 때 프론트매터로 연결:

```yaml
---
cycle_id: 008
agent: content
project: cadam
triggered_by: [[marketing/raw/cycles/cadam/cycle-007]]
parallel_with: []
follow_up_to: []
---
```

## 2.5 _shared/refs/{프로젝트}/ stub

외부 정본 vault(예: ~/second-brain)의 자주 참조되는 페이지를 에이전트 vault 안에서도
백링크 가능하게 만드는 어댑터. 본문은 정본 URI 링크 + 에이전트 관점 메모만.

- stub 생성 기준: 1회 이상 사이클에서 참조된 엔티티부터
- 정본 정보 복제 금지 (SSOT 원칙)
- 본문은 "에이전트 관점 메모" 누적만

## 2.6 vault 외부 자산 참조

vault 외부 자산은 텍스트 참조만:
- **second-brain (카담 정본)**: ~/second-brain/wiki/...
  → `_shared/refs/cadam/` stub 통해 참조
- **GitHub**: github.com/iori21y-ops/solo-company-os (vault 자체가 일부)
- **Supabase, n8n, 외부 API**: 참조 정보(테이블명, 워크플로 ID)만 기록
- **핸드오프 시스템**: ~/projects/_meta/handoff/ (별도 시스템)

---

# 3. 페이지 형식 규칙

모든 wiki 페이지의 양식 규칙. 공통 프론트매터(필수4·조건부2·선택3, scope 판정)·내부 링크·페이지 타입별 필수 섹션(cycle/insight/synthesis/playbook/failure/concept/entity/project-ref/scout-candidate)·명명 규칙·본문 작성 규칙 상세는 [_shared/ref-page-formats.md](_shared/ref-page-formats.md) 참조.

---

# 4. 4계층 학습 흐름

학습 결과물은 4개 계층으로 구분된다. 하위 계층이 상위 계층으로 승격되며, 각 계층은 성격·승격 트리거가 다르다.

## 4.1 cycles (사실 기록)

- 성격: 불변(immutable). 한 번 작성되면 수정하지 않음
- 내용: 사이클 실행 중 발생한 사실, 관찰, 결과
- 위치: `{에이전트}/raw/cycles/{프로젝트}/cycle-NNN-{슬러그}.md`

## 4.2 insights (가설)

- 성격: 가변. 상태값으로 관리: `pending` → `confirmed` 또는 `rejected`
- 내용: cycles에서 도출된 가설. 검증 전이므로 단정 금지
- 승격 트리거: 동일 가설이 다른 사이클에서 재확인되면 `confirmed`
- 위치: `{프로젝트}/insights/{주제}.md` (프론트매터에 status 명시)

## 4.3 syntheses (횡단 분석)

- 성격: 여러 insights를 묶어 패턴 추출
- 승격 트리거: 다음 둘 중 하나
  - 같은 프로젝트 내 confirmed insights 3건 이상
  - 서로 다른 프로젝트 간 confirmed insights 2건 이상
- 위치: `{프로젝트}/syntheses/{패턴명}.md` 또는 `_shared/syntheses/`

## 4.4 playbooks (행동 원칙)

- 성격: 다음 사이클에 자동 적용되는 규칙
- 승격 트리거: synthesis가 행동 가능한 규칙으로 정제됨
- 내용: "X 상황에서는 Y 한다" 형식의 단언문
- 위치: `wiki/{프로젝트}/playbooks/` 또는 `_skill/playbooks/`

## 4.5 수명 정책

> [!warning] 미정
> 각 계층별 수명·아카이브 정책은 실제 사이클 운영 후 결정. 현재는 모든 계층 영구 보존.

---

# 5. 워크플로우

## 5.1 목적

§4가 4계층의 *정의*라면, §5는 *운영 절차*다. 사이클을 시작할 때 무엇을 로드하고, 끝낼 때 어떤 순서로 마무리하는지 정한다.

## 5.2 사이클 시작 시 로드 순서

새 사이클을 시작할 때 다음 순서로 컨텍스트를 로드한다:

1. `wiki/index.md` — 단일 진실 소스
2. `wiki/_skill/playbooks/` Tier 1 — 직무 공통 행동 원칙
3. `wiki/{현재 프로젝트}/playbooks/` Tier 1 — 프로젝트 행동 원칙
4. `_skill/insights/` confirmed + 관련 pending — 직무 가설
5. `{프로젝트}/insights/` confirmed + 관련 pending — 프로젝트 가설
6. `_shared/refs/{프로젝트}/` 관련 stub — 횡단 참조

playbooks가 먼저 (행동 원칙이 가설보다 우선), insights가 다음 (검증된 것 → 검증 중), refs는 마지막 (필요할 때만).

## 5.3 사이클 종료 시 절차

다음 순서로 마무리한다. 순서가 중요하다 — 앞 단계의 출력이 뒤 단계의 입력이다.

1. **결과 측정** — 에이전트별 KPI에 따라 cycles 기록 (사실부터)
2. **승격 게이트** — pending insights를 사람 승인으로 `confirmed` 또는 `rejected` 처리
3. **직무 승격** — confirmed insights 중 playbook으로 정제 가능한 것을 `{프로젝트}/playbooks/` 또는 `_skill/playbooks/`로 승격
4. **횡단 종합 트리거** — syntheses 조건 검사 (같은 프로젝트 confirmed 3건 이상, 또는 다른 프로젝트 간 confirmed 2건 이상)
5. **린트** — 모순/고아/누락/오래됨 점검 (마지막 청소)

**순서 근거:**
- 사실 없이 가설 판정 불가 → 측정이 먼저
- insights가 confirmed 돼야 playbook 후보가 됨 → 게이트 → 직무 승격
- 같은 프로젝트 내 정제가 안정돼야 횡단 입력이 깨끗함 → 직무 승격 → 횡단
- 모든 변경 끝난 뒤 청소 → 린트 마지막

## 5.4 주의

- 로드 순서·종료 절차 둘 다 운영하면서 조정 가능. 현재는 출발점.
- 5.3의 순서는 자동화 시에도 동일 (n8n 등으로 자동화하더라도 단계 순서 유지).
- 사이클 종료 절차는 §6 학습 추출 가이드(5가지 질문 답변)와 병행 — 5.3 단계 1(측정) 직후 §6 질문에 답하는 것이 자연스러움.

---

# 6. 학습 추출 가이드

## 6.1 목적

사이클이 끝날 때마다 5가지 질문에 답한다. 답변은 §4의 4계층
학습 흐름으로 들어가는 입력이다. 질문에 답하지 않으면 cycles는
사실 기록으로만 남고 학습은 일어나지 않는다.

## 6.2 5가지 질문

사이클 종료 시 다음 5가지 질문에 답한다:

1. 이번 사이클에서 처음 알게 된 것이 있는가?
2. 예상과 다른 결과가 나온 부분이 있는가?
3. 다음 사이클에서 다르게 할 점이 있는가?
4. 다른 프로젝트에서도 적용될 가능성이 있는가?
5. 절대 다시 하지 말아야 할 패턴이 있는가?

답이 "없다"여도 명시적으로 "없음"이라고 적는다. 빈칸은 질문을
건너뛴 것과 구분되지 않는다.

질문 자체는 운영하면서 다듬을 수 있다. 단 변경 시 변경 이력을
남기고, 변경 전후 사이클을 비교할 때 질문 차이를 고려해야 한다.

## 6.3 답변이 가는 곳

| 질문 | 산출물 위치 | status |
|------|-----------|--------|
| 1. 처음 알게 된 것 | `{프로젝트}/insights/{날짜}-{주제}.md` | pending |
| 2. 예상과 다른 결과 | `{프로젝트}/insights/{날짜}-{주제}.md` | pending |
| 3. 다음에 다르게 할 점 | `{프로젝트}/insights/{날짜}-{주제}.md` | pending |
| 4. 다른 프로젝트 적용 가능성 | `{프로젝트}/insights/{날짜}-{주제}.md` (프론트매터에 `cross_project: true`) | pending |
| 5. 절대 다시 하지 말 패턴 | `{프로젝트}/insights/{날짜}-{주제}.md` (failure 태그) | pending |

모든 답변은 처음에 `status: pending`으로 시작한다. confirmed/rejected
전환 규칙은 §4.2 참조.

## 6.4 운영 순서

1. 사이클 종료
2. cycles 파일 작성 완료 (사실 기록)
3. 5가지 질문에 답
4. 답변별로 insights 파일 생성 (status: pending)
5. 질문 4번 답이 "있다"면 해당 insights 프론트매터에 `cross_project: true` 추가

## 6.5 §4 승격 트리거 (재확인)

§6에서 생성된 insights는 §4 학습 흐름을 따른다:

- 같은 프로젝트 내 confirmed insights 3건 이상 → synthesis 생성
- 서로 다른 프로젝트 간 confirmed insights 2건 이상 → 횡단 synthesis 생성
- synthesis가 "X 상황에서는 Y 한다" 형태로 단언 가능 → playbook 승격

상세 규칙은 §4.3, §4.4 참조.

## 6.6 주의

- 5가지 질문에 답하지 않은 사이클은 §4 학습 흐름에 들어가지 않는다
- 답변은 추측이 아닌 사이클 중 실제 관찰한 것만 적는다
- 질문 4번에 "있다"고 답해놓고 `cross_project: true` 표시를 빠뜨리면 횡단 학습이 누락된다

---

# 7. 에이전트 간 인사이트 참조

## 7.1 목적

에이전트가 다른 에이전트의 정보를 참조해야 할 때, 책임 경계를 명확히 하고 해석 권한이 섞이지 않도록 한다.

## 7.2 원칙: synthesis/playbook만 참조

에이전트 A가 에이전트 B의 데이터를 참조해야 할 때, A는 B의 원본(raw/, cycles/, insights/)을 직접 읽지 않고, B가 정기적으로 박제한 synthesis/playbook 페이지만 읽는다.

이유:
- 각 에이전트가 자기 영역의 해석 권한 유지
- 인터페이스가 명확해서 책임 추적 가능
- B의 원본 구조 변경이 A에 영향을 주지 않음

### 참조 관계 vs 공급 관계

§7.2는 참조 관계(학습 인용)에만 적용된다 — synthesis/playbook만, 금지 대상은 B의 raw/cycles/insights(내부 학습물).

이와 별개로 공급 관계(data→content→marketing 파이프라인)가 있다. 다운스트림은 업스트림의 outputs/approved/(공개 납품물)를 직접 읽는다. 이는 §7.2 금지 대상이 아니다 — approved는 결재를 거쳐 타 에이전트에 넘기려고 공개한 산출물이기 때문.

- 참조 관계: synthesis/playbook만 (학습 인용)
- 공급 관계: outputs/approved 직접 (재료 수급)
- 추적: 공급 시 다운스트림 cycle의 inputs에 사용한 approved 항목 기록. 업스트림 output은 source_cycle로 자기 cycle을 가리킴.

## 7.3 예외: 정찰 위탁(B-J) 시 한정 권한

content가 다른 에이전트의 정찰을 위탁받는 사이클(트리거 B-J)에 한해, content는 의뢰 에이전트의 raw/cycles 읽기 권한을 가진다.

조건:
- 위탁 사이클 범위 내에서만 유효
- 정찰 결과는 의뢰 에이전트 영역이 아닌 content 본인의 J 사이클에 박제
- 의뢰 에이전트는 정찰 결과를 인용/링크만

## 7.4 sales 정기 산출물

sales는 marketing이 참조할 수 있도록 전환 분석 리포트를 정기 박제한다.

- 파일: sales/cadam/syntheses/synthesis-conversion-report-YYYYMM.md
- 주기: 월 1회
- 내용: 주제별 전환율 표, 추천 주제 / 비추천 주제

marketing은 Tier 판정의 Q4(전환력)에서 최신 리포트만 참조한다:
- 리포트에 추천 주제로 있으면 → Q4 가산점
- 리포트에 비추천 주제로 있으면 → Q4 감점
- 리포트에 언급 없으면 → Q4 중립
- 리포트 부재 또는 30일 이상 경과 → "리포트 부재" 명시, Q4 중립

## 7.5 자율 발굴 영역

각 에이전트의 자율 발굴 영역 매트릭스는 _shared/scout-territories.md에 단일 진실로 박제한다. 각 에이전트 SKILL.md에는 자기 부분만 발췌·참조한다.

## 7.6 후속 작업 (이번 세션 미반영)

다음 두 파일은 §7과 함께 갱신하기로 했으나 별도 작업으로 남긴다:
- boundary-rules.md: marketing ↔ sales 경계 (노출까지 / 클릭 이후)
- sales SKILL.md: synthesis-conversion-report-YYYYMM 정기 산출물 추가 (월 1회)

## 7.7 폐기 기록

옵션 가/나/다(다른 합의안)는 폐기됨. 라(synthesis만 참조)만 살아 있음.

---

# 8. 위임 프레임워크 적용

작업을 어떤 도구에 맡길지 5가지 질문(정답 명확성·안전성·반복성·비창의성·검증 가능성)의 Yes 개수로 판단한다(5=위임 OK / 4=검토 후 / 3이하=Claude 직접). **위험신호(결제·리드·고객 응대·SEO·법적 영향) 5종은 Yes 개수와 무관하게 위임 금지.** §0.2 자가수정 금지는 위임 여부와 무관하게 유지. 통과 기준 표·위임 대상(Ollama/Groq/n8n)·참조 파일·주의사항 상세는 [_shared/ref-delegation.md](_shared/ref-delegation.md) 참조.

---

# 9. 사이클 생애주기

상태 흐름: started → in-progress → completed → measured → archived (각 전이는 §5 워크플로우 해당 단계 완료 전제). 중도 취소 시 `status=cancelled` + `cancel-reason` 필수. cycle_kind 5종(regular/batch/audit/adhoc/builder), 자율 발굴 두 층(정찰↔정식 분리), initiative 단위 상세는 [_shared/ref-cycle-lifecycle.md](_shared/ref-cycle-lifecycle.md) 참조.

---

# 10. 민감정보 처리

이 섹션은 vault에 저장해도 되는 정보와 저장해서는 안 되는 정보의 기준을 정의한다.

## 10.1 절대 저장 금지

아래 항목은 vault 어디에도 저장하지 않는다. 요약·마스킹 여부 무관.

- 비밀번호 (서비스 로그인, DB, API 게이트웨이)
- API 키 / 토큰 / 시크릿 (Supabase, OpenAI, Vercel, GitHub 등)
- 고객 개인정보 (실명, 연락처, 이메일, 차량번호 등)
- 매출 절대액 (특정 거래 단위 또는 월·연 매출 총액)

## 10.2 마스킹 후 저장 가능

아래 형태로 변환한 뒤에는 학습 노트에 포함할 수 있다.

- 가격 범위 (예: "30~50만 원대" — 구체 금액 아님)
- 트렌드 비율 (예: "전월 대비 +12%" — 절대액 미포함)
- 익명화 사례 (특정 고객 식별 불가 수준으로 가공)

## 10.3 GitHub 푸시 전 lint

vault 커밋·푸시 전 민감정보 패턴 포함 파일이 없는지 확인한다.

- 점검 대상: `*.md`, `*.yaml`, `*.json` (vault 내 모든 텍스트 파일)
- 점검 명령: `grep -r "sk-\|eyJ\|ghp_\|supabase\|password" . --include="*.md" -l`
- 위반 발견 시: 해당 파일 수정 → 재점검 → 커밋 진행

## 10.4 로컬 민감정보 보관소

vault 외부에 민감정보를 보관할 경우 `.cadam-secrets/` 디렉토리를 사용한다.

- 위치: `~/projects/_meta/agents/.cadam-secrets/` (로컬 전용)
- 현재 상태: 폴더 미생성, `agents/.gitignore` 패턴 미등록
- **별도 작업 필요**: `agents/.gitignore`에 `.cadam-secrets/` 패턴 추가 후 사용

---

# 11. index.md 형식

각 에이전트 `wiki/index.md`는 그 에이전트의 학습 단일 진실 소스(사이클 시작 시 첫 진입점, 종료 시 갱신)다. 운영 원칙·프론트매터·섹션 구조 7종(진행중 사이클/Playbooks/Insights/Syntheses/Failures/Entities&Concepts/Refs)·scope 분리·Tier 표기·갱신 시점 상세는 [_shared/ref-index-format.md](_shared/ref-index-format.md) 참조.

---

# 12. log.md 형식

각 에이전트 `wiki/log.md`는 그 에이전트의 시간순 변경 기록(append-only, 최신이 위로)이다. 운영 원칙·프론트매터·엔트리 양식·타입 8종(cycle-start/cycle-end/insight-promotion/synthesis/playbook-promotion/skill-promotion/lint/update)·보존 규칙 상세는 [_shared/ref-log-format.md](_shared/ref-log-format.md) 참조.

---

# 13. 안전 규칙

이 섹션은 vault 운영 시 지켜야 할 **불변 원칙**과, 위임 관련 **상세 규칙 파일의 인덱스**를 제공한다.

## 13.1 vault 운영 5대 원칙

1. **raw 불변 원칙** — `data/raw/` 하위 파일은 수정·삭제 금지. 가공은 `processed/`로 복사 후.
2. **wiki 수정 전 한국어 이유 명시** — `wiki/index.md` / `wiki/log.md` 변경 전 사유를 한국어로 먼저 기록.
3. **자가수정 금지** — 에이전트는 자기 `SKILL.md` / `wiki/` / `CLAUDE.md`를 수정 못 함 (§0.2).
4. **5+ 변경 시 사전 공유** — 한 번에 5개 이상 변경 시 실행 전 변경 목록 공유 + 합의.
5. **삭제 시 로그 기록** — 모든 삭제는 `wiki/log.md`에 일자·대상·사유 기록.

## 13.2 위임 안전 규칙 (3계층)

위임 가능 여부는 아래 3개 파일에서 정의된다. 모호하면 항상 **더 보수적인 쪽**을 따른다.

| 계층 | 파일 | 줄수 | 내용 |
|------|------|------|------|
| 절대 금지 | [`_shared/security/delegation-blacklist.md`](_shared/security/delegation-blacklist.md) | 28 | DB 파괴 / 고객·리드 데이터 / 파일·환경 / 외부 실거래 |
| 사전 승인 | [`_shared/security/approval-required.md`](_shared/security/approval-required.md) | 51 | 마스터 데이터 / 차량 이미지 본 컬럼 / 콘텐츠 발행 / 대량 작업 / 버전 관리 / 승인 메시지 형식 |
| 자동 허용 | [`_shared/security/auto-allowed.md`](_shared/security/auto-allowed.md) | 26 | 데이터 수집 / 결과 저장 / 알림 / 이미지 처리 |

판단 순서:
1. blacklist 해당? → 중단
2. approval-required 해당? → 사용자 승인 대기
3. auto-allowed 해당? → 자동 실행

## 13.3 수정 체크리스트

CLAUDE.md / SKILL.md / 핵심 양식 파일을 수정할 때는 [`_shared/modification-checklist.md`](_shared/modification-checklist.md)를 따른다.

## 13.4 위반 시 처리

위 원칙 위반 (또는 위반 의심) 시: 즉시 중단 → 해당 에이전트 `wiki/log.md`에 기록 → 사용자 보고 후 복구 합의.

---

# 14. Obsidian 호환

vault는 Obsidian으로 열어 그래프뷰·Dataview·백링크를 쓴다. 링크 양식(위키링크 vs 마크다운 링크)·콜아웃 문법·프론트매터(YAML)·이미지 참조 4가지 양식 상세는 [_shared/ref-obsidian.md](_shared/ref-obsidian.md) 참조.

---

# 15. 에이전트별 특화 규칙

이 CLAUDE.md는 vault 공통 규칙이다.
에이전트별 업무 프로세스·산출물·KPI·경계는 각 `{에이전트}/SKILL.md` 참조.

자율 발굴 영역 정의는 `_shared/scout-territories.md` 참조.
에이전트 간 경계는 `_shared/boundary-rules.md` 참조.
