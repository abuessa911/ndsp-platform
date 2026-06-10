import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const ROUTES = {
  "/": "home",
  "/index.html": "home",
  "/NDSP_Asset_View.html": "asset",
  "/NDSP_Command_Center.html": "command",
  "/NDSP_Daily_Brief.html": "brief",
  "/NDSP_Settings_Alerts.html": "settings"
};

const I18N = {
  ar: {
    brand: "NDSP — منصة نواف لدعم القرار",
    sub: "بوابة المستخدم",
    home: "المنصة",
    assetView: "عرض الأصل",
    command: "مركز القرار",
    brief: "يوميات القرار",
    settings: "الإعدادات والتنبيهات",
    elite: "النخبة",
    trial: "تجربة ١٦ يوم",
    live: "حي",
    ref: "مرجعي",
    refresh: "تحديث",
    selectAsset: "اختر الأصل",
    platformState: "حالة المنصة",
    activeAsset: "الأصل النشط",
    decisionSummary: "مختصر القرار",
    quickLinks: "روابط سريعة",
    homeNote: "ملخص عام فقط: حالة المنصة، الأصل النشط، مختصر القرار، وروابط سريعة بدون تكرار قائمة المتابعة.",
    assetOnly: "صفحة الأصل فقط",
    price: "السعر",
    marketState: "حالة السوق",
    scenario: "مستويات السيناريو المرجعية",
    reading: "قراءة الأصل",
    arrival: "الوصول",
    review: "المراجعة",
    activation: "التفعيل",
    cancel: "الإلغاء",
    commandOnly: "مركز القرار فقط",
    decisionState: "حالة القرار",
    decisionQuality: "جودة القرار",
    tdl: "منطق البعد الزمني",
    nmp: "نقطة التقاء نواف",
    devil: "محامي الشيطان",
    golden: "إشارة نواف الذهبية",
    noPriceTable: "هذه الصفحة مخصصة لحالة القرار فقط، بدون جدول أسعار كامل.",
    dailyOnly: "يوميات القرار فقط",
    todayLog: "سجل اليوم",
    shortReadings: "قراءات مختصرة",
    lastReviews: "آخر مراجعات",
    settingsOnly: "إعدادات فقط",
    language: "اللغة",
    alerts: "التنبيهات",
    dataSources: "حالة مصادر البيانات",
    noPricesHere: "لا أسعار ولا سيناريوهات داخل صفحة الإعدادات.",
    safe: "المخرجات تفسيرية وليست أوامر تداول.",
    contextualUp: "صعود سياقي",
    contextualDown: "هبوط سياقي",
    extended: "أفق ممتد",
    high: "عالية",
    medium: "متوسطة",
    protected: "محمي",
    botConnector: "ربط البوت الخارجي",
    botPolicy: "البوت يبقى تكاملًا خارجيًا عبر API/Webhook ولا يدخل في قلب NDSP.",
    unavailable: "غير متاح"
  },
  en: {
    brand: "NDSP — Nawaf Decision Support Platform",
    sub: "User Portal",
    home: "Platform",
    assetView: "Asset View",
    command: "Command Center",
    brief: "Decision Journal",
    settings: "Settings & Alerts",
    elite: "Elite",
    trial: "16-day trial",
    live: "LIVE",
    ref: "REF",
    refresh: "Refresh",
    selectAsset: "Select asset",
    platformState: "Platform State",
    activeAsset: "Active Asset",
    decisionSummary: "Decision Summary",
    quickLinks: "Quick Links",
    homeNote: "Summary only: platform state, active asset, decision summary, and quick links without duplicating the full watchlist.",
    assetOnly: "Asset page only",
    price: "Price",
    marketState: "Market State",
    scenario: "Reference Scenario Levels",
    reading: "Asset Reading",
    arrival: "Arrival",
    review: "Review",
    activation: "Activation",
    cancel: "Cancel",
    commandOnly: "Command Center only",
    decisionState: "Decision State",
    decisionQuality: "Decision Quality",
    tdl: "TDL",
    nmp: "NMP",
    devil: "Devil's Advocate",
    golden: "Nawaf Golden Alignment",
    noPriceTable: "This page is dedicated to decision state only, without a full price table.",
    dailyOnly: "Decision journal only",
    todayLog: "Today Log",
    shortReadings: "Short Readings",
    lastReviews: "Last Reviews",
    settingsOnly: "Settings only",
    language: "Language",
    alerts: "Alerts",
    dataSources: "Data Source Status",
    noPricesHere: "No prices or scenarios inside the settings page.",
    safe: "Outputs are explanatory and are not trading orders.",
    contextualUp: "Contextual Up",
    contextualDown: "Contextual Down",
    extended: "Extended Horizon",
    high: "High",
    medium: "Medium",
    protected: "Protected",
    botConnector: "External Bot Connector",
    botPolicy: "The bot remains an external API/Webhook integration and does not enter NDSP core.",
    unavailable: "Unavailable"
  }
};

