---
name: 01_일일수집로그 시트 구조 변경 (04-15)
description: 01 시트에서 J~M열(전환수/전환율/매출/ROAS) 삭제. 현재 A~K 11열 구조. 대시보드 QUERY Col 번호에 영향.
type: project
originSessionId: da056e7f-cdbd-47c4-9e66-17f672fb5a10
---
2026-04-15 변경: 01_일일수집로그에서 J~M열 삭제 (전환수/전환율/매출/ROAS — AD 리포트에 없어 항상 0이었음)

**현재 구조 (A~K, 11열):**
A=수집일, B=채널, C=캠페인, D=광고그룹, E=상품명, F=노출, G=클릭, H=CTR, I=비용, J=평균노출순위, K=상품명(매핑)

**Why:** AD 리포트에 전환/매출 데이터가 없어서 항상 0 표시. 혼란 방지를 위해 삭제.

**How to apply:**
- 03_대시보드 QUERY 수식은 A3:I 범위 사용 (Col9=비용이 마지막)
- QUERY Col 번호: Col3=캠페인, Col5=상품명, Col6=노출, Col7=클릭, Col9=비용
- n8n 시트_저장_Phase2 노드 매핑 컬럼도 확인 필요 (J~M열 삭제 영향 없는지)
