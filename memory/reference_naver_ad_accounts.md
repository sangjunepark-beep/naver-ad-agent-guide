---
name: 네이버 검색광고 계정 2개 (A/B)
description: A계정=스마트스토어 쇼핑검색, B계정=자사몰 파워링크+쇼핑+브랜드. 자격증명은 n8n 변수_설정에만 저장, 메모리 평문 저장 금지
type: reference
---

## A 계정 — 스마트스토어 (기본)
- CUSTOMER_ID: `1872088`
- 로그인 ID: hana1644 / hanasign7523
- 광고 상품: 쇼핑검색광고 (SHOPPING) 12개 캠페인
- 랜딩: smartstore.naver.com/hanasign
- n8n 변수: `naver_api_key / naver_secret_key / naver_customer_id`
- 관련 노드: 서명_생성_*, StatReport_*, HTTP Request(campaigns), HTTP_adgroups, TSV_파싱, 이름조인, 시트_저장_Phase2, 시트_저장_Conv

## B 계정 — 자사몰 (2026-04-22 추가)
- CUSTOMER_ID: `1558945`
- 광고 상품: 
  - WEB_SITE (파워링크) 5개 — 001 파워링크(27만), 002 신규몰(10만), 주력상품(2만), 주말(2만), 서브상품(정지)
  - SHOPPING (쇼핑검색) 3개 — 검색광고(70원), 신규몰 검색상품노출(5만), 요일제(8만)
  - BRAND_SEARCH 1개 — 하나사인몰 브랜드(정지)
- 광고그룹 76개, bidAmt 전수 존재
- 랜딩: hanasignmall.com (메인 자사몰) + hanasignmall.kr (신규몰)
- pcChannelId: `bsn-a001-00-000000001656390` (자사몰.com/kr) + `bsn-a001-00-000000013122478` (SHOPPING 3개)
- n8n 변수: `naver_api_key_2 / naver_secret_key_2 / naver_customer_id_2`
- 관련 노드: *_B 접미사 11개 (서명_생성_stats_POST_B 등) — 복제만 완료, 시작점/끝점 미연결

## ADVoost 쇼핑 (A계정 계정 아래 디스플레이 광고)
- 네이버 광고주센터 (ad.naver.com 계열) → 디스플레이 광고 → ADVoost 쇼핑
- 공식 API 없음. CSV 수동 다운로드 + 구글시트 기록 방식
- 시트: 메인 시트 내 `애드부스트_일별` 탭 (A~J 10컬럼)

## 보안 정책
- 모든 API 키는 n8n `변수_설정` 노드에만 저장
- 메모리(.md) 파일에 평문 저장 금지
- 세션 종료 시 키 노출 가능성 있으면 재발급 + n8n 갱신
- 재발급 경로: searchad.naver.com → 도구 → API 관리 → 새 Access License/Secret 발급

**Why**: 계정 2개 구조를 한 곳에 요약. 다음 세션에서 B 계정 수집 경로 연결할 때 참조. 자격증명은 여기 안 적고 n8n에만.

**How to apply**: 파이프라인 신규 작업 시 A/B 구분 먼저 확인. B 계정 관련 코드는 `_B` 접미사 규칙 유지.