const ASSETS = [
  { symbol: "XAUUSD", display: "XAU/USD", ar: "الذهب", en: "Gold" },
  { symbol: "EURUSD", display: "EUR/USD", ar: "يورو / دولار", en: "EUR / USD" },
  { symbol: "CLF", display: "WTI", ar: "نفط غرب تكساس", en: "WTI Crude Oil" },
  { symbol: "BTCUSDT", display: "BTC/USD", ar: "بيتكوين", en: "Bitcoin" },
  { symbol: "ETHUSDT", display: "ETH/USD", ar: "إيثريوم", en: "Ethereum" },
  { symbol: "SOLUSDT", display: "SOL/USD", ar: "سولانا", en: "Solana" }
];

function getPage() {
  return ROUTES[window.location.pathname] || "home";
}

function fmt(v, symbol) {
  const n = Number(v);
  if (!Number.isFinite(n)) return "—";
  if (symbol === "EURUSD") return n.toFixed(5);
  if (n >= 1000) return n.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  if (n >= 10) return n.toFixed(2);
  return n.toFixed(4);
}

async function fetchJson(url) {
  const res = await fetch(url, { cache: "no-store", credentials: "same-origin", headers: { Accept: "application/json" } });
  if (!res.ok) throw new Error(`HTTP_${res.status}`);
  return res.json();
}

async function fetchPrice(symbol) {
  const urls = [
    `/api/market/prices?symbol=${encodeURIComponent(symbol)}`,
    `https://api.ndsp.app/api/market/prices?symbol=${encodeURIComponent(symbol)}`
  ];
  for (const url of urls) {
    try {
      const data = await fetchJson(url);
      const rows = Array.isArray(data?.prices) ? data.prices : [];
      const row = rows.find((r) => String(r.symbol || "").toUpperCase() === symbol);
      if (row && String(row.provider_status || "").toLowerCase() === "live" && Number(row.price) > 0) return row;
    } catch {}
  }
  return null;
}

async function fetchScenario(symbol) {
  const urls = [
    `/api/scenario/levels?symbol=${encodeURIComponent(symbol)}`,
    `https://api.ndsp.app/api/scenario/levels?symbol=${encodeURIComponent(symbol)}`
  ];
  for (const url of urls) {
    try {
      const data = await fetchJson(url);
      if (data?.ok === true && data?.levels) return data.levels;
    } catch {}
  }
  return null;
}

function App() {
  const [page, setPage] = useState(getPage());
  const [lang, setLang] = useState(() => localStorage.getItem("ndsp_lang") === "en" ? "en" : "ar");
  const [symbol, setSymbol] = useState(() => localStorage.getItem("ndsp_active_symbol") || "XAUUSD");
  const [price, setPrice] = useState(null);
  const [scenario, setScenario] = useState(null);
  const [prices, setPrices] = useState({});

  const tr = I18N[lang];
  const asset = useMemo(() => ASSETS.find((a) => a.symbol === symbol) || ASSETS[0], [symbol]);
  const assetName = lang === "ar" ? asset.ar : asset.en;

  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
    document.body.dir = document.documentElement.dir;
    localStorage.setItem("ndsp_lang", lang);
  }, [lang]);

  useEffect(() => localStorage.setItem("ndsp_active_symbol", symbol), [symbol]);

  useEffect(() => {
    const onPop = () => setPage(getPage());
    window.addEventListener("popstate", onPop);
    return () => window.removeEventListener("popstate", onPop);
  }, []);

  async function refresh() {
    const p = await fetchPrice(symbol);
    setPrice(p);
    setScenario(await fetchScenario(symbol));

    const collected = {};
    await Promise.all(ASSETS.map(async (a) => {
      const row = await fetchPrice(a.symbol);
      if (row) collected[a.symbol] = row;
    }));
    setPrices(collected);

    window.NDSP_USER_PORTAL_VITE = {
      ok: true,
      stack: "vite-react",
      page,
      lang,
      symbol,
      live_count: Object.keys(collected).length,
      updated_at: new Date().toISOString()
    };
  }

  useEffect(() => {
    refresh();
    const id = setInterval(refresh, 60000);
    return () => clearInterval(id);
  }, [symbol, page, lang]);

  function nav(href) {
    window.history.pushState({}, "", href);
    setPage(getPage());
  }

  return (
    <div className="shell">
      <Header tr={tr} lang={lang} setLang={setLang} page={page} nav={nav} />
      <main>
        {page === "home" && <Home tr={tr} assetName={assetName} asset={asset} price={price} nav={nav} />}
        {page === "asset" && <AssetPage tr={tr} lang={lang} symbol={symbol} setSymbol={setSymbol} assetName={assetName} asset={asset} price={price} scenario={scenario} refresh={refresh} />}
        {page === "command" && <CommandPage tr={tr} price={price} />}
        {page === "brief" && <BriefPage tr={tr} lang={lang} prices={prices} />}
        {page === "settings" && <SettingsPage tr={tr} lang={lang} setLang={setLang} />}
      </main>
      <footer className="footer">{tr.brand} · {tr.safe}</footer>
    </div>
  );
}

