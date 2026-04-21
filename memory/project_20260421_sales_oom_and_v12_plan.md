---
name: 2026-04-21 매출시트 OOM 우회 + 리포트 v12 재정비 계획
description: 04-21 리포트 v11 수동 실행 중 매출시트 25K rows OOM → 매출 분기 임시 비활성화 + AI 검증 파이프라인 이슈 발견. 내일 v12로 리포트 전면 재정비 예정
type: project
originSessionId: e6bca7da-b70c-4168-8fc9-20198abca61e
---
## 오늘(2026-04-21) 진행 요약

### 1. 원래 계획 4개 중 3개 완료
- **1번 리포트 v11 수동 실행**: 부분 성공 (메일·GitHub Pages 발송은 되지만 내용 이상)
- **2번 네이버 B 계정 자격증명**: 사용자 미공유 (대기)
- **3번 Google Ads MCC + Developer Token 가이드**: ✅ 완료
  - `/mnt/단순등록자동화/Google_Ads_MCC_DevToken_가이드.md`
- **4번 쿠팡/ESM Plus 문의 메일 템플릿**: ✅ 완료
  - `/mnt/단순등록자동화/쿠팡_ESM_Plus_API문의_메일템플릿.md`

### 2. 매출시트 OOM 여정 (v1 → v11, n8n API PUT으로 11번 시도)

| 버전 | 시도 | 결과 |
|---|---|---|
| v1 | 매출시트_조회를 httpRequest + gviz URL | 403 인증 실패 (private 시트, gviz 미지원) |
| v2 | googleSheets + filtersUI (년=2026, 월=4) | "The column '년' could not be found" 헤더 감지 실패 |
| v3 | Sheets API v4 batchGet, ranges=[A1:T1, A20000:T27000] | "Unable to parse range" (A20000:T27000 시트 최대 초과) |
| v4 | 같은 batchGet, ranges=[A1:T1, 'A22000:T'] | open-ended "A22000:T" 문법 parse 거부 |
| v5 | 단일 GET `/values/현황!A:T` | 역시 parse 실패 (원인 불명, sheet name 추정) |
| v6 | googleSheets 원본 복원 + Code 스트림 최적화 (.map 제거) | **매출시트_조회 노드 자체 OOM** (25K rows 변환 한계) |
| v7 | 매출시트_조회 → Code 더미 (`{_stub:true}`) | PUT은 OK, 하지만 뒷단 타이밍 이슈 발생 |
| v8 | 채널별_집계에 try-catch + 날짜 fallback 추가 | "Execute Step" 단독 실행 오인 → 사용자 "Execute Workflow로 했다" 확인 |
| v9 | 광고비교_집계도 같은 안전처리 예방 적용 | PUT 시 채널별_집계가 원복된 상태로 덮어쓰기됨 (버그) |
| v10 | 누적 덮어쓰기 버그 발견 → 최신 GET 후 매출시트_조회만 재설정 | 채널별_집계 또 원복 상태 발견 |
| v11 | 최신 GET + 채널별_집계 강제 재적용 + Verifier_L1 try-catch 래핑 | **실행 성공, 메일·GitHub Pages 정상 도달** |

### 3. v11 이후 발견된 리포트 내용 품질 이슈

사용자가 공유한 `https://sangjunepark-beep.github.io/hanasignmall-ad-reports/reports/2026-04-20.html` 점검 결과:

**정상 동작**
- 광고 KPI: 노출 166,279 / 클릭 536 / 비용 740,234원 / 스마트스토어 광고매출 329,700원 / ROAS 44.5%
- 캠페인별 실적 표 정상 (소재수, 노출, 클릭, 비용, 매출)

**이상 1: 매출 분기 비활성화로 0원 표시 (의도됨, sales mirror 구축 대기)**
- CS 매출 / 자사몰(com, kr) / 쿠팡 / G마켓 / 영업(영호) 전부 0원
- 이유: `채널별_집계`가 stub 0원 반환 상태

**이상 2: 리포트 템플릿에 샘플 하드코딩값 잔존** ★★★
- 리포트_생성 노드 코드 line 426에 정적 HTML:
  ```html
  <div class="kpi-value">359,167</div>
  <div class="kpi-label">CS 평균 단가 (원)</div>
  <div class="kpi-delta neutral">▼ -1.1%</div>
  ```
