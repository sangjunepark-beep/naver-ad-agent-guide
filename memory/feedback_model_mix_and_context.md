---
name: 모델 혼합·컨텍스트 알림 규칙 (구체 매핑 포함)
description: Haiku/Sonnet/Opus 용도별 분리 사용 규칙 + 스킬·n8n 노드·업무유형별 기본 모델 매핑. 2026-04-17 매핑표 추가.
type: feedback
originSessionId: 73d17a75-c9c6-489e-b049-e2b9201fb05d
---
토큰 소비 절감을 위해 모델을 계층적으로 분리해서 사용하고, 컨텍스트 사용률 임계점마다 자동 보고한다.

**Why:** 2026-04-16 박상준 차장이 프로젝트 전반의 토큰 소비를 관리하기 위해 세팅. Phase 1~4까지 오면서 컨텍스트 누적·반복 호출 비용이 커짐. 최종 결정권·사전 컨펌 원칙(feedback_decision_and_token_confirmation.md)의 실행 세부 규칙.

**How to apply:**

### 1) 모델 기본 원칙
- **Haiku**: 단순 반복·기계 작업. 판단 여지 적고 입력→출력 매핑이 명확한 경우.
- **Sonnet (기본값)**: 실무 대부분. 글쓰기·디버깅·분석·문서화.
- **Opus**: 구조 설계·전략 판단·복잡 근본원인 추적. 판단 파급도가 크고 잘못되면 되돌리기 어려운 경우.
- Haiku/Opus 전환 시 **착수 전 "이 작업은 ○○ 모델로 돌리겠습니다" 한 줄 보고 후 진행**
- 모델 전환은 사용자가 Cowork UI에서 수동 전환하는 구조. Claude는 요청 형태로 안내.

### 2) 스킬별 기본 모델 매핑

**Haiku (기계적·반복·변환)**
- admin-toggle-fix — 체크박스 토글 감사/수정
- github-deploy — API 업로드
- schedule — 스케줄 등록
- consolidate-memory — 파일 정리·인덱스 갱신
- productivity:task-management — TASKS.md 추가/완료 처리
- productivity:update — 동기화
- xlsx / pdf / docx — **단순 추출·변환·값 입력만**일 때
- card-news — 템플릿 채우기 수준

**Sonnet (실무·글쓰기·분석)**
- docx / xlsx / pdf / pptx — 구조 설계·서식 있는 문서 작성
- marketing:* 전체 (draft-content, content-creation, brand-review, email-sequence, performance-report, seo-audit, competitive-brief)
- customer-support:* 전체
- operations: status-report, runbook, process-doc, vendor-review, compliance-tracking, process-optimization
- data:* 전체 (write-query, sql-queries, explore-data, analyze, validate-data, statistical-analysis, data-visualization, create-viz, build-dashboard, data-context-extractor)
- productivity:memory-management
- 일반 n8n 워크플로우 디버깅·JSON 수정
- **세션 기본값**

**Opus (구조 설계·전략·근본 판단)**
- operations:risk-assessment — Phase 단위 리스크 체계
- operations:capacity-plan — 인력/리소스 전략
- operations:change-request — Phase 5 같은 중대 변경 요청서
- marketing:campaign-plan — 분기 단위 캠페인 설계
- skill-creator — 새 스킬 아키텍처 설계
- Phase 전체 설계 / 파이프라인 아키텍처 / 규칙 제정 / 다계층 LLM 오케스트레이션 설계

### 3) n8n 파이프라인 노드별 모델 매핑 (권장)

현재 전 노드 `claude-sonnet-4-20250514` 단일 사용 중. Phase 5 선행 과제로 재배치.

| 노드 | 역할 | 현재 | 권장 |
|------|------|------|------|
| Analyst | 이상치 탐지·데이터 요약 | Sonnet | **Haiku** |
| Verifier_L1 | 정상/이상 분기 | Sonnet | **Haiku** |
| Strategist | 전략 판단·입찰가 제안 | Sonnet | **Sonnet 유지** |
| Critic | 제안 반박 논리 | Sonnet | **Sonnet 유지** (교차 효과용 Opus도 고려) |
| Verifier_L2 | 최종 검토 | Sonnet | **Sonnet 유지** |
| Reporter_정상 | 정상일 리포트 생성 | Sonnet | **Haiku** (템플릿 채우기 수준이면) |

