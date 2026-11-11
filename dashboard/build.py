#!/usr/bin/env python3
"""Engine dashboard: reads the real files (engine settings, rules, work files, launchd, logs, data registries, COMPAT_LIST)
and writes one self-contained page — nothing here is typed by hand, so a rebuild always shows the current state.

  python3 ~/projects/_meta/dashboard/build.py [--open]     → ~/projects/_meta/dashboard/index.html

Read-only: it changes nothing but its own index.html. It imports no project code (files are read as text / JSON / YAML).
Engines come from engines.yaml; a new engine = one entry there + (for a new kind) one reader function below.
"""
from __future__ import annotations

import html
import json
import plistlib
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
HOME = Path.home()
NOW = datetime.now()
WEEKDAYS = "일월화수목금토"


def P(s) -> Path:
    return Path(str(s).replace("~", str(HOME), 1)) if str(s).startswith("~") else Path(str(s))


def esc(x) -> str:
    return html.escape("" if x is None else str(x))


def short(p) -> str:
    return str(p).replace(str(HOME / "projects") + "/", "").replace(str(HOME), "~")


def ago(ts: float | None) -> str:
    if not ts:
        return "-"
    d = NOW - datetime.fromtimestamp(ts)
    if d < timedelta(minutes=1):
        return "방금"
    if d < timedelta(hours=1):
        return f"{int(d.total_seconds() // 60)}분 전"
    if d < timedelta(days=1):
        return f"{int(d.total_seconds() // 3600)}시간 전"
    return f"{d.days}일 전"


def mtime(p: Path) -> float | None:
    try:
        return p.stat().st_mtime
    except OSError:
        return None


def day(ts: float | None) -> str:
    return datetime.fromtimestamp(ts).strftime("%m-%d %H:%M") if ts else "-"


def pill(text: str, kind: str = "") -> str:
    return f'<span class="pill {kind}">{esc(text)}</span>'


def table(head: list, rows: list, cls: str = "") -> str:
    """rows: lists of already-escaped HTML cells."""
    if not rows:
        return '<p class="muted">없음</p>'
    th = "".join(f"<th>{esc(h)}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tw"><table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def md_inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)


def md_tables(text: str) -> list[dict]:
    """Every markdown table in the text: {"heading": nearest heading above, "head": [...], "rows": [[...]]}."""
    out, heading, lines = [], "", text.split("\n")
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("#"):
            heading = ln.lstrip("# ").strip()
        if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|\s*$", lines[i + 1]):
            cells = lambda x: [c.strip() for c in re.split(r"(?<!\\)\|", x.strip().strip("|"))]   # noqa: E731
            head, rows = cells(ln), []
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(cells(lines[i]))
                i += 1
            out.append({"heading": heading, "head": head, "rows": rows})
            continue
        i += 1
    return out


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return ""


def read_json(p: Path, default=None):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


# ── launchd ──────────────────────────────────────────────────────────────
def schedule_text(d: dict) -> str:
    cal = d.get("StartCalendarInterval")
    if cal:
        items = cal if isinstance(cal, list) else [cal]
        parts = []
        for c in items:
            t = f"{c.get('Hour', 0):02d}:{c.get('Minute', 0):02d}" if "Hour" in c else f"매시 {c.get('Minute', 0):02d}분"
            if "Weekday" in c:
                parts.append(f"{WEEKDAYS[c['Weekday'] % 7]} {t}")
            elif "Day" in c:
                parts.append(f"매월 {c['Day']}일 {t}")
            else:
                parts.append(f"매일 {t}")
        if len(parts) > 4:
            return f"{parts[0]} 외 {len(parts) - 1}회"
        return " · ".join(parts)
    if d.get("StartInterval"):
        n = int(d["StartInterval"])
        return f"{n // 3600}시간마다" if n % 3600 == 0 else f"{n // 60}분마다" if n >= 60 else f"{n}초마다"
    if d.get("KeepAlive") or d.get("RunAtLoad"):
        return "상시 실행"
    return "수동"


def last_line(p: Path) -> str:
    try:
        with open(p, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 4000))
            lines = f.read().decode("utf-8", "replace").split("\n")
    except OSError:
        return ""
    for ln in reversed(lines):
        s = ln.strip()
        if s and "NotOpenSSLWarning" not in s and "warnings.warn" not in s:
            return s[:150]
    return ""


def launchd_jobs(prefixes: list) -> list[dict]:
    loaded = {}
    try:
        for ln in subprocess.run(["launchctl", "list"], capture_output=True, text=True, timeout=20).stdout.split("\n")[1:]:
            p = ln.split("\t")
            if len(p) == 3:
                loaded[p[2]] = (p[0], p[1])
    except Exception:  # noqa: BLE001 — the page still builds without live status
        pass
    jobs = []
    for f in sorted((HOME / "Library/LaunchAgents").glob("*.plist")):
        try:
            d = plistlib.loads(f.read_bytes())
        except Exception:  # noqa: BLE001
            continue
        label = d.get("Label", f.stem)
        if not any(label.startswith(p) for p in prefixes):
            continue
        args = [str(a) for a in d.get("ProgramArguments") or [d.get("Program", "")]]
        cmd = " ".join(short(a) for a in args if a not in ("/usr/bin/python3", "/bin/bash", "/bin/sh", "/bin/zsh", "-c", "-lc"))
        m = re.search(r"projects/([^/\s]+)", " ".join(args) + " " + str(d.get("WorkingDirectory", "")))
        log = Path(d["StandardOutPath"]) if d.get("StandardOutPath") else None
        pid, code = loaded.get(label, (None, None))
        if label not in loaded:
            state, kind = "꺼짐(미등록)", "off"
        elif pid and pid != "-":
            state, kind = "실행 중", "run"
        elif code == "0":
            state, kind = "정상", "ok"
        else:
            state, kind = f"오류(종료 코드 {code})", "bad"
        jobs.append({"label": label, "cmd": cmd, "raw": " ".join(args), "project": m.group(1) if m else "-", "schedule": schedule_text(d),
                     "state": state, "kind": kind, "log": log, "log_m": mtime(log) if log else None, "log_last": last_line(log) if log else ""})
    return jobs


def jobs_table(jobs: list[dict], with_project: bool = True) -> str:
    rows = []
    for j in jobs:
        rows.append([f"<b>{esc(j['label'])}</b>", *([esc(j["project"])] if with_project else []), esc(j["schedule"]), pill(j["state"], j["kind"]),
                     f"<code>{esc(j['cmd'][:110])}</code>", f"{esc(ago(j['log_m']))}<div class='muted small'>{esc(j['log_last'][:120])}</div>"])
    return table(["예약 작업", *(["프로젝트"] if with_project else []), "주기", "상태", "실행하는 것", "마지막 기록"], rows, "jobs")


# ── blog engine ──────────────────────────────────────────────────────────
STATUS_KO = {"published": "발행됨", "review": "승인 대기", "queued": "발행 대기열", "draft": "초안", "cancelled": "버림", "edited": "수정 발행",
             "publishing": "발행 중", "rejected": "반려", "discarded": "버림", "done": "완료", "pending": "대기"}
KEY_KO = {"discord_content_name": "디스코드 글 채널", "discord_content": "디스코드 글 채널", "discord_system": "디스코드 시스템 채널", "naver": "네이버 블로그",
          "youtube": "유튜브", "wordpress": "워드프레스", "blog_id": "블로그 ID", "server": "발행 서버", "channel": "채널", "url": "주소", "category": "카테고리"}
STATUS_KIND = {"published": "ok", "edited": "ok", "done": "ok", "review": "warn", "queued": "warn", "publishing": "run", "cancelled": "off", "discarded": "off", "rejected": "off"}


def hold_cards(b: dict) -> tuple[str, bool]:
    out, any_on = [], False
    seen = {}
    for kind, path in (b.get("hold") or {}).items():
        seen.setdefault(path, []).append({"writing": "글쓰기", "publishing": "발행"}.get(kind, kind))
    for path, kinds in seen.items():
        p = P(path)
        on = p.exists()
        any_on |= on
        note = read(p).strip()[:80] if on else ""
        out.append(f'<div class="kv"><span>{esc("·".join(kinds))} 보류</span><span>{pill("보류 중" if on else "꺼짐(정상 진행)", "warn" if on else "ok")}'
                   f'<div class="muted small">{esc(note)} · <code>{esc(short(p))}</code></div></span></div>')
    return "".join(out) or '<p class="muted">보류 스위치 없음</p>', any_on


