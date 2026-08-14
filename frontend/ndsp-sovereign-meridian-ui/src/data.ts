export type Tone = "success" | "warning" | "danger" | "review" | "info" | "neutral";

export type InstrumentAnalysis = {
  id: string;
  name: string;
  symbol: string;
  direction: "صاعد" | "هابط" | "محايد";
  confidence: number;
  reportDate: string;
  effectiveWeek: string;
  freshness: string;
  evidence: Array<{ label: string; value: string; tone: Tone }>;
};

export const publicNavigation = [
  { label: "الرئيسية", path: "/" },
  { label: "المنهجية", path: "/methodology" },
  { label: "التحليل الحالي", path: "/analysis" },
  { label: "التوثيق", path: "/documentation" },
];

export const adminNavigation = [
  { label: "نظرة عامة", path: "/admin/cot/overview", icon: "overview" },
  { label: "التقارير", path: "/admin/cot/reports", icon: "reports" },
  { label: "التحكم اليومي", path: "/admin/cot/daily-control", icon: "calendar" },
  { label: "التجارب", path: "/admin/cot/experiments", icon: "experiments" },
  { label: "المقارنات", path: "/admin/cot/comparisons", icon: "compare" },
  { label: "الحوكمة", path: "/admin/cot/governance", icon: "governance" },
  { label: "سجل التدقيق", path: "/admin/cot/audit-logs", icon: "audit" },
  { label: "العقود", path: "/admin/cot/contracts", icon: "contracts" },
  { label: "الإعدادات", path: "/admin/cot/settings", icon: "settings" },
];

export const analyses: InstrumentAnalysis[] = [
  {
    id: "gold",
    name: "الذهب",
    symbol: "XAU/USD",
    direction: "صاعد",
    confidence: 84,
    reportDate: "2026-08-07",
    effectiveWeek: "2026-W32",
    freshness: "محدّث منذ 18 دقيقة",
    evidence: [
      { label: "مؤشر هيكلي (أ)", value: "تراكم إيجابي", tone: "success" },
      { label: "مؤشر هيكلي (ب)", value: "انكشاف منضبط", tone: "info" },
      { label: "الضغط الكلي", value: "داعم", tone: "success" },
      { label: "اكتمال الأدلة", value: "12 / 12", tone: "success" },
    ],
  },
  {
    id: "eur",
    name: "اليورو",
    symbol: "EUR/USD",
    direction: "محايد",
    confidence: 62,
    reportDate: "2026-08-07",
    effectiveWeek: "2026-W32",
    freshness: "محدّث منذ 21 دقيقة",
    evidence: [
      { label: "مؤشر هيكلي (أ)", value: "ميل إيجابي", tone: "success" },
      { label: "مؤشر هيكلي (ب)", value: "تعارض جزئي", tone: "warning" },
      { label: "الضغط الكلي", value: "غير حاسم", tone: "review" },
      { label: "اكتمال الأدلة", value: "10 / 12", tone: "warning" },
    ],
  },
  {
    id: "oil",
    name: "النفط الخام",
    symbol: "WTI",
    direction: "هابط",
    confidence: 76,
    reportDate: "2026-08-07",
    effectiveWeek: "2026-W32",
    freshness: "محدّث منذ 25 دقيقة",
    evidence: [
      { label: "مؤشر هيكلي (أ)", value: "تراجع مراكز", tone: "danger" },
      { label: "مؤشر هيكلي (ب)", value: "ضغط بيعي", tone: "danger" },
      { label: "الضغط الكلي", value: "سلبي", tone: "warning" },
      { label: "اكتمال الأدلة", value: "11 / 12", tone: "success" },
    ],
  },
];

export const adminRows = [
  {
    report: "COT · الذهب",
    week: "2026-W32",
    core: "صاعد",
    expanded: "صاعد",
    agreement: "متفق",
    status: "مكتمل",
  },
  {
    report: "COT · اليورو",
    week: "2026-W32",
    core: "محايد",
    expanded: "صاعد",
    agreement: "اختلاف",
    status: "قيد المراجعة",
  },
  {
    report: "COT · النفط الخام",
    week: "2026-W32",
    core: "هابط",
    expanded: "هابط",
    agreement: "متفق",
    status: "مكتمل",
  },
  {
    report: "TFF · مؤشر الدولار",
    week: "2026-W32",
    core: "محايد",
    expanded: "هابط",
    agreement: "اختلاف",
    status: "قيد المراجعة",
  },
];

export const serviceCards = [
  { name: "محرك حوكمة المؤشرات", version: "v2.8.1", environment: "Production", health: "سليم", lastRun: "08:30 التوقيت العالمي" },
  { name: "بوابة المؤشرات الأساسية", version: "v1.14.0", environment: "Production", health: "سليم", lastRun: "08:17 التوقيت العالمي" },
  { name: "منظور المعالجة المركزي", version: "v4.3.2", environment: "Production", health: "سليم", lastRun: "08:31 التوقيت العالمي" },
  { name: "EXPANDED Experiment", version: "v0.9.7", environment: "Shadow", health: "مراقبة", lastRun: "08:32 التوقيت العالمي" },
  { name: "التوقيت العالمي Calendar Policy", version: "v1.6.0", environment: "Global", health: "سليم", lastRun: "00:00 التوقيت العالمي" },
  { name: "Report Activation Policy", version: "v3.1.4", environment: "Production", health: "سليم", lastRun: "08:33 التوقيت العالمي" },
];
