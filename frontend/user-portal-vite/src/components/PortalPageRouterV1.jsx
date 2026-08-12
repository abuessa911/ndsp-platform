import React, { useMemo, useState } from "react";

import { useMarket } from "../hooks/useMarket";
import { CompletedDecisionsPanelV37 } from "./CompletedDecisionsPanelV37";
import { CanonicalDecisionSummary } from "./CanonicalDecisionSummary";
import { ApplicationShell } from "./layout/ApplicationShell";

const ASSETS = [
  { symbol: "XAUUSD", ar: "الذهب" },
  { symbol: "BTCUSDT", ar: "بيتكوين" },
  { symbol: "ETHUSDT", ar: "إيثريوم" },
  { symbol: "EURUSD", ar: "اليورو دولار" },
  { symbol: "USOIL", ar: "النفط الأمريكي" },
  { symbol: "SPX", ar: "S&P 500" }
];

const PUBLIC_SYSTEM_NAMES = [
  "TDL",
  "NMP",
  "الإشارة الذهبية",
  "الإشارة الذهبية المعززة",
  "محامي الشيطان"
];

function normalizePathname(pathname) {
  const value = String(pathname || "/portal/").toLowerCase();
  return value.length > 1 ? value.replace(/\/+$/, "") : value;
}

function resolvePortalPage(pathname) {
  const path = normalizePathname(pathname);

  if (path.includes("completed") || path.includes("history")) {
    return "completed";
  }

  if (
    path.includes("market") ||
    path.includes("asset") ||
    path.includes("instrument")
  ) {
    return "markets";
  }

  if (
    path.includes("brief") ||
    path.includes("summary") ||
    path.includes("digest")
  ) {
    return "brief";
  }

  if (
    path.includes("setting") ||
    path.includes("account") ||
    path.includes("profile")
  ) {
    return "settings";
  }

  if (
    path.includes("decision") ||
    path.includes("command") ||
    path.includes("workspace")
  ) {
    return "decision";
  }

  return "home";
}

function formatNumber(value) {
  const number = Number(value);

  if (!Number.isFinite(number)) {
    return "—";
  }

  return number.toLocaleString("en-US", {
    maximumFractionDigits: 2
  });
}

function PageHeader({ kicker, title, description }) {
  return (
    <header className="portalPageHeader">
      <span className="kicker">{kicker}</span>
      <h1>{title}</h1>
      <p>{description}</p>
    </header>
  );
}

function HomePage({ asset, livePrice }) {
  return (
    <section className="portalPage portalPage--home" data-portal-page="home">
      <div className="card portalHero">
        <PageHeader
          kicker="NDSP"
          title="مساحة القرار"
          description="واجهة افتتاحية مختصرة تعرض حالة البيانات والأصل النشط بدون تكرار تفاصيل مركز القرار."
        />
      </div>

      <div className="portalMetricGrid">
        <article className="card portalMetric">
          <small>الأصل النشط</small>
          <strong>{asset.ar}</strong>
          <span>{asset.symbol}</span>
        </article>

        <article className="card portalMetric">
          <small>سعر السوق</small>
          <strong>{formatNumber(livePrice)}</strong>
          <span>{livePrice != null ? "بيانات متاحة" : "بانتظار البيانات"}</span>
        </article>

        <article className="card portalMetric">
          <small>السجل المحكوم</small>
          <strong>16/16</strong>
          <span>اكتمال المنظومة داخليًا</span>
        </article>
      </div>

      <div className="card portalHomeNote">
        <h2>ابدأ من المهمة</h2>
        <p>الأسواق للبيانات، مركز القرار للتحليل، والموجز للقراءة السريعة، بينما السجل يعرض القرارات المكتملة فقط.</p>
      </div>
    </section>
  );
}

function DecisionPage({ asset, livePrice }) {
  return (
    <section className="portalPage portalPage--decision" data-portal-page="decision">
      <div className="card portalDecisionHero">
        <PageHeader
          kicker="Decision Center"
          title="مركز القرار"
          description="مساحة مخصصة لحالة القراءة والأنظمة العامة المصرح بعرضها."
        />

        <div className="portalDecisionState">
          <small>حالة بيانات الأصل</small>
          <strong>{livePrice != null ? "متاحة للتحليل" : "بانتظار البيانات"}</strong>
          <span>{asset.ar} · {asset.symbol}</span>
        </div>
      </div>

      <div className="card portalPublicSystems">
        <div className="sectionHead">
          <div>
            <div className="kicker">Public Projection</div>
            <h2>الأنظمة العامة</h2>
          </div>
          <span>16/16 داخليًا</span>
        </div>

        <div className="portalPublicSystemGrid">
          {PUBLIC_SYSTEM_NAMES.map((name) => (
            <div className="portalPublicSystem" key={name}>
              <strong>{name}</strong>
            </div>
          ))}
        </div>
      </div>

      <CanonicalDecisionSummary symbol={asset.symbol} />

      <div className="card portalGovernanceCard">
        <h2>حدود الاستخدام</h2>
        <p>المخرجات تفسيرية لدعم القرار، وليست أمر تنفيذ أو توصية شراء أو بيع.</p>
      </div>
    </section>
  );
}

