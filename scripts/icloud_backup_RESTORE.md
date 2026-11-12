# 맥 서버 복원 안내 (iCloud 백업에서)

> 이 파일은 `icloud_backup.sh`가 실행될 때마다 iCloud `data-warehouse-backup/RESTORE.md`로 복사된다. (2026-11-13)

## 백업에 들어 있는 것
| 파일 | 내용 | 주기·보관 |
|---|---|---|
| `data_날짜.tar.zst` | 데이터 창고 `~/projects/_data` 전체(사진·영상 제외). Postgres(cadam) 덤프 포함(`rentailor/backups/auto/postgres/`). SQLite는 안전 사본이 `shared/work/icloud-backup/sqlite-snapshot/`에 있음 → **DB는 이 사본으로 복원** | 매일 01:30 · 최근 7개 + 일요일분 4개 |
| `system_날짜.tar.zst` | `~/projects` 코드·문서 전체(_data 제외), Claude 설정·메모리·스킬, 예약 작업(LaunchAgents), `.gitconfig`·`.zprofile`·`.ssh/config`, `~/backups`, `manifest/`(설치 목록 등) | 매일 · 최근 7개 + 일요일분 4개 |
| (data 안) `rentailor/backups/auto/supabase/` | **렌테일러 사이트 DB(Supabase)** 전체 덤프(사이트 표 전부 = public 영역, 읽기 전용 모드로 받음. auth(관리자 로그인 계정)·storage(파일 목록)는 권한이 없어 빠짐 → 복원 시 관리자 계정 다시 만들기) | 매일 · 14개 |
| `media_날짜.tar` | 모든 사업의 `media/`(사진·영상) | 토요일 · 최근 4개 |
| `secrets_날짜.tar.zst.enc` | 비밀 파일(`.env`, `~/.cadam-secrets`, `~/.ssh`, `.zshrc`, 키·쿠키) — **사장님 암호로 AES-256 잠금** | 매일 · 최근 7개 |

**비밀 파일**은 system 묶음에서 빠지고 `secrets_` 암호화 묶음에만 있다. 암호는 맥 키체인(`icloud-backup-secrets`)과 사장님 보관처(폰 등)에만 있다 — **맥이 죽으면 사장님이 기억·보관한 암호가 유일한 열쇠**. `node_modules`·`.next`·가상환경은 아래 6번에서 다시 설치한다. Obsidian 위키(second-brain)는 원래 iCloud에 있다.

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
   **Supabase(렌테일러 사이트 DB)**: 사본은 `rentailor/backups/auto/supabase/supabase-날짜.dump`(매일, 14개). Supabase가 살아 있으면 복원할 필요가 없다. Supabase 데이터가 사라졌거나 망가졌을 때만, **사장님 승인 후** 새 프로젝트에 `pg_restore --no-owner -d "<새 프로젝트 접속 주소>" supabase-날짜.dump`로 넣는다(표 하나만 되살릴 때는 `-t 표이름`).
5. 비밀 파일 복원 (암호 입력 창이 뜬다):
   ```
   cd ~ && openssl enc -d -aes-256-cbc -pbkdf2 -iter 600000 -in "$B"/secrets_날짜.tar.zst.enc | zstd -dc | tar -xf -
   chmod 700 ~/.ssh ~/.cadam-secrets && chmod 600 ~/.ssh/id_*
   ```
   그 뒤 키체인에 같은 암호를 다시 넣는다: `security add-generic-password -a "$USER" -s icloud-backup-secrets -w` (입력 창에 암호)
6. 각 리포에서 `npm install` 또는 `pip install -r`을 실행한다. 가상환경 목록은 `~/manifest/venv-requirements.txt`에 있다. `~/manifest/git-repos.txt`에서 GitHub에 안 올라간 변경(dirty·unpushed)을 확인한다.
7. 예약 작업 켜기: `~/manifest/launchctl-list.txt`에 있는 것만 `launchctl load ~/Library/LaunchAgents/<이름>.plist`. **보류 중인 프로젝트(_paused)는 켜지 않는다.**

## 확인
- 백업 결과: 디스코드 "✅ iCloud 백업" 메시지, 로그 `~/projects/_data/shared/work/icloud-backup/backup.log`
- 수동 실행: `~/projects/_meta/scripts/icloud_backup.sh all`
