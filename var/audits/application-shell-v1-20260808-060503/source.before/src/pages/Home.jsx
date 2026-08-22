import React from "react";

export default function Home({ tr, assetName, asset, price, nav }) {
  return (
    <section className="grid heroGrid">
      <div className="card wide">
        <h1>{tr.brand}</h1>
        <p>{tr.homeNote}</p>

        <div className="kpis">
          <div>{tr.activeAsset}: {assetName}</div>
          <div>{tr.price}: {price?.price || "—"}</div>
        </div>
      </div>

      <div className="card">
        <button onClick={() => nav("/NDSP_Asset_View.html")}>
          {tr.assetView}
        </button>
      </div>
    </section>
  );
}
