set -Eeuo pipefail

PROJECT_ROOT="/home/nawaf511/empire-core-v5-1-1-clean"
cd "$PROJECT_ROOT"

STAMP="$(date +%Y%m%d_%H%M%S)"
REPORT_DIR="$PROJECT_ROOT/ndsp-final-visible-cleanup-$STAMP"
BACKUP="/home/nawaf511/ndsp-final-visible-cleanup-backup-$STAMP.tar.gz"

mkdir -p "$REPORT_DIR"

echo "NDSP final visible cleanup"
echo "Project: $PROJECT_ROOT"
echo "Report: $REPORT_DIR"
echo "Backup: $BACKUP"

tar \
  --exclude='./node_modules' \
  --exclude='./backend/node_modules' \
  --exclude='./runtime' \
  --exclude='./backend/runtime' \
  --exclude='./.git' \
  --exclude='./.next' \
  --exclude='./dist' \
  --exclude='./build' \
  --exclude='./coverage' \
  --exclude='./var' \
  --exclude='./backups' \
  --exclude='./backup' \
  --exclude='./archive' \
  --exclude='./archives' \
  --exclude='./backend/_backups' \
  --exclude='./backend/architecture/reports' \
  -czf "$BACKUP" .

CHANGED="$REPORT_DIR/changed-files.txt"
: > "$CHANGED"

patch_file() {
  local f="$1"
  [ -f "$f" ] || return 0

  local before after
  before="$(sha256sum "$f" | awk '{print $1}')"

  perl -0pi -e '
    s/منصة نواف لدعم القرار/منصة دعم القرار/g;
    s/إشارة نواف الذهبية المعززة/الإشارة الذهبية المعززة/g;
    s/إشارة نواف الذهبية/الإشارة الذهبية/g;
    s/نقطة التقاء نواف/NMP/g;
    s/منطق البعد الزمني/TDL/g;

    s/Nawaf Decision Support Platform/Decision Support Platform/g;
    s/NAWAF DECISION SUPPORT PLATFORM/DECISION SUPPORT PLATFORM/g;
    s/nawaf decision support platform/decision support platform/g;

    s/Nawaf Meeting Point/NMP/g;
    s/Nawaf Meet Point/NMP/g;
    s/NAWAF MEETING POINT/NMP/g;

    s/Enhanced Nawaf Golden Signal/Enhanced Golden Signal/g;
    s/Nawaf Enhanced Golden Signal/Enhanced Golden Signal/g;
    s/Nawaf Golden Signal/Golden Signal/g;

    s/Nawaf Golden Alignment/Golden Signal/g;
    s/NAWAF GOLDEN ALIGNMENT/GOLDEN SIGNAL/g;
    s/nawaf golden alignment/Golden Signal/g;

    s/Even '\''Golden Signal'\'' is/Even Golden Signal is/g;
    s/Even '\''Nawaf Golden Alignment'\'' is/Even Golden Signal is/g;

    s/<b style="color:var\(--txt\)">Nawaf<\/b>/<b style="color:var(--txt)">NDSP<\/b>/g;
    s/>Nawaf</>NDSP</g;

    s/إشارة شراء استراتيجية/تحديث قرار استراتيجي/g;
    s/إشارة بيع/تحديث مخاطر/g;
    s/إشارة شراء/تحديث قرار/g;
    s/buy signal/decision update/ig;
    s/sell signal/risk update/ig;
  ' "$f"

  after="$(sha256sum "$f" | awk '{print $1}')"
  if [ "$before" != "$after" ]; then
    echo "$f" >> "$CHANGED"
  fi
}

echo "Patching active user-facing and policy files..."

