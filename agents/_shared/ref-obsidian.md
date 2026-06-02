---
title: "참조 — Obsidian 호환 양식"
type: reference
status: active
source: "CLAUDE.md §14에서 분리 (2026-06-02)"
---

# Obsidian 호환 (CLAUDE.md §14 상세)

이 vault는 Obsidian으로 직접 열어 그래프뷰·Dataview·백링크를 활용한다. 모든 페이지는 아래 4가지 양식을 준수한다.

## 14.1 링크 양식

vault 내부 참조는 **위키링크**, 운영 문서는 **마크다운 링크**로 작성한다.

- **위키링크 `[[경로]]`** — 학습 노트와 vault 내부 자산: `wiki/index.md`, `wiki/log.md`, `raw/cycles/`, `_shared/templates/` 등. 그래프뷰·백링크가 동작해야 하는 모든 페이지.
- **마크다운 링크 `[표시](경로)`** — 운영 문서: CLAUDE.md, README.md, 각 에이전트의 SKILL.md, `_shared/security/`. GitHub 웹뷰·모바일 cat에서도 동작해야 하는 페이지.
- vault 외부 자산(Supabase URL, 외부 사이트 등)은 §2.6 참조.

## 14.2 콜아웃 문법

Obsidian 콜아웃은 `> [!타입]` 문법으로 작성한다.

[!note] 메모
본문…
[!warning] 경고
본문…
지원 타입: `note` / `info` / `tip` / `warning` / `danger` / `important` / `example`.

언제 어떤 콜아웃을 쓰는지(가설은 `[!note]`, 모순은 `[!warning]` 등)는 §3.12 참조.

## 14.3 프론트매터 (YAML)

모든 페이지는 YAML 프론트매터로 시작한다. 구체 키 표준은 **§11.2(index.md)**, **§12.2(log.md)** 참조. 페이지 타입별 추가 키는 §3.4~§3.10 참조.

공통 원칙:
- 모든 키는 Dataview 쿼리에서 정렬·필터 가능해야 한다.
- 날짜는 `YYYY-MM-DD`, 리스트는 YAML 배열, 불리언은 `true`/`false`.
- 페이지 타입(`type:`)은 다음 중 하나: `index` / `log` / `cycle` / `insight` / `synthesis` / `playbook` / `failure` / `concept` / `entity` / `project-ref` / `scout-candidate`.
- 새 키·새 타입을 추가할 때는 §11.2 또는 해당 §3.X를 먼저 갱신한다.

## 14.4 이미지 참조

이미지는 vault 내 `assets/` 폴더에 저장하고 위키링크로 참조한다.

- 권장: `![[assets/diagram.png]]`
- 비권장: `![diagram](assets/diagram.png)`

대용량 이미지(>1MB)나 빈번한 업데이트가 예상되는 이미지는 vault에 박지 말고 외부 CDN(Supabase Storage 등) URL 사용 권장. 외부 자산 참조 양식은 §2.6 참조.
