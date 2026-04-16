---
name: 네이버 쇼핑검색광고 API PUT 요구사항
description: 쇼핑검색광고(SHOPPING_PRODUCT_AD) 입찰가 변경 시 주의사항 모음 (2026-04-16 Phase4 구축 중 확인)
type: project
---

네이버 쇼핑검색광고(SHOPPING_PRODUCT_AD) 소재 입찰가를 PUT으로 변경할 때의 요구사항.

**Why:** Phase 4 승인→자동반영 파이프라인 구축 중 연속 에러를 거치며 확인한 실제 API 동작. 네이버 공식 문서에 명확히 기재 안 된 부분이 많음.

**How to apply:** 향후 입찰가 변경/광고 수정 자동화 만들 때 아래 체크.

## 엔드포인트
- 판단 단위가 소재(nad-)면 `/ncc/ads/{id}` 사용 (adgroup 아님)
- PUT 시 쿼리 `?fields=adAttr` 필수
- GET 응답에서 bidAmt는 루트가 아니라 `adAttr.bidAmt` 경로

## PUT body 필수 필드
```json
{
  "nccAdId": "nad-xxx",
  "type": "SHOPPING_PRODUCT_AD",
  "adAttr": { "bidAmt": 2270, "useGroupBidAmt": false }
}
```
- `type` 없으면 "Invalid ad type"
- `nccAdId` 누락해도 "Invalid request"

## bidAmt 제약
- **10원 단위**만 허용. 아니면 "remainder of division is not zero (xxx / 10), at '/bidAmt' with 'multipleOf'"
- 최소 70원
- 계산 후 `Math.round(raw / 10) * 10` 처리 필수

## 서명
- HMAC-SHA256(message = `timestamp.METHOD.uri`)
- uri는 쿼리스트링 제외 (`/ncc/ads/{id}`만, `?fields=...` 빼고)
