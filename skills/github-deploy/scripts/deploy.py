#!/usr/bin/env python3
"""
GitHub Deploy Script
Cowork 환경에서 GitHub API를 통해 파일을 리포지토리에 직접 배포합니다.
git clone/commit/push 없이 REST API로 처리.
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


def load_config(config_path):
    """설정 파일 로드"""
    config_path = os.path.expanduser(config_path)
    if not os.path.exists(config_path):
        print(f"ERROR: 설정 파일이 없습니다: {config_path}")
        print("설정 파일을 먼저 생성해주세요.")
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def github_api(method, url, token, data=None):
    """GitHub API 호출"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
    }

    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            error_json = json.loads(error_body)
            error_msg = error_json.get('message', error_body)
        except json.JSONDecodeError:
            error_msg = error_body
        print(f"ERROR: GitHub API {e.code} - {error_msg}")
        if e.code == 401:
            print("→ 토큰이 만료되었거나 잘못되었습니다. PAT를 재발급하세요.")
        elif e.code == 404:
            print("→ 리포지토리를 찾을 수 없습니다. 이름과 권한을 확인하세요.")
        elif e.code == 409:
            print("→ 충돌 발생. SHA가 변경되었을 수 있습니다. 재시도합니다.")
            return {'error': 'conflict', 'code': 409}
        elif e.code == 422:
            print(f"→ 처리할 수 없는 요청: {error_msg}")
        return {'error': error_msg, 'code': e.code}


def get_file_sha(owner, repo, path, branch, token):
    """기존 파일의 SHA 가져오기 (업데이트 시 필요)"""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    result = github_api('GET', url, token)
    if result and 'sha' in result:
        return result['sha']
    return None


def is_binary_file(file_path):
    """바이너리 파일 여부 판단"""
    binary_extensions = {
        '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.svg',
        '.webp', '.pdf', '.zip', '.tar', '.gz', '.mp4', '.mp3',
        '.woff', '.woff2', '.ttf', '.eot', '.otf'
    }
    return Path(file_path).suffix.lower() in binary_extensions


def read_and_encode(file_path):
    """파일 읽고 base64 인코딩"""
    with open(file_path, 'rb') as f:
        content = f.read()
    return base64.b64encode(content).decode('utf-8')


def deploy_file(owner, repo, local_path, repo_path, branch, token, message):
    """단일 파일 배포"""
    print(f"  배포 중: {os.path.basename(local_path)} → {repo_path}")

    # base64 인코딩
    content_b64 = read_and_encode(local_path)

    # 기존 파일 SHA 확인 (업데이트인 경우)
    sha = get_file_sha(owner, repo, repo_path, branch, token)

    # API 요청 데이터
    data = {
        'message': message,
        'content': content_b64,
        'branch': branch,
    }
    if sha:
        data['sha'] = sha
        action = "업데이트"
    else:
        action = "신규 생성"

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{repo_path}"
    result = github_api('PUT', url, token, data)

    if result and 'content' in result:
        commit_url = result.get('commit', {}).get('html_url', 'N/A')
        print(f"  ✓ {action} 완료: {repo_path}")
        print(f"    커밋: {commit_url}")
        return True
    elif result and result.get('error') == 'conflict':
        # SHA 충돌 시 재시도
        print("  → SHA 충돌, 최신 SHA로 재시도...")
        sha = get_file_sha(owner, repo, repo_path, branch, token)
        if sha:
            data['sha'] = sha
            result = github_api('PUT', url, token, data)
            if result and 'content' in result:
                print(f"  ✓ {action} 완료 (재시도 성공)")
                return True

    print(f"  ✗ 실패: {repo_path}")
    return False


def main():
    parser = argparse.ArgumentParser(description='GitHub에 파일 배포')
    parser.add_argument('--config', default='~/.github-deploy-config.json',
                        help='설정 파일 경로')
    parser.add_argument('--repo', required=True,
                        help='대상 리포지토리 이름')
    parser.add_argument('--owner', default=None,
                        help='리포 소유자 (설정 파일의 default_owner 사용)')
    parser.add_argument('--files', nargs='+', required=True,
                        help='배포할 파일 경로(들)')
    parser.add_argument('--dest', default='',
                        help='리포 내 대상 경로 (기본: 루트)')
    parser.add_argument('--rename', default=None,
                        help='리포에 올릴 때 파일명 변경 (예: index.html). 단일 파일일 때만 사용')
    parser.add_argument('--message', default='Update files via Cowork deploy',
                        help='커밋 메시지')
    parser.add_argument('--branch', default=None,
                        help='대상 브랜치 (설정 파일 우선)')

    args = parser.parse_args()

    # 설정 로드
    config = load_config(args.config)
    token = config.get('github_token')
    if not token:
        print("ERROR: 설정 파일에 github_token이 없습니다.")
        sys.exit(1)

    owner = args.owner or config.get('default_owner')
    if not owner:
        print("ERROR: 리포 소유자를 지정해주세요. (--owner 또는 설정 파일의 default_owner)")
        sys.exit(1)

    # 리포 설정
    repo_config = config.get('repos', {}).get(args.repo, {})
    branch = args.branch or repo_config.get('branch', 'main')
    pages_url = repo_config.get('pages_url', '')

    print(f"========================================")
    print(f"  GitHub Deploy")
    print(f"  리포: {owner}/{args.repo}")
    print(f"  브랜치: {branch}")
    print(f"  파일 수: {len(args.files)}")
    print(f"========================================\n")

    # 파일 배포
    success_count = 0
    fail_count = 0

    for file_path in args.files:
        if not os.path.exists(file_path):
            print(f"  ✗ 파일 없음: {file_path}")
            fail_count += 1
            continue

        # 리포 내 경로 결정
        if args.rename and len(args.files) == 1:
            filename = args.rename
        else:
            filename = os.path.basename(file_path)
        if args.dest:
            repo_path = f"{args.dest.strip('/')}/{filename}"
        else:
            repo_path = filename

        if deploy_file(owner, args.repo, file_path, repo_path, branch, token, args.message):
            success_count += 1
        else:
            fail_count += 1

    print(f"\n========================================")
    print(f"  결과: 성공 {success_count} / 실패 {fail_count}")
    if pages_url:
        print(f"  Pages: {pages_url}")
        print(f"  (반영까지 1~2분 소요)")
    print(f"========================================")

    # 결과를 JSON으로도 출력 (스킬에서 파싱용)
    result = {
        'success': fail_count == 0,
        'deployed': success_count,
        'failed': fail_count,
        'pages_url': pages_url,
        'repo': f"{owner}/{args.repo}",
        'branch': branch
    }
    print(f"\n__RESULT_JSON__:{json.dumps(result)}")


if __name__ == '__main__':
    main()
