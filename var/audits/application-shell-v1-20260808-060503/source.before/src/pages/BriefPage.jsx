import React from "react";

export default function BriefPage({ tr }) {
  return (
    <section className="grid">
      <div className="card wide">
        <h1>{tr.brief}</h1>
      </div>
    </section>
  );
}
