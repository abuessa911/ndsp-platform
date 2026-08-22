import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";
import { useMarket } from "./hooks/useMarket";

const ASSETS = [
  { symbol: "XAUUSD", ar: "الذهب", en: "Gold" },
  { symbol: "BTCUSDT", ar: "بيتكوين", en: "Bitcoin" },
  { symbol: "ETHUSDT", ar: "إيثريوم", en: "Ethereum" },
  { symbol: "EURUSD", ar: "اليورو دولار", en: "EUR/USD" },
  { symbol: "USOIL", ar: "النفط الأمريكي", en: "WTI Oil" },
  { symbol: "SPX", ar: "S&P 500", en: "S&P 500" }
];

const ENGINES = [
  { name: "منطق البعد الزمني TDL", visible: true },
  { name: "نقطة التقاء نواف NMP", visible: true },
  { name: "محامي الشيطان", visible: true },
  { name: "جودة القرار", visible: true },

  { name: "طبقة محمية", visible: false },
  { name: "طبقة محمية", visible: false },
  { name: "طبقة محمية", visible: false },
  { name: "طبقة محمية", visible: false },
  { name: "طبقة محمية", visible: false },
  { name: "طبقة محمية", visible: false },
  { name: "طبقة محمية", visible: false },
  { name: "طبقة محمية", visible: false },
  { name: "طبقة محمية", visible: false },
  { name: "طبقة محمية", visible: false },
  { name: "طبقة محمية", visible: false },
  { name: "طبقة محمية", visible: false }
];

function fmt(v) {
  const n = Number(v);
  if (!Number.isFinite(n)) return "—";
  return n.toLocaleString("en-US", { maximumFractionDigits: 2 });
}

function App() {
  const [symbol, setSymbol] = useState("XAUUSD");
  const { price, loading, refresh } = useMarket(symbol);

  const asset = useMemo(
    () => ASSETS.find((a) => a.symbol === symbol) || ASSETS[0],
    [symbol]
  );

  useEffect(() => {
    document.documentElement.lang = "ar";
    document.documentElement.dir = "rtl";
  }, []);

  const livePrice = price?.price;
  const quality = livePrice ? 84 : 41;
  const completed = livePrice ? 7 : 0;

  return (
    <div className="terminal">
      <header className="topbar">
        <div>
          <div className="brand">NDSP</div>
          <div className="subtitle">منصة نواف لدعم القرار</div>
        </div>

        <nav>
          <button>المنصة</button>
          <button>الأصل</button>
          <button>مركز القرار</button>
          <button>القرارات المكتملة</button>
          <button>الإعدادات</button>
        </nav>

        <div className="status">
          <span className="dot"></span>
          قناة البيانات نشطة
        </div>
      </header>

      <main className="layout">
        <section className="hero card">
          <div className="heroText">
            <div className="kicker">Decision Intelligence Terminal</div>
            <h1>مركز القرار المؤسسي</h1>
            <p>
              قراءة تحليلية متعددة الطبقات، تعرض حالة الأصل، جودة القرار،
              ومحركات المنظومة بدون أي أوامر تداول.
            </p>
          </div>

          <div className="radarWrap">
            <div className="radar">
              <div className="sweep"></div>
              <div className="ring r1"></div>
              <div className="ring r2"></div>
              <div className="ring r3"></div>
              <div className="cross h"></div>
              <div className="cross v"></div>
              <div className="target t1"></div>
              <div className="target t2"></div>
              <div className="target t3"></div>
            </div>
          </div>
        </section>

        <section className="card assetCard">
          <div className="kicker">الأصل النشط</div>
          <select value={symbol} onChange={(e) => setSymbol(e.target.value)}>
            {ASSETS.map((a) => (
              <option key={a.symbol} value={a.symbol}>
                {a.ar} — {a.symbol}
              </option>
            ))}
          </select>

          <div className="price">{fmt(livePrice)}</div>
          <div className="muted">{asset.ar} · {asset.symbol}</div>

          <button className="goldBtn" onClick={refresh}>
            {loading ? "جاري التحديث..." : "تحديث القراءة"}
          </button>
        </section>

        <section className="card quality">
          <div className="kicker">جودة القرار</div>
          <div className="gauge">
            <span>{quality}</span>
          </div>
          <p>قراءة حوكمة داخلية وليست توصية تنفيذية.</p>
        </section>

        <section className="card decisionState">
          <div className="kicker">حالة القرار</div>
          <h2>{livePrice ? "تحت المراقبة" : "بانتظار البيانات"}</h2>
          <p>
            لا يتم إعلان القرار المكتمل إلا بعد توافق طبقات المنظومة
            ومرور القراءة عبر بوابة الجودة.
          </p>
        </section>

        <section className="card engines">
          <div className="sectionHead">
            <div>
              <div className="kicker">محركات المنظومة</div>
              <h2>16 طبقة قرار</h2>
            </div>
            <span>{livePrice ? "نشطة" : "جزئية"}</span>
          </div>

          <div className="engineGrid">
            {ENGINES.map((e, i) => (
              <div className="engine" key={i}>
                <b>{e.name}</b>
                <small>{e.visible ? "مسموح عرضها ضمن الباقة" : "مفعّلة ضمن الحوكمة"}</small>
              </div>
            ))}
          </div>
        </section>

        <section className="card completed">
          <div className="sectionHead">
            <div>
              <div className="kicker">القرارات المكتملة</div>
              <h2>{completed} قرارات قابلة للتصدير</h2>
            </div>
            <span>قناة تكامل خارجية</span>
          </div>

          <div className="decisionList">
            <div>
              <strong>{asset.symbol}</strong>
              <span>قراءة مكتملة · جودة {quality}%</span>
            </div>
            <div>
              <strong>مخرجات محكومة</strong>
              <span>مخرجات محكومة بدون كشف الطبقات الداخلية</span>
            </div>
            <div>
              <strong>بوابة التصدير</strong>
              <span>جاهزية تصدير مؤسسية عند اكتمال الشروط</span>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

createRoot(document.getElementById("root")).render(<App />);
