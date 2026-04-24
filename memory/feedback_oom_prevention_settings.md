---
name: n8n 수동 실행 OOM 방지 settings
description: 매출시트 2000행 등 큰 input이 있는 워크플로우 수동 실행 시 중간 데이터 저장을 껐음. 메일/GitHub 액션은 정상
type: feedback
originSessionId: 35d08f6a-12fd-40ba-9cd3-904848f3b709
---
**규칙**: 워크플로우 settings에 다음 4개 키 설정.

```
saveExecutionProgress: false
saveManualExecutions: false
saveDataSuccessExecution: 'none'
saveDataErrorExecution: 'all'   ← 에러는 디버깅용 유지
```

**Why**: 2026-04-24 확인 — 차장님이 UI에서 Execute Workflow 눌렀을 때 `서명_생성` 노드에서 "Execution stopped at this node — n8n may have run out of memory" OOM 발생. 노드 자체는 단순 HMAC 계산이지만 수동 실행 시 n8n UI가 모든 중간 데이터(매출시트 2000행, 애드부스트, Conv TSV, 광고그룹 76개 등)를 저장하려고 해서 메모리 소진. n8n cloud 플랜 메모리 한도 내에서 이 파이프라인이 원래 OOM에 걸리기 쉬운 구조(`project_20260421_sales_oom_and_v12_plan.md`의 "OOM 여정" 이력과 일관).

**How to apply**:
- n8n public API PUT으로 한 번에 설정 가능 (`ALLOWED_SETTINGS`에 4개 키 모두 포함됨)
- 이 설정 후 수동 실행은 정상 동작(메일 발송·GitHub Pages 업로드 정상). 단 n8n Executions 목록에 기록 안 남아서 API로 실행 결과 직접 확인 불가 → 메일/리포트 URL로 검증 필요
- 그래도 OOM 나면 대안: (a) 스케줄러 cron을 현재+2분으로 임시 변경 후 자동 트리거(UI 없이 실행) (b) 매출시트_조회 range 축소 (c) 내일 09:00 자동 트리거 기다림
- n8n cloud 플랜 업그레이드하면 근본 해결되지만 비용 증가
