---
name: Phase 5-1/5-2 사후 ROAS 자동 측정 + 효과판정 고도화 완료
description: KvCkk3M3sNcegLgU — 사후 ROAS 측정 + 변경 전 비교 상대판정 적용 완료
type: project
---
**Phase 5-1 사후 ROAS 자동 측정 완료** (2026-04-18)
워크플로우 KvCkk3M3sNcegLgU 활성화. 매일 10:00. 첫 측정 2026-04-21 이후.

**Phase 5-2 효과판정 고도화 완료** (2026-04-18)
노드 구성: 측정대상_필터 → 서명_생성_stats → 네이버_통계_조회(post) → 서명_생성_pre → 네이버_통계_pre(pre) → ROAS계산_효과판정 → 실행로그_사후ROAS_업데이트

판정 로직:
- postCost < 1000 → '데이터부족'
- preCost < 1000 → 절대값 기준 (>=200%:호전 / >=100%:유지 / 미만:악화)
- 양쪽 모두 충분 → 상대비교 (ratio=post/pre, >=1.2:성공 / >=0.9:중립 / 미만:실패)

05_실행로그 업데이트 컬럼: 사후ROAS, 효과, 메모(변경전ROAS:X% / 변경후ROAS:Y% 형식)
preStartDate/preEndDate: 실행일 -3일 ~ -1일

**Why**: 절대 ROAS만으로는 계절·상품 특성 무시 → 변경 전 대비 상대적 판정으로 신뢰도 향상
**How to apply**: Phase 5-3(실패학습) 착수 시 '실패' 레코드를 패턴 분석 소스로 활용
