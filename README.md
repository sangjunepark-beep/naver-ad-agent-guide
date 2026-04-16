# naver-ad-agent-guide

하나사인몰 **네이버검색광고 에이전트 빌드** 프로젝트의 지침·메모리·워크플로우·리포트 통합 백업 리포지토리.

Cowork(Claude) 세션 간 컨텍스트를 유지하고, 프로젝트 복구/인수인계 시 참조용으로 사용합니다.

---

## 📁 리포 구조

```
/
├─ README.md                    ← 본 문서
├─ guidelines/                  ← 사용자·프로젝트 지침
│   ├─ user_preferences.md      하나사인몰/웹팀 배경, 답변 원칙·스타일
│   └─ project_instructions.md  프로젝트 목적, Phase 진행, 제약사항
├─ memory/                      ← auto-memory 15개
│   ├─ MEMORY.md                인덱스
│   ├─ project_*.md             프로젝트 상태·결정사항
│   ├─ feedback_*.md            사용자 피드백/규칙
│   └─ reference_*.md           외부 시스템 참조
├─ workflows/                   ← n8n 워크플로우 JSON
│   ├─ Phase3_final.json        LLM 교차검증 파이프라인
│   ├─ Phase3.5_final.json      리포트 고도화 (대시보드 HTML)
│   ├─ Phase4_final.json        메인 파이프라인 (승인 링크 포함)
│   └─ Phase4_approve_webhook.json  승인→자동반영 Webhook
└─ reports/                     ← 결과물 HTML
    ├─ interim_report_0415.html 중간보고서
    ├─ daily_report_sample.html 일일리포트 샘플
    └─ pipeline_diagram.html    전체 파이프라인 다이어그램
```

## 📊 프로젝트 현황 (2026-04-16 기준)

| Phase | 내용 | 상태 |
|-------|------|------|
| 1 | 캠페인 목록 수집 | ✅ 완료 |
| 2-A | AD 리포트 수집 | ✅ 완료 |
| 2-B | 전환 리포트 수집 | ✅ 완료 |
| 3 | LLM 교차 검증 | ✅ 완료 |
| 3.5 | 리포트 고도화 | ✅ 완료 |
| 4 | 승인→자동반영 | ✅ 완료 (실제 입찰가 변경 검증) |
| 5 | 사후 ROAS 피드백 | ⬜ 미착수 |

## 🔄 다음 세션에서 이어받는 방법

이 리포의 메모리는 Cowork auto-memory 시스템의 **스냅샷**입니다. 실제 동작하는 메모리는 Cowork 로컬에서 로드되며, 이 리포는 백업/참조용입니다.

### 세션 컨텍스트 복구 절차

1. 새 Cowork 세션 시작
2. 필요 시 이 리포 URL을 공유하면 Claude가 내용 참조 가능
3. 또는 `memory/MEMORY.md` + `memory/project_overall_progress.md` 붙여넣기로 맥락 요약 전달

### 권장 참조 순서

| 순번 | 파일 | 용도 |
|------|------|------|
| 1 | `guidelines/user_preferences.md` | 톤·스타일·배경 이해 |
| 2 | `guidelines/project_instructions.md` | 프로젝트 목적 이해 |
| 3 | `memory/project_overall_progress.md` | 전체 진행 현황 |
| 4 | `memory/project_phase4_done.md` | 최신 완료 상태 |
| 5 | `memory/project_naver_shopping_ad_api_quirks.md` | API 특이사항 |

## 🔧 n8n 운영 환경

- **도메인**: `hanasignmall.app.n8n.cloud`
- **메인 파이프라인**: "네이버 검색광고 에이전트_파이프라인"
- **Webhook**: "Phase4_승인_자동반영" (실운영 중)

## 📑 구글 시트

"하나사인몰 광고 에이전트" 시트에 전체 데이터 집계:
- 00_시트안내, 01_일일수집로그, 상품매핑, 02_전환수집로그
- 03_실_ROAS_대시보드, 03_이상치로그, 04_제안기록, 05_실행로그

## ⚠️ 주요 제약사항

1. **네이버 광고 콘솔 전환매출은 실매출의 약 5배** — `구매전환매출` 컬럼 사용
2. **CS 경유 오프라인 전환 비중 큼** — 온라인 전환 0건 ≠ 매출 0
3. **쇼핑검색광고 API PUT**: `type`/`nccAdId` 필수, `bidAmt` 10원 단위
4. **n8n은 JSON import 방식** — 브라우저 조작 금지

## 🚀 다음 할 일 (Phase 5)

1. 사후 ROAS 자동 측정 로직
2. 효과 판정 규칙 정의
3. 실패 학습 루프
4. 전체 가동 스케줄 확정

---

**마지막 동기화**: 2026-04-16
**관리자**: 박상준 차장 (웹팀 총괄)
