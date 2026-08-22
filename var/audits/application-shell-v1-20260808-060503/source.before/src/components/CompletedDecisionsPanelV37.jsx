import React, { useMemo, useState } from "react";
import { useCompletedDecisionsV37 } from "../hooks/useCompletedDecisionsV37";

const NDSP_COMPLETED_DECISIONS_UI_V37 = true;

const LAYER_LABELS = {
  "NDSP-CORE-L01": { ar: "TDL المتوسط والطويل", en: "TDL Medium & Long" },
  "NDSP-CORE-L02": { ar: "TDL القصير والمضاربي", en: "TDL Short & Speculative" },
  "NDSP-CORE-L03": { ar: "اتجاه السوق الحاكم", en: "Governing Market Direction" },
  "NDSP-CORE-L04": { ar: "بوابة التصحيح", en: "Correction Gate" },
  "NDSP-CORE-L05": { ar: "محرك الانحراف", en: "Divergence Engine" },
  "NDSP-CORE-L06": { ar: "المنطق الزمني واليومي", en: "Temporal & Day Logic" },
  "NDSP-CORE-L07": { ar: "مستويات السيناريو", en: "Scenario Levels" },
  "NDSP-CORE-L08": { ar: "نقطة التقاء نواف", en: "Nawaf Meet Point" },
  "NDSP-CORE-L09": { ar: "محرك الزخم", en: "Momentum Engine" },
  "NDSP-CORE-L10": { ar: "السيولة والبنية", en: "Liquidity & Structure" },
  "NDSP-CORE-L11": { ar: "الدولار والماكرو", en: "USD & Macro" },
  "NDSP-CORE-L12": { ar: "محرك المخاطر", en: "Risk Engine" },
  "NDSP-CORE-L13": { ar: "إشارة نواف الذهبية", en: "Nawaf Golden Signal" },
  "NDSP-CORE-L14": { ar: "إشارة نواف الذهبية المعززة", en: "Enhanced Nawaf Golden Signal" },
  "NDSP-CORE-L15": { ar: "محامي الشيطان", en: "Devil's Advocate" },
  "NDSP-CORE-L16": { ar: "حالة الجاهزية والقرار", en: "Readiness & Decision State" }
};

