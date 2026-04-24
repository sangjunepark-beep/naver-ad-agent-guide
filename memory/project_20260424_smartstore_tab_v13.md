---
name: 스마트스토어 탭 v13 재설계 (3스토어 분리)
description: 리포트_생성 노드 스마트스토어 탭 HTML 템플릿+데이터 로직 전면 교체. 하나사인몰/더바른사인/로켓출력공장 3섹션 분리, 전환 상품 전체 노출, 매출 순 정렬, 비전환 광고비 TOP 10 감사용
type: project
originSessionId: 35d08f6a-12fd-40ba-9cd3-904848f3b709
---
**사실**: 2026-04-24 PUT (KST 17:12) — 리포트_생성 노드 jsCode 55,798자 → 62,304자 확장. 3곳 치환:

1. **데이터 계산 로직 추가** (PRODUCT_ROWS 정의 직전):
   - 이름조인에서 `상품ID → 캠페인` 매핑 구축 (`prodCmpMap`)
   - `classifyStore(cmp)` 함수: includes('로켓'/'더바른'/'하나몰') 3분류
   - `storeAgg.HANA/BARUN/ROCKET` 버킷에 광고비·노출·클릭·전환건·매출·products 집계
   - `renderStoreProducts(products, type)`: type='conv'면 전환 상품 전체 매출 순, type='cost'면 비전환 광고비 TOP 10
   - 6개 placeholder 생성: `PRODUCT_ROWS_{HANA|BARUN|ROCKET}_{CONV|COST}`
   - 3개 KPI 블록: `KPI_STORE_{HANA|BARUN|ROCKET}` (광고비/노출/클릭/전환/매출/ROAS 6카드)
   - `BARUN_ALERT`: 더바른사인 전환 0건+광고비>0이면 경고 배너

2. **HTML 템플릿 스마트스토어 탭 교체**:
   - 기존: KPI_AD/KPI_DIRECT/KPI_ADVOOST/KPI_STORE_TOTAL 4카드 블록 + PRODUCT_ROWS 테이블 TOP 20 + CAMPAIGN_ROWS 테이블
   - 신규: 통합 KPI_STORE_TOTAL → 3스토어 섹션(각 KPI 6카드 + 전환 상품 테이블 + 광고비 TOP 10 테이블) → ADVoost 유지
   - 스토어별 좌측 색상 바: 하나사인몰 파랑(#3b82f6), 더바른사인 주황(#f59e0b), 로켓출력공장 보라(#a855f7)
   - ROAS 색상: 300%+ 녹색, 100~300% 파랑, 1~99% 주황, 0 회색

3. **치환 map에 placeholder 10개 추가**:
   - KPI_STORE_HANA, KPI_STORE_BARUN, KPI_STORE_ROCKET
   - PRODUCT_ROWS_HANA_CONV, PRODUCT_ROWS_HANA_COST
   - PRODUCT_ROWS_BARUN_CONV, PRODUCT_ROWS_BARUN_COST
   - PRODUCT_ROWS_ROCKET_CONV, PRODUCT_ROWS_ROCKET_COST
   - BARUN_ALERT

**04-23 기준 예상 결과** (내일 검증):
- 🏠 하나사인몰: 광고비 568k / 전환 9건 / 매출 988k / **ROAS 174%**
- ⚠️ 더바른사인: 광고비 40k / 전환 0건 / 매출 0원 / **ROAS 0%** + 경고 배너
- 🚀 로켓출력공장: 광고비 103k / 전환 4건 / 매출 99k / **ROAS 96.5%**

**Why**: 기존 리포트가 PRODUCT_ROWS TOP 20을 광고비 순으로만 노출해서 (1) 매출 상품이 다 안 보임 (2) 3스토어가 뒤섞여 개별 성과 판단 불가 (3) 전환 0건 스토어(더바른사인)가 묻힘. 차장님 지적으로 재설계.

**How to apply**:
- 내일 09:00 자동 스케줄 실행 시 자동 적용. 또는 지금 수동 실행(OOM 방지 settings 적용됨)
- GitHub Pages URL: `https://sangjunepark-beep.github.io/hanasignmall-ad-reports/reports/2026-04-23.html` (Ctrl+Shift+R 새로고침)
- `classifyStore` 함수는 캠페인명 텍스트 매칭이라 향후 새 캠페인에 '하나몰'/'더바른'/'로켓' 키워드 없이 등록 시 '기타'로 빠짐 — 신규 캠페인 명명 규칙 유지 필요
- 검증 실패 시 롤백 지점: 이전 jsCode 백업은 exec 히스토리에 없고(saveManualExecutions=false), 이 메모에 명시된 OLD 블록 3개를 역치환하면 복구 가능

**주의·재발 방지**:
- 리포트_생성 코드는 62KB로 매우 큼. 수정 시 치환 블록 엄격히 일치해야 함 (공백·줄바꿈 포함)
- 새 placeholder 추가 시 반드시 치환 map(라인 49238 부근)에도 등록해야 `{{X}}` 그대로 리포트에 노출되는 사고 방지
- HTML 내 CSS 클래스 `tag normal/watch/cs-check`는 기존 스타일 재사용 — 리포트 style 섹션 수정 시 영향
