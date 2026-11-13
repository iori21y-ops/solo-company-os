#!/usr/bin/env python3
"""Doc audit — find rules/manuals that no longer match the real system.

Checks (settings in ~/projects/_meta/governance/doc_registry.yaml):
  1. retired   — a retired name/path (cadam-n8n, n8n, old script paths …) still used as if current
  2. missing   — a ~/projects/... path written in a doc that does not exist on disk
  3. plist     — a launchd plist copy in a repo differs from ~/Library/LaunchAgents
  4. status    — a doc says a launchd job is installed/not installed and launchctl says otherwise

Output: ~/projects/_meta/logs/doc_audit.md (report) + doc_audit.json (for the engine dashboard).
  python3 doc_audit.py            # report only
  python3 doc_audit.py --linear   # also open/refresh/close one Linear issue per check (key doc-audit:<check>)
Read-only towards the docs: it never edits a file. Python 3.9 (launchd /usr/bin/python3).
"""
from __future__ import annotations

import fnmatch
import glob
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()
META = HOME / "projects/_meta"
REGISTRY = META / "governance/doc_registry.yaml"
OUT_MD = META / "logs/doc_audit.md"
OUT_JSON = META / "logs/doc_audit.json"
LINEAR = HOME / "projects/_shared/solo_common/linear_alert.py"  # run as a CLI (JSON window), never imported
AGENTS = HOME / "Library/LaunchAgents"
PATH_RE = re.compile(r"(?:~|/Users/kim)/projects/[^\s`'\"|)<>,;*{}\]]+")
LABEL_RE = re.compile(r"com\.[a-z0-9]+\.[A-Za-z0-9_.-]+")


def load_registry() -> dict:
    import yaml
    return yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))


def expand(p: str) -> str:
    return os.path.expanduser(p)


def doc_files(reg: dict) -> list[Path]:
    seen, out = set(), []
    for pat in reg.get("docs", []):
        for f in sorted(glob.glob(expand(pat))):
            if f in seen or not os.path.isfile(f):
                continue
            if any(fnmatch.fnmatch(f, s) for s in reg.get("skip", [])):
                continue
            seen.add(f)
            out.append(Path(f))
    return out


def short(p) -> str:
    return str(p).replace(str(HOME), "~")


def is_history(line: str, markers: list[str]) -> bool:
    return any(m in line for m in markers)


def in_code_fence_map(lines: list[str]) -> list[bool]:
    flags, inside = [], False
    for l in lines:
        if l.strip().startswith("```"):
            inside = not inside
            flags.append(True)
            continue
        flags.append(inside)
    return flags


BANNER_RE = re.compile(r"^\s*>.*(폐기|기록용)")
HEAD_RE = re.compile(r"^(#{1,6})\s")


def live_lines(f: Path) -> list[tuple[int, str]]:
    """(line number, text) of lines that describe the current system.
    Skips: a whole file whose first 20 lines carry a '> … 폐기/기록용' banner, and a section whose heading is
    followed within 3 lines by such a banner (until the next heading of the same or higher level)."""
    lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
    if any(BANNER_RE.match(l) for l in lines[:20]) and not any(HEAD_RE.match(l) and len(HEAD_RE.match(l).group(1)) >= 2 for l in lines[:3]):
        if any(BANNER_RE.match(l) for l in lines[:8]):
            return []
    out, dead_level = [], 0
    for i, l in enumerate(lines):
        m = HEAD_RE.match(l)
        if m:
            lvl = len(m.group(1))
            if dead_level and lvl <= dead_level:
                dead_level = 0
            if not dead_level and any(BANNER_RE.match(x) for x in lines[i + 1:i + 4]):
                dead_level = lvl
        if not dead_level:
            out.append((i + 1, l))
    return out


def check_retired(files, reg) -> list[dict]:
    rules = [(re.compile(r["pattern"]), r) for r in reg.get("retired", [])]
    markers = reg.get("history_markers", [])
    out = []
    for f in files:
        for i, line in live_lines(f):
            if is_history(line, markers):
                continue
            for rx, r in rules:
                if rx.search(line):
                    out.append({"file": short(f), "line": i, "text": line.strip()[:160],
                                "why": f"'{r['pattern']}' 은(는) {r['since']}부터 없음 → {r['now']}"})
                    break
    return out


def check_missing_paths(files, reg) -> list[dict]:
    markers = reg.get("history_markers", [])
    out = []
    for f in files:
        for i, line in live_lines(f):
            if is_history(line, markers):
                continue
            for mo in PATH_RE.finditer(line):
                if line[mo.end():mo.end() + 1] in ("*", "{"):
                    continue  # glob or brace pattern (e.g. weekly_check_*.md) — not a single path
                p = mo.group(0).rstrip(".:")
                if any(c in p for c in "<>$[]") or "YYYY" in p or "MM-DD" in p:
                    continue
                if not os.path.exists(expand(p.replace("/Users/kim", "~"))):
                    out.append({"file": short(f), "line": i, "text": line.strip()[:160], "why": f"경로 없음: {p}"})
    return out


