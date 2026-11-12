#!/usr/bin/env python3
"""Serve the dashboard to the owner's phone over Tailscale.

RETIRED 2026-11-12: the page is shown inside the ERP (/engine-dashboard, cadam-erp src/lib/engine-dashboard.ts);
launchd com.blogengine.dashboard-web was booted out and its plist renamed to .disabled. Kept for reference / rollback.

Shares only ./public (the copy build.py writes) and listens only on this Mac's Tailscale address,
so the page is reachable from the owner's own Tailscale devices and nowhere else.
Run by launchd (launchd/com.blogengine.dashboard-web.plist); if Tailscale is not up yet it exits and launchd retries.

  http://100.64.130.22:8787/
"""
from __future__ import annotations

import functools
import json
import http.server
import re
import subprocess
import sys
from pathlib import Path

PORT = 8787
PUBLIC = Path(__file__).resolve().parent / "public"
RUN = Path.home() / "projects/blog-engine/run.py"
BUILD = Path(__file__).resolve().parent / "build.py"
CHECK = {"kind": re.compile(r"^(topic|candidate|wp)$"), "do": re.compile(r"^(publish|delete|pick|dismiss)$"),
         "id": re.compile(r"^([0-9a-f-]{36}|\d{1,9})?$"), "date": re.compile(r"^(\d{4}-\d{2}-\d{2})?$"), "code": re.compile(r"^(B\d{1,2})?$")}


def tailscale_ip() -> str:
    """This Mac's Tailscale address (100.64.0.0/10), read from the network interfaces (the Tailscale CLI does not answer under launchd)."""
    out = subprocess.run(["/sbin/ifconfig"], capture_output=True, text=True, timeout=10).stdout
    for ip in re.findall(r"inet (100\.(\d+)\.\d+\.\d+)", out):
        if 64 <= int(ip[1]) <= 127:
            return ip[0]
    raise SystemExit("Tailscale address not found (is Tailscale running?)")


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")   # always show the latest rebuild
        super().end_headers()

    def list_directory(self, path):  # no folder listings
        self.send_error(404)

    def log_message(self, *args):  # keep the log quiet
        pass

    def reply(self, code: int, obj: dict) -> None:
        data = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        """Dashboard buttons → `run.py rentailor dash-action` only (all writes and guards live in blog-engine)."""
        if self.path != "/api/action":
            return self.reply(404, {"ok": False, "msg": "없는 주소"})
        if self.headers.get("X-Dashboard") != "1" or self.headers.get("Origin") != f"http://{self.headers.get('Host')}":
            return self.reply(403, {"ok": False, "msg": "대시보드 화면에서 보낸 요청이 아닙니다"})
        try:
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(min(n, 2048)) or b"{}")
            a = {k: str(body.get(k) or "") for k in CHECK}
            if not all(CHECK[k].match(a[k]) for k in CHECK) or not a["kind"] or not a["do"]:
                return self.reply(400, {"ok": False, "msg": "잘못된 요청"})
        except ValueError:
            return self.reply(400, {"ok": False, "msg": "잘못된 요청"})
        argv = ["/usr/bin/python3", str(RUN), "rentailor", "dash-action", a["kind"], "--do", a["do"]]
        for k in ("id", "date", "code"):
            if a[k]:
                argv += [f"--{k}", a[k]]
        try:
            r = subprocess.run(argv, capture_output=True, text=True, timeout=420, cwd="/tmp")
            line = (r.stdout.strip().splitlines() or ["{}"])[-1]
            res = json.loads(line) if line.startswith("{") else {"ok": False, "msg": (r.stderr or "응답 없음")[-200:]}
        except subprocess.TimeoutExpired:
            res = {"ok": False, "msg": "시간 초과 — 디스코드·대시보드에서 결과를 확인하세요"}
        if res.get("ok"):
            subprocess.Popen(["/usr/bin/python3", str(BUILD)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        return self.reply(200, res)


def main() -> int:
    PUBLIC.mkdir(exist_ok=True)
    ip = tailscale_ip()
    server = http.server.ThreadingHTTPServer((ip, PORT), functools.partial(Handler, directory=str(PUBLIC)))
    print(f"serving {PUBLIC} on http://{ip}:{PORT}/", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
