# 회사 PC 시작 프롬프트 템플릿

네이버검색광고 에이전트 프로젝트 — 회사 Cowork 새 대화 열 때 복붙용 프롬프트 모음.

**전제**: `sync_memory.sh` 가 GitHub 리포(`naver-ad-agent-guide`)에 올라와 있어야 합니다.

---

## A. 회사 PC 최초 1회 — 스크립트 + 메모리 동시 설치

> 신규 회사 PC이거나, 기존 `sync_memory.sh` 가 사라졌을 때. Private 리포면 `[PAT]` 자리에 실제 토큰 입력 후 복붙.

```
아래 작업 순서대로 해줘:

1. 회사 PC 워크스페이스 폴더 경로 확인 (/sessions/*/mnt/ 아래)
2. GitHub 리포 sangjunepark-beep/naver-ad-agent-guide 에서 sync_memory.sh 를
   워크스페이스 폴더에 다운로드
   (Private이면 토큰 사용: GH_TOKEN=[PAT])
3. chmod +x sync_memory.sh
4. bash sync_memory.sh pull 실행 (GitHub → .auto-memory 15개 복원)
5. bash sync_memory.sh check 로 15/15 확인
6. 마지막에 "나 누구야?" / "지금 프로젝트 어디까지 진행됐어?" 두 질문 답해서 복원 검증
```

---

## B. 회사 PC 일상 시작 — 메모리만 최신화

> `sync_memory.sh` 가 이미 워크스페이스 폴더에 있는 경우. 매번 새 대화 열 때 사용.

**Public 리포일 때:**
```
워크스페이스의 sync_memory.sh pull 실행해서
.auto-memory 최신으로 땡기고, check로 15/15 확인해줘.
```

**Private 리포일 때:**
```
GH_TOKEN=[PAT] 로 워크스페이스의 sync_memory.sh pull 실행해서
.auto-memory 최신으로 땡기고, check로 15/15 확인해줘.
```

---

## C. 회사 작업 종료 — 메모리 GitHub에 push

> 회사에서 작업 끝내고 집으로 돌아가기 전. **반드시 실행**해야 집에서 이어서 작업 가능.

```
GH_TOKEN=[PAT] 로 워크스페이스의 sync_memory.sh push 실행해서
현재 .auto-memory 15개를 GitHub 리포에 반영해줘.
결과 성공/실패 숫자 알려줘.
```

---

## D. 집↔회사 동기화 일상 리듬

| 시점 | 명령 | PAT 필요? |
|------|------|-----------|
| 회사 출근 / 세션 시작 | `sync_memory.sh pull` | Private일 때만 |
| 작업 진행 (자동) | (Claude가 .auto-memory 자동 갱신) | — |
| 퇴근 / 세션 종료 | `sync_memory.sh push` | 항상 필요 |
| 집 도착 / 세션 시작 | `sync_memory.sh pull` | Private일 때만 |
| 취침 / 세션 종료 | `sync_memory.sh push` | 항상 필요 |

---

## E. 체크리스트 — 회사 복귀 첫날

- [ ] 새 PAT 발급 완료 (https://github.com/settings/tokens, repo 권한)
- [ ] PAT를 1Password/메모장 등 안전한 곳에 보관
- [ ] 회사 PC Cowork에 user_preferences, project_instructions 이식 (가이드 STEP 1~2)
- [ ] 회사 PC에서 위 **A 프롬프트** 실행 (스크립트 + 메모리 한 번에 복원)
- [ ] "나 누구야?" / "지금 프로젝트 어디까지 진행됐어?" 질문으로 검증
- [ ] Phase 5 작업 재개

---

## F. 문제 해결

| 증상 | 원인 | 해결 |
|------|------|------|
| pull 시 HTTP 404 | 리포가 Private인데 PAT 누락 | `GH_TOKEN=ghp_xxx` 앞에 붙이기 |
| pull 시 HTTP 401 | PAT 만료/오입력 | https://github.com/settings/tokens 에서 새 PAT 발급 |
| push 시 HTTP 422 | 파일 SHA 불일치 (동시 편집) | pull 먼저 실행 후 재시도 |
| .auto-memory 경로 못 찾음 | 세션명 변경 | 스크립트 수정 없이 동작해야 정상. 오류 시 `ls /sessions/*/mnt/` 로 확인 |
| Claude가 메모리 못 읽음 | 세션 재시작 안 함 | Cowork 새 대화 열기 (기존 대화는 캐시된 상태) |

---

**작성일**: 2026-04-16
**관련 리포**: https://github.com/sangjunepark-beep/naver-ad-agent-guide
