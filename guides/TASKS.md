# Tasks

## Active

### 🔴 오늘~주말 (보안)
- [ ] **자격증명 3종 폐기** — 오늘 밤 내
  - GitHub PAT `ghp_deFq...` (과거 노출분) → github.com → Settings → Developer settings → Personal access tokens → Revoke
  - GitHub PAT `ghp_FhO05...` (이식 작업용) → 동일 절차
  - 네이버 검색광고 API Key/Secret → 광고 관리자 → API 관리 → Secret 재발급
  - Reference: `Phase5_선행_리스크_레지스터.md` R6

### 🔴 월요일 (2026-04-20) 1시간 액션 플랜
- [ ] **09:00 n8n 실행 이력 스냅샷** — 5분
  - hanasignmall.app.n8n.cloud/home/executions 캡처 (최근 7일 success/failed)
- [ ] **09:05 메인 파이프라인 Active 확인 + 수동 실행** — 15분
  - "네이버 검색광고 에이전트_파이프라인" Active ON 여부, Timezone Asia/Seoul
  - Execute Workflow 버튼으로 수동 1회 실행
- [ ] **09:20 시트 반영 교차 확인** — 10분
  - 01_일일수집로그 / 02_전환수집로그 / 03_이상치로그 / 04_제안기록 각각 오늘자 행 추가 확인
  - 03_실_ROAS_대시보드 조회일자 오늘로 갱신 확인
- [ ] **09:30 Phase4_승인_자동반영 Append 노드 매핑** — 10분
  - Document ID / Sheet 이름 "05_실행로그" / Map Each Column Manually 3축 점검
- [ ] **09:40 Phase 4 소폭(±1%) 재테스트** — 15분
  - 04_제안기록에 P999 테스트 행 → Webhook POST → 05_실행로그에 E00X 기록 확인 → 10분 내 수동 원복
- [ ] **09:55 History 표에 결과 기록** — 5분
  - 런북 "History" 섹션에 실행자·시각·관찰사항 기록

### 🟠 이번 주 (2026-04-20~26) Phase 5 선행 과제
- [ ] **R3 롤백 Webhook 구현** — 예상 2~3시간
  - Phase4_승인_자동반영 워크플로우에 "변경 전 bidAmt" 필드 저장
  - 별도 "1-클릭 원복 Webhook" 워크플로우 신규 구축 (실행ID 역적용)
  - 05_실행로그에 "원복링크" 컬럼 추가
- [ ] **R4 가드레일 Function 노드 3종** — 예상 1~2시간
  - 일일 변경 건수 상한 (기본 10건)
  - 변경폭 상한 (±20% 초과 차단)
  - 중복 승인 방지 (동일 제안ID 재승인 거부)
- [ ] **네이버 콘솔 일일 예산 상한 점검** (R9 병행)

### 🟡 다음 주 이후 (Phase 5 본착수 직전)
- [ ] **LLM 프롬프트 "CS 주문 가능성" 명시 재점검** (R5)
- [ ] **OAuth 만료 대응 로직 추가** (R7) — 실패 시 재시도 3회
- [ ] **승인 대기 48h 자동 알림 설계** (R11)
- [ ] **Phase 5 change-request 문서 작성** (operations:change-request 스킬 활용)
- [ ] **n8n LLM 모델 믹싱 재배치** — 예상 30분 (노드 JSON 파라미터 수정)
  - Analyst → Haiku (이상치 탐지·요약)
  - Verifier_L1 → Haiku (정상/이상 분기)
  - Reporter_정상 → Haiku (템플릿형 리포트)
  - Strategist/Critic/Verifier_L2 → Sonnet 유지
  - 예상 효과: 해당 3개 노드 호출 비용 약 1/10 절감
  - Reference: `feedback_model_mix_and_context.md` §3

## Waiting On

- [ ] **GitHub push** — 2026-04-19 PAT 필요 (config 없음)
  - memory/*.md 15개 + TASKS.md + 회사PC_시작프롬프트.md + sync_memory.sh
  - GH_TOKEN=[PAT] bash sync_memory.sh push 로 진행

## Someday

- [ ] **Phase 5 사후 ROAS 자동 측정 로직** (선행 4과제 해결 후)
- [ ] **Phase 5 효과 판정 규칙 정의**
- [ ] **Phase 5 실패 학습 루프** (비슷한 제안 재발 방지)
- [ ] **Phase 5 전체 가동 스케줄 확정** (일/주 주기)
- [ ] **Self-hosted n8n 이관 옵션 검토** (R10 분기 과제)
- [ ] **네이버 API 스키마 분기 점검 루틴** (R12)
- [ ] **CRM/주문관리 연동으로 CS 매출 자동 반영** (R5 근본 해결, 장기)

## 재평가 마일스톤

- [ ] **2026-04-24 (D+7): R1·R2·R6 상태 재평가**
  - E2E 가동 여부·시트 기록·자격증명 폐기 완료 교차 확인
- [ ] **2026-05-01 (D+14): R3·R4·R9 완료 여부 재평가 → Phase 5 Go/No-Go**

## Done

- [x] ~~상품 링크 근본 수정 완료~~ (2026-04-19)
  - 스마트스토어 CSV 2개(하나몰 1016개 + 더바른사인 303개) JOIN → D열 full URL 2208개 저장
  - pLink 코드 D열 직접 사용 방식으로 변경 (nvMid 기반 오류 완전 해소)
  - 테스트 이메일 jimrn22@gmail.com INBOX 도착 확인 ✅
- [x] ~~Phase 4 후속 점검 보고서 작성~~ (2026-04-17)
- [x] ~~파이프라인 재가동 런북 작성~~ (2026-04-17)
- [x] ~~메모리 정리 (consolidate-memory)~~ (2026-04-17)
  - project_phase4_done.md 재작성 (시트 기록까지 완결 → 부분완료)
  - project_overall_progress.md 재작성 (Phase 5 선행 4과제 명시)
  - MEMORY.md 인덱스 2줄 갱신
- [x] ~~Phase 5 선행 리스크 레지스터 작성~~ (2026-04-17)
  - Critical 1 / High 5 / Medium 4 / Low 2 = 총 12건
- [x] ~~집 PC Cowork 이식 + 동기화 체계 구축~~ (2026-04-16)
- [x] ~~Phase 4 실입찰가 변경 테스트 (2900→2470)~~ (2026-04-16)
- [x] ~~Phase 3.5 리포트 고도화~~ (2026-04-15)
- [x] ~~Phase 3 LLM 파이프라인 완주~~ (2026-04-15)
