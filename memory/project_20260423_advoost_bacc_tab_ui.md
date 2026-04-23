---
name: 2026-04-23 ADVoost + B계정 + 탭 UI 통합 작업
description: 04-22~23 애드부스트 연동·B계정 자격증명 등록·리포트 탭 UI 3개·Strategist 입찰가 절대값 강화. 다음 세션 이어갈 포인트 목록 포함
type: project
originSessionId: 3caa48ca-de84-4e34-83b7-086d140a6d43
---
## 세션 범위
2026-04-22 저녁 ~ 04-23 오전 KST. v12-17 ~ v12-22 패치 적용.

## 완료

### 1. ADVoost 애드부스트 전체 구축 (완결)
- **시트 탭 신설**: 메인시트(`1Yuw_8we4nEzL1nslHI66LHBBE_uWc-ErALzhn2vvLGI`)에 `애드부스트_일별` 탭. 헤더 10컬럼: `수집일/채널/노출/클릭/비용/전환수/매출/ROAS/원본파일/등록시각`
- **수집 루틴**: 사용자가 `/mnt/단순등록자동화/애드부스트/` 에 result.csv 투입 → Cowork가 파싱 → 시트 append → `/처리완료/YYYY-MM-DD_result.csv`로 이동
- **n8n 신규 노드**: `애드부스트_조회` (httpRequest, batchGet `애드부스트_일별!A1:J1000`, executeOnce, cred id `HjfwX5DgD4iXkptZ`)
- **위치**: `매출시트_조회` → `애드부스트_조회` → `채널별_집계` (직렬 삽입)
- **채널별_집계**: `$('애드부스트_조회').all()` 파싱 → advBy[수집일] 맵 → `ADVoost_비용_T, ADVoost_매출_T, ADVoost_노출_T, ADVoost_클릭_T, ADVoost_전환수_T, ADVoost_ROAS_T, ADVoost_비용_Tm1, ADVoost_매출_Tm1` 필드 신설

### 2. 04-21/22 실데이터 시트 기록 (검증용)
| 날짜 | 노출 | 클릭 | 비용 | 전환 | 매출(역산) | ROAS |
|---|---|---|---|---|---|---|
| 2026-04-21 | 13,136 | 44 | 50,303원 | 3 | 350,361원 | 696.5% |
| 2026-04-22 | 8,072 | 47 | 46,321원 | 4 | 1,388,851원 | 2,998.3% |

매출은 CSV의 "총 광고수익률(%)" 컬럼으로 역산 (매출 = 비용 × ROAS / 100, 상품별 합산).

### 3. 리포트 UI 3탭 재구성 (v12-19 ~ v12-20)
- 탭: **📊 요약 / 🛍️ 스마트스토어 / 🌐 자사몰**
- 순수 HTML+CSS+JS (GitHub Pages 전용. 이메일은 요약본 별도)
- Hero 영역: 금액 중심(`광고비 775,925원 → 매출 2,084,951원`) + ROAS는 보조 1줄 (v12-20)
- 본문 폰트 일괄 +20% (11→13, 12→14, 13→16, 14→17, 15→18, 16→19, 17→20, 18→22, 19→23, 20→24)
- 자사몰 탭 내부: `🏠 하나사인몰.com` (파워링크 4개·쇼핑검색 2개·브랜드검색 1개) + `🆕 하나사인몰.kr` (파워링크 1·쇼핑검색 1) 분리 placeholder

### 4. 이메일 요약(reportHtml) 재디자인 (v12-19)
- 제목: "하나사인몰 네이버 광고 통합 보고서"
- Hero: table 기반 레이아웃 (이메일 호환) — 광고비·기여매출 금액 + ROAS 보조
- 3카드: 쇼핑검색 / ADVoost / 통합
- Subject: `[하나사인몰] {날짜} 네이버 광고 통합 보고서 · 통합 ROAS {tot}%`

