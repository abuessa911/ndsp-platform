import {
  ArrowDown,
  ArrowUp,
  CalendarBlank,
  CheckCircle,
  Clock,
  Minus,
  ShieldCheck,
} from "@phosphor-icons/react";
import { useMemo, useState } from "react";
import { AuthorityBar } from "../components/AuthorityBar";
import { StatusChip } from "../components/StatusChip";
import { analyses } from "../data";

export function AnalysisPage() {
  const [selectedId, setSelectedId] = useState(analyses[0].id);
  const analysis = useMemo(() => analyses.find((item) => item.id === selectedId) ?? analyses[0], [selectedId]);
  const DirectionIcon = analysis.direction === "صاعد" ? ArrowUp : analysis.direction === "هابط" ? ArrowDown : Minus;
  const directionTone = analysis.direction === "صاعد" ? "success" : analysis.direction === "هابط" ? "danger" : "warning";

  return (
    <div className="page-surface analysis-page">
      <section className="page-hero page-hero--compact">
        <div className="container">
          <span className="eyebrow">CURRENT ANALYSIS</span>
          <h1>التحليل الرسمي الحالي</h1>
          <p>آخر نتيجة معتمدة، مع مستوى الثقة وحداثة التقرير والأدلة المساندة.</p>
        </div>
      </section>

      <section className="container analysis-workspace">
        <div className="segmented-control" aria-label="اختر الأداة">
          {analyses.map((item) => (
            <button key={item.id} type="button" className={item.id === selectedId ? "active" : ""} onClick={() => setSelectedId(item.id)}>
              <span>{item.name}</span><small dir="ltr">{item.symbol}</small>
            </button>
          ))}
        </div>

        <article className="official-result">
          <header className="official-result__header">
            <div><span className="eyebrow">OFFICIAL DIRECTION</span><h2>{analysis.name}</h2><span dir="ltr">{analysis.symbol}</span></div>
            <StatusChip label={analysis.freshness} tone="success" />
          </header>

          <div className="official-result__body">
            <div className={`direction-orb direction-orb--${directionTone}`}>
              <DirectionIcon size={34} weight="bold" />
              <strong>{analysis.direction}</strong>
              <span>الاتجاه الرسمي</span>
            </div>
            <div className="confidence-block">
              <div><span>قوة الأدلة</span><strong>{analysis.confidence}%</strong></div>
              <div className="confidence-track" role="progressbar" aria-valuemin={0} aria-valuemax={100} aria-valuenow={analysis.confidence}>
                <span style={{ inlineSize: `${analysis.confidence}%` }} />
              </div>
              <p>اتفاق مرتفع بين المنظور المؤسسي والسياق الكلي مع اكتمال بوابات الحوكمة.</p>
            </div>
          </div>

          <AuthorityBar compact />
        </article>

        <div className="analysis-meta-grid">
          <article><CalendarBlank size={20} /><span>تاريخ التقرير</span><strong dir="ltr">{analysis.reportDate}</strong></article>
          <article><Clock size={20} /><span>الأسبوع الفعّال</span><strong dir="ltr">{analysis.effectiveWeek}</strong></article>
          <article><ShieldCheck size={20} /><span>الإصدار الحوكمي</span><strong dir="ltr">CORE v4.3.2</strong></article>
          <article><CheckCircle size={20} /><span>حالة النشر</span><strong>معتمد</strong></article>
        </div>

        <section className="evidence-section">
          <div className="section-heading"><span className="eyebrow">VERIFIABLE EVIDENCE</span><h2>ملخص الأدلة</h2><p>المؤشرات التي تفسر الاتجاه دون كشف تفاصيل تشغيلية داخلية.</p></div>
          <div className="evidence-grid">
            {analysis.evidence.map((item) => (
              <article key={item.label}><span>{item.label}</span><StatusChip label={item.value} tone={item.tone} /></article>
            ))}
          </div>
        </section>
      </section>
    </div>
  );
}
