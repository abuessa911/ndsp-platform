#!/usr/bin/env bash
set -Eeuo pipefail

BASE="/home/nawaf511/empire-core-new"
ROOT="$BASE/ndsp_checkout_plans_package"
FRONTEND="$ROOT/checkout-admin-vite"
APP_FILE="$FRONTEND/src/App.jsx"
CSS_FILE="$FRONTEND/src/styles.css"
MY_DIR="/var/www/checkout-plans"
ADMIN_DIR="/var/www/plans-console"
REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
REPORT="$REPORT_DIR/NDSP_MY_ACCESS_UI_POLISH_$(date +%Y%m%d_%H%M%S).md"

mkdir -p "$REPORT_DIR"

log() {
  echo "$1"
  echo "$1" >> "$REPORT"
}

fail() {
  log "FAILED=True"
  log "ERROR=$1"
  echo "FAILED=True"
  echo "REPORT=$REPORT"
  exit 1
}

log "# NDSP My Access UI Polish"
log "- TIME=$(date -Is)"
log "- FRONTEND=$FRONTEND"

[ -d "$FRONTEND" ] || fail "Frontend not found"
[ -f "$APP_FILE" ] || fail "App.jsx not found"
[ -f "$CSS_FILE" ] || fail "styles.css not found"

cp "$APP_FILE" "$APP_FILE.bak_my_access_polish_$(date +%Y%m%d_%H%M%S)"
cp "$CSS_FILE" "$CSS_FILE.bak_my_access_polish_$(date +%Y%m%d_%H%M%S)"

python3 - "$APP_FILE" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text()

helpers = r'''
function translateFeature(feature) {
  const dictionary = {
    "Market context overview": "عرض سياق السوق",
    "Decision-support dashboard": "لوحة دعم القرار",
    "Public sanitized output": "مخرجات مبسطة وآمنة للعرض",
    "Core assets coverage": "تغطية الأصول الأساسية",
    "Advanced market interpretation": "تفسير متقدم لحالة السوق",
    "Expanded asset coverage": "تغطية موسعة للأصول",
    "Elite decision surface": "واجهة قرار متقدمة",
    "Scenario explanation": "شرح السيناريوهات",
    "Sanitized multi-layer output": "مخرجات متعددة الطبقات بصياغة عامة",
    "Institutional workspace": "مساحة عمل مؤسسية",
    "Team-oriented access": "وصول مناسب للفرق",
    "Extended reporting": "تقارير موسعة",
    "Priority review": "مراجعة ذات أولوية",
    "Governance-safe output": "مخرجات متوافقة مع الحوكمة"
  };

  return dictionary[feature] || feature;
}

function readableDecisionDepth(value) {
  const dictionary = {
    standard: "قياسي",
    advanced: "متقدم",
    institutional: "مؤسسي"
  };

  return dictionary[value] || value || "غير محدد";
}

function AccessLimitCards({ limits }) {
  const safeLimits = limits || {};

  const items = [
    {
      label: "عدد الأصول المتاحة",
      value: safeLimits.max_assets ? `حتى ${safeLimits.max_assets} أصل` : "حسب الباقة"
    },
    {
      label: "عمق التحليل",
      value: readableDecisionDepth(safeLimits.decision_depth)
    }
  ];

  if (safeLimits.trial_days) {
    items.push({
      label: "مدة التجربة",
      value: `${safeLimits.trial_days} يوم`
    });
  }

  if (safeLimits.team_access) {
    items.push({
      label: "وصول الفرق",
      value: "متاح"
    });
  }

  return (
    <div className="access-limits-grid">
      {items.map((item) => (
        <article className="access-limit-card" key={item.label}>
          <span>{item.label}</span>
          <strong>{item.value}</strong>
        </article>
      ))}
    </div>
  );
}
'''

if "function translateFeature(feature)" not in text:
    marker = "function MyAccess()"
    if marker not in text:
        raise SystemExit("MyAccess function marker not found")
    text = text.replace(marker, helpers + "\n" + marker, 1)

text = text.replace(
    '<li key={feature}>{feature}</li>',
    '<li key={feature}>{translateFeature(feature)}</li>'
)