def rules_block(root: Path) -> tuple[str, int]:
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.name not in (".DS_Store",))
    rows = []
    for p in files:
        text = read(p)
        first = next((ln.strip().lstrip("# ") for ln in text.split("\n") if ln.strip()), "")
        rows.append([f"<code>{esc(p.relative_to(root))}</code>", esc(first[:90]), f"{len(text):,}자", esc(day(mtime(p)))])
    log = read(root / "CHANGELOG.md").strip().split("\n")
    recent = [ln for ln in log if ln.strip().startswith(("-", "*", "|", "20"))][-5:]
    extra = ("<h4>최근 규칙 변경</h4><ul>" + "".join(f"<li>{md_inline(ln.lstrip('-* '))}</li>" for ln in recent) + "</ul>") if recent else ""
    return table(["규칙 파일", "첫 줄", "분량", "고친 때"], rows) + extra, len(files)


def facts_block(cfg: dict) -> str:
    p = P(cfg.get("facts_cli", ""))
    text = read(p)
    if not text:
        return '<p class="muted">데이터 창구 없음</p>'
    names = [n for n in re.findall(r"^def ([a-z]\w*)\(", text, flags=re.M) if n != "main"]
    m = re.search(r"^COMMANDS = \(([^)]*)\)", text, flags=re.M)
    commands = set(re.findall(r'"(\w+)"', m.group(1))) if m else set()
    chips = "".join(f'<span class="chip {"cmd" if n in commands else ""}">{esc(n)}</span>' for n in names)
    return (f'<p>엔진이 사업 프로젝트의 데이터를 받는 유일한 길: <code>{esc(short(p))}</code> — 명령 {len(names)}개'
            f'{f" (그중 데이터를 바꾸는 명령 {len(commands)}개, 주황색)" if commands else ""}</p><div class="chips">{chips}</div>')


def football_posts(outbox: Path) -> dict:
    posts = [read_json(p, {}) for p in sorted((outbox / "posts").glob("*.json"))]
    posts = [p for p in posts if p.get("key")]
    week = (NOW - timedelta(days=7)).isoformat()
    rows = []
    for s in sorted(posts, key=lambda s: s.get("created_at", ""), reverse=True)[:15]:
        url = s.get("naver_url") or ""
        title = f'<a href="{esc(url)}">{esc(s.get("title", ""))}</a>' if url.startswith("http") else esc(s.get("title", ""))
        v = (s.get("video") or {}).get("status")
        rows.append([esc(s["key"]), title, esc(s.get("category", "")), pill(STATUS_KO.get(s.get("status"), s.get("status", "")), STATUS_KIND.get(s.get("status"), "")),
                     esc((s.get("published_at") or s.get("created_at") or "")[5:16].replace("T", " ")), esc(v or "")])
    cands = sorted((outbox / "candidates").glob("20*.json"))
    return {"counts": Counter(s.get("status") for s in posts), "total": len(posts),
            "week": sum(1 for s in posts if s.get("status") in ("published", "edited") and (s.get("published_at") or "") >= week),
            "last_pub": max((s.get("published_at") or "" for s in posts if s.get("status") == "published"), default=""),
            "table": table(["글", "제목", "카테고리", "상태", "발행·작성", "영상"], rows),
            "cand": cands[-1].stem if cands else "-"}


def rentailor_outbox(outbox: Path) -> dict:
    drafts = [read_json(p, {}) for p in sorted((outbox / "naver").glob("20*.json"))]
    drafts = [d for d in drafts if d.get("key")]
    rows = []
    for d in sorted(drafts, key=lambda d: d.get("key", ""), reverse=True)[:15]:
        url = d.get("naver_url") or d.get("url") or ""
        title = f'<a href="{esc(url)}">{esc(d.get("title", ""))}</a>' if str(url).startswith("http") else esc(d.get("title", ""))
        rows.append([esc(d["key"]), esc(d.get("keyword", "")), title, esc(d.get("kind", "")),
                     pill(STATUS_KO.get(d.get("status"), d.get("status", "")), STATUS_KIND.get(d.get("status"), ""))])
    cands = sorted((outbox / "candidates").glob("20*.json"))
    dirs = [[f"<code>{esc(p.name)}/</code>", f"{sum(1 for _ in p.iterdir()):,}개", esc(day(max((mtime(x) or 0 for x in p.iterdir()), default=0) or None))]
            for p in sorted(outbox.iterdir()) if p.is_dir()]
    return {"counts": Counter(d.get("status") for d in drafts), "total": len(drafts),
            "table": table(["네이버 초안", "글감", "제목", "유형", "상태"], rows), "cand": cands[-1].stem if cands else "-",
            "dirs": table(["작업 폴더", "파일", "마지막 변경"], dirs)}


def registry_block(cfg: dict) -> str:
    text = read(P(cfg.get("registry", "")))
    if not text:
        return '<p class="muted">데이터 목록 문서 없음</p>'
    out = [f'<p class="muted small">원본: <code>{esc(short(P(cfg["registry"])))}</code> · {esc(day(mtime(P(cfg["registry"]))))} 갱신</p>']
    for t in md_tables(text)[:6]:
        rows = [[md_inline(c) for c in r] + [""] * (len(t["head"]) - len(r)) for r in t["rows"]]
        out.append(f'<details {"open" if len(out) == 1 else ""}><summary>{esc(t["heading"] or "표")} <span class="muted">({len(rows)}줄)</span></summary>{table(t["head"], rows, "reg")}</details>')
    counts = read(P(cfg.get("registry_counts", ""))) if cfg.get("registry_counts") else ""
    bullets = [ln[2:] for ln in counts.split("\n") if ln.startswith("- ")]
    if bullets:
        out.append("<details><summary>표별 행 수</summary><ul>" + "".join(f"<li>{md_inline(b)}</li>" for b in bullets) + "</ul></details>")
    return "".join(out)


def health_block(cfg: dict) -> tuple[str, int]:
    st = read_json(P(cfg.get("health_state", "")), None) if cfg.get("health_state") else None
    if not st:
        return "", 0
    rows, n_prob = [], 0
    for cmd, r in sorted((st.get("runs") or {}).items(), key=lambda kv: kv[1].get("start", ""), reverse=True):
        probs = r.get("problems") or []
        n_prob += bool(probs)
        rows.append([f"<b>{esc(cmd)}</b>", esc(r.get("start", "")[5:16].replace("T", " ")), pill("문제 있음" if probs else ("잠금으로 건너뜀" if r.get("busy") else "정상"), "bad" if probs else ("warn" if r.get("busy") else "ok")),
                     esc("; ".join(probs)[:200])])
    alerts = sorted((st.get("last_alert") or {}).items(), key=lambda kv: kv[1], reverse=True)[:6]
    extra = "<h4>최근 디스코드 경고</h4><ul>" + "".join(f"<li><code>{esc(k)}</code> — {esc(v[5:16].replace('T', ' '))}</li>" for k, v in alerts) + "</ul>" if alerts else ""
    return "<h4>자동 점검(마지막 실행)</h4>" + table(["명령", "시작", "결과", "문제"], rows) + extra, n_prob


def compat_block(path: Path) -> tuple[str, int, int]:
    text = read(path)
    out, total, overdue = [], 0, 0
    today = NOW.strftime("%Y-%m-%d")
    for t in md_tables(text):
        rows = []
        for r in t["rows"]:
            due = r[-1] if r else ""
            m = re.search(r"20\d\d-\d\d-\d\d", due)
            late = bool(m and m.group(0) < today)
            soon = bool(m and today <= m.group(0) <= (NOW + timedelta(days=14)).strftime("%Y-%m-%d"))
            total += 1
            overdue += late
            cells = [md_inline(c) for c in r[:-1]] + [pill(due, "bad" if late else "warn" if soon else "")]
            rows.append(cells + [""] * (len(t["head"]) - len(cells)))
        out.append(f"<h3>{esc(t['heading'])}</h3>" + table(t["head"], rows, "reg"))
    head = re.search(r"마지막 점검[^\n]*", text)
    return (f'<p class="muted">{esc(head.group(0)) if head else ""} · 원본 <code>{esc(short(path))}</code></p>' + "".join(out)), total, overdue


