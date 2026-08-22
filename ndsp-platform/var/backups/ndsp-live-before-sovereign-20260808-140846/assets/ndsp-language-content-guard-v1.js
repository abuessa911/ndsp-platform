(function(){
  'use strict';

  const LANG_FILE_VERSION = 'NDSP_SINGLE_I18N_CLEAN_V9';
  const STORE_KEYS = ['ndsp_lang_final','ndsp_final_lang','ndsp_lang'];
  const BUTTON_ID = 'ndsp-language-content-switcher';
  const STYLE_ID = 'ndsp-language-content-style-v9';

  function getLang(){
    for (const k of STORE_KEYS) {
      const v = localStorage.getItem(k);
      if (v === 'ar' || v === 'en') return v;
    }
    return 'ar';
  }

  function setLang(lang){
    STORE_KEYS.forEach(k => localStorage.setItem(k, lang));
  }

  function isAdminOrOwner(){
    const p = location.pathname || '/';
    return /^\/admin(?:\/|\.html|$)/i.test(p) || /^\/owner(?:\/|\.html|$)/i.test(p);
  }

  const KEEP = new Set([
    'NDSP','NMP','TDL','UTC','API','VaR','DXY','RSI',
    'BTC/USD','ETH/USD','SOL/USD','XRP/USD','EUR/USD','GBP/USD','XAU/USD','XAG/USD','WTI','SPX',
    'BTC','ETH','SOL','XRP','NG'
  ]);

  const PHRASES = [
    // ===== Data Infrastructure =====
    ['Modular Providers Health & Failover','صحة مزودي البيانات والمسار الاحتياطي'],
    ['Modular Providers, Failover Health','صحة مزودي البيانات والمسار الاحتياطي'],
    ['Modular Providers Health','صحة مزودي البيانات'],
    ['Providers Health','صحة مزودي البيانات'],
    ['Data Provider Health','صحة مزود البيانات'],
    ['DATA PROVIDER HEALTH','صحة مزود البيانات'],
    ['Failover Health','صحة المسار الاحتياطي'],
    ['Modular data layer with manual failover. Each provider monitored for latency, freshness, and completeness.','طبقة بيانات مرنة مع مسار احتياطي يدوي. تتم مراقبة كل مزود من حيث زمن الاستجابة وحداثة البيانات والاكتمال.'],
    ['Modular data layer with manual failover','طبقة بيانات مرنة مع مسار احتياطي يدوي'],
    ['Each provider monitored for latency, freshness, and completeness','تتم مراقبة كل مزود من حيث زمن الاستجابة وحداثة البيانات والاكتمال'],
    ['manual failover','مسار احتياطي يدوي'],
    ['manual fail over','مسار احتياطي يدوي'],
    ['Failover','المسار الاحتياطي'],
    ['failover','المسار الاحتياطي'],
    ['fail over','المسار الاحتياطي'],
    ['over فشل','المسار الاحتياطي'],
    ['فشل over','المسار الاحتياطي'],
    ['over. Each provider monitoredفشل','المسار الاحتياطي. تتم مراقبة كل مزود'],
    ['over degraded','مسار متدهور'],
    ['degraded','متدهور'],
    ['DEGRADED','متدهور'],
    ['Providers','مزودو البيانات'],
    ['PROVIDERS','مزودو البيانات'],
    ['Provider','مزود البيانات'],
    ['Connected','متصل'],
    ['connected','متصل'],
    ['AVG latency','متوسط زمن الاستجابة'],
    ['Latency AVG','متوسط زمن الاستجابة'],
    ['AVG زمن الاستجابة','متوسط زمن الاستجابة'],
    ['Average Latency','متوسط زمن الاستجابة'],
    ['Across active feeds','عبر القنوات النشطة'],
    ['active feeds','القنوات النشطة'],
    ['AVG completeness','متوسط الاكتمال'],
    ['Completeness AVG','متوسط الاكتمال'],
    ['NESS مكتمل AVG','متوسط الاكتمال'],
    ['Last 24h','آخر 24 ساعة'],
    ['Last 24H','آخر 24 ساعة'],
    ['REGIONS COVERED','المناطق المغطاة'],
    ['Regions Covered','المناطق المغطاة'],
    ['OVER TOPOLOGY','هيكل المسار الاحتياطي'],
    ['Over Topology','هيكل المسار الاحتياطي'],
    ['Topology','الهيكل'],
    ['TOPOLOGY','الهيكل'],
    ['Coverage','التغطية'],
    ['COVERAGE','التغطية'],
    ['OVER TEST fail TRIGGER','اختبار تشغيل المسار الاحتياطي'],
    ['OVER TEST فشل TRIGGER','اختبار تشغيل المسار الاحتياطي'],
    ['OVER TEST','اختبار المسار الاحتياطي'],
    ['TRIGGER','التشغيل'],
    ['Trigger','التشغيل'],
    ['INGEST THROUGHPUT · LAST 60 MIN','معدل إدخال البيانات · آخر 60 دقيقة'],
    ['Ingest Throughput · Last 60 Min','معدل إدخال البيانات · آخر 60 دقيقة'],
    ['INGEST THROUGHPUT','معدل إدخال البيانات'],
    ['LAST 60 MIN','آخر 60 دقيقة'],
    ['msg/min','رسالة/دقيقة'],
    ['Next: Fri 19:30 UTC','التالي: الجمعة 19:30 UTC'],
    ['Next:','التالي:'],
    ['Market Data WS','قناة بيانات السوق'],
    ['Market Data','بيانات السوق'],
    ['On-Chain Stream','قناة بيانات السلسلة'],
    ['On-Chain','بيانات السلسلة'],
    ['Macro Polling','تحديث البيانات الكلية'],
    ['Weekly Batch','دفعة أسبوعية'],
    ['Sentiment Stream','قناة المعنويات'],
    ['Health','الصحة'],
    ['Freshness','حداثة البيانات'],
    ['Latency','زمن الاستجابة'],
    ['Completeness','الاكتمال'],
    ['us-east, us-west, eu-west, eu-central, ap-northeast','شرق الولايات المتحدة، غرب الولايات المتحدة، غرب أوروبا، وسط أوروبا، شمال شرق آسيا'],
    ['us-east','شرق الولايات المتحدة'],
    ['us-west','غرب الولايات المتحدة'],
    ['eu-west','غرب أوروبا'],
    ['eu-central','وسط أوروبا'],
    ['ap-northeast','شمال شرق آسيا'],

    // public provider privacy
    ['Binance Spot ↔ Coinbase Pro','مزود أسعار مباشر ↔ مزود أسعار احتياطي'],
    ['TwelveData ↔ Polygon.io','مزود بيانات السوق ↔ مزود مؤشرات'],
    ['Glassnode','مزود بيانات السلسلة'],
    ['Binance Spot','مزود أسعار مباشر'],
    ['Coinbase Pro','مزود أسعار احتياطي'],
    ['Coinbase','مزود أسعار احتياطي'],
    ['TwelveData','مزود بيانات السوق'],
    ['Polygon.io','مزود مؤشرات'],
    ['Quant','مزود تحليلي'],

    // ===== Strategy Lab =====
    ['Scenario Analysis & What-If Simulation','تحليل السيناريوهات ومحاكاة ماذا لو'],
    ['Scenario Analysis','تحليل السيناريوهات'],
    ['What-If Simulation','محاكاة ماذا لو'],
    ['Stress-test the decision engine under different macro and regime scenarios. Compare engine outputs side-by-side.','اختبر محرك القرار تحت سيناريوهات مختلفة للحالة والسياق الكلي، ثم قارن مخرجات المحرك جنبًا إلى جنب.'],
    ['Stress-test the decision engine under different macro and regime scenarios','اختبر محرك القرار تحت سيناريوهات مختلفة للحالة والسياق الكلي'],
    ['Compare engine outputs side-by-side','قارن مخرجات المحرك جنبًا إلى جنب'],
    ['Fed Hawkish Surprise','مفاجأة تشدد الفيدرالي'],
    ['Geopolitical Escalation (ME)','تصعيد جيوسياسي في الشرق الأوسط'],
    ['Soft Landing Confirmation','تأكيد الهبوط السلس'],
    ['Liquidity Crisis Echo','أثر أزمة السيولة'],
    ['SCENARIO CONDITIONS','شروط السيناريو'],
    ['Scenario Conditions','شروط السيناريو'],
    ['ACTIVE REGIME','الحالة النشطة'],
    ['Active Regime','الحالة النشطة'],
    ['PROBABILITY WEIGHT','وزن الاحتمال'],
    ['Probability Weight','وزن الاحتمال'],
    ['MODELED triggers','المحفزات المحاكاة'],
    ['MODELED','محاكاة'],
    ['Volatility shift > 1.5σ','تغير التذبذب أعلى من 1.5σ'],
    ['Volatility shift','تغير التذبذب'],
    ['Correlation change','تغير الارتباط'],
    ['Macro narrative dominance flip','تحول السرد الكلي المهيمن'],
    ['Liquidity contraction event','حدث انكماش السيولة'],
    ['STRESS TEST RESULT','نتيجة اختبار الضغط'],
    ['Stress Test Result','نتيجة اختبار الضغط'],
    ['Portfolio P&L','أثر المحفظة'],
    ['Max Drawdown','أقصى تراجع'],
    ['VaR Breach','تجاوز VaR'],
    ['Recovery Time (est.)','زمن التعافي التقديري'],
    ['Recovery Time','زمن التعافي'],
    ['Stability','الاستقرار'],
    ['NO','لا'],
    ['days','أيام'],
    ['REVERSAL','انعكاس'],
    ['COMMODITY','السلع'],
    ['PANIC','هلع'],
    ['TREND CONTINUATION','استمرار الاتجاه'],

    // ===== Governance / Risk =====
    ['Controls, Compliance & Kill-Switch','حدود التحكم والامتثال وإيقاف الطوارئ'],
    ['Controls','حدود التحكم'],
    ['Control','التحكم'],
    ['Concurrent positions','المراكز المتزامنة'],
    ['CONCURRENT POSITIONS','المراكز المتزامنة'],
    ['PORTFOLIO','المحفظة'],
    ['Portfolio','المحفظة'],
    ['DAILY VAR (95%)','قيمة المخاطر اليومية (95%)'],
    ['DAILY VAR','قيمة المخاطر اليومية'],
    ['Limit $300k','الحد 300 ألف دولار'],
    ['Limit','الحد'],
    ['utilized','مستخدم'],
    ['Hard guardrails enforced at engine level. Every decision passes through these checks before execution authorization.','ضوابط صارمة مطبقة على مستوى المحرك، وكل قرار يمر عبر هذه الفحوصات قبل السماح بأي إجراء تنفيذي.'],
    ['Hard guardrails enforced at engine level','ضوابط صارمة مطبقة على مستوى المحرك'],
    ['Every decision passes through these checks before execution authorization','كل قرار يمر عبر هذه الفحوصات قبل السماح بأي إجراء تنفيذي'],
    ['Trade Limit','حد التداول'],
    ['Drawdown','التراجع'],
    ['Compliance Checks','فحوصات الامتثال'],
    ['CHECKS','الفحوصات'],
    ['PASS','اجتاز'],
    ['WARN','تنبيه'],
    ['FAIL','فشل'],
    ['ARMED','مفعّل'],
    ['READY','جاهز'],
    ['Position Sizing within VaR','حجم المركز ضمن VaR'],
    ['Position Sizing','حجم المركز'],
    ['Concentration < 35% per class','التركيز أقل من 35% لكل فئة'],
    ['Liquidity Coverage > 30D','تغطية السيولة أكثر من 30 يوم'],
    ['Correlation Cluster Limit','حد ترابط المجموعة'],
    ['Counterparty Exposure','تعرض الطرف المقابل'],
    ['Regulatory Reporting (MiFID II)','التقارير التنظيمية'],
    ['Provider Outage > 30s','انقطاع مزود البيانات لأكثر من 30 ثانية'],
    ['Manual Override','تجاوز يدوي'],
    ['Recent Events','الأحداث الأخيرة'],
    ['RECENT EVENTS','الأحداث الأخيرة'],

    // ===== Common portal =====
    ['Executive Overview','النظرة التنفيذية'],
    ['Markets Monitor','مراقبة الأسواق'],
    ['Phase Engine','محرك المراحل'],
    ['Intelligence Engine','محرك الذكاء'],
    ['Decision Engine','محرك القرار'],
    ['Governance & Risk','الحوكمة والمخاطر'],
    ['Data Infrastructure','بنية البيانات'],
    ['Strategy Lab','مختبر الاستراتيجية'],
    ['Architecture','المعمارية'],
    ['Market State','حالة السوق'],
    ['Global Market State','حالة السوق'],
    ['Decision Confidence','ثقة القرار'],
    ['Risk Posture','وضع المخاطر'],
    ['Governance','الحوكمة'],
    ['Session','جلسة'],
    ['Markets Live','الأسواق مباشرة'],
    ['Secure Access','وصول آمن'],
    ['System Online','النظام متاح'],
    ['Risk Analyst','محلل مخاطر'],
    ['Command','الأوامر'],
    ['Intelligence','الذكاء'],
    ['Operations','العمليات'],
    ['Live','مباشر'],
    ['Last 24H','آخر 24 ساعة'],
    ['Last 24h','آخر 24 ساعة'],
    ['Price','السعر'],
    ['Class','الفئة'],
    ['Symbol','الرمز'],
    ['Phase','المرحلة'],
    ['Assets','الأصول'],
    ['Instruments','الأصول'],
    ['All','الكل'],
    ['Indices','المؤشرات'],
    ['Commodities','السلع'],
    ['Forex','الفوركس'],
    ['Crypto','العملات الرقمية'],
    ['Expansion','توسع'],
    ['Trend Continuation','استمرار الاتجاه'],
    ['Accumulation','تجميع'],
    ['Compression','ضغط'],
    ['Neutral','حياد'],
    ['Rotation','دوران'],
    ['Distribution','توزيع'],
    ['Reversal Risk','خطر انعكاس'],
    ['Exhaustion','استنزاف'],
    ['Panic','هلع'],
    ['Pages','الصفحات'],
    ['Home','الصفحة الرئيسية'],
    ['Login','تسجيل الدخول'],
    ['Create new user','تسجيل مستخدم جديد'],
    ['System admin','مدير النظام'],
    ['System owner','مالك النظام']
  ];

  const WHOLE_HEADINGS = [
    {
      test: s => /Modular|Providers|Failover|Health|over فشل|فشل over/.test(s),
      ar: 'صحة مزودي البيانات والمسار الاحتياطي'
    },
    {
      test: s => /Scenario Analysis|What-If|Simulation/.test(s),
      ar: 'تحليل السيناريوهات ومحاكاة ماذا لو'
    },
    {
      test: s => /Controls|Kill-Switch|Compliance/.test(s) && /Drawdown|التراجع|Trade|التداول/.test(s),
      ar: 'حدود التداول والتراجع والامتثال وإيقاف الطوارئ'
    }
  ];

  function applyPairs(value){
    let s = String(value || '');

    PHRASES
      .slice()
      .sort((a,b) => b[0].length - a[0].length)
      .forEach(([from,to]) => {
        if (KEEP.has(from)) return;
        s = s.split(from).join(to);
      });

    // إصلاحات بقايا الترجمة الجزئية
    s = s.replace(/over\s*فشل/g, 'المسار الاحتياطي');
    s = s.replace(/فشل\s*over/g, 'المسار الاحتياطي');
    s = s.replace(/\bover\b/g, 'المسار الاحتياطي');

    s = s.replace(/حد التداول\s*[,،]\s*[sS]\s*التراجع/g, 'حدود التداول والتراجع');
    s = s.replace(/حد التداول\s*[sS]\s*التراجع/g, 'حدود التداول والتراجع');
    s = s.replace(/([\u0600-\u06FF])\s*[,،]\s*[sS]\s*[,،]?\s*([\u0600-\u06FF])/g, '$1، $2');

    s = s.replace(/AVG\s+زمن الاستجابة/g, 'متوسط زمن الاستجابة');
    s = s.replace(/AVG\s+مكتمل\s+NESS/g, 'متوسط الاكتمال');
    s = s.replace(/مزودو البيانات\s+متصل/g, 'مزودو البيانات المتصلون');
    s = s.replace(/متصل\s+مزودو البيانات/g, 'مزودو البيانات المتصلون');

    s = s.replace(/\s{2,}/g, ' ');
    s = s.replace(/\s+،/g, '،');
    s = s.replace(/،\s*،/g, '،');
    return s.trim();
  }

  function translateNodeText(lang){
    if (lang !== 'ar') return;

    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode(node){
        const p = node.parentElement;
        if (!p) return NodeFilter.FILTER_REJECT;
        if (p.closest('script,style,noscript,textarea,code,pre')) return NodeFilter.FILTER_REJECT;
        if (p.closest('#' + BUTTON_ID)) return NodeFilter.FILTER_REJECT;
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });

    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);

    nodes.forEach(node => {
      const oldValue = node.nodeValue;
      const newValue = applyPairs(oldValue);
      if (newValue !== oldValue) node.nodeValue = newValue;
    });
  }

  function translateWholeHeadings(lang){
    if (lang !== 'ar') return;

    document.querySelectorAll('h1,h2,h3,[class*="title"],[class*="heading"]').forEach(el => {
      const raw = (el.textContent || '').replace(/\s+/g, ' ').trim();
      if (!raw || raw.length > 180) return;

      for (const h of WHOLE_HEADINGS) {
        if (h.test(raw)) {
          el.textContent = h.ar;
          return;
        }
      }

      const fixed = applyPairs(raw);
      if (fixed !== raw) el.textContent = fixed;
    });
  }

  function translateAttrs(lang){
    if (lang !== 'ar') return;

    ['placeholder','title','aria-label','alt','value'].forEach(attr => {
      document.querySelectorAll('[' + attr + ']').forEach(el => {
        const oldValue = el.getAttribute(attr);
        const newValue = applyPairs(oldValue);
        if (newValue !== oldValue) el.setAttribute(attr, newValue);
      });
    });
  }

  function injectStyle(){
    document.getElementById(STYLE_ID)?.remove();

    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = `
      #${BUTTON_ID}{
        display:inline-flex;
        align-items:center;
        gap:6px;
        padding:6px;
        border:1px solid rgba(212,175,55,.34);
        background:linear-gradient(180deg,rgba(14,12,8,.92),rgba(5,5,5,.94));
        color:#f7f1df;
        border-radius:999px;
        font-family:system-ui,-apple-system,"Segoe UI",Tahoma,Arial,sans-serif;
        flex:0 0 auto;
      }
      #${BUTTON_ID} button{
        border:0;
        border-radius:999px;
        padding:7px 12px;
        background:transparent;
        color:#b9ad91;
        cursor:pointer;
        font-weight:900;
        font-size:12px;
        letter-spacing:.08em;
      }
      #${BUTTON_ID} button.active{
        background:linear-gradient(135deg,#f4d77d,#d4af37);
        color:#080705;
      }
    `;
    document.head.appendChild(style);
  }

  function placeButton(lang){
    document.getElementById(BUTTON_ID)?.remove();

    const box = document.createElement('div');
    box.id = BUTTON_ID;
    box.setAttribute('dir','ltr');
    box.innerHTML = `
      <button type="button" data-lang="ar">AR</button>
      <button type="button" data-lang="en">EN</button>
    `;

    box.querySelectorAll('button').forEach(btn => {
      const target = btn.getAttribute('data-lang');
      if (target === lang) btn.classList.add('active');
      btn.addEventListener('click', () => {
        setLang(target);
        location.reload();
      });
    });

    const pagesBtn = Array.from(document.querySelectorAll('button,a,div,span'))
      .find(el => (el.textContent || '').trim() === 'الصفحات' || (el.textContent || '').trim() === 'Pages');

    if (pagesBtn && pagesBtn.parentElement) {
      pagesBtn.parentElement.insertBefore(box, pagesBtn.nextSibling);
      return;
    }

    const top = document.querySelector('header,.topbar,[class*="topbar"],[class*="Topbar"]') || document.body;
    top.insertBefore(box, top.firstChild);
  }

  function applyLanguage(){
    const lang = getLang();

    document.documentElement.setAttribute('lang', lang);
    document.documentElement.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    document.documentElement.setAttribute('data-ndsp-lang', lang);

    injectStyle();
    placeButton(lang);

    if (lang === 'ar') {
      translateWholeHeadings(lang);
      translateNodeText(lang);
      translateAttrs(lang);
      translateWholeHeadings(lang);
    }
  }

  function boot(){
    applyLanguage();

    let timer = null;
    const obs = new MutationObserver(() => {
      clearTimeout(timer);
      timer = setTimeout(applyLanguage, 120);
    });

    obs.observe(document.documentElement, {
      childList:true,
      subtree:true,
      characterData:true
    });

    [200,600,1200,2200,3500,5000].forEach(ms => setTimeout(applyLanguage, ms));
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
