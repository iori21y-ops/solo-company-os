#!/bin/bash
# Off-machine backup of the data warehouse (~/projects/_data) to iCloud Drive. Owner-approved 2026-11-13.
#
# Why: the warehouse (~16GB, all businesses) had no copy outside this Mac. iCloud is outside the house and
# always on; files are stored as DATED ARCHIVES (not a synced mirror), so a deletion on the Mac never deletes
# the backup.
#
# What it does (read-only on the warehouse; other sessions may keep working while it runs):
#   daily  -> data_YYYYMMDD.tar.zst : everything in _data except <business>/media and .git
#             + consistent SQLite snapshots (sqlite3 .backup) under shared/work/icloud-backup/sqlite-snapshot/
#             (restore DBs from the snapshot copy, not from the live file in the archive)
#   weekly -> media_YYYYMMDD.tar    : every <business>/media folder (photos/videos, no compression)
#             runs on Saturdays, or whenever no media archive exists yet
# The folder list is discovered on every run, so moved/new folders are picked up automatically.
#   daily  -> system_YYYYMMDD.tar.zst : ~/projects code/docs (no _data, no node_modules/.next/venv, NO secrets),
#             Claude settings+memory, LaunchAgents, dotfiles, manifests (Brewfile, crontab, git repo states,
#             venv requirements, secret file NAMES). Restore guide: RESTORE.md in the iCloud folder.
#   daily  -> secrets_YYYYMMDD.tar.zst.enc : .env files, ~/.cadam-secrets, ~/.ssh, .zshrc, keys/cookies — AES-256
#             encrypted with the owner's passphrase (keychain item icloud-backup-secrets). Keep 7.
# Keep: data/system = 7 newest + 4 newest Sunday archives; media = 4 newest.
# launchd: com.solo.icloud-backup (daily 01:30). Discord message on success and on failure.
# Restore: cd <dest> && zstd -dc data_YYYYMMDD.tar.zst | tar -xf -   /   tar -xf media_YYYYMMDD.tar
export LANG=en_US.UTF-8
export PATH=/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin
HOME=/Users/kim
WH="$HOME/projects/_data"
DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/data-warehouse-backup"
STATE="$WH/shared/work/icloud-backup"
SNAP="$STATE/sqlite-snapshot"
LOG="$STATE/backup.log"
TODAY=$(date +%Y%m%d)
MODE="${1:-auto}"   # auto | data | system | secrets | media | all

mkdir -p "$STATE" "$SNAP" "$DEST"
log() { echo "$(date '+%F %T') $*" >> "$LOG"; }
notify() { source "$HOME/.cadam-secrets/notify_discord.sh" && notify_discord "$1"; }
fail() { log "FAIL: $*"; notify "❌ iCloud 데이터 창고 백업 실패: $* (로그 $LOG)"; exit 1; }

cd "$WH" || fail "창고 폴더 없음"
[ -d "$DEST" ] || fail "iCloud 폴더 없음"
LOCK="$STATE/.lock.d"   # mkdir is atomic; a lock older than 12h is treated as stale (crashed run)
if ! mkdir "$LOCK" 2>/dev/null; then
  if [ -n "$(find "$LOCK" -maxdepth 0 -mmin +720 2>/dev/null)" ]; then rmdir "$LOCK"; mkdir "$LOCK" || exit 0
  else log "another run is active, skip"; exit 0; fi
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

free_gb() { df -g "$HOME" | awk 'NR==2{print $4}'; }

