---
name: github-deploy
description: "GitHub 리포지토리에 파일을 배포하는 스킬. Cowork에서 만든 HTML, 이미지, CSS 등 모든 파일을 GitHub API로 직접 업로드합니다. git clone/commit/push 없이 API 한 방으로 처리. '깃헙에 올려줘', 'GitHub Pages 배포', '리포에 푸시', 'GitHub에 업로드', '깃헙 배포', '깃에 올려', 'push 해줘', '페이지 업데이트' 등의 요청 시 반드시 이 스킬을 사용하세요."
---

# GitHub Deploy 스킬

Cowork 환경에서 GitHub 리포지토리에 파일을 배포하는 스킬입니다.
git 명령어 대신 GitHub REST API를 사용하므로 인증 문제 없이 한 번에 처리됩니다.

## 왜 이 방식인가

Cowork 샌드박스에서는 git push가 인증 문제로 실패합니다. GitHub API는 토큰만 있으면 파일을 직접 생성/수정할 수 있어서, clone → commit → push 과정이 필요 없습니다.

## 사전 준비

### 설정 파일 확인

배포 전에 반드시 설정 파일을 확인합니다:

```
config 파일 경로: ~/.github-deploy-config.json
```

설정 파일 구조:
```json
{
  "github_token": "ghp_xxxxxxxxxxxxx",
  "default_owner": "sangjunepark-beep",
  "repos": {
    "sign_yellow": {
      "branch": "main",
      "pages_url": "https://sangjunepark-beep.github.io/sign_yellow/"
    }
  }
}
```

설정 파일이 없으면 사용자에게 안내:
1. GitHub PAT가 필요하다고 알려줌
2. PAT 발급 방법 안내 (Settings → Developer settings → Personal access tokens → Tokens classic → repo 권한)
3. 사용자가 토큰을 주면 설정 파일 생성

## 배포 프로세스

### 1단계: 설정 로드

```bash
cat ~/.github-deploy-config.json
```

토큰과 리포 정보를 읽어옵니다.

### 2단계: 대상 확인

사용자에게 확인할 것:
- 어떤 파일을 올릴 것인지 (경로)
- 어떤 리포에 올릴 것인지 (설정에 없는 리포면 추가)
- 리포 내 어떤 경로에 올릴 것인지 (기본: 루트)

### 3단계: 배포 스크립트 실행

`scripts/deploy.py`를 사용합니다:

```bash
python3 /path/to/skill/scripts/deploy.py \
  --config ~/.github-deploy-config.json \
  --repo <repo-name> \
  --files <file1> <file2> ... \
  --dest <destination-path-in-repo> \
  --message "커밋 메시지"
```

### 4단계: 결과 확인

배포 성공 시:
- 커밋 URL 표시
- GitHub Pages URL 표시 (있는 경우)
- "배포 완료. GitHub Pages 반영까지 1~2분 소요됩니다." 안내

배포 실패 시:
- 에러 원인 분석 (토큰 만료, 권한 부족, 파일 크기 초과 등)
- 해결 방법 안내

## 주의사항

- GitHub API 파일 크기 제한: 100MB (base64 인코딩 시 약 75MB 원본)
- 이미지 등 바이너리 파일도 base64로 인코딩하여 업로드 가능
- 한 번에 여러 파일 올릴 때는 파일마다 개별 API 호출 (순차 처리)
- 토큰은 절대 대화에 직접 노출하지 않음

## 리포 추가

새 리포가 필요하면 설정 파일에 추가:
```json
{
  "repos": {
    "new_repo": {
      "branch": "main",
      "pages_url": "https://owner.github.io/new_repo/"
    }
  }
}
```

## 트러블슈팅

| 에러 | 원인 | 해결 |
|------|------|------|
| 401 Unauthorized | 토큰 만료 또는 잘못됨 | PAT 재발급 |
| 404 Not Found | 리포 이름 오류 또는 권한 없음 | 리포명 확인, 토큰에 repo 권한 확인 |
| 409 Conflict | SHA 불일치 (다른 곳에서 수정됨) | 스크립트가 자동으로 최신 SHA 가져와서 재시도 |
| 422 Unprocessable | 파일 경로 잘못됨 | 경로 확인 |
