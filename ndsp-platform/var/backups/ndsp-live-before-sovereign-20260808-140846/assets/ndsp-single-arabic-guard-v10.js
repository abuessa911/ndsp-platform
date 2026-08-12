(function(){
  'use strict';

  const VERSION = 'NDSP_SINGLE_ARABIC_GUARD_V10';
  const KEY = 'ndsp_lang_final';

  function currentLang(){
    return localStorage.getItem(KEY)
      || localStorage.getItem('ndsp_final_lang')
      || localStorage.getItem('ndsp_lang')
      || 'ar';
  }

  function isArabic(){
    return currentLang() === 'ar';
  }

  function isProtectedSymbol(s){
    const x = String(s || '').trim();
    return /^(NDSP|NMP|TDL|UTC|API|VaR|DXY|RSI|BTC\/USD|ETH\/USD|SOL\/USD|XRP\/USD|EUR\/USD|GBP\/USD|XAU\/USD|XAG\/USD|WTI|SPX|BTC|ETH|SOL|XRP|NG|AK)$/i.test(x);
  }

  const exact = [
    // الصفحات والعناوين العامة
    ['Executive Overview','النظرة التنفيذية'],
    ['Global Decision Intelligence','ذكاء القرار'],
    ['Live cross-asset state, regime mapping, decision confidence and governance posture across all monitored markets.','حالة مباشرة متعددة الأصول، وربط للحالة، وثقة القرار، ووضع الحوكمة عبر الأسواق قيد المراقبة.'],
    ['Markets Monitor','مراقبة الأسواق'],
    ['Multi-Asset Watchlists & Cross-Market Dependencies','قوائم مراقبة الأصول وترابط الأسواق'],
    ['Real-time bias, phase, volatility, liquidity and conviction across Crypto, Forex, Commodities and Indices.','قراءة مباشرة للانحياز والمرحلة والتذبذب والسيولة وقوة القراءة عبر العملات الرقمية والفوركس والسلع والمؤشرات.'],
    ['Market Regime Classification','تصنيف حالة السوق'],
    ['Identifies the prevailing market state per asset using structural, volatility, volume and on-chain signals — driving every downstream decision.','يحدد حالة السوق السائدة لكل أصل باستخدام البنية والتذبذب والحجم وبيانات السلسلة لدعم القرار اللاحق.'],
    ['Smart Money + Narrative Reasoning Layer','طبقة الأموال الذكية والسرد التحليلي'],
    ['Combines controlled concepts (SMC) with NMP-style narrative & positioning context. Every signal is explained in plain language.','تدمج مفاهيم الأموال الذكية مع سياق سردي وتمركزي بأسلوب NMP، مع شرح كل إشارة بلغة واضحة.'],
    ['Final Outputs & Engine Dependency Chain','مخرجات القرار النهائية وسلسلة اعتماد المحركات'],
    ['Every decision is traceable to a weighted set of upstream engines and signals — full explainability for governance review.','كل قرار قابل للتتبع إلى مجموعة موزونة من المحركات والإشارات، مع قابلية شرح كاملة للمراجعة الحوكمية.'],
    ['Scenario Analysis & What-If Simulation','تحليل السيناريوهات ومحاكاة ماذا لو'],
    ['Stress-test the decision engine under different macro and regime scenarios. Compare engine outputs side-by-side.','اختبار محرك القرار تحت سيناريوهات كلية وحالات سوق مختلفة، مع مقارنة المخرجات جنبًا إلى جنب.'],
    ['Modular Providers Health & Failover','صحة مزودي البيانات والمسار الاحتياطي'],
    ['Modular Providers Health','صحة مزودي البيانات'],
    ['Modular data layer with manual failover. Each provider monitored for latency, freshness, and completeness.','طبقة بيانات مرنة مع مسار احتياطي يدوي. تتم مراقبة كل مزود من حيث زمن الاستجابة وحداثة البيانات والاكتمال.'],
    ['Controls, Compliance & Kill-Switch','حدود التحكم والامتثال وإيقاف الطوارئ'],
    ['Hard guardrails enforced at engine level. Every decision passes through these checks before execution authorization.','ضوابط صارمة مطبقة على مستوى المحرك، وكل قرار يمر عبر هذه الفحوصات قبل السماح بأي إجراء تنفيذي.'],

    // العناوين الداخلية
    ['REGIME DISTRIBUTION','توزيع الحالة'],
    ['ENGINE CONSENSUS','إجماع المحركات'],
    ['COMPOSITE CONFIDENCE','الثقة المركبة'],
    ['PHASE MAP','خريطة المراحل'],
    ['SIGNAL CONTRIBUTION','مساهمة الإشارات'],
    ['CONFIDENCE METER','مقياس الثقة'],
    ['DECISION STREAM','سجل القرارات'],
    ['DECISION RATIONALE','مبررات القرار'],
    ['ENGINE DEPENDENCY CHAIN','سلسلة اعتماد المحركات'],
    ['MACRO / NARRATIVE CONTEXT','السياق الكلي والسردي'],
    ['ACTIVE NARRATIVE THREADS','المسارات السردية النشطة'],
    ['CONTROLLED POSITIONING','التموضع المحكوم'],
    ['EXPLAINABLE INTELLIGENCE OUTPUT','مخرجات الذكاء القابلة للشرح'],
    ['WHY THIS MATTERS','لماذا هذا مهم'],
    ['SCENARIO CONDITIONS','شروط السيناريو'],
    ['STRESS TEST RESULT','نتيجة اختبار الضغط'],
    ['DATA PROVIDER HEALTH','صحة مزود البيانات'],
    ['OVER TOPOLOGY','هيكل المسار الاحتياطي'],
    ['INGEST THROUGHPUT','معدل إدخال البيانات'],
    ['REGIONS COVERED','المناطق المغطاة'],
    ['PROVIDERS','مزودو البيانات'],
    ['CONNECTED','متصل'],
    ['ACTIVE','نشط'],
    ['SIGNALS','الإشارات'],
    ['SMART MONEY CONCEPTS','مفاهيم الأموال الذكية'],
    ['RECENT EVENTS','الأحداث الأخيرة'],
    ['COMPLIANCE CHECKS','فحوصات الامتثال'],
    ['CHECKS','الفحوصات'],

    // مصطلحات القرار
    ['Market State','حالة السوق'],
    ['Global Market State','حالة السوق'],
    ['Decision Confidence','ثقة القرار'],
    ['Risk Posture','وضع المخاطر'],
    ['Governance','الحوكمة'],
    ['Trade Limit','حد التداول'],
    ['Drawdown','التراجع'],
    ['Concurrent positions','المراكز المتزامنة'],
    ['Portfolio P&L','أثر المحفظة'],
    ['Max Drawdown','أقصى تراجع'],
    ['VaR Breach','تجاوز قيمة المخاطر'],
    ['Recovery Time (est.)','زمن التعافي التقديري'],
    ['Stability','الاستقرار'],
    ['Action','الإجراء'],
    ['Asset','الأصل'],
    ['Confidence','الثقة'],
    ['Approved','معتمد'],
    ['APPROVED','معتمد'],
    ['Long','شراء'],
    ['LONG','شراء'],
    ['Short','بيع'],
    ['SHORT','بيع'],
    ['Reduce Risk','خفض المخاطر'],
    ['REDUCE RISK','خفض المخاطر'],
    ['No Trade','لا تداول'],
    ['NO TRADE','لا تداول'],
    ['Hold','انتظار'],
    ['HOLD','انتظار'],
    ['Blocked','محجوب'],
    ['BLOCKED','محجوب'],
    ['Pass','اجتاز'],
    ['PASS','اجتاز'],
    ['Warn','تنبيه'],
    ['WARN','تنبيه'],
    ['Fail','فشل'],
    ['FAIL','فشل'],
    ['Armed','مفعّل'],
    ['ARMED','مفعّل'],
    ['Ready','جاهز'],
    ['READY','جاهز'],
    ['NO','لا'],

    // المراحل والحالات
    ['Expansion','توسع'],
    ['Trend Continuation','استمرار الاتجاه'],
    ['Accumulation','تجميع'],
    ['Compression','ضغط'],
    ['Neutral','حياد'],
    ['Rotation','دوران'],
    ['Distribution','توزيع'],
    ['Reversal Risk','خطر انعكاس'],
    ['Reversal','انعكاس'],
    ['REVERSAL','انعكاس'],
    ['Exhaustion','استنزاف'],
    ['Panic','هلع'],
    ['PANIC','هلع'],
    ['Commodity','سلع'],
    ['COMMODITY','سلع'],
    ['Risk-On','إقبال على المخاطر'],
    ['RISK-ON','إقبال على المخاطر'],
    ['Moderate','متوسط'],

    // صفحة السيناريوهات
    ['Fed Hawkish Surprise','مفاجأة تشدد الفيدرالي'],
    ['Geopolitical Escalation (ME)','تصعيد جيوسياسي في الشرق الأوسط'],
    ['Soft Landing Confirmation','تأكيد الهبوط السلس'],
    ['Liquidity Crisis Echo','أثر أزمة السيولة'],
    ['Active Regime','الحالة النشطة'],
    ['Probability Weight','وزن الاحتمال'],
    ['Modeled','محاكاة'],
    ['Volatility shift','تغير التذبذب'],
    ['Correlation change','تغير الارتباط'],
    ['Macro narrative dominance flip','تحول السرد الكلي المهيمن'],
    ['Liquidity contraction event','حدث انكماش السيولة'],
    ['days','أيام'],

    // صفحة الذكاء
    ['Liquidity Sweep','سحب سيولة'],
    ['Displacement','اندفاع قوي'],
    ['Order Block','منطقة أمرية'],
    ['Inefficiency','عدم كفاءة سعرية'],
    ['Trap Zone','منطقة فخ'],
    ['1H equal lows at 65,200 swept then reclaimed','تم سحب قيعان متساوية على إطار ساعة عند 65,200 ثم استعاد السعر المنطقة'],
    ['Strong impulsive candle from 65,400 → 66,800','شمعة اندفاع قوية من 65,400 إلى 66,800'],
    ['Bearish OB at 1.2680 untested → tagged → respected','منطقة أمرية هابطة عند 1.2680 لم تختبر ثم تم احترامها'],
    ['Buy-side liquidity stacked above 2,360','سيولة شرائية متراكمة أعلى 2,360'],
    ['Stop-hunt below local liquidity pool followed by aggressive reclaim — controlled fingerprints.','اصطياد وقف أسفل تجمع سيولة محلي تبعه استرداد قوي، وهي بصمة تموضع محكوم.'],
    ['Imbalanced move signals positioning shift. Often precedes continuation.','حركة غير متوازنة تشير إلى تحول في التموضع، وغالبًا تسبق استمرار الاتجاه.'],
    ['Last bullish candle before displacement acted as supply, confirming bearish structure.','آخر شمعة صاعدة قبل الاندفاع عملت كمنطقة عرض وأكدت البنية الهابطة.'],
    ['High probability of sweep-then-reverse if narrative weakens.','احتمال مرتفع لسحب السيولة ثم الانعكاس إذا ضعف السرد.'],
    ['Extreme net-short','تمركز بيعي حاد'],
    ['Sustained net-long','تمركز شرائي مستمر'],
    ['Accumulation pace','وتيرة التجميع'],
    ['Net inflow streak','سلسلة تدفقات داخلة'],
    ['Structural bid','دعم هيكلي'],
    ['Whales','محافظ كبيرة'],
    ['Central Banks · Gold','البنوك المركزية · الذهب'],
    ['Central Bank Gold','تجميع ذهب البنوك المركزية'],
    ['ETF Flows · BTC','تدفقات الصناديق · BTC'],
    ['Bitcoin ETF Net Inflows','تدفقات بيتكوين الصافية'],
    ['Fed Pause Priced In','تسعير توقف الفيدرالي'],
    ['ECB Dovish Pivot Lagging Fed','تحول أوروبي ميسّر متأخر عن الفيدرالي'],
    ['China Stimulus Reflation','تحفيز الصين وإعادة التضخم'],
    ['Structural Demand','طلب هيكلي'],
    ['STRUCTURAL DEMAND','طلب هيكلي'],
    ['Structural Bid','دعم هيكلي'],
    ['STRUCTURAL BID','دعم هيكلي'],
    ['Commodity Tailwind','دعم من السلع'],
    ['COMMODITY TAILWIND','دعم من السلع'],
    ['Positioning','التموضع'],
    ['POSITIONING','التموضع'],
    ['commercials net-short -28k contracts','تمركز بيعي صافي بمقدار 28 ألف عقد'],
    ['Smart money positioning extreme — historically precedes 4-8 week downside.','تموضع الأموال الذكية عند مستوى متطرف، وغالبًا يسبق ضغطًا هابطًا خلال 4 إلى 8 أسابيع.'],

    // صفحة بنية البيانات
    ['Failover','المسار الاحتياطي'],
    ['failover','المسار الاحتياطي'],
    ['over فشل','المسار الاحتياطي'],
    ['فشل over','المسار الاحتياطي'],
    ['over degraded','مسار متدهور'],
    ['degraded','متدهور'],
    ['DEGRADED','متدهور'],
    ['Provider','مزود البيانات'],
    ['Providers','مزودو البيانات'],
    ['Connected','متصل'],
    ['AVG latency','متوسط زمن الاستجابة'],
    ['Average Latency','متوسط زمن الاستجابة'],
    ['Across active feeds','عبر القنوات النشطة'],
    ['Completeness AVG','متوسط الاكتمال'],
    ['Last 24h','آخر 24 ساعة'],
    ['Health','الصحة'],
    ['Freshness','حداثة البيانات'],
    ['Latency','زمن الاستجابة'],
    ['Completeness','الاكتمال'],
    ['Coverage','التغطية'],
    ['Market Data WS','قناة بيانات السوق'],
    ['Market Data','بيانات السوق'],
    ['On-Chain Stream','قناة بيانات السلسلة'],
    ['Macro Polling','تحديث البيانات الكلية'],
    ['Weekly Batch','دفعة أسبوعية'],
    ['Sentiment Stream','قناة المعنويات'],
    ['msg/min','رسالة/دقيقة'],
    ['Next:','التالي:'],
    ['us-east, us-west, eu-west, eu-central, ap-northeast','شرق الولايات المتحدة، غرب الولايات المتحدة، غرب أوروبا، وسط أوروبا، شمال شرق آسيا'],
    ['us-east','شرق الولايات المتحدة'],
    ['us-west','غرب الولايات المتحدة'],
    ['eu-west','غرب أوروبا'],
    ['eu-central','وسط أوروبا'],
    ['ap-northeast','شمال شرق آسيا'],

    // أسماء مصادر عامة: لا تظهر للمستخدم العام
    ['Binance Spot ↔ Coinbase Pro','مزود أسعار مباشر ↔ مزود أسعار احتياطي'],
    ['TwelveData ↔ Polygon.io','مزود بيانات السوق ↔ مزود مؤشرات'],
    ['Glassnode','مزود بيانات السلسلة'],
    ['Binance Spot','مزود أسعار مباشر'],
    ['Coinbase Pro','مزود أسعار احتياطي'],
    ['Coinbase','مزود أسعار احتياطي'],
    ['TwelveData','مزود بيانات السوق'],
    ['Polygon.io','مزود مؤشرات'],
    ['Quant','مزود تحليلي'],

    // أزرار وقوائم
    ['Pages','الصفحات'],
    ['Home','الصفحة الرئيسية'],
    ['Login','تسجيل الدخول'],
    ['Create new user','تسجيل مستخدم جديد'],
    ['System admin','مدير النظام'],
    ['System owner','مالك النظام'],
    ['System Online','النظام متاح'],
    ['Markets Live','الأسواق مباشرة'],
    ['Secure Access','وصول آمن'],
    ['Session','جلسة'],
    ['APR','أبريل'],
    ['Last 24H','آخر 24 ساعة'],
    ['Last 24h','آخر 24 ساعة'],
    ['All','الكل'],
    ['Indices','المؤشرات'],
    ['Commodities','السلع'],
    ['Forex','الفوركس'],
    ['Crypto','العملات الرقمية'],
    ['Price','السعر'],
    ['Class','الفئة'],
    ['Symbol','الرمز'],
    ['Phase','المرحلة'],
    ['Assets','الأصول'],
    ['Instruments','الأصول']
  ];

  function escapeReg(s){
    return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function flexibleReplace(text, from, to){
    const parts = String(from).trim().split(/\s+/).map(escapeReg);
    const re = new RegExp(parts.join('\\s+'), 'gi');
    return text.replace(re, to);
  }

  function translateText(value){
    if (!isArabic()) return value;

    let s = String(value || '');
    if (!s.trim()) return s;
    if (isProtectedSymbol(s)) return s;

    exact
      .slice()
      .sort((a,b) => b[0].length - a[0].length)
      .forEach(([from,to]) => {
        if (!from || isProtectedSymbol(from)) return;
        s = flexibleReplace(s, from, to);
      });

    // تنظيف بقايا الترجمة الجزئية والحرف S
    s = s.replace(/([\u0600-\u06FF])\s*[,،]\s*[sS]\s*[,،]?\s*([\u0600-\u06FF])/g, '$1 و$2');
    s = s.replace(/([\u0600-\u06FF])\s+[sS]\s+([\u0600-\u06FF])/g, '$1 و$2');
    s = s.replace(/حد التداول\s*[،,]?\s*[sS]\s*التراجع/g, 'حد التداول والتراجع');
    s = s.replace(/التداول\s*[،,]?\s*[sS]\s*التراجع/g, 'التداول والتراجع');
    s = s.replace(/over\s*فشل/g, 'المسار الاحتياطي');
    s = s.replace(/فشل\s*over/g, 'المسار الاحتياطي');
    s = s.replace(/\bover\b/g, 'المسار الاحتياطي');

    // عبارات متبقية مركبة
    s = s.replace(/Scenario\s+Analysis\s*&\s*What-If\s+Simulation/gi, 'تحليل السيناريوهات ومحاكاة ماذا لو');
    s = s.replace(/Final\s+Outputs\s*&\s*Engine\s+Dependency\s+Chain/gi, 'مخرجات القرار النهائية وسلسلة اعتماد المحركات');
    s = s.replace(/Smart\s+Money\s*\+\s*Narrative\s+Reasoning\s+Layer/gi, 'طبقة الأموال الذكية والسرد التحليلي');
    s = s.replace(/Modular\s+Providers\s+Health/gi, 'صحة مزودي البيانات');
    s = s.replace(/Macro\s*\/\s*Narrative\s+Context/gi, 'السياق الكلي والسردي');

    s = s.replace(/\s{2,}/g, ' ');
    s = s.replace(/\s+،/g, '،');
    s = s.replace(/،\s*،/g, '،');
    return s;
  }

  function forceKnownHeadings(){
    if (!isArabic()) return;

    document.querySelectorAll('h1,h2,h3,[class*="title"],[class*="heading"]').forEach(el => {
      const raw = (el.textContent || '').replace(/\s+/g, ' ').trim();
      if (!raw) return;

      if (/Scenario Analysis|What-If|Simulation/i.test(raw)) {
        el.textContent = 'تحليل السيناريوهات ومحاكاة ماذا لو';
      } else if (/Final Outputs|Engine Dependency Chain/i.test(raw)) {
        el.textContent = 'مخرجات القرار النهائية وسلسلة اعتماد المحركات';
      } else if (/Smart Money|Narrative Reasoning/i.test(raw)) {
        el.textContent = 'طبقة الأموال الذكية والسرد التحليلي';
      } else if (/Modular Providers|Failover|Health/i.test(raw)) {
        el.textContent = 'صحة مزودي البيانات والمسار الاحتياطي';
      } else if (/Controls|Compliance|Kill-Switch/i.test(raw)) {
        el.textContent = 'حدود التحكم والامتثال وإيقاف الطوارئ';
      } else {
        const fixed = translateText(raw);
        if (fixed !== raw) el.textContent = fixed;
      }
    });
  }

  function translateDOM(){
    if (!document.body || !isArabic()) return;

    document.documentElement.lang = 'ar';
    document.documentElement.dir = 'rtl';

    forceKnownHeadings();

    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode(node){
        const p = node.parentElement;
        if (!p) return NodeFilter.FILTER_REJECT;
        if (p.closest('script,style,noscript,textarea,code,pre')) return NodeFilter.FILTER_REJECT;
        if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });

    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);

    nodes.forEach(node => {
      const oldText = node.nodeValue;
      const newText = translateText(oldText);
      if (newText !== oldText) node.nodeValue = newText;
    });

    ['placeholder','title','aria-label','alt','value'].forEach(attr => {
      document.querySelectorAll('[' + attr + ']').forEach(el => {
        const oldVal = el.getAttribute(attr);
        const newVal = translateText(oldVal);
        if (newVal !== oldVal) el.setAttribute(attr, newVal);
      });
    });

    forceKnownHeadings();
  }

  let busy = false;
  function run(){
    if (busy) return;
    busy = true;
    try { translateDOM(); }
    finally { setTimeout(() => { busy = false; }, 80); }
  }

  function boot(){
    run();
    [150,400,900,1500,2500,4000,6500].forEach(ms => setTimeout(run, ms));

    const obs = new MutationObserver(() => {
      if (isArabic()) setTimeout(run, 120);
    });

    obs.observe(document.documentElement, {
      childList:true,
      subtree:true,
      characterData:true
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
