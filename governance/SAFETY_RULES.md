# 안전 규칙 (SAFETY_RULES)

> 무엇을 정하는 파일: 승인이 필요한 일, 절대 하면 안 되는 일, DB 쓰기·삭제·백업·비밀 파일 다루는 법.
> 마지막 갱신: 2026-11-11 (사장님 결정 2 반영) · **이 파일이 원본 — 다른 문서는 여기를 가리킨다.** 지도: [RULES_MAP.md](RULES_MAP.md)
> cadam 상세(Supabase 단계별 확인·RLS·도구별 허용 표·오류별 대응)는 `~/projects/cadam/docs/security.md`. 내용이 다르면 이 파일이 우선.

## 1. 승인 범위 (사장님 결정 3·8·10·11, 2026-11-11)
원칙: **되돌릴 수 없는 것만 승인**받는다. 나머지는 하고 나서 보고한다.

| 승인 필요 (먼저 묻고 "예"를 받은 뒤 실행) | 승인 불필요 — 하고 나서 보고 |
|---|---|
| DB 쓰기 (INSERT·UPDATE·DELETE, 표 만들기·바꾸기) | git 커밋 (작업 전 `checkpoint:` 커밋 포함) |
| git push · 배포 (cadam-web push = 즉시 사이트 반영) | 문서 수정 (CLAUDE.md·docs·규칙 파일) |
| 서비스 재시작 (`launchctl kickstart -k`, 서버 재시작) | 새 예약 작업(launchd) 등록, 예약 작업의 파일 경로 수정 |
| 파일 삭제 (보관함 비우기 포함) | 다시 만들 수 있는 캐시 삭제 (`.next`, `__pycache__`, 병합된 worktree) |
| 운영 중인 예약 작업 끄기 (`launchctl unload`) | 코드 수정·읽기·조회·백업 만들기 |
| 운영 중인 예약 작업의 **실행 시각 변경** | 글쓰기 보류 스위치 **켜기**(`cadam-pipeline/data/WRITING_PAUSE` 만들기 = 발행 멈춤) |
| 글쓰기 보류 스위치 **끄기**(재개 — WP·네이버 발행이 다시 시작됨) | |
| 실행 중인 서비스의 설정 변경 (위 "경로 수정"은 제외 — 전역 규칙 "확인 없이 설정 변경 금지") | |

- **"마무리해줘"(세션 종료 요청) = 문서·규칙 리포(cadam-doc·_meta·_shared 등) push 승인**으로 본다. 코드·사이트 리포(cadam-web·cadam-pipeline·blog-engine 등) push는 따로 승인 (결정 10).

- 승인은 그때 그 일 하나에만 유효하다. 한 번 "예"가 다음 일까지 허락하지 않는다.
- 확신이 없으면 승인 필요 쪽으로 본다 (판단 순서: 안전 > 정확 > 속도).
- 승인 요청 양식: 작업 / 영향 범위 / 지금 상태 / 바뀐 뒤 상태 / 되돌리는 법 → "진행할까요?"

## 2. 절대 금지 (NEVER — 사장님이 시켜도 위험을 설명하고 하지 않는다)
| 구분 | 금지 |
|---|---|
| DB | `DROP TABLE`·`TRUNCATE` (표 통째 삭제·비우기) |
| DB | `WHERE`(조건) 없는 `DELETE`·`UPDATE` |
| DB | 백업 없이 스키마(표 구조) 바꾸기 |
| DB | 운영 Supabase에 `psql` 등으로 직접 접속 — 승인 받은 쓰기만 MCP 또는 Management API로 (결정 9) |
| DB | 브라우저용 anon 클라이언트(공개 키)로 UPDATE·DELETE — 서버 API(service_role) 경유 |
| 비밀 | `.env`·`.env.local`·API 키·토큰·비밀번호를 git에 커밋하거나 화면·로그에 출력 |
| 비밀 | 비밀 파일(`.env`, `~/.cadam-secrets/`, 발행 서버 `config.json`·쿠키) 옮기기·복사 — 제자리에서 읽기만 |
| 파일 | `rm -rf`, `rm -r` (폴더 통째 삭제) |
| git | `--force` push (강제 덮어쓰기), `git reset --hard` (작업 내용 날리기) |
| 시스템 | 시스템 폴더(`/etc`, `/usr`, `/System` 등)·시스템 설정 변경, 맥미니 재부팅·종료 |
| 시스템 | launchd plist 삭제 — 멈출 땐 `unload`(승인 후) |
| 접근 | GPU 서버에 IP 직접 입력 — 항상 `ssh gpu-server` |

안전장치: `~/.claude/hooks/block_dangerous_sql.py`가 DROP·TRUNCATE·WHERE 없는 DELETE/UPDATE를 자동으로 막는다. 막혀도 규칙은 그대로 — 채팅 승인은 따로 받는다.

## 3. DB 쓰기 절차 (운영 DB 쓰기는 승인 후 MCP·Management API로만, WHERE 필수·사전 조회 — 결정 9)
1. 바꿀 대상의 **지금 상태**를 조회해 보여 준다 (UPDATE·DELETE는 같은 WHERE로 SELECT 먼저, 영향 행 수 확인).
2. 무엇을 바꾸는지 **요약**한다 (변경 전/후 대조).
3. **되돌리는 법**을 적는다 (백업 SELECT·파일).
4. **승인** 후 실행 → 다시 SELECT로 결과·행 수 확인.
- 10행 이상이면 영향 범위를 명시하고, 가능하면 5~10행씩 나눠 실행.
- Supabase는 무료 플랜 한도 안에서 — 대량 입력·새 표·이미지 업로드 전 용량 확인 ([WORK_RULES.md](WORK_RULES.md) 비용).

