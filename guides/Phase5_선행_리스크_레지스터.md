# Phase 5 착수 전 리스크 레지스터

**대상**: 네이버 검색광고 AI 에이전트 — Phase 5 (전체 가동 + 사후 ROAS 피드백) 착수 전 선행 리스크
**작성일**: 2026-04-17
**작성자**: 박상준 차장 (웹팀 총괄)
**근거 문서**: `Phase4_후속점검_보고서.md`, `런북_파이프라인_재가동.md`

---

## 0. 결론 (Top 3)

| 순위 | 리스크 | 등급 | 즉시 조치 |
|------|--------|------|----------|
| 1 | E2E 파이프라인 상시 가동 중단 (04-14 이후) | **Critical** | 월요일 런북 Step 2~3 수행 |
| 2 | 롤백 경로 부재 | **High** | Phase 5 착수 전 1-클릭 원복 구현 |
| 3 | 가드레일 부재 (일일 변경 상한·중복 승인 방지) | **High** | Phase 5 착수 전 Function 노드 3종 추가 |

**판정**: Phase 5 직행은 **수용 불가 리스크**. 위 3개 중 최소 2개 해결 전까지 Phase 5 착수 보류.

---

## 1. 리스크 매트릭스 (상황 배치)

```
                Low Impact    Medium Impact    High Impact
High Likelihood   R8             R5               R1 ★
Medium Lik.       R10            R7, R11          R3, R4, R6, R9, R12
Low Likelihood    —              —                R2
```

R1은 이미 "발생 중"인 상태라 이미 Critical 등급. 나머지는 잠재 리스크.

---

## 2. 리스크 레지스터 (12건)

### R1. E2E 파이프라인 상시 가동 중단 🔴 **Critical**
- **설명**: 2026-04-14 이후 메인 파이프라인("네이버 검색광고 에이전트_파이프라인") 실행 흔적 없음. 일일 9시 Cron 스케줄이 비활성 또는 실패 반복 중인 상태.
- **카테고리**: Operational
- **Likelihood / Impact**: 이미 발생 / High (데이터 축적 안 되면 Phase 5 사후 ROAS 측정 자체가 불가능)
- **Mitigation**:
  1. 런북 Step 2에 따라 Active 토글 + Timezone 확인
  2. 실행 이력에서 실패 유형(Credential/네트워크/스키마) 식별
  3. 수동 1회 실행으로 04-15~04-17 누락분 복구
  4. 다음 D+7 동안 매일 실행 이력 모니터링
- **Owner**: 박상준 차장
- **Status**: Open — 월요일 착수
- **재발 방지**: n8n 알림(Slack/이메일) 설정해 실패 시 자동 통보

### R2. 05_실행로그 자동 기록 경로 단절 🔴 **High**
- **설명**: Phase4_승인_자동반영 워크플로우가 04-16에 실제 API PUT은 수행했으나 05_실행로그에 행을 남기지 않음. Google Sheets Append 노드가 다른 시트·시트명을 가리키거나 컬럼 매핑이 깨진 상태 의심.
- **카테고리**: Operational
- **Likelihood / Impact**: Low (경로 자체는 구축됨, 재현율은 확인 필요) / High (기록 없으면 변경 이력 추적 불가 = 사후 ROAS 피드백 무의미)
- **Mitigation**:
  1. 런북 Step 4에 따라 Append 노드 단독 실행 테스트
  2. Document ID / Sheet 이름 / 컬럼 매핑 3가지 축 점검
  3. Mapping Column Mode는 "Map Each Column Manually"로 고정
- **Owner**: 박상준 차장
- **Status**: Open — 월요일 착수
- **재발 방지**: JSON import 후 체크리스트에 "시트 매핑 재확인" 단계 추가

### R3. 롤백 경로 부재 🔴 **High**
- **설명**: AI가 승인·반영한 변경을 1-클릭으로 원복할 수단이 없음. 현재 원복은 네이버 광고 관리자에서 수동 + 변경 전 값을 editTm 역추적으로 추정해야 함.
- **카테고리**: Operational / Financial
- **Likelihood / Impact**: Medium (Phase 5 가동 후 주 1~3회 발생 가능) / High (입찰가 급등 시 분 단위로 광고비 누적)
- **Mitigation**:
  1. Phase4_승인_자동반영 워크플로우에 "변경 전 bidAmt" 필드를 이메일·시트에 함께 기록
  2. 별도 "1-클릭 원복 Webhook" 워크플로우 구축 (실행ID 넘기면 해당 변경 역적용)
  3. 05_실행로그에 "원복링크" 컬럼 추가
- **Owner**: 박상준 차장
- **Status**: Open — Phase 5 착수 전 필수
- **예상 구현 시간**: n8n JSON 기준 2~3시간

