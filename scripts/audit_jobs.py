#!/usr/bin/env python3
"""Auto job coverage for audit-agent.sh (2026-11-13).

Reads every loaded LaunchAgent of ours from ~/Library/LaunchAgents instead of a hand-written list, and prints
findings in audit-agent's format, one per line:  CODE|SEV|label|description
  A1  resident (KeepAlive) service loaded but no process
  A1  scheduled job failed N audits in a row (exit != 0; for scheduled jobs SIGTERM -15/143 counts as a failure)
  A4  job log not updated for more than 2 x its schedule period
Usage:
  audit_jobs.py --streak FILE            # print findings, update the streak file
  audit_jobs.py --streak FILE --dry-run  # print findings, keep the streak file
  audit_jobs.py --table                  # print the coverage table (what is watched and how)
Exit 0 unless this script itself breaks.
"""
import argparse, glob, os, plistlib, subprocess, sys, time
from pathlib import Path

HOME = Path.home()
AGENTS = HOME / "Library/LaunchAgents"
PREFIXES = ("com.cadam.", "com.rentailor.", "com.blogengine.", "com.importlease.", "com.iori21y.",
            "com.kim.", "com.solo.", "com.user.secondbrain.", "homebrew.mxcl.postgresql")
FRESH_MULT = 2          # owner decision 2026-11-13: alert after 2 x schedule period
STREAK_N = 2            # consecutive failing audits before alerting
POLLER_MAX = 3600       # interval jobs at or below this only log when they have work -> no log-age check

DAY = 86400
# Jobs that write their real log somewhere other than StandardOutPath. Newest mtime among these wins.
REAL_LOGS = {
    "com.kim.keyword-scan": [str(HOME / "projects/_data/shared/collected/keyword-scan/logs/*.log")],
    "com.user.secondbrain.ingest": [str(HOME / "second-brain-git/logs/cron.log"), str(HOME / "second-brain/logs/cron.log")],
    "com.cadam.audit": [str(HOME / "projects/_meta/audit/audit.log")],
    "com.rentailor.health-check": [str(HOME / "projects/_meta/logs/health-check.log")],
    "com.cadam.data-registry": [str(HOME / "projects/cadam/docs/data-registry-counts.md")],
}
# Not checked for log age (reason in the value). Exit status is still checked.
NO_LOG_AGE = {
    "com.kim.ollama-env": "runs once at login",
}


def launchctl_state(label):
    uid = os.getuid()
    out = subprocess.run(["launchctl", "print", f"gui/{uid}/{label}"], capture_output=True, text=True).stdout
    st = {"loaded": bool(out), "pid": None, "exit": None, "runs": 0}
    for line in out.splitlines():
        s = line.strip()
        if s.startswith("pid = "):
            st["pid"] = s.split("= ", 1)[1]
        elif s.startswith("last exit code = "):
            v = s.split("= ", 1)[1]
            st["exit"] = None if "never" in v else v.split(":")[0].strip()
        elif s.startswith("last terminating signal = "):  # killed jobs report a signal, not an exit code
            st["exit"] = "signal " + s.split("= ", 1)[1].split(":")[-1].strip()
        elif s.startswith("runs = "):
            st["runs"] = int(s.split("= ", 1)[1])
    return st


def period_of(d):
    """Schedule period in seconds (the coarsest unit, so multi-slot schedules are not over-alerted)."""
    if "StartInterval" in d:
        return int(d["StartInterval"])
    c = d.get("StartCalendarInterval")
    if c is None:
        return None
    entries = c if isinstance(c, list) else [c]
    keys = set().union(*[set(e) for e in entries])
    if "Month" in keys:
        return 366 * DAY
    if "Day" in keys:
        return 31 * DAY
    if "Weekday" in keys:
        return 7 * DAY
    if "Hour" in keys:
        return DAY
    return 3600


def newest_mtime(label, d):
    paths = []
    for g in REAL_LOGS.get(label, []):
        paths += glob.glob(g)
    if not REAL_LOGS.get(label):
        paths += [p for p in (d.get("StandardOutPath"), d.get("StandardErrorPath")) if p and p != "/dev/null"]
    ms, blocked = [], False
    for p in paths:
        try:
            ms.append(os.stat(p).st_mtime)
        except PermissionError:  # iCloud (~/second-brain) is closed to launchd-started python
            blocked = True
        except OSError:
            pass
    if not ms and blocked:
        return "blocked"
    return max(ms) if ms else None


def jobs():
    for f in sorted(AGENTS.glob("*.plist")):
        try:
            d = plistlib.load(open(f, "rb"))
        except Exception as e:
            yield f.name, None, f"plist unreadable: {e}"
            continue
        label = d.get("Label", "")
        if label.startswith(PREFIXES):
            yield label, d, f


def human(sec):
    return f"{sec / DAY:.1f}일" if sec >= DAY else f"{sec / 3600:.0f}시간"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--streak")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--table", action="store_true")
    a = ap.parse_args()

    prev = {}
    if a.streak and os.path.exists(a.streak):
        for line in open(a.streak):
            p = line.split()
            if len(p) == 2 and p[1].isdigit():
                prev[p[0]] = int(p[1])
    new_streak, findings, table = {}, [], []
    now = time.time()

    for label, d, f in jobs():
        if d is None:
            findings.append(f"A1|med|{label}|{f}")
            continue
        st = launchctl_state(label)
        if not st["loaded"]:
            continue  # plist present but not loaded = deliberately off (football writers etc.)
        resident = bool(d.get("KeepAlive"))
        period = period_of(d)
        kind = "resident" if resident else (f"every {period}s" if "StartInterval" in d else f"cal {human(period)}" if period else "atload")
        table.append(f"{label}\t{kind}\t{'pid ' + st['pid'] if st['pid'] else 'exit ' + str(st['exit'])}")

        if resident:
            if not st["pid"]:
                findings.append(f"A1|high|{label}|상주(KeepAlive) 서비스인데 프로세스 없음 — 죽음 의심(마지막 종료 코드 {st['exit']})")
            continue

        # exit status streak (scheduled/interval jobs; SIGTERM counts as failure — owner decision 2026-11-13)
        cur = 0
        if st["exit"] not in (None, "0"):
            cur = prev.get(label, 0) + 1
        new_streak[label] = cur
        if cur >= STREAK_N:
            findings.append(f"A1|med|{label}|예약 작업 연속 실패 {cur}회(종료 코드 {st['exit']}) — 구조적 실패 의심")

        # log age
        if label in NO_LOG_AGE or not period or ("StartInterval" in d and period <= POLLER_MAX):
            continue
        limit = period * FRESH_MULT
        m = newest_mtime(label, d)
        if m == "blocked":
            continue  # cannot read the log here; not evidence that the job stopped
        loaded_at = os.path.getmtime(f)  # plist rewritten = job (re)loaded; give it one full window
        if m is None:
            if now - loaded_at > limit:
                findings.append(f"A4|med|{label}|로그 파일 없음 — 등록 후 {human(now - loaded_at)} 지나도록 실행 흔적 없음")
            continue
        age = now - m
        if age > limit:
            findings.append(f"A4|med|{label}|로그 정지 — 마지막 기록 {human(age)} 전(주기 {human(period)}의 {FRESH_MULT}배 초과)")

    if a.table:
        print("\n".join(table))
        return
    if a.streak and not a.dry_run:
        Path(a.streak).write_text("".join(f"{k} {v}\n" for k, v in sorted(new_streak.items())))
    print("\n".join(findings))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # never block the audit
        print(f"A1|med|audit_jobs.py|자동 감시 스크립트 오류: {e}")
