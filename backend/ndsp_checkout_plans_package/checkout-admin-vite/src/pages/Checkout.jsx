import React, { useEffect, useMemo, useState } from "react";
import { apiGet, apiPost } from "../api.js";

export default function Checkout() {
  const [plans, setPlans] = useState([]);
  const [selectedCode, setSelectedCode] = useState("");
  const [email, setEmail] = useState("");
  const [telegramId, setTelegramId] = useState("");
  const [network, setNetwork] = useState("TRC20");
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");
  const [checkout, setCheckout] = useState(null);

  useEffect(() => {
    let mounted = true;

    async function loadPlans() {
      try {
        setLoading(true);
        setError("");
        const data = await apiGet("/api/v1/plans");

        if (!mounted) return;

        const nextPlans = data.plans || [];
        setPlans(nextPlans);
        setSelectedCode(nextPlans[0]?.code || "");
      } catch (err) {
        if (mounted) setError(err.message || "failed_to_load_plans");
      } finally {
        if (mounted) setLoading(false);
      }
    }

    loadPlans();

    return () => {
      mounted = false;
    };
  }, []);

  const selectedPlan = useMemo(() => {
    return plans.find((plan) => plan.code === selectedCode) || null;
  }, [plans, selectedCode]);

  async function submitCheckout(event) {
    event.preventDefault();

    try {
      setCreating(true);
      setError("");
      setCheckout(null);

      const data = await apiPost("/api/v1/checkout", {
        plan_code: selectedCode,
        email,
        telegram_id: telegramId,
        network
      });

      setCheckout(data.checkout);
    } catch (err) {
      setError(err.message || "failed_to_create_checkout");
    } finally {
      setCreating(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="hero-card">
        <div>
          <p className="eyebrow">NDSP Checkout</p>
          <h1>اختيار الباقة وطلب التفعيل</h1>
          <p className="hero-text">
            اختر الباقة المناسبة. التفعيل لا يتم تلقائيًا، وكل طلب يخضع لمراجعة إدارية قبل فتح الوصول.
          </p>
        </div>
        <div className="hero-badge">Decision Active / Execution Sanitized</div>
      </section>

      {loading && <div className="notice">جاري تحميل الباقات...</div>}
      {error && <div className="notice error">خطأ: {error}</div>}

      {!loading && plans.length > 0 && (
        <section className="checkout-grid">
          <div className="plans-grid">
            {plans.map((plan) => (
              <button
                key={plan.code}
                className={`plan-card ${selectedCode === plan.code ? "selected" : ""}`}
                onClick={() => setSelectedCode(plan.code)}
                type="button"
              >
                <span className="plan-code">{plan.name_en}</span>
                <strong>${Number(plan.price_usd).toFixed(2)}</strong>
                <small>{plan.billing_period}</small>
                <p>{plan.description_ar}</p>
                <ul>
                  {(plan.features || []).slice(0, 5).map((feature) => (
                    <li key={feature}>{feature}</li>
                  ))}
                </ul>
                {plan.trial_days > 0 && (
                  <span className="trial-badge">{plan.trial_days} يوم تجربة</span>
                )}
              </button>
            ))}
          </div>

          <form className="checkout-form" onSubmit={submitCheckout}>
            <h2>بيانات الطلب</h2>

            <label>
              الباقة
              <input value={selectedPlan?.name_en || ""} readOnly />
            </label>

            <label>
              البريد الإلكتروني
              <input
                type="email"
                placeholder="name@example.com"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
              />
            </label>

            <label>
              Telegram ID اختياري
              <input
                placeholder="@username أو ID"
                value={telegramId}
                onChange={(event) => setTelegramId(event.target.value)}
              />
            </label>

            <label>
              شبكة الدفع
              <select value={network} onChange={(event) => setNetwork(event.target.value)}>
                <option value="TRC20">USDT TRC20</option>
                <option value="BEP20">USDT BEP20</option>
              </select>
            </label>

            <div className="summary-box">
              <span>المبلغ</span>
              <strong>
                ${selectedPlan ? Number(selectedPlan.price_usd).toFixed(2) : "0.00"} / USDT
              </strong>
            </div>

            <button className="primary-btn" disabled={creating || !selectedCode}>
              {creating ? "جاري إنشاء الطلب..." : "إنشاء طلب الاشتراك"}
            </button>

            <p className="safe-note">
              لا يتم عرض أي منطق داخلي حساس. الواجهة تعرض نتيجة مؤسسية مبسطة فقط.
            </p>
          </form>
        </section>
      )}

      {checkout && (
        <section className="result-card">
          <h2>تم إنشاء الطلب</h2>
          <p>رقم الطلب: <strong>{checkout.checkout_ref}</strong></p>
          <p>الحالة: <strong>{checkout.status}</strong></p>
          <p>الباقة: <strong>{checkout.plan_code}</strong></p>
          <p>المبلغ: <strong>{checkout.amount_usd} {checkout.payment_currency}</strong></p>
          <p>الشبكة: <strong>{checkout.payment_network}</strong></p>
          <p className="safe-note">
            احتفظ برقم الطلب. سيتم التفعيل بعد المراجعة الإدارية.
          </p>
        </section>
      )}
    </main>
  );
}