function Header({ tr, lang, setLang, page, nav }) {
  const items = [
    ["/index.html", "home", tr.home],
    ["/NDSP_Asset_View.html", "asset", tr.assetView],
    ["/NDSP_Command_Center.html", "command", tr.command],
    ["/NDSP_Daily_Brief.html", "brief", tr.brief],
    ["/NDSP_Settings_Alerts.html", "settings", tr.settings]
  ];

  return (
    <header className="topbar">
      <button className="brand" onClick={() => nav("/index.html")}>
        <div className="logo">N</div>
        <div>
          <div className="brandTitle">{tr.brand}</div>
          <div className="brandSub">{tr.sub}</div>
        </div>
      </button>
      <nav className="nav">
        {items.map(([href, id, label]) => (
          <button key={href} className={page === id ? "active" : ""} onClick={() => nav(href)}>{label}</button>
        ))}
      </nav>
      <div className="actions">
        <span className="pill gold">● {tr.elite}</span>
        <span className="pill">{tr.trial}</span>
        <select className="language" value={lang} onChange={(e) => setLang(e.target.value)} aria-label="language">
          <option value="ar">العربية</option>
          <option value="en">English</option>
        </select>
      </div>
    </header>
  );
}

function Home({ tr, assetName, asset, price, nav }) {
  return (
    <section className="grid heroGrid">
      <Card wide>
        <Kicker>{tr.platformState}</Kicker>
        <h1>{tr.brand}</h1>
        <p className="muted">{tr.homeNote}</p>
        <div className="kpis">
          <Kpi label={tr.activeAsset} value={`${assetName} · ${asset.display}`} />
          <Kpi label={tr.price} value={price ? fmt(price.price, asset.symbol) : "—"} note={price ? tr.live : tr.ref} />
          <Kpi label={tr.decisionSummary} value={tr.contextualUp} note={tr.extended} />
          <Kpi label={tr.decisionQuality} value="84" note={tr.high} />
        </div>
      </Card>
      <Card>
        <Kicker>{tr.quickLinks}</Kicker>
        <div className="linkList">
          <button onClick={() => nav("/NDSP_Asset_View.html")}>{tr.assetView}</button>
          <button onClick={() => nav("/NDSP_Command_Center.html")}>{tr.command}</button>
          <button onClick={() => nav("/NDSP_Daily_Brief.html")}>{tr.brief}</button>
          <button onClick={() => nav("/NDSP_Settings_Alerts.html")}>{tr.settings}</button>
        </div>
      </Card>
    </section>
  );
}

function AssetPage({ tr, lang, symbol, setSymbol, assetName, asset, price, scenario, refresh }) {
  return (
    <section className="grid">
      <Card wide>
        <Kicker>{tr.assetOnly}</Kicker>
        <div className="assetHeader">
          <div>
            <h1>{assetName}</h1>
            <p className="muted">{asset.display} · {price ? tr.live : tr.ref}</p>
          </div>
          <button className="primary" onClick={refresh}>{tr.refresh}</button>
        </div>
        <div className="controls">
          <label>{tr.selectAsset}</label>
          <select value={symbol} onChange={(e) => setSymbol(e.target.value)}>
            {ASSETS.map((a) => <option key={a.symbol} value={a.symbol}>{lang === "ar" ? a.ar : a.en} — {a.display}</option>)}
          </select>
        </div>
        <div className="kpis">
          <Kpi label={tr.price} value={price ? fmt(price.price, symbol) : "—"} />
          <Kpi label={tr.marketState} value={price ? tr.live : tr.ref} />
          <Kpi label={tr.reading} value={tr.contextualUp} note={tr.extended} />
          <Kpi label={tr.decisionQuality} value="84" note={tr.high} />
        </div>
      </Card>
      <Card>
        <Kicker>{tr.scenario}</Kicker>
        <div className="levels">
          <Level label={tr.arrival} value={scenario?.arrival_price ? fmt(scenario.arrival_price, symbol) : "—"} />
          <Level label={tr.review} value={scenario?.review_price ? fmt(scenario.review_price, symbol) : "—"} />
          <Level label={tr.activation} value={scenario?.activation_price ? fmt(scenario.activation_price, symbol) : "—"} />
          <Level label={tr.cancel} value={scenario?.cancel_price ? fmt(scenario.cancel_price, symbol) : "—"} />
        </div>
        <p className="safe">{tr.safe}</p>
      </Card>
    </section>
  );
}

