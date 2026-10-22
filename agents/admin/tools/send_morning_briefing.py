#!/usr/bin/env python3
"""Send the stocks morning briefing (briefing_data.json) to Discord as embeds.

Used by 관리팀장's "모닝 브리핑" mission (see ../SKILL.md). This script only
does mechanical work: read the JSON, assemble Discord embeds in the fixed
section order, split across embeds/messages to respect Discord limits, and
POST them. Writing the "관전포인트" commentary and per-stock analysis
comments is 관리팀장's own judgment call (grounded in the JSON's us/kr/
score_detail/수급 values and 관리팀장's own WebSearch results) -- pass the
market commentary in via --commentary/--commentary-file and per-stock
comments via --stock-comments-file (JSON {ticker: comment}); this script
does not fabricate either.

Weekday sends split into two Discord messages: ①시황+가치Top5(+코멘트),
②낙폭과대Top5(+코멘트)+보유평가+종목별뉴스+고지. --stock-comments-file is
optional -- omitting it reproduces the pre-comment single-embeds-per-Top5
behavior exactly (backward compatible), just still split across the two
messages.

English comments per repo convention; secrets are never printed.
"""
import argparse
import json
import os
import sys
import time
import urllib.parse

import requests

BRIEFING_PATH_DEFAULT = os.path.expanduser("~/projects/stocks/data/briefing_data.json")
CHARTS_DIR_DEFAULT = os.path.expanduser("~/projects/stocks/data/charts")
ENV_PATH_DEFAULT = os.path.expanduser("~/.openclaw/workspace/claude-broker/.env")
CHANNEL_ID_DEFAULT = "1527296041169322135"
STATE_PATH_DEFAULT = os.path.expanduser("~/projects/_meta/agents/admin/tools/.morning-briefing-state.json")
DISCORD_API = "https://discord.com/api/v10"

EMBED_TOTAL_MAX = 6000     # per-embed cap: pack_embeds() splits an embed's own fields once ITS OWN total hits this
FIELD_VALUE_MAX = 1024
FIELD_NAME_MAX = 256
FIELDS_PER_EMBED_MAX = 25
EMBEDS_PER_MESSAGE_MAX = 10
# Discord's real 6000-char embed limit is actually the SUM across ALL embeds
# in a single message, not per-embed (see chunk_into_messages) -- discovered
# 2026-07-23 when per-stock comment fields pushed a message's embed total
# past 6000 while each individual embed still measured under 6000.
MESSAGE_EMBED_TOTAL_MAX = 6000
MAX_ATTACHMENT_BYTES = 10 * 1024 * 1024  # Discord per-file cap

COLOR_RISK = 0xE74C3C    # red: used when KOSPI fell sharply (<= -3%)
COLOR_NORMAL = 0x3498DB  # blue: normal/positive day
RISK_CHG_THRESHOLD = -3.0

MANDATORY_DISCLAIMER_LINE = "매수/매도 제안가는 기계적 산출 참고선입니다."


