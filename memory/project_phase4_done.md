---
name: Phase 4 승인→자동반영 파이프라인 완성
description: 04-16 Phase 4 Webhook + 메인 파이프라인 import/테스트 완료. 실제 입찰가 변경 성공 확인.
type: project
---

**Phase 4 승인→자동반영 — 완성 (2026-04-16)**

**최종 동작 확인:**
- 소재 nad-a001-02-000000284215314 입찰가 2900원 → 2470원 (−15%) 변경 성공
- 승인 완료 화면 정상 출력
- 시트 기록까지 전 흐름 검증 완료

**파일:**
1. `단순등록자동화/Phase4_승인_자동반영.json` — Webhook 워크플로우 (16노드, 로그_데이터_준비 추가됨)
2. `단순등록자동화/네이버_검색광고_에이전트_Phase4_완성본.json` — 메인 파이프라인 (승인링크 포함)

**퍼블리시 이력:**
- v1~v5: 디버깅 중 버전
- v6~v9: adAttr 경로, type 필드, 10원 단위 반올림 등 순차 수정
- 최종 동작 버전은 v9 계열

**Why:** 이메일 리포트의 '사람 승인 필요' 항목에 버튼 삽입 → 클릭 시 Webhook 호출 → 자동 입찰가 변경까지 완결.

**How to apply:**
- 향후 다른 업종/광고주 확장 시 `project_naver_shopping_ad_api_quirks.md` 참조
- `실행로그_기록` 노드 Mapping Column Mode는 JSON import 때마다 Manually로 리셋되는 이슈 있음 → 재import 시 Map Automatically 다시 설정
- 남은 일: Phase 5(사후 ROAS/효과 기록), 프로젝트 전체 종결 정리
