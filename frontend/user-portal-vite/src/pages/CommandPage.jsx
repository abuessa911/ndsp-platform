import React from "react";

export default function CommandPage({ tr }) {
  return (
    <section className="grid">
      <div className="card wide">
        <h1>{tr.command}</h1>
        <p>{tr.noPriceTable}</p>
      </div>
    </section>
  );
}
