import {
  ArrowLeft,
  ArrowsLeftRight,
  BracketsCurly,
  CalendarBlank,
  CaretDown,
  CheckCircle,
  Clock,
  Database,
  FileText,
  Flask,
  Funnel,
  GearSix,
  GitBranch,
  MagnifyingGlass,
  Plus,
  Pulse,
  Scroll,
  ShieldCheck,
  SlidersHorizontal,
  WarningCircle,
} from "@phosphor-icons/react";
import { useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import { GovernanceDialog } from "../../components/GovernanceDialog";
import { StatusChip } from "../../components/StatusChip";
import { adminRows, serviceCards } from "../../data";

function MetricCard({ label, value, meta, icon: Icon, tone = "neutral" }: { label: string; value: string; meta: string; icon: typeof Pulse; tone?: string }) {
  return (
    <article className={`metric-card metric-card--${tone}`}>
      <div className="metric-card__icon"><Icon size={21} /></div>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{meta}</small>
    </article>
  );
}

function ResultTable({ rows = adminRows }: { rows?: typeof adminRows }) {
  return (
    <div className="data-table-wrap">
      <table className="data-table">
        <thead><tr><th>التقرير</th><th>الأسبوع الفعّال</th><th>CORE</th><th>EXPANDED</th><th>الاتفاق</th><th>الحالة</th><th aria-label="إجراءات" /></tr></thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.report}>
              <td><strong>{row.report}</strong></td>
              <td dir="ltr">{row.week}</td>
              <td><StatusChip label={row.core} tone={row.core === "صاعد" ? "success" : row.core === "هابط" ? "danger" : "warning"} compact /></td>
              <td><StatusChip label={row.expanded} tone="review" compact /></td>
              <td><StatusChip label={row.agreement} tone={row.agreement === "متفق" ? "success" : "warning"} compact /></td>
              <td>{row.status}</td>
              <td><button className="table-action" type="button">عرض <ArrowLeft size={14} /></button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function AdminOverviewPage() {
  const [agreement, setAgreement] = useState("all");
  const [query, setQuery] = useState("");
  const [dialogOpen, setDialogOpen] = useState(false);
  const filteredRows = useMemo(() => adminRows.filter((row) => (agreement === "all" || row.agreement === agreement) && row.report.includes(query)), [agreement, query]);

  return (
    <>
      <section className="metrics-grid">
        <MetricCard label="تقارير فعّالة" value="24" meta="هذا الأسبوع" icon={FileText} tone="gold" />
        <MetricCard label="اتفاق CORE" value="87%" meta="+4% عن الأسبوع الماضي" icon={CheckCircle} tone="success" />
        <MetricCard label="تجارب نشطة" value="3" meta="SHADOW MODE" icon={Flask} tone="review" />
        <MetricCard label="عناصر للمراجعة" value="5" meta="تحتاج قرارًا" icon={WarningCircle} tone="warning" />
      </section>

      <section className="admin-panel">
        <header className="admin-panel__header">
          <div><span className="eyebrow">CORE / EXPANDED</span><h2>نتائج الأسبوع الفعّال</h2><p>مقارنة داخلية لا تظهر في الواجهة العامة.</p></div>
          <button className="button button--primary button--small" type="button" onClick={() => setDialogOpen(true)}><ShieldCheck size={17} /> إنشاء طلب ترقية</button>
        </header>

        <div className="filter-bar">
          <label><MagnifyingGlass size={16} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="ابحث عن تقرير" /></label>
          <div className="filter-chips" aria-label="مرشح الاتفاق">
            <button className={agreement === "all" ? "active" : ""} type="button" onClick={() => setAgreement("all")}>الكل</button>
            <button className={agreement === "متفق" ? "active" : ""} type="button" onClick={() => setAgreement("متفق")}>متفق</button>
            <button className={agreement === "اختلاف" ? "active" : ""} type="button" onClick={() => setAgreement("اختلاف")}>اختلاف</button>
          </div>
          <button className="button button--ghost button--small" type="button"><Funnel size={16} /> مرشحات متقدمة</button>
        </div>
        <ResultTable rows={filteredRows} />
      </section>

      <section className="admin-two-column">
        <article className="admin-panel compact-panel">
          <header className="admin-panel__header"><div><span className="eyebrow">SYSTEM HEALTH</span><h2>سلامة الخدمات</h2></div><StatusChip label="6 / 6 سليمة" tone="success" /></header>
          <div className="health-list">
            {serviceCards.slice(0, 4).map((service) => <div key={service.name}><span className="health-dot" /><div><strong dir="ltr">{service.name}</strong><small dir="ltr">{service.version} · {service.lastRun}</small></div><StatusChip label={service.health} tone={service.health === "سليم" ? "success" : "warning"} compact /></div>)}
          </div>
        </article>
        <article className="admin-panel compact-panel">
          <header className="admin-panel__header"><div><span className="eyebrow">GOVERNANCE QUEUE</span><h2>القرارات المعلّقة</h2></div><span className="count-badge">3</span></header>
          <div className="decision-list">
            <button type="button" onClick={() => setDialogOpen(true)}><span><strong>ترقية Perspective v4.4</strong><small>يتطلب اعتمادين</small></span><ArrowLeft size={16} /></button>
            <button type="button"><span><strong>اعتماد التوقيت العالمي Policy v1.7</strong><small>مراجعة أثر التوقيت</small></span><ArrowLeft size={16} /></button>
            <button type="button"><span><strong>إغلاق تجربة E-029</strong><small>اكتملت 16 دورة</small></span><ArrowLeft size={16} /></button>
          </div>
        </article>
      </section>

      <GovernanceDialog open={dialogOpen} onClose={() => setDialogOpen(false)} />
    </>
  );
}

export function AdminReportsPage() {
  const [mode, setMode] = useState("all");
  const rows = useMemo(() => adminRows.filter((row) => mode === "all" || (mode === "agreement" ? row.agreement === "متفق" : row.agreement === "اختلاف")), [mode]);

  return (
    <section className="admin-panel">
      <header className="admin-panel__header"><div><span className="eyebrow">REPORT REGISTRY</span><h2>سجل التقارير</h2><p>كل تقرير مرتبط بأسبوع فعّال وإصدار وأثر بيانات.</p></div><button className="button button--outline button--small" type="button"><Plus size={16} /> استيراد تقرير</button></header>
      <div className="filter-bar">
        <div className="filter-chips"><button className={mode === "all" ? "active" : ""} onClick={() => setMode("all")}>الكل</button><button className={mode === "agreement" ? "active" : ""} onClick={() => setMode("agreement")}>متفق</button><button className={mode === "difference" ? "active" : ""} onClick={() => setMode("difference")}>اختلاف</button></div>
        <button className="button button--ghost button--small" type="button"><CalendarBlank size={16} /> 2026-W32 <CaretDown size={14} /></button>
      </div>
      <ResultTable rows={rows} />
    </section>
  );
}

export function AdminExperimentsPage() {
  const [created, setCreated] = useState(false);
  const experiments = [
    { id: "E-031", name: "Expanded Day-Control", version: "v0.9.7", runs: "12 / 16", status: "RUNNING", delta: "+3.8%" },
    { id: "E-029", name: "Perspective Weighting", version: "v0.8.4", runs: "16 / 16", status: "READY FOR REVIEW", delta: "+1.2%" },
    { id: "E-027", name: "Macro Conflict Gate", version: "v0.7.9", runs: "16 / 16", status: "STOPPED", delta: "-0.6%" },
  ];

  return (
    <>
      <div className="admin-callout"><ShieldCheck size={21} /><div><strong>عزل كامل عن المسار العام</strong><p>جميع التجارب تعمل في SHADOW MODE ولا تملك صلاحية الكتابة إلى Public API.</p></div><StatusChip label="PUBLIC EXPOSURE · DISABLED" tone="success" /></div>
      <section className="admin-panel">
        <header className="admin-panel__header"><div><span className="eyebrow">EXPERIMENT REGISTRY</span><h2>الاختبارات النشطة والسابقة</h2></div><button className="button button--primary button--small" type="button" onClick={() => setCreated(true)}><Plus size={16} /> Start Shadow Test</button></header>
        {created && <div className="inline-success"><CheckCircle size={18} weight="fill" /> تم إنشاء مسودة تجربة جديدة. لم يبدأ التشغيل بعد.</div>}
        <div className="experiment-grid">
          {experiments.map((experiment) => (
            <article key={experiment.id} className="experiment-card">
              <header><span dir="ltr">{experiment.id}</span><StatusChip label={experiment.status} tone={experiment.status === "RUNNING" ? "success" : experiment.status === "STOPPED" ? "danger" : "review"} compact /></header>
              <h3 dir="ltr">{experiment.name}</h3><p dir="ltr">{experiment.version}</p>
              <div className="experiment-card__stats"><span>الدورات<strong dir="ltr">{experiment.runs}</strong></span><span>فرق الدقة<strong dir="ltr">{experiment.delta}</strong></span></div>
              <button type="button">فتح التجربة <ArrowLeft size={15} /></button>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}

export function AdminGovernancePage() {
  const [dialogOpen, setDialogOpen] = useState(false);
  const requests = [
    { id: "GPR-104", title: "Promote Day-Control Perspective", from: "EXPANDED v0.9.7", to: "CORE v4.4.0", owner: "Governance Council", status: "قيد الاعتماد" },
    { id: "GPR-103", title: "Update التوقيت العالمي Calendar Policy", from: "v1.6.0", to: "v1.7.0", owner: "Platform Operations", status: "مسودة" },
    { id: "GPR-102", title: "Evidence Completeness Gate", from: "v3.2.0", to: "v3.2.1", owner: "Data Governance", status: "معتمد" },
  ];

  return (
    <section className="admin-panel">
      <header className="admin-panel__header"><div><span className="eyebrow">PROMOTION REQUESTS</span><h2>طلبات التغيير والاعتماد</h2><p>كل تغيير حساس يوضح أثره والإصدار والسبب وتوقيت التنفيذ.</p></div><button className="button button--primary button--small" type="button" onClick={() => setDialogOpen(true)}><Plus size={16} /> طلب جديد</button></header>
      <div className="governance-list">
        {requests.map((request) => <article key={request.id}><div className="governance-list__id" dir="ltr">{request.id}</div><div><h3 dir="ltr">{request.title}</h3><p>{request.owner}</p></div><div className="governance-list__versions" dir="ltr"><span>{request.from}</span><ArrowLeft size={14} /><strong>{request.to}</strong></div><StatusChip label={request.status} tone={request.status === "معتمد" ? "success" : request.status === "مسودة" ? "neutral" : "warning"} /></article>)}
      </div>
      <GovernanceDialog open={dialogOpen} onClose={() => setDialogOpen(false)} />
    </section>
  );
}

const settingTabs = ["عام", "المنظور الهيكلي", "التحكم اليومي", "التوقيت العالمي", "الاختبار الظلي", "الصلاحيات", "سجل التدقيق", "عقود النظام"];

export function AdminSettingsPage() {
  const [tab, setTab] = useState(settingTabs[0]);
  return (
    <>
      <div className="settings-tabs" role="tablist" aria-label="أقسام الإعدادات">{settingTabs.map((item) => <button role="tab" aria-selected={tab === item} className={tab === item ? "active" : ""} key={item} onClick={() => setTab(item)} dir="ltr">{item}</button>)}</div>
      <section className="admin-panel">
        <header className="admin-panel__header"><div><span className="eyebrow">{tab.toUpperCase()}</span><h2>الخدمات والسياسات</h2><p>كل مكوّن مستقل بإصداره وحالته وبيئته وآخر تعديل حوكمي.</p></div><button className="button button--outline button--small" type="button"><GearSix size={16} /> إعدادات القسم</button></header>
        <div className="service-grid">
          {serviceCards.map((service) => (
            <article key={service.name} className="service-card">
              <header><div className="service-card__icon"><Database size={20} /></div><StatusChip label={service.health} tone={service.health === "سليم" ? "success" : "warning"} compact /></header>
              <h3 dir="ltr">{service.name}</h3><span dir="ltr">{service.version}</span>
              <dl><div><dt>البيئة</dt><dd dir="ltr">{service.environment}</dd></div><div><dt>آخر تشغيل</dt><dd dir="ltr">{service.lastRun}</dd></div><div><dt>آخر تعديل حوكمي</dt><dd dir="ltr">2026-08-08</dd></div></dl>
              <button type="button">عرض السجل <ArrowLeft size={14} /></button>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}

const genericConfig = {
  "daily-control": { icon: CalendarBlank, title: "سياسة الأسبوع الفعّال", text: "تحديد يوم التفعيل ومنطقة التوقيت العالمي وحالة آخر تقرير، مع منع أي تداخل بين أسبوعين.", action: "تعديل السياسة" },
  comparisons: { icon: ArrowsLeftRight, title: "مقارنة النسخ", text: "اختر نسختين لمقارنة الاتجاه وقوة الأدلة والبوابات المتأثرة دون تغيير أي نتيجة.", action: "إنشاء مقارنة" },
  "audit-logs": { icon: Scroll, title: "أثر تشغيلي قابل للتدقيق", text: "بحث دقيق حسب المستخدم والخدمة والإصدار والوقت والحالة، مع عرض الفرق قبل وبعد.", action: "تصدير السجل" },
  contracts: { icon: BracketsCurly, title: "حدود العقود البرمجية", text: "Public API يقرأ من CORE فقط، بينما تبقى عقود المراجعة والتجارب ضمن الشبكة الداخلية.", action: "عرض OpenAPI" },
};

export function AdminGenericPage() {
  const location = useLocation();
  const key = location.pathname.split("/").filter(Boolean).at(-1) as keyof typeof genericConfig;
  const config = genericConfig[key] ?? genericConfig["daily-control"];
  const Icon = config.icon;
  return (
    <section className="admin-panel generic-admin-page">
      <div className="generic-admin-page__hero"><div className="generic-admin-page__icon"><Icon size={32} /></div><div><span className="eyebrow">CONTROLLED WORKSPACE</span><h2>{config.title}</h2><p>{config.text}</p></div><button className="button button--primary" type="button">{config.action} <ArrowLeft size={16} /></button></div>
      <div className="generic-card-grid">
        <article><Clock size={21} /><span>آخر تحديث</span><strong dir="ltr">2026-08-11 · 08:34 التوقيت العالمي</strong></article>
        <article><ShieldCheck size={21} /><span>الإصدار الحوكمي</span><strong dir="ltr">v4.3.2</strong></article>
        <article><GitBranch size={21} /><span>حالة النشر</span><strong>مستقر</strong></article>
      </div>
      <div className="generic-empty-state"><SlidersHorizontal size={32} /><h3>اختر مرشحًا للبدء</h3><p>المكوّن جاهز لربطه بمصدر البيانات الفعلي دون تغيير بنية الواجهة.</p><button className="button button--outline" type="button">فتح المرشحات</button></div>
    </section>
  );
}
