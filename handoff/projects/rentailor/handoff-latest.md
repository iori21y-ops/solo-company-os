---
project: rentailor
session: /info 페이지 컨테이너 너비 통일 + PC 좌우 네비 버튼 + 약관비교 transpose
date: 2026-05-24
status: 완료, 다음 세션 인계
---

# 핸드오프: /info 페이지 UI 개선 완료 → 약관비교 카드화

## 이번 세션 완료 사항

### 1. 이미지 컨테이너 너비 수정
- 원인: `HorizontalScroll` / `ClipsHorizontal` outer div에 max-width 없어서 스크롤 영역이 뷰포트 전체 폭으로 확장
- 수정: outer div에 `max-w-3xl mx-auto w-full` 추가
- 파일: `InfoArticles.tsx`, `InfoClips.tsx`

### 2. 약관비교 표 transpose + sticky
- 행↔열 전환: 회사 기준 행 → 조건항목 기준 행
- 조건항목 열 sticky left + `shadow-[2px_0_4px_rgba(0,0,0,0.05)]` + 교번 배경색
- 파일: `TermsComparisonTable.tsx`

### 3. 전체 너비 홈탭(max-w-2xl = 672px)과 통일
- 홈(/), NavBar 모두 `max-w-2xl` 확인 후 /info도 동일하게 맞춤
- `max-w-3xl` → `max-w-2xl` (InfoArticles, InfoClips, TermsComparisonTable)
- 카드 너비: `w-[min(90vw,760px)]` → `w-[min(90vw,632px)]` (peek 효과 확보)
- 카드뉴스 이미지: `object-cover` → `object-contain` (세로형 잘림 방지)

### 4. PC 좌우 네비게이션 버튼 (아티클/클립/카드뉴스)
- `md:` 이상에서만 표시 (모바일 기존 스와이프 유지)
- `ChevronLeft` / `ChevronRight` (lucide-react)
- 첫/마지막 항목 비활성화 (opacity-30, cursor-not-allowed)
- `goTo(index)` 함수: `card.offsetLeft - 20` 기반 smooth scroll
- 내부 `activeIdx` state 관리 (부모 `onActiveChange`도 동시 호출)
- 약관비교 탭은 미적용 (다음 세션 카드화 시 추가 예정)

---

## 현재 파일 상태

| 파일 | 현재 max-w | 비고 |
|------|-----------|------|
| `src/components/info/InfoArticles.tsx` | max-w-2xl | ChevronLeft/Right import, HorizontalScroll+ClipsHorizontal 버튼 포함 |
| `src/components/info/InfoClips.tsx` | max-w-2xl | 동일 패턴 |
| `src/components/info/TermsComparisonTable.tsx` | max-w-2xl | transpose 완료, 좌우 버튼 없음 |

---

## 다음 세션 작업: 약관비교 탭 카드화

### 목표
약관비교를 현재 가로 스크롤 테이블에서 카드 형태로 전환

### 결정 필요 사항 (세션 시작 시 사용자에게 물어볼 것)

**Q1. 카드 기준 선택**
- **옵션 A: 조건항목별 카드** — 카드 1장 = "중도해지 위약금" 조건. 카드 안에 회사별 값 나열. 좌우 스와이프 = 다음 조건항목
- **옵션 B: 회사별 카드** — 카드 1장 = "KB캐피탈". 카드 안에 조건항목별 값 나열. 좌우 스와이프 = 다음 회사
- **옵션 C: 표+카드 토글** — 기존 테이블 + 카드 형태 토글 버튼

**Q2. 기존 테이블 유지 여부** (완전 대체 vs 토글)

### 현재 데이터 구조 (TermsComparisonTable.tsx 내 하드코딩)
```
RENTAL_DATA: 5개사 × 7개 조건항목
  - KB캐피탈, 신한카드, 하나캐피탈, 현대캐피탈, 아마존렌터카
  - 중도해지/규정손해/초과운행/만기처리/승계수수료/지연배상금/반환차량상태

LEASE_DATA: 7개사 × 6개 조건항목
  - KB캐피탈, 신한카드(표준), 신한카드(개별), 롯데오토리스, 우리카드, 롯데캐피탈, MG캐피탈
  - 중도해지/규정손해/초과운행/반환지연금/승계수수료/지연배상금
```

### 구현 시 참고
- `HorizontalScroll` 패턴 재사용 가능 (이미 max-w-2xl + prev/next 버튼 완성)
- PC 좌우 버튼도 동일 패턴으로 추가
- `TermsComparisonTable.tsx` 단일 파일에서 모두 처리 가능

---

## 배포 정보
- 리포: `github.com/iori21y-ops/cadam.git` (branch: main)
- 배포: `npx vercel --prod` (수동, GitHub Actions 미연동)
- 최신 배포: `https://www.rentailor.co.kr` (2026-05-24 완료)
