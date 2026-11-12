# 맥 서버 복원 안내 (iCloud 백업에서)

> 이 파일은 `icloud_backup.sh`가 실행될 때마다 iCloud `data-warehouse-backup/RESTORE.md`로 복사된다. (2026-11-13)

## 백업에 들어 있는 것
| 파일 | 내용 | 주기·보관 |
|---|---|---|
| `data_날짜.tar.zst` | 데이터 창고 `~/projects/_data` 전체(사진·영상 제외). Postgres(cadam) 덤프 포함(`rentailor/backups/auto/postgres/`). SQLite는 안전 사본이 `shared/work/icloud-backup/sqlite-snapshot/`에 있음 → **DB는 이 사본으로 복원** | 매일 01:30 · 최근 7개 + 일요일분 4개 |
| `system_날짜.tar.zst` | `~/projects` 코드·문서 전체(_data 제외), Claude 설정·메모리·스킬, 예약 작업(LaunchAgents), `.gitconfig`·`.zprofile`·`.ssh/config`, `~/backups`, `manifest/`(설치 목록 등) | 매일 · 최근 7개 + 일요일분 4개 |
| `media_날짜.tar` | 모든 사업의 `media/`(사진·영상) | 토요일 · 최근 4개 |

**들어 있지 않은 것**: 비밀 파일(`.env`, `~/.cadam-secrets/`, 키·쿠키·토큰, SSH 키). 이름 목록만 `manifest/secret-file-names.txt`에 있다 → 비밀번호 보관함에서 다시 만든다. `node_modules`·`.next`·가상환경은 아래 6번에서 다시 설치한다. Obsidian 위키(second-brain)는 원래 iCloud에 있다.

## 복원 순서 (새 맥 또는 초기화된 맥)
1. macOS 로그인 → iCloud 로그인 → Finder에서 `iCloud Drive/data-warehouse-backup` 폴더를 우클릭하고 "지금 다운로드"를 누른다.
2. Homebrew 설치 → 터미널에서:
   ```
   B="$HOME/Library/Mobile Documents/com~apple~CloudDocs/data-warehouse-backup"
   ```
3. 코드·설정 복원 (가장 최신 system 파일):
   ```
   cd ~ && zstd -dc "$B"/system_날짜.tar.zst | tar -xf -
   brew bundle --file=~/manifest/Brewfile      # 설치 프로그램 일괄 재설치
   ```
4. 데이터 복원:
   ```
   cd ~/projects/_data && zstd -dc "$B"/data_날짜.tar.zst | tar -xf -
   tar -xf "$B"/media_날짜.tar
   ```
   SQLite DB는 `shared/work/icloud-backup/sqlite-snapshot/<원래 경로>`의 사본을 원래 자리에 덮어쓴다.
   Postgres: `pg_restore -d cadam rentailor/backups/auto/postgres/cadam-날짜.dump`
5. 비밀 파일 다시 만들기: `~/manifest/secret-file-names.txt` 목록대로 `.env`와 `~/.cadam-secrets`를 채운다. SSH 키는 새로 만들어 GPU 서버와 GitHub에 등록한다.
6. 각 리포에서 `npm install` 또는 `pip install -r`을 실행한다. 가상환경 목록은 `~/manifest/venv-requirements.txt`에 있다. `~/manifest/git-repos.txt`에서 GitHub에 안 올라간 변경(dirty·unpushed)을 확인한다.
7. 예약 작업 켜기: `~/manifest/launchctl-list.txt`에 있는 것만 `launchctl load ~/Library/LaunchAgents/<이름>.plist`. **보류 중인 프로젝트(_paused)는 켜지 않는다.**

## 확인
- 백업 결과: 디스코드 "✅ iCloud 백업" 메시지, 로그 `~/projects/_data/shared/work/icloud-backup/backup.log`
- 수동 실행: `~/projects/_meta/scripts/icloud_backup.sh all`
