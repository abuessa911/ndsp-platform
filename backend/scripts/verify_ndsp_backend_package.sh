#!/bin/sh
# ==========================================================================
# NDSP Backend — verifier (READ-ONLY, makes no changes)
# Checks files, env example, API health, DB connectivity (best-effort),
# nginx, exposed secrets, unofficial paths. Writes a report.
# Usage:  sh verify_ndsp_backend.sh
# ==========================================================================
set -eu

ROOT="/home/nawaf511/empire-core-new"
BACKEND="$ROOT/backend"
REPORTS="/home/nawaf511/ndsp_launch_reports"
TS=$(date +%Y%m%d-%H%M%S)
REPORT="$REPORTS/verify_report_$TS.txt"

PASS=0; WARN=0; FAILN=0
ok()   { printf '  [OK]   %s\n' "$*";   PASS=$((PASS+1)); }
warn() { printf '  [WARN] %s\n' "$*";   WARN=$((WARN+1)); }
bad()  { printf '  [FAIL] %s\n' "$*";   FAILN=$((FAILN+1)); }

mkdir -p "$REPORTS"
{ echo "NDSP verify report"; echo "timestamp: $TS"; echo "target: $BACKEND"; echo "------------------"; } > "$REPORT"

echo "==> Files"
for f in requirements.txt .env.example app/main.py db/schema.sql; do
  if [ -f "$BACKEND/$f" ]; then ok "$f present"; else bad "$f missing"; fi
done

echo "==> Env example (no real secrets)"
if [ -f "$BACKEND/.env.example" ]; then
  if grep -qE '^(JWT_SECRET|DATABASE_URL|TWELVEDATA_API_KEY|NOWPAYMENTS_API_KEY|TELEGRAM_BOT_TOKEN)=.+' "$BACKEND/.env.example"; then
    bad ".env.example contains real-looking values"
  else
    ok ".env.example has no real secrets"
  fi
  grep -q 'CORS_ORIGINS=https://ndsp.app' "$BACKEND/.env.example" && ok "CORS restricted to official domains" || warn "CORS origins not as expected"
else
  bad ".env.example missing"
fi

echo "==> No real secrets committed (.env should not be tracked)"
if [ -f "$BACKEND/.gitignore" ] && grep -q '^\.env$' "$BACKEND/.gitignore"; then
  ok ".env is gitignored"
else
  warn ".env not found in .gitignore — ensure it is never committed"
fi

echo "==> No forbidden artifacts in package"
FOUND_ART=0
for d in node_modules .next dist build; do
  if find "$BACKEND" -name "$d" -type d 2>/dev/null | grep -q .; then warn "found $d (should be excluded)"; FOUND_ART=1; fi
done
[ "$FOUND_ART" -eq 0 ] && ok "no node_modules/.next/dist/build in package"

echo "==> No unofficial paths / reports inside project"
if find "$BACKEND" -type d -name 'ndsp_launch_reports' 2>/dev/null | grep -q .; then
  bad "reports dir found inside project — reports belong in /home/nawaf511/ndsp_launch_reports only"
else
  ok "no reports written inside project"
fi
if grep -rqs '/var/www' "$BACKEND/app" 2>/dev/null; then
  warn "/var/www referenced in code (deployment output only)"
else
  ok "no /var/www used as code source"
fi

echo "==> API health"
if command -v curl >/dev/null 2>&1; then
  if curl -fsS "http://127.0.0.1:8000/health" >/dev/null 2>&1; then ok "API /health responding"; else warn "API /health not responding (service may be stopped)"; fi
  if curl -fsS "http://127.0.0.1:8000/governance" >/dev/null 2>&1; then ok "governance endpoint responding"; fi
else
  warn "curl not available — skipped API checks"
fi

echo "==> Database connectivity (best-effort)"
if [ -f "$BACKEND/.env" ] && command -v psql >/dev/null 2>&1; then
  DBURL=$(grep -E '^DATABASE_URL=' "$BACKEND/.env" | head -n1 | cut -d= -f2-)
  PGURL=$(printf '%s' "$DBURL" | sed 's#postgresql+psycopg#postgresql#')
  if [ -n "$PGURL" ] && psql "$PGURL" -c '\q' >/dev/null 2>&1; then ok "PostgreSQL reachable"; else warn "PostgreSQL not reachable / not configured"; fi
else
  warn "psql or .env not available — skipped DB check"
fi

echo "==> nginx"
if command -v nginx >/dev/null 2>&1; then
  nginx -t >/dev/null 2>&1 && ok "nginx -t OK" || warn "nginx -t reported issues"
else
  warn "nginx not present — skipped"
fi

{
  echo "passed: $PASS"; echo "warnings: $WARN"; echo "failed: $FAILN";
} >> "$REPORT"

echo ""
echo "==> Summary: PASS=$PASS WARN=$WARN FAIL=$FAILN"
echo "    Report: $REPORT"
[ "$FAILN" -eq 0 ] || { echo "    One or more checks FAILED."; exit 1; }