# Build path lists: data = all top-level entries (except .git) with each business folder expanded so that
# its media/ child can be left out; media = every <business>/media.
DATA_ITEMS=(); MEDIA_ITEMS=()
for e in * .[!.]*; do
  [ -e "$e" ] || continue
  [ "$e" = ".git" ] && continue
  if [ -d "$e" ] && [ ! -L "$e" ]; then
    for c in "$e"/* "$e"/.[!.]*; do
      [ -e "$c" ] || continue
      if [ "$(basename "$c")" = "media" ]; then MEDIA_ITEMS+=("$c"); else DATA_ITEMS+=("$c"); fi
    done
  else
    DATA_ITEMS+=("$e")
  fi
done

# Verify an archive can be read end to end; prints the file count.
count_entries() { if [[ "$1" == *.zst ]]; then zstd -dc "$1" | tar -tf - | wc -l | tr -d " "; else tar -tf "$1" | wc -l | tr -d " "; fi; }

run_data() {
  # 1) consistent SQLite copies (live DBs may be mid-write; copying them raw can give a broken file)
  find "$SNAP" -type f -delete 2>/dev/null
  local n=0 bad=0
  while IFS= read -r -d '' f; do
    rel="${f#./}"; out="$SNAP/$rel"; mkdir -p "$(dirname "$out")"
    if sqlite3 -readonly "$f" ".timeout 20000" ".backup '$out'" 2>>"$LOG" \
       && [ "$(sqlite3 "$out" 'PRAGMA quick_check;' 2>/dev/null)" = "ok" ]; then n=$((n+1))
    else bad=$((bad+1)); log "sqlite snapshot failed: $rel"; fi
  done < <(find . \( -name .git -o -name media -o -path ./shared/work/icloud-backup \) -prune -o \
              -type f \( -name '*.db' -o -name '*.sqlite' -o -name '*.sqlite3' \) -print0)
  log "sqlite snapshots ok=$n failed=$bad"

  # 2) archive (write .partial first so a half-written file never looks like a backup)
  local out="$DEST/data_$TODAY.tar.zst" tmp="$DEST/.data_$TODAY.tar.zst.partial"
  [ "$(free_gb)" -ge 10 ] || fail "맥 남은 공간 $(free_gb)GB (10GB 미만)"
  tar -cf - "${DATA_ITEMS[@]}" 2>>"$LOG" | zstd -q -T0 -6 -o "$tmp" -f
  local rc=("${PIPESTATUS[@]}")
  # tar exits 1 when a file vanished/changed while reading (another session working) — accept, verify below
  [ "${rc[1]}" -eq 0 ] || { rm -f "$tmp"; fail "data 압축 실패 (zstd ${rc[1]})"; }
  local cnt; cnt=$(count_entries "$tmp")
  [ "${cnt:-0}" -gt 100 ] || { rm -f "$tmp"; fail "data 압축본 검증 실패 (항목 ${cnt:-0}개)"; }
  mv -f "$tmp" "$out"
  DATA_MSG="data $(du -h "$out" | cut -f1) · 파일 ${cnt}개 · DB 사본 ${n}개$([ $bad -gt 0 ] && echo " (실패 $bad)")$([ "${rc[0]}" -ne 0 ] && echo " · 작업 중 바뀐 파일 경고 있음")"
  log "data ok: $out ($cnt entries, tar rc=${rc[0]})"
  [ $bad -eq 0 ] || SNAP_WARN=1
}

run_media() {
  [ ${#MEDIA_ITEMS[@]} -gt 0 ] || { MEDIA_MSG="media 폴더 없음"; return; }
  local need; need=$(( $(du -sg "${MEDIA_ITEMS[@]}" | awk '{s+=$1} END{print s}') + 5 ))
  [ "$(free_gb)" -ge "$need" ] || fail "맥 남은 공간 $(free_gb)GB (media 백업에 ${need}GB 필요)"
  local out="$DEST/media_$TODAY.tar" tmp="$DEST/.media_$TODAY.tar.partial"
  tar -cf "$tmp" "${MEDIA_ITEMS[@]}" 2>>"$LOG"; local rc=$?
  local cnt; cnt=$(count_entries "$tmp")
  [ "${cnt:-0}" -gt 100 ] || { rm -f "$tmp"; fail "media 묶음 검증 실패 (tar $rc, 항목 ${cnt:-0}개)"; }
  mv -f "$tmp" "$out"
  MEDIA_MSG="media $(du -h "$out" | cut -f1) · 파일 ${cnt}개$([ $rc -ne 0 ] && echo " · 작업 중 바뀐 파일 경고 있음")"
  log "media ok: $out ($cnt entries, tar rc=$rc)"
}

run_system() {
  # Everything needed to rebuild this Mac quickly besides the warehouse: all code/docs under ~/projects,
  # Claude settings+memory, launchd jobs, dotfiles, and manifests of installed software.
  # Regenerable folders and SECRET FILES are left out (SAFETY_RULES: secrets are never copied) —
  # manifest/secret-file-names.txt lists their names only, so a restore knows what to re-create.
  local M="$STATE/manifest"; find "$M" -type f -delete 2>/dev/null; mkdir -p "$M"
  brew bundle dump --file="$M/Brewfile" --force >/dev/null 2>&1 || brew list --versions > "$M/brew-list.txt" 2>/dev/null
  crontab -l > "$M/crontab.txt" 2>/dev/null
  launchctl list | grep -E 'com\.(kim|cadam|solo|iori21y|blogengine|rentailor|user)' > "$M/launchctl-list.txt" 2>/dev/null
  npm ls -g --depth=0 > "$M/npm-global.txt" 2>/dev/null
  { sw_vers; python3 --version; node --version; } > "$M/versions.txt" 2>&1
  # python venvs -> requirements (venv folders themselves are not backed up)
  find "$HOME/projects" -path "$HOME/projects/_data" -prune -o \( -name .venv -o -name venv \) -type d -prune -print 2>/dev/null |
    while IFS= read -r v; do [ -x "$v/bin/pip" ] && { echo "### $v"; "$v/bin/pip" freeze 2>/dev/null; }; done > "$M/venv-requirements.txt"
  # git state of every repo: remote, branch, uncommitted / unpushed counts (what GitHub does NOT have)
  find "$HOME/projects" "$HOME/.claude" -maxdepth 4 -name .git -not -path '*/node_modules/*' 2>/dev/null | sort |
    while IFS= read -r g; do r=$(dirname "$g")
      echo "$r | $(git -C "$r" remote get-url origin 2>/dev/null || echo NO-REMOTE) | $(git -C "$r" branch --show-current 2>/dev/null) | dirty=$(git -C "$r" status --porcelain 2>/dev/null | wc -l | tr -d ' ') | unpushed=$(git -C "$r" rev-list --count @{u}..HEAD 2>/dev/null || echo ?)"
    done > "$M/git-repos.txt"
  # secret files: NAMES ONLY
  { echo "# secret files NOT in this backup (re-create from your password store)"; ls -1 "$HOME/.cadam-secrets" 2>/dev/null | sed 's#^#~/.cadam-secrets/#'
    find "$HOME/projects" -path "$HOME/projects/_data" -prune -o \( -name node_modules -o -name .next \) -prune -o -type f \( "${SECRET_FIND[@]}" \) -print 2>/dev/null; } > "$M/secret-file-names.txt"
  # .zshrc with secret values blanked
  sed -E 's/^([^#]*(KEY|TOKEN|SECRET|PASSWORD|PASS)[A-Za-z_]*=).*/\1<REDACTED>/I' "$HOME/.zshrc" > "$M/zshrc.redacted" 2>/dev/null

  local items=("projects" "Library/LaunchAgents" ".claude/CLAUDE.md" ".claude/settings.json" ".claude/keybindings.json"
               ".claude/skills" ".claude/agents" ".claude/commands" ".gitconfig" ".zprofile" ".ssh/config" "backups")
  local have=(); for i in "${items[@]}"; do [ -e "$HOME/$i" ] && have+=("$i"); done
  while IFS= read -r d; do have+=("${d#$HOME/}"); done < <(find "$HOME/.claude/projects" -maxdepth 2 -type d -name memory 2>/dev/null)

  local out="$DEST/system_$TODAY.tar.zst" tmp="$DEST/.system_$TODAY.tar.zst.partial"
  [ "$(free_gb)" -ge 10 ] || fail "맥 남은 공간 $(free_gb)GB (10GB 미만)"
  tar -C "$HOME" -cf - --exclude 'projects/_data/*' "${SYS_EXCLUDES[@]}" "${have[@]}" -C "$STATE" manifest 2>>"$LOG" \
    | zstd -q -T0 -6 -o "$tmp" -f
  local rc=("${PIPESTATUS[@]}")
  [ "${rc[1]}" -eq 0 ] || { rm -f "$tmp"; fail "system 압축 실패 (zstd ${rc[1]})"; }
  local cnt; cnt=$(count_entries "$tmp")
  [ "${cnt:-0}" -gt 1000 ] || { rm -f "$tmp"; fail "system 압축본 검증 실패 (항목 ${cnt:-0}개)"; }
  if zstd -dc "$tmp" | tar -tf - | grep -E "$SECRET_RE" | head -1 | grep -q .; then
    rm -f "$tmp"; fail "system 압축본에 비밀 파일이 섞여 있어 폐기함"; fi
  mv -f "$tmp" "$out"
  SYS_MSG="system $(du -h "$out" | cut -f1) · 파일 ${cnt}개"
  log "system ok: $out ($cnt entries, tar rc=${rc[0]})"
}

