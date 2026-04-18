---
name: 상품명 매핑 + 스마트스토어 링크 수정 이력
description: 상품매핑 D열 full URL 완성(2208개). pLink 코드 D열 직접 사용으로 최종 완료. 2026-04-19.
type: project
originSessionId: c41dfa35-6a70-4e58-ac21-b97b9aa990fb
---
**상품명 매핑 수정 이력** (2026-04-18~19 최종완료)

## 최종 상태 (완료)

상품매핑 시트 D열에 스마트스토어 full URL 2208개 입력 완료.
pLink 헬퍼가 D열 URL을 직접 사용하도록 수정 완료.
테스트 이메일(jimrn22@gmail.com) INBOX 도착 확인.

## 수정 이력 요약

| 단계 | 수정 내용 |
|------|----------|
| 1차 (04-18) | `상품매핑_읽기` 활성화 + range A:D, pLink 코드 추가 |
| 2차 (04-18) | nvMid 기반 URL → "상품이 존재하지 않습니다" 확인 → 근본 원인: nvMid ≠ smartstore productNo |
| 3차 (04-18~19) | 스마트스토어 판매자센터 CSV 2개 업로드 → JOIN → D열 full URL 직접 저장 |

## 구글 시트 D열 현황
- 스프레드시트 ID: `1Yuw_8we4nEzL1nslHI66LHBBE_uWc-ErALzhn2vvLGI`
- 시트: 상품매핑 (gid=1248602534)
- 범위: D2:D2209 (총 2208개)
  - hanasign: `https://smartstore.naver.com/hanasign/products/{ss번호}` — 1899개
  - thecorrectsign: `https://smartstore.naver.com/thecorrectsign/products/{ss번호}` — 238개
  - 빈값: 71개 (CSV에 없는 상품)

## pLink 최종 코드 (`리포트_생성` 노드)
```javascript
const pUrlMap = {};
try {
  for (const item of $('상품매핑_읽기').all()) {
    const m = item.json;
    const adId = m['adId'] || m['소재ID'] || '';
    const nm = m['상품명'] || '';
    const pUrl = m['스마트스토어이상품번호'] || '';  // D열 = full URL
    if (pUrl) {
      if (adId) pUrlMap[adId] = pUrl;
      if (nm) pUrlMap[nm] = pUrl;
    }
  }
} catch(e) {}
const pLink = (name, id) => {
  const url = pUrlMap[id] || pUrlMap[name] || '';
  if (!url) return name;
  return '<a href="' + url + '" target="_blank" style="color:#1e40af;text-decoration:none;font-weight:700">' + name + '</a>';
};
```

## 임시 워크플로우 (정리 필요)
- `XquBGKrgVVWVUTyN` (D열 업데이트용) — 삭제 예정
- `1RFPrHhg7cpchpxg` (테스트 이메일 발송용) — 삭제 예정

**Why:** nvMid(광고API 카탈로그ID)와 스마트스토어 productNo가 다른 ID 체계 → CSV JOIN으로 해결
**How to apply:** D열이 full URL이므로 pLink에서 바로 사용. nvMid 관련 코드 제거 가능
