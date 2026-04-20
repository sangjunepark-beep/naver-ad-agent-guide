/**
 * batch_click.js — 체크박스 배치 .click()
 *
 * 실행 전 주입 필요:
 *   UNCHECK_VALUES : 해제할 value 배열 (예: ["03`2`05-03`엘리베이터"])
 *   CHECK_VALUES   : 체크할 value 배열 (예: ["03`2`05-01`주차장"])
 *
 * 동작:
 *   1. 해제 대상 중 checked 상태인 것 .click()
 *   2. 체크 대상 중 unchecked 상태인 것 .click()
 *   3. 30개 초과 시 자동 배치 분할 (150ms 간격)
 *
 * 반환:
 *   {total, done, errors[]}
 *
 * 주의:
 *   - FnSelOptChk() 직접 호출 절대 금지
 *   - 실행 전 스냅샷(audit.js) 저장 필수
 *   - 완료 후 페이지 새로고침 → audit.js 재실행으로 검증 필수
 */
(function(UNCHECK_VALUES, CHECK_VALUES){
  const allCbs = Array.from(document.querySelectorAll('input[type="checkbox"]'));
  const errors = [];
  const targets = [];

  // 해제 대상
  (UNCHECK_VALUES||[]).forEach(val => {
    const cb = allCbs.find(c => c.value === val);
    if(!cb){ errors.push({val, err:'NOT_FOUND'}); return; }
    if(cb.checked) targets.push({cb, action:'uncheck'});
  });

  // 체크 대상
  (CHECK_VALUES||[]).forEach(val => {
    const cb = allCbs.find(c => c.value === val);
    if(!cb){ errors.push({val, err:'NOT_FOUND'}); return; }
    if(!cb.checked) targets.push({cb, action:'check'});
  });

  const total = targets.length;
  window.__batchClickDone = 0;
  window.__batchClickErrors = errors;

  // 30개씩 배치 처리
  const BATCH = 30, DELAY = 150;
  function runBatch(start){
    const slice = targets.slice(start, start + BATCH);
    slice.forEach((t, i) => {
      setTimeout(() => {
        t.cb.click();
        window.__batchClickDone++;
      }, i * DELAY);
    });
    // 다음 배치
    if(start + BATCH < targets.length){
      setTimeout(() => runBatch(start + BATCH), BATCH * DELAY + 200);
    }
  }

  runBatch(0);
  return {total, done: 0, errors, note: '배치 실행 시작. window.__batchClickDone 으로 진행 확인'};
})(
  /* UNCHECK_VALUES */ [],
  /* CHECK_VALUES   */ []
)
