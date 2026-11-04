#!/usr/bin/env python3
"""Replace every n8n Telegram node with an HTTP Request node that posts to Discord #시스템알림.

The Discord bot token is stored once as an n8n credential (httpHeaderAuth, encrypted by n8n), never inside a
workflow JSON. Node names/positions/connections are kept, so the rest of each workflow is untouched.
Each workflow is backed up before it is changed; one failing workflow does not stop the others.

  python3 n8n_telegram_to_discord.py            # dry-run: list what would change, change nothing
  python3 n8n_telegram_to_discord.py --apply    # create credential (if missing), back up, update workflows
  python3 n8n_telegram_to_discord.py --restore DIR   # put the backed-up workflows from DIR back
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

HOME = Path.home()
SECRETS = HOME / ".cadam-secrets/secrets.env"
BROKER_ENV = HOME / ".openclaw/workspace/claude-broker/.env"
BACKUP_ROOT = HOME / "projects/_meta/n8n-backups"
CRED_NAME = "Discord Bot (시스템알림)"
CRED_FILE = BACKUP_ROOT / "discord_credential_id.txt"
SETTINGS_KEYS = {"executionOrder", "saveDataErrorExecution", "saveDataSuccessExecution", "saveManualExecutions",
                 "saveExecutionProgress", "timezone", "callerPolicy", "errorWorkflow"}
KEEP = ("id", "name", "position", "onError", "continueOnFail", "alwaysOutputData", "retryOnFail", "maxTries",
        "waitBetweenTries", "executeOnce", "disabled", "notes", "notesInFlow")


def envfile(path: Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


SEC = envfile(SECRETS)


def n8n(method: str, path: str, body: dict | None = None):
    req = urllib.request.Request(SEC["N8N_BASE_URL"].rstrip("/") + path, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"X-N8N-API-KEY": SEC["N8N_API_KEY"], "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"n8n HTTP {e.code} {method} {path}: {e.read()[:300]!r}") from None


def all_workflows() -> list[dict]:
    out, cursor = [], None
    while True:
        d = n8n("GET", "/api/v1/workflows?limit=100" + (f"&cursor={cursor}" if cursor else ""))
        out += d.get("data", [])
        cursor = d.get("nextCursor")
        if not cursor:
            return out


def http_node(old: dict, channel: str, cred: dict) -> dict:
    p = old.get("parameters", {})
    text = p.get("text", "")
    node = {k: old[k] for k in KEEP if k in old}
    node.update(
        type="n8n-nodes-base.httpRequest", typeVersion=4.2,
        parameters={
            "method": "POST",
            "url": f"https://discord.com/api/v10/channels/{channel}/messages",
            "authentication": "genericCredentialType", "genericAuthType": "httpHeaderAuth",
            "sendHeaders": True,
            "headerParameters": {"parameters": [{"name": "User-Agent", "value": "DiscordBot (cadam-n8n, 1.0)"}]},
            "sendBody": True, "contentType": "json", "specifyBody": "keypair",
            "bodyParameters": {"parameters": [{"name": "content", "value": text}]},
            "options": {"timeout": 15000},
        },
        credentials={"httpHeaderAuth": cred},
    )
    return node


def ensure_credential(apply: bool) -> dict:
    if CRED_FILE.exists():
        return {"id": CRED_FILE.read_text().strip(), "name": CRED_NAME}
    if not apply:
        return {"id": "<created on --apply>", "name": CRED_NAME}
    token = envfile(BROKER_ENV).get("DISCORD_BOT_TOKEN", "")
    if not token:
        raise SystemExit("Discord bot token not found")
    d = n8n("POST", "/api/v1/credentials", {"name": CRED_NAME, "type": "httpHeaderAuth",
                                           "data": {"name": "Authorization", "value": f"Bot {token}"}})
    CRED_FILE.parent.mkdir(parents=True, exist_ok=True)
    CRED_FILE.write_text(d["id"])
    return {"id": d["id"], "name": CRED_NAME}


def put(w: dict) -> None:
    body = {"name": w["name"], "nodes": w["nodes"], "connections": w["connections"],
            "settings": {k: v for k, v in (w.get("settings") or {}).items() if k in SETTINGS_KEYS}}
    n8n("PUT", f"/api/v1/workflows/{w['id']}", body)


def main() -> int:
    if "--restore" in sys.argv:
        d = Path(sys.argv[sys.argv.index("--restore") + 1])
        for f in sorted(d.glob("wf-*.json")):
            w = json.loads(f.read_text(encoding="utf-8"))
            put(w)
            print("restored", w["name"])
        return 0
    apply = "--apply" in sys.argv
    channel = SEC["DISCORD_SYSTEM_CHANNEL_ID"]
    cred = ensure_credential(apply)
    targets = []
    for w in all_workflows():
        if w["name"].startswith("텔레그램 명령어"):  # chat-command responder, not an alert sender
            continue
        idx = [i for i, n in enumerate(w["nodes"]) if n.get("type") == "n8n-nodes-base.telegram"]
        if idx:
            targets.append((w, idx))
    bdir = BACKUP_ROOT / datetime.now().strftime("%Y%m%d-%H%M%S")
    print(f"{'APPLY' if apply else 'DRY-RUN'}: {len(targets)} workflows with Telegram nodes")
    ok = fail = 0
    for w, idx in targets:
        names = [w["nodes"][i]["name"] for i in idx]
        print(f"- {w['name']} (id={w['id']}, active={w.get('active')}): {len(idx)} nodes {names}")
        for i in idx:
            op = w["nodes"][i].get("parameters", {}).get("operation", "sendMessage")
            if op != "sendMessage":
                print(f"    ! node {w['nodes'][i]['name']} operation={op} (not plain sendMessage)")
        if not apply:
            continue
        try:
            bdir.mkdir(parents=True, exist_ok=True)
            (bdir / f"wf-{w['id']}.json").write_text(json.dumps(w, ensure_ascii=False), encoding="utf-8")
            for i in idx:
                w["nodes"][i] = http_node(w["nodes"][i], channel, cred)
            put(w)
            ok += 1
        except Exception as e:  # noqa: BLE001 — keep going with the other workflows
            fail += 1
            print(f"    FAILED: {e}")
    if apply:
        print(f"done: {ok} updated, {fail} failed. backups: {bdir}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
