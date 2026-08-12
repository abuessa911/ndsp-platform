set -Eeuo pipefail

PROJECT_ROOT="/home/nawaf511/empire-core-new"
cd "$PROJECT_ROOT"

STAMP="$(date +%Y%m%d_%H%M%S)"
REPORT_DIR="$PROJECT_ROOT/ndsp-live-verify-$STAMP"
mkdir -p "$REPORT_DIR"

echo "NDSP live verification after cleanup"
echo "Project: $PROJECT_ROOT"
echo "Report: $REPORT_DIR"

echo "1) Source verification..."

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
| sort > "$REPORT_DIR/source-files.txt"

while read -r f; do
  grep -InE "نواف|Nawaf|NAWAF|nawaf" "$f" || true
done < "$REPORT_DIR/source-files.txt" \
| grep -v "/home/nawaf511/" \
| grep -v "loadEnvFile" \
| grep -v "loadEnv(" \
| grep -v "NAWAF_GOLDEN_SIGNAL" \
| grep -v "nawaf_golden_signal" \
| grep -v "nawaf_enhanced_golden_signal" \
> "$REPORT_DIR/source-public-name-hits.txt" || true

while read -r f; do
  grep -InE "إشارة شراء|إشارة بيع|ادخل الآن|نفّذ الصفقة|نفذ الصفقة|ربح مضمون|دقة مضمونة|buy signal|sell signal|execute trade|guaranteed profit|guaranteed accuracy" "$f" || true
done < "$REPORT_DIR/source-files.txt" \
| grep -vi "does not execute" \
| grep -vi "لا تنفذ" \
| grep -vi "لا تنفّذ" \
| grep -vi "not execute" \
> "$REPORT_DIR/source-forbidden-claims.txt" || true

echo "2) Build checks..."

run_build() {
  local dir="$1"
  local label
  label="$(echo "$dir" | tr '/.' '__')"

  [ -f "$dir/package.json" ] || return 0

  (
    cd "$dir"
    if node -e "const p=require('./package.json'); process.exit(p.scripts && p.scripts.build ? 0 : 1)" 2>/dev/null; then
      timeout 300s npm run build > "$REPORT_DIR/build-${label}.log" 2>&1 || true
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

for log in "$REPORT_DIR"/build-*.log; do
  [ -f "$log" ] || continue
  if grep -Eiq "error|failed|ERR!" "$log"; then
    echo "FAIL_OR_WARN: $log" >> "$REPORT_DIR/build-status.txt"
  else
    echo "OK_OR_NO_SCRIPT: $log" >> "$REPORT_DIR/build-status.txt"
  fi
done

echo "3) Live HTTP verification..."

URLS=(
  "https://ndsp.app"
  "https://ndsp.app/"
  "https://my.ndsp.app"
  "https://my.ndsp.app/login"
  "https://my.ndsp.app/register"
  "https://my.ndsp.app/subscription"
)

: > "$REPORT_DIR/live-status.txt"
: > "$REPORT_DIR/live-public-name-hits.txt"
: > "$REPORT_DIR/live-forbidden-claims.txt"

for url in "${URLS[@]}"; do
  safe="$(echo "$url" | sed 's#https\?://##; s#[^A-Za-z0-9._-]#_#g')"
  html="$REPORT_DIR/live-${safe}.html"

  code="$(curl -k -L --connect-timeout 10 --max-time 30 -A "NDSP-live-verify/1.0" -o "$html" -w "%{http_code}" "$url" || true)"
  echo "$url => $code" >> "$REPORT_DIR/live-status.txt"

  grep -InE "نواف|Nawaf|NAWAF|nawaf" "$html" \
    | grep -v "/home/nawaf511/" \
    | grep -v "NAWAF_GOLDEN_SIGNAL" \
    | grep -v "nawaf_golden_signal" \
    | grep -v "nawaf_enhanced_golden_signal" \
    >> "$REPORT_DIR/live-public-name-hits.txt" || true

  grep -InE "إشارة شراء|إشارة بيع|ادخل الآن|نفّذ الصفقة|نفذ الصفقة|ربح مضمون|دقة مضمونة|buy signal|sell signal|execute trade|guaranteed profit|guaranteed accuracy" "$html" \
    | grep -vi "does not execute" \
    | grep -vi "لا تنفذ" \
    | grep -vi "لا تنفّذ" \
    | grep -vi "not execute" \
    >> "$REPORT_DIR/live-forbidden-claims.txt" || true
done

{
  echo "NDSP Live Verify Summary"
  echo "Timestamp: $STAMP"
  echo "Project: $PROJECT_ROOT"
  echo
  echo "Source public name hits:"
  if [ -s "$REPORT_DIR/source-public-name-hits.txt" ]; then
    cat "$REPORT_DIR/source-public-name-hits.txt"
  else
    echo "None"
  fi
  echo
  echo "Source forbidden claims:"
  if [ -s "$REPORT_DIR/source-forbidden-claims.txt" ]; then
    cat "$REPORT_DIR/source-forbidden-claims.txt"
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
  echo "Live HTTP status:"
  cat "$REPORT_DIR/live-status.txt"
  echo
  echo "Live public name hits:"
  if [ -s "$REPORT_DIR/live-public-name-hits.txt" ]; then
    cat "$REPORT_DIR/live-public-name-hits.txt"
  else
    echo "None"
  fi
  echo
  echo "Live forbidden claims:"
  if [ -s "$REPORT_DIR/live-forbidden-claims.txt" ]; then
    cat "$REPORT_DIR/live-forbidden-claims.txt"
  else
    echo "None"
  fi
  echo
  echo "Note:"
  echo "If source is clean but live pages still show old text, the issue is deployment output, service cache, CDN/browser cache, or old Nginx root."
} > "$REPORT_DIR/SUMMARY.txt"

echo
echo "DONE"
echo "Report: $REPORT_DIR"
cat "$REPORT_DIR/SUMMARY.txt"
