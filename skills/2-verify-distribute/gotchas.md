# 함정 (Gotchas) — 자동배분 검증

- originChannelId가 비면 데이터봇 Discord 알림이 실패한다.
  → #대표이사실 채널 ID(1510170922005565470) 하드코딩으로 주입.
  createLedgerTask에서 주입하고 자식 task가 상속하게 한다.
- 유령 [TASK] 카드 이중 생성 주의. 프롬프트 가드 + dispatchTask kind 가드 둘 다 필요.
- originChannelId는 erp_tasks(대시보드 /api/tasks)에 저장 안 됨.
  broker 로컬 ledger(JSON)에만 있음. 그래서 대시보드 API로는 상속 검증 불가.
  → 상속/알림 검증은 8-databot-alert-debug 런북에서 ledger 직접 확인할 것.