run_secrets() {
  # Owner-approved exception 2026-11-13 (SAFETY_RULES §7): secret files go to iCloud ONLY as an archive encrypted
  # with a passphrase the owner chose. The passphrase lives in the login keychain (service icloud-backup-secrets),
  # put there by the owner; it is passed to openssl on a file descriptor, never on disk, argv or env.
  if ! security find-generic-password -a "$USER" -s icloud-backup-secrets >/dev/null 2>&1; then
    SEC_MSG="⚠️ 비밀 파일 백업 건너뜀(키체인에 암호 없음)"; log "secrets skipped: no keychain passphrase"; return; fi
  local list="$STATE/.secret-list"
  { [ -d "$HOME/.cadam-secrets" ] && echo ".cadam-secrets"
    [ -d "$HOME/.ssh" ] && echo ".ssh"
    [ -f "$HOME/.zshrc" ] && echo ".zshrc"
    find "$HOME/projects" -path "$HOME/projects/_data" -prune -o \( -name node_modules -o -name .next -o -name .venv -o -name venv \) -prune -o \
      -type f \( "${SECRET_FIND[@]}" \) -print 2>/dev/null | sed "s#^$HOME/##"; } > "$list"
  local out="$DEST/secrets_$TODAY.tar.zst.enc" tmp="$DEST/.secrets_$TODAY.partial"
  tar -C "$HOME" -cf - --exclude ".ssh/agent" -T "$list" 2>>"$LOG" | zstd -q -T0 -9 | \
    openssl enc -aes-256-cbc -pbkdf2 -iter 600000 -salt -pass fd:3 -out "$tmp" \
      3< <(security find-generic-password -a "$USER" -s icloud-backup-secrets -w)
  local rc=("${PIPESTATUS[@]}")
  [ "${rc[2]}" -eq 0 ] && [ -s "$tmp" ] || { rm -f "$tmp"; fail "비밀 파일 암호화 실패"; }
  # verify: decrypt with the same passphrase and count entries
  local cnt; cnt=$(openssl enc -d -aes-256-cbc -pbkdf2 -iter 600000 -pass fd:3 -in "$tmp" \
      3< <(security find-generic-password -a "$USER" -s icloud-backup-secrets -w) | zstd -dc | tar -tf - | wc -l | tr -d ' ')
  [ "${cnt:-0}" -gt 5 ] || { rm -f "$tmp"; fail "비밀 파일 묶음 검증 실패 (항목 ${cnt:-0}개)"; }
  mv -f "$tmp" "$out"; rm -f "$list"
  SEC_MSG="secrets(암호화) 파일 ${cnt}개"
  log "secrets ok: $out ($cnt entries)"
}

