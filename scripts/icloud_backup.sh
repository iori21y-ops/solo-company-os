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
# Keep: data = 7 newest + 4 newest Sunday archives; media = 4 newest.
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
MODE="${1:-auto}"   # auto | data | media | all

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

prune() {
  # data: keep 7 newest + 4 newest that were made on a Sunday. media: keep 4 newest. Only our own files.
  local keep=() f d
  while IFS= read -r f; do keep+=("$f"); done < <(ls -1 "$DEST"/data_*.tar.zst 2>/dev/null | sort -r | head -7)
  while IFS= read -r f; do
    d=$(basename "$f" | sed -E 's/data_([0-9]{8}).*/\1/')
    [ "$(date -j -f %Y%m%d "$d" +%u 2>/dev/null)" = "7" ] && echo "$f"
  done < <(ls -1 "$DEST"/data_*.tar.zst 2>/dev/null | sort -r) | head -4 > "$STATE/.keep_sundays"
  while IFS= read -r f; do keep+=("$f"); done < "$STATE/.keep_sundays"
  for f in "$DEST"/data_*.tar.zst; do
    [ -e "$f" ] || continue
    printf '%s\n' "${keep[@]}" | grep -qxF "$f" || { rm -f "$f"; log "pruned $(basename "$f")"; }
  done
  ls -1 "$DEST"/media_*.tar 2>/dev/null | sort -r | tail -n +5 | while IFS= read -r f; do rm -f "$f"; log "pruned $(basename "$f")"; done
}

log "start mode=$MODE free=$(free_gb)GB"
DATA_MSG=""; MEDIA_MSG=""
case "$MODE" in
  data)  run_data ;;
  media) run_media ;;
  all)   run_data; run_media ;;
  auto)  run_data
         if [ "$(date +%u)" = "6" ] || ! ls "$DEST"/media_*.tar >/dev/null 2>&1; then run_media; fi ;;
  *) fail "알 수 없는 모드 $MODE" ;;
esac
prune
TOTAL=$(du -sh "$DEST" | cut -f1)
log "done (iCloud folder $TOTAL)"
notify "✅ iCloud 데이터 창고 백업 $(date '+%m-%d') — ${DATA_MSG}${MEDIA_MSG:+ / $MEDIA_MSG} · iCloud 백업 합계 $TOTAL$([ -n "$SNAP_WARN" ] && echo ' ⚠️ DB 사본 일부 실패')"
exit 0