def check_plists(reg) -> list[dict]:
    out = []
    for d in reg.get("plist_copies", []):
        for f in sorted(glob.glob(os.path.join(expand(d), "*.plist"))):
            real = AGENTS / os.path.basename(f)
            if not real.exists():
                out.append({"file": short(f), "line": 0, "text": "", "why": "LaunchAgents에 원본 없음 (설치 안 된 사본이거나 폐기된 작업)"})
            elif Path(f).read_bytes() != real.read_bytes():
                out.append({"file": short(f), "line": 0, "text": "", "why": f"원본({short(real)})과 내용이 다름"})
    return out


def loaded_labels() -> set[str]:
    try:
        r = subprocess.run(["launchctl", "list"], capture_output=True, text=True, timeout=20)
        return {l.split("\t")[-1] for l in r.stdout.splitlines()[1:] if "\t" in l}
    except Exception:
        return set()


def check_status(files, reg) -> list[dict]:
    words = reg.get("status_words", {})
    loaded = loaded_labels()
    if not loaded:
        return []
    out = []
    for f in files:
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            labels = [l.rstrip(".") for l in LABEL_RE.findall(line)]
            labels = [l[:-6] if l.endswith(".plist") else l for l in labels]
            if not labels:
                continue
            says_off = any(w in line for w in words.get("off", []))
            says_on = any(w in line for w in words.get("on", []))
            if says_off == says_on:  # nothing or ambiguous
                continue
            for lab in labels:
                if says_off and lab in loaded:
                    out.append({"file": short(f), "line": i, "text": line.strip()[:160], "why": f"{lab}: 문서는 꺼짐/미설치, 실제는 켜져 있음"})
                elif says_on and lab not in loaded and (AGENTS / f"{lab}.plist").exists():
                    out.append({"file": short(f), "line": i, "text": line.strip()[:160], "why": f"{lab}: 문서는 켜짐, 실제는 내려져 있음"})
    return out


def code_files(reg: dict) -> list[Path]:
    skip = set(reg.get("code_skip_dirs", []))
    seen, out = set(), []
    for pat in reg.get("code", []):
        for f in glob.glob(expand(pat), recursive=True):
            if f in seen or not os.path.isfile(f) or skip.intersection(Path(f).parts):
                continue
            seen.add(f)
            out.append(Path(f))
    return sorted(out)


def check_code(reg) -> list[dict]:
    rules = [(re.compile(r["pattern"]), r) for r in reg.get("code_retired", [])]
    markers = reg.get("code_markers", [])
    out = []
    for f in code_files(reg):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if len(line) > 400 or any(m in line for m in markers):
                continue
            for rx, r in rules:
                if rx.search(line):
                    out.append({"file": short(f), "line": i, "text": line.strip()[:160], "why": f"옛 경로·주소 → {r['now']}"})
                    break
    return out


CHECKS = {
    "retired": "없어진 이름·경로가 현재처럼 적힌 줄",
    "missing": "적힌 경로가 실제로 없음",
    "plist": "예약 작업 설정 사본이 원본과 다름",
    "status": "예약 작업 상태가 문서와 실제가 다름",
    "code": "코드·예약 작업 설정에 남은 옛 경로·주소",
}


def linear_sync(results: dict) -> None:
    items = []
    for key, rows in results.items():
        if not rows:
            continue
        files = sorted({r["file"] for r in rows})
        body = (f"문서 점검(`_meta/scripts/doc_audit.py`)이 찾은 **{CHECKS[key]}** {len(rows)}건 ({len(files)}개 문서).\n\n"
                f"전체 목록: `~/projects/_meta/logs/doc_audit.md`. 고치는 법: `_meta/governance/DOCS_RULES.md` §구조 변경 후 문서 정리.\n\n"
                + "\n".join(f"- {r['file']}:{r['line']} — {r['why']}" for r in rows[:30])
                + ("\n- …" if len(rows) > 30 else ""))
        items.append({"key": f"doc-audit:{key}", "title": f"[문서 점검] {CHECKS[key]} {len(rows)}건", "body": body})
    try:
        subprocess.run([sys.executable, str(LINEAR), "sync", "doc-audit:"], input=json.dumps(items, ensure_ascii=False),
                       text=True, timeout=120)
    except Exception as e:
        print(f"[doc_audit] linear sync failed: {e}", file=sys.stderr)


def main() -> int:
    reg = load_registry()
    files = doc_files(reg)
    results = {
        "retired": check_retired(files, reg),
        "missing": check_missing_paths(files, reg),
        "plist": check_plists(reg),
        "status": check_status(files, reg),
        "code": check_code(reg),
    }
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    md = [f"# 문서 점검 결과 ({now})", "", f"점검한 문서 {len(files)}개. 설정 `_meta/governance/doc_registry.yaml`.", ""]
    for key, rows in results.items():
        md.append(f"## {CHECKS[key]} — {len(rows)}건")
        md += [f"- `{r['file']}:{r['line']}` — {r['why']}" + (f"  \n  > {r['text']}" if r["text"] else "") for r in rows] or ["- 없음"]
        md.append("")
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    OUT_JSON.write_text(json.dumps({"at": now, "docs": len(files), "counts": {k: len(v) for k, v in results.items()},
                                    "results": results}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(" · ".join(f"{CHECKS[k]} {len(v)}" for k, v in results.items()), f"(문서 {len(files)}개) → {short(OUT_MD)}")
    if "--linear" in sys.argv:
        linear_sync(results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
