set -Eeuo pipefail

PROJECT_ROOT="/home/nawaf511/empire-core-v5-1-1-clean"
cd "$PROJECT_ROOT"

REPORT_DIR="./ndsp-source-only-scan-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$REPORT_DIR"

echo "Project: $PROJECT_ROOT"
echo "Report: $REPORT_DIR"

echo "Detecting app source roots..."

find \
  ./apps \
  ./frontend \
  ./ndsp-platform \
  ./backend \
  -maxdepth 5 \
  -type f \( \
    -name "package.json" -o \
    -name "vite.config.*" -o \
    -name "next.config.*" \
  \) \
  -not -path "*/node_modules/*" \
  -not -path "*/runtime/*" \
  -not -path "*/quarantine/*" \
  -not -path "*/backup*" \
  -not -path "*/backups/*" \
  -not -path "*/archive*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -path "*/.next/*" \
  2>/dev/null \
  | sort > "$REPORT_DIR/source-roots-candidates.txt"

echo "Scanning visible source only..."

find \
  ./apps \
  ./frontend \
  ./ndsp-platform \
  ./backend \
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
    -name archive -o \
    -name archives \
  \) -prune -o \
  -type f \( \
    -name "*.tsx" -o -name "*.ts" -o -name "*.jsx" -o -name "*.js" -o \
    -name "*.mjs" -o -name "*.cjs" -o -name "*.vue" -o -name "*.svelte" -o \
    -name "*.html" -o -name "*.css" -o -name "*.scss" -o -name "*.sass" -o \
    -name "*.json" -o -name "*.jsonld" -o -name "*.md" -o -name "*.mdx" -o \
    -name "*.svg" -o -name "*.yml" -o -name "*.yaml" -o -name "*.xml" \
  \) \
  -not -path "*/node_modules/*" \
  -not -path "*/runtime/*" \
  -not -path "*/quarantine/*" \
  -not -path "*/backup*" \
  -not -path "*/backups/*" \
  -not -path "*/archive*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -path "*/.next/*" \
  -print0 2>/dev/null \
| xargs -0 grep -InE "نواف|Nawaf|NAWAF|nawaf|منصة نواف لدعم القرار|Nawaf Decision Support Platform|Nawaf Golden Signal|Enhanced Nawaf Golden Signal|Nawaf Enhanced Golden Signal" \
> "$REPORT_DIR/name-hits-source-only.txt" || true

cut -d: -f1 "$REPORT_DIR/name-hits-source-only.txt" \
  | sort \
  | uniq -c \
  | sort -nr \
  > "$REPORT_DIR/top-hit-files.txt"

echo
echo "Source roots:"
cat "$REPORT_DIR/source-roots-candidates.txt"

echo
echo "Top hit files:"
head -80 "$REPORT_DIR/top-hit-files.txt"

echo
echo "Total hits:"
wc -l "$REPORT_DIR/name-hits-source-only.txt"

echo
echo "Affected files:"
cut -d: -f1 "$REPORT_DIR/name-hits-source-only.txt" | sort -u | wc -l

echo
echo "DONE"
echo "$REPORT_DIR"
