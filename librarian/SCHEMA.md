# 사서 스냅샷 스키마 (SCHEMA.md)

- 용도: 센서(멍청한 데몬)가 떨굴 JSON의 규격. 센서 스크립트와 사서 AI가 공통으로 읽는다.
- 성격: 규격 문서. 지침(SKILL.md)도 아니고 데이터(snapshot.json)도 아니다. 셋을 섞지 않는다.
- 확정일: 2026-06-02
- 원칙: 센서는 사실만 기록(판단 금지). 판단은 사서 AI가 snapshot을 읽고 한다.

## 저장 위치
- 최신 1장: `~/projects/_meta/librarian/snapshot-latest.json` (사서가 항상 읽는 파일)
- 이력: `~/projects/_meta/librarian/history/snapshot-YYYYMMDD-HHMM.json` (연속 2장 diff = 변경이력)

## 형식
- JSON. 사람용 SYSTEM_MAP.md 변환은 별도 트랙.

## 항목 (9묶음)

| 묶음 | 담을 내용 |
|---|---|
| meta | 찍은 시각(ISO8601), 호스트명, 센서 버전 |
| disk | 루트 사용률(%), 여유 GB |
| memory | 사용/여유 |
| services | 아래 별도 정의 |
| docker | 컨테이너별 이름, 상태, 이미지 |
| launchd | 커스텀 잡 라벨, PID, 상태코드 |
| backup | 마지막 백업 파일 시각, 크기 |
| git | _meta repo 마지막 커밋 시각 |
| remote | GPU서버·Supabase·Vercel 도달 여부 |

## services (핵심)

각 서비스 항목:
{
"name":      "서비스명",
"port":      포트번호 또는 null,
"pid":       PID 또는 null,
"type":      "managed" | "adhoc",
"expected":  true | false,
"alive":     true | false
}

- type=managed: launchd/docker에 등록된 정식 서비스. 죽으면 이상.
- type=adhoc: 손으로 띄운 임시 프로세스(예: python -m http.server). 죽어도 정상일 수 있음.
- expected: launchd/docker 등록 시 자동 true (B방식). adhoc은 false.

별도 필드:
"expected_exceptions": [ "서비스명", ... ]
- 사서가 "expected지만 죽음"을 보고 → 사람이 "꺼둬도 됨"이라 답한 서비스가 여기 누적.
- 다음부터 그 서비스는 이상 판정에서 제외.

## 정상 기준선 (확인된 사실)
- managed + expected=true 인데 현재 alive=false (= 살려야 할 대상):
  - price-crawler (port 9722, launchd com.cadam.price-crawler)
  - encar-crawler-v2 (launchd com.cadam.encar-crawler-v2)
- adhoc (죽어도 조용): 9730, 9740, 8888 (전부 python -m http.server)
