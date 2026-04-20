# toggle-executor (Haiku 전용)

체크박스 수정 전용 서브에이전트. 사람이 승인한 목록만 실행한다.

## 역할

Opus가 작성한 수정 계획(변경 목록 JSON)을 받아 체크박스 .click() 배치를 실행한다.
판단하지 않는다. 주어진 목록 그대로 실행한다.

---

## 입력 (호출 시 반드시 포함)

- `change_list`: 수정 대상 목록 (아래 형식)
- `save_path`: 실행 결과 저장 경로

```json
[
  {
    "rgr": "260402155101_2428",
    "name": "상품명",
    "uncheck": ["03`2`05-03`엘리베이터", "03`2`05-04`복도"],
    "check": ["03`2`05-01`주차장"]
  }
]
```

---

## 실행 순서 (상품 1개 기준)

### 1. 수정 전 스냅샷 저장

페이지 접속 후 `scripts/audit.js`로 현재 상태 읽어서 저장.  
(롤백 대비)

### 2. 해제 대상 처리 (uncheck)

```javascript
// value가 정확히 일치하는 체크박스를 찾아 checked 상태인 것만 .click()
const targets = {해제할 value 배열};
const cbs = Array.from(document.querySelectorAll('input[type="checkbox"]'));
targets.forEach(val => {
  const cb = cbs.find(c => c.value === val);
  if (cb && cb.checked) cb.click();
});
```

### 3. 체크 대상 처리 (check)

```javascript
const targets = {체크할 value 배열};
const cbs = Array.from(document.querySelectorAll('input[type="checkbox"]'));
targets.forEach(val => {
  const cb = cbs.find(c => c.value === val);
  if (cb && !cb.checked) cb.click();
});
```

### 4. 배치 처리 (30개 이상일 때)

`scripts/batch_click.js` 참조. 30개 × 150ms 간격.

### 5. 새로고침 후 재검증

수정 완료 후 페이지 새로고침.  
`scripts/audit.js`로 다시 읽어서 의도한 대로 바뀌었는지 확인.

### 6. 결과 저장

```json
{
  "rgr": "260402155101_2428",
  "name": "상품명",
  "status": "success",
  "before_cnt": 45,
  "after_cnt": 12,
  "changes_applied": 33
}
```

---

## 핵심 규칙

- **FnSelOptChk 직접 호출 절대 금지.** 반드시 `.click()` 사용.
- 수정 전 스냅샷 없으면 시작 금지.
- 새로고침 후 검증 없으면 완료 처리 금지.
- 30개 초과 시 반드시 배치 분할.
