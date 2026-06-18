#!/usr/bin/env python3
"""읽기 전용 Supabase 조회. SELECT/WITH만 허용. 쓰기·다중문 차단."""
import os, sys, json, subprocess, re
from pathlib import Path

def _load_env():
    envp = Path.home()/'projects/cadam/cadam-n8n/.env'
    if envp.exists():
        for ln in envp.read_text().splitlines():
            ln=ln.strip()
            if ln and not ln.startswith('#') and '=' in ln:
                k,v=ln.split('=',1); os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
_load_env()

FORBIDDEN = ('INSERT','UPDATE','DELETE','DROP','ALTER','TRUNCATE','GRANT','CREATE','REPLACE','MERGE','COPY')

def _guard(sql):
    # 주석 제거
    s = re.sub(r'--.*', '', sql)
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S).strip()
    # 세미콜론으로 statement 분리 → 각 조각 검사 (다중문 DROP 차단)
    stmts = [x.strip() for x in s.split(';') if x.strip()]
    if not stmts:
        sys.exit("거부: 빈 쿼리")
    for st in stmts:
        head = st.split(None,1)[0].upper() if st.split() else ''
        if head not in ('SELECT','WITH'):
            sys.exit(f"거부: SELECT/WITH로 시작해야 함 (받음: {head})")
        up = st.upper()
        for f in FORBIDDEN:
            if re.search(r'\b'+f+r'\b', up):
                sys.exit(f"거부: 금지 키워드 {f}")
    return s

def query(sql, limit=50):
    safe = _guard(sql)
    ref = os.environ['SUPABASE_PROJECT_REF']
    tok = os.environ['SUPABASE_ACCESS_TOKEN']
    url = f"https://api.supabase.com/v1/projects/{ref}/database/query"
    r = subprocess.run(['curl','-s','-X','POST',url,
        '-H',f'Authorization: Bearer {tok}',
        '-H','Content-Type: application/json',
        '-d',json.dumps({'query':safe})], capture_output=True, text=True)
    try:
        rows = json.loads(r.stdout)
    except Exception:
        print(r.stdout[:500]); return
    if isinstance(rows, list):
        for row in rows[:limit]:
            print(json.dumps(row, ensure_ascii=False))
        if len(rows) > limit:
            print(f"... ({len(rows)}행 중 {limit}행만 표시)")
    else:
        print(json.dumps(rows, ensure_ascii=False))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('사용법: python3 query.py "SELECT ..."')
    query(sys.argv[1])
