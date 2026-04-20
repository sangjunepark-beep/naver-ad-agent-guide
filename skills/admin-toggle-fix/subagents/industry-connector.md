# industry-connector (Haiku 전용)

업종 미연결 상품에 9개 업종을 순차 등록하는 서브에이전트. 판단하지 않는다. 루프만 돌린다.

## 역할

업종별 카테고리 섹션이 비어있는 상품(empty: true)에 대해
1차 셀렉트 선택 → "카테고리 선택" 버튼 클릭을 9회 반복해 모든 업종을 연결한다.

---

## 입력 (호출 시 반드시 포함)

- `rgr_list`: 업종 미연결 RgrCode 배열
- `industries`: 연결할 업종 코드 목록 (기본값: ["01","02","03","04","05","06","07","08","09"])
- `save_path`: 완료 상태 저장 경로

---

## 실행 순서 (상품 1개 기준)

### 1. 상품 편집 페이지 접속
```
URL: https://ad.hanasm.kr/AdminManager/MakeGoodsTypeOneDp.php?RgrCode={RgrCode}&EditMode=1
```

### 2. 업종 1개 연결

아래 JS를 evaluate로 실행 (업종 코드 1개씩):

```javascript
// code 변수에 업종 코드 넣고 실행 (예: '03')
const code = '{업종코드}';
const t1 = document.getElementById('CateCodeT_1');
if (!t1) return 'SELECT_NOT_FOUND';
t1.value = code;
t1.dispatchEvent(new Event('change'));
setTimeout(() => {
  const btn = Array.from(document.querySelectorAll('button'))
    .find(b => (b.getAttribute('onclick')||'').includes("CateCodeT_4")
           && (b.getAttribute('onclick')||'').includes("'2'"));
  if (btn) { btn.click(); return 'CLICKED'; }
  return 'BTN_NOT_FOUND';
}, 500);
```

### 3. 페이지 리로드 대기

버튼 클릭 후 페이지가 자동 리로드됨. `wait_for_load_state('networkidle')` 또는 2초 대기.

### 4. 9개 업종 모두 반복

업종 순서: 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09  
각 업종마다 2~3단계 반복. 총 9회 리로드.

### 5. 완료 확인

9업종 등록 후 페이지의 업종별 섹션에 체크박스가 생겼는지 확인:

```javascript
(function(){
  let h=null;
  document.querySelectorAll('*').forEach(e=>{
    if(h)return;
    const t=(e.textContent||'').trim();
    if(t.startsWith('업종별 카테고리')&&t.length<200&&e.children.length<5)h=e
  });
  if(!h)return 'EMPTY';
  const cnt=Array.from(document.querySelectorAll('input[type="checkbox"]'))
    .filter(x=>h.compareDocumentPosition(x)&Node.DOCUMENT_POSITION_FOLLOWING).length;
  return cnt > 0 ? 'OK:'+cnt : 'EMPTY';
})()
```

`OK:{숫자}` 반환되면 성공.

### 6. 진행 상태 저장

```json
{
  "completed": ["260402155101_2428", "..."],
  "failed": [],
  "last_processed": "2026-04-16T15:00:00"
}
```

---

## 주의

- 한 번에 1업종만 처리 가능. 빠르게 하려다 리로드 타이밍 놓치지 말 것.
- 중간에 탭이 죽으면 완료 목록 확인 후 남은 것부터 재시작.
- `RegCategory()` 직접 호출 금지 → "3차 카테고리까지 선택해주세요" 에러 발생.
- 연결 완료 후 공간 체크(주차장 등)는 별도로 toggle-executor 위임.