### R4. 가드레일 부재 (일일 상한·중복 승인 방지) 🔴 **High**
- **설명**: AI가 동일 소재를 반복 제안하거나, 하루에 과다 건수를 변경하거나, 변경폭이 큰(±30% 이상) 제안이 그대로 실행될 가능성.
- **카테고리**: Operational / Financial
- **Likelihood / Impact**: Medium / High (일일 광고비 과지출 또는 순위 급락)
- **Mitigation**:
  1. Webhook 앞단에 Function 노드 3종 추가
     - 일일 변경 건수 상한 (기본 10건)
     - 변경폭 상한 (±20% 초과 시 차단)
     - 중복 승인 방지 (동일 제안ID 재승인 거부)
  2. 상한 초과 시 승인 버튼 클릭 시 에러 리턴 + 박상준 차장에게 이메일 알림
- **Owner**: 박상준 차장
- **Status**: Open — Phase 5 착수 전 필수
- **예상 구현 시간**: 1~2시간

### R5. CS 경유 오프라인 전환 미반영 🟡 **High (구조적)**
- **설명**: 사인물 업종 특성상 CS/전화/카톡 주문 비중이 큼. 온라인 전환 0건이어도 매출 존재. AI가 "실적 없음 → 소재 OFF 또는 입찰 인하" 제안 시 오판 가능.
- **카테고리**: Strategic / Operational
- **Likelihood / Impact**: High (상시 발생) / Medium (케이스별 수십만원 매출 손실 가능)
- **Mitigation (Accept with controls)**:
  1. LLM 프롬프트에 "CS 주문 가능성" 명시 (기존 반영 여부 확인)
  2. 소재 OFF·입찰 인하 제안은 CS 확인 후 수동 승인
  3. 월 1회 CS 매출 vs 온라인 전환 교차 분석
  4. 장기: CRM/주문관리 연동으로 CS 매출 자동 반영
- **Owner**: 박상준 차장 + CS팀
- **Status**: Accepted (구조적, 완전 제거 불가)

### R6. 자격증명 노출 🔴 **High**
- **설명**: 최근 세션에서 GitHub PAT와 네이버 API 키가 대화창에 직접 입력된 이력 있음. 대화·메모리 기록에 남아 있을 가능성.
- **카테고리**: Security
- **Likelihood / Impact**: Medium / High (광고비 도용 또는 리포지토리 접근 피해)
- **Mitigation**:
  1. 즉시 폐기: 과거 PAT `ghp_deFq...`, 이식용 PAT `ghp_FhO05...`, 점검 세션에 사용한 네이버 API Key/Secret
  2. 이후 자격증명은 **n8n Credential 등록** 또는 **환경변수**로만 사용, 대화창에 직접 붙여넣지 않음
  3. 월 1회 자격증명 로테이션 (PAT 90일·API 키 180일)
- **Owner**: 박상준 차장
- **Status**: Open — 오늘~주말 내 폐기 필요

### R7. Google OAuth 토큰 만료 🟡 **Medium**
- **설명**: n8n의 Google Sheets 노드가 OAuth 토큰 만료로 "permission denied" 리턴 → 시트 기록 일시 중단.
- **카테고리**: Operational
- **Likelihood / Impact**: Medium (주기적) / Medium (최대 하루 수집 데이터 누락)
- **Mitigation**:
  1. n8n Credential에 Service Account 방식 병행 고려
  2. 실패 시 재시도 로직 (최대 3회)
  3. 일일 09:30에 시트 기록 유무 자동 체크 → 없으면 알림
- **Owner**: 박상준 차장
- **Status**: Open — Phase 5 착수 후 모니터링

### R8. LLM 무한루프 / JSON 파싱 오류 🟢 **Low**
- **설명**: Analyst→Strategist→Critic→Verifier 4단계에서 Critic이 Strategist를 계속 반박하거나, LLM 응답에 마크다운·주석 섞여 JSON 파싱 실패.
- **카테고리**: Operational
- **Likelihood / Impact**: Low (v6~v9 디버깅 완료) / Medium (해당 일 리포트만 실패)
- **Mitigation**:
  1. System prompt에 "Return JSON only, no markdown" 명시
  2. Verifier에 max iteration = 2 가드 이미 적용 여부 확인
  3. 실패 시 전일 리포트로 대체 + 알림
- **Owner**: 박상준 차장
- **Status**: Mitigated (추가 모니터링만)

### R9. 입찰가 과다 변경으로 일일 광고비 급증 🟠 **Medium-High**
- **설명**: AI가 "순위 회복 필요"로 동시에 여러 소재 입찰가를 큰 폭 인상 → 일일 광고비 예산 초과.
- **카테고리**: Financial
- **Likelihood / Impact**: Low (가드레일 없어도 건수 적음) / High (일일 수십만원 초과 가능)
- **Mitigation**: R4와 동일한 가드레일로 커버. 추가로 광고 관리자 일일 예산 한도(네이버 콘솔) 병행 설정 권장.
- **Owner**: 박상준 차장
- **Status**: Open — R4 구현 시 동시 해결

