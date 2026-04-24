---
name: 채널별_집계 일자 오타 자동 보정 로직
description: 시트 C열(일) 컬럼의 오타를 이웃 ±2행 기준 majority voting으로 자동 보정. 04-23 기준 229,000원 건 보정 등 18건 보정
type: project
originSessionId: 35d08f6a-12fd-40ba-9cd3-904848f3b709
---
**로직** (채널별_집계 노드 내):

```js
const correctDate = (i) => {
  const orig = rawDates[i];
  if (!orig) return orig;
  const neighbors = [];
  for (let j = Math.max(startIdx, i-2); j <= Math.min(rows.length-1, i+2); j++) {
    if (j === i) continue;
    const d = rawDates[j];
    if (d) neighbors.push(d);
  }
  if (neighbors.length < 3) return orig;
  const count = {};
  neighbors.forEach(d => count[d] = (count[d]||0)+1);
  let top = orig, topCnt = 0;
  for (const [k, v] of Object.entries(count)) {
    if (v > topCnt) { top = k; topCnt = v; }
  }
  if (topCnt >= 3 && top !== orig) return top;
  return orig;
};
```

**규칙**: 이웃 ±2행 중 3개 이상이 동일 일자이고 현재 행만 다르면 → 그 일자로 보정.
- 앞뒤가 서로 다른 일자면 보정 안 함 (안전)
- 월 경계, 년 경계 동일 동작

**Why**: 2026-04-24 확인 — 업체계약현황 시트에 일 컬럼 오타가 상당수 존재. 예: 04-23 등록 배치 중간에 "21" 오타 1건 있으면 파이프라인은 04-21자로 집계. 차장님이 "6,033,460원이 아니고?"라고 한 것이 단서. 실제 전체 시트에서 18건 오타 발견(2028-03-31 같은 연도 타이포 포함).

**How to apply**:
- 04-23 CS 보정 결과 21건/5,804,460원 → 22건/6,033,460원
- 보정 건수와 상위 20건 로그는 채널별_집계 output의 `_날짜보정_건수`, `_날짜보정_로그` 필드에 포함. 리포트_생성 노드에서 참조해 "일자 보정 N건" 섹션 추가 가능
- 시트에 같은 일자끼리 순차 append 되는 패턴 전제. 정렬이 섞이면 보정 약해짐
- 양성오류(실제는 04-21인데 04-23으로 잘못 보정) 리스크는 이웃 3개 이상 조건으로 최소화. 100행(04-21, 이웃 혼재)은 보정 안 함 확인
