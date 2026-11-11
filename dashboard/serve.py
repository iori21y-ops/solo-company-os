#!/usr/bin/env python3
"""Serve the dashboard to the owner's phone over Tailscale.

Shares only ./public (the copy build.py writes) and listens only on this Mac's Tailscale address,
so the page is reachable from the owner's own Tailscale devices and nowhere else.
Run by launchd (launchd/com.blogengine.dashboard-web.plist); if Tailscale is not up yet it exits and launchd retries.

  http://100.64.130.22:8787/
"""
from __future__ import annotations

import functools
import http.server
import re
import subprocess
import sys
from pathlib import Path

PORT = 8787
PUBLIC = Path(__file__).resolve().parent / "public"


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


def main() -> int:
    PUBLIC.mkdir(exist_ok=True)
    ip = tailscale_ip()
    server = http.server.ThreadingHTTPServer((ip, PORT), functools.partial(Handler, directory=str(PUBLIC)))
    print(f"serving {PUBLIC} on http://{ip}:{PORT}/", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    sys.exit(main())
