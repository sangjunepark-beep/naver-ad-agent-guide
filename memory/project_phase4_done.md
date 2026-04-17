---
name: Phase 4 승인→자동반영 — E2E 완결 (2026-04-18)
description: 04-18 E2E 전체 파이프라인 완결 확인. Webhook→토큰검증→네이버 API 변경→05_실행로그 A열 정상 기록까지 검증 완료.
type: project
originSessionId: f32d44fe-befa-41f0-a807-485c5ff003ef
---
**Phase 4 승인→자동반영 — E2E 완결 (2026-04-18)**

## 검증된 것 (✅)
- 소재 `nad-a001-02-000000284215314` 입찰가 반복 변경 성공 (2900→2470→2350→2230→2120)
- Webhook → 파라미터검증 → 네이버 API PUT → 05_실행로그 Append 전 구간 정상
- 05_실행로그 Row 7에 A~K 11개 컬럼 정상 기록 확인 (2026-04-18)
- n8n REST API (PUT /api/v1/workflows/{id}) 로 노드 설정 프로그래밍 저장 성공

## 핵심 수정 내용 (04-18)
- **실행로그_기록 노드 문제**: `matchingColumns`에 타이틀 "05. 실행 로그..." 캐싱, `schema` 1개 컬럼만 인식
- **수정 방법**: n8n REST API PUT으로 `matchingColumns=[]`, `schema` 11개 컬럼, `headerRow=3` 저장
- **시트 구조**: Row1=타이틀(L1에 잔여 '메모'), Row2=빈 행, Row3=실제 헤더, Row4~=데이터. gviz는 빈 Row2 스킵하므로 gviz Row2 = 실제 시트 Row3
- **n8n Autosave 우회**: UI 저장 반복 실패 → API Key 발급 → PUT으로 직접 저장

## 미완 항목 (🟡)
- 05_실행로그 Row1 L1='메모' 잔여 (사용자 수동 삭제 필요, 기능 영향 없음)
- 롤백 경로 미구현
- 가드레일 미구현 (일일 건수·변경폭 상한)
- 중복 승인 방지 미검증
- E2E 파이프라인 상시 스케줄 가동 미확인

## n8n API 활용 (중요)
- n8n API Key: Settings → n8n API에서 발급
- PUT /api/v1/workflows/{id} payload: `{name, nodes, connections, settings(executionOrder만), staticData}`
- `binaryMode` 등 추가 settings 키는 400 에러 → filtered_settings로 허용 키만 추출 필요

## 파일
1. `단순등록자동화/Phase4_승인_자동반영.json` — Webhook 워크플로우 (16노드)
2. `단순등록자동화/네이버_검색광고_에이전트_Phase4_완성본.json` — 메인 파이프라인
3. `네이버검색광고 에이전트 빌드/Phase4_후속점검_보고서.md` — 04-17 검증 원자료
4. `네이버검색광고 에이전트 빌드/런북_파이프라인_재가동.md` — 재가동·재검증 절차 SOP

## How to apply
- n8n 노드 수정은 UI보다 REST API PUT이 안정적. API Key 보관 필요.
- 시트 headerRow는 gviz 기준이 아닌 실제 시트 행 번호 사용 (gviz가 빈 행 스킵함)
- Phase 5 착수 전 메인 파이프라인 스케줄 재가동 선행 필수
