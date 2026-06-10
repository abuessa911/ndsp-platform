const BLOOMBERG_HEADLINES = [
  "S&P 500 rises 0.4% as Fed officials signal patience on rate cuts",
  "Oil holds near $78 after OPEC+ reaffirms output strategy",
  "Dollar strengthens against yen as US yields climb",
  "Tech stocks lead gains; Nvidia surges on AI demand outlook",
  "US 10-year Treasury yield edges higher to 4.52%",
  "Gold retreats from record highs amid dollar strength",
  "Fed's Powell: 'We are in no hurry' to adjust monetary policy",
  "China PMI data surprises to the upside, lifting Asia markets",
  "European equities slip on weak manufacturing data",
  "Bitcoin holds above $68,000 as institutional inflows continue",
];

const INVESTING_HEADLINES = [
  "EUR/USD struggles below 1.0850 ahead of ECB minutes",
  "Crude oil: WTI at $77.90, Brent at $81.40 — markets eye demand signals",
  "US jobless claims fall more than expected, labor market remains tight",
  "Natural gas futures drop 2.1% on warmer weather forecasts",
  "Dow Jones Industrial Average: +0.31% at 39,214",
  "S&P 500 Technical Outlook: resistance at 5,280 remains key level",
  "MSCI Emerging Markets Index gains 0.6% on China optimism",
  "Japan's Nikkei 225 closes at 38,780 — up 0.9%",
  "UK FTSE 100 slips 0.2% on lower energy and mining stocks",
  "US CPI preview: Analysts forecast 3.4% YoY — markets on alert",
];

interface TickerTrackProps {
  items: string[];
  source: string;
  color: string;
  speed?: number;
}

function TickerTrack({ items, source, color, speed = 60 }: TickerTrackProps) {
  const allItems = [...items, ...items];
  const duration = allItems.length * speed * 0.18;

  return (
    <div className="flex items-center overflow-hidden" style={{ minWidth: 0 }}>
      <div
        className="flex items-center gap-0 whitespace-nowrap"
        style={{
          animation: `ticker-scroll ${duration}s linear infinite`,
          willChange: "transform",
        }}
      >
        {allItems.map((headline, i) => (
          <span key={i} className="flex items-center">
            <span
              className="text-[10px] font-bold tracking-widest px-2 py-0.5 rounded mr-2"
              style={{ color, border: `1px solid ${color}55`, background: `${color}18` }}
            >
              {source}
            </span>
            <span className="text-[11px] text-slate-300 mr-8">{headline}</span>
            <span className="text-slate-600 mr-8">|</span>
          </span>
        ))}
      </div>
    </div>
  );
}

export function NewsTicker() {
  return (
    <>
      <style>{`
        @keyframes ticker-scroll {
          0%   { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
      `}</style>

      <div className="border-b border-slate-800 bg-[#090d14]">
        <div className="flex items-center border-b border-slate-800/60" style={{ height: 28 }}>
          <div
            className="flex-shrink-0 px-3 flex items-center gap-1.5 border-r border-slate-700 h-full"
            style={{ background: "#1a1200" }}
          >
            <div className="w-2 h-2 rounded-full bg-orange-500 animate-pulse" />
            <span className="text-[10px] font-bold text-orange-400 tracking-widest whitespace-nowrap">
              BLOOMBERG
            </span>
          </div>
          <div className="flex-1 overflow-hidden px-3">
            <TickerTrack items={BLOOMBERG_HEADLINES} source="BBG" color="#f97316" speed={55} />
          </div>
        </div>

        <div className="flex items-center" style={{ height: 28 }}>
          <div
            className="flex-shrink-0 px-3 flex items-center gap-1.5 border-r border-slate-700 h-full"
            style={{ background: "#0a1a0a" }}
          >
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
            <span className="text-[10px] font-bold text-green-400 tracking-widest whitespace-nowrap">
              INVESTING
            </span>
          </div>
          <div className="flex-1 overflow-hidden px-3">
            <TickerTrack items={INVESTING_HEADLINES} source="INV" color="#22c55e" speed={65} />
          </div>
        </div>
      </div>
    </>
  );
}
