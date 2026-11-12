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
#   daily  -> Supabase (site DB) read-only pg_dump -> _data/rentailor/backups/auto/supabase/ (14 kept), then into data_
#             (temporary read-only login role from the Management API; no stored DB password)
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
MODE="${1:-auto}"   # auto | supabase | data | system | secrets | media | all

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

run_supabase() {
  # Owner-approved 2026-11-13: daily READ-ONLY pg_dump of the production Supabase DB (the Rentailor site DB),
  # because the free plan gives no downloadable backup. No DB password is stored anywhere: each run asks the
  # Management API (SUPABASE_ACCESS_TOKEN in ~/.cadam-secrets/secrets.env) for a temporary CLI login role
  # (300s TTL — the same mechanism `supabase db dump` uses), connects with default_transaction_read_only=on
  # (owner-approved 2026-11-13), dumps through the session pooler, then deletes the role. Dumps land in _data/rentailor/backups/auto/supabase/ (14 kept).
  local dir="$WH/rentailor/backups/auto/supabase" out tmp
  mkdir -p "$dir"; out="$dir/supabase-$(date +%F).dump"; tmp="$out.partial"
  ( set -a; source "$HOME/.cadam-secrets/secrets.env" >/dev/null 2>&1; set +a
    /usr/bin/python3 - "$tmp" <<'PY'
import os, sys, json, subprocess, urllib.request
ref, tok = os.environ.get("SUPABASE_PROJECT_REF", ""), os.environ.get("SUPABASE_ACCESS_TOKEN", "")
if not ref or not tok: sys.exit("missing SUPABASE_PROJECT_REF/ACCESS_TOKEN")
api = f"https://api.supabase.com/v1/projects/{ref}"
def call(method, path, body=None):
    r = urllib.request.Request(api + path, method=method, headers={"Authorization": "Bearer " + tok,
        "Content-Type": "application/json", "User-Agent": "solo-backup"}, data=json.dumps(body).encode() if body is not None else None)
    with urllib.request.urlopen(r, timeout=30) as f: t = f.read(); return json.loads(t) if t else {}
pool = call("GET", "/config/database/pooler"); pool = pool[0] if isinstance(pool, list) else pool
# Owner decision 2026-11-13: the read-only role cannot read locked-down tables (consultations, ...), so use the
# normal CLI login role (300s TTL, deleted after) but force every transaction read-only; pg_dump only reads.
role = call("POST", "/cli/login-role", {"read_only": False})
try:
    env = dict(os.environ, PGHOST=pool["db_host"], PGPORT="5432", PGUSER=f'{role["role"]}.{ref}', PGPASSWORD=role["password"],
               PGDATABASE="postgres", PGSSLMODE="require", PGCONNECT_TIMEOUT="20", PGOPTIONS="-c default_transaction_read_only=on")
    # Only the public schema: every site table lives there (no custom schemas in migrations or site code,
    # checked 2026-11-13). Supabase-managed schemas (auth, storage, ...) are locked even for the CLI login role.
    args = ["pg_dump", "-Fc", "--no-owner", "--no-privileges", "-n", "public", "-f", sys.argv[1]]
    # a fresh login role needs a few seconds to reach the pooler ("password authentication failed") — retry
    import time
    for attempt in range(10):
        time.sleep(3 if attempt == 0 else 5)
        p = subprocess.run(args, env=env, stderr=subprocess.PIPE, text=True)
        rc = p.returncode
        if rc == 0 or not any(m in p.stderr for m in ("password authentication failed", "Network is unreachable", "timeout expired")): break
        print(f"pg_dump connect not ready ({p.stderr.strip().splitlines()[0][:120] if p.stderr.strip() else rc}), retry {attempt + 1}", file=sys.stderr)
    if rc != 0: sys.stderr.write(p.stderr)
finally:
    try: call("DELETE", "/cli/login-role")
    except Exception as e: print("login-role delete failed:", e, file=sys.stderr)
sys.exit(rc)
PY
  ) 2>>"$LOG"
  local rc=$?
  if [ $rc -ne 0 ] || ! pg_restore -l "$tmp" >/dev/null 2>&1; then
    rm -f "$tmp"; SB_MSG="❌ Supabase 백업 실패(rc $rc)"; SB_FAIL=1; log "supabase FAIL rc=$rc"; return; fi
  mv -f "$tmp" "$out"
  local tables; tables=$(pg_restore -l "$out" | grep -c ' TABLE DATA ')
  ls -1 "$dir"/supabase-*.dump 2>/dev/null | sort -r | tail -n +15 | while IFS= read -r f; do rm -f "$f"; log "pruned $(basename "$f")"; done
  SB_MSG="Supabase DB $(du -h "$out" | cut -f1) · 표 ${tables}개"
  log "supabase ok: $out ($tables tables with data)"
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
DATA_MSG=""; MEDIA_MSG=""; SYS_MSG=""; SEC_MSG=""; SB_MSG=""; SB_FAIL=""
case "$MODE" in
  data)   run_data ;;
  media)  run_media ;;
  system) run_system ;;
  secrets) run_secrets ;;
  supabase) run_supabase ;;
  all)    run_supabase; run_data; run_system; run_secrets; run_media ;;
  auto)   run_supabase; run_data; run_system; run_secrets
         if [ "$(date +%u)" = "6" ] || ! ls "$DEST"/media_*.tar >/dev/null 2>&1; then run_media; fi ;;
  *) fail "알 수 없는 모드 $MODE" ;;
esac
prune
TOTAL=$(du -sh "$DEST" | cut -f1)
log "done (iCloud folder $TOTAL)"
notify "$([ -n "$SB_FAIL" ] && echo ❌ || echo ✅) iCloud 백업(데이터 창고+맥 복원용) $(date '+%m-%d') — ${SB_MSG:+$SB_MSG / }${DATA_MSG}${SYS_MSG:+ / $SYS_MSG}${SEC_MSG:+ / $SEC_MSG}${MEDIA_MSG:+ / $MEDIA_MSG} · iCloud 백업 합계 $TOTAL$([ -n "$SNAP_WARN" ] && echo ' ⚠️ DB 사본 일부 실패')"
exit 0
