set -Eeuo pipefail

PROJECT_ROOT="/home/nawaf511/empire-core-new"
cd "$PROJECT_ROOT"

STAMP="$(date +%Y%m%d_%H%M%S)"
REPORT_DIR="$PROJECT_ROOT/ndsp-final-public-copy-clean-$STAMP"
BACKUP="/home/nawaf511/ndsp-final-public-copy-clean-backup-$STAMP.tar.gz"

mkdir -p "$REPORT_DIR"

echo "NDSP final public copy cleanup"
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

patch_text_file() {
  local f="$1"
  [ -f "$f" ] || return 0

  local before after
  before="$(sha256sum "$f" | awk '{print $1}')"

  perl -0pi -e '
    s/منصة نواف لدعم القرار/منصة دعم القرار/g;
    s/منصة نواف/منصة دعم القرار/g;
    s/<b>نواف<\/b>/<b>NDSP<\/b>/g;

    s/نقطة التقاء نواف NMP/NMP/g;
    s/نقطة التقاء نواف/NMP/g;
    s/التوافق الذهبي لنواف/الإشارة الذهبية/g;
    s/إشارة نواف الذهبية المعززة/الإشارة الذهبية المعززة/g;
    s/إشارة نواف الذهبية/الإشارة الذهبية/g;
    s/إشارة نواف الذهبي/الإشارة الذهبية/g;

    s/Nawaf Decision Support Platform/Decision Support Platform/g;
    s/Nawaf Meeting Point \(NMP\)/NMP/g;
    s/Nawaf Meeting Point/NMP/g;
    s/Nawaf Meet Point/NMP/g;
    s/Nawaf Golden Alignment/Golden Signal/g;
    s/Nawaf Golden Signal/Golden Signal/g;
    s/Enhanced Nawaf Golden Signal/Enhanced Golden Signal/g;
    s/Nawaf Enhanced Golden Signal/Enhanced Golden Signal/g;

    s/Timed Direction Logic · Nawaf Meeting Point · Devil'\''s Advocate · Nawaf Golden Alignment/TDL · NMP · Devil'\''s Advocate · Golden Signal/g;
    s/منطق البُعد الزمني · نقطة التقاء نواف · محامي الشيطان · الإشارة الذهبية/TDL · NMP · محامي الشيطان · الإشارة الذهبية/g;

    s/Meeting point — Nawaf[^",\]\n]*/Meeting point — NMP/g;
    s/Nawaf-Treffpunkt/NMP/g;
    s/Nawafův setkávací bod/NMP/g;
    s/Punto de Encuentro Nawaf/NMP/g;
    s/Point de rencontre Nawaf/NMP/g;
    s/Nawaf találkozópontja/NMP/g;
    s/Titik Pertemuan Nawaf/NMP/g;
    s/Punto di incontro Nawaf/NMP/g;
    s/Nawaf 만남 지점/NMP/g;
    s/Nawaf-ontmoetingspunt/NMP/g;
    s/Punkt spotkania Nawaf/NMP/g;
    s/Ponto de Encontro Nawaf/NMP/g;
    s/Punctul de întâlnire Nawaf/NMP/g;
    s/Nawaf mötespunkt/NMP/g;
    s/Nukta ya Mkutano wa Nawaf/NMP/g;
    s/Nawaf Buluşma Noktası/NMP/g;
    s/نواف ملاقات کا نقطہ/NMP/g;
    s/Điểm Gặp Gỡ Nawaf/NMP/g;
    s/Nawaf会合点/NMP/g;
    s/نقطه ملاقات نواف/NMP/g;
    s/نقطة ملاقات نواف/NMP/g;
    s/Σημείο συνάντησης Nawaf/NMP/g;

    s/Meeting point The golden signal/Golden Signal/g;

    s/"name":\s*"Nawaf"/"name": "NDSP"/g;
    s/"email":\s*"nawaf\.barrak\.911\@gmail\.com"/"email": ""/g;

    s/<b style="color:var\(--txt\)">Nawaf<\/b>/<b style="color:var(--txt)">NDSP<\/b>/g;
    s/>Nawaf</>NDSP</g;
  ' "$f"

  after="$(sha256sum "$f" | awk '{print $1}')"
  if [ "$before" != "$after" ]; then
    echo "$f" >> "$CHANGED"
  fi
}

echo "Patching visible UI, translations, public data, and admin static pages..."

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
  -print0 2>/dev/null \
| while IFS= read -r -d '' f; do
    patch_text_file "$f"
  done

echo "Final scan..."

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

echo "Build checks..."

run_build() {
  local dir="$1"
  local label
  label="$(echo "$dir" | tr '/.' '__')"

  [ -f "$dir/package.json" ] || return 0

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

for log in "$REPORT_DIR"/build-*.log; do
  [ -f "$log" ] || continue
  if grep -Eiq "error|failed|ERR!" "$log"; then
    echo "FAIL_OR_WARN: $log" >> "$REPORT_DIR/build-status.txt"
  else
    echo "OK_OR_NO_SCRIPT: $log" >> "$REPORT_DIR/build-status.txt"
  fi
done

{
  echo "NDSP Final Public Copy Clean Summary"
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
  echo "Build status:"
  if [ -s "$REPORT_DIR/build-status.txt" ]; then
    cat "$REPORT_DIR/build-status.txt"
  else
    echo "No build logs generated"
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
