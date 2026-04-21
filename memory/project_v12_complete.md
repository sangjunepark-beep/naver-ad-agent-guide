---
name: 2026-04-21 v12 리포트 전면 재정비 완료
description: v12-1~v12-9 총 9개 패치로 AI 4단계 복구, 매출시트 OOM 해결(Sheets API batchGet), 상품별 링크, 광고그룹 딥링크, 용어 한글화까지 완료
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

**Why**: 04-21 아침에 v11까지 매출시트 OOM/stub 회피만 반복하다가 사용자 "이 꼴로는 내일 전면 재정비"(=v12) 결정. 하루 만에 UX·데이터·액션 전부 복구.

**How to apply**: 다음 세션 시작 시 이 파일부터 읽고 현재 상태 파악. 추가 개선 시 v12-10 부터 번호 이어 붙일 것.
