/* NDSP_INTEGRATED_MARKET_SUITE_NAV_V1 */
/* NDSP_MARKET_SUITE_FINAL_NAV_V9 — additive navigation bridge */
(()=>{
  'use strict';
  if(window.__NDSP_MARKET_SUITE_FINAL_NAV_V9__) return;
  window.__NDSP_MARKET_SUITE_FINAL_NAV_V9__=true;
  const path=location.pathname.toLowerCase();
  if(path.includes('/market-suite')||path.includes('/login')||path.includes('/register')||path.includes('/admin')||path.includes('/owner')||path.includes('/reset')) return;
  function add(){
    const candidates=[...document.querySelectorAll('aside nav, aside [role="navigation"], nav')];
    const nav=candidates.find(n=>/غرفة القرار|الأسواق|مركز القيادة|لوحة|الرئيسية/.test(n.textContent||''))||candidates[0];
    if(!nav||nav.querySelector('[data-ndsp-market-suite-nav]')) return false;
    const box=document.createElement('div');
    box.setAttribute('data-ndsp-market-suite-nav','v9');
    box.style.cssText='margin:14px 0;padding:10px 6px;border-top:1px solid rgba(216,170,74,.18);border-bottom:1px solid rgba(216,170,74,.18)';
    const title=document.createElement('div');
    title.textContent='الأسواق المتكاملة';
    title.style.cssText='padding:0 10px 8px;color:#9f8a62;font-size:10px;font-weight:800';
    box.appendChild(title);
    const items=[
      ['/market-suite/#/markets','◫','الأسواق والأصول'],
      ['/market-suite/#/chart/BTCUSDT','⌁','الشارت والتحليل الفني'],
      ['/market-suite/#/decision','◎','غرفة القرار'],
      ['/market-suite/#/opportunities','⌕','مستكشف الفرص'],
      ['/market-suite/#/watchlist','☆','قوائم المراقبة'],
      ['/market-suite/#/alerts','◉','التنبيهات'],
      ['/market-suite/#/news','◌','الأخبار والأحداث'],
      ['/market-suite/#/guide','?','دليل الاستخدام']
    ];
    for(const [href,icon,label] of items){
      const a=document.createElement('a');
      a.href=href;
      a.style.cssText='display:flex;align-items:center;gap:10px;padding:9px 10px;margin:2px 0;border-radius:9px;text-decoration:none;color:inherit;font-size:12px';
      a.onmouseenter=()=>a.style.background='rgba(216,170,74,.09)';
      a.onmouseleave=()=>a.style.background='transparent';
      a.innerHTML=`<span style="width:18px;color:#d8aa4a">${icon}</span><span>${label}</span>`;
      box.appendChild(a);
    }
    nav.appendChild(box);
    return true;
  }
  if(add()) return;
  let tries=0;
  const mo=new MutationObserver(()=>{if(add()||++tries>100)mo.disconnect()});
  mo.observe(document.documentElement,{childList:true,subtree:true});
  setTimeout(()=>mo.disconnect(),20000);
})();
