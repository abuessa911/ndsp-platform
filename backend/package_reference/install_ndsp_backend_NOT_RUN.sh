#!/bin/sh
# ==========================================================================
# NDSP Backend — installer (safe, non-destructive)
# - Never deletes anything. Backs up before any change.
# - Merges this package into the OFFICIAL backend path only.
# - Writes a report to the OFFICIAL reports dir.
# Usage:  sh install_ndsp_backend.sh
# ==========================================================================
set -eu

# ---- official paths (do not invent alternatives) ----
ROOT="/home/nawaf511/empire-core-new"
BACKEND="$ROOT/backend"
REPORTS="/home/nawaf511/ndsp_launch_reports"
BACKUPS="/home/nawaf511/ndsp_backups"
SNAPSHOTS="/home/nawaf511/ndsp_snapshots"

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SRC="$SCRIPT_DIR/backend"
TS=$(date +%Y%m%d-%H%M%S)
REPORT="$REPORTS/install_report_$TS.txt"

log() { printf '%s\n' "$*"; }
fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }

# ---- 1) preflight checks ----
log "==> [1/9] Preflight checks"
[ -d "$SRC" ] || fail "source backend/ not found next to this script"
[ -f "$SRC/requirements.txt" ] || fail "requirements.txt missing in package"
[ -f "$SRC/.env.example" ] || fail ".env.example missing in package"
command -v python3 >/dev/null 2>&1 || fail "python3 not found"

# Refuse to source code from deployment-only dir
case "$SRC" in
  /var/www/*) fail "/var/www is deployment output only, not a code source" ;;
esac

mkdir -p "$REPORTS" "$BACKUPS" "$SNAPSHOTS" "$ROOT"
[ -d "$BACKEND" ] || { log "    backend/ does not exist yet — will create $BACKEND"; mkdir -p "$BACKEND"; }

{
  echo "NDSP backend install report"
  echo "timestamp: $TS"
  echo "source: $SRC"
  echo "target: $BACKEND"
  echo "----------------------------------------"
} > "$REPORT"

# ---- 2) backup BEFORE any change ----
log "==> [2/9] Backup current backend"
if [ -n "$(ls -A "$BACKEND" 2>/dev/null || true)" ]; then
  BK="$BACKUPS/backend_backup_$TS.tar.gz"
  tar -czf "$BK" -C "$BACKEND" . 2>/dev/null || fail "backup failed"
  log "    backup created: $BK"
  echo "backup: $BK" >> "$REPORT"
else
  log "    backend is empty — nothing to back up"
  echo "backup: none (empty backend)" >> "$REPORT"
fi

# ---- 3) merge/copy (no deletes) ----
log "==> [3/9] Copy/merge package into backend (no deletes)"
if command -v rsync >/dev/null 2>&1; then
  rsync -a \
    --exclude 'node_modules' --exclude '.next' --exclude 'dist' \
    --exclude 'build' --exclude '__pycache__' --exclude '.env' \
    "$SRC"/ "$BACKEND"/
else
  ( cd "$SRC" && tar -cf - \
      --exclude node_modules --exclude .next --exclude dist \
      --exclude build --exclude __pycache__ --exclude .env . ) | ( cd "$BACKEND" && tar -xf - )
fi
echo "merge: done" >> "$REPORT"

# ---- 4) ensure .env exists (never overwrite a real one) ----
log "==> [4/9] Ensure .env present"
if [ ! -f "$BACKEND/.env" ]; then
  cp "$BACKEND/.env.example" "$BACKEND/.env"
  log "    created $BACKEND/.env from example — FILL REAL VALUES before going live"
  echo "env: created from example (needs real values)" >> "$REPORT"
else
  log "    existing .env kept untouched"
  echo "env: existing kept" >> "$REPORT"
fi

# ---- 5) python venv + dependencies ----
log "==> [5/9] Install Python dependencies (venv)"
cd "$BACKEND"
if [ ! -d ".venv" ]; then python3 -m venv .venv; fi
# shellcheck disable=SC1091
. .venv/bin/activate
python -m pip install --upgrade pip >/dev/null
python -m pip install -r requirements.txt
echo "deps: installed" >> "$REPORT"

# ---- 6) prepare migrations (does not require live DB to be reachable) ----
log "==> [6/9] Prepare database migrations"
if command -v alembic >/dev/null 2>&1; then
  if [ -z "$(ls -A migrations/versions 2>/dev/null || true)" ]; then
    alembic revision --autogenerate -m "initial schema" || \
      log "    autogenerate skipped (DB not reachable) — apply db/schema.sql manually"
  fi
  alembic upgrade head || log "    'alembic upgrade head' deferred — run after DB is reachable"
else
  log "    alembic not on PATH — use: python -m alembic ... or apply db/schema.sql"
fi
echo "migrations: prepared (apply when DB reachable)" >> "$REPORT"

# ---- 7) nginx config test (only if nginx present) ----
log "==> [7/9] nginx test"
if command -v nginx >/dev/null 2>&1; then
  if nginx -t >/dev/null 2>&1; then
    log "    nginx -t OK"; echo "nginx: ok" >> "$REPORT"
  else
    log "    nginx -t reported issues — review api.ndsp.app server block"
    echo "nginx: check-needed" >> "$REPORT"
  fi
else
  log "    nginx not found — skipping"; echo "nginx: not present" >> "$REPORT"
fi

# ---- 8) (re)start service if a unit exists ----
log "==> [8/9] Service restart (if configured)"
if command -v systemctl >/dev/null 2>&1 && systemctl list-unit-files 2>/dev/null | grep -q '^ndsp-api'; then
  systemctl restart ndsp-api && log "    ndsp-api restarted" && echo "service: restarted" >> "$REPORT"
else
  log "    ndsp-api service not found — start manually (see BACKEND_GUIDE.md)"
  echo "service: manual start required" >> "$REPORT"
fi

# ---- 9) health checks + final assertions ----
log "==> [9/9] Health checks"
HEALTH_URL="http://127.0.0.1:8000/health"
if command -v curl >/dev/null 2>&1; then
  if curl -fsS "$HEALTH_URL" >/dev/null 2>&1; then
    log "    health OK ($HEALTH_URL)"; echo "health: ok" >> "$REPORT"
  else
    log "    health not responding yet — start the service, then re-check"
    echo "health: pending" >> "$REPORT"
  fi
fi

# final assertions: secrets must not be committed
if grep -rqE '^(JWT_SECRET|DATABASE_URL|TWELVEDATA_API_KEY|NOWPAYMENTS_API_KEY|TELEGRAM_BOT_TOKEN)=.+' "$BACKEND/.env.example" 2>/dev/null; then
  fail "SECURITY: .env.example appears to contain real values — aborting"
fi
echo "assertions: passed" >> "$REPORT"

log ""
log "==> DONE. Report: $REPORT"
log "    Next: fill $BACKEND/.env, run bootstrap to create admin, start ndsp-api."
