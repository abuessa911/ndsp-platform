import type {
  CorePublic,
  EvidencePayload,
  MarketContext,
  PublicOverview,
} from "@/contracts/public-contracts"

export const demoOverview: PublicOverview = {
  mode: "demo",
  updatedAt: new Date().toISOString(),
  kpis: [
    {
      id: "governance",
      label: "الحوكمة",
      value: "معتمد",
      detail: "Public Projection",
      status: "positive",
    },
    {
      id: "evidence",
      label: "الأدلة",
      value: "متاحة",
      detail: "Authorized Evidence",
      status: "positive",
    },
    {
      id: "freshness",
      label: "حداثة البيانات",
      value: "حديثة",
      detail: "Freshness Aware",
      status: "neutral",
    },
  ],
  trend: [
    { label: "03 أغسطس", value: 42 },
    { label: "04 أغسطس", value: 48 },
    { label: "05 أغسطس", value: 46 },
    { label: "06 أغسطس", value: 55 },
    { label: "07 أغسطس", value: 59 },
    { label: "08 أغسطس", value: 63 },
  ],
}

export const demoCore: CorePublic = {
  mode: "demo",
  updatedAt: new Date().toISOString(),
  direction: "الاتجاه الرسمي",
  summary:
    "ستعرض هذه المساحة مخرج CORE العام المصرح به بعد ربط Public API الحقيقي.",
  governanceStatus: "Governance Protected",
  evidenceStatus: "Authorized Evidence",
  freshnessStatus: "Freshness Aware",
}

export const demoMarketContext: MarketContext = {
  mode: "demo",
  updatedAt: new Date().toISOString(),
  title: "سياق السوق",
  summary:
    "تمثيل توضيحي لواجهة السياق. لا تمثل القيم الحالية توصية أو نتيجة فعلية.",
  contextSeries: [
    { label: "03 أغسطس", value: 35 },
    { label: "04 أغسطس", value: 39 },
    { label: "05 أغسطس", value: 37 },
    { label: "06 أغسطس", value: 45 },
    { label: "07 أغسطس", value: 50 },
    { label: "08 أغسطس", value: 54 },
  ],
}

export const demoEvidence: EvidencePayload = {
  mode: "demo",
  updatedAt: new Date().toISOString(),
  rows: [
    {
      id: "EV-001",
      source: "مصدر مؤسسي",
      category: "بيانات مؤسسية",
      status: "مصرح",
      freshness: "حديث",
      updatedAt: new Date().toISOString(),
    },
    {
      id: "EV-002",
      source: "مرجع تحليلي",
      category: "تقارير وتحليلات",
      status: "مصرح",
      freshness: "حديث",
      updatedAt: new Date().toISOString(),
    },
    {
      id: "EV-003",
      source: "سياق تشغيلي",
      category: "سياق تشغيلي",
      status: "مصرح",
      freshness: "مراجع",
      updatedAt: new Date().toISOString(),
    },
    {
      id: "EV-004",
      source: "مصدر خارجي",
      category: "معلومات خارجية",
      status: "مصرح",
      freshness: "حديث",
      updatedAt: new Date().toISOString(),
    },
    {
      id: "EV-005",
      source: "مرجع معياري",
      category: "معايير وسياسات",
      status: "مصرح",
      freshness: "مراجع",
      updatedAt: new Date().toISOString(),
    },
  ],
}