function CommandPage({ tr, price }) {
  return (
    <section className="grid">
      <Card wide>
        <Kicker>{tr.commandOnly}</Kicker>
        <h1>{tr.command}</h1>
        <p className="muted">{tr.noPriceTable}</p>
        <div className="decisionMatrix">
          <Decision label={tr.decisionState} value={tr.contextualUp} tone="green" />
          <Decision label={tr.decisionQuality} value="84" tone="gold" />
          <Decision label={tr.tdl} value={tr.extended} />
          <Decision label={tr.nmp} value={tr.high} />
          <Decision label={tr.devil} value={tr.protected} tone="red" />
          <Decision label={tr.golden} value={price ? tr.live : tr.ref} tone="gold" />
        </div>
      </Card>
      <Card>
        <Kicker>{tr.botConnector}</Kicker>
        <p className="muted">{tr.botPolicy}</p>
        <div className="connectorFlow">
          <span>NDSP Core</span><b>→</b><span>Sanitized API</span><b>→</b><span>External Bot</span>
        </div>
      </Card>
    </section>
  );
}

function BriefPage({ tr, lang, prices }) {
  return (
    <section className="grid">
      <Card wide>
        <Kicker>{tr.dailyOnly}</Kicker>
        <h1>{tr.brief}</h1>
        <div className="journal">
          {ASSETS.slice(0, 4).map((a) => {
            const row = prices[a.symbol];
            return (
              <div className="journalRow" key={a.symbol}>
                <div>
                  <strong>{lang === "ar" ? a.ar : a.en}</strong>
                  <p>{a.display} · {tr.shortReadings}</p>
                </div>
                <span className={row ? "badge live" : "badge ref"}>{row ? tr.live : tr.ref}</span>
              </div>
            );
          })}
        </div>
      </Card>
      <Card>
        <Kicker>{tr.lastReviews}</Kicker>
        <p className="muted">{tr.safe}</p>
        <div className="auditBox">
          <div>{tr.todayLog}</div>
          <strong>{new Date().toLocaleDateString(lang === "ar" ? "ar-SA" : "en-US")}</strong>
        </div>
      </Card>
    </section>
  );
}

function SettingsPage({ tr, lang, setLang }) {
  return (
    <section className="grid">
      <Card wide>
        <Kicker>{tr.settingsOnly}</Kicker>
        <h1>{tr.settings}</h1>
        <p className="muted">{tr.noPricesHere}</p>
        <div className="settingsList">
          <div className="settingRow">
            <div><strong>{tr.language}</strong><p>{tr.settings}</p></div>
            <select value={lang} onChange={(e) => setLang(e.target.value)}>
              <option value="ar">العربية</option>
              <option value="en">English</option>
            </select>
          </div>
          <div className="settingRow"><div><strong>{tr.alerts}</strong><p>Telegram / Email</p></div><span className="badge live">{tr.live}</span></div>
          <div className="settingRow"><div><strong>{tr.dataSources}</strong><p>/api/market/prices · /api/scenario/levels</p></div><span className="badge live">{tr.live}</span></div>
        </div>
      </Card>
      <Card>
        <Kicker>{tr.botConnector}</Kicker>
        <p className="muted">{tr.botPolicy}</p>
      </Card>
    </section>
  );
}

function Card({ children, wide }) { return <div className={wide ? "card wide" : "card"}>{children}</div>; }
function Kicker({ children }) { return <div className="kicker">{children}</div>; }
function Kpi({ label, value, note }) { return <div className="kpi"><span>{label}</span><strong>{value}</strong>{note && <small>{note}</small>}</div>; }
function Level({ label, value }) { return <div className="level"><span>{label}</span><strong>{value}</strong></div>; }
function Decision({ label, value, tone }) { return <div className={`decision ${tone || ""}`}><span>{label}</span><strong>{value}</strong></div>; }

createRoot(document.getElementById("root")).render(<App />);
