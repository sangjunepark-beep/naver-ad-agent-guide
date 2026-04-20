/**
 * connect_industry.js — 업종 1개 연결
 * 실행 전: code 변수에 업종 코드 주입 (예: code = '03')
 * 동작: 1차 셀렉트 선택 → "카테고리 선택" 버튼 클릭 → 페이지 리로드
 *
 * 반환값:
 *   'CLICKED'        — 성공, 페이지 리로드 대기
 *   'SELECT_NOT_FOUND' — CateCodeT_1 셀렉트 없음
 *   'BTN_NOT_FOUND'  — 카테고리 선택 버튼 없음
 *
 * 주의:
 *   - 한 번 실행에 1업종만 처리 가능
 *   - 클릭 후 wait_for_load_state('networkidle') 또는 2초 대기 필수
 *   - RegCategory() 직접 호출 금지
 *   - code 값: '01'~'09'
 */
(function(code){
  const t1 = document.getElementById('CateCodeT_1');
  if(!t1) return 'SELECT_NOT_FOUND';
  t1.value = code;
  t1.dispatchEvent(new Event('change'));
  return new Promise(resolve => {
    setTimeout(() => {
      const btn = Array.from(document.querySelectorAll('button'))
        .find(b => (b.getAttribute('onclick')||'').includes("CateCodeT_4")
               && (b.getAttribute('onclick')||'').includes("'2'"));
      if(!btn){ resolve('BTN_NOT_FOUND'); return; }
      btn.click();
      resolve('CLICKED');
    }, 500);
  });
})('__CODE__')