## 4. 오류가 나면
- 즉시 멈추고 오류 메시지 전체를 보고한다.
- 자동 재시도는 최대 2회(총 3번). 3번째도 실패하면 멈추고 원인 분석을 보고.
- 되돌릴 수 있으면 방법을 제시만 한다 — 자동 되돌리기는 하지 않는다(승인 필요).
- merge 충돌은 자동 해결하지 않는다. push 거부 시 `git pull --rebase`는 제안만.

## 5. 정리·삭제 (결정 3 + [FOLDER_RULES.md](FOLDER_RULES.md) §5)
1. 다시 만들 수 있는 것(`.next`, `__pycache__`, 병합된 worktree)은 바로 지우고 보고. worktree는 `git worktree remove`.
2. 그 밖의 파일·폴더는 지우지 않고 **보관함** `~/projects/_archive/<YYYY-MM-DD>/<원래 경로>`로 옮긴다 → 예약 작업·코드가 그 파일을 안 쓰는지 확인.
3. **7일** 뒤 목록을 사장님께 보여 주고, 승인 받으면 비운다.
4. 실행 중인 예약 작업이 가리키는 파일을 옮기면 같은 작업에서 plist도 고치고 다시 불러온다.
5. 옮기기 전 그 저장소에서 `checkpoint:` 커밋. 다른 세션의 미커밋 변경이 있으면 멈추고 보고.

## 6. 백업 (사장님 결정 4, 2026-11-11)
| 종류 | 위치 |
|---|---|
| 자동 백업 (예약 작업이 만드는 것) | `~/projects/<사업>/backups/` (예: DB 덤프 `backups/postgres/`) |
| 일회성 백업 (작업 전 손으로 뜨는 것) | `~/projects/<사업>/backups-manual/` |
| 기존 `~/backups/` | 옮기지 않는다. **읽기 전용 보관** — 새 백업을 여기 만들지 않는다 |
| 로컬 PostgreSQL DB (`cadam`) | `~/projects/cadam/backup_cadam.sh`: 로컬 최근 **30개** + iCloud Drive 사본 **주 1회, 최근 8개**(약 2달) |
| blog-engine `outbox/` 글쓰기 파일(json·md) | 같은 스크립트가 매일 `blog-engine-outbox.tar.gz`로 묶어 cadam `backups/`에 |
| 데이터 창고 `~/projects/_data` 전체 (맥 밖 사본) | `_meta/scripts/icloud_backup.sh` (예약 `com.solo.icloud-backup` 매일 01:30) → iCloud Drive `data-warehouse-backup/`: 매일 `data_날짜.tar.zst`(media 제외, SQLite 안전 사본·Postgres 덤프 포함, 최근 7개+일요일분 4개) + 매일 `system_날짜.tar.zst`(맥 복원용: `~/projects` 코드·문서, Claude 설정·메모리, LaunchAgents, 설치 목록 — 비밀 파일·node_modules 제외) + 토요일 `media_날짜.tar`(사진·영상, 최근 4개). 동기화가 아니라 날짜별 묶음이라 맥에서 지워도 백업은 남는다. 결과는 디스코드. 복원 순서: iCloud 폴더의 `RESTORE.md` (2026-11-13). **예외 승인 2건(사장님 2026-11-13)**: ① 비밀 파일은 사장님 암호로 AES-256 잠근 `secrets_날짜.tar.zst.enc`로만 보관(암호=키체인 `icloud-backup-secrets`) ② 운영 Supabase DB(사이트 public 표 전부)를 매일 **읽기 전용(GET)** 으로 내보냄 — `scripts/supabase_rest_export.py`, 사이트 서비스 키로 REST API 조회 → `_data/rentailor/backups/auto/supabase/날짜/표.jsonl.gz` 14일. (pg_dump는 임시 DB 계정이 상담 등 잠긴 표를 못 읽어 포기, auth·storage 제외) |
| `_meta`·`content-engine`(옛 이름 blog-engine)·`_shared` 코드·문서 | 사업 폴더가 아니므로 따로 backups 폴더를 두지 않는다 — **GitHub 리모트가 백업** (커밋·push로 보관) |

- 파일 이름: `{원본파일명}_{YYYYMMDD}_{HHMMSS}.bak`
- 설정 파일(plist·`brand.yaml`·`config.json` 등)은 고치기 전에 백업 → 고친 뒤 `diff`로 확인. JSON이면 `python3 -m json.tool`로 문법 확인.

## 7. 비밀 파일
- 실제 위치: **`~/.cadam-secrets/`** (git 금지, 옮기기·복사 금지) + 각 프로젝트의 `.env`·`config/.env`.
- 값은 화면·로그·git·위키·메모리에 남기지 않는다. 필요한 코드는 그 경로에서 직접 읽는다.
- 고객 개인정보(이름·연락처·차량번호)는 위키·학습 노트·로그에 저장하지 않는다.
