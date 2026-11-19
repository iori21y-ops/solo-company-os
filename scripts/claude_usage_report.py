#!/usr/bin/env python3
"""Claude 사용량 리포트 — 모델 분담(WORK_RULES §7.1) 효과를 재는 용도 (2026-11-19).

Reads Claude Code transcripts (~/.claude/projects/**/*.jsonl) and the claude -p bridge log, and prints:
  - estimated cost-weighted share per model (API list prices as a proxy for subscription limit weight)
  - main window vs subagent share, Opus main: conversation vs execution turns
  - Fable usage by folder
Saves a JSON snapshot to ~/projects/_data/shared/claude-usage/YYYY-MM-DD.json and, with --compare FILE,
prints the change against an earlier snapshot.

Run: python3 claude_usage_report.py [--days 7] [--compare ~/projects/_data/shared/claude-usage/2026-11-19.json]
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import glob
import json
import os
import time
from pathlib import Path

# $/MTok: (input, output, cache_read). Cache write billed at 1.25x input.
PRICES = {
    "opus": (4.0, 20.0, 0.20),
    "sonnet": (2.0, 10.0, 0.20),
    "haiku": (0.10, 0.50, 0.01),
    "fable": (10.0, 50.0, 0.25),
}
OUT_DIR = Path.home() / "projects/_data/shared/claude-usage"
BRIDGE_LOG = Path.home() / "projects/cadam/collect/claude_bridge/usage.jsonl"


def family(model: str) -> str | None:
    m = (model or "").lower()
    for k in PRICES:
        if k in m:
            return k
    return None


def cost(fam: str, u: dict) -> float:
    pi, po, pr = PRICES[fam]
    return ((u.get("input_tokens") or 0) * pi + (u.get("cache_creation_input_tokens") or 0) * pi * 1.25
            + (u.get("cache_read_input_tokens") or 0) * pr + (u.get("output_tokens") or 0) * po) / 1e6


def collect(days: int) -> dict:
    cut = time.time() - days * 86400
    by_model = collections.Counter()
    by_side = collections.Counter()
    opus_turn = collections.Counter()
    fable_dir = collections.Counter()
    seen = set()
    for f in glob.glob(str(Path.home() / ".claude/projects/**/*.jsonl"), recursive=True):
        if os.path.getmtime(f) < cut:
            continue
        sub = "/subagents/" in f
        folder = f.split("/.claude/projects/")[1].split("/")[0].replace("-Users-kim-", "")
        prev = "talk"
        for line in open(f, errors="ignore"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("type") == "user":
                c = d.get("message", {}).get("content")
                prev = "exec" if isinstance(c, list) and any(isinstance(x, dict) and x.get("type") == "tool_result" for x in c) else "talk"
                continue
            if d.get("type") != "assistant":
                continue
            ts = d.get("timestamp") or ""
            if ts:
                try:
                    if dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp() < cut:
                        continue
                except ValueError:
                    pass
            m = d.get("message", {})
            u, mid = m.get("usage"), m.get("id")
            fam = family(m.get("model"))
            if not u or not fam or mid in seen:
                continue
            seen.add(mid)
            x = cost(fam, u)
            by_model[fam] += x
            side = "subagent" if (sub or d.get("isSidechain")) else "main"
            by_side[side] += x
            if fam == "opus" and side == "main":
                opus_turn[prev] += x
            if fam == "fable":
                fable_dir[folder] += x
    auto = collections.Counter()
    if BRIDGE_LOG.exists():
        since = (dt.datetime.now() - dt.timedelta(days=days)).strftime("%Y-%m-%d")
        for line in BRIDGE_LOG.open():
            try:
                r = json.loads(line)
            except ValueError:
                continue
            fam = family(r.get("model"))
            if fam and r.get("ts", "") >= since:
                # bridge logs input incl. cache reads; treat as plain input (upper bound)
                auto[fam] += cost(fam, {"input_tokens": r.get("input_tokens", 0), "output_tokens": r.get("output_tokens", 0)})
    return {"date": dt.date.today().isoformat(), "days": days,
            "interactive_by_model": dict(by_model), "interactive_by_side": dict(by_side),
            "opus_main_turns": dict(opus_turn), "fable_by_folder": dict(fable_dir.most_common(8)),
            "automation_by_model": dict(auto)}


def pct(d: dict) -> dict:
    t = sum(d.values()) or 1
    return {k: round(v / t * 100, 1) for k, v in sorted(d.items(), key=lambda kv: -kv[1])}


def show(s: dict) -> None:
    inter, auto = sum(s["interactive_by_model"].values()), sum(s["automation_by_model"].values())
    print(f"== {s['date']} 기준 최근 {s['days']}일 (API 가격 환산 추정치) ==")
    print(f"대화창 ${inter:,.0f} · 자동 작업 ${auto:,.0f} · 합계 ${inter + auto:,.0f}")
    print("대화창 모델별 %:", pct(s["interactive_by_model"]))
    print("본창/일꾼 %:", pct(s["interactive_by_side"]))
    print("Opus 본창 대화/실행 %:", pct(s["opus_main_turns"]))
    print("Fable 쓴 폴더($):", {k: round(v) for k, v in s["fable_by_folder"].items()})


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--compare")
    a = ap.parse_args()
    s = collect(a.days)
    show(s)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / f"{s['date']}.json").write_text(json.dumps(s, ensure_ascii=False, indent=1))
    if a.compare:
        b = json.loads(Path(a.compare).expanduser().read_text())
        tot = lambda x: sum(x["interactive_by_model"].values()) + sum(x["automation_by_model"].values())
        print(f"\n== 비교: {b['date']} → {s['date']} ==")
        print(f"전체 ${tot(b):,.0f} → ${tot(s):,.0f} ({(tot(s) / tot(b) - 1) * 100:+.1f}%)")
        for key, label in (("interactive_by_model", "모델별"), ("interactive_by_side", "본창/일꾼")):
            print(f"{label} %: {pct(b[key])} → {pct(s[key])}")
        print("(주의: 일한 양 자체가 다르면 총액은 같이 움직인다 — 비중 변화를 함께 볼 것)")


if __name__ == "__main__":
    main()
