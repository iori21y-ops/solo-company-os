"""Minimal markdown -> phone-friendly HTML (headings, tables, lists, quotes, bold, code)."""
import html, re, sys

def inline(t):
    t = html.escape(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    return t

def convert(md):
    out, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s\-|:]+\|$", lines[i + 1]):
            head = [c.strip() for c in l.strip("|").split("|")]
            rows = []
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip("|").split("|")]); i += 1
            if len(head) > 3:  # wide table -> one card per row (phone width)
                for r in rows:
                    title = " ".join(inline(c) for c in r[:2]) if head[0] == "#" else inline(r[0])
                    rest = list(zip(head, r))[2 if head[0] == "#" else 1:]
                    out.append(f'<div class="card"><div class="ct">{title}</div>' + "".join(
                        f'<div class="kv"><span class="k">{inline(k)}</span><span class="v">{inline(v)}</span></div>' for k, v in rest if v and v != "—") + "</div>")
            else:
                out.append("<table><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr>")
                for r in rows:
                    out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
                out.append("</table>")
            continue
        m = re.match(r"^(#{1,4}) (.*)", l)
        if m:
            n = len(m.group(1)); out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
        elif l.startswith("> "):
            out.append(f"<blockquote>{inline(l[2:])}</blockquote>")
        elif re.match(r"^\s*(- |\d+\. )", l):
            out.append("<ul>")
            while i < len(lines) and re.match(r"^\s*(- |\d+\. )", lines[i]):
                item = re.sub(r"^\s*(- |\d+\. )", "", lines[i])
                sub = ' class="sub"' if lines[i].startswith("  ") else ""
                out.append(f"<li{sub}>{inline(item)}</li>"); i += 1
            out.append("</ul>"); continue
        elif l.strip():
            out.append(f"<p>{inline(l)}</p>")
        i += 1
    html_out, opened = [], False
    for o in out:
        if o.startswith("<h2>"):
            if opened: html_out.append("</section>")
            html_out.append('<section class="sec">'); opened = True
        elif not opened and o.startswith("<h1>"):
            html_out.append('<section class="sec">'); opened = True
        html_out.append(o)
    if opened: html_out.append("</section>")
    return "\n".join(html_out)

CSS = """body{font-family:-apple-system,'Apple SD Gothic Neo',sans-serif;margin:0;padding:16px;font-size:17px;line-height:1.6;color:#111;background:#fff}
h1{font-size:24px;color:#1f4d3a;margin-top:4px}h2{font-size:21px;margin-top:6px;border-bottom:2px solid #1f4d3a;padding-bottom:4px;color:#1f4d3a}
table{border-collapse:collapse;width:100%;font-size:15px;margin:8px 0}th,td{border:1px solid #ccc;padding:6px;vertical-align:top}th{background:#eef4f0}
blockquote{margin:6px 0;padding:8px 12px;background:#f6f6f6;border-left:4px solid #e8c547;font-size:15px}
code{background:#f1f1f1;padding:1px 4px;border-radius:4px;font-size:12px}li.sub{margin-left:18px;list-style:circle}
.sec{padding:14px 2px 18px}li{margin:4px 0}
.card{border:1px solid #d5e2da;border-radius:12px;padding:10px 12px;margin:10px 0;background:#fbfdfc}.ct{font-weight:800;color:#fff;background:#1f4d3a;margin:-10px -12px 8px;padding:8px 12px;border-radius:12px 12px 0 0;font-size:18px}
.kv{display:flex;gap:10px;padding:6px 0;border-top:1px dashed #e3e3e3;font-size:16px}.k{flex:0 0 96px;color:#5a6b62;font-size:14px;font-weight:600}.v{flex:1}"""

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    body = convert(open(src, encoding="utf-8").read())
    open(dst, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>{CSS}</style></head><body>{body}</body></html>')
