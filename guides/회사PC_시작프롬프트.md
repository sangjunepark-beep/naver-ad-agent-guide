# 회사 PC 시작 프롬프트 — 네이버검색광고 에이전트 프로젝트

> **마지막 업데이트**: 2026-04-19 (집 PC 세션 종료 시점)
> **현재 진행상태**: Phase 1~5-4 완료. 상품링크 수정 완료. 다음: 롤백 Webhook(R3), 가드레일(R4), 임시 워크플로우 정리

---

## ✅ 오늘(2026-04-19) 완료한 작업 요약

| 작업 | 결과 |
|------|------|
| 상품매핑 D열 full URL 입력 | 2208개 완료 (hanasign 1899 + thecorrectsign 238 + 빈값 71) |
| pLink 코드 수정 | D열 URL 직접 사용 방식으로 변경 (nvMid 오류 완전 해소) |
| 테스트 이메일 발송 | jimrn22@gmail.com INBOX 도착 확인 ✅ |
| 메모리·TASKS.md 업데이트 | 완료 |

---

## A. 회사 PC 최초 1회 — 스크립트 + 메모리 동시 설치

> 신규 회사 PC이거나, 기존 `sync_memory.sh` 가 사라졌을 때.
> Private 리포면 `[PAT]` 자리에 실제 토큰 입력 후 복붙.

```
아래 작업 순서대로 해줘:

1. 회사 PC 워크스페이스 폴더 경로 확인 (/sessions/*/mnt/ 아래)
2. GitHub 리포 sangjunepark-beep/naver-ad-agent-guide 에서 sync_memory.sh 를
   워크스페이스 폴더에 다운로드
   (Private이면 토큰 사용: GH_TOKEN=[PAT])
3. chmod +x sync_memory.sh
4. bash sync_memory.sh pull 실행 (GitHub → .auto-memory 복원)
5. bash sync_memory.sh check 로 숫자 확인
6. "나 누구야?" / "지금 프로젝트 어디까지 진행됐어?" 두 질문으로 복원 검증
```

---

## B. 회사 PC 일상 시작 — 메모리만 최신화

> `sync_memory.sh` 가 이미 워크스페이스 폴더에 있는 경우.

**Public 리포일 때:**
```
워크스페이스의 sync_memory.sh pull 실행해서
.auto-memory 최신으로 땡기고, check로 숫자 확인해줘.
```

**Private 리포일 때:**
```
GH_TOKEN=[PAT] 로 워크스페이스의 sync_memory.sh pull 실행해서
.auto-memory 최신으로 땡기고, check로 숫자 확인해줘.
```

---

## C. 회사 작업 종료 — 메모리 GitHub에 push

> 작업 끝내고 집으로 돌아가기 전. **반드시 실행**.

```
GH_TOKEN=[PAT] 로 워크스페이스의 sync_memory.sh push 실행해서
현재 .auto-memory를 GitHub 리포에 반영해줘.
결과 성공/실패 숫자 알려줘.
```

---

## D. 집↔회사 동기화 리듬

| 시점 | 명령 | PAT 필요? |
|------|------|-----------|
| 회사 출근 / 세션 시작 | `sync_memory.sh pull` | Private일 때만 |
| 작업 진행 (자동) | (Claude가 .auto-memory 자동 갱신) | — |
| 퇴근 / 세션 종료 | `sync_memory.sh push` | 항상 필요 |
| 집 도착 / 세션 시작 | `sync_memory.sh pull` | Private일 때만 |
| 취침 / 세션 종료 | `sync_memory.sh push` | 항상 필요 |

---

## E. 다음 할 일 (우선순위 순)

### 1. 임시 워크플로우 정리 (n8n) — 10분
- `XquBGKrgVVWVUTyN` (D열 업데이트용 Webhook) → 삭제
- `1RFPrHhg7cpchpxg` (테스트 이메일 발송용) → 삭제
- hanasignmall.app.n8n.cloud/workflows 에서 직접 삭제

