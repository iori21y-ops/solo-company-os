---
title: "참조 — vault 전체 디렉토리 구조"
type: reference
status: active
source: "CLAUDE.md §2.1에서 분리 (2026-06-02)"
---

# vault 전체 디렉토리 구조 (CLAUDE.md §2.1 상세)

```
~/projects/_meta/agents/
├── .obsidian/                            # Obsidian vault 설정
├── CLAUDE.md                             # vault 공통 규칙 (핵심) + 참조 파일 색인
├── README.md                             # vault 진입 안내
├── _shared/                              # 에이전트 공통 자산
│   ├── boundary-rules.md                 # 에이전트 간 경계 규칙
│   ├── promotion-rules.md                # 승격 게이트 규칙
│   ├── scout-territories.md              # 자율 발굴 영역 정의
│   ├── delegation-template.md            # 위임 작업 양식
│   ├── workflow-template.md              # 자율 워크플로 양식
│   ├── ref-vault-structure.md            # (이 파일) §2.1 디렉토리 구조
│   ├── ref-page-formats.md               # §3 페이지 형식 규칙
│   ├── ref-index-format.md               # §11 index.md 형식
│   ├── ref-log-format.md                 # §12 log.md 형식
│   ├── ref-obsidian.md                   # §14 Obsidian 호환
│   ├── security/                         # 위임 권한 단계
│   │   ├── blacklist.md
│   │   ├── approval-required.md
│   │   └── auto-allowed.md
│   ├── templates/                        # cycle 양식 (별도 파일)
│   │   ├── cycle-marketing.md
│   │   ├── cycle-content.md
│   │   └── cycle-data.md
│   ├── counters/                         # 프로젝트별 사이클 카운터
│   │   ├── README.md
│   │   └── cadam.md
│   └── refs/                             # 프로젝트 정본 stub
│       └── cadam/
│           └── _index.md
│
├── marketing/                            # 에이전트별 작업·학습 공간
│   ├── SKILL.md                          # 역할·산출물·KPI·경계 정의
│   ├── raw/cycles/cadam/                 # 사이클 사실 기록
│   └── wiki/
│       ├── index.md
│       ├── log.md
│       ├── _skill/                       # 직무 학습 (모든 프로젝트 재사용)
│       │   ├── insights/
│       │   ├── syntheses/
│       │   ├── playbooks/
│       │   ├── failures/
│       │   ├── concepts/
│       │   └── entities/
│       └── cadam/                        # 프로젝트별 학습
│           ├── insights/
│           ├── syntheses/
│           ├── playbooks/
│           ├── failures/
│           └── scouts/                   # 자율 발굴 후보 카탈로그
│               ├── pending/
│               ├── approved/
│               ├── rejected/
│               └── completed/
│
├── content/                              # marketing + 다음 추가
│   └── assets/cadam/                     # 비축 자산 (wiki 밖)
│       ├── infographics/
│       ├── charts/
│       ├── cards/
│       ├── fact-blocks/
│       ├── comparisons/
│       └── reports/
│
├── data/                                 # marketing + 다음 추가
│   ├── _config/                          # 운영 설정 (audit 규칙, 임계값)
│   │   ├── source-tiers.md
│   │   ├── consistency-thresholds.md
│   │   ├── freshness-thresholds.md
│   │   └── audit-rules-{internal,referential,cross_source,temporal,semantic}.md
│   ├── _inbox/
│   │   └── adhoc-queue.md                # 사람 요청 임시 큐
│   ├── initiatives/                      # 대형 작업 단위
│   │   └── wf-vi/
│   │       ├── README.md
│   │       └── milestones.md
│   ├── builders/cadam/                   # 스크립트 자산 카탈로그
│   │   ├── README.md
│   │   ├── quantitative/
│   │   ├── visual/
│   │   ├── textual/
│   │   └── video/
│   └── wiki/cadam/
│       ├── audits/                       # 정합성 추세 (시계열)
│       │   ├── consistency-trend.md
│       │   ├── source-reliability-trend.md
│       │   └── {internal,referential,cross_source,temporal,semantic}/
│       └── initiatives/wf-vi/
│           ├── insights/
│           ├── syntheses/
│           └── playbooks/
│
├── sales/, cs/, ops/, finance/, legal/, strategy/   # 기본 구조 동일
```
