---
project: rentailor
session: /info 캐러셀 UX 개선 + 카드뉴스 진단
date: 2026-05-24
status: 완료, 다음 세션 인계
---

# 핸드오프: /info 캐러셀 UX 개선 + 카드뉴스 진단 완료

## 이번 세션 완료 사항

### 1. /info 탭 → 세로 스크롤 + 앵커 네비 전환 (이전 세션, 유지)

**섹션 순서**: 아티클 → 카드뉴스 → 클립 → 약관비교  
`InfoSectionNav.tsx`: `sticky top-[52px] z-30`, `IntersectionObserver` 기반 active 감지  
URL params(`?tab=xxx`) → 앵커 스크롤 변환 유지

---

### 2. 캐러셀 dot indicator 추가

- `HorizontalScroll`에 dot indicator 추가 (약관비교 `TermsComparisonCards`와 동일 디자인)
- 스타일: `flex justify-center gap-1.5 pb-4` / `w-1.5 h-1.5 rounded-full transition-all` / active: `bg-primary w-4`
- `articles.length > 1` 조건일 때만 표시 (1개이면 숨김)
- dot 클릭 → 해당 카드 scrollTo, activeIdx 연동
- 아티클 / 카드뉴스 / 클립 3개 섹션 모두 적용

---

### 3. 아티클 이미지 제목 오버레이

- `HorizontalScroll`에 `showTitleOverlay` prop 추가, 아티클 섹션만 `true`
- 이미지 하단 그라데이션: `bg-gradient-to-t from-black/70 via-black/30 to-transparent`
- 제목: `text-white font-semibold text-lg md:text-xl line-clamp-2 absolute bottom-0`
- 카드뉴스(인포그래픽 자체가 콘텐츠), 클립(영상 썸네일) 제외

---

### 4. 카드뉴스 반응형 다중 표시

- `HorizontalScroll`에 `multiCol` prop 추가, 카드뉴스 섹션만 `true`
- 카드 width: 모바일 `w-[min(90vw,632px)]` / 태블릿·PC `md:w-[calc(50%-6px)] lg:w-[calc(50%-6px)]`
- 모바일 1장 / 태블릿·PC 2장 (3장→2장, 가독성 우선)
- 컨테이너 `max-w-2xl` 통일 (다른 섹션과 동일 폭)
- dot indicator 카드 단위 11개 유지, 캐러셀 스크롤 정상
- `handleScroll`에서 카드 폭을 `el.children[0].offsetWidth`로 읽어 반응형 정확도 개선

---

### 5. WP perPage 50으로 증가

- `src/app/info/page.tsx`: `fetchWpPosts()` → `fetchWpPosts({ perPage: 50 })`
- `src/app/api/info-articles/route.ts`: 동일하게 변경
- 카드뉴스 DB 11개 정상 노출 확인
- **"카드뉴스 1개만 보임" 이슈는 모바일에서 dot/버튼 없어서 착각한 것** — 실제 콘텐츠 부재 없음

---

### 6. 카드뉴스 DB 11개 진단 결과 (이번 세션 완료)

| 항목 | 결과 |
|------|------|
| DB 카드뉴스 게시물 수 | 11개, 전체 `is_active=true` |
| WP 동기화 | wp-sync LaunchAgent 정상 (1시간 주기, 오늘 06:00 완료) |
| 원인 | 콘텐츠 부재 아님 — 모바일 UX(dot 없음)로 인한 착각 |

---

## 현재 파일 상태

| 파일 | 역할 | 상태 |
|------|------|------|
| `src/components/info/InfoSectionNav.tsx` | sticky 앵커 네비 | 유지 |
| `src/components/info/InfoArticles.tsx` | dot indicator + 오버레이 + multiCol | 수정 완료 |
| `src/components/info/CarouselNavButtons.tsx` | 공통 좌우 네비 버튼 | 유지 |
| `src/components/info/TermsComparisonCards.tsx` | 약관비교 카드 캐러셀 | 유지 |
| `src/components/info/TermsComparisonTable.tsx` | 약관비교 표 (구버전) | 롤백 대비 유지 |
| `src/app/info/page.tsx` | perPage 50 | 수정 완료 |
| `src/app/api/info-articles/route.ts` | perPage 50 | 수정 완료 |

백업 파일: `InfoArticles.tsx.bak`, `.bak3`, `.bak4`, `.bak5`, `.bak6`, `.bak7`

---

### 7. 약관비교 카드 내부 레이아웃: 그리드 → 세로 리스트

- 기존: `grid grid-cols-1 sm:grid-cols-2` 회사별 박스 그리드
- 변경: `flex items-start` 회사명/조건 1:1 가로 정렬 세로 리스트
- 회사명: `w-24 md:w-32 font-semibold text-primary`(고정 폭)
- 조건: `flex-1`, `getCellClass()` 유지 (미기재=회색 이탤릭)
- 행 구분: `border-b border-gray-100 last:border-b-0`
- 회사 간 비교 용이성 개선, 커밋: `71ef416`

---

## 다음 세션 후보

현재 안정 상태. 추가 UX 개선이 필요하면:
- 클립 섹션 dot indicator 디자인 재검토 (현재 클립 데이터 0개)
- 아티클 오버레이 폰트 크기 모바일 가독성 점검

---

## 배포 정보
- 리포: `github.com/iori21y-ops/cadam.git` (branch: main)
- 커밋: `0ff2cb6` feat(info): 캐러셀 dot indicator + 아티클 제목 오버레이 + 카드뉴스 반응형
- 배포: `https://www.rentailor.co.kr` (2026-05-24)