const TEXT = {
  ar: {
    kicker: "السجل القانوني للقرارات",
    title: "القرارات المكتملة وسجل التغيّرات",
    subtitle: "يعرض فقط القرارات التي اجتازت الطبقات الست عشرة وبوابات الجاهزية والنشر.",
    currentTab: "القرارات الحالية",
    historyTab: "السجل التاريخي",
    refresh: "تحديث السجل",
    refreshing: "جاري التحديث...",
    allAssets: "كل الأصول",
    allModes: "كل أنماط القراءة",
    allTimeframes: "كل الأطر الزمنية",
    currentCount: "القرارات الحالية",
    historyCount: "السجلات التاريخية",
    chainIntegrity: "سلامة السجل",
    connected: "متصل",
    verified: "متحقق",
    unavailable: "غير متاح",
    lastUpdate: "آخر تحميل",
    noCurrent: "لا يوجد قرار مكتمل يطابق المرشحات الحالية.",
    noHistory: "لا يوجد سجل تاريخي يطابق المرشحات الحالية.",
    complete: "قراءة مكتملة",
    direction: "الاتجاه الحاكم",
    scenario: "حالة السيناريو",
    levels: "مستويات السيناريو",
    activation: "التفعيل",
    arrival: "الوصول",
    review: "المراجعة",
    invalidation: "الإلغاء",
    nmp: "نقطة التقاء نواف",
    risk: "المخاطر",
    devils: "محامي الشيطان",
    readiness: "الجاهزية",
    allowed: "مسموح قانونيًا",
    notAllowed: "غير مسموح",
    passed: "اجتاز",
    objected: "اعترض",
    notBlocked: "لا يوجد حجب",
    riskScore: "درجة المخاطر",
    layers: "الطبقات المنفذة",
    averageEvidence: "متوسط ثقة الأدلة",
    beginnerExplanation: "التفسير المبسط",
    professionalExplanation: "التفسير الاحترافي",
    layerDetails: "تفاصيل الطبقات",
    state: "الحالة",
    confidence: "الثقة",
    blocking: "حاجبة",
    notBlocking: "غير حاجبة",
    sourceRuntime: "مصدر التشغيل",
    contract: "العقد",
    decisionId: "معرّف القرار",
    eventId: "معرّف الحدث التاريخي",
    recordHash: "بصمة السجل",
    semanticHash: "بصمة القرار",
    capturedAt: "وقت الحفظ",
    generatedAt: "وقت التوليد",
    historyNote: "يحفظ السجل نسخة جديدة فقط عند تغيّر جوهري في القرار.",
    investmentStatus: "حالة القراءة الاستثمارية",
    investmentBlockedText: "القراءة الاستثمارية ليست قرارًا مكتملًا حاليًا، لذلك لا تظهر داخل سجل القرارات المكتملة.",
    investmentReadyText: "القراءة الاستثمارية اجتازت بوابات الجاهزية، وستظهر في السجل عند نشرها كقرار مكتمل.",
    blockers: "الموانع",
    noBlockers: "لا توجد موانع مسجلة",
    governance: "هذه مخرجات تفسيرية لدعم القرار فقط، وليست توصية شراء أو بيع ولا أمر تنفيذ.",
    noFabricatedScore: "لا يتم اختلاق درجة جودة رقمية مستقلة؛ المعروض هو متوسط ثقة الأدلة الفعلية.",
    record: "سجل",
    current: "حالي",
    historical: "تاريخي",
    activeAsset: "الأصل المفتوح في غرفة القرار",
    viewDetails: "عرض التفاصيل",
    hideDetails: "إخفاء التفاصيل",
    dataError: "تعذر تحميل جزء من السجل. بقيت البيانات التي وصلت بنجاح ظاهرة.",
    all16: "تم تنفيذ جميع الطبقات القانونية الست عشرة.",
    readinessPassed: "اجتازت القراءة بوابة الجاهزية وأصبحت قابلة للنشر.",
    levelsExplain: "تُستخدم المستويات للمتابعة المنظمة، وليست أوامر دخول أو خروج.",
    riskClear: "طبقة المخاطر لم تسجل حجبًا نهائيًا.",
    riskBlocked: "طبقة المخاطر سجلت حجبًا يمنع اكتمال القراءة.",
    devilClear: "محامي الشيطان لم يسجل اعتراضًا حاجبًا.",
    devilBlocked: "محامي الشيطان سجل اعتراضًا حاجبًا.",
    nmpAvailable: "نقطة التقاء نواف متاحة داخل القراءة.",
    nmpUnavailable: "نقطة التقاء نواف غير متاحة داخل هذه القراءة.",
    integrityFail: "فشل التحقق من سلسلة السجل",
    sourceCurrent: "المصدر الحالي V35",
    sourceHistory: "السجل التاريخي V36"
  },
  en: {
    kicker: "Governed Decision Registry",
    title: "Completed Decisions & Change History",
    subtitle: "Only decisions that passed all sixteen layers, readiness gates, and publishing controls are shown.",
    currentTab: "Current Decisions",
    historyTab: "Decision History",
    refresh: "Refresh Registry",
    refreshing: "Refreshing...",
    allAssets: "All Assets",
    allModes: "All Reading Modes",
    allTimeframes: "All Timeframes",
    currentCount: "Current Decisions",
    historyCount: "History Records",
    chainIntegrity: "Ledger Integrity",
    connected: "Connected",
    verified: "Verified",
    unavailable: "Unavailable",
    lastUpdate: "Last Load",
    noCurrent: "No completed decision matches the current filters.",
    noHistory: "No historical record matches the current filters.",
    complete: "Completed Reading",
    direction: "Governing Direction",
    scenario: "Scenario State",
    levels: "Scenario Levels",
    activation: "Activation",
    arrival: "Arrival",
    review: "Review",
    invalidation: "Invalidation",
    nmp: "Nawaf Meet Point",
    risk: "Risk",
    devils: "Devil's Advocate",
    readiness: "Readiness",
    allowed: "Governed Use Allowed",
    notAllowed: "Not Allowed",
    passed: "Passed",
    objected: "Objected",
    notBlocked: "No Final Block",
    riskScore: "Risk Score",
    layers: "Executed Layers",
    averageEvidence: "Evidence Confidence Average",
    beginnerExplanation: "Beginner Explanation",
    professionalExplanation: "Professional Explanation",
    layerDetails: "Layer Details",
    state: "State",
    confidence: "Confidence",
    blocking: "Blocking",
    notBlocking: "Non-blocking",
    sourceRuntime: "Source Runtime",
    contract: "Contract",
    decisionId: "Decision ID",
    eventId: "History Event ID",
    recordHash: "Record Hash",
    semanticHash: "Decision Fingerprint",
    capturedAt: "Captured At",
    generatedAt: "Generated At",
    historyNote: "A new record is appended only when the decision changes meaningfully.",
    investmentStatus: "Investment Reading Status",
    investmentBlockedText: "The investment reading is not a completed decision, so it is not shown in the completed-decision registry.",
    investmentReadyText: "The investment reading passed readiness gates and will appear after it is published as a completed decision.",
    blockers: "Blockers",
    noBlockers: "No blockers recorded",
    governance: "These are explanatory decision-support outputs only, not a buy/sell recommendation or an execution instruction.",
    noFabricatedScore: "No independent numeric quality score is fabricated; the displayed number is the average confidence of actual evidence.",
    record: "Record",
    current: "Current",
    historical: "Historical",
    activeAsset: "Asset currently open in the decision room",
    viewDetails: "View Details",
    hideDetails: "Hide Details",
    dataError: "Part of the registry could not be loaded. Successfully loaded data remains visible.",
    all16: "All sixteen governed layers were executed.",
    readinessPassed: "The reading passed readiness and became publishable.",
    levelsExplain: "Levels support governed follow-up and are not entry or exit instructions.",
    riskClear: "The risk layer did not register a final block.",
    riskBlocked: "The risk layer registered a block that prevents completion.",
    devilClear: "Devil's Advocate did not register a blocking objection.",
    devilBlocked: "Devil's Advocate registered a blocking objection.",
    nmpAvailable: "Nawaf Meet Point is available in this reading.",
    nmpUnavailable: "Nawaf Meet Point is unavailable in this reading.",
    integrityFail: "Ledger chain verification failed",
    sourceCurrent: "Current source V35",
    sourceHistory: "Historical ledger V36"
  }
};

