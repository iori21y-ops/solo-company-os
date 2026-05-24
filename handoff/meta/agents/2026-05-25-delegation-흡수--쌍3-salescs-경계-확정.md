---
area: meta/agents
date: 2026-05-25
session: delegation 흡수 + 쌍3 sales↔cs 경계 확정
---
# 이어가는 중
5월 22~24일 솔로 운영 OS 구축의 연속. 이번 세션은 두 가지 큰 작업 완료.

# 완료한 것
1. delegation/ 폴더 완전 제거 (cadam)
   - 위임 도구 3종(template/workflow/security) → _meta/agents/_shared/ 로 흡수
   - WF-VI 자료 16개 → cadam/docs/wf-vi/ 로 이동 (inventory 10 + archive 5 + STATUS + pilot-vehicle-images)
   - 모든 이동은 git mv (히스토리 보존)
   - 양쪽 리포 commit + push 완료
2. 쌍3 sales↔cs 경계 확정 (대안1: 백오피스 vs 프론트)
   - 경계선: "이 산출물이 사람(고객·딜러)에게 직접 발송되는가?"
   - sales = 회계·분석실 (스코어링·ROI·KPI·CRM 정합성)
   - cs = 매장 직원 (1차 응대~체결 직전까지)
   - 사업모델 반영: 계약은 딜러↔고객 사이, 체결 후는 딜러 책임 → cs는 체결 전까지만
3. 4개 파일 갱신 완료
   - boundary-rules.md (쌍3 섹션 51줄 추가, 회색지대 14케이스)
   - sales/SKILL.md (스텁 → 전체 정의, 8섹션)
   - cs/SKILL.md (스텁 → 전체 정의, 8섹션)
   - README.md (4·5번 정의됨 승격, 경계 현황 갱신)
4. Claude 메모리 #24·#7 갱신

# 미해결 / 알려진 이슈
없음. 이번 세션은 깨끗하게 마감.

# 핵심 통찰
- delegation/ 흡수 시 단순 폴더 이동 아니라 SKILL.md의 "위임 등급" 섹션과 security 3단계를 매핑해야 살아있는 자원이 됨
- sales/cs 첫 안이 틀린 가설(계약 후 cs 응대)이었음. 사업모델(딜러 중개)을 다시 확인하니 깔끔해짐
- 경계 정의의 정석: 산출물이 다른가? 같으면 부서 분류, 다르면 직무 분류

# 다음 작업 (메타-에이전트)
남은 쌍 4개:
- 쌍4 ops ↔ data (가장 임박, 둘 다 데이터 다룸)
- 쌍5 strategy ↔ 전체 (수직 감독 관계)
- 쌍6 legal ↔ finance
- 추가: sales ↔ marketing 경계 (리드 유입 시점)
파트4(디스코드봇) + 파트5(학습루프) + 클코 실제구현은 모든 경계 확정 후

# 새 세션 시작 방법
- PC: 자동으로 클립보드 박힘 → ⌘V
- 모바일: 홈화면 "이어받기" → 에이전트 선택
