set -Eeuo pipefail

PROJECT_ROOT="/home/nawaf511/empire-core-new"
cd "$PROJECT_ROOT"

STAMP="$(date +%Y%m%d_%H%M%S)"
REPORT_DIR="$PROJECT_ROOT/ndsp-zero-public-name-final-$STAMP"
BACKUP="/home/nawaf511/ndsp-zero-public-name-final-backup-$STAMP.tar.gz"

mkdir -p "$REPORT_DIR"

echo "NDSP zero public name final cleanup"
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
    s/Nawaf Gold/Golden Signal/g;
    s/Nawaf Golden Alignment/Golden Signal/g;
    s/Nawaf Golden Signal/Golden Signal/g;
    s/Nawaf Meeting Point/NMP/g;
    s/Nawaf Meet Point/NMP/g;

    s/จุดนัดพบ Nawaf/NMP/g;

    s/نقطة التقاء نواف/NMP/g;
    s/طة التقاء نواف/NMP/g;
    s/تقاء نواف/NMP/g;
    s/اء نواف/NMP/g;
    s/إشارة نواف الذهبي/الإشارة الذهبية/g;
    s/إشارة نواف الذهبية/الإشارة الذهبية/g;
    s/التوافق الذهبي لنواف/الإشارة الذهبية/g;

    s/"name":\s*"Nawaf"/"name": "NDSP"/g;
    s/"email":\s*"nawaf\.barrak\.911\@gmail\.com"/"email": ""/g;
    s/<b style="color:var\(--txt\)">Nawaf<\/b>/<b style="color:var(--txt)">NDSP<\/b>/g;
    s/>Nawaf</>NDSP</g;

    s/منصة نواف/منصة دعم القرار/g;
    s/<b>نواف<\/b>/<b>NDSP<\/b>/g;
  ' "$f"

  after="$(sha256sum "$f" | awk '{print $1}')"
  if [ "$before" != "$after" ]; then
    echo "$f" >> "$CHANGED"
  fi
}

echo "Patching exact remaining files..."

patch_file "./apps/admin-console/data/owner-layer-source-map.json"
patch_file "./apps/admin-console/index.html"
patch_file "./apps/admin-console/NDSP_Admin_Console.html"
patch_file "./apps/admin-console/NDSP_Help_Center.html"
patch_file "./apps/admin-console/NDSP_Terms_Privacy.html"
patch_file "./frontend/public-site/src/i18n/locales/th.ts"
patch_file "./frontend/user-portal-vite/public/assets/ndsp-governance-44-v26.js"
patch_file "./frontend/user-portal-vite/public/market-suite/index.html"
patch_file "./frontend/user-portal-vite/src/components/PortalPageRouterV1.jsx"
patch_file "./frontend/user-portal-vite/src/main.jsx"
patch_file "./ndsp-platform/frontend/public/src/components/ndsp/hero-section.tsx"

echo "Final public scan..."

SCAN="$REPORT_DIR/scanned-files.txt"

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
  -not -path "*/package-lock.json" \
  -print 2>/dev/null \
| sort > "$SCAN"

while read -r f; do
  grep -InE "نواف|Nawaf|NAWAF|nawaf" "$f" || true
done < "$SCAN" \
| grep -v "/home/nawaf511/" \
| grep -v "loadEnvFile" \
| grep -v "loadEnv(" \
| grep -v "NAWAF_GOLDEN_SIGNAL" \
| grep -v "nawaf_golden_signal" \
| grep -v "nawaf_enhanced_golden_signal" \
> "$REPORT_DIR/remaining-public-name-hits.txt" || true

while read -r f; do
  grep -InE "إشارة شراء|إشارة بيع|ادخل الآن|نفّذ الصفقة|نفذ الصفقة|ربح مضمون|دقة مضمونة|buy signal|sell signal|execute trade|guaranteed profit|guaranteed accuracy" "$f" || true
done < "$SCAN" \
| grep -vi "does not execute" \
| grep -vi "لا تنفذ" \
| grep -vi "لا تنفّذ" \
| grep -vi "not execute" \
> "$REPORT_DIR/remaining-forbidden-claims.txt" || true

{
  echo "NDSP Zero Public Name Final Summary"
  echo "Timestamp: $STAMP"
  echo "Project: $PROJECT_ROOT"
  echo "Backup: $BACKUP"
  echo
  echo "Changed files:"
  sort -u "$CHANGED" || true
  echo
  echo "Remaining public name hits:"
  if [ -s "$REPORT_DIR/remaining-public-name-hits.txt" ]; then
    cat "$REPORT_DIR/remaining-public-name-hits.txt"
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
  echo "Not changed automatically:"
  echo "- /home/nawaf511 OS paths."
  echo "- Internal canonical identifiers: nawaf_golden_signal, nawaf_enhanced_golden_signal, NAWAF_GOLDEN_SIGNAL if used as contracts."
} > "$REPORT_DIR/SUMMARY.txt"

echo
echo "DONE"
echo "Report: $REPORT_DIR"
cat "$REPORT_DIR/SUMMARY.txt"
