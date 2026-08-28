import {
  ArrowCounterClockwise,
  CheckCircle,
  LockKey,
  ShieldCheck,
  WarningCircle,
} from "@phosphor-icons/react";
import { useEffect, useMemo, useState } from "react";
import { Link, Navigate } from "react-router-dom";
import { useAnalysisContext } from "../analysis/AnalysisContext";
import type { CapabilityState } from "../analysis/types";
import { getCapabilityCoverage } from "../api/decision";
import type { CapabilityCoverage } from "../api/decision";

const AUTHORITATIVE_CAPABILITY_CONTRACT_COUNT = 311;
// NAW-22 proved 311 CAP contract records exist, but those records mix inferred source,
// documentation-only, and historical references. Until NAW-27 reconciles which records
// are true user-relevant runtime capabilities and maps them to governed public families,
// the UI must not claim global capability completeness.
const GLOBAL_CAPABILITY_MAPPING_RECONCILED = false;

const STATE_LABELS: Record<CapabilityState, string> = {
  CONTRIBUTED: "ساهمت",
  BLOCKED: "محظورة",
  NOT_APPLICABLE: "غير منطبقة",
  UNAVAILABLE: "غير متاحة",
  STALE: "بيانات قديمة",
  PARTIAL: "جزئية",
  GOVERNANCE_PROTECTED: "محمية حوكميًا",
};

