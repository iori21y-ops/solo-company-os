---
title: WF-VI-003 정합성 점검 Verdict
type: verdict
subject: wfvi-consistency
date: 2026-06-02
source_cycle: [[데이터/raw/cycles/wfvi/cycle-003-consistency-check]]
status: pending-approval
---

# WF-VI-003 4자 정합성 대조 Verdict

**점검일:** 2026-06-02  
**대상 4축:** vehicles DB (257건) ↔ VEHICLE_LIST (81건) ↔ public/cars (200 webp) ↔ car-images 버킷 (99건)

> **사전 메모:** 관리팀장 지시에서 VEHICLE_LIST를 "~42차종"으로 명시했으나, 실제 `src/constants/vehicles.ts` VEHICLE_LIST는 **81건**임을 먼저 확인. 서비스 브랜드(현대·기아·제네시스·르노코리아·KGM·테슬라) 전체 포함 수치이며, 이후 수치는 실측 기준.

---

## 1. 최종 Verdict 요약

| 대조 경로 | 결과 | 건수 | 판정 |
|---|---|---|---|
| VL → public/cars | 파일없음 | 0건 | 🟢 GREEN |
| VL → car-images 버킷 | 파일없음 | 0건 | 🟢 GREEN |
| VL → DB (slug 매칭) | 미등록 | 0건 | 🟢 GREEN |
| DB image_key 누락 (active) | null 차량 | 29건 | 🟡 YELLOW |
| DB image_key 불일치 (active) | 베이스 키 사용 | 8건 | 🟡 YELLOW |
| 고아자산 public/cars | VL 미참조 | 119건 | 🟡 YELLOW |
| 고아자산 car-images 버킷 | VL 미참조 | 18건 (1 sitemap) | 🟡 YELLOW |
| VEHICLE_LIST 중복 ID | kg12 중복 | 1건 | 🟠 ISSUE |

**사이트 표시 가용성:** 🟢 GREEN — 모든 VL 81건에 대해 public/cars 및 car-images 버킷 파일이 완전히 존재. 현재 사이트 차량 이미지 표시에 지장 없음.

---

## 2. 세부 대조 결과

### 2-A. VEHICLE_LIST 기준선

`src/constants/vehicles.ts` VEHICLE_LIST 실측 건수:

| 브랜드 | 건수 |
|---|---|
| 현대 | 25건 |
| 기아 | 27건 |
| 제네시스 | 10건 |
| 르노코리아 | 5건 |
| KGM | 11건 |
| 테슬라 | 3건 |
| **합계** | **81건** |

> ⚠️ 주석에 "KGM (12종)"으로 표기되어 있으나 실제는 11건. 아래 중복 ID 이슈와 연관.

---

### 2-B. VL → public/cars (200 webp)

- **VL 81건 전체에 대응하는 webp 파일 존재** ✓
- **파일없음: 0건** 🟢

VL 미참조 파일 (고아자산) **119건** — 수입 브랜드 이미지 및 일부 비활성 국산 차종:

**수입 브랜드 (VL 범위 밖, 향후 확장용으로 추정):**
Audi 13건, BMW 26건, Honda 2건, Jeep 2건, Land Rover 7건, Lexus 7건, Mercedes 21건, MINI 7건, Peugeot 3건, Porsche 9건, Toyota 6건, Volkswagen 5건, Volvo 6건 → **소계 114건**

**국산 브랜드 VL-미등록 파일 (비활성 또는 미출시):**
| 파일명 | DB 상태 | 비고 |
|---|---|---|
| hyundai-porter2-v2.webp | is_active=false | 포터 II |
| kia-bongo3-v2.webp | is_active=false | 봉고 III |
| kia-tasman-v2.webp | is_active=false | 타스만 |
| tesla-model-s-v2.webp | is_active=false | Model S |
| tesla-model-x-v2.webp | is_active=false | Model X |

**소계 5건**

---

### 2-C. VL → car-images 버킷 (99건)

- **VL 81건 전체에 대응하는 버킷 파일 존재** ✓
- **파일없음: 0건** 🟢

버킷 고아자산 **18건:**

