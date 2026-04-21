---
name: 광고매체 통합 수집 계획 — 04-21 문서 2건 완료, 자격증명 대기
description: Google Ads MCC 가이드 + 쿠팡/ESM 문의 템플릿 작성 완료. 네이버 B계정 자격증명 공유 대기. API 승인 후 n8n 연동
type: project
originSessionId: 56117a92-499d-458f-9b4e-f428c8b0b6ed
---
## 2026-04-21 진행 상태
- **Google Ads MCC + Developer Token 가이드** ✅ 작성 완료 → `/mnt/단순등록자동화/Google_Ads_MCC_DevToken_가이드.md`
  - MCC 생성, Developer Token 신청 영문 템플릿, OAuth2, n8n 연동 단계별 가이드
  - 토큰 승인 1~3영업일 소요 예정
- **쿠팡/ESM Plus 문의 메일 템플릿** ✅ 작성 완료 → `/mnt/단순등록자동화/쿠팡_ESM_Plus_API문의_메일템플릿.md`
  - Wing Partner API + ESM Open API 두 건
  - 판매자 ID만 교체하면 즉시 발송 가능
- **네이버 B계정 (파워링크·자사몰)** — 사용자가 API Key / Secret / CUSTOMER_ID 3개 공유 대기 중

## 결정 — 2026-04-21 착수 (완료된 부분 제외)
리포트 v11 수동 실행 검증과 별개로, **광고 매체별 데이터 수집 경로 전수 점검 및 통합 파이프라인 설계**.

## 하나사인몰 광고 계정 구조 (확정)

| 계정 | 광고상품 | 용도 | API | 현 연결 상태 |
|---|---|---|---|---|
| 네이버 A | 쇼핑검색광고 | 스마트스토어 소재 | searchad.naver.com (ID_A) | ✅ n8n에 기본 연결 (naver_api_key) |
| 네이버 B | 파워링크(사이트검색광고) | **자사몰**(hanasignmall.com / .kr) 랜딩 | searchad.naver.com (ID_B) | ❌ 미연결. 별도 CUSTOMER_ID+키 필요 |
| Google Ads | 검색/디스플레이 | (전체) | ads.googleapis.com | ❌ Developer Token 미발급 |
| 쿠팡 Rocket Growth | 검색광고 | 쿠팡 입점 | developers.coupangcorp.com | ❌ 미연결. 광고 성과 API 범위 확인 필요 |
| G마켓/옥션 | AI매출업·스마일광고 등 | ESM Plus | **공식 광고 API 없음** | ❌ robots.txt 전면 차단 + 약관상 스크래핑 금지 |

## 채널별 도입 계획

### 1) 네이버 B (파워링크·자사몰) — 난이도 낮음
- 필요 입력: `naver_api_key_2`, `naver_secret_key_2`, `naver_customer_id_2`
- 작업: 변수_설정에 3개 변수 추가 → 수집 노드 2벌로 분기 → 01 시트에 `계정`·`광고상품` 컬럼 추가
- 예상: 1~2시간
- **착수 조건**: 박상준 차장이 B 계정 자격증명 3개 공유

### 2) Google Ads — 난이도 중
- 선행: Google Ads 매니저 계정(MCC) 확보 → Developer Token 신청 → 승인 5~14 영업일
- Access Level 목표: **Basic**(15,000 ops/day로 충분)
- 인증: OAuth2 (refresh_token 획득)
- 2026-04부터 Cloud-managed 옵션도 선택지 (토큰 없이 Google Cloud org 단위 관리)
- 예상: 토큰 발급 2주 + 개발 4~6시간

### 3) 쿠팡 Rocket Growth — 난이도 중~상
- 공식 Open API(developers.coupangcorp.com)의 **광고 성과 API 범위 확인** 필수 (Product Creation/Management는 확인, 성과 데이터는 불확실)
- WING 담당 MD에 공식 문의 필요
- 인증: API Key + HMAC-SHA256
- 예상: 담당자 협의 후 PoC → 범위 보이면 반나절 개발

### 4) G마켓/옥션 — 자동 수집 **비권장**
- `ad.esmplus.com/robots.txt` Disallow: / (전면 차단)
- ESM Plus 이용약관상 스크래핑 명시 금지
- **대안 A**: 운영자가 주 1~2회 수동 export → 구글 시트 붙여넣기 (시트 참조로 리포트에 편입)
- **대안 B**: ESM 본사/담당 MD에 "광고 리포트 API 제공 여부" 공식 문의 (메일 1통)
- **대안 C**: 이미 매출시트 `G마켓` 진행자로 매출은 집계됨. 광고비·ROAS만 수동 기재 운영
- 권장: B(공식 문의) + C(현 매출시트 유지)

## 내일(2026-04-21) 세션 우선순위

1. 박상준 차장이 네이버 B 계정 3종 자격증명 공유 가능한지 확인 → 가능 시 즉시 반영 (단계 1)
2. Google Ads Developer Token 신청 가이드 작성 + 매니저 계정(MCC) 발급 절차 안내 (단계 2 착수)
3. 쿠팡 WING 담당 MD 이메일 템플릿 작성 — "Rocket Growth Ads 광고 성과 API 공식 범위" 문의 (단계 3 대기)
4. ESM Plus 공식 문의 메일 템플릿 작성 (단계 4 대안 B)

## 오늘(2026-04-20) 세션에서 미완료된 것
1. **리포트 v11 수동 실행 검증** — `project_report_redesign_v11_inprogress.md` 참조. 사용자가 n8n UI에서 Execute Workflow 한 번 돌려야 GitHub Pages·Gmail 정상 동작 확인 가능
2. **GitHub PAT 보안** — 현재 n8n 워크플로우 JSON에 평문 저장. 세션 종료 후 **폐기 또는 재발급 후 n8n credential로 이전** 권장
3. **"오늘의 종합 결과" → "어제의 종합 결과"** — v11 코드엔 이미 반영됨 (overview-label 하드코딩이라 자동 갱신되진 않음, 필요 시 수동 편집)

**Why**: 단일 채널(네이버 A) 기준 리포트 완성만으로는 "전체 광고 효율" 판단이 어려움. 다채널 통합 후 실 ROAS·채널 비중을 한 화면에 보여야 의사결정 가능.

**How to apply**: 내일 세션 시작 시 이 메모 먼저 읽고, 단계 1부터 순차 진행. 자격증명 기다리는 구간은 단계 2·3 문서 작업 병행.
