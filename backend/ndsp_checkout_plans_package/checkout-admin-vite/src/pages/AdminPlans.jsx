import React, { useEffect, useState } from "react";
import { apiGet, apiPatch } from "../api.js";

function parseJsonInput(value, fallback) {
  try {
    return JSON.parse(value);
  } catch {
    return fallback;
  }
}

export default function AdminPlans() {
  const [adminKey, setAdminKey] = useState(() => localStorage.getItem("NDSP_ADMIN_KEY") || "");
  const [plans, setPlans] = useState([]);
  const [editing, setEditing] = useState({});
  const [loading, setLoading] = useState(false);
  const [savingCode, setSavingCode] = useState("");
  const [error, setError] = useState("");
  const [okMessage, setOkMessage] = useState("");

  async function loadPlans() {
    try {
      setLoading(true);
      setError("");
      setOkMessage("");

      const data = await apiGet("/api/v1/admin/plans", {
        headers: {
          "x-admin-key": adminKey
        }
      });

      setPlans(data.plans || []);

      const editState = {};
      for (const plan of data.plans || []) {
        editState[plan.code] = {
          name_ar: plan.name_ar || "",
          name_en: plan.name_en || "",
          description_ar: plan.description_ar || "",
          description_en: plan.description_en || "",
          price_usd: plan.price_usd || 0,
          billing_period: plan.billing_period || "monthly",
          trial_days: plan.trial_days || 0,
          sort_order: plan.sort_order || 100,
          is_active: Boolean(plan.is_active),
          is_public: Boolean(plan.is_public),
          features: JSON.stringify(plan.features || [], null, 2),
          limits: JSON.stringify(plan.limits || {}, null, 2),
          metadata: JSON.stringify(plan.metadata || {}, null, 2)
        };
      }

      setEditing(editState);
      localStorage.setItem("NDSP_ADMIN_KEY", adminKey);
    } catch (err) {
      setError(err.message || "failed_to_load_admin_plans");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (adminKey) {
      loadPlans();
    }
  }, []);

  function updateField(code, field, value) {
    setEditing((current) => ({
      ...current,
      [code]: {
        ...(current[code] || {}),
        [field]: value
      }
    }));
  }

  async function savePlan(code) {
    const draft = editing[code];

    if (!draft) return;

    try {
      setSavingCode(code);
      setError("");
      setOkMessage("");

      const payload = {
        name_ar: draft.name_ar,
        name_en: draft.name_en,
        description_ar: draft.description_ar,
        description_en: draft.description_en,
        price_usd: Number(draft.price_usd),
        billing_period: draft.billing_period,
        trial_days: Number(draft.trial_days),
        sort_order: Number(draft.sort_order),
        is_active: Boolean(draft.is_active),
        is_public: Boolean(draft.is_public),
        features: parseJsonInput(draft.features, []),
        limits: parseJsonInput(draft.limits, {}),
        metadata: parseJsonInput(draft.metadata, {})
      };

      await apiPatch(`/api/v1/admin/plans/${code}`, payload, {
        headers: {
          "x-admin-key": adminKey
        }
      });

      setOkMessage(`تم تحديث الباقة: ${code}`);
      await loadPlans();
    } catch (err) {
      setError(err.message || "failed_to_save_plan");
    } finally {
      setSavingCode("");
    }
  }

  return (
    <main className="page-shell">
      <section className="hero-card">
        <div>
          <p className="eyebrow">NDSP Admin</p>
          <h1>إدارة الباقات</h1>
          <p className="hero-text">
            تعديل الأسعار، حالة الظهور، مدة التجربة، والخصائص العامة بدون كشف أي منطق داخلي حساس.
          </p>
        </div>
        <div className="hero-badge">Admin Protected</div>
      </section>

      <section className="admin-key-card">
        <label>
          Admin Key
          <input
            dir="ltr"
            type="password"
            value={adminKey}
            onChange={(event) => setAdminKey(event.target.value)}
            placeholder="x-admin-key"
          />
        </label>
        <button className="primary-btn" onClick={loadPlans} disabled={!adminKey || loading}>
          {loading ? "جاري التحميل..." : "تحميل الباقات"}
        </button>
      </section>

      {error && <div className="notice error">خطأ: {error}</div>}
      {okMessage && <div className="notice success">{okMessage}</div>}

      <section className="admin-plans-list">
        {plans.map((plan) => {
          const draft = editing[plan.code] || {};

          return (
            <article className="admin-plan-card" key={plan.code}>
              <header>
                <div>
                  <span className="plan-code">{plan.code}</span>
                  <h2>{plan.name_en}</h2>
                </div>
                <div className="status-pills">
                  <span>{plan.is_active ? "Active" : "Inactive"}</span>
                  <span>{plan.is_public ? "Public" : "Hidden"}</span>
                </div>
              </header>

              <div className="admin-form-grid">
                <label>
                  الاسم عربي
                  <input
                    value={draft.name_ar || ""}
                    onChange={(event) => updateField(plan.code, "name_ar", event.target.value)}
                  />
                </label>

                <label>
                  الاسم English
                  <input
                    dir="ltr"
                    value={draft.name_en || ""}
                    onChange={(event) => updateField(plan.code, "name_en", event.target.value)}
                  />
                </label>

                <label>
                  السعر USD
                  <input
                    type="number"
                    step="0.01"
                    value={draft.price_usd}
                    onChange={(event) => updateField(plan.code, "price_usd", event.target.value)}
                  />
                </label>

                <label>
                  Billing Period
                  <select
                    value={draft.billing_period || "monthly"}
                    onChange={(event) => updateField(plan.code, "billing_period", event.target.value)}
                  >
                    <option value="monthly">monthly</option>
                    <option value="yearly">yearly</option>
                    <option value="one_time">one_time</option>
                  </select>
                </label>

                <label>
                  Trial Days
                  <input
                    type="number"
                    value={draft.trial_days}
                    onChange={(event) => updateField(plan.code, "trial_days", event.target.value)}
                  />
                </label>

                <label>
                  Sort Order
                  <input
                    type="number"
                    value={draft.sort_order}
                    onChange={(event) => updateField(plan.code, "sort_order", event.target.value)}
                  />
                </label>

                <label className="check-row">
                  <input
                    type="checkbox"
                    checked={Boolean(draft.is_active)}
                    onChange={(event) => updateField(plan.code, "is_active", event.target.checked)}
                  />
                  Active
                </label>

                <label className="check-row">
                  <input
                    type="checkbox"
                    checked={Boolean(draft.is_public)}
                    onChange={(event) => updateField(plan.code, "is_public", event.target.checked)}
                  />
                  Public
                </label>
              </div>

              <label>
                الوصف عربي
                <textarea
                  value={draft.description_ar || ""}
                  onChange={(event) => updateField(plan.code, "description_ar", event.target.value)}
                />
              </label>

              <label>
                Description English
                <textarea
                  dir="ltr"
                  value={draft.description_en || ""}
                  onChange={(event) => updateField(plan.code, "description_en", event.target.value)}
                />
              </label>

              <div className="json-grid">
                <label>
                  features JSON
                  <textarea
                    dir="ltr"
                    value={draft.features || "[]"}
                    onChange={(event) => updateField(plan.code, "features", event.target.value)}
                  />
                </label>

                <label>
                  limits JSON
                  <textarea
                    dir="ltr"
                    value={draft.limits || "{}"}
                    onChange={(event) => updateField(plan.code, "limits", event.target.value)}
                  />
                </label>

                <label>
                  metadata JSON
                  <textarea
                    dir="ltr"
                    value={draft.metadata || "{}"}
                    onChange={(event) => updateField(plan.code, "metadata", event.target.value)}
                  />
                </label>
              </div>

              <button
                className="primary-btn"
                onClick={() => savePlan(plan.code)}
                disabled={savingCode === plan.code}
              >
                {savingCode === plan.code ? "جاري الحفظ..." : "حفظ التعديل"}
              </button>
            </article>
          );
        })}
      </section>
    </main>
  );
}
