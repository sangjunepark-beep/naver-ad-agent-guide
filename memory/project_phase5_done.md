---
name: Phase 5-1 사후 ROAS 자동 측정 완료
description: Phase5 워크플로우 n8n 저장 및 활성화 완료. 매일 10:00 자동 실행.
type: project
originSessionId: c41dfa35-6a70-4e58-ac21-b97b9aa990fb
---
Phase5_사후ROAS_자동측정 워크플로우 완료. 2026-04-18 기준.

**워크플로우 ID**: KvCkk3M3sNcegLgU
**상태**: Active (매일 10:00 자동 실행)

**흐름**: Schedule Trigger(10:00) → 변수_설정 → 실행로그_전체읽기(05_실행로그) → 측정대상_필터 → 대상_있는지_확인 → Loop → 서명_생성_stats → 네이버_통계_조회 → ROAS계산_효과판정 → 실행로그_사후ROAS_업데이트 → 완료_로그

**필터 조건**: 실행결과=성공 + 사후ROAS 공란 + 실행일시 3일 이상 경과 + nccAdId 유효

**효과 판정 기준**: ROAS≥300%=호전, ≥150%=개선, ≥100%=유지, <100%=악화, 비용=0=데이터없음

**측정 기간**: 실행일 다음날 ~ 실행일+3일 (3일간 누적)

**첫 실제 측정 대상 예상**: 2026-04-21 이후 (Phase4 실행 3일 경과 후)

**Why**: Phase 4에서 입찰가 변경을 실행했는데, 변경 효과를 사후 추적해서 향후 제안 품질을 개선하기 위함.

**How to apply**: Phase 5-2(효과 판정 개선), Phase 5-3(실패 학습 루프) 구축 시 이 워크플로우 결과 데이터를 활용.

**n8n API Key**: 주요 트러블슈팅 - Google Sheets sheetName은 mode:"name" + value:"05_실행로그" 형식 사용 (mode:"url"은 activate 불가)
