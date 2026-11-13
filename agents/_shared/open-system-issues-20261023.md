# 열린 시스템 이슈 (2026-10-23 정리)

broker 작업대장에 owner='시스템'/'기획팀장'으로 쌓여 있던 미처리 요청 56건(6/16~10/23)을 정리한 결과.
처리 주체(봇)가 없어 한 번도 실행되지 않았던 요청들이다. 해결·중복 건은 대장에서 닫았고, 남은 주제만 여기 모은다.
앞으로 같은 유형은 broker의 매일 09시 [미결재 알림]에 "미처리 요청"으로 함께 표시된다.

## 해결 확인 후 종결 (43건)
- info_articles 신규 0건 (26건): info_articles는 크롤러가 아니라 WordPress 발행글 미러(com.cadam.wp-sync). 원인은 GWP-2 자동발행 장애(종료된 LLM 모델). 10/23 모델 교체로 복구, 14:53 신규 행 확인.
- repair_shops 재수집 (8건): 2026-07-08 재수집(34,366행), 매월 1일 launchd(com.cadam.api-hub.repair-shops).
- extracted_insights / vehicle_powertrains 조회 차단 (5건): 10/23 데이터 봇 정상 조회 확인.
- GWP-1 크롤링 타임아웃 (1건): 10/23 LLM 모델 교체로 23분 완료.
- n8n .env SUPABASE 변수 (1건): GWP-2가 $env.SUPABASE_URL로 상태 갱신 성공 → 반영됨.
- EV 보조금 스팟 확인·GPU 서버 스펙 문의 (2건): 7월 시점 단발 문의, 시효 경과로 종결.

## 아직 열린 주제
| # | 주제 | 현황 | 원 요청 |
|---|---|---|---|
| 1 | vehicle_msrp 수집 정지 | 최신 week_key 2026-W17. `~/second-brain/scripts/upload_msrp_to_supabase.py` 계열, 자동 스케줄 없음 | 0009·0011·0018·0029 (7/5) |
| 2 | ev_subsidies·finance_rates 미수집 | ev_subsidies 6/9, finance_rates 7/11이 마지막. `fetch_ev_subsidies.py`는 미커밋·스케줄 없음 | 0701-0003·0725-0004·0726-0005 |
| 3 | 인사이트 추출 | **해결(10/23)**: `collect/extract/insight_extractor.py` 신설(5d047cd), gwp1 3단계로 매일 새벽 자동 실행. 자동 검증(근거 문장·수치·차명·구체성·약관 문구·중복)을 통과한 행만 status=approved로 저장(WF-7은 pending만 병합하므로 마스터 데이터 무영향). 잔여 위험=GWP-2가 글감과 무관하게 상위 8건을 가져옴(관련도 필터 필요) | 0724-0003·0725-0003 |
| 4 | audit-agent.sh 실패 시 무알림 | A3/A4 경보가 실패해도 알림 경로 없음 | 0713-0006·0721-0012·0721-0013·0730-0007 |
| 5 | 모닝브리핑 message2 Discord 500 | 7/28 재현성 500(개별 전송은 200). 재발 여부 미확인 | 0728-0011 |
| 6 | 카드 title 콜론 뒤 잘림·instruction 비는 저장 버그 | #161·#171 사례, 원인 미조사 | 0705-0039 |
| 7 | n8n DB 무결성 손상 의심 | 7/27 보고. 10/23 n8n 정상 기동·실행은 확인, 무결성 점검은 미실시 | 0728-0008 |

## 일시중지한 주기 카드 (재개 조건)
입력 자료가 수개월째 없어 매일 "대상 없음"으로 끝나며 Claude 호출만 쓰던 카드. 2026-10-23 cadence를 null로 바꿔 정지.
| 카드 | source_ref | 원래 cadence / earliest_hour | 재개 조건 |
|---|---|---|---|
| 114 | DATA-05 인사이트 정합성 게이트 | daily / 6 | **폐기 권장**: 코드 검증이 대체. 필요하면 주 1회 보고형 요약으로 |
| 115 | CONT-01 팩트블록 생산 | daily / 7 | **폐기 권장**: 소비처 없음(fact-blocks/ 0개, 블로그·웹 미연결) |
| 117 | MKTG-03 발행 D+7 측정 | daily / 8 | 마케팅 cycle(인스타·쇼츠) 발행 재개 |

재개: `update erp_tasks set cadence='daily' where id in (...)` (broker가 최대 1시간 내 반영).
