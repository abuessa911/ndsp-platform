import { ArrowLeft, CheckCircle, ShieldCheck, WarningCircle } from "@phosphor-icons/react";
import { useEffect, useMemo, useState } from "react";
import type { FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useAnalysisContext } from "../analysis/AnalysisContext";
import type { AnalysisMode, AnalysisTimeframe, PresentationMode } from "../analysis/types";
import {
  getAnalysisSetupOptions,
  validateAnalysisContext,
} from "../api/decision";
import type { AnalysisSetupOptions } from "../api/decision";

const VALIDATION_MESSAGES: Record<string, string> = {
  UNSUPPORTED_TIMEFRAME: "الفريم غير مدعوم من عقد التحليل الحالي.",
  UNSUPPORTED_ANALYSIS_MODE: "نمط التحليل غير مدعوم.",
  UNSUPPORTED_PRESENTATION_MODE: "نمط العرض غير مدعوم.",
  QUALITY_SOURCE_UNAVAILABLE: "مصدر التحليل الحي غير متاح لهذا الاختيار.",
  MARKET_SYMBOL_MISMATCH: "الأصل لا ينتمي إلى السوق المحدد حسب مصدر الباك إند.",
};

export function AnalysisSetupPage() {
  const navigate = useNavigate();
  const analysisContext = useAnalysisContext();
  const [options, setOptions] = useState<AnalysisSetupOptions | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [validationErrors, setValidationErrors] = useState<string[]>([]);

  const [market, setMarket] = useState("");
  const [symbol, setSymbol] = useState("");
  const [timeframe, setTimeframe] = useState("");
  const [analysisMode, setAnalysisMode] = useState("");
  const [presentationMode, setPresentationMode] = useState("");

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    void getAnalysisSetupOptions(controller.signal)
      .then((payload) => {
        if (!payload.ok) throw new Error(payload.error ?? "SETUP_OPTIONS_UNAVAILABLE");
        setOptions(payload);
      })
      .catch((requestError) => {
        if (controller.signal.aborted) return;
        setError(requestError instanceof Error ? requestError.message : "تعذر تحميل خيارات التحليل.");
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });

    return () => controller.abort();
  }, []);

  const assets = useMemo(
    () => (options?.assets ?? []).filter((asset) => !market || asset.market === market),
    [market, options?.assets],
  );

  const resetDownstream = (nextMarket: string) => {
    setMarket(nextMarket);
    setSymbol("");
    setValidationErrors([]);
  };

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setValidationErrors([]);

    if (!market || !symbol || !timeframe || !analysisMode || !presentationMode) {
      setValidationErrors(["أكمل جميع عناصر Analysis Context قبل المتابعة."]);
      return;
    }

    setSubmitting(true);
    try {
      const selection = {
        market,
        symbol,
        timeframe: timeframe as AnalysisTimeframe,
        analysisMode: analysisMode as AnalysisMode,
        presentationMode: presentationMode as PresentationMode,
      };
      const validation = await validateAnalysisContext(selection);
      if (!validation.valid_context) {
        setValidationErrors(
          validation.errors.map((code) => VALIDATION_MESSAGES[code] ?? code),
        );
        return;
      }

      analysisContext.setValidatedContext(selection, validation.context.as_of);
      navigate("/analysis", { replace: true });
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "تعذر التحقق من سياق التحليل.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="page-surface analysis-setup-page" dir="rtl">
      <section className="page-hero page-hero--compact">
        <div className="container">
          <span className="eyebrow">GOVERNED ANALYSIS SETUP</span>
          <h1>إعداد سياق التحليل</h1>
          <p>ثبّت السوق والأصل والفريم ونمط التحليل ونمط العرض قبل فتح أي نتيجة.</p>
        </div>
      </section>

      <section className="container governed-setup">
        <div className="governed-setup__notice">
          <ShieldCheck size={22} />
          <div>
            <strong>لا توجد قيم حسابية افتراضية مخفية</strong>
            <span>كل اختيار سيُرسل كما هو إلى عقد الباك إند، وتغيير سياق الحساب يبطل النتائج السابقة.</span>
          </div>
        </div>

        {loading ? <div className="governed-state">جارٍ تحميل الأسواق والأصول من المصادر الحية…</div> : null}
        {error ? <div className="governed-state governed-state--danger"><WarningCircle size={20} /> تعذر تحميل الإعداد: {error}</div> : null}

        {!loading && options ? (
          <form className="governed-setup__form" onSubmit={submit}>
            <label>
              <span>1. السوق / فئة الأصل</span>
              <select value={market} onChange={(event) => resetDownstream(event.target.value)} required>
                <option value="">اختر السوق</option>
                {options.markets.map((item) => (
                  <option key={item.id} value={item.id}>{item.label_ar} — {item.assets_count}</option>
                ))}
              </select>
            </label>

            <label>
              <span>2. الأصل</span>
              <select value={symbol} onChange={(event) => { setSymbol(event.target.value); setValidationErrors([]); }} required disabled={!market}>
                <option value="">اختر الأصل</option>
                {assets.map((item) => (
                  <option key={`${item.market}:${item.symbol}`} value={item.symbol}>{item.label}</option>
                ))}
              </select>
            </label>

            <label>
              <span>3. الفريم الزمني</span>
              <select value={timeframe} onChange={(event) => { setTimeframe(event.target.value); setValidationErrors([]); }} required>
                <option value="">اختر الفريم</option>
                {options.timeframes.map((item) => <option key={item.id} value={item.id}>{item.label_ar}</option>)}
              </select>
            </label>

            <label>
              <span>4. نمط التحليل</span>
              <select value={analysisMode} onChange={(event) => { setAnalysisMode(event.target.value); setValidationErrors([]); }} required>
                <option value="">اختر نمط التحليل</option>
                {options.analysis_modes.map((item) => <option key={item.id} value={item.id}>{item.label_ar}</option>)}
              </select>
            </label>

            <label>
              <span>5. نمط العرض</span>
              <select value={presentationMode} onChange={(event) => { setPresentationMode(event.target.value); setValidationErrors([]); }} required>
                <option value="">اختر نمط العرض</option>
                {options.presentation_modes.map((item) => <option key={item.id} value={item.id}>{item.label_ar}</option>)}
              </select>
            </label>

            {validationErrors.length ? (
              <div className="governed-state governed-state--danger governed-setup__full">
                <WarningCircle size={20} />
                <div>{validationErrors.map((message) => <div key={message}>{message}</div>)}</div>
              </div>
            ) : null}

            <div className="governed-setup__full governed-setup__actions">
              <button className="button button--primary" type="submit" disabled={submitting}>
                {submitting ? "جارٍ التحقق…" : "تثبيت السياق وفتح التغطية"}
                {submitting ? null : <ArrowLeft size={17} />}
              </button>
              <span className="governed-setup__source"><CheckCircle size={16} /> الأصول تأتي من Binance metadata وسجل quality-live الخارجي.</span>
            </div>
          </form>
        ) : null}
      </section>
    </div>
  );
}
