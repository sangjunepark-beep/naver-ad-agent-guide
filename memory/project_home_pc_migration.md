---
name: 집 PC Cowork 이식 완료 + 동기화 체계 구축
description: 2026-04-16 집 PC에 auto-memory 15개 복원 완료. GitHub 리포 기반 pull/push 동기화 스크립트 구축.
type: project
---
**집 PC Cowork 이식 완료** (2026-04-16 밤)

## 완료된 작업
- 집 PC `.auto-memory/` 에 GitHub 리포 `naver-ad-agent-guide` 의 `memory/*.md` 15개 복원
- 검증 3종 질문(나 누구야 / 프로젝트 진행도 / 네이버 콘솔 전환매출 주의점) 모두 통과
- 집 ↔ 회사 양방향 동기화 체계 구축

## 구축된 파일
- `scripts/sync_memory.sh` (GitHub 리포) — pull/push/check 3개 서브커맨드
- `guides/회사PC_시작프롬프트.md` (GitHub 리포) — 회사 PC 복귀 시 사용할 프롬프트 템플릿

## 동기화 규칙
- 세션 시작: `bash sync_memory.sh pull`
- 세션 종료: `GH_TOKEN=ghp_xxx bash sync_memory.sh push`
- PAT는 환경변수로만 주입 (하드코딩 금지)
- 회사↔집 동시 편집 금지 (나중에 push한 쪽이 덮어씀)

## 보안 메모 (2026-04-16)
- 과거 노출된 PAT `ghp_deFq...` → 폐기 필요
- 이식 작업용 PAT `ghp_FhO05...` → 작업 완료 후 폐기 필요
- 향후 PAT는 대화창에 절대 노출 금지

**Why:** 회사/집 Cowork 환경에서 동일 메모리/지침/프로젝트 맥락 유지를 위함. 공식 동기화 기능이 없어서 GitHub 리포 기반 수동 동기화가 현실적 해법.

**How to apply:** 새 세션 시작 시 sync_memory.sh pull부터 실행. 작업 종료 전 push. 메모리 파일 추가 시 sync_memory.sh의 FILES 배열도 함께 갱신.
