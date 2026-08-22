import React from "react";

export default function AssetPage({ tr, lang, symbol, setSymbol, assetName, asset, price, scenario, refresh }) {
  return (
    <section className="grid">
      <div className="card wide">
        <h1>{assetName}</h1>

        <button onClick={refresh}>{tr.refresh}</button>

        <div>
          <label>{tr.selectAsset}</label>
          <select value={symbol} onChange={(e) => setSymbol(e.target.value)}>
            <option value="XAUUSD">Gold</option>
            <option value="EURUSD">EUR/USD</option>
          </select>
        </div>

        <div>
          {price?.price || "—"}
        </div>
      </div>

      <div className="card">
        <h3>{tr.scenario}</h3>
        <div className="muted">ملخص السيناريو متاح عبر لوحة القرار الآمنة.</div>
      </div>
    </section>
  );
}
