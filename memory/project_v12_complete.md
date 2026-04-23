---
name: v12 리포트 재정비 완결 (v12-1~v12-22) — 4-21 → 4-23
description: v12-1~22 총 22개 패치. 요일버그·딥링크·한글화·입찰가배지 + ADVoost 연동·탭 UI·금액중심 Hero·입찰가 절대값 제안까지. 상세 4-23 작업은 project_20260423_advoost_bacc_tab_ui.md
type: project
originSessionId: eb681c62-81c8-4f8f-a28b-ccc2714cd691
---
## 2026-04-21 v12 작업 전체 요약

n8n 워크플로우 `UJrNqijTudgU91sX` (네이버 검색광고 에이전트_파이프라인) 리포트 시스템 전면 재정비. 총 9개 패치 적용 + 수차례 GET 전 PUT 실수 복구 + sheet tab 이름 오판 복구.

## 패치 계보

| 패치 | 내용 | 핵심 변경 |
|---|---|---|
| v12-1 | Verifier_L1 fallback 제거 | `$input.all()` 직접 사용. try-catch로 `rows=[]` 나던 문제 해결 |
| v12-2 | 리포트_생성 하드코딩 제거 | 359,167 / 24 / +4.6% / +2건 / -1.1% 샘플 HTML 블록 4줄 삭제 |
| v12-1.5 | Analyst_프롬프트 upstream 수정 | `$('Verifier_L1').first().json` 사용 (이상치로그_기록 로그행 대신) |
| v12-3 | 영업섹션 코드 정상 확인 | 실제 데이터 들어오면 자연 해소 |
| v12-5 | AI max_tokens + 프롬프트 제한 | Analyst 2000→8000, 나머지 2000→4000, "심각도 상 최대 15개" 지시 추가 |
| v12-6 | AI 4단계 JSON 파싱 렌더 | ```json``` 코드 블록 대신 자연어 소견 + "▼ 상세 N건" 접힌 카드 |
| v12-7 | 상품별 실적 TOP 20 + pLink | 2208개 스마트스토어 URL pUrlMap 활용. 관찰 카드·상품명 클릭 → 스토어 이동 |
| v12-8 | 매출시트 OOM 해결 | googleSheets 노드 → **httpRequest + Sheets API batchGet** (`executeOnce: true` 필수) |
| v12-9 | 용어 한글화 + 액션 버튼 | COST-NO-CONV → "광고비만 나가고 매출 0" 등. 버튼 2종: 스토어 / 광고그룹 딥링크 |
| v12-10 | 요일 표기 버그 수정 (04-21 14:20) | `fmtDateKo` + Overview `dow` 두 곳. `T12:00:00Z` + `getUTCDay()`로 서버 타임존(UTC) 영향 제거 |
| v12-11 | 광고그룹 딥링크 캠페인 무시 버그 (04-21 14:45) | grpMap[광고그룹명] 이름키 → grpByProd[상품ID] 상품ID키. 이름조인 return에 `캠페인ID`/`광고그룹ID` 필드 보존 추가. 동일 이름 광고그룹이 서로 다른 캠페인에 있는 케이스(예: "게시판" 3개 ID 분산) 정상 처리 |
| v12-17 | ADVoost 시트 연동 (04-22) | 애드부스트_일별 탭 신설, 애드부스트_조회 노드, 채널별_집계 ADVoost 필드 8개 추가. 매출 역산(비용×ROAS/100) |
| v12-18 | 리포트 KPI_CHANNEL_ROAS 3카드 (04-22) | 쇼핑검색/ADVoost/통합 ROAS. B계정 노드 복제 때 덮어씀 사고 → 복구 PUT |
| v12-19 | 리포트 탭 UI 3개 + 이메일 재디자인 (04-22 밤) | 요약/스마트스토어/자사몰 탭. 이메일은 table 기반 Hero |
| v12-20 | Hero 금액 중심 재구성 + 본문 폰트 +20% (04-23) | "주객전도"(ROAS 64px) 해결. 40px 광고비/매출 + 작은 ROAS 보조 |
| v12-21 | 요약/스마트스토어 광고비 일치 (04-23) | AD_COST/AD_ROAS를 tot_*로. 스마트스토어 탭에 ADVoost 5카드 + 유입전체 3카드 |
| v12-22 | Strategist 입찰가 절대값 제안 (04-23) | 프롬프트에 상품별 현재 입찰가 주입. 스키마 강제: "현재_입찰가" "변경후_입찰가" 필드. 10원 단위·70원 최소 |

## v12-11 광고그룹 딥링크 캠페인 무시 버그 핵심 (재발 방지)

**증상**: 리포트의 📊 광고그룹 "XXX" 보기 버튼이 엉뚱한 캠페인의 광고그룹으로 이동. 예: "슬림업 사무실 게시판 4구" 상품이 다른 캠페인의 "게시판" 광고그룹으로 링크됨.

