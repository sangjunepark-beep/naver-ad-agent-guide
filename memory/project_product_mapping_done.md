---
name: 상품명 매핑 + 스마트스토어 링크 수정 이력
description: 상품매핑_읽기 enable, 이름조인/데이터_합산 버그 수정, 리포트 링크 추가. 2026-04-18 완료.
type: project
originSessionId: c41dfa35-6a70-4e58-ac21-b97b9aa990fb
---
**상품명 매핑 수정 이력** (2026-04-18)

## 문제 원인
`상품매핑_읽기` 노드가 `disabled: true` + leaf node(출력 연결 없음) 상태.
→ `$('상품매핑_읽기').all()`이 아무 데이터도 반환하지 않아 이름조인·데이터_합산 모두 nad-... ID fallback.

## 수정 내역

| 노드 | 수정 내용 |
|------|----------|
| `상품매핑_읽기` | disabled 제거(활성화) + range A:B → A:C (nvMid 컬럼 포함) |
| `이름조인` | productMap에 nvMid 포함 `{ 상품명, nvMid }`, 출력에 nvMid 컬럼 추가 |
| `데이터_합산` | `adId = r['상품명']` 버그 → `r['상품ID']` 수정. displayName=`r['상품명']` 우선 |
| `리포트_생성` | nvMidMap 구축 + pLink 헬퍼 추가. 이상탐지/AI교차검증 상품명 클릭 링크화 |

## 링크 구조
- URL: `https://smartstore.naver.com/hanasign/products/{nvMid}`
- 스토어 ID: `hanasign` (hanasignmall 아님)
- nvMid 소스: 상품매핑 시트 C열

## 미완료: productNo 불일치
- 현재 C열 nvMid = 네이버 광고 API의 nvMid (쇼핑 카탈로그 ID)
- 스마트스토어 URL의 productNo와 다른 ID 체계
- **해결 방법**: 스마트스토어 파트너센터 → 상품관리 → 엑셀 다운로드 → 상품번호 컬럼을 시트 D열에 추가
- 소스 파일 없이는 정확한 매핑 불가

## 검증 결과 (실행 #145)
- `상품매핑_읽기` executionTime: 1687ms (정상 실행)
- 리포트 내 nad-... 개수: 0 (완전 제거)
- 스마트스토어 링크 수: 18개 (이상탐지 + AI교차검증)

**Why:** 이상탐지·AI교차검증 섹션에서 상품명 대신 nad-... ID가 노출되어 식별 불가했음
**How to apply:** productNo 소스 파일 확보 시 D열 추가 → 코드에서 nvMid 대신 D열 우선 사용