def blog_engine(e: dict, jobs: list[dict], compat: tuple) -> tuple[str, list[str]]:
    root = P(e["root"])
    brands_html, kpis, nav = [], [], []
    for bdir in sorted((root / "brands").glob("*/brand.yaml")):
        name = bdir.parent.name
        b = yaml.safe_load(read(bdir)) or {}
        cfg = (e.get("brands") or {}).get(name, {})
        outbox = bdir.parent / "outbox"
        holds, on = hold_cards(b)
        mine = [j for j in jobs if any(p in j["raw"] for p in cfg.get("job_patterns", []))]
        rules_html, n_rules = rules_block(bdir.parent / "rules")
        health_html, n_prob = health_block(cfg)
        pubs = "".join(f'<div class="kv"><span>{esc(KEY_KO.get(k, k))}</span><span>{esc(", ".join(f"{KEY_KO.get(a, a)} {c}" for a, c in v.items()) if isinstance(v, dict) else v)}</span></div>' for k, v in (b.get("publishers") or {}).items())
        chans = "".join(f'<div class="kv"><span>{esc(KEY_KO.get(k, k))}</span><span>{esc(v)}</span></div>' for k, v in (b.get("channels") or {}).items())
        cmds = table(["명령", "하는 일", "스크립트"], [[f"<code>run.py {esc(name)} {esc(k)}</code>", esc(c.get("desc", "")), f"<code>{esc(short(c.get('script', '')))}</code>"] for k, c in (b.get("commands") or {}).items()])
        if (outbox / "posts").exists():
            fp = football_posts(outbox)
            work = (f'<div class="stats">{"".join(f"<div><b>{n}</b><span>{esc(STATUS_KO.get(s, s))}</span></div>" for s, n in fp["counts"].most_common())}'
                    f'<div><b>{fp["week"]}</b><span>최근 7일 발행</span></div><div><b>{esc(fp["cand"][5:])}</b><span>마지막 글감 후보</span></div></div>' + fp["table"])
            kpis.append((b.get("display_name", name), f'최근 7일 발행 {fp["week"]}편', f'마지막 발행 {fp["last_pub"][5:16].replace("T", " ") or "-"}', "warn" if on else "ok", "발행 보류 중" if on else "진행 중"))
        elif outbox.exists():
            ro = rentailor_outbox(outbox)
            work = (f'<div class="stats">{"".join(f"<div><b>{n}</b><span>네이버 {esc(STATUS_KO.get(s, s))}</span></div>" for s, n in ro["counts"].most_common())}'
                    f'<div><b>{esc(ro["cand"][5:])}</b><span>마지막 글감 후보</span></div></div>' + ro["table"] + "<h4>작업 폴더</h4>" + ro["dirs"]
                    + '<p class="muted small">워드프레스 발행 글·대기열은 Supabase(curated_topics, info_articles)에 있어 이 화면에는 아직 없습니다.</p>')
            kpis.append((b.get("display_name", name), f'네이버 초안 {ro["total"]}건', f'마지막 글감 후보 {ro["cand"][5:]}', "warn" if on else "ok", "글쓰기 보류 중" if on else "진행 중"))
        else:
            work = '<p class="muted">작업 파일 없음</p>'
        bad_jobs = [j for j in mine if j["kind"] == "bad"]
        nav.append((name, b.get("display_name", name)))
        brands_html.append(f"""
<section class="brand" id="brand-{esc(name)}">
  <h2>{esc(b.get("display_name", name))} <span class="muted">brands/{esc(name)}</span> {pill("보류 중", "warn") if on else pill("진행 중", "ok")}
      {pill(f"예약 작업 오류 {len(bad_jobs)}", "bad") if bad_jobs else ""} {pill(f"자동 점검 문제 {n_prob}", "bad") if n_prob else ""}</h2>
  <div class="grid">
    <div class="card"><h3>보류 스위치</h3>{holds}</div>
    <div class="card"><h3>채널·발행처</h3>{chans}{pubs}<div class="kv"><span>사업 프로젝트</span><span><code>{esc(short(P(b.get("project", cfg.get("business", "")))))}</code></span></div></div>
  </div>
  <details open><summary>글 현황 <span class="muted">outbox/</span></summary>{work}</details>
  <details><summary>예약 작업 <span class="muted">({len(mine)}개)</span></summary>{jobs_table(mine, False)}{health_html}</details>
  <details><summary>규칙 <span class="muted">({n_rules}개 파일, <code>{esc(short(bdir.parent / "rules"))}</code>)</span></summary>{rules_html}</details>
  <details><summary>명령 <span class="muted">({len(b.get("commands") or {})}개)</span></summary>{cmds}</details>
  <details><summary>데이터 창구</summary>{facts_block(cfg)}</details>
  <details><summary>수집기·데이터 목록 <span class="muted">(사업 프로젝트)</span></summary>{registry_block(cfg)}</details>
</section>""")
    engine_jobs = [j for j in jobs if "blog-engine" in j["raw"] or "football-blog/run.py" in j["raw"]]
    overview = "".join(f'<div class="card kpi"><h3>{esc(n)}</h3><p class="big">{esc(a)}</p><p class="muted">{esc(c)}</p>{pill(lab, k)}</div>' for n, a, c, k, lab in kpis)
    overview += (f'<div class="card kpi"><h3>엔진 예약 작업</h3><p class="big">{len(engine_jobs)}개</p><p class="muted">오류 {sum(j["kind"] == "bad" for j in engine_jobs)} · 꺼짐 {sum(j["kind"] == "off" for j in engine_jobs)}</p>'
                 f'{pill("오류 있음", "bad") if any(j["kind"] == "bad" for j in engine_jobs) else pill("정상", "ok")}</div>'
                 f'<div class="card kpi"><h3>임시 연결·사본</h3><p class="big">{compat[1]}건</p><p class="muted">기한 지남 {compat[2]}</p>{pill("기한 지남", "bad") if compat[2] else pill("기한 안", "ok")}</div>')
    links = "".join(f'<a href="#brand-{esc(k)}">{esc(v)}</a>' for k, v in nav)
    body = f'<p class="lead">{esc(e.get("summary", ""))} <code>{esc(short(root))}</code></p><div class="grid kpis">{overview}</div><nav class="sub">브랜드: {links}</nav>' + "".join(brands_html)
    return body, [k[0] for k in kpis]


def planned_engine(e: dict) -> str:
    items = "".join(f"<li>{esc(x)}</li>" for x in e.get("will_show") or [])
    return f'<div class="card"><h3>{esc(e["name"])} — 아직 연결 전</h3><p>{esc(e.get("summary", ""))}</p><p class="muted">연결되면 보일 것:</p><ul>{items}</ul><p class="muted small">추가 방법: <code>_meta/dashboard/engines.yaml</code>에서 status를 active로 바꾸고 build.py에 읽는 함수를 붙입니다.</p></div>'


# ── data tabs: one per business, grouped by topic category (data_categories.yaml) ──────────────────
def code_texts(usage: dict) -> dict:
    """label → [(file name, text)] for every .py under the listed folders / files (shallow: generated and vendor folders skipped)."""
    out = {}
    for label, paths in (usage or {}).items():
        files = []
        for raw in paths:
            p = P(raw)
            cand = [p] if p.is_file() else [f for f in p.rglob("*.py") if not any(x in f.parts for x in ("node_modules", ".venv", "venv", "__pycache__", "_archive", "outbox", "data"))
                                             and len(f.relative_to(p).parts) <= 3] if p.is_dir() else []
            files += [(f.name, read(f)) for f in cand[:400]]
        out[label] = files
    return out


def used_by(table: str, texts: dict, sql_only: bool) -> list:
    """[(label, [file names])] — groups of code that read this table. sql_only: FROM/JOIN context only (plain-word table names)."""
    t = re.escape(table)
    pat = re.compile(rf"(?:FROM|JOIN)\s+(?:\w+\.)?{t}\b" if sql_only else rf"(?:FROM|JOIN)\s+(?:\w+\.)?{t}\b|[\"'](?:\w+\.)?{t}[\"']", re.I)
    out = []
    for label, files in texts.items():
        hit = sorted({n for n, txt in files if pat.search(txt)})
        if hit:
            out.append((label, hit))
    return out


