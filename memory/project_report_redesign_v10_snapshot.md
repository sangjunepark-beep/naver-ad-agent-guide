---
name: 리포트 개편 v10 스냅샷 — 샘플 디자인 완료, n8n 실연동 대기
description: 2026-04-20 세션 종료 시점. GitHub Pages 샘플(04-17 평일 v10) 사용자 컨펌까지 완료. 다음 세션에서 n8n 2단계 실연동 착수
type: project
originSessionId: 6d1b954e-cc6c-4309-8ced-effc48f4c987
---
## 완료 범위 (2026-04-20)

### 매출 0원 이슈 복구
- **원인**: 01_일일수집로그 시트에 상품ID 컬럼 부재 → 시트_저장_Phase2 output에 상품ID 누락 → 데이터_합산 JOIN 실패
- **A안 핫픽스**: 데이터_합산에 상품명→adId 역매핑 fallback (허수 매출 유발로 이후 제거됨)
- **B안 정식화**: 01 시트 E2/K2 헤더 수정(상품명→상품ID / 상품명(매핑)→상품명) + 시트_저장_Phase2 schema에 상품ID 추가
- **A안 fallback 제거**: 동명이품 오매핑 방지
- 검증 완료: exec 163/164/166, 상품ID 1270/1270 채움

### 리포트 개편 1단계 완료
- GitHub 리포 `hanasignmall-ad-reports` 신규 생성 (Public, Pages 활성)
- URL: https://sangjunepark-beep.github.io/hanasignmall-ad-reports/
- robots.txt (검색엔진 차단) + index.html + reports/{YYYY-MM-DD}.html 구조
- 샘플: 2026-04-17 (평일), 2026-04-19 (일요일) 두 개

### 샘플 디자인 확정 (v10)
- 전체 다크 테마 (#0b1120)
- 네이버 공식 로고 (#03C75A) + 제목 "네이버 스마트스토어 광고 보고서"
- 오늘의 종합 결과 카드 (대표용 요약)
- 전일 대비 / 주간 평균 대비 비교 박스
- 광고 활동 KPI (노출/클릭/CTR/광고비)
- 네이버 검색광고 직접 성과 KPI (스마트스토어 광고 매출/건수/ROAS) ← 초록 하이라이트
- **채널별 매출 분포 테이블** (스마트스토어 전체/자사몰×2/쿠팡/G마켓/합계)
- CS 동반 지표 (매출/건수/평균단가)
- 영업 매출 참조 (점선 박스)
- 용어 풀이 (스마트스토어 광고 ROAS/자연 매출/자사몰/CS/영업)
- 캠페인별 실적 표 (전일 매출 비교 포함)
- 확인 요청 항목 아코디언
- AI 4단계 순차 검증 (1. 데이터 분석 → 2. 개선 제안 → 3. 반박 검토 → 4. 최종 판정) · 자신감 게이지
- 승인/보류 버튼 카드
- 이슈 맥락 (L1 업종·계절 / L2 과거 패턴 / L3 실시간 검색)

### 판정 기준 (사용자 확정)
- **평일 임계치**: 스마트스토어 광고 ROAS 300% 미만 = 경고
- **주말 임계치**: 별도 (자연 저조 반영, 28.5% 수준도 정상)
- "심각/경고" 표현 완화 → "CS 확인 요청/관찰/정상" 톤

### 하나사인몰 일별 매출 기준값 (확정)
- CS 매출 평일 평균: 800~900만원
- 온라인(스마트스토어 광고) 매출 평일 평균: 280~350만원
- 주말/공휴일은 현저히 낮음 (주말 CS ≈ 0)

## 미완 (다음 세션에서 착수)

### Task #12 · 리포트 개편 2단계 — 리포트_생성 노드 분리
- 이메일 = 요약 + [상세 보기] 링크 (GitHub Pages URL)
- 상세 페이지 JSON 덤프 노드 추가
- 영업일 규칙: T=월요일 → T-3(금) 비교, 나머지 T-1 비교

### Task #13 · 리포트 개편 3단계 — n8n이 HTML 자동 생성 + GitHub Pages 푸시
- 리포트_생성 코드 노드에서 템플릿 치환 방식
- github-deploy 스킬 로직 참고 (GitHub API PUT)

### Task #14 · 리포트 개편 4단계 — 이상 탐지 전체 펼치기 + AI 4단계 상세 렌더링
- AI 프롬프트에 전 영업일 비교 컨텍스트 주입
- Analyst/Strategist/Critic/Verifier_L2 각자 의견 전체 노출

### Task #15 · 리포트 개편 5단계 — 이슈 맥락 혼합
- 레벨 1: 업종·계절 고정 규칙 (4월 비수기 등)
- 레벨 2: 내부 실패 패턴 DB (06_실패패턴 시트 활용)
- 레벨 3: 웹 검색 (n8n HTTP 노드로 네이버 검색 API 또는 유사)

### Task #16 · 리포트 개편 6단계 — 네이버 로고 + 제목 + E2E 테스트
- 메일 제목: "하나사인몰 네이버 스마트스토어 광고 보고서"
- 네이버 로고: 현재 #03C75A 텍스트 로고로 처리 (사용자 OK)

### Task #9 · 03_실_ROAS_대시보드 04-14 멈춤 원인 조사 (별건)

## 주요 참조

- 매출 시트 ID: `169BTstGNSOPxx0aKglV2sTb_zhZWEfW1KTcht-K3afA` (읽기 전용, gid=1952467949)
- 진행자 채널 매핑: `reference_sales_sheet.md`
- 평일 기준값: `project_hanasignmall_daily_baseline.md`
- n8n 메인 워크플로우: UJrNqijTudgU91sX
- n8n credential: Google Sheets "Google Sheets - 하나사인몰" (HjfwX5DgD4iXkptZ)
- GitHub Pages 리포: sangjunepark-beep/hanasignmall-ad-reports

## 샘플 최신 버전 (v10)

- **평일 (04-17 금)**: https://sangjunepark-beep.github.io/hanasignmall-ad-reports/reports/2026-04-17.html
- **주말 (04-19 일)**: https://sangjunepark-beep.github.io/hanasignmall-ad-reports/reports/2026-04-19.html (아직 v7 상태, 용어 미업데이트)

**How to apply**: 다음 세션 시작 시 — (1) 메모리 pull → (2) 이 스냅샷 확인 → (3) Task #12 (리포트_생성 노드 분리 + JSON 덤프 + GitHub Pages 자동 푸시)부터 착수. 가상 샘플 수치를 실제 집계값으로 교체하는 작업.
