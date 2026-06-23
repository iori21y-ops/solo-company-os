---
title: "관계 정합성 점검 규칙"
type: audit-rules
status: draft
created: 2026-05-27
updated: 2026-06-08
audit_kind: referential
threshold_status: undefined   # green/yellow/red 임계 미정, 데이터봇 소비 금지
source_script: cadam-data/scripts/wf_vi_m1_audit.py
---

# 관계 정합성 점검 규칙

테이블 간 / 4자정합성 / 외래키 무결성 규칙.
이 파일의 규칙은 wf_vi_m1_audit.py 가 실제로 수행하는 비교에서만 추출됨.
스크립트에 없는 검사는 포함하지 않는다.

## 운영 원칙

- 이 파일은 에이전트 운영 설정. 학습 페이지(wiki)와 분리.
- audit 사이클 누적에 따라 규칙/임계 보정 가능 (사람 승인 필요).
- 변경 시 사이클 프론트매터 `rules_applied`에 영향 명시.

## 4소스 식별

| 기호 | 소스 | 매칭 키 |
|------|------|---------|
| A | Supabase `vehicles` 테이블 (`is_active=True`) | `slug` |
| B | `cadam-web/src/constants/vehicles.ts` VEHICLE_LIST | `slug` → `imageKey` |
| C | `cadam-web/public/cars/*.webp` | `imageKey` (확장자 제거) |
| D | Supabase Storage `car-images` 버킷 | `imageKey` (`.webp` 제거) |

## 규칙 목록

### R1 — DB active ↔ VEHICLE_LIST 양방향 slug 정합성

**점검 방법**
- A\B: DB active slug이 VL에 없음 → P4(노출 불가) 건수
- B\A: VL slug이 DB active에 없음 → P5(역방향 불일치) 건수

**불일치 판정 조건**
- P4 > 0: 해당 slug는 DB에 활성 상태이나 웹 노출 불가
- P5 > 0: 해당 slug는 VL에 있으나 DB에 없음 (데드링크 위험)

**임계**
임계 미정 — 스크립트에 green/yellow/red 분류 근거 없음.
스크립트 출력: P4·P5 건수 및 슬러그 목록.

---

### R2 — VEHICLE_LIST imageKey ↔ public/cars 파일 존재 정합성

**점검 방법**
- A∩B 슬러그에 대해 slug_to_imagekey로 imageKey 조회 → C에 없으면 P3(복구 가능)

**불일치 판정 조건**
- P3 > 0: imageKey에 해당하는 public/cars/*.webp 파일 없음 → 이미지 표시 불가

**임계**
임계 미정 — 스크립트에 green/yellow/red 분류 근거 없음.
스크립트 출력: P3 건수 및 슬러그 목록.

---

### R3 — public/cars 파일 ↔ car-images Storage 정합성

**점검 방법**
- A∩B 슬러그이고 C에 있는 imageKey → D에 없으면 P2(미처리)

**불일치 판정 조건**
- P2 > 0: public/cars에는 있으나 car-images 버킷에 없음 → Storage 업로드 미완료

**임계**
임계 미정 — 스크립트에 green/yellow/red 분류 근거 없음.
스크립트 출력: P2 건수 및 슬러그 목록.

---

## 검산 규칙

스크립트는 `P1+P2+P3 == A∩B` 를 검산한다.
- 일치 → OK
- 불일치 → WARN (데이터 이상, 수동 확인 후 재실행)

검산 WARN 발생 시 R1~R3 판정보다 우선하여 데이터 확인.

---

## verdict 연결 (합의메모-verdict형식.md 기준)

- `audit_kind: referential`
- `data_type: visual`

**종합 임계 — 미정**
현재 스크립트는 건수만 출력하며 green/yellow/red 기준을 정의하지 않음.
아래는 사람이 채워야 할 항목:

```
green 조건: _______ (예: P2=P3=P4=P5=0 + 검산 OK)
yellow 조건: _______
red 조건: _______
```

임계 미확정 상태에서 생성된 verdict는 pending 격리 대상.
