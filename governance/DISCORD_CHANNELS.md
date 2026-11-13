# 디스코드 채널 지도 (사업별 정리)

> 무엇을 정하는 파일: 어느 알림이 어느 채널로 가는지, 어떤 봇이 보내는지. 지도: [RULES_MAP.md](RULES_MAP.md)
> 마지막 갱신: 2026-11-13 (결재 에이전트 체계 폐지 반영 — 봇은 "알림" 하나)
> 채널 이름을 바꾸면 알림이 끊긴다 — 여러 프로그램이 채널을 **이름**으로 찾는다
> (`_shared/solo_common/discord_client.find_channel`: "콘텐츠기획"·"데이터"·"축구블로그"·"클리퍼").
> 그래서 사업별 정리는 **이름은 그대로 두고 카테고리(채널 묶음)만** 나눈다.
> 새 사업 채널 이름에 `데이터`·`마케팅`·`콘텐츠기획`을 다시 쓰지 말 것(이름 찾기가 겹친다).

## 봇
- **"알림" 봇 하나만 쓴다** (옛 이름 관리팀장, 2026-11-13 이름 변경). 토큰 `DISCORD_BOT_TOKEN`은 `~/.cadam-secrets/secrets.env`에서 읽는다(값 출력 금지).
- 보내는 코드: `_shared/solo_common/discord_client.py`, `cadam/collect/lib/notify.py`, `~/.cadam-secrets/notify_discord.sh`, `_meta/scripts/server-health-check.sh`, ERP 알림(`web-engine/cadam-erp`).
- 옛 에이전트 봇(마케팅·콘텐츠·데이터·기획팀장)은 쓰지 않는다 — 서버에서 내보내기·앱 삭제는 사장님이 직접(디스코드 / Developer Portal).

## 카테고리 구성
| 카테고리 | 채널 | 무엇이 오나 |
|---|---|---|
| 📁 렌테일러 | #콘텐츠기획 | 글감 후보(B코드)·크롤러/큐레이터·발행 (content-engine rentailor), GPU 이미지 작업 알림·검토(`cadam/services/gpu-agent/config/loop-config.json`, 11-13 #대표이사실에서 이동) |
| | #데이터 | 키워드 스캔(keyword-scan), 수집기 알림(가격표 대조·가격·옵션·색상 변경·렌트료 반영·사진 확인표·데이터 점검·수집기 실패 — `cadam/collect/lib/notify.py` 한 곳을 거침), 엔카 시세·RSS |
| | #마케팅 | 주간 유입 분석, 검색 문구 실험(S코드) |
| | #상담 (1570612529640640512) | 🆕 새 상담 알림 R-#### (Spidey Bot 웹훅, ERP) |
| 📁 축구 | #축구블로그 | 축구 초안·발행·자동 점검 경고 (football-blog, 11/11부터 보류) |
| 📁 공통 | #시스템알림 | 백업·서버 점검·비밀값 점검·감사(audit-agent)·Supabase 로그 한도·사이트맵 변화·카담 일일 리포트·Linear 진단(🩺 REN-###)·ERP 아침 브리핑 |
| (카테고리 없음, 알림 끔) | #클리퍼 | 사장님이 링크를 올리면 `cadam/collect/telegram_clipper/discord_clip_poller.py`(launchd `com.cadam.discord-clipper`, 60초마다)가 읽어 처리 |

- 카테고리 id: 렌테일러 1570612114920439939 · 축구 1570612128405262436 · 공통 1570612144116867182.
- 봇은 채널 관리 권한이 없음(403) → 채널 삭제·카테고리·웹훅 변경·알림 끄기는 사장님 계정 디스코드 웹(ego-browser)으로 처리.
- 텔레그램: 2026-11-13 완전 폐지 — 텔레그램 클리퍼 봇(`com.cadam.clipserver`) 끔(설정은 `LaunchAgents/disabled/`), 옛 `telegram_notifier.py`는 `_archive/2026-11-13/telegram/`(크롤러·큐레이터 디스코드 알림은 `cadam/core/scripts/common/content_notifier.py`). 링크 저장은 #클리퍼만 쓴다.
- 확인 안 된 것: GPU 서버에서 보내는 알림(11/13 접속 시간 초과) — 확인 후 이 표에 적는다.

## 정리 기록 (2026-11-13)
> ⚠️ 기록용 — 지금 규칙이 아니라 경과
- 결재 에이전트 체계 폐지: 에이전트 카드 스레드(관리팀장·데이터·마케팅)는 더 생기지 않는다. 옛 #관리팀장 채널 기록은 `_data/shared/collected/discord-archive/discord-관리팀장-채널-20261113.json`에 보관, 채널은 없어짐.
- #대표이사실(1510170922005565470): 봇 권한 부족으로 삭제 실패 → **사장님 직접 삭제 예정**. 새 상담 알림은 이미 #상담으로 옮김.
- #관리팀장실: 이미 서버에 없음(404).
- 주식 모닝 브리핑 중지(2026-10-28부터 안 돎).
