---
title: S-4 버킷 고아자산 조사 결과 + S-3 코드 수정 제안
type: report
subject: wfvi-s4-orphan / wfvi-s3-kg12
date: 2026-06-03
status: pending-approval
note: 데이터 봇이 결재 상신 시 파일을 디스크에 쓰지 않아, 브로커 로그(2026-06-03T05:07)에서 본문을 복구해 재생성함.
---

# S-4 버킷 고아자산 조사 결과 + S-3 코드 수정 제안

S-4 조사 완료. S-3 코드 파일 변경 내용도 확인했습니다. 결과를 정리합니다.

---

## [S-4] 버킷 고아자산 조사 결과

### 고아 WebP 3건 — DB 완전 미등록 확정

| 파일 | DB 조회 결과 | 판정 |
|---|---|---|
| `hyundai-sonata-hybrid-v2.webp` | slug/name 모두 미존재 | 과거 차종 잔류 파일 → **삭제 권고** |
| `kia-stinger-v2.webp` | slug/name 모두 미존재 | 단종 차종 잔류 파일 → **삭제 권고** |
| `renault-xm3-hybrid-v2.webp` | slug/name 모두 미존재 | 단종 차종 잔류 파일 → **삭제 권고** |

### sitemap 오브젝트 — 실체 파악

`sitemap`은 단일 오브젝트가 아닌 **`sitemap/` 폴더**로, 사이트 UI 스크린샷 PNG **53개**(2026-05-21 업로드)가 들어 있습니다.

```
sitemap/home.png, sitemap/cars-avante.png, sitemap/diagnosis.png,
sitemap/admin.png, sitemap/simulator.png ... (총 53개)
```

**판단:** car-images 버킷에 잘못 업로드된 사이트 문서/QA 스크린샷 모음. 차량 이미지 파이프라인과 무관. → **삭제 권고** (단, 고의 업로드일 수 있으므로 배경 확인 후 처리)

> 고아 WebP 3건 + sitemap/ 폴더 삭제는 버킷 쓰기 작업으로, S-1 결재 완료 후 별도 제안합니다.

---

## [S-3] VL kg12 중복 ID 수정

**대상 파일:** `/Users/kim/projects/cadam/cadam-web/src/constants/vehicles.ts` 118번째 줄

현재 중복 상태:
- 줄 110: `id: 'kg12'` — 액티언 (actyon)
- 줄 118: `id: 'kg12'` — **무쏘 EV** (musso-ev) ← 여기만 수정

사용 중인 KGM ID: `kg01~kg06, kg09~kg12` (kg07·kg08·kg13 미사용)

**변경안:** 무쏘 EV를 `kg12` → **`kg13`** 으로 변경

코드 수정은 DB 게이트 대상이 아니나, 사이트 직접 영향 코드이므로 별도 승인 후 진행합니다.

---

## 현재 대기 상태

| 항목 | 상태 |
|---|---|
| **S-1** (DB 29건) | ⏳ 확인코드 `WRITE-S1-c7e2` 대기 중 |
| **S-2** (DB 8건) | S-1 완료 후 제안 예정 |
| **S-3** (코드 수정) | 위 변경안 승인 대기 |
| **S-4** (조사) | ✅ 완료 — 고아 WebP 3건 + sitemap/ 폴더 삭제 제안 예정 |
| **S-5** | 모니터링 대기 (기획 결정 필요) |

**S-1 + S-3 동시 승인 가능합니다.** S-1은 `WRITE-S1-c7e2`, S-3은 "S-3 승인" 또는 `WRITE-S1-c7e2` 회신 시 함께 처리하겠습니다.
