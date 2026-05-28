import express from "express";
import cors from "cors";

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

const auditLogs = [];
const displaySwitches = { BTC: false, ETH: false, GOLD: false, GLOBAL: false };

function audit(action, details = {}) {
  auditLogs.unshift({
    id: `audit_${Date.now()}`,
    action,
    details,
    created_at: new Date().toISOString()
  });
  if (auditLogs.length > 100) auditLogs.pop();
}

const mockContext = {
  BTC: {
    asset: "BTC",
    public_state: "سياق سوق مستقر نسبيًا",
    analytical_bias: "انحياز تحليلي إيجابي منضبط",
    context_quality: 86.4,
    risk_state: "مراقبة متوسطة",
    decision_zone: "64,176.70",
    user_notice: "هذه قراءة تحليلية عامة لدعم القرار وليست توصية مالية أو تنفيذًا مباشرًا أو ضمانًا للنتائج."
  },
  ETH: {
    asset: "ETH",
    public_state: "سياق متابعة نشط",
    analytical_bias: "انحياز تحليلي متوازن",
    context_quality: 82.1,
    risk_state: "مراقبة منخفضة",
    decision_zone: "3,418.00",
    user_notice: "هذه قراءة تحليلية عامة لدعم القرار وليست توصية مالية أو تنفيذًا مباشرًا أو ضمانًا للنتائج."
  },
  GOLD: {
    asset: "GOLD",
    public_state: "سياق حساس للتذبذب",
    analytical_bias: "انحياز تحليلي محافظ",
    context_quality: 79.8,
    risk_state: "مراقبة مرتفعة",
    decision_zone: "2,340.00",
    user_notice: "هذه قراءة تحليلية عامة لدعم القرار وليست توصية مالية أو تنفيذًا مباشرًا أو ضمانًا للنتائج."
  }
};

app.get("/api/health", (req, res) => {
  res.json({ ok: true, service: "ndsp-api", mode: "sanitized" });
});

app.get("/api/context/:asset", (req, res) => {
  const asset = String(req.params.asset || "BTC").toUpperCase();

  if (displaySwitches.GLOBAL || displaySwitches[asset]) {
    audit("PUBLIC_CONTEXT_BLOCKED", { asset });
    return res.json({
      asset,
      public_state: "العرض العام متوقف مؤقتًا",
      context_quality: 0,
      risk_state: "تعليق العرض",
      user_notice: "تم تعليق عرض هذا السياق مؤقتًا من لوحة الإدارة."
    });
  }

  audit("PUBLIC_CONTEXT_READ", { asset });
  res.json(mockContext[asset] || mockContext.BTC);
});

app.get("/api/trial/status", (req, res) => {
  res.json({
    trial_name: "NDSP Elite Trial",
    duration_days: 16,
    total_seats: 50,
    used_seats: 36,
    state: "active",
    segments: {
      ordinary: { used: 14, total: 20 },
      specialist: { used: 6, total: 10 },
      featured: { used: 16, total: 20 }
    },
    notice: "التجربة تعرض وصولًا محكومًا ومخرجات عامة آمنة دون كشف أي منطق داخلي حساس."
  });
});

app.post("/api/admin/display-switch", (req, res) => {
  const { asset = "GLOBAL", halted = false } = req.body || {};
  const key = String(asset).toUpperCase();

  if (!Object.prototype.hasOwnProperty.call(displaySwitches, key)) {
    return res.status(400).json({ ok: false, error: "Unsupported display target." });
  }

  displaySwitches[key] = Boolean(halted);
  audit("DISPLAY_SWITCH_UPDATED", { target: key, halted: Boolean(halted) });

  res.json({ ok: true, display_switches: displaySwitches });
});

app.get("/api/admin/audit-logs", (req, res) => {
  res.json({ ok: true, logs: auditLogs });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`NDSP API running on http://0.0.0.0:${PORT}`);
});