function MarketsPage({
  symbol,
  setSymbol,
  asset,
  livePrice,
  allPrices,
  loading,
  refresh
}) {
  return (
    <section className="portalPage portalPage--markets" data-portal-page="markets">
      <div className="card portalMarketControl">
        <PageHeader
          kicker="Markets"
          title="واجهة الأسواق"
          description="السوق هنا مستقل عن سجل القرارات ويعرض بيانات الأصل فقط."
        />

        <label htmlFor="portal-market-symbol">الأصل</label>
        <select
          id="portal-market-symbol"
          value={symbol}
          onChange={(event) => setSymbol(event.target.value)}
        >
          {ASSETS.map((item) => (
            <option key={item.symbol} value={item.symbol}>
              {item.ar} — {item.symbol}
            </option>
          ))}
        </select>

        <div className="portalMarketPrice">
          <strong>{formatNumber(livePrice)}</strong>
          <span>{asset.ar} · {asset.symbol}</span>
        </div>

        <button type="button" className="goldBtn" onClick={refresh}>
          {loading ? "جاري التحديث..." : "تحديث بيانات السوق"}
        </button>
      </div>

      <div className="card portalMarketBoard">
        <h2>الأصول المتاحة</h2>
        <div className="portalMarketRows">
          {ASSETS.map((item) => {
            const row = allPrices.find(
              (price) => String(price?.symbol || "").toUpperCase() === item.symbol
            );

            return (
              <button
                type="button"
                className={item.symbol === symbol ? "portalMarketRow isActive" : "portalMarketRow"}
                key={item.symbol}
                onClick={() => setSymbol(item.symbol)}
              >
                <span>
                  <strong>{item.ar}</strong>
                  <small>{item.symbol}</small>
                </span>
                <b>{formatNumber(row?.price)}</b>
              </button>
            );
          })}
        </div>
      </div>
    </section>
  );
}

function BriefPage({ asset, livePrice }) {
  return (
    <section className="portalPage portalPage--brief" data-portal-page="brief">
      <div className="card portalBriefHero">
        <PageHeader
          kicker="Executive Brief"
          title="الموجز التنفيذي"
          description="قراءة سريعة للحالة الحالية بدون إعادة شاشة مركز القرار."
        />
      </div>

      <div className="portalBriefTimeline">
        <article className="card">
          <small>01 · الأصل</small>
          <h2>{asset.ar}</h2>
          <p>{asset.symbol}</p>
        </article>

        <article className="card">
          <small>02 · السوق</small>
          <h2>{formatNumber(livePrice)}</h2>
          <p>{livePrice != null ? "قناة البيانات متاحة" : "بانتظار بيانات السوق"}</p>
        </article>

        <article className="card">
          <small>03 · الحوكمة</small>
          <h2>16/16</h2>
          <p>يظهر الاكتمال فقط دون كشف تفاصيل داخلية.</p>
        </article>
      </div>
    </section>
  );
}

function CompletedPage({ symbol }) {
  return (
    <section className="portalPage portalPage--completed" data-portal-page="completed">
      <PageHeader
        kicker="Decision Registry"
        title="القرارات المكتملة"
        description="سجل مستقل للقرارات التي اجتازت بوابات النشر والحوكمة."
      />
      <CompletedDecisionsPanelV37 activeSymbol={symbol} />
    </section>
  );
}

function SettingsPage() {
  return (
    <section className="portalPage portalPage--settings" data-portal-page="settings">
      <div className="card portalSettingsHero">
        <PageHeader
          kicker="Preferences"
          title="الإعدادات"
          description="إعدادات الواجهة والحساب منفصلة عن التحليل وبيانات السوق."
        />
      </div>

      <div className="card portalSettingsList">
        <div>
          <small>لغة الواجهة</small>
          <strong>العربية</strong>
        </div>
        <div>
          <small>اتجاه العرض</small>
          <strong>RTL</strong>
        </div>
        <div>
          <small>نمط المخرجات</small>
          <strong>دعم قرار محكوم</strong>
        </div>
      </div>
    </section>
  );
}

export function PortalPageRouterV1() {
  const pathname = window.location.pathname;
  const page = resolvePortalPage(pathname);
  const [symbol, setSymbol] = useState("XAUUSD");
  const { price, allPrices = [], loading, refresh } = useMarket(symbol);

  const asset = useMemo(
    () => ASSETS.find((item) => item.symbol === symbol) || ASSETS[0],
    [symbol]
  );

  const livePrice = price?.price;

  let content;

  switch (page) {
    case "decision":
      content = <DecisionPage asset={asset} livePrice={livePrice} />;
      break;
    case "markets":
      content = (
        <MarketsPage
          symbol={symbol}
          setSymbol={setSymbol}
          asset={asset}
          livePrice={livePrice}
          allPrices={allPrices}
          loading={loading}
          refresh={refresh}
        />
      );
      break;
    case "brief":
      content = <BriefPage asset={asset} livePrice={livePrice} />;
      break;
    case "completed":
      content = <CompletedPage symbol={symbol} />;
      break;
    case "settings":
      content = <SettingsPage />;
      break;
    default:
      content = <HomePage asset={asset} livePrice={livePrice} />;
  }

  return (
    <ApplicationShell pathname={pathname}>
      {content}
    </ApplicationShell>
  );
}
