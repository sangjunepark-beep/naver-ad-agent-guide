---
name: 외부 평가서 + 워크플로우 복잡도 분석 + 다음 세션 인수인계
description: 다른 Cowork 세션에서 작성된 평가서(B-) 도착. 분석 결과 "꼬임 아님 / 중복 많음"으로 진단. 다음 세션 우선순위 8단계 정리
type: project
originSessionId: 35d08f6a-12fd-40ba-9cd3-904848f3b709
---
**사실**: 2026-04-25 작성된 외부 평가서 `광고관리에이전트_평가.md` 입수. 내용 요약 + 내 분석 결과:

### 평가서 핵심
- 종합 점수 **B-** (기획 A-, 운영 C, 유지보수성 C-)
- Failure rate 16.7%, 노드 71개(현재 77개), Anthropic ROI 미측정
- 8단계 개선 플랜: 0=Sticky note, 1=Retry, 2=Error Trigger, 3=Polling, 4=Prompt caching, 5=모델 분리(Haiku), 6=4분할, 7=Phase B 정리

### 평가서가 못 본 부분 (오늘 04-24 세션에서 처리됨)
- 5개 노드 KST 날짜 버그 → 패치
- 채널 분류 영호/하나몰 버그 → 패치
- 일자 오타 자동 보정 → 추가
- 스마트스토어 탭 v13 3스토어 분리 UI → 재설계
- 필드명/뱃지 5건 → 수정
- 네이버 매출 부풀림 1.3~1.9배 (5배 아님) → 재검증
- Phase B 의도는 메모리에 명확히 기록됨 (자사몰 1558945 B계정 수집) — 평가서가 메모리 못 봄

### 워크플로우 복잡도 분석 (2026-04-24 KST 17:50 측정)
- 총 77개 (활성 73, 비활성 4)
- 엣지 68개, **엣지/노드 = 0.88** → 1.0 미만 = 거의 일직선 그래프
- fan-out 최대 3 (변수_설정), fan-in 최대 2 (Phase3_시작_대기·리포트_생성)
- 사이클 없음
- 원거리 참조 핫스팟: 리포트_생성 12개 (hub 역할로 자연스러움), Strategist_프롬프트 6개

**진단**: **꼬임(entanglement) 아님. 중복(redundancy) 많음.**
- 서명_생성 12개, TSV_파싱 3개, 30/60초_대기+상태확인+분기 6개 = sub-workflow화 가능
- Deactivated 4개 = 즉시 삭제 가능
- 흐름은 추적 쉬움. 다만 시각적으로 길어 보임

### 시뮬레이션 (정리 효과)
| 작업 | 예상 노드 수 |
|---|---|
| 현재 | 77 |
| Deactivated 4개 삭제 | 73 |
| 서명_생성 sub-workflow화 | 62 |
| TSV_파싱 sub-workflow화 | 60 |
| Polling 패턴 통합 | 약 54 |

평가서의 "20~25개" 목표는 비현실적이지만 50대 중반은 도달 가능.

### 다음 세션 우선순위 (Top 4 — 1.5~2시간)
1. **Anthropic billing 캡처** (5분, 차장님이 콘솔에서 4월 청구액 확인) — ROI 베이스라인
2. **Error Trigger 워크플로우** (30분, n8n PUT) — 실패 묻힘 차단
3. **HTTP Retry 3회/5초 일괄** (15분, 약 20개 httpRequest 노드 일괄 PUT) — Failure rate 즉시 감소
4. **Sticky note 7장** (30분, Phase별 1줄씩 메모리→캔버스 동기화)

### 다음 세션 우선순위 (이번 주~이번 달)
5. Prompt Caching (Anthropic 4개 노드, 비용 50~80% 절감)
6. Analyst → Haiku 모델 다운그레이드
7. Polling 패턴 (Stats/Conv/B 3라인) — Failure rate 5% 목표
8. 워크플로우 4분할 + 서명_생성 sub-workflow

### 다음 세션 우선순위 (대기 큐 그대로)
- A: B계정 실데이터 수집 경로 연결
- B: B계정 Conv 경로 복제
- C: 메인 스케줄 09:30 + Cowork 자동화
- F: ADVoost 상품별 리포트 반영 (이미 데이터 추출 가능 확인)
- (보류) H: 허수 구분 시스템 — Conv API 재검증으로 필요성 하락

**Why**: 외부 평가가 정확한 부분(중복·Error Trigger·ROI 미측정·prompt caching)과 부정확한 부분(꼬임 표현·Phase B 의도 망각)을 구분해서 다음 세션 행동 우선순위 결정. 데이터 정확성 5건은 오늘 PUT으로 회복됐으니 다음은 운영 안정성·비용 효율 차례.

**How to apply**:
- 다음 세션 시작 시 이 메모와 `project_20260424_session_summary.md` 두 개 먼저 읽으면 즉시 이어갈 수 있음
- 평가서 8단계는 평가서 원문(`/mnt/uploads/광고관~1.MD`) 또는 메모리만으로 충분히 재구성 가능
- 차장님이 Anthropic billing 캡처 먼저 끝내주시면 ROI 측정 베이스라인 확보 즉시 가능
- n8n executions 기록 안 남는 상태(saveManualExecutions=false) 유지 — 메일·GitHub Pages로 검증
- 6번째 PUT부터는 다시 **최신 GET 기반 누적 수정 후 1회 PUT** 원칙 복귀 권장 (오늘 5회는 직렬 수행으로 충돌 없었음)

**주의**:
- 외부 평가서가 "Failure rate 16.7%"라고 한 근거 미확인 (n8n executions API에서 확인 가능했지만 saveManualExecutions=false라 향후 측정 어려움). 정확한 측정 필요 시 settings 일시 복원 후 1주일 운영 → 다시 false 권장
- "Phase B 의도 망각"은 평가서가 잘못 본 것. 메모리에 명확히 기록됨. 다만 캔버스 sticky note 부재는 사실
