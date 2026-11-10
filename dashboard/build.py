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


CSS = """
:root{--bg:#f6f7f9;--card:#fff;--ink:#16202a;--muted:#6b7785;--line:#e3e7ec;--ok:#0f7b4f;--okbg:#e2f5ec;--warn:#9a5b00;--warnbg:#fff1d6;--bad:#b3261e;--badbg:#fde7e5;--run:#1456c4;--runbg:#e3edff;--off:#5f6975;--offbg:#eceff3;--accent:#10201b}
@media(prefers-color-scheme:dark){:root{--bg:#11161b;--card:#1a2129;--ink:#e8edf2;--muted:#93a0ad;--line:#2b3540;--okbg:#113626;--ok:#6fd7a5;--warnbg:#40300e;--warn:#f2c46a;--badbg:#45201d;--bad:#ff9a92;--runbg:#182c52;--run:#9dbcff;--offbg:#262f39;--off:#aab4bf;--accent:#f2c84b}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.55 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Noto Sans KR",sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--card);border-bottom:1px solid var(--line);padding:10px 20px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
header h1{font-size:17px;margin:0}header .gen{margin-left:auto;color:var(--muted);font-size:12px}
.tabs{display:flex;gap:6px;flex-wrap:wrap}.tabs button{border:1px solid var(--line);background:transparent;color:var(--ink);padding:6px 12px;border-radius:999px;cursor:pointer;font:inherit}
.tabs button.on{background:var(--accent);color:var(--bg);border-color:var(--accent)}.tabs button .muted{font-size:11px}
main{max-width:1280px;margin:0 auto;padding:16px 20px 60px}.panel{display:none}.panel.on{display:block}
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
nav.sub{margin:14px 0 0;color:var(--muted)}nav.sub a{margin-right:12px}a{color:var(--run)}
.brand{border-top:2px solid var(--line);margin-top:22px}input.filter{width:100%;max-width:360px;padding:7px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--ink);font:inherit;margin:8px 0}
"""

JS = """
function show(id){document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('on',p.id==='p-'+id));document.querySelectorAll('.tabs button').forEach(b=>b.classList.toggle('on',b.dataset.t===id));try{localStorage.setItem('tab',id)}catch(e){}}
document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>show(b.dataset.t));
var saved=null;try{saved=localStorage.getItem('tab')}catch(e){};if(saved&&document.getElementById('p-'+saved))show(saved);
var f=document.getElementById('jobfilter');if(f)f.oninput=function(){var q=f.value.toLowerCase();document.querySelectorAll('#alljobs tbody tr').forEach(function(r){r.style.display=r.textContent.toLowerCase().indexOf(q)<0?'none':''})};
"""


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
    tabs += [("jobs", "예약 작업 전체", ""), ("compat", "임시 연결·남은 일", "")]
    panels += [("jobs", jobs_panel), ("compat", '<p class="lead">이사하면서 남긴 임시 연결·사본·규칙 위반 목록과 없애는 기한.</p>' + compat[0])]
    first = tabs[0][0]
    page = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>엔진 대시보드</title><style>{CSS}</style></head><body>'
            f'<header><h1>엔진 대시보드</h1><div class="tabs">'
            + "".join(f'<button data-t="{esc(i)}" class="{"on" if i == first else ""}">{esc(n)}{f" <span class=muted>{esc(s)}</span>" if s else ""}</button>' for i, n, s in tabs)
            + f'</div><span class="gen">만든 때 {NOW:%Y-%m-%d %H:%M} · 다시 만들기 <code>python3 ~/projects/_meta/dashboard/build.py --open</code></span></header><main>'
            + "".join(f'<div class="panel {"on" if i == first else ""}" id="p-{esc(i)}">{b}</div>' for i, b in panels)
            + f"</main><script>{JS}</script></body></html>")
    out = HERE / "index.html"
    out.write_text(page, encoding="utf-8")
    print(f"{out}  ({len(page) // 1024} KB, 예약 작업 {len(jobs)}개, 임시 연결 {compat[1]}건)")
    if "--open" in sys.argv:
        subprocess.run(["open", str(out)])
    return 0


if __name__ == "__main__":
    sys.exit(main())
