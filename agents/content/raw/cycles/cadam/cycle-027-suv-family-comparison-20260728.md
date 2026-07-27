---
title: "우선순위1·3 팩트블록 위탁 처리 — 2026-07-28"
type: cycle
status: done
created: 2026-07-28
cycle_id: "027"
agent: content
project: cadam
cycle_kind: factblock
trigger_source: marketing (CONTENT-20260727-0005, 07-06 확정 발행계획 우선순위1·3, 21일 지연분)
channel: task-ledger:internal
inputs:
  - marketing/outputs/approved/topic-scout-tier-20260706.md (확정 발행계획 우선순위1·3)
  - data/outputs/approved/verdict-santafe-20260611.md (green, quantitative)
  - data/outputs/approved/verdict-sorento-20260611.md (green, quantitative)
  - data/outputs/approved/verdict-palisade-20260611.md (green, quantitative)
  - data/outputs/approved/verdict-sportage-20260611.md (green, quantitative)
  - data/outputs/approved/proposal-renttailor-newdata-20260608.md (렌탈료 계산 입력 미검증 근거)
  - data/outputs/approved/decision-msrp-source-consolidation-20260713.md (가격 파이프라인 현황)
  - supabase: vehicle_powertrains, vehicles (직접 조회, 2026-07-28)
related_assets:
  - content/outputs/pending/factblock-suv-family-quant-20260728.md
---

# cycle-027 — 우선순위1·3 팩트블록 위탁 처리 (2026-07-28)

## 배경
마케팅 07-06 확정 발행계획(topic-scout-tier-20260706) 우선순위1(아반떼 장기렌트 월 납입금)·우선순위3(SUV 가족차 장기렌트 비교) 팩트블록 위탁이 21일 지연 상태.
index.md 07-06/07-13 갱신 로그에 이미 "rental_prices/finance_rates 미검증(전역 디폴트)"로 우선순위1·3 게이트 보류 기록 존재.

## 처리
1. **우선순위3 (SUV 가족차 비교)**: 가격 수치 없이도 verdict green(quantitative) 커버 범위(연비·CO2·공차중량·구동방식·휠) 만으로 비교 콘텐츠 성립 가능 판단 → Supabase `vehicle_powertrains`/`vehicles` 직접 조회(2026-07-28)로 santafe·sorento·palisade·sportage 4종 대표 트림 수치 확보 → `factblock-suv-family-quant-20260728.md` 작성, `outputs/pending/` 등록.
2. **우선순위1 (아반떼 월 납입금)**: 토픽 자체가 렌탈 월 납입금(가격) 수치를 요구하나, `rental_prices`(5건 샘플 벤치마크, source=null)·`finance_rates`(전역 디폴트 1세트)는 07-28 현재도 verdict 없음(2026-06-08 proposal 이후 미해소, decision-msrp-source-consolidation-20260713도 별건). 가격 없는 아반떼 팩트블록은 이미 approved인 `factblock-avante-visual-complete-20260609.md`와 중복 → 신규 산출물 없음. 대표님 결정 필요 사항으로 에스컬레이트.

## 부가 발견
`assets/cadam/index.md`에 2026-06-18~07-06 사이 등록된 `factblock-*-quant-*.md` 배치 항목 약 40건이 실제 파일로 존재하지 않음(outputs/pending, outputs/approved, assets 어디에도 없음; git 삭제 이력도 없음 — 애초에 파일 생성 없이 인덱스 행만 기록된 것으로 추정). `content/raw/cycles/cadam/`도 `.gitkeep`만 존재해 프론트매터가 참조하는 cycle 파일들이 실제로는 없었음. 별도 보고.

## 학습 추출
- 가격(월 납입금) 요청 토픽은 착수 전 rental_prices/finance_rates verdict 여부부터 확인 — 스펙만으로 대체 불가능한 토픽은 제작 자체가 불가하므로 조기 에스컬레이트가 맞음.
- index.md 등록 = 실제 파일 존재를 의미하지 않았던 과거 관행 확인. 이번 cycle부터 등록 전 파일 존재 확인을 선행.
