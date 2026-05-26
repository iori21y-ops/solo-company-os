---
title: "WF-VI: 차량 이미지 워크플로 initiative"
type: initiative
status: in-progress
created: 2026-05-27
project: cadam
---

# WF-VI (차량 이미지 워크플로)

랜테일러 사이트 차량 이미지 정합성·품질 확보 initiative.

## 목표

4자정합성: DB ↔ VEHICLE_LIST ↔ public/cars ↔ car-images 버킷.

## 핵심 규약

- 사이트 source of truth: `VEHICLE_LIST` (`src/constants/vehicles.ts`)
- 홈 카드: `public/cars/{imageKey}.webp` (800×600, 흰 캔버스)
- 상세 페이지: `car-images` 버킷 (carImageUrl 함수)
- 360 뷰: `car-360/{slug}/{frame}.webp`
- 대표 이미지 기준: 좌측면 약 90° + 흰 배경 + 그림자 최소

## 워크플로 분류

- 001a / 001b / 002 / 003 / 004 / 005

## 자동화 자산

- `/admin/images` 페이지가 360 → reprocessCarImage → car-images upsert → revalidate 자동 처리
- 좌측면 프레임: 현대 #009, 기아 #001, KGM #032, 르노 (기본 #017 / filante #012 / sm6 #014)

## 진행 현황

세부 세션 기록은 핸드오프 시스템 참조: `~/projects/_meta/handoff/projects/rentailor/`.

이 README는 initiative 개요만 박제. 사이클별 사실은 `data/raw/cycles/cadam/`,
학습은 `data/wiki/cadam/initiatives/wf-vi/` 에 누적.

## 본문 (미완성)

TBD — 세부 마일스톤·KPI·산출물 추적표.
