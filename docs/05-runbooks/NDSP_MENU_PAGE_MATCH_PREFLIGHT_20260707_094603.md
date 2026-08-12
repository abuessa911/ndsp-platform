# NDSP Menu Page Match Preflight
DATE=2026-07-07T09:46:03+02:00

## 1) Current frontend HTML files
alerts-log.html
asset-selector.html
completed-decisions.html
daily-brief.html
decision-center.html
decision-guide.html
decision-modes-guide.html
decision-radar.html
disclaimer.html
dollar-impact.html
dollar-news.html
index.html
my-watchlist.html
nmp.html
pro-guide.html
settings.html
support-center.html
usd-pulse.html
user-guide.html

## 2) Current global menu file
-rw-rw-r-- 1 nawaf511 nawaf511 9.7K يوليو   5 18:58 /var/www/ndsp-my/assets/ndsp-global-menu.js

## 3) Global menu content snapshot
     1	/* NDSP_MENU_PAGE_NAMES_MATCH_V24 */
     2	/*
     3	  Purpose:
     4	  - Match menu labels with actual page identities.
     5	  - Do not hide content.
     6	  - Do not clean JSON.
     7	  - Do not touch radar rendering.
     8	  - Do not modify backend/PM2/Nginx.
     9	*/
    10	(function(){
    11	  if(window.NDSP_GLOBAL_MENU_V24_BOOTED) return;
    12	  window.NDSP_GLOBAL_MENU_V24_BOOTED = true;
    13	
    14	  function lang(){
    15	    var saved = "";
    16	    try { saved = localStorage.getItem("ndsp_lang") || ""; } catch(e){}
    17	    var htmlLang = document.documentElement.lang || "";
    18	    return (saved || htmlLang || "ar").toLowerCase().startsWith("en") ? "en" : "ar";
    19	  }
    20	
    21	  function symbol(){
    22	    try{
    23	      return new URL(location.href).searchParams.get("symbol") || "BTCUSDT";
    24	    }catch(e){
    25	      return "BTCUSDT";
    26	    }
    27	  }
    28	
    29	  function pageMap(){
    30	    return {
    31	      "/asset-selector.html": {
    32	        ar:"الأسواق والأصول",
    33	        en:"Markets & Assets",
    34	        subAr:"اختيار السوق والأصل",
    35	        subEn:"Choose market and asset"
    36	      },
    37	      "/decision-center.html": {
    38	        ar:"مركز القرار",
    39	        en:"Decision Center",
    40	        subAr:"قراءة القرار والتفسير",
    41	        subEn:"Decision reading and explanation"
    42	      },
    43	      "/decision-radar.html": {
    44	        ar:"الرادار",
    45	        en:"Premium Decision Radar",
    46	        subAr:"الرادار الذهبي وحالة القرار",
    47	        subEn:"Golden radar and decision state"
    48	      },
    49	      "/completed-decisions.html": {
    50	        ar:"سجل القرار",
    51	        en:"Decision Journal",
    52	        subAr:"ذاكرة القرار وتغير الجودة",
    53	        subEn:"Decision memory and quality changes"
    54	      },
    55	      "/decision-guide.html": {
    56	        ar:"دليل القرار",
    57	        en:"Decision Guide",
    58	        subAr:"شرح قراءة القرار",
    59	        subEn:"How to read the decision"
    60	      },
    61	      "/user-guide.html": {
    62	        ar:"دليل المستخدم",
    63	        en:"User Guide",
    64	        subAr:"استخدام المنصة خطوة بخطوة",
    65	        subEn:"How to use the platform"
    66	      },
    67	      "/pro-guide.html": {
    68	        ar:"دليل المحترف",
    69	        en:"Professional Guide",
    70	        subAr:"قراءة مؤسسية متقدمة",
    71	        subEn:"Advanced institutional reading"
    72	      },
    73	      "/decision-modes-guide.html": {
    74	        ar:"أنماط المستخدم",
    75	        en:"User Modes",
    76	        subAr:"مبتدئ ومحترف ومؤسسي",
    77	        subEn:"Beginner, Pro, Institutional"
    78	      },
    79	      "/usd-pulse.html": {
    80	        ar:"نبض الدولار",
    81	        en:"USD Pulse",
    82	        subAr:"حالة الدولار والماكرو",
    83	        subEn:"Dollar and macro state"
    84	      },
    85	      "/dollar-news.html": {
    86	        ar:"أخبار الدولار",
    87	        en:"Dollar News",
    88	        subAr:"الأخبار المؤثرة على الدولار",
    89	        subEn:"Dollar-impacting news"
    90	      },
    91	      "/dollar-impact.html": {
    92	        ar:"أثر الدولار",
    93	        en:"Dollar Impact",
    94	        subAr:"أثر الدولار على الأصول",
    95	        subEn:"Dollar impact on assets"
    96	      },
    97	      "/my-watchlist.html": {
    98	        ar:"قائمة المتابعة",
    99	        en:"Watchlist",
   100	        subAr:"الأصول التي تتابعها",
   101	        subEn:"Assets you follow"
   102	      },
   103	      "/alerts-log.html": {
   104	        ar:"سجل التنبيهات",
   105	        en:"Alerts Log",
   106	        subAr:"تنبيهات المتابعة",
   107	        subEn:"Monitoring alerts"
   108	      },
   109	      "/settings.html": {
   110	        ar:"الإعدادات",
   111	        en:"Settings",
   112	        subAr:"تفضيلات المستخدم والتنبيهات",
   113	        subEn:"User and alert preferences"
   114	      },
   115	      "/support-center.html": {
   116	        ar:"الدعم",
   117	        en:"Support Center",
   118	        subAr:"المساعدة والتواصل",
   119	        subEn:"Help and support"
   120	      },
   121	      "/daily-brief.html": {
   122	        ar:"الموجز اليومي",
   123	        en:"Daily Brief",
   124	        subAr:"ملخص يومي للأسواق",
   125	        subEn:"Daily market brief"
   126	      },
   127	      "/nmp.html": {
   128	        ar:"NMP",
   129	        en:"NMP",
   130	        subAr:"منطقة الالتقاء الحرجة",
   131	        subEn:"Critical meet point"
   132	      }
   133	    };
   134	  }
   135	
   136	  function activePath(){
   137	    var p = location.pathname || "/asset-selector.html";
   138	    if(p === "/" || p === "/index.html") return "/asset-selector.html";
   139	    return p;
   140	  }
   141	
   142	  function label(item){
   143	    return lang() === "ar" ? item.ar : item.en;
   144	  }
   145	
   146	  function sub(item){
   147	    return lang() === "ar" ? item.subAr : item.subEn;
   148	  }
   149	
   150	  function T(){
   151	    var ar = lang() === "ar";
   152	    return {
   153	      menu: ar ? "القائمة" : "Menu",
   154	      close: ar ? "إغلاق" : "Close",
   155	      brandSmall:"NDSP COMMAND",
   156	      brand: ar ? "التنقل" : "Navigation",
   157	      main: ar ? "الرئيسية" : "Main",
   158	      decision: ar ? "مسار القرار" : "Decision Flow",
   159	      macro: ar ? "الماكرو والدولار" : "Macro & USD",
   160	      follow: ar ? "المتابعة" : "Follow-up",
   161	      guides: ar ? "الأدلة والدعم" : "Guides & Support",
   162	      note: ar
   163	        ? "أسماء القائمة مطابقة لهوية الصفحات. NDSP منصة دعم قرار وليست توصية مالية أو أمر تنفيذ."
   164	        : "Menu labels match page identities. NDSP is a decision-support platform, not financial advice or execution instruction."
   165	    };
   166	  }
   167	
   168	  function href(path){
   169	    var s = symbol();
   170	    if(path === "/decision-center.html" || path === "/decision-radar.html"){
   171	      return path + "?symbol=" + encodeURIComponent(s);
   172	    }
   173	    return path;
   174	  }
   175	
   176	  function link(path, primary){
   177	    var map = pageMap();
   178	    var item = map[path];
   179	    if(!item) return "";
   180	
   181	    var active = activePath() === path ? " active" : "";
   182	    return '<a class="ndsp-menu-link '+(primary?'primary':'')+active+'" href="'+href(path)+'">' +
   183	      '<span><b>'+label(item)+'</b><small>'+sub(item)+'</small></span>' +
   184	      '<span class="arrow">›</span>' +
   185	    '</a>';
   186	  }
   187	
   188	  function updateDocumentTitle(){
   189	    var item = pageMap()[activePath()];
   190	    if(item){
   191	      document.title = "NDSP — " + label(item);
   192	      document.documentElement.setAttribute("data-ndsp-page-name", label(item));
   193	    }
   194	  }
   195	
   196	  function build(){
   197	    updateDocumentTitle();
   198	
   199	    document.querySelectorAll(".ndsp-menu-button,.ndsp-menu-backdrop,.ndsp-menu-panel").forEach(function(el){
   200	      el.remove();
   201	    });
   202	
   203	    var t = T();
   204	
   205	    var btn = document.createElement("button");
   206	    btn.className = "ndsp-menu-button";
   207	    btn.type = "button";
   208	    btn.setAttribute("aria-label", t.menu);
   209	    btn.innerHTML = '<span class="bars"><span></span></span><span>'+t.menu+'</span>';
   210	
   211	    var backdrop = document.createElement("div");
   212	    backdrop.className = "ndsp-menu-backdrop";
   213	
   214	    var panel = document.createElement("nav");
   215	    panel.className = "ndsp-menu-panel";
   216	    panel.setAttribute("aria-label", t.menu);
   217	
   218	    panel.innerHTML =
   219	      '<div class="ndsp-menu-head">' +
   220	        '<div class="ndsp-menu-brand">' +
   221	          '<div class="ndsp-menu-mark">ND</div>' +
   222	          '<div><small>'+t.brandSmall+'</small><b>'+t.brand+'</b></div>' +
   223	        '</div>' +
   224	        '<button class="ndsp-menu-close" type="button" aria-label="'+t.close+'">×</button>' +
   225	      '</div>' +
   226	
   227	      '<div class="ndsp-menu-group">' +
   228	        '<p class="ndsp-menu-group-title">'+t.main+'</p>' +
   229	        '<div class="ndsp-menu-links">' +
   230	          link("/asset-selector.html", true) +
   231	        '</div>' +
   232	      '</div>' +
   233	
   234	      '<div class="ndsp-menu-group">' +
   235	        '<p class="ndsp-menu-group-title">'+t.decision+'</p>' +
   236	        '<div class="ndsp-menu-links">' +
   237	          link("/decision-center.html", false) +
   238	          link("/decision-radar.html", false) +
   239	          link("/completed-decisions.html", false) +
   240	        '</div>' +
   241	      '</div>' +
   242	
   243	      '<div class="ndsp-menu-group">' +
   244	        '<p class="ndsp-menu-group-title">'+t.macro+'</p>' +
   245	        '<div class="ndsp-menu-links">' +
   246	          link("/usd-pulse.html", false) +
   247	          link("/dollar-news.html", false) +
   248	          link("/dollar-impact.html", false) +
   249	          link("/daily-brief.html", false) +
   250	        '</div>' +
   251	      '</div>' +
   252	
   253	      '<div class="ndsp-menu-group">' +
   254	        '<p class="ndsp-menu-group-title">'+t.follow+'</p>' +
   255	        '<div class="ndsp-menu-links">' +
   256	          link("/my-watchlist.html", false) +
   257	          link("/alerts-log.html", false) +
   258	          link("/settings.html", false) +
   259	        '</div>' +
   260	      '</div>' +

## 4) Page titles / H1 snapshot
--- alerts-log.html ---
<title>NDSP — سجل التنبيهات
<h1>Alerts Log

--- asset-selector.html ---
<title>NDSP — Markets & Assets
<h1 data-i18n="title">الأسواق والأصول

--- completed-decisions.html ---
<title>NDSP — سجل القرار
<h1>Decision Journal

--- daily-brief.html ---
<title>NDSP — موجز اليوم
<h1>Daily Intelligence Brief

--- decision-center.html ---
<title>NDSP — مركز القرار
<h1>Decision Brief

--- decision-guide.html ---
<title>NDSP — الدليل
<h1>NDSP Academy

--- decision-modes-guide.html ---
<title>NDSP — أنماط القرار
<h1>Decision Modes

--- decision-radar.html ---
<title>NDSP — رادار القرار
<h1>Premium Decision Radar

--- disclaimer.html ---
<title>NDSP — إخلاء المسؤولية
<h1>إخلاء المسؤولية

--- dollar-impact.html ---
<title>NDSP — أثر الدولار
<h1>Dollar Impact

--- dollar-news.html ---
<title>NDSP — أخبار الدولار
<h1>Dollar News

--- index.html ---
<title>NDSP

--- my-watchlist.html ---
<title>NDSP — قائمة المتابعة
<h1>Watchlist

--- nmp.html ---
<title>NDSP — NMP
<h1>NMP Intelligence

--- pro-guide.html ---
<title>NDSP — دليل المحترف
<h1>Professional Guide

--- settings.html ---
<title>NDSP — الإعدادات
<h1>Settings & Alerts

--- support-center.html ---
<title>NDSP — مركز الدعم
<h1>Support Center

--- usd-pulse.html ---
<title>NDSP — نبض الدولار
<h1>USD Pulse

--- user-guide.html ---
<title>NDSP — دليل المستخدم
<h1>User Modes

## 5) Official route HTTP checks
[200] size=874 https://my.ndsp.app/
[200] size=874 https://my.ndsp.app/index.html
[200] size=874 https://my.ndsp.app/decision-support.html
[200] size=874 https://my.ndsp.app/NDSP_Asset_View.html
[200] size=874 https://my.ndsp.app/NDSP_Command_Center.html
[200] size=874 https://my.ndsp.app/NDSP_Daily_Brief.html
[200] size=874 https://my.ndsp.app/NDSP_Settings_Alerts.html
[200] size=4677 https://my.ndsp.app/disclaimer.html

## 6) Duplicate menu/gate scripts scan
/var/www/ndsp-my/alerts-log.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/alerts-log.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>Alerts Log</h1><p>تنبيهات NDSP.</p></section><section class="brief-grid"><article class="card"><h3>النمط الحاكم</h3><span>قراءة مؤسسية مختصرة.</span></article><article class="card"><h3>تغير الجودة</h3><span>يتحول لاحقًا إلى سجل زمني.</span></article><article class="card"><h3>محامي الشيطان</h3><span>سبب التحذير أو المنع.</span></article><article class="card"><h3>Hidden Consensus</h3><span>إجماع المحركات المخفية كمؤشر فقط.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/asset-selector.html:14:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/asset-selector.html:61:    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/completed-decisions.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/completed-decisions.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>Decision Journal</h1><p>ذاكرة القرار وتغير الجودة.</p></section><section class="brief-grid"><article class="card"><h3>النمط الحاكم</h3><span>قراءة مؤسسية مختصرة.</span></article><article class="card"><h3>تغير الجودة</h3><span>يتحول لاحقًا إلى سجل زمني.</span></article><article class="card"><h3>محامي الشيطان</h3><span>سبب التحذير أو المنع.</span></article><article class="card"><h3>Hidden Consensus</h3><span>إجماع المحركات المخفية كمؤشر فقط.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/daily-brief.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/daily-brief.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>Daily Intelligence Brief</h1><p>موجز الأسواق.</p></section><section class="brief-grid"><article class="card"><h3>النمط الحاكم</h3><span>قراءة مؤسسية مختصرة.</span></article><article class="card"><h3>تغير الجودة</h3><span>يتحول لاحقًا إلى سجل زمني.</span></article><article class="card"><h3>محامي الشيطان</h3><span>سبب التحذير أو المنع.</span></article><article class="card"><h3>Hidden Consensus</h3><span>إجماع المحركات المخفية كمؤشر فقط.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/decision-center.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/decision-center.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>Decision Brief</h1><p>تقرير قرار مؤسسي.</p></section><section class="brief-grid"><article class="card"><h3>النمط الحاكم</h3><span>قراءة مؤسسية مختصرة.</span></article><article class="card"><h3>تغير الجودة</h3><span>يتحول لاحقًا إلى سجل زمني.</span></article><article class="card"><h3>محامي الشيطان</h3><span>سبب التحذير أو المنع.</span></article><article class="card"><h3>Hidden Consensus</h3><span>إجماع المحركات المخفية كمؤشر فقط.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/decision-guide.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/decision-guide.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>NDSP Academy</h1><p>شرح أنماط المستخدم وأنماط القرار.</p></section><section class="brief-grid"><article class="card"><h3>Beginner</h3><span>خلاصة بسيطة.</span></article><article class="card"><h3>Pro</h3><span>TDL وNMP والدولار والمخاطر.</span></article><article class="card"><h3>Institutional</h3><span>مقارنة الأصول وتغير الجودة والسجل.</span></article><article class="card"><h3>Owner</h3><span>وضع داخلي للمالك.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/decision-modes-guide.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/decision-modes-guide.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>Decision Modes</h1><p>Investor / Tactical / Intraday / Research.</p></section><section class="brief-grid"><article class="card"><h3>Beginner</h3><span>خلاصة بسيطة.</span></article><article class="card"><h3>Pro</h3><span>TDL وNMP والدولار والمخاطر.</span></article><article class="card"><h3>Institutional</h3><span>مقارنة الأصول وتغير الجودة والسجل.</span></article><article class="card"><h3>Owner</h3><span>وضع داخلي للمالك.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/decision-radar.html:4:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/decision-radar.html:5:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>Premium Decision Radar</h1><p>رادار فخم يتلون حسب حالة الأصل.</p></section><section class="radar-layout"><div class="radar-box"><div class="radar"><div class="core"><span data-live-state>Loading</span></div><div class="node n1">TDL</div><div class="node n2">NMP</div><div class="node n3">USD Macro</div><div class="node n4">Risk</div><div class="node n5">Devil Gate</div><div class="node n6">Hidden Consensus</div></div><div class="notice">الأصل: <b data-selected-symbol>ETHUSDT</b> — السعر: <b data-live-price>تحميل</b></div></div><div class="brief-box"><h2>Premium Decision Radar</h2><div class="brief-grid"><article class="card"><h3>Decision Core</h3><span data-live-state>تحميل</span></article><article class="card"><h3>Decision Quality</h3><span>مؤشر جودة القرار.</span></article><article class="card"><h3>Devil’s Advocate</h3><span>الطبقة الوحيدة التي يسمح لها بالمنع.</span></article><article class="card"><h3>Scenario Levels</h3><span>Activation / Arrival / Review / Invalidation</span></article></div><div class="notice">قراءة JSON الحية:</div><pre data-live-json>تحميل...</pre></div></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>  <script src="/assets/ndsp-radar-safe-clean.js?v=23"></script>
/var/www/ndsp-my/decision-radar.html:6:  <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/dollar-impact.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/dollar-impact.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>Dollar Impact</h1><p>الأثر الكلي.</p></section><section class="brief-grid"><article class="card"><h3>النمط الحاكم</h3><span>قراءة مؤسسية مختصرة.</span></article><article class="card"><h3>تغير الجودة</h3><span>يتحول لاحقًا إلى سجل زمني.</span></article><article class="card"><h3>محامي الشيطان</h3><span>سبب التحذير أو المنع.</span></article><article class="card"><h3>Hidden Consensus</h3><span>إجماع المحركات المخفية كمؤشر فقط.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/dollar-news.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/dollar-news.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>Dollar News</h1><p>الأخبار المؤثرة.</p></section><section class="brief-grid"><article class="card"><h3>النمط الحاكم</h3><span>قراءة مؤسسية مختصرة.</span></article><article class="card"><h3>تغير الجودة</h3><span>يتحول لاحقًا إلى سجل زمني.</span></article><article class="card"><h3>محامي الشيطان</h3><span>سبب التحذير أو المنع.</span></article><article class="card"><h3>Hidden Consensus</h3><span>إجماع المحركات المخفية كمؤشر فقط.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/index.html:10:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/index.html:15:    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/my-watchlist.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/my-watchlist.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>Watchlist</h1><p>متابعة الأصول.</p></section><section class="controls"><div class="control"><label>الأسواق</label><div class="pills" data-market-pills></div></div><div class="control"><label>نمط المستخدم</label><div class="pills"><button class="pill active">Beginner</button><button class="pill">Pro</button><button class="pill">Institutional</button><button class="pill">Owner</button></div></div><div class="control"><label>نمط القرار</label><div class="pills"><button class="pill active">Investor</button><button class="pill">Tactical Weekly</button><button class="pill">Intraday Watch</button><button class="pill">Research</button></div></div></section><section class="grid4"><article class="card"><h3>الأصول المغطاة</h3><div class="big" data-count-assets>50+</div><span>أكثر من سوق داخل غرفة واحدة.</span></article><article class="card"><h3>Hidden Consensus</h3><div class="big" data-hidden-avg>--</div><span>إجماع داخلي دون كشف أسماء المحركات.</span></article><article class="card"><h3>Decision Quality</h3><div class="big">Live</div><span>جودة القرار لكل أصل.</span></article><article class="card"><h3>Devil’s Advocate</h3><div class="big">Gate</div><span>بوابة المنع الوحيدة.</span></article></section><section class="table-wrap"><div class="table-head"><b>Asset Intelligence Matrix</b><span>مقارنة مؤسسية للأصول والأسواق</span></div><table><thead><tr><th>Asset</th><th>Market</th><th>Price</th><th>Decision</th><th>Scenario</th><th>Quality</th><th>NMP</th><th>USD</th><th>Devil</th><th>Hidden</th><th>Action</th></tr></thead><tbody data-assets-body></tbody></table></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/nmp.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/nmp.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>NMP Intelligence</h1><p>منطقة الالتقاء الحرجة.</p></section><section class="brief-grid"><article class="card"><h3>النمط الحاكم</h3><span>قراءة مؤسسية مختصرة.</span></article><article class="card"><h3>تغير الجودة</h3><span>يتحول لاحقًا إلى سجل زمني.</span></article><article class="card"><h3>محامي الشيطان</h3><span>سبب التحذير أو المنع.</span></article><article class="card"><h3>Hidden Consensus</h3><span>إجماع المحركات المخفية كمؤشر فقط.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/pro-guide.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/pro-guide.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>Professional Guide</h1><p>قراءة احترافية للطبقات.</p></section><section class="brief-grid"><article class="card"><h3>Beginner</h3><span>خلاصة بسيطة.</span></article><article class="card"><h3>Pro</h3><span>TDL وNMP والدولار والمخاطر.</span></article><article class="card"><h3>Institutional</h3><span>مقارنة الأصول وتغير الجودة والسجل.</span></article><article class="card"><h3>Owner</h3><span>وضع داخلي للمالك.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/settings.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/settings.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>Settings & Alerts</h1><p>إعدادات العرض والتنبيهات.</p></section><section class="brief-grid"><article class="card"><h3>Beginner</h3><span>خلاصة بسيطة.</span></article><article class="card"><h3>Pro</h3><span>TDL وNMP والدولار والمخاطر.</span></article><article class="card"><h3>Institutional</h3><span>مقارنة الأصول وتغير الجودة والسجل.</span></article><article class="card"><h3>Owner</h3><span>وضع داخلي للمالك.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/support-center.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/support-center.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>Support Center</h1><p>مساعدة وملاحظات.</p></section><section class="brief-grid"><article class="card"><h3>Beginner</h3><span>خلاصة بسيطة.</span></article><article class="card"><h3>Pro</h3><span>TDL وNMP والدولار والمخاطر.</span></article><article class="card"><h3>Institutional</h3><span>مقارنة الأصول وتغير الجودة والسجل.</span></article><article class="card"><h3>Owner</h3><span>وضع داخلي للمالك.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/usd-pulse.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/usd-pulse.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>USD Pulse</h1><p>أثر الدولار.</p></section><section class="brief-grid"><article class="card"><h3>النمط الحاكم</h3><span>قراءة مؤسسية مختصرة.</span></article><article class="card"><h3>تغير الجودة</h3><span>يتحول لاحقًا إلى سجل زمني.</span></article><article class="card"><h3>محامي الشيطان</h3><span>سبب التحذير أو المنع.</span></article><article class="card"><h3>Hidden Consensus</h3><span>إجماع المحركات المخفية كمؤشر فقط.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>
/var/www/ndsp-my/user-guide.html:3:  <script src="/assets/ndsp-disclaimer-gate.js?v=1"></script>
/var/www/ndsp-my/user-guide.html:4:</head><body><div class="shell"><aside class="sidebar"><div class="brand"><b>NDSP</b><span>Nawaf Decision Support Platform<br>Private Decision Intelligence Terminal</span></div><nav class="nav"><div data-nav></div></nav></aside><main class="main"><section class="mobile"><div class="mobile-head"><div><b>NDSP</b><span>تنقل مباشر للجوال</span></div><div class="mobile-badge">ND</div></div><nav class="mobile-nav"><div data-nav></div></nav></section><section class="topbar"><div class="metric"><small>USD Pulse</small><strong>محايد مراقب</strong></div><div class="metric"><small>Data Freshness</small><strong>Live / Mixed</strong></div><div class="metric"><small>Risk Climate</small><strong>حذر مؤسسي</strong></div><div class="metric"><small>Coverage</small><strong data-count-assets>50+</strong></div></section><section class="hero"><div class="kicker">NDSP PREMIUM INTELLIGENCE</div><h1>User Modes</h1><p>Beginner / Pro / Institutional / Owner.</p></section><section class="brief-grid"><article class="card"><h3>Beginner</h3><span>خلاصة بسيطة.</span></article><article class="card"><h3>Pro</h3><span>TDL وNMP والدولار والمخاطر.</span></article><article class="card"><h3>Institutional</h3><span>مقارنة الأصول وتغير الجودة والسجل.</span></article><article class="card"><h3>Owner</h3><span>وضع داخلي للمالك.</span></article></section><div class="notice">NDSP منصة دعم قرار فقط. ليست توصية مالية، وليست أمر شراء أو بيع، وليست نظام تنفيذ تداول.</div></main></div><script src="/assets/premium.js?v=22-restore-radar"></script>    <script src="/assets/ndsp-global-menu.js?v=24-page-match"></script>

FINAL_STATUS=MENU_PAGE_MATCH_PREFLIGHT_DONE
REPORT=docs/05-runbooks/NDSP_MENU_PAGE_MATCH_PREFLIGHT_20260707_094603.md