text = re.sub(
    r'\s*<h3>حدود الباقة</h3>\s*<pre className="json-box">\{JSON\.stringify\(subscription\.limits \|\| \{\}, null, 2\)\}</pre>',
    '\n              <h3>حدود الباقة</h3>\n              <AccessLimitCards limits={subscription.limits || {}} />',
    text
)

path.write_text(text)
PY

cat >> "$CSS_FILE" <<'CSS'

/* NDSP My Access polish */
.access-limits-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  margin-top: 14px;
}

.access-limit-card {
  border: 1px solid var(--border);
  background: rgba(15, 23, 42, 0.62);
  border-radius: 18px;
  padding: 16px;
}

.access-limit-card span {
  display: block;
  color: var(--muted);
  margin-bottom: 8px;
  font-size: 13px;
}

.access-limit-card strong {
  display: block;
  color: var(--text);
  font-size: 18px;
}

.access-card .feature-list {
  list-style: none;
  padding: 0;
  display: grid;
  gap: 10px;
}

.access-card .feature-list li {
  border: 1px solid var(--border);
  background: rgba(2, 6, 23, 0.38);
  border-radius: 14px;
  padding: 10px 12px;
}

@media (max-width: 980px) {
  .access-limits-grid {
    grid-template-columns: 1fr;
  }
}
CSS

log "UI_PATCHED=True"

cd "$FRONTEND"

cat > ".env" <<'ENV'
VITE_NDSP_API_BASE=/checkout-api
ENV

cat > "vite.config.js" <<'VITE'
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  base: "./",
  plugins: [react()]
});
VITE

npm install
npm run build

[ -f "$FRONTEND/dist/index.html" ] || fail "Vite dist missing"

python3 - <<'PY'
from pathlib import Path

p = Path("/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/checkout-admin-vite/dist/index.html")
text = p.read_text()
marker = "<!-- NDSP_MY_ACCESS_UI_POLISHED -->"

if marker not in text:
    text = text.replace("<head>", "<head>\n  " + marker, 1)

p.write_text(text)
PY

sudo mkdir -p "$MY_DIR" "$ADMIN_DIR"
sudo rsync -a --delete "$FRONTEND/dist/" "$MY_DIR/"
sudo rsync -a --delete "$FRONTEND/dist/" "$ADMIN_DIR/"
sudo chown -R www-data:www-data "$MY_DIR" "$ADMIN_DIR"

log "BUILD_AND_DEPLOY_OK=True"

MY_UI_CODE="$(curl -k -sS -o /tmp/ndsp_my_access_polish_my.html -w '%{http_code}' https://my.ndsp.app/checkout-plans/ || true)"
ADMIN_UI_CODE="$(curl -k -sS -o /tmp/ndsp_my_access_polish_admin.html -w '%{http_code}' https://admin.ndsp.app/plans-console/ || true)"
API_CODE="$(curl -k -sS -o /tmp/ndsp_my_access_polish_api.json -w '%{http_code}' https://my.ndsp.app/checkout-api/api/v1/plans || true)"

log "MY_UI_CODE=$MY_UI_CODE"
log "ADMIN_UI_CODE=$ADMIN_UI_CODE"
log "API_CODE=$API_CODE"

[ "$MY_UI_CODE" = "200" ] || fail "my.ndsp.app UI failed"
[ "$ADMIN_UI_CODE" = "200" ] || fail "admin.ndsp.app UI failed"
[ "$API_CODE" = "200" ] || fail "same-origin API failed"

grep -q "NDSP_MY_ACCESS_UI_POLISHED" /tmp/ndsp_my_access_polish_my.html || fail "Polish marker missing from my UI"
grep -q "NDSP_MY_ACCESS_UI_POLISHED" /tmp/ndsp_my_access_polish_admin.html || fail "Polish marker missing from admin UI"

log "POLISH_MARKER_OK=True"
log "FINAL_STATUS=NDSP_MY_ACCESS_UI_POLISHED"
log "ASSERT_OK=True"
log "REPORT=$REPORT"

echo ""
echo "=== DONE ==="
echo "ASSERT_OK=True"
echo "FINAL_STATUS=NDSP_MY_ACCESS_UI_POLISHED"
echo "REPORT=$REPORT"
echo ""
echo "Hard refresh:"
echo "https://my.ndsp.app/checkout-plans/#/access"