# Regenerable or secret paths left out of the system archive (bsdtar patterns match any path component).
SYS_EXCLUDES=(--exclude node_modules --exclude .next --exclude .next-prev --exclude .venv --exclude venv --exclude __pycache__
  --exclude .turbo --exclude .cache --exclude .DS_Store --exclude '*.pyc'
  --exclude '.env' --exclude '.env.*'
  --exclude '*.pem' --exclude '*.key' --exclude '*.p12' --exclude '*secret*.json' --exclude 'client_secret*'
  --exclude 'credentials.json' --exclude 'token*.json' --exclude 'tokens.json' --exclude '*cookie*.json'
  --exclude 'storage_state*' --exclude 'discord_credential*' --exclude '.npmrc' --exclude '.netrc')
SECRET_FIND=(-name .env -o -name '.env.*' -o -name '*.pem' -o -name '*.p12' -o -iname '*secret*.json' -o -name 'client_secret*'
  -o -name credentials.json -o -name 'token*.json' -o -iname '*cookie*.json' -o -name 'storage_state*' -o -name 'discord_credential*')
SECRET_RE='(^|/)(\.env(\.[a-z.]+)?|[^/]*\.pem|[^/]*\.p12|[^/]*secret[^/]*\.json|client_secret[^/]*|credentials\.json|tokens?[^/]*\.json|[^/]*cookie[^/]*\.json|storage_state[^/]*|discord_credential[^/]*|\.npmrc|\.netrc)$'