TARGETS=(
  "./apps/admin-console/index.html"
  "./apps/admin-console/NDSP_Admin_Console.html"
  "./apps/admin-console/NDSP_Admin_Operations_Center.html"
  "./apps/admin-console/NDSP_Help_Center.html"
  "./apps/admin-console/NDSP_Terms_Privacy.html"
  "./apps/admin-console/NDSP_Design_System.html"
  "./apps/admin-console/NMP_Research_Lab.html"
  "./apps/admin-console/data/owner-layer-source-map.json"
  "./apps/admin-console/nmp-lab-summary.json"

  "./apps/user-portal/lib/ndsp-data.ts"
  "./apps/user-portal/components/command-center.tsx"
  "./apps/user-portal/components/dashboard-shell.tsx"
  "./apps/user-portal/components/devil-advocate-visible-card.tsx"
  "./apps/user-portal/components/charts.tsx"
  "./apps/user-portal/app/page.tsx"
  "./apps/user-portal/app/layout.tsx"
  "./apps/user-portal/app/landing/page.tsx"
  "./apps/user-portal/app/upgrade/page.tsx"
  "./apps/user-portal/app/account/page.tsx"
  "./apps/user-portal/app/settings/page.tsx"
  "./apps/user-portal/app/daily-brief/page.tsx"
  "./apps/user-portal/app/market-intelligence/page.tsx"
  "./apps/user-portal/data/command-center-real.json"
  "./apps/user-portal/public/ndsp-devil-advocate-integrated-final.js"

  "./apps/public-landing/index.html"

  "./backend/auth_api/ndsp_layer_name_masking_policy.cjs"
  "./backend/auth_api/ndsp_saas_packages_policy.cjs"
  "./backend/auth_api/ndsp_admin_ui_proxy.cjs"
  "./backend/ndsp_layer_name_masking_policy.cjs"
  "./backend/ndsp_saas_packages_policy.cjs"
  "./backend/ndsp_admin_ui_proxy.cjs"

  "./apps/ndsp-commercial-auth-payment-staging/server/src/server.ts"
)

for f in "${TARGETS[@]}"; do
  patch_file "$f"
done

echo "Adding explicit public layer masking policy where applicable..."

for f in \
  "./backend/auth_api/ndsp_layer_name_masking_policy.cjs" \
  "./backend/ndsp_layer_name_masking_policy.cjs"