**원인**: 기존 `grpMap[g.name] = g.nccAdgroupId` (HTTP_adgroups 순회). 서로 다른 캠페인에 같은 이름 광고그룹이 있으면 **마지막 순회된 것이 덮어씀** → 1:N 이름 충돌 정보 상실.

**데이터 흐름 발견**: TSV_파싱 시점에 이미 `campaignId`, `adgroupId`가 raw에 존재. 이름조인 노드가 이름으로 치환하면서 ID를 버리고 있었음. → **ID만 보존하면 추가 API 호출(/ncc/campaigns) 없이 해결**.

**최종 해결 방식**:
1. 이름조인 return에 `캠페인ID: r.캠페인ID, 광고그룹ID: r.광고그룹ID` 필드 추가
2. 리포트_생성에서 `grpByProd[상품ID] = 광고그룹ID` 맵 구축 (from `$('이름조인').all()`)
3. `grpUrl(prodId)` 시그니처로 변경. actionBtns는 `grpUrl(id)` 호출

**실측 결과 (04-20 리포트 수동 실행)**: 광고그룹명 "게시판"이 3개 서로 다른 adgroupId(grp-..40179742 / grp-..39916011 / grp-..40574034)로 정확히 분산. 이름 충돌 실제 존재 확인 + v12-11이 이를 상품ID 단위로 정확 매핑.

## 대안으로 검토된 방법 (채택 안 함)

- 캠페인 API 노드 신규 추가(서명_생성_campaigns_GET + HTTP_campaigns) → 이미 `HTTP Request` 노드가 `/ncc/campaigns` 호출 중이고 `이름조인`에서 참조. 그러나 **TSV raw에 adgroupId가 있어 API 없이 해결 가능**해서 불필요.
- `{캠페인명::광고그룹명}` 복합키 → 상품ID 키보다 더 복잡하고, 상품 1개가 광고그룹 1개에 속하는 구조상 상품ID 키가 자연스러움.

## v12-10 요일 버그 핵심 (재발 방지)

**증상**: 04-20 리포트 헤더에 "2026-04-20(일요일)"로 표기. 실제 04-20은 월요일.

**원인**: n8n Cloud 서버 로컬 타임존이 UTC. `new Date('2026-04-20T00:00:00+09:00')`는 UTC 기준 `2026-04-19T15:00Z` 시점. `.getDay()`가 서버 로컬(UTC) 기준으로 호출되므로 **하루 전(일요일)** 반환.

**수정**: `ymd + 'T12:00:00Z'` (UTC 정오로 파싱, 서버 타임존 불문 같은 date) + `getUTCDay()` 조합. Overview 본문의 `isWeekend` 판정도 동일 패턴 적용.

**검증**: `node -e "..."` 스모크 테스트 — 04-18(토) ~ 04-25(토) 8일 요일 전수 일치 확인.

## 2026-04-20 실측 검증 결과 (04-21 14:16)

- 매출 전 채널 실금액 표시: CS 1,153만 / 스토어 205만(광고 329,700) / 자사com 51만 / 자사kr 28만 / 쿠팡 57만 / G마켓 27만 / 영업 0원 ✓
- CS 평균 단가 268,323원, 주문 43건 — 하드코딩 해소 ✓
- AI 4단계 정상 동작 (자동실행 1 / 사람승인 14 / 보류 0) ✓
- 영업 섹션 정상 문장 ("당일 0원·0건 / 주간 평균 213,620원") ✓
- AI 한글 키 ("왜 그런가요?", "AI 확신", "할 일" 등) ✓
- 규칙 한글 문구 ("광고비만 나가고 매출 0") ✓
- 상품 TOP 20 pLink 전수 적용 ✓
- 광고그룹 딥링크 (accountId=1872088) 전수 적용 ✓
- **요일 버그만 유일한 이슈 → v12-10으로 해결**

## v12-8 매출시트 해결 핵심 (재발 방지)

**문제 3중**:
1. googleSheets 노드는 25K rows에서 OOM 발생 (04-21 오전 v1~v11 시행착오)
2. Sheet API range "현황!A1:Q2000" → parse 실패. **실제 tab 이름은 "업체계약현황"** (n8n 캐시 "현황"은 오래됨)
3. 매출시트_조회 upstream에 상품매핑_읽기(2208 items)가 물려있어 executeOnce 없으면 2208번 API 호출 → quota 초과

**최종 설정**:
- Node type: `n8n-nodes-base.httpRequest` (typeVersion 4.2)
- URL: `https://sheets.googleapis.com/v4/spreadsheets/{id}/values:batchGet`
- queryParameters:
  - `ranges`: `업체계약현황!A1:R2000` (R열 = 총 금액)
  - `valueRenderOption`: `UNFORMATTED_VALUE`
- Authentication: `predefinedCredentialType` → `googleSheetsOAuth2Api` (cred id `HjfwX5DgD4iXkptZ`)
- **`executeOnce: true`** (노드 최상위, 필수)