def load_state(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_state(path, trading_date):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"last_sent_trading_date": trading_date, "sent_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}, f, ensure_ascii=False, indent=2)


def post_failure_alert(token, channel_id, stage, detail=""):
    """Best-effort one-line failure notice. Never raises -- a broken alert
    must not mask or replace the original failure."""
    try:
        headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
        content = f"⚠️ 모닝 브리핑 생성 실패: {stage}"
        if detail:
            content += f"\n{detail[:300]}"
        requests.post(
            f"{DISCORD_API}/channels/{channel_id}/messages",
            headers=headers, json={"content": content[:2000]}, timeout=20,
        )
    except Exception as e:
        print(f"[send_morning_briefing] failure-alert itself failed: {e}", file=sys.stderr)


def load_env(path):
    env = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def _field(name, value, inline=False):
    return {"name": str(name)[:FIELD_NAME_MAX], "value": str(value or "-")[:FIELD_VALUE_MAX], "inline": inline}


def _embed_char_count(embed):
    total = len(embed.get("title", "")) + len(embed.get("description", ""))
    total += len(embed.get("footer", {}).get("text", ""))
    for f in embed.get("fields", []):
        total += len(f["name"]) + len(f["value"])
    return total


def pack_embeds(title, fields, description=None, color=COLOR_NORMAL):
    """Pack a flat list of fields into 1+ embeds honoring Discord's per-embed
    6000-char total and 25-field limits. Continuation embeds get "(계속)"."""
    embeds = []
    current = {"title": title, "color": color, "fields": []}
    if description:
        current["description"] = description[:4096]
    for f in fields:
        candidate_fields = current["fields"] + [f]
        candidate = {**current, "fields": candidate_fields}
        if (_embed_char_count(candidate) > EMBED_TOTAL_MAX or len(candidate_fields) > FIELDS_PER_EMBED_MAX) and current["fields"]:
            embeds.append(current)
            current = {"title": f"{title} (계속)", "color": color, "fields": [f]}
        else:
            current["fields"] = candidate_fields
    embeds.append(current)
    return embeds


def fmt_num(val, digits=2):
    if not isinstance(val, (int, float)):
        return "-"
    return f"{val:,.{digits}f}"


def fmt_pct(val):
    if not isinstance(val, (int, float)):
        return None
    return f"{val:+.2f}%"


def build_us_embeds(us_items):
    fields = []
    for item in us_items:
        chg = fmt_pct(item.get("chg"))
        value = fmt_num(item.get("val")) + (f" ({chg})" if chg else "")
        fields.append(_field(item["name"], value, inline=True))
    return pack_embeds("🇺🇸 미국장 지표", fields)


def build_regime_line(market_regime):
    """market_regime (regime.py output via briefing_data.json) -> one summary
    line if every index is 상승, else a ⚠️ warning line naming which index is
    below which MA line (reusing each index's own `basis` sentence). Returns
    None if market_regime is missing/empty (regime calc failed upstream) --
    per spec, a regime failure omits the warning rather than fabricating one."""
    if not market_regime:
        return None
    non_up = [info for info in market_regime.values() if info.get("regime") != "상승"]
    if not non_up:
        return "국면: " + " · ".join(f"{name} 상승" for name in market_regime)
    return "⚠️ 국면 경고\n" + "\n".join(info["basis"] for info in non_up)


def build_kr_embeds(kr_items, market_regime=None):
    fields = []
    kospi_chg = None
    for item in kr_items:
        if item["name"] == "코스피":
            kospi_chg = item.get("chg")
        if "순매수" in item["name"]:
            value = fmt_num(item.get("val") / 1e8 if isinstance(item.get("val"), (int, float)) else None, 0)
            value = f"{value}억" if value != "-" else "-"
        else:
            chg = fmt_pct(item.get("chg"))
            value = fmt_num(item.get("val")) + (f" ({chg})" if chg else "")
        fields.append(_field(item["name"], value, inline=True))
    regime_line = build_regime_line(market_regime)
    if regime_line:
        fields.append(_field("국면", regime_line, inline=False))
    color = COLOR_RISK if isinstance(kospi_chg, (int, float)) and kospi_chg <= RISK_CHG_THRESHOLD else COLOR_NORMAL
    return pack_embeds("🇰🇷 코스피·수급", fields, color=color), color


def build_commentary_embed(commentary_text, color):
    return pack_embeds("📌 관전포인트", [], description=commentary_text, color=color)


def _build_levels_basis_lines(levels):
    # 1-line basis digest: buy1/buy2/target basis strings end in "-> X 채택",
    # take that tail; stop1/stop2 basis is already a short "A x 0.93 = B" formula.
    lines = []
    for key, label in [("buy1", "1차매수"), ("buy2", "2차매수"), ("target1", "1차목표"), ("target", "2차목표"), ("stop1", "손절1"), ("stop2", "손절2")]:
        lvl = levels.get(key)
        if not lvl or lvl.get("px") is None:
            continue
        full_basis = lvl.get("basis", "")
        basis_short = full_basis.split("→")[-1].strip() if "→" in full_basis else full_basis
        lines.append(f"· {label} {lvl['px']:,}({lvl['pct']:+.1f}%): {basis_short}")
    return lines


def build_comment_field(pick, stock_comments):
    comment = stock_comments.get(pick["ticker"], "코멘트 없음")
    return _field(f"💬 {pick['name']} 코멘트", comment, inline=False)


def build_pick_field(pick):
    br_labels = ["밸류", "수급", "실적", "배당", "모멘텀", "미국장"]
    br = pick.get("br") or []
    br_str = " / ".join(f"{lbl} {v:.1f}" for lbl, v in zip(br_labels, br))

    tags = pick.get("tags") or []
    tag_str = ", ".join(t.get("label", "") for t in tags) if tags else "-"

    basis_lines = _build_levels_basis_lines(pick.get("levels") or {})

    value = (
        f"총점 {pick['score']:.1f} [{br_str}]\n"
        f"PER {pick.get('per')} / PBR {pick.get('pbr')} / 배당 {pick.get('div')}%\n"
        + "\n".join(basis_lines) + "\n"
        f"태그: {tag_str}"
    )
    name = f"🎯 #{pick['rank']} {pick['name']}({pick['ticker']})"
    return _field(name, value, inline=False)


def _attach_chart(embed, charts_dir, filename):
    """Set embed['image'] to attachment://<filename> only if that file
    actually exists under charts_dir -- a missing/unreadable chart just
    leaves the embed text-only rather than referencing an attachment that
    was never uploaded (which would render as a broken image)."""
    if charts_dir and os.path.exists(os.path.join(charts_dir, filename)):
        embed["image"] = {"url": f"attachment://{filename}"}


def build_picks_embeds(picks, stock_comments=None):
    fields = []
    for p in picks:
        fields.append(build_pick_field(p))
        if stock_comments is not None:
            fields.append(build_comment_field(p, stock_comments))
    return pack_embeds("🎯 추천 Top5", fields)


def build_swing_pick_field(pick):
    detail = pick.get("score_detail") or []
    detail_str = " / ".join(f"{d['name']} {d['pts']:.1f}/{d['max']}" for d in detail)

    tags = pick.get("tags") or []
    tag_str = ", ".join(t.get("label", "") for t in tags) if tags else "-"

    basis_lines = _build_levels_basis_lines(pick.get("levels") or {})

    value = (
        f"스윙총점 {pick['score']:.1f} [{detail_str}]\n"
        + "\n".join(basis_lines) + "\n"
        f"태그: {tag_str}"
    )
    name = f"🔄 #{pick['rank']} {pick['name']}({pick['ticker']})"
    return _field(name, value, inline=False)


def build_swing_picks_embeds(swing_picks, stock_comments=None):
    fields = []
    for p in swing_picks:
        fields.append(build_swing_pick_field(p))
        if stock_comments is not None:
            fields.append(build_comment_field(p, stock_comments))
    return pack_embeds("🔄 낙폭과대 반등 Top5", fields)


def build_holdings_embeds(holdings):
    fields = []
    for h in holdings:
        levels = h.get("levels") or {}
        stop_personal = levels.get("stop_personal")
        sp_line = f"개인화 손절: {stop_personal['px']:,}({stop_personal['pct']:+.1f}%)" if stop_personal else "개인화 손절: -"
        pl_won = h.get("pl_won")
        pl_pct = h.get("pl_pct")
        value = (
            f"현재가 {fmt_num(h.get('cur'))} / 평단 {fmt_num(h.get('avg'))}\n"
            f"평가손익 {fmt_num(pl_won, 0)}원 ({fmt_pct(pl_pct)})\n"
            f"{sp_line}\n"
            f"신호: {h.get('signal')}"
        )
        fields.append(_field(f"💼 {h['name']}({h['ticker']})", value, inline=False))
    return pack_embeds("💼 보유 평가", fields)


def build_news_embeds(picks):
    fields = []
    for p in picks:
        fields.append(_field(f"📰 {p['name']}", p.get("news", "-"), inline=False))
    return pack_embeds("📰 종목별 뉴스", fields)


def is_us_only(data):
    """Weekend lightweight briefing: main.py --us-only output has no
    "picks" key at all (weekday output always has it, even if empty list)."""
    return "picks" not in data


PERFORMANCE_SECTION_LABELS = {"value": "가치 Top5", "swing": "낙폭과대 Top5"}
PERFORMANCE_STATUS_LABELS = {"target_hit": "목표도달", "stop_hit": "손절", "expired": "만료"}
PERFORMANCE_DETAIL_MAX_LINES = 10  # per-section closed-trade detail cap; excess is summarized, not silently dropped


def build_performance_embeds(weekly_performance):
    """history/performance_report.json embedded via performance.py's
    build_weekly_report() output -- see stocks/performance.py. Absent or
    still-accumulating data renders a single placeholder embed instead of
    failing (weekend briefing must not break because performance tracking
    hasn't accumulated a sample yet)."""
    if not weekly_performance or weekly_performance.get("status") == "데이터 축적 중":
        return pack_embeds("📊 추천 성과 (주간)", [_field("상태", "데이터 축적 중 (표본 쌓이는 중)", inline=False)])

    fields = []
    sections = weekly_performance.get("sections") or {}
    for key, label in PERFORMANCE_SECTION_LABELS.items():
        section = sections.get(key)
        if not section:
            continue

        if section.get("sample_note"):
            summary = section["sample_note"]
        else:
            summary = (
                f"승률 {section.get('win_rate_pct')}% (종결 {section.get('closed_count')}건)\n"
                f"평균 {section.get('avg_return_pct')}% / 최고 {section.get('max_return_pct')}% / 최저 {section.get('min_return_pct')}%"
            )
        open_summary = section.get("open_summary") or {}
        summary += f"\n진행 중 {open_summary.get('count', 0)}건, 평균 평가수익률 {open_summary.get('avg_return_pct')}%"
        fields.append(_field(f"{label} 성과", summary, inline=False))

        detail = section.get("closed_detail") or []
        if detail:
            lines = []
            for d in detail[:PERFORMANCE_DETAIL_MAX_LINES]:
                status_label = PERFORMANCE_STATUS_LABELS.get(d.get("status"), d.get("status"))
                both = " (동시도달, 손절우선)" if d.get("both_hit") else ""
                return_pct = d.get("return_pct")
                return_str = f"{return_pct:+.1f}%" if isinstance(return_pct, (int, float)) else "-"
                lines.append(f"· {d.get('name')}({d.get('ticker')}) {status_label}{both} {return_str} ({d.get('holding_days')}일)")
            if len(detail) > PERFORMANCE_DETAIL_MAX_LINES:
                lines.append(f"...외 {len(detail) - PERFORMANCE_DETAIL_MAX_LINES}건 생략")
            fields.append(_field(f"{label} 종결 내역", "\n".join(lines), inline=False))

    return pack_embeds("📊 추천 성과 (주간)", fields)


def build_weekend_embeds(data, commentary_text):
    """Saturday briefing: US indicators + 관리팀장 commentary + 추천 성과
    + disclaimer. No KR section, no picks, no holdings -- see admin/SKILL.md
    §8-1 weekend branch."""
    embeds = []
    notice = build_error_notice(data.get("errors") or [])
    if notice:
        embeds.append(notice)
    embeds += pack_embeds(
        "🇺🇸 주말 브리핑 — 미국 금요장 마감",
        [_field(item["name"], fmt_num(item.get("val")) + (f" ({fmt_pct(item.get('chg'))})" if fmt_pct(item.get("chg")) else ""), inline=True) for item in (data.get("us") or [])],
    )
    embeds += pack_embeds("📌 관리팀장 코멘트", [], description=commentary_text)
    embeds += build_performance_embeds(data.get("weekly_performance"))
    embeds.append({"title": "고지", "color": 0x808080, "description": (data.get("disclaimer") or "")[:4096]})
    return embeds


def build_error_notice(errors):
    if not errors:
        return None
    text = "\n".join(f"- {e}" for e in errors[:10])
    return {"title": "⚠️ 데이터 수집 중 일부 실패", "color": COLOR_RISK, "description": text[:4096]}


def assemble_message1_embeds(data, commentary_text, stock_comments=None, charts_dir=None):
    """①시황+가치Top5: error notice, US/KR indicators, 관전포인트, 가치 Top5
    (+ per-stock comment fields if stock_comments is provided). charts_dir
    is None by default (--with-charts not passed) -- every line below is
    identical to the pre-charts behavior in that case."""
    embeds = []
    notice = build_error_notice(data.get("errors") or [])
    if notice:
        embeds.append(notice)
    embeds += build_us_embeds(data.get("us") or [])
    kr_embeds, color = build_kr_embeds(data.get("kr") or [], data.get("market_regime"))
    embeds += kr_embeds
    embeds += build_commentary_embed(commentary_text, color)
    picks_embeds = build_picks_embeds(data.get("picks") or [], stock_comments)
    if charts_dir and picks_embeds:
        _attach_chart(picks_embeds[0], charts_dir, "levels_value.png")
    embeds += picks_embeds
    return embeds


def assemble_message2_embeds(data, stock_comments=None, charts_dir=None):
    """②낙폭과대 반등Top5(+코멘트)+[스윙점수]+보유평가+종목별뉴스+고지. The
    스윙점수 embed only appears when charts_dir is set AND score_swing.png
    exists -- charts_dir=None (default) reproduces the pre-charts embed
    list exactly."""
    embeds = []
    swing_embeds = build_swing_picks_embeds(data.get("swing_top5") or [], stock_comments)
    if charts_dir and swing_embeds:
        _attach_chart(swing_embeds[0], charts_dir, "levels_swing.png")
    embeds += swing_embeds
    if charts_dir and os.path.exists(os.path.join(charts_dir, "score_swing.png")):
        embeds.append({"title": "📊 스윙 점수", "color": COLOR_NORMAL, "image": {"url": "attachment://score_swing.png"}})
    embeds += build_holdings_embeds(data.get("holdings") or [])
    embeds += build_news_embeds((data.get("picks") or []) + (data.get("swing_top5") or []))

    disclaimer_text = data.get("disclaimer") or ""
    if MANDATORY_DISCLAIMER_LINE not in disclaimer_text:
        disclaimer_text = f"{MANDATORY_DISCLAIMER_LINE} {disclaimer_text}".strip()
    embeds.append({"title": "고지", "color": 0x808080, "description": disclaimer_text[:4096]})
    return embeds


def _files_for_messages(messages, charts_dir):
    """Scan each already-chunked message's embeds for attachment://<file>
    image refs (set above when charts_dir was passed to assemble_message*)
    and build the files_per_message dict send_messages() expects. This is
    chunk-index-agnostic -- whichever message chunk_into_messages() put the
    image-bearing embed into is picked up automatically."""
    files_per_message = {}
    for i, embeds in enumerate(messages):
        found = []
        for e in embeds:
            url = (e.get("image") or {}).get("url", "")
            if url.startswith("attachment://"):
                found.append(os.path.join(charts_dir, url[len("attachment://"):]))
        if found:
            files_per_message[i] = found
    return files_per_message


def chunk_into_messages(embeds):
    """Split into Discord messages honoring BOTH limits: max 10 embeds/message
    AND max 6000 chars summed across all embeds in that message (Discord
    counts the latter per-message, not per-embed -- see MESSAGE_EMBED_TOTAL_MAX)."""
    messages = []
    current = []
    current_chars = 0
    for e in embeds:
        e_chars = _embed_char_count(e)
        if current and (len(current) >= EMBEDS_PER_MESSAGE_MAX or current_chars + e_chars > MESSAGE_EMBED_TOTAL_MAX):
            messages.append(current)
            current = []
            current_chars = 0
        current.append(e)
        current_chars += e_chars
    if current:
        messages.append(current)
    return messages


def _prepare_attachments(paths):
    """Filter to files that exist and are under Discord's per-file cap.
    Unreadable/oversize files are dropped with a warning -- a bad chart
    file must not abort the whole send (per spec)."""
    valid = []
    for path in paths or []:
        try:
            size = os.path.getsize(path)
        except OSError as e:
            print(f"[send_morning_briefing] 첨부 제외 (열기 실패): {path}: {e}", file=sys.stderr)
            continue
        if size > MAX_ATTACHMENT_BYTES:
            print(f"[send_morning_briefing] 첨부 제외 (10MB 초과, {size:,} bytes): {path}", file=sys.stderr)
            continue
        valid.append(path)
    return valid


def _post_multipart(token, channel_id, payload, files):
    """POST a message with file attachments. `files` is a list of local
    paths (already validated by _prepare_attachments). Builds the
    `attachments` array in payload_json and one files[N] part per file,
    per Discord's multipart attachment API; embeds reference images via
    attachment://<filename> (set by the caller before this is invoked)."""
    payload = {**payload, "attachments": [{"id": idx, "filename": os.path.basename(p)} for idx, p in enumerate(files)]}
    headers = {"Authorization": f"Bot {token}"}  # no Content-Type -- requests sets the multipart boundary
    handles = [open(p, "rb") for p in files]
    try:
        multipart_files = [
            (f"files[{idx}]", (os.path.basename(p), fh, "image/png"))
            for idx, (p, fh) in enumerate(zip(files, handles))
        ]
        return requests.post(
            f"{DISCORD_API}/channels/{channel_id}/messages",
            headers=headers,
            data={"payload_json": json.dumps(payload)},
            files=multipart_files,
            timeout=30,
        )
    finally:
        for fh in handles:
            fh.close()


def send_messages(token, channel_id, messages, dry_run=False, files_per_message=None):
    headers = {"Authorization": f"Bot {token}", "Content-Type": "application/json"}
    sent = []
    for i, embeds in enumerate(messages):
        payload = {"embeds": embeds}
        if dry_run:
            sent.append({"dry_run": True, "embeds": len(embeds)})
            continue
        files = _prepare_attachments((files_per_message or {}).get(i)) if files_per_message else None
        if files:
            resp = _post_multipart(token, channel_id, payload, files)
            if resp.status_code >= 300:
                raise RuntimeError(f"Discord API {resp.status_code}: {resp.text[:300]}")
            sent.append(resp.json())
            time.sleep(0.5)
            continue
        resp = requests.post(f"{DISCORD_API}/channels/{channel_id}/messages", headers=headers, json=payload, timeout=20)
        if resp.status_code >= 300:
            raise RuntimeError(f"Discord API {resp.status_code}: {resp.text[:300]}")
        sent.append(resp.json())
        time.sleep(0.5)  # be polite between messages in the same channel
    return sent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--briefing-path", default=BRIEFING_PATH_DEFAULT)
    ap.add_argument("--env-path", default=ENV_PATH_DEFAULT)
    ap.add_argument("--channel-id", default=CHANNEL_ID_DEFAULT)
    ap.add_argument("--state-path", default=STATE_PATH_DEFAULT)
    ap.add_argument("--commentary", default=None, help="관전포인트 text (3-5 sentences)")
    ap.add_argument("--commentary-file", default=None)
    ap.add_argument("--stock-comments-file", default=None, help="JSON {ticker: 4-6 sentence comment} for 가치+낙폭과대 Top10. Omit for backward-compatible behavior (no comment fields).")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--with-charts", action="store_true", help="attach data/charts/*.png images to the relevant embeds. Default OFF -- omitting this reproduces text-only behavior exactly (backward compatible)")
    ap.add_argument("--charts-dir", default=CHARTS_DIR_DEFAULT)
    ap.add_argument("--force", action="store_true", help="send even if kr_trading_date matches last_sent_trading_date")
    ap.add_argument("--alert-only", default=None, help="post the standard failure alert for <stage> and exit (used when an earlier pipeline stage, e.g. main.py, failed before this script even ran)")
    args = ap.parse_args()

    env = load_env(args.env_path)
    token = env.get("DISCORD_BOT_TOKEN")
    if not token:
        raise SystemExit(f"DISCORD_BOT_TOKEN not found in {args.env_path}")

    if args.alert_only:
        post_failure_alert(token, args.channel_id, args.alert_only)
        print(f"[send_morning_briefing] posted failure alert for stage: {args.alert_only}")
        return

    try:
        with open(args.briefing_path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        post_failure_alert(token, args.channel_id, "briefing_data.json 읽기", str(e))
        raise

    weekend_mode = is_us_only(data)
    trading_date = None
    if not weekend_mode:
        # Safety rule: skip if this trading date was already sent (market
        # holiday / weekend re-run reusing the same cached KR session). Not
        # a failure -- log only, no alert, no send. (No such dedup concept
        # for the weekend US-only briefing: its own card only fires once a
        # week via scheduledCardPoll's own cadence=weekly dedup.)
        trading_date = data.get("kr_trading_date")
        state = load_state(args.state_path)
        if not args.force and trading_date and state.get("last_sent_trading_date") == trading_date:
            print(f"[send_morning_briefing] 휴장일 스킵: 기준일 {trading_date} 은(는) 이미 발송됨 (직전 발송: {state.get('sent_at')})")
            return

    commentary = args.commentary
    if not commentary and args.commentary_file:
        with open(args.commentary_file, encoding="utf-8") as f:
            commentary = f.read().strip()
    if not commentary:
        raise SystemExit("commentary is required (--commentary or --commentary-file); this script does not invent it")

    stock_comments = None
    if args.stock_comments_file:
        with open(args.stock_comments_file, encoding="utf-8") as f:
            stock_comments = json.load(f)

    charts_dir = args.charts_dir if args.with_charts else None

    try:
        if weekend_mode:
            embeds = build_weekend_embeds(data, commentary)
            messages = chunk_into_messages(embeds)
        else:
            msg1_embeds = assemble_message1_embeds(data, commentary, stock_comments, charts_dir=charts_dir)
            msg2_embeds = assemble_message2_embeds(data, stock_comments, charts_dir=charts_dir)
            embeds = msg1_embeds + msg2_embeds
            # keep the ①/② split intact even if either side's own embeds
            # overflow the 10-embeds-per-message limit and need continuation
            messages = chunk_into_messages(msg1_embeds) + chunk_into_messages(msg2_embeds)

        total_chars = sum(_embed_char_count(e) for e in embeds)
        print(f"[send_morning_briefing] embeds={len(embeds)} messages={len(messages)} total_chars={total_chars}")
        for i, msg_embeds in enumerate(messages, start=1):
            titles = ", ".join(e.get("title", "") for e in msg_embeds)
            print(f"  message {i}: {len(msg_embeds)} embed(s) -> {titles}")

        files_per_message = _files_for_messages(messages, charts_dir) if charts_dir else None
        results = send_messages(token, args.channel_id, messages, dry_run=args.dry_run, files_per_message=files_per_message)
    except Exception as e:
        post_failure_alert(token, args.channel_id, "디스코드 발송", str(e))
        raise

    for r in results:
        if args.dry_run:
            print("  [dry-run]", r)
        else:
            print(f"  sent message id={r.get('id')}")

    if not args.dry_run and trading_date:
        save_state(args.state_path, trading_date)
        print(f"[send_morning_briefing] 상태 파일 갱신: last_sent_trading_date={trading_date} -> {args.state_path}")


if __name__ == "__main__":
    main()