def job_for(text: str, jobs: list[dict]) -> list:
    """[(collector name, schedule, state, kind)] of the launchd jobs a '수집' note names (matched on the label's last parts)."""
    out = []
    for j in jobs:
        suffix = j["label"].split(".", 2)[-1]
        last = suffix.split(".")[-1]
        if (suffix in text or (len(last) >= 5 and re.search(rf"(?<![\w-]){re.escape(last)}(?![\w-])", text))) and j["schedule"] != "수동":
            out.append((suffix, j["schedule"], j["state"], j["kind"]))
    return list(dict.fromkeys(out))


BLOG_USE = {"✅": ("출처 표기하고 사용", "ok"), "🔒": ("출처 이름 없이 통계로만", "warn"), "⏸": ("결정 전 사용 금지", "off"), "⛔": ("사용 금지", "bad")}
STATE_KO = {"ok": "정상", "warn": "주의", "bad": "문제", "none": "점검 대상 아님"}


def cadam_rows(d: dict, jobs: list[dict]) -> tuple[list, dict, str]:
    cat = md_tables(read(P(d["catalog"])))
    health = {}
    for t in md_tables(read(P(d["health"]))):
        if t["head"][:2] == ["상태", "대상"]:
            for r in t["rows"]:
                if len(r) >= 5:
                    h = health.setdefault(r[1], {"worst": "✅"})
                    h[r[3]] = r[4]
                    if r[0] != "✅":
                        h["worst"] = r[0] if h["worst"] != "❌" else "❌"
    reg = md_tables(read(P(d["registry"])))
    site = [t for t in reg if t["head"] and t["head"][0] == "테이블" or (t["heading"] in ("약관·금융사", "고객·운영 (생성형)"))]
    counts = dict(re.findall(r"([a-z_]+) ([\d,]+)", read(P(d["counts"]))))
    texts = code_texts(d.get("usage"))

    def site_use(name: str) -> list:
        out = []
        for t in site:
            for r in t["rows"]:
                names = re.findall(r"[a-z][a-z_]*\*?", r[0])
                if name in names or any(n.endswith("*") and name.startswith(n[:-1]) for n in names):
                    out.append(" · ".join(c for c in r[2:4] if c))
        return out[:2]

    rows = []
    for t in cat[:1]:
        for r in t["rows"]:
            r = r + [""] * (7 - len(r))
            name = re.sub(r"`", "", r[0]).split(" ")[0].split(".")[-1]   # `data.kosis_x` → kosis_x
            h = health.get(r[1], {})
            agem = re.search(r"\((\d+)일 전", h.get("fresh", ""))
            flag = r[5].strip()[:1]
            rows.append({"table": name, "table_md": r[0], "title": r[1], "kind": r[2], "since": r[3], "allow": r[4].strip(), "collect": r[6],
                         "collectors": job_for(r[6], jobs), "fresh": re.sub(r"\(.*?허용.*?\)", "", h.get("fresh", "")).strip(),
                         "age": int(agem.group(1)) if agem else None, "nrows": h.get("rows", "-"),
                         "status": {"✅": "ok", "⚠️": "warn", "❌": "bad"}.get(h.get("worst"), "none"),
                         "blog": BLOG_USE.get(flag, (r[5].strip(), "")) if flag else None, "blog_note": r[5].strip()[1:].strip(),
                         "site": site_use(name), "uses": used_by(name, texts, False)})
    head_note = next((ln for ln in read(P(d["health"])).split("\n") if ln.startswith("점검 ")), "")
    meta = {"note": f'저장: {md_inline(d.get("store", ""))} · 상태 점검: {esc(head_note)} ({esc(day(mtime(P(d["health"]))))}) · 목록 원본 <code>{esc(short(P(d["catalog"])))}</code>'}
    # Supabase tables the site reads (registry §2): table → API → pages, + who writes them (§1) + row counts
    coll = next((t for t in reg if t["head"] and t["head"][0].startswith("수집기")), None)
    srows = []
    for t in site:
        for r in t["rows"]:
            r = r + [""] * (4 - len(r))
            names = re.findall(r"[a-z][a-z_]{3,}", r[0])
            writers = []
            for c in (coll["rows"] if coll else []):
                if len(c) >= 4 and any(re.search(rf"\b{re.escape(n)}\b", c[3]) for n in names):
                    writers.append(f'<div class="small"><code>{esc(re.sub(r" *[(].*", "", c[0]))}</code> {esc(c[1][:40])}</div>')
            cnt = " · ".join(f"{n} {counts[n]}" for n in names if n in counts)
            srows.append([md_inline(r[0]) + (f"<div class='small muted'>{esc(cnt)}</div>" if cnt else ""), "".join(writers[:3]) or '<span class="muted">사이트·운영에서 생성</span>',
                          md_inline(r[1]), md_inline(r[2]), md_inline(r[3])])
    extra = (f'<details><summary>사이트가 읽는 표 (Supabase) <span class="muted">({len(srows)}묶음 — 표 → API → 페이지. 신선도 점검 대상이 아니라 상태는 모름)</span></summary>'
             + table(["표 · 행 수", "채우는 수집기", "읽는 API", "쓰는 페이지", "활용"], srows, "data") + "</details>")
    return rows, meta, extra


def football_rows(d: dict, jobs: list[dict]) -> tuple[list, dict, str]:
    reg = md_tables(read(P(d["registry"])))
    texts = code_texts(d.get("usage"))
    live, art = {}, (None, "")
    try:
        import sqlite3
        con = sqlite3.connect(f"file:{P(d['warehouse'])}?mode=ro", uri=True, timeout=10)
        for (n,) in con.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall():
            live[n] = con.execute(f'SELECT COUNT(*) FROM "{n}"').fetchone()[0]
        con.close()
        con = sqlite3.connect(f"file:{P(d['articles'])}?mode=ro", uri=True, timeout=10)
        art = con.execute("SELECT COUNT(*), MAX(published_at) FROM articles").fetchone()
        con.close()
    except Exception as ex:  # noqa: BLE001
        art = (None, f"읽지 못함: {ex}")
    chk = read_json(P(d["datacheck"]), {}) or {}
    probs = chk.get("problems") or []
    run_job = {"매일 07:00": "football-data", "월요일 06:10": "football-brain"}
    rows, seen = [], set()
    for t in reg[:1]:
        for r in t["rows"]:
            r = r + [""] * (7 - len(r))
            name = r[1].strip("`")
            seen.add(name)
            bad = [str(p) for p in probs if name in str(p)]
            job = next((j for j in jobs if j["label"].endswith(run_job.get(r[3], "~"))), None)
            rows.append({"table": name, "table_md": f"`{name}`", "title": r[0], "kind": r[2], "since": "", "allow": r[4].strip("- "), "collect": f"{r[3]} · 수동: {r[6]}",
                         "collectors": [(job["label"].split(".", 2)[-1], job["schedule"], job["state"], job["kind"])] if job else [],
                         "fresh": "", "age": None, "nrows": f"{live[name]:,}행" if name in live else r[5], "status": "bad" if bad else "ok",
                         "problem": "; ".join(bad)[:160], "blog": None, "blog_note": "", "site": [], "uses": used_by(name, texts, True)})
    aux = [[f"<code>{esc(n)}</code>", f"{c:,}", use_chips(used_by(n, texts, True)) or '<span class="muted">-</span>'] for n, c in sorted(live.items()) if n not in seen]
    dd = P(d["data_dir"])
    files = [["기사 제목·요약·링크 (RSS)", f"<code>{esc(short(P(d['articles'])))}</code>", f"{art[0]:,}건 · 최신 {esc(str(art[1])[:16].replace('T', ' '))}" if art[0] is not None else esc(art[1]), "매일 07:40 morning (수집) → 글감 순위"],
             ["선수·구단 페이지 (brain)", f"<code>{esc(short(dd / 'entities'))}/</code>", f"{sum(1 for _ in (dd / 'entities').glob('*.json')):,}개", "월요일 06:10 brain → 초안 배경 자료·내부 링크"],
             ["공식 인스타 사진 창고", f"<code>{esc(short(dd / 'media/insta'))}/</code>", f"사진 목록 {len(read_json(dd / 'media/insta/index.json', []) or []):,}장 · {esc(day(mtime(dd / 'media/insta/index.json')))}", "매일 07:00 data → 썸네일·본문 사진"]]
    meta = {"note": f'저장: {md_inline(d.get("store", ""))} · 품질 점검: {esc((chk.get("at") or "")[:16].replace("T", " "))} ({esc(chk.get("level", ""))}) 문제 {len(probs)}건 · 목록 원본 <code>{esc(short(P(d["registry"])))}</code>'
                    ' · 표별 "최신 자료 날짜"는 이 목록에 없어 점검 통과 여부만 표시'}
    extra = ("<h3>표가 아닌 자료</h3>" + table(["자료", "위치", "분량·최신", "언제·어디에"], files)
             + f'<details><summary>목록에 없는 보조 표 <span class="muted">({len(aux)}개 — 수집 기록·점검용 등)</span></summary>' + table(["표", "행 수", "쓰는 곳"], aux) + "</details>")
    return rows, meta, extra


