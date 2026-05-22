# 공개/비공개 분리 원칙

## 공개 (GitHub 포함)
- `handoff/README.md` — 핸드오프 시스템 설명
- `handoff/template-short.md` — 200자 템플릿
- `handoff/template-full.md` — 7단계 전체 템플릿
- `handoff/templates/` — 자급자족 등 범용 템플릿

## 로컬 전용 (.gitignore 처리됨)
- `handoff/projects/` — 프로젝트별 핸드오프 전체
  - 이유: Tailscale IP, Supabase ref 등 식별자 포함
  - 이유: 진행 중 사업 디테일 포함

## 동일 원칙 — 다른 디렉토리
- `agents/` → 공개 (정의·구조·경계 규칙)
- `agents-private/` → .gitignore (사업별 디테일, 필요 시 생성)
- `delegation/` → 공개 예정 (위임 방법론)
- `delegation-private/` → .gitignore (필요 시 생성)