export function AnalysisPage() {
  const analysisContext = useAnalysisContext();
  const [coverage, setCoverage] = useState<CapabilityCoverage | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const context = analysisContext.context;
  const requestKey = context
    ? `${context.market}:${context.symbol}:${context.timeframe}:${context.analysisMode}:${context.presentationMode}:${context.generation}`
    : "missing";

  useEffect(() => {
    if (!analysisContext.complete || !context) return;

    const controller = new AbortController();
    setCoverage(null);
    setError(null);
    setLoading(true);

    void getCapabilityCoverage(context, controller.signal)
      .then((payload) => {
        if (!payload.ok) throw new Error("CAPABILITY_COVERAGE_UNAVAILABLE");
        setCoverage(payload);
      })
      .catch((requestError) => {
        if (controller.signal.aborted) return;
        setError(requestError instanceof Error ? requestError.message : "تعذر تحميل تغطية القدرات.");
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });

    return () => controller.abort();
  }, [analysisContext.complete, context, requestKey]);

  const counts = useMemo(() => coverage?.capability_counts ?? {}, [coverage]);

  if (!analysisContext.complete || !context) {
    return <Navigate to="/analysis/setup" replace />;
  }

  const summary = coverage?.decision_summary;
  const professional = context.presentationMode === "professional";
  const effectiveDecisionReady = Boolean(
    coverage?.decision_ready && GLOBAL_CAPABILITY_MAPPING_RECONCILED,
  );

  return (
    <div className="page-surface analysis-page governed-analysis" dir="rtl">
      <section className="page-hero page-hero--compact">
        <div className="container">
          <span className="eyebrow">GOVERNED DECISION EXPERIENCE</span>
          <h1>تغطية القرار المحكومة</h1>
          <p>كل قدرة مؤهلة تظهر بحالتها. لا تعاد حساب الطبقات المحمية داخل المتصفح ولا تُختلق نتيجة عند نقص المحركات.</p>
        </div>
      </section>

      <section className="container governed-analysis__workspace">
        <div className="analysis-context-strip">
          <span><small>السوق</small><strong>{context.market}</strong></span>
          <span><small>الأصل</small><strong dir="ltr">{context.symbol}</strong></span>
          <span><small>الفريم</small><strong>{context.timeframe}</strong></span>
          <span><small>التحليل</small><strong>{context.analysisMode}</strong></span>
          <span><small>العرض</small><strong>{context.presentationMode}</strong></span>
          <Link className="button button--outline" to="/analysis/setup"><ArrowCounterClockwise size={16} /> تغيير السياق</Link>
        </div>

        <div className="governed-state governed-state--danger">
          <ShieldCheck size={20} />
          <div>
            <strong>بوابة التغطية الشاملة ما زالت Fail-Closed</strong>
            <div>
              السجل الحاكم يحتوي {AUTHORITATIVE_CAPABILITY_CONTRACT_COUNT} سجل CAP مكتشفًا، بينما هذه الصفحة تعرض حاليًا عائلات القدرات المربوطة بعقد المستخدم. لا نعتبر ذلك إثباتًا بأن كل سجل تاريخي يمثل قدرة Runtime مستقلة، ولا ندّعي اكتمال القوة حتى تنتهي مصالحة NAW-27.
            </div>
          </div>
        </div>

        {loading ? <div className="governed-state">جارٍ جلب عقد القرار وتغطية القدرات…</div> : null}
        {error ? <div className="governed-state governed-state--danger"><WarningCircle size={20} /> {error}</div> : null}

        {coverage ? (
          <>
            <article className={`governed-decision-state governed-decision-state--${effectiveDecisionReady ? "ready" : "blocked"}`}>
              <div className="governed-decision-state__icon">
                {effectiveDecisionReady ? <CheckCircle size={30} /> : <ShieldCheck size={30} />}
              </div>
              <div>
                <span className="eyebrow">OFFICIAL STATE</span>
                <h2>{effectiveDecisionReady ? "القراءة الرسمية جاهزة" : "لا توجد نتيجة رسمية مكتملة"}</h2>
                <p>
                  {effectiveDecisionReady
                    ? summary?.sanitized_summary ?? "اكتملت بوابات التغطية الحاكمة."
                    : "المنظومة تعمل Fail-Closed: تظهر الأدلة المتاحة والفجوات، لكن لا تُرفع القراءة إلى نتيجة رسمية ما دامت قدرة حرجة ناقصة أو مصفوفة القدرات الشاملة غير مصالحة."}
                </p>
              </div>
            </article>

            <div className="coverage-metrics">
              <article><span>سجلات CAP الحاكمة</span><strong>{AUTHORITATIVE_CAPABILITY_CONTRACT_COUNT}</strong></article>
              <article><span>عائلات التغطية الحالية</span><strong>{coverage.capabilities.length}</strong></article>
              <article><span>ساهمت</span><strong>{counts.CONTRIBUTED ?? 0}</strong></article>
              <article><span>محمية</span><strong>{counts.GOVERNANCE_PROTECTED ?? 0}</strong></article>
              <article><span>جزئية</span><strong>{counts.PARTIAL ?? 0}</strong></article>
              <article><span>غير متاحة</span><strong>{counts.UNAVAILABLE ?? 0}</strong></article>
            </div>

            <section className="governed-summary">
              <div className="section-heading">
                <span className="eyebrow">BACKEND READING</span>
                <h2>القراءة الآمنة الحالية</h2>
                <p>هذه حقول صادرة من الباك إند. إذا كانت النتيجة الرسمية محظورة فتبقى قراءة سياقية فقط.</p>
              </div>
              <div className="governed-summary__grid">
                <article><span>السياق الاتجاهي</span><strong>{summary?.directional_bias ?? "غير متاح"}</strong></article>
                <article><span>جودة القرار</span><strong>{summary?.decision_quality ?? "غير متاحة"}</strong></article>
                <article><span>أفق القراءة</span><strong>{summary?.reading_horizon ?? "غير متاح"}</strong></article>
                <article><span>حالة السوق</span><strong>{summary?.market_state ?? "غير متاحة"}</strong></article>
                <article><span>التفعيل</span><strong>{summary?.activation ?? "غير متاح"}</strong></article>
                <article><span>الوصول</span><strong>{summary?.arrival ?? "غير متاح"}</strong></article>
                <article><span>المراجعة</span><strong>{summary?.review ?? "غير متاح"}</strong></article>
                <article><span>الإلغاء</span><strong>{summary?.invalidation ?? "غير متاح"}</strong></article>
              </div>
              {summary?.caution_reason ? <div className="governed-state"><WarningCircle size={18} /> {summary.caution_reason}</div> : null}
            </section>

            <section className="capability-coverage-section">
              <div className="section-heading">
                <span className="eyebrow">CAPABILITY COVERAGE GATE</span>
                <h2>قوة المنظومة — بدون إخفاء صامت</h2>
                <p>كل عائلة قدرة في عقد التغطية الحالي تظهر حتى عندما تكون غير متاحة أو محمية. نمط المحترف يضيف شرحًا آمنًا فقط ولا يغيّر الحساب.</p>
              </div>
              <div className="capability-coverage-grid">
                {coverage.capabilities.map((item) => (
                  <article key={item.id} className="capability-card">
                    <div className="capability-card__head">
                      <strong>{item.public_label}</strong>
                      {item.protected ? <LockKey size={16} aria-label="قدرة محمية" /> : null}
                    </div>
                    <span className={`capability-state capability-state--${item.state.toLowerCase()}`}>
                      {STATE_LABELS[item.state] ?? item.state}
                    </span>
                    <small>الأثر: {item.effect}</small>
                    {professional ? <p>{item.safe_detail}</p> : null}
                  </article>
                ))}
              </div>
            </section>

            <section className="layer-coverage-section">
              <div className="section-heading">
                <span className="eyebrow">16-LAYER GOVERNANCE LEDGER</span>
                <h2>سجل الطبقات الـ16</h2>
                <p>هذا السجل يثبت وجود كل طبقة في التغطية دون كشف الصيغ أو الأوزان أو العتبات المحمية.</p>
              </div>
              <div className="layer-ledger">
                {coverage.layer_coverage.map((layer) => (
                  <article key={layer.layer}>
                    <span>طبقة {layer.layer}</span>
                    <strong>{layer.public_label}</strong>
                    <em>{STATE_LABELS[layer.state] ?? layer.state}</em>
                    {layer.protected ? <LockKey size={15} /> : null}
                  </article>
                ))}
              </div>
            </section>

            <div className="governance-proof">
              <ShieldCheck size={20} />
              <span>Frontend recomputation: {coverage.governance.frontend_recomputes_protected_logic ? "مرفوض" : "لا"}</span>
              <span>Protected formulas exposed: {coverage.governance.protected_formulas_exposed ? "نعم" : "لا"}</span>
              <span>Current-family omission check: {coverage.governance.no_silent_omission ? "PASS" : "FAIL"}</span>
              <span>Global registry reconciliation: {GLOBAL_CAPABILITY_MAPPING_RECONCILED ? "PASS" : "PENDING"}</span>
              <span>Fail closed: {coverage.governance.fail_closed ? "PASS" : "FAIL"}</span>
            </div>
          </>
        ) : null}
      </section>
    </div>
  );
}
