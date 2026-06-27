import React from "react";

export default function SettingsPage({ tr, lang, setLang }) {
  return (
    <section className="grid">
      <div className="card wide">
        <h1>{tr.settings}</h1>

        <select value={lang} onChange={(e) => setLang(e.target.value)}>
          <option value="ar">العربية</option>
          <option value="en">English</option>
        </select>
      </div>
    </section>
  );
}
