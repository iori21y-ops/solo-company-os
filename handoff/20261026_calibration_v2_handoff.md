# 핸드오프 — 리스·렌트 교정식 v2 + 차즘 만원 반올림 표기 (2026-10-26)

> **2026-10-26 갱신**: 이 핸드오프의 '다음 작업'(차즘 만원 반올림 표기)과 전환 순서는 `~/projects/cadam/docs/reports/pricing_consolidated_20261026.md`로 통합·대체됨(화물차 렌트 불가·테슬라 가격 반영, 웹 통합 브랜치 `pricing-integration`).


## 현재 상태 (사실)
- **v1 교정식은 프로덕션 적용 완료** (2026-10-25): DB `finance_calibration` `chazm-2026-10-24-v1-min` 활성, pricing 7,416행 재생성, cadam-web `d1ee39e` 배포. 기준=금융사 최저, 노출 86종 표시값 약 −22%.
- **v2 구현 완료, 아직 아무것도 실행/배포 안 함** (로컬 커밋만):
  - cadam-web: 브랜치 `calibration-v2` (커밋 `bdc50e3`, main 기준 `9b820a9`) — `calc-monthly.ts`·`display-price.ts`·호출부 5곳(slug 전달). 패치 백업 `backups-manual/calibration_v2_web_20261026.patch`. main 작업 폴더에는 반영 안 함(다른 세션이 push하면 즉시 배포되기 때문).
  - cadam-n8n: main 로컬 커밋 `e3d41c7` (`generate_pricing.py` v2 + `--calibration-version`). v1 행 기준 결과가 이전 코드와 2160/2160 동일하므로 디스크 반영 상태로 두어도 안전.
  - cadam-doc: 로컬 커밋 `87634bd` (분석서·설계서·SQL `supabase/20261026_finance_calibration_v2*.sql`). **푸시 안 함**.
  - DB v2 행(`chazm-2026-10-26-v2-min`): **INSERT 안 함**. 값 JSON `backups-manual/calibration_v2_params_row_20261026.json`.
- v2 내용: 렌트 = (PMT×1.05) + 고정 10만원, 전기차 17종 보조금 차감, 테슬라 렌트 +4.13%p·리스 −0.56%p, BMW i −1.92%p. 효과(렌트 평균절대오차): 전체 11.5→7.3%, EV 17.1→9.9%, 경차 30.8→14.1%. 노출 86종 표시값 v1 대비 중앙 +1.9%(−17%~+37%).
- 검증 완료: TS↔파이썬 600조합 일치, 86종 표 재현 86/86, v1 형식 파라미터 이전 코드와 600/600·파이썬 2160/2160 동일, 월액→신차가 역산 한계 이내, tsc 0 오류.

## v2 전환 순서 (각 단계 사용자 승인 필요)
1. 백업(pricing·finance_calibration 덤프) + 다른 세션 push 여부 확인
2. DB: `20261026_finance_calibration_v2.sql` 실행 (v2 행 비활성 INSERT)
3. `python3 generate_pricing.py --all --calibration-version chazm-2026-10-26-v2-min` (pricing v2 선재생성; 목록은 캐시 만료 후 v2)
4. **바로** `calibration-v2` 브랜치를 main에 반영 → push (새 코드는 `model_version` 없는 DB v1 행을 무시하고 내장 v2 사용)
5. 배포 Ready 후 86종·상세·진단 계산기 검증
6. DB 전환(한 트랜잭션): v1 `is_active=false` → v2 `is_active=true`
7. docs 반영 + cadam-doc push(Notion 동기화; 이제 워크플로 fetch-depth 0 수정됨)
롤백: v1 행 재활성 + `generate_pricing.py --all` + 웹 revert. 전환 사고 전례: 다른 세션 push가 데이터 준비 전에 교정식을 배포한 적 있음(2026-10-25 16:14).

## 다음 작업: "차즘 데이터 만원 반올림 표기" 선택지 (미착수)
사용자 결정(2026-10-26): ① **운영자 설정 스위치**로 선택('보정 예상가' / '차즘 만원 반올림') ② **구현 후 바로 켜기**(차즘 동의 메일 미발송 — 약관 제10조 8호 위험은 고지함. 켜는 배포는 단계별 승인).
조사 결과(설계 입력):
- 사이트에 기존 "가격 표기 선택" 기능 없음 → 설정 저장소(예: 작은 설정 테이블/플래그)·ERP 또는 관리자 토글을 새로 만들어야 함.
- 차즘 렌트 60개월·1만km·무보증 견적과 신차가가 **정확히 일치하는 트림은 사이트 379트림 중 126개(33%)**. 차종 단위로는 86종 중 66종에 차즘 렌트 견적이 있고(20종 없음: bmw-i, casper-ev, ev3-gt/ev4-gt/ev5-gt, filante, g70-sb, g80ev, grand-koleos-hybrid, gv70ev, kona-ev, musso, musso-ev, niro, rexton-summit, sonata-the-edge(+hybrid), tivoli-turbo, torres-van, arkana-gasoline — 이름 매칭 실패 포함), 차종 최저가 트림이 일치하는 차종은 57종.
- 따라서 트림별이 아니라 **차종 단위 "시장 최저 시작가"**(차즘 렌트 60개월·1만km·무보증, 차종 최저 월 납입금 → 만원 반올림)를 목록 카드·상세 헤더·비슷한 차종에 쓰고, 데이터 없는 차종은 보정 예상가로 폴백하는 설계가 현실적. 트림 카드(상세)는 예상가 유지 시 헤더와 어긋나므로 처리 방침(헤더만 시장가 / 트림도 비율 환산 / 시장가 모드에서는 트림 카드 비노출) 결정 필요.
- 저장 제안: `market_rent_refs(slug, monthly_manwon, as_of, source)` — 만원 반올림 값만 저장(원 단위 원본·금융사·트림명 미저장), RLS는 서버(service_role) 전용 읽기. 적재는 로컬 `cadam-n8n/price_crawler/data/chazm/*.jsonl` 기반 스크립트.
- 라벨/출처 표기(예: "시장 최저 참고가")·기준일 노출 여부는 미정 — 출처 표기가 분쟁 위험을 낮춘다는 이전 권고 있음.

## 주의
- cadam-web은 push=즉시 배포. 다른 세션 push가 로컬 커밋을 함께 올림 → 가격 관련 변경은 `calibration-v2` 브랜치에 두고 순서대로 반영.
- 이 문서·메모리 외 상세: `rental_param_v2_design_20261026.md`, `pricing_cutover_runbook_20261025.md`, `docs/web-detail.md` 2026-10-25 섹션.
