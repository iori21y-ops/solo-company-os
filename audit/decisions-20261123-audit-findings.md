# 감사 결함 3건 결정표 (2026-11-23, 그릴미)

07:30 감사 알림 "결함 3건"을 조사한 결과와 결정.

| # | 결정 | 사장님 답 | 근거·비고 |
|---|---|---|---|
| 1 | 인카 중고차 수집(com.importlease.encar-used) — 감사 착오, 감사 쪽 수정 | ㅇ (AI가 정한 것 ⓐ) | 11-17 정상 수집(19개 브랜드). 감사가 늘 비어 있는 err.log를 보고 있었음 → `scripts/audit_jobs.py` REAL_LOGS에 `encar_used.log` 추가 (f0dc6e5) |
| 2 | 세컨드브레인 RSS(com.user.secondbrain.rss) — 감사 착오, 주기 7일로 | ㅇ (AI가 정한 것 ⓑ) | 11-18부터 collect_all.sh는 월요일 밤만 실제 수집 → PERIOD_OVERRIDE 7일 (f0dc6e5). 수정 후 audit_jobs.py 결과 0건 |
| 3 | 문서 감사(com.solo.doc-audit) — plist를 `/bin/zsh -c`로 감싸 실행 | ㅇ (Q1 ①) | 11-16 09:05 launchd 실행에서 iCloud 볼트 CLAUDE.md 읽기 PermissionError. 손 실행은 성공. 다른 위키 작업은 zsh 경유라 정상. 옛 plist 백업: `~/projects/_archive/2026-11-23/com.solo.doc-audit.plist.bak` |

## 남은 확인
- ✅ 11-23 09:05 문서 감사 자동 실행 성공(종료 0, 문서 173개 점검). 새로 열린 REN-253(위키 경로 1건)·REN-254(plist 사본 2건 중 doc-audit 건은 38341f5로 해결, daily-stop 사본은 별개)
- 11-24 07:30 감사 알림에서 3건 사라졌는지
