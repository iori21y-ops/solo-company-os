#!/usr/bin/env node
// 결재물(.md) 모바일 뷰어 — 의존성 0, Node 내장 http만 사용.
// Tailscale 망 안에서만 접근 허용(로그인 없음). 결재물 .md를 표·서식 그대로 렌더링.
// 접근: http://macmini.tail466d13.ts.net:9724/

import { createServer } from "node:http";
import { readFile, readdir, stat } from "node:fs/promises";
import { existsSync } from "node:fs";
import { resolve, join, basename, sep } from "node:path";

const ROOT = "/Users/kim/projects/_meta/agents";
const PORT = Number(process.env.MD_VIEWER_PORT || 9724);
const STAGES = ["pending", "approved", "rejected"];

// Tailscale(100.64.0.0/10)·로컬호스트만 허용. 집 LAN 등 외부 차단.
function isAllowed(req) {
  const a = String(req.socket.remoteAddress || "");
  return (
    a.startsWith("100.") ||
    a.startsWith("::ffff:100.") ||
    a === "127.0.0.1" ||
    a === "::1" ||
    a === "::ffff:127.0.0.1"
  );
}

// p(상대경로)를 ROOT 안의 .md 파일로만 안전하게 해석. 경로 탈출·비-md 차단.
function safeMdPath(p) {
  if (!p) return null;
  const abs = resolve(ROOT, p);
  if (abs !== ROOT && !abs.startsWith(ROOT + sep)) return null;
  if (!abs.toLowerCase().endsWith(".md")) return null;
  // macOS 파일명은 NFD로 저장됨. 입력이 NFC여도 매칭되도록 정규화 폴백.
  for (const cand of [abs, abs.normalize("NFD"), abs.normalize("NFC")]) {
    if (existsSync(cand)) return cand;
  }
  return null;
}

function esc(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

function pageShell(title, inner) {
  return `<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css@5/github-markdown.min.css">
<style>
  body{margin:0;background:#0d1117;color:#c9d1d9;font-family:-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",sans-serif}
  .wrap{max-width:900px;margin:0 auto;padding:16px}
  .markdown-body{background:#0d1117;color:#c9d1d9;padding:8px}
  a{color:#58a6ff}
  .top{padding:10px 16px;background:#161b22;border-bottom:1px solid #30363d;position:sticky;top:0}
  .top a{margin-right:14px;text-decoration:none}
  .item{display:block;padding:12px 14px;margin:8px 0;background:#161b22;border:1px solid #30363d;border-radius:8px;text-decoration:none;color:#c9d1d9}
  .item:hover{border-color:#58a6ff}
  .badge{font-size:12px;color:#8b949e}
  h2{border-bottom:1px solid #30363d;padding-bottom:6px}
</style></head><body>
<div class="top"><a href="/">📋 결재물 목록</a></div>
<div class="wrap">${inner}</div>
</body></html>`;
}

async function listPage() {
  const agents = (await readdir(ROOT, { withFileTypes: true }))
    .filter((d) => d.isDirectory() && !d.name.startsWith("_") && !d.name.startsWith("."))
    .map((d) => d.name)
    .sort();
  let html = "<h1>결재물</h1>";
  for (const agent of agents) {
    let agentBlock = "";
    for (const stage of STAGES) {
      const dir = join(ROOT, agent, "outputs", stage);
      if (!existsSync(dir)) continue;
      let files = [];
      try {
        files = (await readdir(dir)).filter((f) => f.toLowerCase().endsWith(".md"));
      } catch { continue; }
      if (stage === "pending" && files.length === 0) continue;
      if (stage !== "pending" && files.length === 0) continue;
      for (const f of files.sort().reverse()) {
        const rel = join(agent, "outputs", stage, f);
        const icon = stage === "pending" ? "🟡 대기" : stage === "approved" ? "✅ 승인" : "❌ 반려";
        agentBlock += `<a class="item" href="/v?p=${encodeURIComponent(rel)}">${esc(f)}<br><span class="badge">${icon} · ${esc(agent)}</span></a>`;
      }
    }
    if (agentBlock) html += `<h2>${esc(agent)}</h2>${agentBlock}`;
  }
  if (html === "<h1>결재물</h1>") html += "<p>표시할 결재물이 없습니다.</p>";
  return pageShell("결재물 목록", html);
}

function viewPage(rel) {
  // 클라이언트에서 raw .md를 받아 marked로 렌더. 표·코드블록 모두 지원.
  return pageShell(basename(rel), `
<div id="md" class="markdown-body">불러오는 중…</div>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script>
  fetch('/raw?p=${encodeURIComponent(rel)}').then(r=>r.text()).then(t=>{
    document.getElementById('md').innerHTML = marked.parse(t, {gfm:true, breaks:true});
  }).catch(e=>{ document.getElementById('md').textContent = '불러오기 실패: '+e; });
</script>`);
}

const server = createServer(async (req, res) => {
  if (!isAllowed(req)) {
    res.writeHead(403, { "content-type": "text/plain; charset=utf-8" });
    res.end("Tailscale 망에서만 접근할 수 있습니다.");
    return;
  }
  try {
    const url = new URL(req.url, "http://x");
    if (url.pathname === "/") {
      res.writeHead(200, { "content-type": "text/html; charset=utf-8" });
      res.end(await listPage());
      return;
    }
    if (url.pathname === "/v") {
      const rel = url.searchParams.get("p");
      if (!safeMdPath(rel)) { res.writeHead(404).end("not found"); return; }
      res.writeHead(200, { "content-type": "text/html; charset=utf-8" });
      res.end(viewPage(rel));
      return;
    }
    if (url.pathname === "/raw") {
      const abs = safeMdPath(url.searchParams.get("p"));
      if (!abs) { res.writeHead(404).end("not found"); return; }
      const body = await readFile(abs, "utf-8");
      res.writeHead(200, { "content-type": "text/plain; charset=utf-8" });
      res.end(body);
      return;
    }
    res.writeHead(404).end("not found");
  } catch (e) {
    res.writeHead(500, { "content-type": "text/plain; charset=utf-8" });
    res.end("error: " + (e?.message || e));
  }
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`md-viewer listening on 0.0.0.0:${PORT} (tailnet-only), ROOT=${ROOT}`);
});