| 파일명 | DB 상태 | 분류 |
|---|---|---|
| chevrolet-trailblazer-v2.webp | is_active=false | 비활성 차종 |
| chevrolet-trax-v2.webp | is_active=false | 비활성 차종 |
| hyundai-porter2-v2.webp | is_active=false | 비활성 차종 |
| hyundai-sonata-v2.webp | DB: 소나타(비활성) | 구형 소나타 |
| hyundai-sonata-hybrid-v2.webp | DB: 없음 | VL·DB 모두 미등록 |
| kgm-torres-evx-v2.webp | is_active=false | 비활성 차종 |
| kgm-torres-evx-van-v2.webp | is_active=false | 비활성 차종 |
| kia-bongo3-v2.webp | is_active=false | 비활성 차종 |
| kia-k3-v2.webp | is_active=false | 비활성 차종 |
| kia-stinger-v2.webp | DB: 없음 | VL·DB 모두 미등록 |
| kia-tasman-v2.webp | is_active=false | 비활성 차종 |
| renault-qm6-v2.webp | is_active=false | 비활성 차종 |
| renault-sm6-v2.webp | is_active=false | 비활성 차종 |
| renault-xm3-v2.webp | is_active=false | 비활성 차종 |
| renault-xm3-hybrid-v2.webp | DB: 없음 | VL·DB 모두 미등록 |
| tesla-model-s-v2.webp | is_active=false | 비활성 차종 |
| tesla-model-x-v2.webp | is_active=false | 비활성 차종 |
| sitemap | — | 폴더/잘못된 오브젝트 |

> ⚠️ `hyundai-sonata-hybrid-v2.webp`, `kia-stinger-v2.webp`, `renault-xm3-hybrid-v2.webp` 3건은 DB에도 없는 완전 미등록 고아자산.  
> ⚠️ `sitemap` 항목은 이미지 파일이 아닌 이상한 오브젝트로 확인 필요.

---

### 2-D. VL → DB 슬러그 대조

모든 VL 81건에 대해 DB에 동일한 slug 존재 확인. **미등록: 0건** 🟢

다만, DB `image_key` 컬럼 정합성 이슈 발견:

**① Active DB image_key=null (29건)** — VL에는 imageKey가 있으나 DB 미기입:

| slug | DB 브랜드 | VL imageKey |
|---|---|---|
| tivoli-turbo | KGM | kgm-tivoli-turbo-v2 |
| rexton | KGM | kgm-rexton-v2 |
| rexton-summit | KGM | kgm-rexton-summit-v2 |
| musso | KGM | kgm-musso-v2 |
| musso-ev | KGM | kgm-musso-ev-v2 |
| actyon | KGM | kgm-actyon-v2 |
| torres-van | KGM | kgm-torres-van-v2 |
| ev4-gt | 기아 | kia-ev4-gt-v2 |
| ev5 | 기아 | kia-ev5-v2 |
| ev5-gt | 기아 | kia-ev5-gt-v2 |
| niro | 기아 | kia-niro-v2 |
| niro-ev | 기아 | kia-niro-ev-v2 |
| niro-phev | 기아 | kia-niro-plus-v2 |
| grand-koleos-hybrid | 르노코리아 | renault-grand-koleos-hybrid-v2 |
| arkana-gasoline | 르노코리아 | renault-arkana-gasoline-v2 |
| venue | 현대 | hyundai-venue-v2 |
| staria-lounge | 현대 | hyundai-staria-lounge-v2 |
| staria-lounge-hybrid | 현대 | hyundai-staria-lounge-hybrid-v2 |
| staria-hybrid | 현대 | hyundai-staria-hybrid-v2 |
| santafe-hybrid | 현대 | hyundai-santafe-hybrid-v2 |
| sonata-the-edge | 현대 | hyundai-sonata-the-edge-v2 |
| sonata-the-edge-hybrid | 현대 | hyundai-sonata-the-edge-hybrid-v2 |
| ioniq9 | 현대 | hyundai-ioniq9-v2 |
| casper-ev | 현대 | hyundai-casper-ev-v2 |
| kona-ev | 현대 | hyundai-kona-ev-v2 |
| palisade-hev | 현대 | hyundai-palisade-hev-v2 |
| tesla-model-3 | 테슬라 | tesla-model-3-v2 |
| tesla-model-y | 테슬라 | tesla-model-y-v2 |
| tesla-model-y-l | 테슬라 | tesla-model-y-l-v2 |

**② Active DB image_key 불일치 (8건)** — 하이브리드 차종이 베이스 모델 키 사용:

