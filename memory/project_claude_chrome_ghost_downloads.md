---
name: Claude in Chrome 유령 다운로드 원인 특정
description: Downloads에 data.csv·json.txt 반복 생성 → 사무실 PC에서 시작된 Cowork 세션이 Claude 확장 통해 현재 PC 브라우저 제어하던 것. 크로스 디바이스 세션 영향
type: project
originSessionId: 35d08f6a-12fd-40ba-9cd3-904848f3b709
---
**사실**: 2026-04-24 오후 차장님 PC Downloads에 `data (1).csv`, `data (1).xlsx`, `json (1).txt`, `json.txt` 같은 파일이 반복 생성됨. 파일명 `(N)` 패턴은 같은 이름 반복 다운로드 시 브라우저 자동 넘버링. `json.txt`의 내용은 gviz `access_denied` 응답 = 누군가 gviz URL을 권한 없는 상태로 반복 호출 중이라는 신호.

**원인**: 브라우저 상단 파란 배너 "`'Claude'에서 이 브라우저에 대한 디버깅을 시작함`" + 탭 목록에 "Review Google Sheets" 탭 → Claude in Chrome 확장이 브라우저를 제어 중. 확인 결과 **사무실 PC에서 이전에 시작한 Cowork 로컬 에이전트 세션이 Anthropic 서버에 살아있었고, 같은 계정으로 로그인된 현재 PC의 Chrome 확장으로 명령이 라우팅**되고 있었던 것.

**Why**: Cowork는 세션을 UI 종료와 별개로 서버측에 유지할 수 있음. 특히 `C:\Users\Administrator\AppData\Roaming\Claude\local-agent-mode-sessions\...` 경로의 로컬 에이전트 모드는 사무실 PC 전원 끄기로 로컬 프로세스는 죽어도 서버측 세션 상태는 남을 수 있음. Claude in Chrome 확장은 브라우저 기반이라 같은 계정 로그인된 **다른 PC의 브라우저로도 명령 전달 가능**.

**How to apply**:
- 해결: 사무실 PC 크롬 로그아웃 + 해당 세션 전체 삭제로 근본 차단됨
- 예방: (1) 작업 끝나면 Claude 앱 종료 전 세션 먼저 닫기 (2) 공용 PC/기기에서 Cowork 쓸 땐 크롬 로그아웃 확인 (3) 브라우저 확장을 쓸 때만 켜기 (`chrome://extensions/`) (4) 주기적으로 `local-agent-mode-sessions` 폴더 정리
- 의심 시 진단: (a) Cowork `list_sessions`에 running/idle 세션 확인 (b) 작업관리자 Claude.exe 프로세스 개수 (c) 브라우저 상단 Claude 디버깅 배너 (d) `chrome://downloads/` 에서 출처 URL 확인
