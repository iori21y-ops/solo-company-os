#!/usr/bin/env python3
"""Read-only export of the production Supabase public tables (the Rentailor site DB) over the REST API.

Why REST and not pg_dump (2026-11-13): the temporary CLI login roles cannot read locked-down tables such as
public.consultations, while the site's service-role key can. Only GET requests are made.

Output: <out_dir>/<table>.jsonl.gz (one JSON row per line) + openapi.json (columns/types/primary keys)
        + summary.json (row counts). Exit code 0 only when every table exported.
Usage:  supabase_rest_export.py <out_dir>    (reads SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY from env)
"""
import gzip, json, os, sys, time, urllib.parse, urllib.request

URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
PAGE = 1000


def get(path, extra=None):
    h = {"apikey": KEY, "Authorization": "Bearer " + KEY, "User-Agent": "solo-backup", "Accept": "application/json"}
    h.update(extra or {})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(URL + path, headers=h), timeout=120) as r:
                return r.read(), dict(r.headers)
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == 4:
                raise RuntimeError(f"HTTP {e.code} {path[:80]}: {e.read()[:200]!r}")
        except Exception:
            if attempt == 4:
                raise
        time.sleep(3 * (attempt + 1))


def main():
    out = sys.argv[1]
    if not URL or not KEY:
        sys.exit("missing SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY")
    os.makedirs(out, exist_ok=True)
    spec_raw, _ = get("/rest/v1/", {"Accept": "application/openapi+json"})
    open(os.path.join(out, "openapi.json"), "wb").write(spec_raw)
    spec = json.loads(spec_raw)
    defs = spec.get("definitions", {})
    summary, failed = {}, []
    for table in sorted(defs):
        props = defs[table].get("properties", {})
        pks = [c for c, p in props.items() if "<pk/>" in (p.get("description") or "")]
        order = ",".join(pks) if pks else (next(iter(props)) if props else "")
        n, offset = 0, 0
        path = os.path.join(out, table + ".jsonl.gz")
        try:
            with gzip.open(path + ".partial", "wt", encoding="utf-8") as f:
                while True:
                    q = {"select": "*", "limit": PAGE, "offset": offset}
                    if order:
                        q["order"] = order
                    body, _ = get(f"/rest/v1/{urllib.parse.quote(table)}?" + urllib.parse.urlencode(q))
                    rows = json.loads(body)
                    for r in rows:
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
                    n += len(rows)
                    if len(rows) < PAGE:
                        break
                    offset += PAGE
            os.replace(path + ".partial", path)
            summary[table] = n
        except Exception as e:
            failed.append(table)
            summary[table] = f"FAILED: {e}"[:300]
            try:
                os.remove(path + ".partial")
            except OSError:
                pass
    json.dump({"tables": summary, "failed": failed, "at": time.strftime("%F %T")},
              open(os.path.join(out, "summary.json"), "w"), ensure_ascii=False, indent=1)
    rows = sum(v for v in summary.values() if isinstance(v, int))
    print(f"tables={len(summary) - len(failed)} rows={rows} failed={len(failed)}")
    if failed:
        print("failed: " + ", ".join(failed), file=sys.stderr)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