예상 절감: Analyst·Verifier_L1·Reporter_정상 Haiku 전환 시 해당 호출 비용 약 1/10 수준.

### 4) 업무 유형별 매핑 요약

| 유형 | 예시 | 모델 |
|------|------|------|
| 파일 복사·이동·rename | sync, deploy | Haiku |
| 시트 값 조회·붙여넣기 | 01_시트 한 줄 읽기 | Haiku |
| JSON 한 줄 수정 | 노드 파라미터 1개 변경 | Haiku |
| 메모리 인덱스 갱신 | MEMORY.md 한 줄 교체 | Haiku |
| 보고서·런북·콘텐츠 작성 | 이번 세션 대부분 | Sonnet |
| n8n 노드 디버깅 | v6~v9 수정 | Sonnet |
| LLM 프롬프트 튜닝 | Analyst 프롬프트 개선 | Sonnet |
| 상세페이지·카드뉴스 초안 | 실제 제작 | Sonnet |
| 데이터 분석·쿼리 작성 | 실_ROAS 교차 분석 | Sonnet |
| Phase 설계 | Phase 5 구조 확정 | Opus |
| 리스크 레지스터 전체 | 이번 세션 Phase 5 선행 리스크 | Opus |
| 변경 요청서 (change-request) | Phase 5 공식 착수 직전 | Opus |
| 복잡 에러 근본원인 | 다계층 장애 분석 | Opus |

### 5) 애매할 때 판단 기준
1. **되돌리기 쉬운가?** 쉬우면 낮은 모델, 어려우면 높은 모델
2. **출력 길이·구조가 예측되는가?** 예측 가능하면 Haiku, 자유도 높으면 Sonnet+
3. **판단 파급도가 여러 후속 작업에 영향 주는가?** 영향 크면 Opus
4. **반복 호출되는가?** 반복성 높으면 Haiku로 떨어뜨릴 수 있는지 먼저 고민

### 6) 컨텍스트 사용률 알림 규칙
- **~50%**: 무알림, 정상 진행
- **50~70%**: 작업 마무리 시 "현재 컨텍스트 약 ○○% 사용 중" 한 줄 고지
- **70~85%**: 즉시 경고. "토큰 소비 급증 구간입니다. 작업 분할 or 메모리 저장 후 새 세션 권장" 컨펌 요청
- **85%+**: 작업 중단. 산출물 요약 → 메모리 저장 → 새 세션 유도

### 7) 추가 룰
- 긴 파일(>1000줄) 읽기 전 "전체 읽으면 컨텍스트 ○○% 소모 예상" 보고 후 부분 읽기 우선 제안
- 에이전트(Task) 호출 결과가 클 것으로 예상되면 **요약 형태로 받기**
- 반복 시트 조회·n8n 워크플로우 전체 덤프는 필요한 부분만 grep/부분 읽기
- 컨텍스트 실시간 수치는 추정치 — 사용자 쪽 Cowork UI 게이지로 교차 확인 권장
- **세션 기본값은 Sonnet.** Opus로 붙어 있는 상태에서 Sonnet 범위 작업이 시작되면 "Sonnet으로 전환 권장합니다" 안내

### 8) 세션 시작 시점 필수 체크 (2026-04-18 추가)
**모델 체크는 반드시 "세션 첫 응답"에서 선제적으로 수행.** 사용자가 지적하기 전에 먼저.

절차:
1. 세션 시작 시 env 블록의 `Model:` 값 확인
2. 사용자 요청 성격 판단 (위 2·4 매핑표 기준)
3. 불일치 시 첫 응답 맨 위에 한 줄 고지:
   - 예: "현재 Opus. 이 작업은 Sonnet 범위입니다 — Cowork UI에서 전환 권장."
4. 일치하면 고지 생략, 바로 작업 진행

**Why:** 2026-04-18 세션에서 Opus로 붙은 상태로 단순 확인 질문을 받았는데 선제 안내 없이 그냥 Opus로 응답함. 사용자가 "모델 규칙 지키고 있냐" 직접 물어본 뒤에야 인지. 토큰 비용 누수의 대표 케이스.

**How to apply:** 첫 응답 전 반드시 이 체크를 돌릴 것. 특히 Opus로 붙어 있으면 "정말 Opus 필요한가?"를 한 번 더 자문.