do
  if [ -f "$f" ]; then
    perl -0pi -e "
      s/visible:\s*\['TDL',\s*'NMP',\s*\"Devil's Advocate\",\s*'Golden Signal'\]/visible: ['TDL', 'NMP', \"Devil's Advocate\", 'Golden Signal']/g;
      s/\{\s*name:\s*'NMP',\s*ar:\s*'NMP'\s*\}/{ name: 'NMP', ar: 'NMP' }/g;
      s/\{\s*name:\s*'Golden Signal',\s*ar:\s*'الإشارة الذهبية'\s*\}/{ name: 'Golden Signal', ar: 'الإشارة الذهبية' }/g;
    " "$f"
    echo "$f" >> "$CHANGED"
  fi
done

echo "Do not change internal stable constants automatically."
echo "Internal constants such as NAWAF_GOLDEN_SIGNAL are documented if still present."

echo "Final scan: visible active files only, excluding internal usernames and stable paths..."

SCAN_FILES="$REPORT_DIR/scanned-files.txt"

find \
  ./apps \
  ./frontend \
  ./ndsp-platform/frontend \
  ./backend/auth_api \
  ./backend/services \
  -type d \( \
    -name node_modules -o \
    -name runtime -o \
    -name quarantine -o \
    -name dist -o \
    -name build -o \
    -name .next -o \
    -name coverage -o \
    -name vendor -o \
    -name backups -o \
    -name backup -o \
    -name _backups -o \
    -name archive -o \
    -name archives \
  \) -prune -o \
  -type f \( \
    -name "*.tsx" -o -name "*.ts" -o -name "*.jsx" -o -name "*.js" -o \
    -name "*.mjs" -o -name "*.cjs" -o -name "*.html" -o -name "*.css" -o \
    -name "*.scss" -o -name "*.sass" -o -name "*.json" -o -name "*.jsonld" -o \
    -name "*.md" -o -name "*.mdx" -o -name "*.svg" -o -name "*.yml" -o \
    -name "*.yaml" -o -name "*.xml" \
  \) \
  -not -path "./apps/*/_next/*" \
  -not -path "./apps/*/package-lock.json" \
  -print 2>/dev/null \
| sort > "$SCAN_FILES"

while read -r f; do
  grep -InE "نواف|Nawaf|NAWAF|nawaf" "$f" || true
done < "$SCAN_FILES" \
| grep -v "/home/nawaf511/" \
| grep -v "loadEnvFile" \
| grep -v "loadEnv(" \
| grep -v "NAWAF_GOLDEN_SIGNAL" \
> "$REPORT_DIR/remaining-visible-name-hits.txt" || true

while read -r f; do
  grep -InE "إشارة شراء|إشارة بيع|ادخل الآن|نفّذ الصفقة|نفذ الصفقة|ربح مضمون|دقة مضمونة|buy signal|sell signal|execute trade|guaranteed profit|guaranteed accuracy" "$f" || true
done < "$SCAN_FILES" \
| grep -vi "does not execute" \
| grep -vi "لا تنفذ" \
| grep -vi "لا تنفّذ" \
| grep -vi "not execute" \
> "$REPORT_DIR/remaining-forbidden-claims.txt" || true

while read -r f; do
  grep -InE "EXPANDED|Shadow Testing|shadow testing|الطبقات الداخلية الست|internal 16|16 internal layer|OWNER_INTERNAL_16" "$f" || true
done < "$SCAN_FILES" \
> "$REPORT_DIR/internal-exposure-candidates.txt" || true

echo "Running build checks where package scripts exist..."

run_build() {
  local dir="$1"
  local label
  label="$(echo "$dir" | tr '/.' '__')"

  if [ ! -f "$dir/package.json" ]; then
    return 0
  fi

  (
    cd "$dir"
    if node -e "const p=require('./package.json'); process.exit(p.scripts && p.scripts.build ? 0 : 1)" 2>/dev/null; then
      timeout 240s npm run build > "$REPORT_DIR/build-${label}.log" 2>&1 || true
    else
      echo "No build script" > "$REPORT_DIR/build-${label}.log"
    fi
  )
}

run_build "./apps/user-portal"
run_build "./apps/public-landing"
run_build "./apps/admin-console"
run_build "./frontend/public-site"
run_build "./frontend/user-portal-vite"
run_build "./ndsp-platform/frontend/public"
run_build "./apps/ndsp-auth-core-clean/ui"
run_build "./apps/ndsp-commercial-auth-payment-staging/ui"

echo "Collecting build status..."

for log in "$REPORT_DIR"/build-*.log; do
  [ -f "$log" ] || continue
  if grep -Eiq "error|failed|ERR!" "$log"; then
    echo "FAIL_OR_WARN: $log" >> "$REPORT_DIR/build-status.txt"
  else
    echo "OK_OR_NO_SCRIPT: $log" >> "$REPORT_DIR/build-status.txt"
  fi
done

{
  echo "NDSP Final Visible Cleanup Summary"
  echo "Timestamp: $STAMP"
  echo "Project: $PROJECT_ROOT"
  echo "Backup: $BACKUP"
  echo
  echo "Changed files:"
  sort -u "$CHANGED" || true
  echo
  echo "Remaining visible name hits:"
  if [ -s "$REPORT_DIR/remaining-visible-name-hits.txt" ]; then
    cat "$REPORT_DIR/remaining-visible-name-hits.txt"
  else
    echo "None"
  fi
  echo
  echo "Remaining forbidden claims:"
  if [ -s "$REPORT_DIR/remaining-forbidden-claims.txt" ]; then
    cat "$REPORT_DIR/remaining-forbidden-claims.txt"
  else
    echo "None"
  fi
  echo
  echo "Internal exposure candidates:"
  if [ -s "$REPORT_DIR/internal-exposure-candidates.txt" ]; then
    head -120 "$REPORT_DIR/internal-exposure-candidates.txt"
  else
    echo "None"
  fi
  echo
  echo "Build status:"
  if [ -s "$REPORT_DIR/build-status.txt" ]; then
    cat "$REPORT_DIR/build-status.txt"
  else
    echo "No build logs generated"
  fi
  echo
  echo "Documented internal leftovers not changed automatically:"
  echo "- /home/nawaf511 paths are OS/user paths, not public brand copy."
  echo "- NAWAF_GOLDEN_SIGNAL may be a stable internal entitlement/contract identifier; not changed automatically."
} > "$REPORT_DIR/SUMMARY.txt"

echo
echo "DONE"
echo "Report: $REPORT_DIR"
echo "Backup: $BACKUP"
echo
cat "$REPORT_DIR/SUMMARY.txt"
