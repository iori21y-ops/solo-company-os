---
title: "참조 — log.md 형식"
type: reference
status: active
source: "CLAUDE.md §12에서 분리 (2026-06-02)"
---

# log.md 형식 (CLAUDE.md §12 상세)

각 에이전트 vault의 `wiki/log.md` 는 **그 에이전트의 시간순 변경 기록**이다.
append-only, 최신이 위로.

## 12.1 운영 원칙

- 위치: `{agent}/wiki/log.md` (9개 에이전트 각각 1개)
- 갱신 주체: 에이전트 본인
- 갱신 방식: append-only (기존 엔트리 수정 금지, 최신을 맨 위에 추가)
- 모든 wiki 변경은 log에 1엔트리 이상 남긴다

## 12.2 프론트매터

```yaml
---
title: "{agent} 에이전트 wiki 변경 로그"
type: log
status: active
created: YYYY-MM-DD
agent: {agent}
---
```

## 12.3 엔트리 양식

```markdown
## [YYYY-MM-DD] 타입 | 한 줄 제목
요약 2~3줄. 무엇을 왜 변경했는지.
영향받은 페이지: [[페이지1]], [[페이지2]], ...
```

- 날짜는 KST 기준
- 타입은 §12.4의 8종 중 하나
- 영향받은 페이지는 위키링크로 명시

## 12.4 타입 8종

| 타입 | 의미 |
|------|------|
| `cycle-start` | 사이클 시작 |
| `cycle-end` | 사이클 종료 (산출물 박제 포함) |
| `insight-promotion` | insight status 변경 (pending → confirmed/rejected) |
| `synthesis` | 횡단 분석 생성 |
| `playbook-promotion` | playbook Tier 승격/강등 |
| `skill-promotion` | 프로젝트 학습 → _skill 직무 학습 승격 |
| `lint` | 모순·고아·누락·오래됨 점검 |
| `update` | 기타 수정 (양식 변경, 오타 수정 등) |

## 12.5 영향받은 페이지 표기

- 위키링크 `[[]]` 사용
- 풀 경로 또는 슬러그만 (옵시디언이 해결)
- 2개 이상이면 쉼표로 구분
- 인덱스 갱신 포함 시 `[[index]]` 명시

## 12.6 보존 기간

영구 보존. 삭제 금지. 자동 정리 대상 아님.

오래된 엔트리는 별도 `log-archive-YYYY.md` 로 이관 가능 (선택사항).