| slug | DB image_key | VL imageKey | 실제 파일 |
|---|---|---|---|
| avante-hybrid | hyundai-avante | hyundai-avante-hybrid-v2 | 별도 파일 존재 |
| grandeur-hybrid | hyundai-grandeur | hyundai-grandeur-hybrid-v2 | 별도 파일 존재 |
| kona-hybrid | hyundai-kona | hyundai-kona-hybrid-v2 | 별도 파일 존재 |
| tucson-hybrid | hyundai-tucson | hyundai-tucson-hybrid-v2 | 별도 파일 존재 |
| k5-hybrid | kia-k5 | kia-k5-hybrid-v2 | 별도 파일 존재 |
| k8-hybrid | kia-k8 | kia-k8-hybrid-v2 | 별도 파일 존재 |
| sportage-hybrid | kia-sportage | kia-sportage-hybrid-v2 | 별도 파일 존재 |
| sorento-hybrid | kia-sorento | kia-sorento-hybrid-v2 | 별도 파일 존재 |

> 참고: DB image_key 기준으로 이미지를 가져올 경우 하이브리드 전용 이미지가 아닌 베이스 모델 이미지가 사용됨. 사이트가 VL.imageKey 기준으로 동작한다면 현재 표시는 정상이나 DB 기반 조회 로직 사용 시 오표시 위험.

---

### 2-E. VEHICLE_LIST 중복 ID

**🟠 ISSUE: `kg12` ID가 두 차종에 중복 할당**

| id | slug | model |
|---|---|---|
| kg12 | actyon | 액티언 |
| kg12 | musso-ev | 무쏘 EV |

> KGM 주석에 "12종"으로 표기되나 실제는 11 slugs (ID 중복으로 1개 오중복). VL을 slug 기준으로 사용할 경우 큰 문제 없으나, id 기준 조회 시 충돌 발생.

---

## 3. 시정안

### 즉시 처리 권고 (사이트 표시 영향 없음, DB 정합성 개선)

**[S-1] DB image_key null 채우기 (29건)**  
대상: 위 2-D-① 목록 전체  
방법: VL.imageKey에서 `-v2` suffix 제거한 값을 DB `image_key`에 UPDATE  
예) `UPDATE vehicles SET image_key = 'kia-ev5' WHERE slug = 'ev5'`  
우선도: MEDIUM (사이트 표시는 VL 기반이므로 즉각 영향 없음, DB 활용 시 필요)

**[S-2] DB image_key 불일치 수정 (8건)**  
대상: 위 2-D-② 목록 전체 하이브리드 차종  
방법: 별도 하이브리드 image_key로 UPDATE  
예) `UPDATE vehicles SET image_key = 'hyundai-kona-hybrid' WHERE slug = 'kona-hybrid'`  
우선도: LOW (하이브리드 이미지 파일 분리 정책 확인 후 진행)

**[S-3] VEHICLE_LIST kg12 중복 ID 수정**  
대상: `src/constants/vehicles.ts`  
방법: 무쏘 EV의 id를 `kg13` 등 고유값으로 변경 (PR 필요)  
우선도: LOW (slug 기반 동작이라 즉각 영향 없음)

### 모니터링 권고

**[S-4] car-images 버킷 고아자산 3건 조사**  
- `hyundai-sonata-hybrid-v2.webp` — 쏘나타 하이브리드(VL·DB 미등록) 배경 확인  
- `kia-stinger-v2.webp` — 스팅어(VL·DB 미등록) 배경 확인  
- `renault-xm3-hybrid-v2.webp` — XM3 하이브리드(VL·DB 미등록) 배경 확인  
- `sitemap` 오브젝트 — 파일 여부 확인 후 삭제  
우선도: LOW (사이트 영향 없음, 스토리지 정리 차원)

**[S-5] 수입 브랜드 119건 (public/cars)**  
향후 수입 브랜드 확장 계획이 없다면 VEHICLE_LIST 외 파일은 고아자산으로 관리. 당장 삭제는 불필요하나, 확장 계획이 있을 경우 DB/VL 미등록 상태를 인지하고 있어야 함.  
우선도: LOW (추후 기획 결정 후 처리)

---

## 4. 데이터 소스 메모

| 소스 | 접근 방식 | 수집 시각 |
|---|---|---|
| vehicles DB | Supabase REST API (service_role) | 2026-06-02 |
| VEHICLE_LIST | `cadam-web/src/constants/vehicles.ts` 직접 분석 | 2026-06-02 |
| public/cars | 로컬 파일시스템 `ls` | 2026-06-02 |
| car-images 버킷 | Supabase Storage API (list) | 2026-06-02 |