def use_chips(uses: list) -> str:
    return "".join(f'<span class="chip use" title="{esc(", ".join(f))}">{esc(label)} <b>{len(f)}</b></span>' for label, f in uses)


def coll_grid(collectors: list) -> str:
    """Collector name and schedule in two aligned columns."""
    if not collectors:
        return ""
    return '<div class="coll">' + "".join(
        f'<code>{esc(n)}</code><span>{esc(s)}{" " + pill(st, k) if k in ("bad", "off") else ""}</span>' for n, s, st, k in collectors) + "</div>"


PLAN_KO = {"ready": ("데이터 준비됨", "ok"), "check": ("검증·확인 필요", "warn"), "wait": ("데이터 쌓이는 중", "off")}
TYPE_ORDER = ["심층 시리즈", "트래커", "뉴스·이슈", "운영"]


def item_label(it: dict) -> str:
    return f'{it.get("series", "")} {it["name"]}'.strip()


def content_chip(it: dict, short_name: bool = False) -> str:
    k = PLAN_KO.get(it.get("plan"), ("", ""))[1]
    name = it["name"] if not short_name else re.split(r" — | \(|,", it["name"])[0]
    return (f'<div class="citem"><span class="ctype t-{TYPE_ORDER.index(it["type"]) if it["type"] in TYPE_ORDER else 9}">{esc(it["type"])}</span>'
            f'<span><b>{esc(it.get("series", ""))}</b> {esc(name)}{" " + pill("시범", "run") if it.get("pilot") else ""}{" " + pill(PLAN_KO[it["plan"]][0], k) if it.get("plan") in ("check", "wait") else ""}</span></div>')


def content_box(items: list, fallback: str = "") -> str:
    if not items:
        return f'<span class="muted">{esc(fallback) if fallback else "정해진 콘텐츠 없음"}</span>'
    items = sorted(items, key=lambda it: (TYPE_ORDER.index(it["type"]) if it["type"] in TYPE_ORDER else 9, it.get("series", ""), it["name"]))
    return "".join(content_chip(it, True) for it in items)


def detail_table(rows: list) -> str:
    out = []
    for r in rows:
        coll = (md_inline(r["collect"]) if r["collect"] else '<span class="muted">-</span>') + coll_grid(r["collectors"])
        fresh = esc(r["fresh"] or "-") + (f"<div class='small muted'>{r['age']}일 전 · 허용 {esc(r['allow'])}일</div>" if r["age"] is not None and r["allow"] else
                                          (f"<div class='small muted'>주기 {esc(r['allow'])}일</div>" if r["allow"] and not r["fresh"] else ""))
        uses = "".join(f'<div class="small">{md_inline(s)}</div>' for s in r["site"]) + use_chips(r["uses"])
        plan = "".join(f'<div class="small">{esc(item_label(it))}</div>' for it in r.get("content", []))
        out.append([f"<b>{esc(r['title'])}</b><div class='small'>{md_inline(r['table_md'])}</div>", esc(r["kind"]) + (f"<div class='small muted'>{esc(r['since'])}~</div>" if r["since"] else ""),
                    coll, fresh, esc(r["nrows"]), pill(STATE_KO[r["status"]], r["status"] if r["status"] != "none" else "") + (f"<div class='small'>{esc(r.get('problem', ''))}</div>" if r.get("problem") else ""),
                    (pill(r["blog"][0], r["blog"][1]) + (f"<div class='small muted'>{esc(r['blog_note'][:70])}</div>" if r["blog_note"] else "")) if r["blog"] else '<span class="muted">-</span>',
                    uses or UNUSED, plan or '<span class="muted">-</span>'])
    return table(["데이터", "구분", "어디서·언제 수집", "최신 자료", "행 수", "상태", "콘텐츠 사용 조건", "지금 읽는 곳", "계획된 콘텐츠"], out, "data")


UNUSED = '<span class="muted">읽는 코드를 못 찾음</span>'


def has_use(r: dict) -> bool:
    return bool(r["site"] or r["uses"])


def dots(rows: list) -> str:
    c = Counter(r["status"] for r in rows)
    return "".join(f'<span class="dot {k}" title="{STATE_KO[k]}"></span>{c[k]} ' for k in ("bad", "warn", "ok", "none") if c[k])


def tightest(rows: list):
    """The dataset closest to its allowed delay (age / allowance) — a yearly statistic 300 days old is not the worry, a daily one 3 days old is."""
    aged = [(r["age"] / int(r["allow"]), r) for r in rows if r["age"] is not None and r["allow"].isdigit() and int(r["allow"])]
    return max(aged, key=lambda x: x[0]) if aged else None


def content_plan_table(items: list, by_name: dict) -> str:
    """Planned content × the current state of the data each piece needs."""
    rows = []
    for it in sorted(items, key=lambda it: (TYPE_ORDER.index(it["type"]) if it["type"] in TYPE_ORDER else 9, it.get("series", ""), it.get("order", (0, "")), it["name"])):
        need = [by_name[t] for t in it.get("tables", []) if t in by_name]
        missing = [t for t in it.get("tables", []) if t not in by_name]
        bad = [r for rs in need for r in rs if r["status"] in ("bad", "warn")]
        late = [r for rs in need for r in rs if r["age"] is not None and r["allow"].isdigit() and int(r["allow"]) and r["age"] > int(r["allow"])]
        state = pill("데이터 문제", "bad") if bad or late or missing else pill("데이터 정상", "ok") if need else pill("데이터 없이 계산", "")
        chips = "".join(f'<span class="chip st-{rs[0]["status"]}" title="{esc(rs[0]["fresh"] or rs[0]["nrows"])}">{esc(rs[0]["title"])}</span>' for rs in need) + "".join(f'<span class="chip bad">{esc(t)} 없음</span>' for t in missing)
        rows.append([f'<span class="ctype t-{TYPE_ORDER.index(it["type"]) if it["type"] in TYPE_ORDER else 9}">{esc(it["type"])}</span>', f"<b>{esc(it.get('series', ''))}</b>", esc(it["name"]) + (" " + pill("시범", "run") if it.get("pilot") else ""),
                     chips or '<span class="muted">세금 규칙 등 코드 계산</span>', pill(*PLAN_KO.get(it.get("plan"), ("-", ""))), state,
                     esc(SOURCE_KO.get(it.get("source"), it.get("source", "-"))), pill(*PROGRESS_KO.get(it.get("status", "planned"), (it.get("status", "-"), "")))])
    return table(["유형", "시리즈", "글", "쓰는 데이터 (지금 상태)", "계획 때 준비 상태", "데이터 상태", "들어온 길", "진행"], rows, "plantab")


