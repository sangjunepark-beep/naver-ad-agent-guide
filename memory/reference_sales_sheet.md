---
name: 하나사인몰 CS/영업 매출 시트 (읽기 전용)
description: 진행건 기준 주문 원장. 진행자 "영호"=영업매출, 그 외=CS매출. 광고 ROAS는 CS만 포함, 영업은 참조용
type: reference
originSessionId: 6d1b954e-cc6c-4309-8ced-effc48f4c987
---
**Spreadsheet ID**: `169BTstGNSOPxx0aKglV2sTb_zhZWEfW1KTcht-K3afA`
**기본 gid**: `1952467949`
**실제 Sheet Tab 이름**: `업체계약현황` ★★ (n8n 캐시 "현황"은 오래된 값. Sheets API에는 "업체계약현황"으로 요청해야 함)
**Sheet dimension**: rows=32687, cols=28 (확인 2026-04-21)
**URL**: https://docs.google.com/spreadsheets/d/169BTstGNSOPxx0aKglV2sTb_zhZWEfW1KTcht-K3afA/edit?gid=1952467949

## ⛔ 쓰기 금지 (2026-04-20 사용자 지시)
- n8n Google Sheets 노드는 **read/query만**, append/update/delete 절대 금지
- 수식 수정, 포맷 변경, 컬럼 추가 모두 금지

## 시트 구조 (20 컬럼, 약 32,687행 · 누적)
| 컬럼 | 의미 |
|---|---|
| 년 / 월 / 일 | **진행건 기준 입력일** (날짜 집계 기준으로 이거 사용) |
| 진행자 | `사인몰(영호)` = 영업매출, 그 외 = CS매출 |
| 견적서 | 견적서 발행일 (참고) |
| 발행날짜 | 세금계산서 발행일 |
| 세금/현영 | 세금계산서 or 현금영수증 |
| 아파트 | 고객 타입 (아파트/학교/개인 등) |
| 담당 | 제작 담당자 |
| 제목/상호 | 고객명 |
| 품명 | 제품 |
| **총 금액** | **주문 금액 (합산 대상)** ★ Q열 (col index 16) |

## 진행자 값 → 채널 매핑 (2026-04-20 사용자 확정)

| 진행자 값 | 채널 | 분류 |
|---|---|---|
| `사인몰(영호)` | 영업 수주 | **영업 매출** — 광고 무관, 리포트 ROAS 제외, 참조 표시 |
| `사인몰(영호 제외)` (민주/경민/혜리/사랑 등) | 전화·카톡·견적 접수 | **CS 매출** — 광고 기여 가능성, 매칭 불가 |
| `스마트스토어` | 네이버 스마트스토어 | **스마트스토어 전체** — 광고 매출(02 로그) + 자연 유입 매출 포함 |
| `고도몰5` | 자사몰 (hanasignmall.com) | 자사몰 · 광고 무관 |
| `신규몰` | 자사몰 (hanasignmall.kr) | 자사몰 · 광고 무관 |
| `쿠팡(신)` | 쿠팡 | 오픈마켓 · 광고 무관 |
| `G마켓` | G마켓 | 오픈마켓 · 광고 무관 |
| (기타 신규 진행자) | — | 신규 파악 시 규칙 업데이트 |

- 날짜 기준은 `년/월/일` (시스템 입력일 = 진행건 기준)
- **네이버 검색광고 ROAS 계산에 직접 반영**되는 것은 **02_전환수집로그(광고 경유 결제)만**

## 리포트 연결 규칙
- **실 ROAS** = (온라인 스마트스토어 매출 + CS 매출) ÷ 광고비
- **영업 매출(영호)** = 리포트에 참조용 별도 섹션으로 표시, ROAS 계산 미포함

## n8n 연결 방식 (2026-04-21 확정)
- **httpRequest 노드 + Sheets API batchGet** 사용 (googleSheets 노드는 25K rows에서 OOM)
- URL: `https://sheets.googleapis.com/v4/spreadsheets/{id}/values:batchGet`
- ranges: `업체계약현황!A1:Q2000` (최근 2000행만, 최신→오래 순)
- valueRenderOption: `UNFORMATTED_VALUE`
- credential: `googleSheetsOAuth2Api` (id=HjfwX5DgD4iXkptZ, "Google Sheets - 하나사인몰")
- **executeOnce: true** 필수 (upstream item 수만큼 반복 호출 방지, quota 초과 방지)

**Why**: 하나사인몰 실제 매출 구조상 CS 경유 주문이 스마트스토어 결제보다 클 때가 많음. 실 ROAS(CS 포함)가 대표 판단에 더 정확.
**How to apply**: n8n에서 매출시트_조회 httpRequest 노드 수정 시 **반드시 Sheet 이름 "업체계약현황"**으로, executeOnce 유지, range를 2000행으로 제한.