function text(lang) {
  return TEXT[lang] || TEXT.ar;
}

function stateLabel(value, lang) {
  const code = String(value || "").toUpperCase();
  const labels = {
    READY: { ar: "جاهزة", en: "Ready" },
    COMPLETED: { ar: "مكتملة", en: "Completed" },
    DATA_BLOCKED: { ar: "محجوبة بسبب البيانات", en: "Data Blocked" },
    MONITORING_ONLY: { ar: "متابعة فقط", en: "Monitoring Only" },
    UNDER_MONITORING: { ar: "تحت المتابعة", en: "Under Monitoring" },
    UNDER_REVIEW: { ar: "تحت المراجعة", en: "Under Review" },
    ACTIVE: { ar: "نشطة", en: "Active" },
    AVAILABLE: { ar: "متاحة", en: "Available" },
    FULL_AVAILABLE: { ar: "متاحة بالكامل", en: "Fully Available" },
    PASSED: { ar: "اجتازت", en: "Passed" },
    ALLOWED: { ar: "مسموحة", en: "Allowed" },
    ELIGIBLE: { ar: "مؤهلة", en: "Eligible" },
    INACTIVE: { ar: "غير نشطة", en: "Inactive" },
    NOT_APPLICABLE: { ar: "غير منطبقة", en: "Not Applicable" },
    PARTIAL_AVAILABLE: { ar: "متاحة جزئيًا", en: "Partially Available" },
    BLOCKED: { ar: "محجوبة", en: "Blocked" }
  };
  return labels[code]?.[lang] || code || "—";
}

function directionLabel(value, lang) {
  const code = String(value || "").toLowerCase();
  const labels = {
    bullish: { ar: "صاعد", en: "Bullish" },
    bearish: { ar: "هابط", en: "Bearish" },
    neutral: { ar: "محايد", en: "Neutral" },
    unknown: { ar: "غير محسوم", en: "Undetermined" }
  };
  return labels[code]?.[lang] || value || "—";
}

