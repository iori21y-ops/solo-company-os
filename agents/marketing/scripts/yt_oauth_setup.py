#!/usr/bin/env python3
"""
유튜브 OAuth 2.0 최초 발급 헬퍼 스크립트
──────────────────────────────────────────
사용 전 준비:
  1. Google Cloud Console에서 client_secrets.json 다운로드
  2. 이 스크립트와 같은 디렉터리에 client_secrets.json 배치
  3. pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client

실행:
  python3 yt_oauth_setup.py
  # 또는 client_secrets.json 경로 직접 지정:
  python3 yt_oauth_setup.py --secrets /path/to/client_secrets.json

결과:
  - 브라우저에서 Google 계정 인증 (1회)
  - YT_OAUTH_TOKEN, YT_REFRESH_TOKEN 출력
  - yt_credentials.json 저장 (재인증 없이 재사용)
  - .env 자동 등록 여부 확인 후 등록
"""
import os
import sys
import json
import argparse

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
ENV_PATH = os.path.expanduser('~/projects/cadam/cadam-n8n/.env')
CREDS_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yt_credentials.json')
DEFAULT_SECRETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client_secrets.json')


def check_deps():
    missing = []
    for pkg in ['google.oauth2.credentials', 'google_auth_oauthlib.flow', 'googleapiclient.discovery']:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg.split('.')[0].replace('_', '-'))
    if missing:
        deps = ' '.join(set(missing))
        print(f'❌ 필수 패키지 없음: {deps}')
        print(f'   pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2')
        sys.exit(1)


def run_oauth_flow(secrets_file):
    from google_auth_oauthlib.flow import InstalledAppFlow
    print(f'\n📋 client_secrets.json 경로: {secrets_file}')
    print('🌐 브라우저가 열립니다 — CADAM 유튜브 채널 Google 계정으로 로그인하세요.\n')
    flow = InstalledAppFlow.from_client_secrets_file(secrets_file, SCOPES)
    creds = flow.run_local_server(port=0, open_browser=True)
    return creds


def verify_token(creds):
    """업로드 스코프 보유 여부 확인 (실제 API 호출 없이 토큰 정보만 확인)"""
    from googleapiclient.discovery import build
    import google.auth.transport.requests
    # 토큰 갱신 시도
    request = google.auth.transport.requests.Request()
    if creds.expired and creds.refresh_token:
        creds.refresh(request)
    return creds.valid


def update_env(key, value):
    """기존 .env 파일에서 키를 업데이트하거나 추가"""
    lines = []
    found = False
    try:
        with open(ENV_PATH, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        pass

    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(f'{key}=') or stripped.startswith(f'{key} ='):
            new_lines.append(f'{key}={value}\n')
            found = True
        else:
            new_lines.append(line)

    if not found:
        new_lines.append(f'\n{key}={value}\n')

    with open(ENV_PATH, 'w') as f:
        f.writelines(new_lines)


def main():
    p = argparse.ArgumentParser(description='YouTube OAuth 2.0 최초 발급 헬퍼')
    p.add_argument('--secrets', default=DEFAULT_SECRETS,
                   help=f'client_secrets.json 경로 (기본: {DEFAULT_SECRETS})')
    p.add_argument('--no-env', action='store_true', help='.env 자동 등록 건너뜀')
    args = p.parse_args()

    print('=' * 60)
    print('  유튜브 OAuth 2.0 토큰 발급 헬퍼')
    print('=' * 60)

    # 의존성 확인
    check_deps()

    # 이미 캐시된 자격증명이 있으면 재사용 제안
    if os.path.exists(CREDS_CACHE):
        print(f'\n⚠️  기존 자격증명 파일 발견: {CREDS_CACHE}')
        ans = input('   재사용하시겠습니까? (y=재사용, n=새로 발급): ').strip().lower()
        if ans == 'y':
            from google.oauth2.credentials import Credentials
            import google.auth.transport.requests
            creds = Credentials.from_authorized_user_file(CREDS_CACHE, SCOPES)
            if creds.expired and creds.refresh_token:
                print('   🔄 토큰 갱신 중...')
                request = google.auth.transport.requests.Request()
                creds.refresh(request)
                print('   ✅ 갱신 완료')
        else:
            if not os.path.exists(args.secrets):
                print(f'\n❌ client_secrets.json 없음: {args.secrets}')
                print('   Google Cloud Console → OAuth 클라이언트 ID → JSON 다운로드 후 배치하세요.')
                sys.exit(1)
            creds = run_oauth_flow(args.secrets)
    else:
        if not os.path.exists(args.secrets):
            print(f'\n❌ client_secrets.json 없음: {args.secrets}')
            print('\n[준비 방법]')
            print('  1. https://console.cloud.google.com/ 접속')
            print('  2. 프로젝트 선택 (또는 새 프로젝트 생성: cadam-marketing)')
            print('  3. API 및 서비스 → YouTube Data API v3 활성화')
            print('  4. 사용자 인증 정보 → OAuth 2.0 클라이언트 ID 만들기')
            print('     앱 유형: 데스크톱 앱, 이름: cadam-marketing-agent')
            print('  5. JSON 다운로드 → 이 디렉터리에 client_secrets.json 으로 저장')
            print(f'     저장 경로: {args.secrets}')
            sys.exit(1)
        creds = run_oauth_flow(args.secrets)

    # 자격증명 캐시 저장
    with open(CREDS_CACHE, 'w') as f:
        f.write(creds.to_json())
    print(f'\n✅ 자격증명 캐시 저장: {CREDS_CACHE}')

    # 토큰 출력
    print('\n' + '─' * 60)
    print('  발급된 토큰 정보')
    print('─' * 60)
    access_token = creds.token or ''
    refresh_token = creds.refresh_token or ''
    print(f'  YT_OAUTH_TOKEN   = {access_token[:20]}...{access_token[-10:] if len(access_token) > 30 else ""}')
    print(f'  YT_REFRESH_TOKEN = {refresh_token[:20]}...{refresh_token[-10:] if len(refresh_token) > 30 else ""}')

    if refresh_token:
        print('\n  ℹ️  YT_REFRESH_TOKEN 보관 권장 — 액세스 토큰(1시간) 만료 시 자동 갱신에 사용됩니다.')

    # .env 등록
    if not args.no_env:
        print(f'\n📝 .env 파일 자동 등록: {ENV_PATH}')
        ans = input('   진행하시겠습니까? (y/n): ').strip().lower()
        if ans == 'y':
            if access_token:
                update_env('YT_OAUTH_TOKEN', access_token)
            if refresh_token:
                update_env('YT_REFRESH_TOKEN', refresh_token)
            print('   ✅ .env 등록 완료')
            print('   → youtube_publish.py 를 실행해 private 업로드 테스트를 진행하세요.')
        else:
            print('\n   수동 등록 방법:')
            print(f'   echo "YT_OAUTH_TOKEN={access_token}" >> {ENV_PATH}')
            if refresh_token:
                print(f'   echo "YT_REFRESH_TOKEN={refresh_token}" >> {ENV_PATH}')
    else:
        print(f'\n   수동 등록:')
        print(f'   YT_OAUTH_TOKEN={access_token}')
        if refresh_token:
            print(f'   YT_REFRESH_TOKEN={refresh_token}')

    print('\n' + '=' * 60)
    print('  다음 단계: private 업로드 테스트')
    print('  python3 youtube_publish.py --video test.mp4 --title "테스트 #Shorts" --shorts')
    print('  (--publish 없이 실행 → YouTube Studio에서 private 영상 확인)')
    print('=' * 60)


if __name__ == '__main__':
    main()