def data_business(d: dict, jobs: list[dict], cats: list, items: list) -> str:
    rows, meta, extra = cadam_rows(d, jobs) if d.get("kind") == "cadam" else football_rows(d, jobs)
    by_table = {t: c["id"] for c in cats for t in c.get("tables", [])}
    by_name: dict = {}
    for r in rows:
        by_name.setdefault(r["table"], []).append(r)
        r["content"] = [it for it in items if r["table"] in it.get("tables", [])]
    groups = {c["id"]: [] for c in cats}
    loose = []
    for r in rows:
        (groups[by_table[r["table"]]] if r["table"] in by_table else loose).append(r)
    # what needs a look right now (monitoring first)
    watch = []
    for r in rows:
        if r["status"] in ("bad", "warn"):
            watch.append((0, f'{pill(STATE_KO[r["status"]], r["status"])} <b>{esc(r["title"])}</b> — {esc(r.get("problem") or r["fresh"] or "점검 결과 확인")}'))
        elif r["age"] is not None and r["allow"].isdigit() and int(r["allow"]) and r["age"] >= 0.8 * int(r["allow"]):
            watch.append((1, f'{pill("곧 기한", "warn")} <b>{esc(r["title"])}</b> — 최신 자료가 {r["age"]}일 전 (허용 {esc(r["allow"])}일)'
                             + (f' · 쓰는 글: {esc(", ".join(item_label(it) for it in r["content"][:2]))}' if r["content"] else "")))
        for n, s, st, k in r["collectors"]:
            if k in ("bad", "off"):
                watch.append((0, f'{pill(st, k)} 수집기 <code>{esc(n)}</code> ({esc(s)}) — <b>{esc(r["title"])}</b>'))
    watch = list(dict.fromkeys(w for _, w in sorted(watch)))
    idle = [r for r in rows if not has_use(r)]
    idle_noplan = [r for r in idle if not r["content"]]
    c = Counter(r["status"] for r in rows)
    head = (f'<p class="muted">{meta["note"]}</p>'
            f'<div class="stats"><div><b>{len(rows)}</b><span>데이터 묶음</span></div><div><b>{c["ok"]}</b><span>정상</span></div><div><b>{c["warn"] + c["bad"]}</b><span>주의·문제</span></div>'
            f'<div><b>{c["none"]}</b><span>점검 대상 아님</span></div><div><b>{len(idle)}</b><span>읽는 코드 없음</span></div>'
            + (f'<div><b>{len(idle_noplan)}</b><span>그중 계획된 콘텐츠도 없음</span></div>' if items else "")
            + f'<div><b>{len(loose)}</b><span>미분류</span></div></div>'
            + '<div class="card watch"><h3>지금 봐야 할 것</h3>' + ("<ul>" + "".join(f"<li>{w}</li>" for w in watch[:12]) + "</ul>" if watch else '<p class="muted">없음 — 점검에 걸린 데이터와 멈춘 수집기가 없습니다.</p>') + "</div>"
            + f'<input class="filter" data-for="p-data-{esc(d["id"])}" placeholder="데이터 이름·표·수집기·글 제목으로 걸러 보기 (자세히 표가 열립니다)">')
    cards, sections = [], []
    for cdef in cats + ([{"id": "loose", "name": "미분류", "desc": "카테고리가 정해지지 않은 데이터. data_categories.yaml에 추가해야 합니다."}] if loose else []):
        rs = loose if cdef["id"] == "loose" else groups[cdef["id"]]
        if not rs:
            continue
        worst = "bad" if any(r["status"] == "bad" for r in rs) else "warn" if any(r["status"] == "warn" for r in rs) else "ok" if any(r["status"] == "ok" for r in rs) else "none"
        tight = tightest(rs)
        unused = [r for r in rs if not has_use(r)]
        mine = [it for it in items if any(r["table"] in it.get("tables", []) for r in rs)]
        ntype = Counter(it["type"] for it in mine)
        trackers = [it for it in mine if it["type"] == "트래커"]   # the flow box lists trackers only (owner 2026-11-10); every piece is in the plan table
        n_deep = ntype["심층 시리즈"]
        box_title = "이 자료로 만드는 트래커" if items else "이 자료로 만드는 콘텐츠"
        if not items or trackers:
            box = content_box(trackers, cdef.get("content", ""))
        else:
            box = '<span class="muted">트래커 없음' + (f" (심층 시리즈 {n_deep}편은 위 계획표에)" if n_deep else "") + "</span>"
        aid = f'cat-{d["id"]}-{cdef["id"]}'
        cards.append(f'<a class="card cat {worst}" href="#{aid}"><h3>{esc(cdef["name"])} <span class="muted">{len(rs)}</span></h3><p class="small muted">{esc(cdef.get("desc", ""))}</p>'
                     f'<p class="small">{dots(rs)}</p>'
                     + (f'<p class="small">기한에 가장 가까운 자료: {esc(tight[1]["title"])} (허용 {esc(tight[1]["allow"])}일 중 {tight[1]["age"]}일)</p>' if tight else "")
                     + f'<p class="small">읽는 곳 있음 {len(rs) - len(unused)} · 없음 {len(unused)}</p>'
                     + (f'<p class="small">콘텐츠: {esc(" · ".join(f"{t} {ntype[t]}" for t in TYPE_ORDER if ntype[t]))}</p>' if mine else (f'<p class="small muted">콘텐츠: {esc(cdef.get("content", "정해진 것 없음"))}</p>')) + "</a>")
        colls = Counter()
        for r in rs:
            for n, s, st, k in r["collectors"]:
                colls[(n, s, st, k)] += 1
        frozen = sum(1 for r in rs if not r["collectors"] and re.search("1회|동결|파생|사본|우리 코드", r["kind"]))
        no_coll = sum(1 for r in rs if not r["collectors"]) - frozen
        left = (coll_grid([k for k, _ in colls.most_common()]) + (f'<div class="small muted">수집이 끝났거나 우리 코드가 만드는 것 {frozen}개</div>' if frozen else "")
                + (f'<div class="small muted">수집 일정을 못 찾은 것 {no_coll}개</div>' if no_coll else ""))
        mid = "".join(f'<span class="chip st-{r["status"]}{" planned" if r["content"] else ""}" title="{esc(r["table"])} · {esc(r["fresh"] or r["nrows"])}">{esc(r["title"])}</span>' for r in rs)
        ulab = Counter()
        for r in rs:
            for label, _f in r["uses"]:
                ulab[label] += 1
            if r["site"]:
                ulab["사이트 페이지"] += 1
        right = "".join(f'<span class="chip use">{esc(k)} <b>{v}</b></span>' for k, v in ulab.most_common()) + (f'<span class="chip muted">읽는 곳 없음 {len(unused)}</span>' if unused else "")
        sections.append(f'<section class="catsec" id="{aid}"><h3 class="cath">{esc(cdef["name"])} <span class="muted">{len(rs)}개</span> {dots(rs)}</h3><p class="muted small">{esc(cdef.get("desc", ""))}</p>'
                        f'<div class="flow"><div><h4>수집 (누가 · 언제)</h4>{left or "<span class=muted>-</span>"}</div><div class="arrow">→</div><div><h4>데이터</h4>{mid}</div><div class="arrow">→</div>'
                        f'<div><h4>활용 (지금 읽는 곳)</h4>{right or UNUSED}</div><div class="arrow">→</div><div class="cbox"><h4>{box_title}</h4>{box}</div></div>'
                        f'<details><summary>자세히 <span class="muted">({len(rs)}개 — 최신 자료·행 수·수집기·읽는 곳·계획된 콘텐츠)</span></summary>{detail_table(rs)}</details></section>')
    legend = ('<p class="small muted">색: <span class="dot ok"></span>정상 <span class="dot warn"></span>주의 <span class="dot bad"></span>문제 <span class="dot none"></span>점검 대상 아님 · '
              '카드를 누르면 그 카테고리로 이동 · 데이터 이름 아래 파란 밑줄 = 계획된 콘텐츠가 있는 데이터 · "읽는 곳"은 표 이름이 코드에 적힌 경우만 찾으므로 "없음"은 확인이 필요한 목록입니다 · 카테고리와 콘텐츠 연결표는 <code>_meta/dashboard/data_categories.yaml</code>(제안)</p>')
    plan = ""
    if items:
        n_pilot = sum(1 for it in items if it.get("pilot"))
        src = Counter(SOURCE_KO.get(it.get("source"), "기타") for it in items)
        plan = (f'<details class="plan"><summary>콘텐츠 계획과 데이터 준비 상태 <span class="muted">({len(items)}개, 시범 {n_pilot}편 — {esc(" · ".join(f"{k} {v}" for k, v in src.most_common()))} · 원본 <code>{esc(short(P(d["content_plan"])))}</code>)</span></summary>'
                + content_plan_table(items, by_name) + "</details>")
    return head + plan + '<h3>카테고리</h3><div class="grid cats">' + "".join(cards) + "</div>" + legend + "".join(sections) + extra


