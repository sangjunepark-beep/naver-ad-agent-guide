---
name: 리포트 개편 v11 — 2026-04-21 실행 완료 (일부 이슈)
description: 04-21 실행 성공. 메일·GitHub Pages 도달. 단 매출시트 OOM으로 매출 분기 비활성화 + 하드코딩 샘플값 잔존 + AI 4단계 "데이터 부재" 판정. v12 재정비 필요
type: project
originSessionId: 56117a92-499d-458f-9b4e-f428c8b0b6ed
---

## 2026-04-21 최종 결과 — v12로 이관

v11 수동 실행 → 파이프라인은 끝까지 완주하나 리포트 내용 품질 이슈 3건:
1. 매출시트 25K rows n8n 메모리 초과 → 매출 분기 Code stub로 임시 비활성화 (모두 0원 표시)
2. 리포트_생성 노드에 샘플 하드코딩값 잔존 (CS 평균 359,167원, 주문 24건 등 정적 HTML)
3. Verifier_L1 try-catch fallback이 rows=[]로 빠지면서 AI 4단계 전부 "데이터 부재" 판정

상세 내역 및 v12 작업 계획: `project_20260421_sales_oom_and_v12_plan.md` 참조
## 2026-04-20 구현 내역

### 추가된 노드 (메인 파이프라인 UJrNqijTudgU91sX)
| 이름 | 타입 | 역할 |
|---|---|---|
| 매출시트_조회 | googleSheets read | 매출시트 25K행 전체 read (credential HjfwX5DgD4iXkptZ) |
| 채널별_집계 | code | 진행자별 GROUP BY · T/T-1/T-2/주간평균 채널 매출 집계 |
| 일일수집로그_조회 | googleSheets read | 01_일일수집로그 전체 read (gid=1416410435) |
| 광고비교_집계 | code | T-1·주간평균 광고 KPI 집계 (노출/클릭/비용/매출/ROAS) |

### 변수_설정 노드 추가 항목
- github_pat (ghp_... 평문 저장, 세션 후 폐기 예정)
- github_owner = sangjunepark-beep
- github_repo = hanasignmall-ad-reports
- report_base_url = https://sangjunepark-beep.github.io/hanasignmall-ad-reports

### 리포트_생성 노드 전면 재작성
- v10 템플릿 HTML (15KB, 20개 플레이스홀더) 인라인 상수
- 데이터 바인딩: 채널별_집계, 광고비교_집계, _meta, Analyst/Strategist/Critic/Verifier_L2 4단계 응답
- GitHub API PUT으로 reports/{수집일}.html 자동 배포 (GET sha → PUT)
- 메일 본문 = 요약 네이버 로고 헤더 + KPI 3개 + [상세 보기] 버튼
- 메일 제목: `[하나사인몰] YYYY-MM-DD(요일) 네이버 스마트스토어 광고 보고서`

### 연결 구조
- 상품매핑_읽기 → 매출시트_조회 → 채널별_집계 (dead-end 분기)
- 상품매핑_읽기 → 일일수집로그_조회 → 광고비교_집계 (dead-end 분기)
- 리포트_생성 코드 내부에서 `$('채널별_집계').first()`, `$('광고비교_집계').first()` 참조

## 미검증 (수동 실행 필수)
1. **dead-end 분기 실행 순서** — 채널별_집계/광고비교_집계가 리포트_생성 실행 전 완료되는지 확인 필요. 실패 시 리포트_생성 전에 merge 노드 추가
2. **GitHub PAT 권한** — 첫 API PUT 호출. 403 시 PAT scope 확인 (repo 필요)
3. **매출시트 25K행 quota** — gviz 아닌 credential API로 읽으므로 quota 제한 다름
4. **HTML 템플릿 이스케이프** — ${...} JS interpolation 이스케이프 처리됐는지 런타임 확인

## 수동 실행 절차 (사용자 수행)
1. n8n UI → 네이버 검색광고 에이전트_파이프라인 열기
2. 우상단 "Execute Workflow" 클릭
3. 실행 종료 후:
   - Gmail 수신함에서 메일 제목·본문 확인 ("[상세 보기]" 버튼 링크)
   - GitHub Pages https://sangjunepark-beep.github.io/hanasignmall-ad-reports/reports/{YYYY-MM-DD}.html 접속
4. 문제 발생 시 실행 화면의 각 노드 output 확인 후 공유

## 백업 파일
- `/sessions/peaceful-vibrant-planck/mnt/단순등록자동화/wf_backup_20260420_매출시트노드_직전.json`

## 보안 메모
- github_pat `ghp_RfaMX...` 워크플로우 JSON에 평문. 세션 종료 후 **폐기 또는 재발급 후 n8n credential로 이전** 권장

**How to apply**: v11은 종결. 내일(04-22+) v12로 리포트_생성 전면 재정비. 하드코딩값 제거 + Verifier_L1 정상화 + 영업 매출 섹션 텍스트 수정.