function modeLabel(value, lang) {
  if (value === "speculative") return lang === "ar" ? "مضاربي" : "Speculative";
  if (value === "investment") return lang === "ar" ? "استثماري" : "Investment";
  return value || "—";
}

function timeframeLabel(value, lang) {
  const map = {
    weekly: { ar: "أسبوعي", en: "Weekly" },
    daily: { ar: "يومي", en: "Daily" },
    monthly: { ar: "شهري", en: "Monthly" }
  };
  return map[value]?.[lang] || value || "—";
}

function formatNumber(value, lang) {
  const number = Number(value);
  if (!Number.isFinite(number)) return "—";
  return number.toLocaleString(lang === "ar" ? "ar-SA" : "en-US", {
    maximumFractionDigits: 4
  });
}

function formatDate(value, lang) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleString(lang === "ar" ? "ar-SA" : "en-US", {
    dateStyle: "medium",
    timeStyle: "short"
  });
}

function confidenceValue(value) {
  const number = Number(value);
  return Number.isFinite(number) ? `${Math.round(number)}%` : "—";
}

function decisionFromEntry(entry, tab) {
  return tab === "history" ? (entry?.decision || {}) : (entry || {});
}

function entryKey(entry, tab, index) {
  if (tab === "history") {
    return entry?.event_id || entry?.record_hash || `history-${index}`;
  }
  return entry?.decision_id || `current-${index}`;
}

function beginnerNarrative(decision, lang) {
  const tr = text(lang);
  const parts = [];

  if (decision?.actual_layers_executed === 16) parts.push(tr.all16);
  if (decision?.readiness?.allowed || decision?.publishable) parts.push(tr.readinessPassed);

  parts.push(
    lang === "ar"
      ? `الاتجاه الحاكم ${directionLabel(decision?.trend_context, lang)}، وحالة السيناريو ${stateLabel(decision?.scenario_state, lang)}.`
      : `The governing direction is ${directionLabel(decision?.trend_context, lang)}, and the scenario is ${stateLabel(decision?.scenario_state, lang)}.`
  );

  parts.push(decision?.nmp?.value != null ? tr.nmpAvailable : tr.nmpUnavailable);
  parts.push(decision?.risk?.blocked ? tr.riskBlocked : tr.riskClear);
  parts.push(decision?.devils_advocate?.blocked ? tr.devilBlocked : tr.devilClear);
  parts.push(tr.levelsExplain);

  return parts.join(" ");
}

function professionalNarrative(decision, entry, tab, lang) {
  const tr = text(lang);
  const riskReasons = decision?.risk?.reasons || [];
  const devilReasons = decision?.devils_advocate?.reasons || [];
  const chunks = [
    `${tr.state}: ${stateLabel(decision?.decision_state, lang)}`,
    `${tr.layers}: ${decision?.actual_layers_executed ?? "—"}/16`,
    `${tr.averageEvidence}: ${confidenceValue(decision?.evidence_confidence_average)}`,
    `${tr.readiness}: ${decision?.readiness?.allowed ? tr.allowed : tr.notAllowed}`,
    `${tr.risk}: ${stateLabel(decision?.risk?.status, lang)} / ${tr.riskScore}: ${formatNumber(decision?.risk?.risk_score, lang)}`,
    `${tr.devils}: ${stateLabel(decision?.devils_advocate?.status, lang)}`,
    `${tr.nmp}: ${stateLabel(decision?.nmp?.status, lang)} / ${formatNumber(decision?.nmp?.value, lang)}`
  ];

  if (riskReasons.length) chunks.push(`${tr.risk}: ${riskReasons.join(" · ")}`);
  if (devilReasons.length) chunks.push(`${tr.devils}: ${devilReasons.join(" · ")}`);
  if (tab === "history" && entry?.record_index) chunks.push(`${tr.record}: #${entry.record_index}`);

  return chunks.join(" | ");
}

function statusClass(decision) {
  if (decision?.publishable && decision?.readiness?.allowed) return "isReady";
  if (String(decision?.decision_state || "").includes("BLOCK")) return "isBlocked";
  return "isMonitoring";
}

