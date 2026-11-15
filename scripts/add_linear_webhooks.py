#!/usr/bin/env python3
"""Add the Linear "Link commits to issues" push webhook to every iori21y-ops repo (skips repos that already have it).

URL/secret are read from ~/.cadam-secrets/linear_github_webhook.env and never printed.
Run:  /usr/bin/python3 ~/projects/_meta/scripts/add_linear_webhooks.py
"""
import json
import os
import subprocess

env = os.path.expanduser("~/.cadam-secrets/linear_github_webhook.env")
d = dict(l.rstrip("\n").split("=", 1) for l in open(env) if "=" in l)
url, secret = d["URL"], d.get("SECRET", "")
repos = subprocess.run(["gh", "repo", "list", "iori21y-ops", "--limit", "100", "--json", "name", "-q", ".[].name"],
                       capture_output=True, text=True).stdout.split()
ok = skip = fail = 0
for r in repos:
    existing = subprocess.run(["gh", "api", f"repos/iori21y-ops/{r}/hooks", "-q", ".[].config.url"],
                              capture_output=True, text=True).stdout
    if url in existing:
        skip += 1
        print("skip ", r)
        continue
    body = {"name": "web", "active": True, "events": ["push"],
            "config": {"url": url, "content_type": "json", "secret": secret, "insecure_ssl": "0"}}
    p = subprocess.run(["gh", "api", "-X", "POST", f"repos/iori21y-ops/{r}/hooks", "--input", "-", "-q", ".id"],
                       input=json.dumps(body), capture_output=True, text=True)
    if p.returncode == 0:
        ok += 1
        print("added", r)
    else:
        fail += 1
        err = p.stderr.replace(url, "<url>")
        if secret:
            err = err.replace(secret, "<secret>")
        print("FAIL ", r, err[:150])
print(f"\nadded {ok}, skipped {skip}, failed {fail}")
