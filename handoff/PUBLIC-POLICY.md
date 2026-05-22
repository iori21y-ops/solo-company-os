---
title: 핸드오프 공개 정책
last-updated: 2026-05-22
status: 활성
---

# 핸드오프 공개 정책

모바일 외부 접근을 위해 `handoff-latest.md`는 공개. 나머지는 비공개.

<!-- SECTION:START name=public_vs_private -->
## 공개 vs 비공개 구분

| 파일 | 공개 | 이유 |
|------|------|------|
| `handoff/projects/{name}/handoff-latest.md` | ✅ 공개 | 모바일 새 세션 페치용 |
| `handoff/projects/{name}/DECISIONS.md` | ❌ 비공개 | 장기 박제, 사업 디테일 누적 |
| `handoff/projects/{name}/current-state.md` | ❌ 비공개 | 인프라 식별자·상태 박스 |
| `handoff/projects/{name}/그외 모든 파일` | ❌ 비공개 | 기본값 차단 |

핵심: **`handoff-latest.md`만 공개. 다른 파일은 디폴트 비공개.**

<!-- SECTION:END name=public_vs_private -->

<!-- SECTION:START name=write_rules -->
## handoff-latest.md 작성 규칙

공개되므로 다음 정보는 **절대 박지 않음**:

### 🚫 금지 (자동 검출 대상)
- IP 주소 (특히 Tailscale `100.x.x.x`, 내부 `192.168.x.x`, `10.x.x.x`)
- API 키, 토큰, 시크릿
- DB 식별자 (Supabase ref, MongoDB URI, Redis 호스트)
- 외부 서비스 ID (시트 ID, 워크플로 ID, 카카오 앱 ID 등)
- 고객·딜러·파트너 식별 정보 (이름, 이메일, 전화)
- 매출·비용 구체 숫자
- 도메인 내부 경로 (관리자 URL 등)

### ✅ OK (공개 가능)
- 작업 맥락 ("9개 에이전트 시스템 쌍3 작업 중")
- 규칙·패턴 ("섹션 마커 str_replace 사용")
- 박제 위치 경로 (`~/projects/_meta/agents/`)
- 공개 인덱스 URL
- 다음 작업 요약

### ⚠️ 회색지대 (사람 판단)
- 프로젝트 이름 (랜테일러는 이미 공개되어 있어 OK)
- 기술 스택 (Next.js, Supabase 등 일반 정보)
- 디렉토리 구조 (민감 경로 아니면 OK)

<!-- SECTION:END name=write_rules -->

<!-- SECTION:START name=self_check -->
## 클코 자가 점검 체크리스트

handoff-latest.md 생성/갱신 시 클코는 다음을 자동 실행:

1. 작성 후 grep으로 금지 패턴 검출:
   - IP: `grep -E '\b(100|192\.168|10)\.[0-9]{1,3}\.[0-9]{1,3}'`
   - Supabase ref: `grep -E '[a-z]{20}\.supabase\.co'` 또는 ref 본체
   - 시트 ID: `grep -E '[a-zA-Z0-9_-]{40,}'` (긴 식별자)
   - 일반 토큰: `grep -iE '(token|key|secret|password)'`

2. 검출되면 즉시 사용자에게 알리고 푸시 중단

3. 통과하면 git add + commit + push 진행

<!-- SECTION:END name=self_check -->

<!-- SECTION:START name=violation_response -->
## 위반 사고 발생 시

이미 공개된 민감 정보 발견 시:

1. **즉시**: 해당 줄을 핸드오프에서 제거 + 커밋
2. **단**: git 히스토리에는 영구 박힘 → 식별자 자체를 회전(rotate)
   - API 키: 즉시 재발급
   - DB ref: 변경 어려움 → 대신 RLS 정책 강화 확인
   - IP: Tailscale은 노출 위험 낮음, 무시 가능
3. **재발 방지**: 어떤 정보가 어떻게 박혔는지 이 문서에 기록

<!-- SECTION:END name=violation_response -->
