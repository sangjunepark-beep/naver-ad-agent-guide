/**
 * audit.js — 업종별 공간 체크 상태 읽기
 * 반환: JSON 문자열 {n, cnt, e, full, detail}
 *
 * n      : 상품명
 * cnt    : 전체 체크된 공간 수
 * e      : true = 업종 미연결 (섹션 자체 없음)
 * full   : true = 과태깅 의심 (cnt > 120)
 * detail : {업종명: [공간코드, ...], ...}
 */
(function(){
  const I={'01':'학교','02':'식당','03':'아파트','04':'호텔','05':'병원','06':'회사','07':'공공','08':'헬스','09':'기타'};
  let h=null;
  document.querySelectorAll('*').forEach(e=>{
    if(h)return;
    const t=(e.textContent||'').trim();
    if(t.startsWith('업종별 카테고리')&&t.length<200&&e.children.length<5)h=e
  });
  if(!h)return JSON.stringify({
    n:(document.querySelector('input[name="GoodsName"]')||{}).value||'',
    cnt:0, e:true, full:false, detail:{}
  });
  const c=Array.from(document.querySelectorAll('input[type="checkbox"]'))
    .filter(x=>h.compareDocumentPosition(x)&Node.DOCUMENT_POSITION_FOLLOWING);
  const r=/^(\d{2})`\d`(05-\d{2})`/;
  const o={};
  c.forEach(x=>{
    const m=(x.value||'').match(r);
    if(!m)return;
    const k=I[m[1]];
    if(!k)return;
    if(!o[k])o[k]=[];
    if(x.checked)o[k].push(m[2])
  });
  const cnt=Object.values(o).reduce((a,b)=>a+b.length,0);
  return JSON.stringify({
    n:(document.querySelector('input[name="GoodsName"]')||{}).value||'',
    cnt,
    e:Object.keys(o).length===0,
    full:cnt>120,
    detail:o
  })
})()
