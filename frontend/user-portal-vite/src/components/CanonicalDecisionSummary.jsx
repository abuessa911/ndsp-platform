import React from "react";
import { useCanonicalDecision } from "../hooks/useCanonicalDecision";

function cleanValue(value) {
  if (value === null || value === undefined || value === "") return "—";
  if (typeof value === "boolean") return value ? "نعم" : "لا";
  if (typeof value === "object") return "متاح";
  return String(value);
}

function DecisionCard({ title, decision }) {
  return (
    <section className="card decisionState">
      <div className="sectionTitle">{title}</div>

      <div className="grid">
        <div>
          <div className="muted">الحالة</div>
          <strong>{cleanValue(decision?.decisionState)}</strong>
        </div>
        <div>
          <div className="muted">الاتجاه</div>
          <strong>{cleanValue(decision?.direction)}</strong>
        </div>
        <div>
          <div className="muted">الجاهزية</div>
          <strong>{cleanValue(decision?.readiness)}</strong>
        </div>
        <div>
          <div className="muted">السيناريو</div>
          <strong>{cleanValue(decision?.scenarioState)}</strong>
        </div>
        <div>
          <div className="muted">المخاطر</div>
          <strong>{cleanValue(decision?.riskFinalState)}</strong>
        </div>
        <div>
          <div className="muted">الإطار</div>
          <strong>{cleanValue(decision?.timeframe)}</strong>
        </div>
      </div>
    </section>
  );
}

export function CanonicalDecisionSummary({ symbol = "XAUUSD", timeframe = "weekly" }) {
  const { speculative, investment, loading, error, refresh } = useCanonicalDecision(symbol, timeframe);

  return (
    <div className="stack">
      <div className="sectionHeader">
        <div>
          <div className="eyebrow">Canonical Decision</div>
          <h2>ملخص القرار الحي</h2>
        </div>
        <button type="button" onClick={refresh} disabled={loading}>
          {loading ? "جاري التحديث..." : "تحديث"}
        </button>
      </div>

      {error ? <div className="card danger">تعذر تحميل القرار: {error}</div> : null}

      <DecisionCard title="قرار مضاربي" decision={speculative} />
      <DecisionCard title="قرار استثماري" decision={investment} />
    </div>
  );
}

export default CanonicalDecisionSummary;
