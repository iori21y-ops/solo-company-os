#!/usr/bin/env python3
"""
marketing 에이전트 — 유튜브 발행 스크립트
- YouTube Data API v3 videos.insert (resumable upload)
- 기본 privacyStatus=private (안전). --publish 로 public 공개.
- ⚠️ 유튜브는 API '키'가 아니라 OAuth2 '액세스 토큰'이 필요 (채널 소유권 증명).

자격증명 우선순위:
  1. yt_credentials.json (yt_oauth_setup.py 실행 결과 — 자동 refresh 지원) ← 권장
  2. .env 의 YT_OAUTH_TOKEN + YT_REFRESH_TOKEN (수동 관리)
  최초 발급: python3 yt_oauth_setup.py --secrets /path/to/client_secrets.json

⚠️ 사전 조건:
  videos.insert 는 쿼터 비용이 큼(약 1600 units/건, 일 기본 10,000) → 하루 최대 6건.

사용 (Shorts 숏폼):
  python3 youtube_publish.py --video short.mp4 --title "제목 #Shorts" \\
      --desc-file desc.txt --tags 장기렌트,렌테일러 --shorts
  # 공개: --publish 추가 (없으면 private 업로드)

의존성: pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
"""
import os, sys, argparse

ENV_PATH = os.path.expanduser('~/projects/cadam/cadam-n8n/.env')
# yt_oauth_setup.py 가 저장하는 자격증명 캐시 (scripts/ 디렉터리 기준)
CREDS_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yt_credentials.json')
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


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


def get_credentials():
    """
    자격증명 로드 순서:
      1. yt_credentials.json (InstalledAppFlow 캐시 — 자동 refresh)
      2. .env YT_OAUTH_TOKEN + YT_REFRESH_TOKEN
    """
    try:
        from google.oauth2.credentials import Credentials
        import google.auth.transport.requests
    except ImportError:
        print('❌ 의존성 미설치')
        print('   pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2')
        sys.exit(2)

    # 1순위: yt_credentials.json
    if os.path.exists(CREDS_CACHE):
        creds = Credentials.from_authorized_user_file(CREDS_CACHE, SCOPES)
        if creds.expired and creds.refresh_token:
            print('🔄 액세스 토큰 만료 → 리프레시 중...')
            request = google.auth.transport.requests.Request()
            creds.refresh(request)
            # 갱신된 토큰 캐시에 저장
            with open(CREDS_CACHE, 'w') as f:
                f.write(creds.to_json())
            print('   ✅ 토큰 갱신 완료')
        if creds.valid:
            print(f'🔑 자격증명 로드: {CREDS_CACHE}')
            return creds
        else:
            print(f'⚠️  yt_credentials.json 유효하지 않음 — .env 폴백 시도')

    # 2순위: .env
    env = load_env()
    access_token = env.get('YT_OAUTH_TOKEN', '')
    refresh_token = env.get('YT_REFRESH_TOKEN', '')

    if not access_token and not refresh_token:
        print('❌ 유튜브 발행 불가 — 자격증명 없음')
        print()
        print('   [해결 방법] 최초 OAuth 발급:')
        print('   1. Google Cloud Console에서 client_secrets.json 다운로드')
        print('   2. python3 yt_oauth_setup.py --secrets /path/to/client_secrets.json')
        print()
        print('   상세 절차: PUBLISH-SOP.md §1-B 또는 sop-yt-oauth-provisioning.md 참조')
        sys.exit(2)

    creds = Credentials(
        token=access_token or None,
        refresh_token=refresh_token or None,
        token_uri='https://oauth2.googleapis.com/token',
    )

    # refresh_token 있으면 갱신 시도
    if creds.expired and creds.refresh_token:
        print('🔄 .env 토큰 만료 → 리프레시 중...')
        request = google.auth.transport.requests.Request()
        creds.refresh(request)
        # 갱신된 토큰 .env 업데이트
        _update_env('YT_OAUTH_TOKEN', creds.token)
        print('   ✅ 토큰 갱신 완료 (.env 업데이트됨)')

    if not creds.valid and not creds.token:
        print('❌ 유효한 액세스 토큰 없음 — yt_oauth_setup.py 를 다시 실행하세요.')
        sys.exit(2)

    print('🔑 자격증명 로드: .env (YT_OAUTH_TOKEN)')
    return creds


def _update_env(key, value):
    lines = []
    found = False
    try:
        with open(ENV_PATH, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        pass
    new_lines = []
    for line in lines:
        if line.strip().startswith(f'{key}='):
            new_lines.append(f'{key}={value}\n')
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f'\n{key}={value}\n')
    with open(ENV_PATH, 'w') as f:
        f.writelines(new_lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--video', required=True, help='업로드할 영상 파일 (mp4)')
    p.add_argument('--title', required=True)
    p.add_argument('--desc-file', help='설명 텍스트 파일')
    p.add_argument('--tags', default='', help='쉼표구분 태그')
    p.add_argument('--category', default='2', help='카테고리 ID (2=Autos & Vehicles)')
    p.add_argument('--shorts', action='store_true', help='Shorts 표시(설명/제목에 #Shorts 권장)')
    p.add_argument('--publish', action='store_true', help='public 공개 (없으면 private)')
    args = p.parse_args()

    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload
    except ImportError:
        print('❌ 의존성 미설치 — google-api-python-client 필요')
        print('   pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2')
        sys.exit(2)

    vid = os.path.expanduser(args.video)
    if not os.path.exists(vid):
        print(f'❌ 영상 파일 없음: {vid}'); sys.exit(1)

    creds = get_credentials()
    yt = build('youtube', 'v3', credentials=creds)

    desc = ''
    if args.desc_file:
        with open(os.path.expanduser(args.desc_file), encoding='utf-8') as f:
            desc = f.read()
    if args.shorts and '#Shorts' not in desc and '#shorts' not in desc.lower():
        desc = (desc + '\n\n#Shorts').strip()

    privacy = 'public' if args.publish else 'private'
    print(f'📤 유튜브 업로드 시도 — privacyStatus: {privacy}')
    body = {
        'snippet': {
            'title': args.title,
            'description': desc,
            'tags': [t.strip() for t in args.tags.split(',') if t.strip()],
            'categoryId': args.category,
        },
        'status': {'privacyStatus': privacy, 'selfDeclaredMadeForKids': False},
    }
    media = MediaFileUpload(vid, chunksize=-1, resumable=True)
    req = yt.videos().insert(part='snippet,status', body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f'   업로드 {int(status.progress() * 100)}%')
    vid_id = resp['id']
    print('✅ 유튜브 업로드 성공')
    print(f'   영상 ID: {vid_id}')
    print(f'   링크: https://youtu.be/{vid_id}  (상태: {privacy})')
    if not args.publish:
        print('🟡 private 업로드 완료 — YouTube Studio에서 검토 후 --publish 로 공개하세요.')


if __name__ == '__main__':
    main()
