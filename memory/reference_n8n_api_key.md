---
name: n8n API Key (현재 유효)
description: n8n 공개 API 접근용 JWT 키. 만료일 2026-05-14 기준. 갱신 필요 시 hanasignmall.app.n8n.cloud/settings/api에서 재발급.
type: reference
originSessionId: c41dfa35-6a70-4e58-ac21-b97b9aa990fb
---
**n8n API Key** (2026-04-18 갱신)

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiNmI0ZjJmMi1jMTg0LTQyMGEtOGNmNy1mNDU1MjU0YWI1ZGYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiMTAyOTYxMGYtZjg2ZS00OTczLWI3NmQtMjRlYWU2YmViMjllIiwiaWF0IjoxNzc2NDQ1MzU1LCJleHAiOjE3NzkwMzAwMDB9.oemQkynw9PdXR9kyd6EtaSWqf49RatXwZBcF6I3dq78
```

**용도**: n8n REST API `/api/v1/` 엔드포인트 호출 시 `X-N8N-API-KEY` 헤더로 사용  
**만료**: exp=1779030000 → 약 2026-05-14  
**발급 위치**: hanasignmall.app.n8n.cloud → Settings → n8n API → Create an API Key

**Why**: n8n 워크플로우 JSON import, 노드 수정, 워크플로우 조회/활성화 등 자동화 작업에 필수  
**How to apply**: curl 명령이나 HTTP 요청 시 이 키를 `X-N8N-API-KEY` 헤더에 삽입
