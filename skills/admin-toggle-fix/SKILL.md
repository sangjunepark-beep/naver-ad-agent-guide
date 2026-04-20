---
name: admin-toggle-fix
description: "하나사인몰 어드민(ad.hanasm.kr)에서 상품의 업종별/상품별 카테고리 체크박스를 브라우저 MCP로 감사(audit)하고 일괄 토글 수정하는 스킬. '업종별 공간 체크', '공간별 수정', '업종별 카테고리 정리', '과태깅 정리', '체크박스 해제', '입간판 공간별', '어드민 카테고리 감사', '토글 수정', '신규몰 체크박스', '어드민 체크 정리' 등 하나사인몰 어드민에서 체크박스를 읽거나 수정하는 모든 요청 시 반드시 이 스킬을 먼저 읽으세요."
---

# 하나사인몰 어드민 토글수정 스킬 (멀티모델 v2)

## 개요

하나사인몰 어드민(ad.hanasm.kr) 상품 편집 페이지의 체크박스를 읽고, 판단하고, 수정하는 워크플로우.

**v2 핵심 변경:** 작업 성격에 따라 모델을 분담해 비용을 최대 1/7로 절감.

---

## 모델 분담 매트릭스 (필독)

| 작업 | 담당 모델 | 서브에이전트 파일 | 이유 |
|------|-----------|------------------|------|
| 전체 오케스트레이션, 예외 상품 판단 | **Opus (메인)** | — | 한국어 문맥, 특수 상품 판정 |
| 상품명 → 과태깅/정상/미연결 분류 | **Sonnet** | `subagents/judgment-advisor.md` | 판단 필요하지만 Opus 불필요 |
| Excel 리포트 생성 | **Sonnet** | `subagents/judgment-advisor.md` | pandas 구조화 작업 |
| 페이지 감사 (체크박스 읽기) | **Haiku** | `subagents/audit-worker.md` | 고정 JS 반복 실행 |
| 업종 9회 연결 (리로드 루프) | **Haiku** | `subagents/industry-connector.md` | 완전 반복 패턴 |
| 체크박스 배치 .click() 수정 | **Haiku** | `subagents/toggle-executor.md` | 단순 실행 |

**규칙:** 판단이 필요 없는 반복 작업은 반드시 Haiku 서브에이전트로 위임할 것.
판단이 애매한 상품(안전안내, 법령표기, 시설안내 등 특수 상품)만 Opus가 직접 처리.

---

## 어드민 구조 핵심

### 상품 편집 URL
```
https://ad.hanasm.kr/AdminManager/MakeGoodsTypeOneDp.php?RgrCode={RgrCode}&EditMode=1
```

### 체크박스 value 형식
```
{업종scode}`{optType}`{subMain}-{subDetail}`{명칭}
```
예: `03`2`05-02`커뮤니티시설`

### 업종 코드
01=학교/학원, 02=식당/카페, 03=아파트, 04=호텔/펜션, 05=병원/요양시설,
06=회사/공장, 07=공공기관, 08=헬스/레저, 09=기타업종

---

## 핵심 규칙 3가지 (Haiku 서브에이전트도 준수)

### 규칙 1: 헤더 기준 체크박스 분리
업종별 카테고리 헤더 뒤에 위치한 체크박스만 필터링.
→ 스크립트: `scripts/audit.js` 참조

### 규칙 2: 수정은 반드시 .click()
`FnSelOptChk()` 직접 호출 금지. DOM 상태 토글 없이 AJAX만 날아가서 역방향 저장됨.
→ 스크립트: `scripts/batch_click.js` 참조

### 규칙 3: 대량 수정은 배치 처리
1배치 = 최대 30개, 간격 = 150ms. 완료 후 새로고침 → 재검증.
→ 스크립트: `scripts/batch_click.js` 참조

---

## 전체 워크플로우

### A. 감사 (읽기만) — Haiku 위임
1. RgrCode 목록 수집 (Opus가 페이지 목록에서 추출)
2. **→ Haiku 서브에이전트(audit-worker) 호출** — `subagents/audit-worker.md` 참조
3. 결과 JSON 수신
4. Opus가 예외 상품 체크 (특수 상품 판단)

### B. 판단 (과태깅/정상/미연결 분류) — Sonnet 위임
1. 감사 결과 + 상품명 목록 준비
2. **→ Sonnet 서브에이전트(judgment-advisor) 호출** — `subagents/judgment-advisor.md` 참조
3. Excel 리포트 생성 포함

### C. 업종 미연결 상품 연결 — Haiku 위임
1. 업종 미연결 목록 확인
2. **→ Haiku 서브에이전트(industry-connector) 호출** — `subagents/industry-connector.md` 참조

### D. 체크박스 수정 — 사람 승인 후 Haiku 위임
1. Opus가 변경 리포트 작성 (수정 전 dry-run)
2. **사람(박상준 차장)에게 승인 받기** — 이 단계는 반드시 Opus가 직접 처리
3. 승인 후 **→ Haiku 서브에이전트(toggle-executor) 호출** — `subagents/toggle-executor.md` 참조

---

## 서브에이전트 호출 방법 (Cowork 기준)

```
Task(Agent) 도구 사용:
- subagent_type: "general-purpose"
- model: "haiku"  (또는 "sonnet")
- prompt: 해당 subagents/*.md 파일 내용 + 구체적 작업 지시
```

서브에이전트에 항상 포함할 정보:
- RgrCode 목록 (또는 단일 RgrCode)
- 작업 범위 (몇 번째 ~ 몇 번째)
- 결과 저장 경로

---

## Prompt Caching 설정 (API 자동화 시)

이 SKILL.md와 JS 스크립트는 반복 호출 시 캐싱 대상.
Python API 연동 방법은 `references/python-automation.md` 참조.

---

## 주의사항

| 항목 | 내용 |
|------|------|
| FnSelOptChk 직접 호출 | **금지** |
| 수정 전 승인 | **필수** — Opus가 리포트 작성 후 사람 확인 |
| 탭 끊김 대비 | tabs_context_mcp로 상태 수시 확인 |
| 업종 비어있는 상품 | industry-connector 서브에이전트 위임 |
| 특수 상품 (안전/법령) | Haiku 판단 금지 → Opus 직접 처리 |