**컬럼 매핑 (실측 2026-04-21)**:
- col 0 = 년 (A, 값만 있고 헤더는 "A1:AB2000" 텍스트)
- col 1 = 월, col 2 = 일, col 3 = 진행자
- col 17 = **총 금액 (R열)** ★ 메모리상 Q였지만 실제로 R
- col 16 = 수량 (P 아닌 Q)

## v12-9 광고그룹 딥링크

**URL 구조**: `https://ads.naver.com/manage/ad-accounts/1872088/sa/adgroups/{grpId}`
- accountId=`1872088` (하나사인몰 계정)
- `HTTP_adgroups` 노드에서 `nccAdgroupId` ↔ `name` 맵 추출
- 상품 item의 `광고그룹` name으로 join → grpId 찾아 딥링크
- 매칭 실패 시 `/adgroups` 리스트 페이지로 fallback

## 규칙 코드 → 한글 매핑 (v12-9 `RULE_NAME`)

| 코드 | 한글 |
|---|---|
| COST-NO-CONV | 광고비만 나가고 매출 0 |
| D-01 | 광고 효율 급락 (실 ROAS 20% 이상↓) |
| D-02 | 클릭률 급락 (40% 이상↓) |
| D-03 | 검색 순위 밀림 (5단계 이상↓) |
| D-04 | 노출되는데 클릭이 없음 |

## AI 응답 JSON 키 한글화 (v12-9 `KEY_KO`)

- 원인분석 → 왜 그런가요?
- 신뢰도 → AI 확신
- 추가확인필요 → 더 봐야 할 것
- 분류 → 결정
- 조치 → 할 일
- 사유 → 이유

## 작업 중 학습된 n8n 노하우

1. **매번 PUT 전 최신 GET 필수**. 로컬 JSON에 기반한 덮어쓰기는 다른 사람/다른 세션의 수정을 지움 (v12-1/2가 v12-1.5 PUT 때 원복된 사고 재발생)
2. **httpRequest 노드의 executeOnce**는 upstream 아이템 수 만큼 반복 호출을 막음. 멀티 아이템 파이프라인에서 외부 API 호출 전 반드시 확인
3. n8n googleSheets 노드의 `sheetName.cachedResultName`은 캐시된 과거 이름. Sheets API 직접 호출 시 현재 tab 이름 별도 확인 필요 (`GET /spreadsheets/{id}?fields=sheets.properties`)
4. `settings` 객체는 PUT 시 `{executionOrder: "v1"}` 만 허용. 다른 필드 포함 시 400
5. `n8n-nodes-base.code`에서 `$('노드이름').first()` 호출은 해당 노드가 먼저 실행돼야 가능. 단독 `Execute step`에선 실패 → try-catch + fallback 필수

## 현재 n8n 노드 상태 (2026-04-21 저녁)

| 노드 | 타입 | 상태 |
|---|---|---|
| 매출시트_조회 | httpRequest | batchGet 업체계약현황!A1:R2000, executeOnce |
| 채널별_집계 | Code | batchGet 응답 파싱 → 영업/CS/스마트/자사/쿠팡/G마켓 집계 |
| Verifier_L1 | Code | `$input.all()` 정상 |
| Analyst_프롬프트 | Code | `$('Verifier_L1').first().json` |
| Analyst_API | httpRequest | max_tokens 8000 |
| Strategist/Critic/Verifier_L2_API | httpRequest | max_tokens 4000 |
| 리포트_생성 | Code | pLink + grpMap + renderStage + 한글화 완료 |

## 백업 파일 (필요 시 복원 지점)
- `/mnt/단순등록자동화/wf_backup_20260421_oom_fix_직전.json` — v12 작업 시작 전
- `/mnt/단순등록자동화/wf_backup_20260421_v12_직전.json` — v12-1,2 적용 전
- `/mnt/단순등록자동화/wf_backup_20260421_before_v12_10.json` — v12-10 적용 전
- (v12-11 직전 스냅샷은 `/sessions/inspiring-stoic-goodall/v12_10/wf_after.json`에 세션 임시 저장됨)

## 내부 규칙 코드 A-01 / F-01 등 노출 이슈 (경미, 이월)

AI 판정 본문에 `A-01 준수(30% 이내)`, `F-01 해당(10% 초과로 사람 승인 필요)` 같은 내부 규칙 코드 노출. `RULE_NAME` 매핑은 D-01~D-04와 COST-NO-CONV만 커버. A/F 계열은 AI가 본문에서 직접 쓴 것이라 후처리 치환 또는 프롬프트 수정 필요. v12-11 후보.

**Why**: 04-21 아침에 v11까지 매출시트 OOM/stub 회피만 반복하다가 사용자 "이 꼴로는 내일 전면 재정비"(=v12) 결정. 하루 만에 UX·데이터·액션 전부 복구.

**How to apply**: 다음 세션 시작 시 이 파일부터 읽고 현재 상태 파악. 추가 개선 시 v12-10 부터 번호 이어 붙일 것.