function uniqueSorted(values) {
  return [...new Set(values.filter(Boolean))].sort();
}

function DecisionCardV37({ entry, tab, lang, readingMode, index }) {
  const tr = text(lang);
  const decision = decisionFromEntry(entry, tab);
  const [expanded, setExpanded] = useState(readingMode === "professional");
  const layers = Array.isArray(decision?.layer_states) ? decision.layer_states : [];
  const levels = decision?.levels || {};

  return (
    <article
      className={`v37DecisionCard ${statusClass(decision)}`}
      data-v37-decision-card
      data-symbol={decision?.symbol || ""}
      data-mode={decision?.analysis_mode || ""}
    >
      <div className="v37DecisionHeader">
        <div>
          <div className="v37DecisionIdentity">
            <strong>{decision?.symbol || "—"}</strong>
            <span>{modeLabel(decision?.analysis_mode, lang)}</span>
            <span>{timeframeLabel(decision?.timeframe, lang)}</span>
            <span>{tab === "history" ? tr.historical : tr.current}</span>
          </div>
          <small>
            {tab === "history"
              ? `${tr.capturedAt}: ${formatDate(entry?.captured_at, lang)}`
              : `${tr.generatedAt}: ${formatDate(decision?.generated_at, lang)}`}
          </small>
        </div>
        <span className="v37StatusSeal">
          {decision?.publishable ? tr.complete : stateLabel(decision?.decision_state, lang)}
        </span>
      </div>

      <div className="v37Explanation">
        <div className="v37ExplanationTitle">
          {readingMode === "professional" ? tr.professionalExplanation : tr.beginnerExplanation}
        </div>
        <p>
          {readingMode === "professional"
            ? professionalNarrative(decision, entry, tab, lang)
            : beginnerNarrative(decision, lang)}
        </p>
      </div>

      <div className="v37LevelGrid" aria-label={tr.levels}>
        <div><small>{tr.activation}</small><strong>{formatNumber(levels.activation, lang)}</strong></div>
        <div><small>{tr.arrival}</small><strong>{formatNumber(levels.arrival, lang)}</strong></div>
        <div><small>{tr.review}</small><strong>{formatNumber(levels.review, lang)}</strong></div>
        <div><small>{tr.invalidation}</small><strong>{formatNumber(levels.invalidation, lang)}</strong></div>
      </div>

      <div className="v37ReasonGrid">
        <div>
          <small>{tr.readiness}</small>
          <strong>{decision?.readiness?.allowed ? tr.allowed : tr.notAllowed}</strong>
          <span>{stateLabel(decision?.readiness?.single_truth_state || decision?.readiness?.status, lang)}</span>
        </div>
        <div>
          <small>{tr.nmp}</small>
          <strong>{formatNumber(decision?.nmp?.value, lang)}</strong>
          <span>{stateLabel(decision?.nmp?.status, lang)}</span>
        </div>
        <div>
          <small>{tr.risk}</small>
          <strong>{tr.riskScore}: {formatNumber(decision?.risk?.risk_score, lang)}</strong>
          <span>{decision?.risk?.blocked ? tr.blocked : tr.notBlocked}</span>
        </div>
        <div>
          <small>{tr.devils}</small>
          <strong>{stateLabel(decision?.devils_advocate?.status, lang)}</strong>
          <span>{decision?.devils_advocate?.blocked ? tr.objected : tr.passed}</span>
        </div>
      </div>

      <button
        type="button"
        className="v37DetailsButton"
        onClick={() => setExpanded((value) => !value)}
        aria-expanded={expanded}
      >
        {expanded ? tr.hideDetails : tr.viewDetails}
      </button>

      {expanded ? (
        <div className="v37Expanded">
          <div className="v37EvidenceGrid">
            <div><small>{tr.decisionId}</small><code>{decision?.decision_id || "—"}</code></div>
            {tab === "history" ? <div><small>{tr.eventId}</small><code>{entry?.event_id || "—"}</code></div> : null}
            <div><small>{tr.sourceRuntime}</small><code>{decision?.source_runtime || "—"}</code></div>
            <div><small>{tr.contract}</small><code>{decision?.contract_version || "—"}</code></div>
            <div><small>{tr.semanticHash}</small><code>{decision?.semantic_fingerprint || "—"}</code></div>
            {tab === "history" ? <div><small>{tr.recordHash}</small><code>{entry?.record_hash || "—"}</code></div> : null}
          </div>

          <div className="v37LayerHead">
            <h3>{tr.layerDetails}</h3>
            <span>{layers.length}/16</span>
          </div>

          <div className="v37LayerTableWrap">
            <table className="v37LayerTable">
              <thead>
                <tr>
                  <th>#</th>
                  <th>{tr.layerDetails}</th>
                  <th>{tr.state}</th>
                  <th>{tr.confidence}</th>
                  <th>{tr.blocking}</th>
                </tr>
              </thead>
              <tbody>
                {layers.map((layer, layerIndex) => (
                  <tr key={layer?.id || layerIndex}>
                    <td>{layerIndex + 1}</td>
                    <td>{LAYER_LABELS[layer?.id]?.[lang] || layer?.name || layer?.id || "—"}</td>
                    <td>{stateLabel(layer?.state, lang)}</td>
                    <td>{confidenceValue(layer?.confidence)}</td>
                    <td>{layer?.blocking ? tr.blocking : tr.notBlocking}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : null}
    </article>
  );
}

export function CompletedDecisionsPanelV37({
  lang = "ar",
  readingMode = "beginner",
  activeSymbol = "",
  canonicalSpeculative = null,
  canonicalInvestment = null
}) {
  const tr = text(lang);
  const registry = useCompletedDecisionsV37();
  const [tab, setTab] = useState("current");
  const [symbolFilter, setSymbolFilter] = useState("all");
  const [modeFilter, setModeFilter] = useState("all");
  const [timeframeFilter, setTimeframeFilter] = useState("all");

  const currentEntries = Array.isArray(registry.current?.decisions) ? registry.current.decisions : [];
  const historyEntries = Array.isArray(registry.history?.records) ? registry.history.records : [];

  const allDecisions = useMemo(
    () => [...currentEntries, ...historyEntries.map((entry) => entry?.decision || {})],
    [currentEntries, historyEntries]
  );

  const symbols = useMemo(() => uniqueSorted(allDecisions.map((decision) => decision?.symbol)), [allDecisions]);
  const modes = useMemo(() => uniqueSorted(allDecisions.map((decision) => decision?.analysis_mode)), [allDecisions]);
  const timeframes = useMemo(() => uniqueSorted(allDecisions.map((decision) => decision?.timeframe)), [allDecisions]);

  const entries = tab === "history" ? historyEntries : currentEntries;

  const filteredEntries = useMemo(
    () => entries.filter((entry) => {
      const decision = decisionFromEntry(entry, tab);
      if (symbolFilter !== "all" && decision?.symbol !== symbolFilter) return false;
      if (modeFilter !== "all" && decision?.analysis_mode !== modeFilter) return false;
      if (timeframeFilter !== "all" && decision?.timeframe !== timeframeFilter) return false;
      return true;
    }),
    [entries, tab, symbolFilter, modeFilter, timeframeFilter]
  );

  const investmentExecution = canonicalInvestment?.execution || {};
  const investmentBlockers = Array.isArray(investmentExecution?.blockers) ? investmentExecution.blockers : [];
  const integrityVerified = registry.integrity?.ok === true && registry.integrity?.chain_verified === true;

  return (
    <section
      id="completed-decisions"
      className="card completed v37Completed"
      data-ndsp-v37="completed-decisions"
      data-runtime-marker="NDSP_COMPLETED_DECISIONS_UI_V37"
    >
      <div className="sectionHead v37SectionHead">
        <div>
          <div className="kicker">{tr.kicker}</div>
          <h2>{tr.title}</h2>
          <p>{tr.subtitle}</p>
        </div>
        <button
          type="button"
          className="controlBtn v37Refresh"
          onClick={registry.refresh}
          disabled={registry.loading}
        >
          {registry.loading ? tr.refreshing : tr.refresh}
        </button>
      </div>

      <div className="v37ConnectionBar">
        <span className={registry.current?.ok ? "isOk" : "isOff"}>
          {tr.sourceCurrent}: {registry.current?.ok ? tr.connected : tr.unavailable}
        </span>
        <span className={registry.history?.ok ? "isOk" : "isOff"}>
          {tr.sourceHistory}: {registry.history?.ok ? tr.connected : tr.unavailable}
        </span>
        <span className={integrityVerified ? "isOk" : "isOff"}>
          {tr.chainIntegrity}: {integrityVerified ? tr.verified : tr.unavailable}
        </span>
        <span>{tr.activeAsset}: {activeSymbol || "—"}</span>
      </div>

      {registry.error ? (
        <div className="v37Error" role="status">
          <strong>{tr.dataError}</strong>
          <code>{registry.error}</code>
        </div>
      ) : null}

      {!integrityVerified && registry.integrity ? (
        <div className="v37IntegrityWarning" role="alert">
          {tr.integrityFail}
        </div>
      ) : null}

      <div className="v37Stats">
        <div><small>{tr.currentCount}</small><strong data-ndsp-v37-current-count>{currentEntries.length}</strong></div>
        <div><small>{tr.historyCount}</small><strong data-ndsp-v37-history-count>{registry.integrity?.record_count ?? historyEntries.length}</strong></div>
        <div><small>{tr.chainIntegrity}</small><strong>{integrityVerified ? tr.verified : tr.unavailable}</strong></div>
        <div><small>{tr.lastUpdate}</small><strong>{formatDate(registry.lastLoadedAt, lang)}</strong></div>
      </div>

      <div className="v37InvestmentStatus">
        <div>
          <small>{tr.investmentStatus}</small>
          <strong>{stateLabel(investmentExecution?.governed_single_truth_state, lang)}</strong>
        </div>
        <p>{investmentExecution?.publishable_completed_decision ? tr.investmentReadyText : tr.investmentBlockedText}</p>
        <div className="v37Blockers">
          <span>{tr.blockers}:</span>
          <strong>{investmentBlockers.length ? investmentBlockers.join(" · ") : tr.noBlockers}</strong>
        </div>
      </div>

      <div className="v37Toolbar">
        <div className="v37Tabs" role="tablist">
          <button type="button" data-v37-tab="current" className={tab === "current" ? "isActive" : ""} onClick={() => setTab("current")}>
            {tr.currentTab}
          </button>
          <button type="button" data-v37-tab="history" className={tab === "history" ? "isActive" : ""} onClick={() => setTab("history")}>
            {tr.historyTab}
          </button>
        </div>

        <div className="v37Filters">
          <select value={symbolFilter} onChange={(event) => setSymbolFilter(event.target.value)} aria-label={tr.allAssets}>
            <option value="all">{tr.allAssets}</option>
            {symbols.map((symbol) => <option key={symbol} value={symbol}>{symbol}</option>)}
          </select>
          <select value={modeFilter} onChange={(event) => setModeFilter(event.target.value)} aria-label={tr.allModes}>
            <option value="all">{tr.allModes}</option>
            {modes.map((mode) => <option key={mode} value={mode}>{modeLabel(mode, lang)}</option>)}
          </select>
          <select value={timeframeFilter} onChange={(event) => setTimeframeFilter(event.target.value)} aria-label={tr.allTimeframes}>
            <option value="all">{tr.allTimeframes}</option>
            {timeframes.map((timeframe) => <option key={timeframe} value={timeframe}>{timeframeLabel(timeframe, lang)}</option>)}
          </select>
        </div>
      </div>

      {tab === "history" ? <p className="v37HistoryNote">{tr.historyNote}</p> : null}

      <div className="v37DecisionStack" data-v37-list={tab}>
        {filteredEntries.length ? (
          filteredEntries.map((entry, index) => (
            <DecisionCardV37
              key={entryKey(entry, tab, index)}
              entry={entry}
              tab={tab}
              lang={lang}
              readingMode={readingMode}
              index={index}
            />
          ))
        ) : (
          <div className="v37Empty">{tab === "history" ? tr.noHistory : tr.noCurrent}</div>
        )}
      </div>

      <div className="v37GovernanceNote">
        <strong>{tr.governance}</strong>
        <span>{tr.noFabricatedScore}</span>
      </div>
    </section>
  );
}

