#!/usr/bin/env python3
"""
marketing 에이전트 발행 스크립트 (MVP)
- WP REST API로 글 1편 발행
- .env(cadam-n8n)에서 인증 재사용
- 기본 draft 상태 발행 (안전), --publish 플래그로 즉시 공개
사용:
  python3 wp_publish.py --title "제목" --file 본문.md
  python3 wp_publish.py --title "제목" --file 본문.md --publish
"""
import os, sys, base64, json, argparse, urllib.request, urllib.error

ENV_PATH = os.path.expanduser('~/projects/cadam/cadam-n8n/.env')

def load_env():
    env = {}
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    return env

def publish(title, content, status):
    env = load_env()
    url = env['WP_URL'].rstrip('/')
    user = env['WP_USER']
    pw = env['WP_APP_PASSWORD'].replace(' ', '')
    token = base64.b64encode(f"{user}:{pw}".encode()).decode()

    payload = json.dumps({
        "title": title,
        "content": content,
        "status": status,   # 'draft' or 'publish'
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{url}/wp-json/wp/v2/posts",
        data=payload,
        headers={
            "Authorization": f"Basic {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
            print("✅ 발행 성공")
            print(f"   글 ID: {data.get('id')}")
            print(f"   상태: {data.get('status')}")
            print(f"   링크: {data.get('link')}")
            print(f"   수정화면: {url}/wp-admin/post.php?post={data.get('id')}&action=edit")
            return data
    except urllib.error.HTTPError as e:
        print(f"❌ 발행 실패 — HTTP {e.code}")
        print(f"   {e.read().decode()[:400]}")
        sys.exit(1)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--title', required=True)
    p.add_argument('--file', required=True, help='본문 파일 경로 (md/html/txt)')
    p.add_argument('--publish', action='store_true', help='즉시 공개 (없으면 draft)')
    args = p.parse_args()

    with open(os.path.expanduser(args.file), encoding='utf-8') as f:
        content = f.read()

    status = 'publish' if args.publish else 'draft'
    print(f"📤 발행 시도 — 상태: {status}")
    publish(args.title, content, status)
