---
name: 파이프라인 메일 발송 복구 (2026-04-20)
description: Phase 5-3 추가 후 04-18부터 끊겼던 일일 리포트 메일을 n8n 노드 skip 이슈 수정으로 04-20 복구
type: project
originSessionId: bb2cc500-121b-4ea9-8757-74ff04ebb61c
---
**증상 (04-18 ~ 04-20)**
- 메인 파이프라인(UJrNqijTudgU91sX) status=success로 매일 실행되는데 일일 리포트 메일 미수신
- 실행 이력상 전체 61노드 중 40~48노드까지만 실행

**근본 원인: n8n "items=0 자동 skip" 동작 + Phase 5-3 추가가 연쇄로 끊어냄**
1. 1차 끊김 — `실패패턴_조회`(Google Sheets read) 빈 시트 → items=0 → 이후 20노드 전부 skip
2. 2차 끊김 — AI가 "데이터 부재로 검증 불가, 최종판정=[]" 응답 → `제안파싱` items=0 → Reporter/Gmail_발송 skip

**해결 (n8n public API PUT)**
1. `실패패턴_조회` 노드: `alwaysOutputData: true` 설정
2. `제안파싱` 노드: `alwaysOutputData: true` + 코드 끝에 empty 분기 추가
   ```js
   if (result.length === 0) {
     return [{ json: { empty: true, 제안없음: true, 판정사유: "AI 검증 결과 제안 0건" } }];
   }
   ```
3. 04-20 09:47 수동 실행 execution#160 → Gmail 수신 확인 ✅

**n8n API PUT 허용 필드 (재확인)**
- top-level: `name`, `nodes`, `connections`, `settings`, `staticData`만
- `settings` 내부 허용: `saveExecutionProgress`, `saveManualExecutions`, `saveDataErrorExecution`, `saveDataSuccessExecution`, `executionTimeout`, `errorWorkflow`, `timezone`, `executionOrder`
- 그 외 (`binaryMode`, `callerPolicy`, `availableInMCP` 등)는 400 에러 유발
- 워크플로우 GET → 필터링 → PUT 방식으로 수정

**백업 파일**
- `/sessions/festive-awesome-curie/mnt/단순등록자동화/wf_backup_20260420_0939.json` (수정 전 전체 워크플로우)

**Why**: n8n v1 기본 동작상 input items=0이면 다음 노드가 자동 skip. Google Sheets read / IF / Filter / Code 등 모든 하류 노드에 공통 적용. `alwaysOutputData=true` 플래그가 유일한 bypass.

**How to apply**: 이후 파이프라인에 **다운스트림이 있는 Sheets read·조회·LLM 응답 파싱 노드**는 처음부터 `alwaysOutputData=true` 기본 설정 + 빈 결과일 때 placeholder item 리턴하는 분기 코드. Phase 5-3 같은 노드 추가 작업 직후 반드시 E2E 실행 테스트.