### 2. 메일 링크 최종 클릭 확인 — 5분
- jimrn22@gmail.com에서 받은 테스트 이메일 열기
- 상품명 클릭 → 스마트스토어 상품 페이지 정상 이동 확인
- hanasign, thecorrectsign 2개 스토어 각 1개씩 확인

### 3. 메인 파이프라인 수동 실행 + 시트 확인 — 20분
- "네이버 검색광고 에이전트_파이프라인" Active ON 확인
- Execute Workflow 수동 실행 1회
- 01_일일수집로그 / 03_이상치로그 / 04_제안기록 행 추가 확인

### 4. R3 롤백 Webhook 구현 — 2~3시간
- Phase4_승인_자동반영 워크플로우에 "변경 전 bidAmt" 저장 필드 추가
- 별도 "1-클릭 원복 Webhook" 워크플로우 신규 구축
- 05_실행로그에 "원복링크" 컬럼 추가

### 5. R4 가드레일 Function 노드 — 1~2시간
- 일일 변경 건수 상한 (기본 10건)
- 변경폭 상한 (±20% 초과 차단)
- 중복 승인 방지 (동일 제안ID 재승인 거부)

---

## F. 현재 시스템 현황

| 항목 | 현황 |
|------|------|
| n8n | hanasignmall.app.n8n.cloud |
| 메인 워크플로우 | 네이버 검색광고 에이전트_파이프라인 |
| Webhook 워크플로우 | Phase4_승인_자동반영 |
| 구글 시트 | 하나사인몰 광고 에이전트 (ID: 1Yuw_8we4nEzL1nslHI66LHBBE_uWc-ErALzhn2vvLGI) |
| n8n API Key | exp≈2026-05-14 (만료 시 /settings/api에서 재발급) |
| Gmail OAuth2 credential | OX8fWhLUH25y3IGX |
| Google Sheets credential | HjfwX5DgD4iXkptZ |
| 상품매핑 D열 | full URL 2208개 입력 완료 (2026-04-19) |

---

## G. 체크리스트 — 회사 복귀 첫날

- [ ] 새 PAT 발급 완료 (https://github.com/settings/tokens, repo 권한)
- [ ] 기존 노출된 PAT 2개 폐기 (`ghp_deFq...`, `ghp_FhO05...`) → GitHub Settings → Revoke
- [ ] 네이버 검색광고 API Secret 재발급 (광고 관리자 → API 관리)
- [ ] 회사 PC Cowork에 user_preferences, project_instructions 이식
- [ ] 회사 PC에서 위 **A 프롬프트** 실행 (스크립트 + 메모리 한 번에 복원)
- [ ] "나 누구야?" / "지금 프로젝트 어디까지 진행됐어?" 검증
- [ ] 임시 워크플로우 2개 삭제 (E.1 참조)
- [ ] 메일 링크 클릭 확인 (E.2 참조)
- [ ] 메인 파이프라인 수동 실행 확인 (E.3 참조)

---

## H. 문제 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| pull 시 HTTP 404 | 리포가 Private인데 PAT 누락 | `GH_TOKEN=ghp_xxx` 앞에 붙이기 |
| pull 시 HTTP 401 | PAT 만료/오입력 | https://github.com/settings/tokens 에서 새 PAT 발급 |
| push 시 HTTP 422 | 파일 SHA 불일치 (동시 편집) | pull 먼저 실행 후 재시도 |
| .auto-memory 경로 못 찾음 | 세션명 변경 | `ls /sessions/*/mnt/` 로 확인 |
| Claude가 메모리 못 읽음 | 세션 재시작 안 함 | Cowork 새 대화 열기 |
| 상품링크 오류 "상품이 존재하지 않습니다" | nvMid ≠ smartstore productNo | D열 full URL로 이미 수정 완료. 재발 시 스마트스토어 CSV 재업로드 |

---

**관련 리포**: https://github.com/sangjunepark-beep/naver-ad-agent-guide