### 5. Strategist 프롬프트 입찰가 절대값 강화 (v12-22)
- 상품ID → 현재 입찰가 맵을 프롬프트 직전 주입 (`HTTP_adgroups` + `이름조인`에서 계산)
- 프롬프트에 "각 상품 현재 입찰가 (반드시 참고)" 섹션 자동 생성
- 출력 스키마 강제: `"현재_입찰가": 380, "변경후_입찰가": 290` (숫자, 10원 단위, 최소 70원)
- `"조치": "입찰가 380원 → 290원 (-23.7%)"` 형식 예시 명시
- 리포트 KEY_KO 매핑: `현재_입찰가` → "현재 입찰가", `변경후_입찰가` → "👉 변경할 입찰가"

### 6. 요약/스마트스토어 광고비 불일치 해결 (v12-21)
- 문제: 요약 탭은 통합(775k), 스마트스토어 탭은 쇼핑검색만(729k) → 46k 차이가 ADVoost
- 수정:
  - `AD_COST, AD_ROAS`를 `tot_비용`, `tot_ROAS.toFixed(1)`로 교체 → 요약 헤드라인 통합값
  - 스마트스토어 탭에 `🎯 ADVoost 쇼핑 성과` 5카드 + `🛍️ 스마트스토어 유입 전체 합계` 3카드 추가
  - 이제 요약 Hero의 광고비 = 스마트스토어 탭 최하단 합계 **동일**

### 7. B 계정(1558945) 기반 준비 (부분완료)
- API Key/Secret/Customer_id **n8n 변수_설정에 영구 저장** (`naver_api_key_2 / naver_secret_key_2 / naver_customer_id_2`)
- **메모리에는 평문 저장 금지 원칙 유지** (세션 종료 후 키 로테이션 권장)
- B 계정 구성 확인: 9개 캠페인
  - WEB_SITE 파워링크 5개 (001 파워링크 일예산 27만, 002 신규몰 10만, 주력상품 2만, 주말 2만, 서브상품 정지)
  - SHOPPING 쇼핑검색 3개 (검색광고 70원, 신규몰 검색상품노출 5만, 요일제 8만)
  - BRAND_SEARCH 1개 (하나사인몰 브랜드 정지)
- 광고그룹 76개 (bidAmt 전수 존재)
- **n8n 노드 11개 복제 완료** (_B 접미사): 서명_생성_stats_POST_B, StatReport_생성요청_B, 30초_대기_B, 서명_생성_status_GET_B, StatReport_상태확인_B, 상태확인_분기_B, 서명_생성_download_GET_B, TSV_다운로드_B, TSV_파싱_B, 서명_생성_adgroups_GET_B, HTTP_adgroups_B
- credential 참조 `naver_api_key` → `naver_api_key_2` 정규식 치환 완료

## 미완료 (다음 세션 시작점)

### 우선순위 A — B 계정 실데이터 수집 경로 연결
1. **스케쥴러에서 B 계정 분기 시작점 연결** — 기존 `스케쥴러 → 서명_생성_stats_POST`(A)와 **병렬**로 `스케쥴러 → 서명_생성_stats_POST_B` 추가
2. **`시트_저장_Phase2_B` 노드 신규** — A의 시트_저장_Phase2 구조 복제, 탭 이름 `01B_일일수집로그`로 변경. `HTTP_adgroups_B` → `시트_저장_Phase2_B` 연결
3. **`01B_일일수집로그` 시트 탭 생성** — A와 동일 컬럼 구조. `계정` 필드 필요 시 추가
4. **채널별_집계 B 계정 파싱 추가** — 새 노드 `자사몰_조회` 또는 기존 `시트_저장_Phase2_B` 출력 참조 → `자사몰_파워링크_비용_T / _매출_T`, `자사몰_쇼핑검색_비용_T / _매출_T` 등 필드 신설
5. **자사몰 탭 실데이터 렌더** — 현재 placeholder 대체. .com/.kr 그룹별 KPI 3카드 + 캠페인별 실적 테이블

### 우선순위 B — Conv 경로도 복제 (전환/매출 집계)
A 계정의 `서명_생성_conv_POST → Conv_TSV_다운로드 → Conv_TSV_파싱 → 시트_저장_Conv` 경로를 B 계정용으로 동일 복제. Conv 없이 B 계정 매출 집계 불가 (비용/노출/클릭만 나옴).

