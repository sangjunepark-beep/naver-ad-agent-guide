---
name: 구글 시트 QUERY 날짜 비교 해결 패턴
description: 구글 시트에서 n8n이 쓴 날짜와 QUERY/FILTER 비교 시 타입 불일치 문제 해결법 — TEXT() 변환 후 FILTER → QUERY 패턴
type: feedback
originSessionId: da056e7f-cdbd-47c4-9e66-17f672fb5a10
---
구글 시트에서 QUERY의 WHERE 절로 날짜 비교하면 타입 불일치(텍스트 vs 날짜)로 실패함.
SUMIF는 자동 변환으로 정상 동작하지만, FILTER/QUERY는 엄격 비교라 안 됨.

**Why:** n8n이 시트에 쓰는 날짜가 텍스트인지 날짜 객체인지 일관되지 않음. 구글 시트 QUERY는 엄격 타입 비교.

**How to apply:** 모든 크로스시트 날짜 비교에 아래 패턴 적용:
```
=QUERY(
  FILTER(범위, TEXT(날짜열,"yyyy-mm-dd")=TEXT($B$1,"yyyy-mm-dd")),
  "SELECT ... GROUP BY ... ORDER BY ...",
  0
)
```
FILTER에서 TEXT()로 양쪽 모두 텍스트 변환 → 타입 무관하게 비교 가능.
2026-04-15 확인, H1 테스트셀에서 1398건 매칭 검증 완료.
