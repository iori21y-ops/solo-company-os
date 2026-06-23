#!/usr/bin/env python3
"""
marketing 에이전트 — 인스타그램 발행 스크립트 (스캐폴드 / MVP)
- Instagram Graph API(콘텐츠 게시) 2단계 플로우: ① 미디어 컨테이너 생성 → ② 게시
- .env(cadam-n8n)에서 인증 재사용 (키 미발급 시 명확히 안내하고 중단 = 안전)
- 기본은 '컨테이너만 생성'(=draft 등가). --publish 플래그가 있어야 실제 공개.

⚠️ 사전 조건 (자격증명 미발급 상태 = 현재):
  .env 에 아래 키가 있어야 동작 — 없으면 친절히 안내하고 종료.
    IG_USER_ID         (인스타 비즈니스 계정 ID, 페이스북 페이지 연결 필수)
    META_ACCESS_TOKEN  (장기 토큰, instagram_content_publish 권한 / 앱 심사 필요)
  미디어(이미지/영상)는 '공개 URL'에 먼저 호스팅돼 있어야 함 (API가 URL을 fetch).
  카드뉴스(이미지 캐러셀)·Reels(숏폼 영상) 모두 지원.

사용 (이미지 1장):
  python3 ig_publish.py --image-url https://.../card.jpg --caption-file cap.txt
사용 (Reels 숏폼 영상):
  python3 ig_publish.py --video-url https://.../short.mp4 --reels --caption-file cap.txt --publish
사용 (캐러셀 = 이미지 여러 장):
  python3 ig_publish.py --image-url url1 --image-url url2 --carousel --caption-file cap.txt
"""
import os, sys, json, time, argparse, urllib.parse, urllib.request, urllib.error

ENV_PATH = os.path.expanduser('~/projects/cadam/cadam-n8n/.env')
GRAPH = 'https://graph.facebook.com/v21.0'
REQUIRED = ['IG_USER_ID', 'META_ACCESS_TOKEN']


def load_env():
    env = {}
    try:
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip()
    except FileNotFoundError:
        pass
    return env


def require_creds(env):
    missing = [k for k in REQUIRED if not env.get(k)]
    if missing:
        print('❌ 인스타 발행 불가 — 자격증명 미발급')
        print(f'   누락 키: {", ".join(missing)}')
        print('   → PUBLISH-SOP.md "프로비저닝 체크리스트(인스타)" 절차로 발급 후 .env 등록.')
        print('   (Meta 앱 + instagram_content_publish 권한 심사 필요 — 수일~수주 소요)')
        sys.exit(2)


def _post(path, params):
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(f'{GRAPH}/{path}', data=data, method='POST')
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def _get(path, params):
    qs = urllib.parse.urlencode(params)
    req = urllib.request.Request(f'{GRAPH}/{path}?{qs}', method='GET')
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def wait_ready(ig_user, creation_id, token, tries=20):
    """영상은 처리에 시간이 걸림 → status_code=FINISHED 까지 대기."""
    for _ in range(tries):
        st = _get(f'{creation_id}', {'fields': 'status_code', 'access_token': token})
        code = st.get('status_code')
        if code == 'FINISHED':
            return True
        if code == 'ERROR':
            print('❌ 미디어 처리 실패(ERROR)')
            sys.exit(1)
        time.sleep(5)
    return False


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--image-url', action='append', default=[], help='공개 이미지 URL (캐러셀이면 여러 번)')
    p.add_argument('--video-url', help='공개 영상 URL (Reels)')
    p.add_argument('--reels', action='store_true', help='영상을 Reels로 게시')
    p.add_argument('--carousel', action='store_true', help='이미지 여러 장을 캐러셀로')
    p.add_argument('--caption-file', help='캡션 텍스트 파일 경로')
    p.add_argument('--publish', action='store_true', help='실제 공개 (없으면 컨테이너만 생성=draft 등가)')
    args = p.parse_args()

    env = load_env()
    require_creds(env)
    ig_user = env['IG_USER_ID']
    token = env['META_ACCESS_TOKEN']

    caption = ''
    if args.caption_file:
        with open(os.path.expanduser(args.caption_file), encoding='utf-8') as f:
            caption = f.read()

    try:
        # ① 컨테이너 생성
        if args.video_url and args.reels:
            print('📤 Reels 컨테이너 생성…')
            c = _post(f'{ig_user}/media', {
                'media_type': 'REELS', 'video_url': args.video_url,
                'caption': caption, 'access_token': token})
            creation_id = c['id']
            print('   영상 처리 대기…')
            if not wait_ready(ig_user, creation_id, token):
                print('❌ 영상 처리 시간 초과'); sys.exit(1)
        elif args.carousel and len(args.image_url) > 1:
            print(f'📤 캐러셀 컨테이너 생성 ({len(args.image_url)}장)…')
            children = []
            for u in args.image_url:
                ch = _post(f'{ig_user}/media', {
                    'image_url': u, 'is_carousel_item': 'true', 'access_token': token})
                children.append(ch['id'])
            c = _post(f'{ig_user}/media', {
                'media_type': 'CAROUSEL', 'children': ','.join(children),
                'caption': caption, 'access_token': token})
            creation_id = c['id']
        else:
            if not args.image_url:
                print('❌ --image-url 또는 --video-url 필요'); sys.exit(1)
            print('📤 단일 이미지 컨테이너 생성…')
            c = _post(f'{ig_user}/media', {
                'image_url': args.image_url[0], 'caption': caption, 'access_token': token})
            creation_id = c['id']

        print(f'   컨테이너 ID: {creation_id}')

        # ② 게시 (--publish 일 때만)
        if not args.publish:
            print('🟡 컨테이너만 생성 완료 (draft 등가). 실제 공개하려면 --publish 추가.')
            print(f'   게시 시: media_publish(creation_id={creation_id})')
            return
        res = _post(f'{ig_user}/media_publish', {
            'creation_id': creation_id, 'access_token': token})
        print('✅ 인스타 게시 성공')
        print(f'   미디어 ID: {res.get("id")}')
    except urllib.error.HTTPError as e:
        print(f'❌ 발행 실패 — HTTP {e.code}')
        print(f'   {e.read().decode()[:500]}')
        sys.exit(1)


if __name__ == '__main__':
    main()