- CS 주문 24건, △+3건 같은 샘플값도 하드코딩됨
- v10 샘플 디자인 때 박아둔 값이 변수 치환 안 되고 그대로 배포 중

**이상 3: AI 4단계 검증 전부 "데이터 부재" 판정**
- Verifier_L1의 try-catch fallback을 `rows = []`로 잡아서 이상 탐지 0건
- Analyst / Strategist / Critic / 최종판정 모두 "데이터 없음" 반복
- 자동실행·사람승인·보류 0건씩

**이상 4: 영업 매출 섹션 텍스트 깨짐**
- "영업 o원·오전·이전 이원·주간 평균 이원" 같은 문구 (템플릿 문자열 파손 의심)

---

## 내일(2026-04-22~) 리포트 v12 작업 계획 (사용자 확정: "B안" = 내일 전면 재정비)

### 우선순위 1: Verifier_L1 fallback 정상화
- `let rows = []; try { rows = $('데이터_합산').all(); } catch (e) { rows = []; }` 구조를 **정상 실행 경로 보장된 위치**에서는 try-catch 제거
- 워크플로우 연결 구조상 `데이터_합산 → Verifier_L1`이 직렬이면 try-catch 불필요
- Verifier_L1 output이 정상이면 Analyst/Strategist/Critic 이후 체인 자동 복구

### 우선순위 2: 리포트_생성 노드 하드코딩 샘플값 전수 제거
- 코드 길이 32KB, 약 800줄
- 의심 라인: 426 (CS 평균 359,167) 외에도 산재 가능성 있음
- 작업:
  - `359,167`, `24`, `3건`, `-1.1%`, `+0.0%` 등 하드코딩 문자열 grep
  - 각각 `${chan.CS_매출_T}`, `${chan.CS_건수_T}`, `${deltaPct(...)}` 등 변수 참조로 교체

### 우선순위 3: 영업 매출 섹션 텍스트 깨짐 수정
- 해당 영역 템플릿 리터럴 점검
- `${fmtN(chan.영업_매출_T||0)}원` 같이 정상 인터폴레이션인지 확인

### 우선순위 4: AI 4단계 체인 입출력 재검증
- Verifier_L1 → Analyst → Strategist → Critic → 최종판정
- 각 노드가 upstream의 어떤 필드 참조하는지 맵 작성
- 테스트 실행 → 각 단계 output이 비어있지 않은지 확인

### 우선순위 5 (여유 시): 매출 섹션 본격 복구 계획
- 매출시트 25K rows OOM 근본 해결 방법 결정:
  - **A안 (추천)**: Mirror spreadsheet 생성 — 별도 시트에 `=QUERY(IMPORTRANGE(...))` → ~2K rows만 n8n 수신
  - B안: n8n Cloud 플랜 업그레이드 (비용 발생)
- 사용자 결정 받고 진행

---

## 현재 n8n 노드 상태 (2026-04-21 23시 기준)

| 노드 | 타입 | 상태 |
|---|---|---|
| 매출시트_조회 | Code | `_stub: true` 더미, 매출 조회 안 함 |
| 채널별_집계 | Code | 모든 채널 0원 반환, 데이터_합산 try-catch 안전 |
| 광고비교_집계 | Code | 데이터_합산 try-catch 안전, 실제 집계는 정상 작동 |
| Verifier_L1 | Code | rows=[] fallback으로 이상 탐지 불가 — **내일 복구 대상** |
| 리포트_생성 | Code | 변수 치환 정상 부분 + 하드코딩 샘플 잔존 혼재 — **내일 재정비 대상** |
| 나머지 | 정상 | |

## n8n API PUT 시 주의사항 (재확인)
- settings 객체는 `{executionOrder: "v1"}`만 허용 (다른 필드는 400 에러)
- 매번 PUT 전에 **최신 GET 필수** — 로컬 json 기반 덮어쓰기 시 이전 수정이 날아감 (오늘 여러 번 실수)

## 백업 파일
- `/mnt/단순등록자동화/wf_backup_20260421_oom_fix_직전.json` (오늘 작업 시작 전 상태)

**How to apply**: 내일 새 컨텍스트 시작 시 이 파일 먼저 읽고, 우선순위 1부터 순차 진행. Verifier_L1 fallback 제거 전 **데이터_합산 → Verifier_L1 연결 직렬성 먼저 확인** 필수. 아니면 또 분기 타이밍 이슈 재발 가능.
