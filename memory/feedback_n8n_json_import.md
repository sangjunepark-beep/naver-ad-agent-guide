---
name: n8n 워크플로우 수정은 JSON import 방식
description: n8n 노드 추가/수정 시 브라우저 조작 대신 JSON export→수정→import 방식 사용. 04-15 확정.
type: feedback
originSessionId: ad23d44c-b418-4515-bcba-21264d1c7351
---
n8n 워크플로우 수정은 **브라우저 조작(Computer Use) 사용 금지**, JSON import 방식으로 진행.

**Why:** 브라우저 조작이 매우 느리고(노드 1개 추가에 5~10분), 막히면 사용자 응답 대기 필요해서 야간/무인 작업 불가. Phase 3 노드 15개를 JSON으로 생성해서 한 번에 import하니 30분 만에 완료됨.

**How to apply:**
- 워크플로우 수정 요청 시: 사용자에게 n8n에서 JSON export 요청 → Claude가 Python으로 JSON 수정 → 사용자가 기존 워크플로우 삭제 후 새 JSON import
- 노드 위치 정리, Sticky Note 추가 등도 JSON으로 처리
- 브라우저 조작은 credential 연결, Activate 토글 등 JSON으로 안 되는 것만 사용
