---
title: 핸드오프 시스템
last-updated: 2026-05-22
---

# 핸드오프 시스템

## 목적
세션 간 컨텍스트 손실 없이 작업을 이어가기 위한 문서 시스템.

## 원칙
- 한 세션 = 한 파트(작업 단위)
- 핸드오프 본문 200자 이내
- 영구 사항은 채팅 클로드 메모리에 박제
- 상세 결정은 DECISIONS.md에 박제
- 새 세션은 ⌘V 한 번으로 시작

## 구조
~/projects/_meta/handoff/
├── README.md                    (이 파일)
├── template-short.md            (200자 핸드오프 템플릿)
├── template-full.md             (전체 핸드오프 7단계 템플릿)
└── projects/
    ├── rentailor/
    │   ├── DECISIONS.md         (누적 결정사항)
    │   ├── current-state.md     (현재 진행 상태)
    │   └── handoff-latest.md    (마지막 핸드오프, ⌘V 대상)
    └── (다른 프로젝트들)

## 사용법
### 세션 종료 시
1. 채팅 클로드에 "세션 마무리해줘" 입력
2. 클로드가 출력하는 클코 명령어를 클코에 붙여넣기
3. 클코가 3개 파일 갱신 + pbcopy 자동 실행

### 새 세션 시작 시
1. 새 채팅에서 ⌘V (유니버설 클립보드로 아이폰에서도 가능)
2. 클로드가 메모리 + 핸드오프로 즉시 컨텍스트 잡음

<!-- SECTION:START name=files_in_this_area -->
## 이 영역의 파일 지도

| 파일 | raw URL | 용도 |
|------|---------|------|
| `handoff/README.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/handoff/README.md) | 인덱스 — 여기 |
| `handoff/template-short.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/handoff/template-short.md) | 200자 핸드오프 템플릿 (일반 세션용) |
| `handoff/template-full.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/handoff/template-full.md) | 7단계 전체 템플릿 (큰 맥락 변화·복귀용) |
| `handoff/templates/self-contained.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/handoff/templates/self-contained.md) | 자급자족 템플릿 (모바일 ⌘V용) |
| `handoff/LOCAL-ONLY.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/handoff/LOCAL-ONLY.md) | 공개/비공개 분리 원칙 |
| `handoff/PUBLIC-POLICY.md` | [링크](https://raw.githubusercontent.com/iori21y-ops/solo-company-os/main/handoff/PUBLIC-POLICY.md) | 공개/비공개 구분 + 금지 패턴 + 자가 점검 |
| `handoff/projects/` | gitignore | 프로젝트별 핸드오프 — 로컬 전용 |
<!-- SECTION:END name=files_in_this_area -->