### R10. n8n Cloud 플랫폼 자체 장애 🟢 **Low**
- **설명**: hanasignmall.app.n8n.cloud 서비스 중단.
- **카테고리**: Operational (외부 의존)
- **Likelihood / Impact**: Low / Medium
- **Mitigation**:
  1. 워크플로우 JSON 정기 백업 (GitHub 리포 `backups/`)
  2. Self-hosted n8n으로 이관 옵션 검토 (분기 1회)
- **Owner**: 박상준 차장
- **Status**: Accepted (현재는 외부 의존 유지)

### R11. 웹팀 5명 모니터링 부담 🟡 **Medium**
- **설명**: Phase 5 가동 후 일일 대시보드·승인 요청·알림이 쌓여 웹팀 부담 증가. 박상준 차장 1인 병목화 우려.
- **카테고리**: Operational / Strategic
- **Likelihood / Impact**: Medium / Medium
- **Mitigation**:
  1. 일일 리포트에 "사람 판단 필요" 항목만 TOP 3 표시, 나머지는 자동 승인
  2. 주 1회 팀원(홍재이 주임·임정민 주임)에게 요약 공유
  3. 승인 대기 48시간 미처리 건은 자동 보류 → 박상준 차장 알림
- **Owner**: 박상준 차장
- **Status**: Open — Phase 5 착수 시 함께 설계

### R12. 네이버 API 스키마 변경 🟡 **Medium**
- **설명**: 네이버 검색광고 API 필드·경로·응답 구조 변경으로 PUT/GET 실패.
- **카테고리**: Operational (외부 의존)
- **Likelihood / Impact**: Low (현행 API 유지 가능성 높음) / High (전체 자동화 중단)
- **Mitigation**:
  1. 분기 1회 API 문서 변경사항 체크 (공지사항 구독)
  2. PUT 호출 실패율 모니터링 (10분 내 3회 실패 시 알림)
  3. 백업 파이프라인(수동 승인 경로) 워크플로우 보존
- **Owner**: 박상준 차장
- **Status**: Open — 분기 점검 루틴화

---

## 3. 우선순위별 조치 일정

### 이번 주 (2026-04-18~19)
- [ ] R1: 런북 Step 1~5 실행 → E2E 파이프라인 재가동
- [ ] R2: 05_실행로그 Append 노드 매핑 확인
- [ ] R6: 자격증명 3종 폐기 + 대체

### 다음 주 (2026-04-20~26)
- [ ] R3: 롤백 Webhook 구현 + 05_실행로그에 원복링크 컬럼 추가
- [ ] R4: 가드레일 Function 노드 3종 추가
- [ ] R9: R4 구현 검증 + 네이버 콘솔 일일 예산 상한 점검

### 다다음 주 이후 (Phase 5 착수)
- [ ] R5: LLM 프롬프트 "CS 주문 가능성" 명시 재점검
- [ ] R7: OAuth 만료 대응 로직 추가
- [ ] R11: 승인 대기 48h 자동 알림 설계
- [ ] R12: 분기 API 점검 루틴 추가

---

## 4. 수용(Accept) 리스크 명시

**R5 (CS 오프라인 전환 미반영)** 과 **R10 (n8n Cloud 플랫폼 장애)** 는 **Accept with controls**.
- R5: 업종 구조상 완전 제거 불가. 프롬프트·수동 승인으로 2차 방어망 유지.
- R10: 외부 의존. 백업·Self-hosted 옵션만 예비 보유, 상시 대응은 포기.

---

## 5. 다음 재평가 일정

- **2026-04-24 (D+7)**: R1·R2·R6 상태 재평가. 해결 안 됐으면 Phase 5 착수 연기.
- **2026-05-01 (D+14)**: R3·R4·R9 구현 완료 여부 재평가. Phase 5 Go/No-Go 판단.
- **2026-05-01 이후 매 분기**: R10·R12 외부 의존 리스크 점검.

---

## 6. 핵심 요약 + 지금 바로 할 일

### 핵심 요약
- **Critical 1건, High 5건, Medium 4건, Low 2건.**
- Phase 5 착수 전 **R1 / R3 / R4** 최소 3건 해결 필요.
- R6(자격증명 노출)은 오늘~주말 내 폐기, 기술 리스크와 별개로 보안 리스크라 즉시 처리.

### 지금 바로 할 일 (우선순위)
1. **자격증명 3종 폐기** (PAT 2개 + 네이버 API 키) — 오늘 밤 내
2. 월요일 런북 실행 (R1·R2 동시 해결)
3. 다음 주 R3·R4 구현 착수

*끝.*