prune_daily() {
  # keep the 7 newest + the 4 newest made on a Sunday. Only our own files.
  local prefix="$1" keep=() f d
  while IFS= read -r f; do keep+=("$f"); done < <(ls -1 "$DEST"/${prefix}_*.tar.zst 2>/dev/null | sort -r | head -7)
  while IFS= read -r f; do
    d=$(basename "$f" | sed -E "s/${prefix}_([0-9]{8}).*/\1/")
    [ "$(date -j -f %Y%m%d "$d" +%u 2>/dev/null)" = "7" ] && echo "$f"
  done < <(ls -1 "$DEST"/${prefix}_*.tar.zst 2>/dev/null | sort -r) | head -4 > "$STATE/.keep_sundays"
  while IFS= read -r f; do keep+=("$f"); done < "$STATE/.keep_sundays"
  for f in "$DEST"/${prefix}_*.tar.zst; do
    [ -e "$f" ] || continue
    printf '%s\n' "${keep[@]}" | grep -qxF "$f" || { rm -f "$f"; log "pruned $(basename "$f")"; }
  done
}
prune() {
  prune_daily data; prune_daily system
  ls -1 "$DEST"/secrets_*.tar.zst.enc 2>/dev/null | sort -r | tail -n +8 | while IFS= read -r f; do rm -f "$f"; log "pruned $(basename "$f")"; done
  ls -1 "$DEST"/media_*.tar 2>/dev/null | sort -r | tail -n +5 | while IFS= read -r f; do rm -f "$f"; log "pruned $(basename "$f")"; done
}

cp -f "$HOME/projects/_meta/scripts/icloud_backup_RESTORE.md" "$DEST/RESTORE.md" 2>/dev/null
log "start mode=$MODE free=$(free_gb)GB"
DATA_MSG=""; MEDIA_MSG=""; SYS_MSG=""; SEC_MSG=""
case "$MODE" in
  data)   run_data ;;
  media)  run_media ;;
  system) run_system ;;
  secrets) run_secrets ;;
  all)    run_data; run_system; run_secrets; run_media ;;
  auto)   run_data; run_system; run_secrets
         if [ "$(date +%u)" = "6" ] || ! ls "$DEST"/media_*.tar >/dev/null 2>&1; then run_media; fi ;;
  *) fail "알 수 없는 모드 $MODE" ;;
esac
prune
TOTAL=$(du -sh "$DEST" | cut -f1)
log "done (iCloud folder $TOTAL)"
notify "✅ iCloud 백업(데이터 창고+맥 복원용) $(date '+%m-%d') — ${DATA_MSG}${SYS_MSG:+ / $SYS_MSG}${SEC_MSG:+ / $SEC_MSG}${MEDIA_MSG:+ / $MEDIA_MSG} · iCloud 백업 합계 $TOTAL$([ -n "$SNAP_WARN" ] && echo ' ⚠️ DB 사본 일부 실패')"
exit 0