SOURCE_KO = {"template": "틀에서 자동", "approved": "제안 → 승인", "request": "직접 요청", "plan": "계획 문서"}
PROGRESS_KO = {"planned": ("계획", ""), "draft": ("초안", "run"), "review": ("승인 대기", "warn"), "published": ("발행", "ok")}


def load_plan(path) -> list:
    """Planned content of one business (the engine's content_plan.yaml): explicit items + series templates × cars."""
    if not path:
        return []
    d = yaml.safe_load(read(P(path))) or {}
    out = []
    for sid, t in (d.get("series_templates") or {}).items():
        for car in t.get("cars") or []:
            for part in t.get("parts") or []:
                out.append({"id": f"{sid}-{car}-{part['part']}", "type": t.get("type", "심층 시리즈"), "series": t.get("series", sid), "name": f"{car} {part['part']} {part['name']}",
                            "plan": part.get("plan", "ready"), "pilot": f"{car} {part['part']}" in (t.get("pilot") or []), "source": "template", "status": "planned",
                            "tables": part.get("tables", []), "order": (t.get("cars").index(car), part["part"])})
    prog = d.get("progress") or {}
    for it in out:
        it["status"] = prog.get(it["id"], it["status"])
    return out + list(d.get("items") or [])


def data_panels(cfg: dict, jobs: list[dict]) -> list:
    cats = yaml.safe_load(read(HERE / "data_categories.yaml")) or {}
    out = []
    for d in cfg.get("data") or []:
        try:
            body = data_business(d, jobs, cats.get(d["id"], []), load_plan(d.get("content_plan")))
        except Exception as ex:  # noqa: BLE001
            body = f'<div class="card"><h3>읽는 중 오류</h3><p class="muted">{esc(type(ex).__name__)}: {esc(ex)}</p></div>'
        out.append((f'data-{d["id"]}', d.get("tab", d["name"]), '<p class="lead">어떤 데이터가 있고, 어디서·언제 수집되고, 지금 신선한지, 어디에 쓰이는지 — 주제별 카테고리로 묶어 봅니다.</p>' + body))
    return out


CSS = """
:root{--bg:#f6f7f9;--card:#fff;--ink:#16202a;--muted:#6b7785;--line:#e3e7ec;--ok:#0f7b4f;--okbg:#e2f5ec;--warn:#9a5b00;--warnbg:#fff1d6;--bad:#b3261e;--badbg:#fde7e5;--run:#1456c4;--runbg:#e3edff;--off:#5f6975;--offbg:#eceff3;--accent:#10201b}
@media(prefers-color-scheme:dark){:root{--bg:#11161b;--card:#1a2129;--ink:#e8edf2;--muted:#93a0ad;--line:#2b3540;--okbg:#113626;--ok:#6fd7a5;--warnbg:#40300e;--warn:#f2c46a;--badbg:#45201d;--bad:#ff9a92;--runbg:#182c52;--run:#9dbcff;--offbg:#262f39;--off:#aab4bf;--accent:#f2c84b}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.55 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR",sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--card);border-bottom:1px solid var(--line);padding:10px 20px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
header h1{font-size:17px;margin:0}header .gen{margin-left:auto;color:var(--muted);font-size:12px}
.tabs{display:flex;gap:6px;flex-wrap:wrap}.tabs a{border:1px solid var(--line);background:transparent;color:var(--ink);padding:6px 12px;border-radius:999px;cursor:pointer;font:inherit;text-decoration:none}
.js .tabs a.on{background:var(--accent);color:var(--bg);border-color:var(--accent)}.tabs a .muted{font-size:11px}
main{max-width:1280px;margin:0 auto;padding:16px 20px 60px}.panel{scroll-margin-top:110px}.js .panel{display:none}.js .panel.on{display:block}.ptitle{font-size:22px;border-bottom:3px solid var(--accent);padding-bottom:6px;margin-top:40px}.js .ptitle{display:none}
h2{font-size:18px;margin:26px 0 10px}h3{font-size:14px;margin:0 0 8px}h4{font-size:13px;margin:14px 0 6px;color:var(--muted)}
.lead{color:var(--muted)}.muted{color:var(--muted)}.small{font-size:12px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px}.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
.kpi .big{font-size:20px;font-weight:700;margin:2px 0}.kpi p{margin:2px 0 8px}
.kv{display:flex;gap:10px;justify-content:space-between;padding:5px 0;border-top:1px solid var(--line)}.kv:first-of-type{border-top:0}.kv>span:first-child{color:var(--muted);white-space:nowrap}.kv>span:last-child{text-align:right}
.pill{display:inline-block;padding:1px 9px;border-radius:999px;font-size:12px;background:var(--offbg);color:var(--off);white-space:nowrap}
.pill.ok{background:var(--okbg);color:var(--ok)}.pill.warn{background:var(--warnbg);color:var(--warn)}.pill.bad{background:var(--badbg);color:var(--bad)}.pill.run{background:var(--runbg);color:var(--run)}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:8px;background:var(--card)}table{border-collapse:collapse;width:100%;font-size:13px}
th,td{padding:7px 10px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}th{background:var(--bg);font-weight:600;white-space:nowrap;position:sticky;top:0}tr:last-child td{border-bottom:0}
table.reg td{min-width:110px}code{font:12px ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--bg);padding:1px 4px;border-radius:4px;word-break:break-all}
details{margin:10px 0}summary{cursor:pointer;font-weight:600;padding:8px 0}details>.tw,details>p,details>div,details>ul{margin-top:6px}
.stats{display:flex;gap:10px;flex-wrap:wrap;margin:6px 0 12px}.stats div{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 14px;min-width:92px}.stats b{display:block;font-size:18px}.stats span{color:var(--muted);font-size:12px}
.chips{display:flex;flex-wrap:wrap;gap:6px}.chip{font:12px ui-monospace,Menlo,monospace;border:1px solid var(--line);border-radius:6px;padding:2px 7px;background:var(--card)}.chip.cmd{border-color:var(--warn);color:var(--warn)}
.chip.use{border-color:var(--run);color:var(--run);margin:2px 3px 0 0;display:inline-block;font-family:inherit}table.data td{min-width:90px}table.data td:first-child{min-width:190px}table.data td:last-child{min-width:230px}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin:0 3px 0 6px;background:var(--off)}.dot.ok{background:var(--ok)}.dot.warn{background:var(--warn)}.dot.bad{background:var(--bad)}
a.card.cat{display:block;text-decoration:none;color:var(--ink);border-left:5px solid var(--off)}a.card.cat.ok{border-left-color:var(--ok)}a.card.cat.warn{border-left-color:var(--warn)}a.card.cat.bad{border-left-color:var(--bad)}a.card.cat p{margin:4px 0}a.card.cat:hover{border-color:var(--run)}
.card.watch{margin:12px 0}.card.watch ul{margin:6px 0 0;padding-left:18px}.card.watch li{margin:4px 0}
.catsec{border-top:1px solid var(--line);margin-top:22px;padding-top:6px;scroll-margin-top:120px}.cath{font-size:16px;margin:10px 0 4px}
.flow{display:grid;grid-template-columns:1.05fr 22px 1.2fr 22px .8fr 22px 1.5fr;gap:6px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px;margin:8px 0}.flow h4{margin:0 0 6px}.flow .arrow{align-self:center;text-align:center;color:var(--muted);font-size:20px}.flow .chip{display:inline-block;margin:2px 3px 2px 0;font-family:inherit}
.chip.st-ok{border-color:var(--ok);background:var(--okbg);color:var(--ok)}.chip.st-warn{border-color:var(--warn);background:var(--warnbg);color:var(--warn)}.chip.st-bad{border-color:var(--bad);background:var(--badbg);color:var(--bad)}.chip.st-none{background:var(--offbg);color:var(--off)}.chip.bad{border-color:var(--bad);color:var(--bad)}.chip.muted{color:var(--muted)}
@media(max-width:1000px){.flow{grid-template-columns:1fr}.flow .arrow{transform:rotate(90deg)}}
.coll{display:grid;grid-template-columns:max-content 1fr;gap:3px 12px;align-items:baseline;font-size:12.5px;margin-top:2px}.coll code{white-space:nowrap}.coll span{white-space:nowrap}table.data{min-width:1240px}
.cbox{border:1px solid var(--line);border-radius:8px;padding:8px 10px;background:var(--bg)}.citem{display:grid;grid-template-columns:78px 1fr;gap:8px;font-size:12.5px;padding:3px 0;border-top:1px dashed var(--line)}.citem:first-of-type{border-top:0}
.ctype{display:inline-block;font-size:11px;border-radius:4px;padding:1px 6px;text-align:center;align-self:start;background:var(--offbg);color:var(--off);white-space:nowrap}.ctype.t-0{background:var(--runbg);color:var(--run)}.ctype.t-1{background:var(--okbg);color:var(--ok)}.ctype.t-2{background:var(--warnbg);color:var(--warn)}
.chip.planned{box-shadow:inset 0 -2px 0 var(--run)}details.plan{margin:14px 0}
table .chip{display:inline-block;white-space:nowrap;margin:2px 4px 2px 0;font-family:inherit}
table.plantab{min-width:1080px}table.plantab td{vertical-align:top}table.plantab td:nth-child(1){width:84px}table.plantab td:nth-child(2){width:150px}table.plantab td:nth-child(3){min-width:210px}table.plantab td:nth-child(4){min-width:330px}table.plantab td:nth-child(n+5){white-space:nowrap}
nav.sub{margin:14px 0 0;color:var(--muted)}nav.sub a{margin-right:12px}a{color:var(--run)}
.brand{border-top:2px solid var(--line);margin-top:22px}input.filter{width:100%;max-width:360px;padding:7px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);font:inherit;margin:8px 0}
"""