### 우선순위 C — 메인 스케줄 09:30 이동 + Cowork 자동화
- n8n `스케쥴러` 노드의 trigger 시각 00:00 → 09:30 이동 (이메일 발송 시각도 함께 조정)
- Cowork `mcp__scheduled-tasks__create_scheduled_task` 등록: 매일 오전 09:00에 애드부스트 폴더 스캔 → `result.csv` 있으면 파싱 → n8n webhook POST → 처리완료 이동
- 관련 webhook 워크플로우 `ADVoost_수집` 상시 등록 (Webhook → Google Sheets Append → 200 응답)

### 우선순위 D — UI 추가 개선 (사용자 피드백 "보기 어려움" 구체화 대기)
후보:
- 요약 탭 세션 축약 (항목 많음)
- 스마트스토어 탭 KPI 섹션 3개 → 2개 병합
- AI 4단계 카드 본문 요약 강화
- 채널별 ROAS 3카드 중복 제거 (요약+스토어 탭 중 하나만)
- 추가 폰트 확대

### 우선순위 E — 메인 파이프라인 날짜 불일치 조사
- 04-23 KST 08:19 실행됐는데 subject가 "04-21(화요일)"로 나옴 (어제 = 04-22여야)
- stat report API 요청의 date 필드 로직 확인 필요 (D-1? D-2?)
- 스크린샷에 보이는 04-22.html 리포트는 내용상 04-22자 데이터로 보이지만 subject 꼬임

## 환경 현황 스냅샷 (2026-04-23 09:50 KST 기준)

| 항목 | 값 |
|---|---|
| n8n 워크플로우 ID | `UJrNqijTudgU91sX` |
| 워크플로우 이름 | 네이버 검색광고 에이전트_파이프라인 |
| 메인 시트 ID | `1Yuw_8we4nEzL1nslHI66LHBBE_uWc-ErALzhn2vvLGI` |
| 매출시트 ID (업체계약현황) | `169BTstGNSOPxx0aKglV2sTb_zhZWEfW1KTcht-K3afA` |
| Sheets OAuth2 credential id | `HjfwX5DgD4iXkptZ` |
| GitHub Pages 리포 | `sangjunepark-beep/hanasignmall-ad-reports` |
| 리포트 URL 패턴 | `.../reports/YYYY-MM-DD.html` |
| ADVoost 폴더 (사용자 PC) | `C:\Users\Administrator\Documents\Claude\Projects\단순등록자동화\애드부스트\` |
| ADVoost 폴더 (Cowork 마운트) | `/mnt/단순등록자동화/애드부스트/` |
| 처리완료 파일 규칙 | `/처리완료/YYYY-MM-DD_result.csv` + zip |
| 메인 스케줄 트리거 | 현재 새벽 00:00 (09:30으로 이동 예정) |

## 주의·재발 방지

1. **PUT 전 반드시 최신 GET** — 이번 세션 v12-18 복구 PUT 후 B노드 복제 PUT이 덮어써서 KPI_CHANNEL_ROAS가 원복된 사고 있음. 덮어쓸 가능성 있는 변경은 같은 로컬 wf_json 기반으로 누적 적용 후 1번에 PUT.
2. **B 계정 API 키 세션 노출됨** — 세션 종료 후 `searchad.naver.com → 고객센터 → API 접근 관리`에서 재발급 + n8n `변수_설정`의 `naver_api_key_2 / naver_secret_key_2` 갱신.
3. **브라우저 캐시** — GitHub Pages 리포트는 반영 후에도 브라우저에 캐시. 캐시 우회: URL 끝에 `?v=아무값` 또는 Ctrl+Shift+R. 사용자 피드백 "그대론데"가 여러 번 캐시였음.
4. **매출 역산 방식** — ADVoost CSV엔 매출 절대값 컬럼이 없어 "총 광고수익률(%)"에서 역산. 상품별 합산 = 전체 매출. 네이버 공식 집계라 값 자체는 정확.

**Why**: 세션 분량이 긴 작업이라 다음 세션에서 맥락 손실 방지 목적. 이 메모만 읽으면 바로 이어갈 수 있도록 현 상태·미완·주의사항 모두 명시.

**How to apply**: 다음 세션 시작 시 이 파일부터 읽고 "우선순위 A"부터 진행. B 계정 실데이터 수집 완성 → 자사몰 탭 실데이터 렌더가 가장 큰 다음 덩어리.
