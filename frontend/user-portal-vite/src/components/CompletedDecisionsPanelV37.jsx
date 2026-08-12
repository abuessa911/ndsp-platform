import React from "react";

export function CompletedDecisionsPanelV37({ lang = "ar" }) {
  const ar = lang !== "en";

  return (
    <div className="stack">
      <div className="sectionHeader">
        <div>
          <div className="eyebrow">Public View</div>
          <h2>{ar ? "السجل العام" : "Public history"}</h2>
        </div>
      </div>

      <section className="card decisionState">
        <div className="sectionTitle">
          {ar ? "تفاصيل السجل الداخلي مخفية" : "Internal history details hidden"}
        </div>

        <p className="muted">
          {ar
            ? "تم إخفاء تفاصيل السجل الداخلي من البوابة العامة مؤقتًا. ستظهر هنا نسخة عامة آمنة بعد تجهيز مصدر بيانات عام لا يحتوي على حقول داخلية."
            : "Internal history details are temporarily hidden from the public portal. A safe public version can be enabled after a public data source is available."}
        </p>
      </section>
    </div>
  );
}

export default CompletedDecisionsPanelV37;