JS = """
document.body.classList.add('js');
function show(id){document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('on',p.id==='p-'+id));document.querySelectorAll('.tabs a').forEach(b=>b.classList.toggle('on',b.dataset.t===id));try{localStorage.setItem('tab',id)}catch(e){}}
document.querySelectorAll('.tabs a').forEach(b=>b.onclick=function(ev){ev.preventDefault();show(b.dataset.t);window.scrollTo(0,0)});
var saved=null;try{saved=localStorage.getItem('tab')}catch(e){};if(saved&&document.getElementById('p-'+saved))show(saved);
document.querySelectorAll('input.filter[data-for]').forEach(function(i){i.oninput=function(){var q=i.value.toLowerCase(),root=document.getElementById(i.dataset.for);root.querySelectorAll('table.data tbody tr').forEach(function(r){r.style.display=r.textContent.toLowerCase().indexOf(q)<0?'none':''});if(q)root.querySelectorAll('details').forEach(function(d){d.open=true})}});
var f=document.getElementById('jobfilter');if(f)f.oninput=function(){var q=f.value.toLowerCase();document.querySelectorAll('#alljobs tbody tr').forEach(function(r){r.style.display=r.textContent.toLowerCase().indexOf(q)<0?'none':''})};
"""


def docaudit_panel() -> tuple[str, int]:
    """Doc audit result (_meta/scripts/doc_audit.py, weekly launchd com.solo.doc-audit) — read only."""
    d = read_json(P("~/projects/_meta/logs/doc_audit.json"), {}) or {}
    if not d:
        return '<p class="muted">아직 결과 없음 — <code>python3 ~/projects/_meta/scripts/doc_audit.py</code></p>', 0
    names = {"retired": "없어진 이름·경로가 현재처럼 적힌 줄", "missing": "적힌 경로가 실제로 없음",
             "plist": "예약 작업 설정 사본이 원본과 다름", "status": "예약 작업 상태가 문서와 실제가 다름"}
    total = sum(d.get("counts", {}).values())
    out = [f'<p class="lead">규칙·매뉴얼이 실제 시스템과 어긋난 곳 {total}건 (문서 {d.get("docs", 0)}개, {esc(d.get("at", ""))} 점검). '
           f'고치는 법: <code>_meta/governance/DOCS_RULES.md</code> · 전체 목록 <code>_meta/logs/doc_audit.md</code></p>']
    for k, rows in (d.get("results") or {}).items():
        out.append(f"<h3>{esc(names.get(k, k))} {pill(str(len(rows)), 'bad' if rows else '')}</h3>")
        if rows:
            out.append(table(["문서", "줄", "무엇이 다른가"], [[esc(r["file"]), str(r["line"]), esc(r["why"])] for r in rows[:200]], "reg"))
    return "".join(out), total


def main() -> int:
    cfg = yaml.safe_load(read(HERE / "engines.yaml"))
    jobs = launchd_jobs(cfg.get("job_prefixes") or [])
    compat = compat_block(P(cfg["compat_list"]))
    tabs, panels = [], []
    for e in cfg["engines"]:
        active = e.get("status") == "active"
        tabs.append((e["id"], e["name"], "" if active else "예정"))
        try:
            body = blog_engine(e, jobs, compat)[0] if active and e.get("kind") == "blog-engine" else planned_engine(e)
        except Exception as ex:  # noqa: BLE001 — one broken reader must not blank the whole page
            body = f'<div class="card"><h3>읽는 중 오류</h3><p class="muted">{esc(type(ex).__name__)}: {esc(ex)}</p></div>'
        panels.append((e["id"], body))
    by_proj = Counter(j["project"] for j in jobs)
    bad = [j for j in jobs if j["kind"] == "bad"]
    jobs_panel = (f'<p class="lead">이 컴퓨터에 등록된 예약 작업(launchd) {len(jobs)}개 — 수집기·글쓰기·점검·백업 전부. 오류 {len(bad)} · 꺼짐 {sum(j["kind"] == "off" for j in jobs)} · 실행 중 {sum(j["kind"] == "run" for j in jobs)}</p>'
                  f'<div class="stats">{"".join(f"<div><b>{n}</b><span>{esc(p)}</span></div>" for p, n in by_proj.most_common())}</div>'
                  + (f"<h3>오류 난 작업</h3>{jobs_table(bad)}" if bad else "")
                  + '<input id="jobfilter" class="filter" placeholder="이름·프로젝트·스크립트로 걸러 보기 (예: football, crawler, 07:)"><div id="alljobs">'
                  + jobs_table(sorted(jobs, key=lambda j: (j["project"], j["label"]))) + "</div>")
    dps = data_panels(cfg, jobs)
    audit = docaudit_panel()
    tabs += [(i, n, "") for i, n, _ in dps] + [("jobs", "예약 작업 전체", ""), ("compat", "임시 연결·남은 일", ""), ("docs", "문서 점검", f"{audit[1]}건" if audit[1] else "")]
    panels += [(i, b) for i, _, b in dps] + [("jobs", jobs_panel), ("compat", '<p class="lead">이사하면서 남긴 임시 연결·사본·규칙 위반 목록과 없애는 기한.</p>' + compat[0]), ("docs", audit[0])]
    first = tabs[0][0]
    names = {i: n for i, n, _ in tabs}
    page = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>엔진 대시보드</title><style>{CSS}</style></head><body>'
            f'<header><h1>엔진 대시보드</h1><div class="tabs">'
            + "".join(f'<a href="#p-{esc(i)}" data-t="{esc(i)}" class="{"on" if i == first else ""}">{esc(n)}{f" <span class=muted>{esc(s)}</span>" if s else ""}</a>' for i, n, s in tabs)
            + f'</div><span class="gen">만든 때 {NOW:%Y-%m-%d %H:%M} · 다시 만들기 <code>python3 ~/projects/_meta/dashboard/build.py --open</code></span></header><main>'
            + "".join(f'<div class="panel {"on" if i == first else ""}" id="p-{esc(i)}"><h2 class="ptitle">{esc(names[i])}</h2>{b}</div>' for i, b in panels)
            + f"</main><script>{JS}</script></body></html>")
    out = HERE / "index.html"
    out.write_text(page, encoding="utf-8")
    print(f"{out}  ({len(page) // 1024} KB, 예약 작업 {len(jobs)}개, 임시 연결 {compat[1]}건)")
    if "--open" in sys.argv:
        subprocess.run(["open", str(out)])
    return 0


if __name__ == "__main__":
    sys.exit(main())
