#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKEND="$ROOT/backend"
TS="$(date +%Y%m%d_%H%M%S)"
REPORT="${1:-$ROOT/backend/architecture/reports/DEV-003-PROJECT-VALIDATOR-RUN-$TS.md}"

# Normalize relative report path to absolute path from repo root
case "$REPORT" in
  /*) ;;
  *) REPORT="$ROOT/$REPORT" ;;
esac

mkdir -p "$(dirname "$REPORT")"

log(){ echo "$*" | tee -a "$REPORT"; }

FAIL=0
WARN=0

cd "$ROOT"

log "# DEV-003 — NDSP Project Validator"
log "Generated=$TS"
log "ROOT=$ROOT"
log "HEAD=$(git log --oneline -1)"
log "BRANCH=$(git branch --show-current)"

log "== 1) GIT STATUS =="
git status --short | tee -a "$REPORT" || true

log "== 2) REAL ENV TRACKING CHECK =="

REAL_ENV_TRACKED="$(
  git ls-files | grep -E '(^|/)\.env$' || true
)"

if [ -n "$REAL_ENV_TRACKED" ]; then
  log "REAL_ENV_TRACKED=FAIL"
  echo "$REAL_ENV_TRACKED" | tee -a "$REPORT"
  FAIL=1
else
  log "REAL_ENV_TRACKED=PASS"
fi

REAL_ENV_HISTORY="$(
  git log --all --name-only --pretty=format: | sort -u | grep -E '(^|/)\.env$' || true
)"

if [ -n "$REAL_ENV_HISTORY" ]; then
  log "REAL_ENV_HISTORY=FAIL"
  echo "$REAL_ENV_HISTORY" | tee -a "$REPORT"
  FAIL=1
else
  log "REAL_ENV_HISTORY=PASS"
fi

log "== 3) LITERAL SECRET SCAN HEAD =="

# Exclude this validator file because it necessarily contains the regex patterns used to detect secrets.
SECRET_HITS="$(
  git grep -nE \
    '[0-9]{8,10}:[A-Za-z0-9_-]{30,}|ghp_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|BEGIN RSA|BEGIN OPENSSH|PRIVATE KEY' \
    HEAD -- . ':!backend/tools/ndsp_project_validator.sh' || true
)"

if [ -n "$SECRET_HITS" ]; then
  log "LITERAL_SECRET_SCAN=FAIL"
  echo "$SECRET_HITS" | tee -a "$REPORT"
  FAIL=1
else
  log "LITERAL_SECRET_SCAN=PASS"
fi

log "== 4) GENERATED ARTIFACTS TRACKING CHECK =="

GENERATED_TRACKED="$(
  git ls-files \
  | grep -E '(^|/)node_modules/|(^|/)dist/|(^|/)build/|(^|/)out/|(^|/)\.next/|(^|/)_next/|(^|/)__pycache__/|\.pyc$|\.log$' || true
)"

if [ -n "$GENERATED_TRACKED" ]; then
  log "GENERATED_ARTIFACTS_TRACKED=FAIL"
  echo "$GENERATED_TRACKED" | tee -a "$REPORT"
  FAIL=1
else
  log "GENERATED_ARTIFACTS_TRACKED=PASS"
fi

log "== 5) REQUIRED ARCHITECTURE FILES CHECK =="

REQUIRED_PATHS=(
  "backend/framework"
  "backend/services"
  "backend/tools/ndsp"
  "backend/architecture"
  "frontend/user-portal-vite"
)

for p in "${REQUIRED_PATHS[@]}"; do
  if [ -e "$ROOT/$p" ]; then
    log "REQUIRED_PATH_PASS=$p"
  else
    log "REQUIRED_PATH_FAIL=$p"
    FAIL=1
  fi
done

SERVICE_REGISTRY_CANDIDATES=(
  "backend/service-registry.json"
  "backend/service_registry.json"
  "backend/architecture/service-registry.json"
  "backend/architecture/service_registry.json"
  "backend/services/service-registry.json"
  "backend/services/service_registry.json"
)

SERVICE_REGISTRY_FOUND=""

for candidate in "${SERVICE_REGISTRY_CANDIDATES[@]}"; do
  if [ -f "$ROOT/$candidate" ]; then
    SERVICE_REGISTRY_FOUND="$candidate"
    break
  fi
done

if [ -n "$SERVICE_REGISTRY_FOUND" ]; then
  log "SERVICE_REGISTRY_PATH_PASS=$SERVICE_REGISTRY_FOUND"
else
  log "SERVICE_REGISTRY_PATH_WARN=NOT_FOUND_DIRECTLY"
  log "SERVICE_REGISTRY_AUTHORITY=NDSP_DOCTOR"
  WARN=1
fi

log "== 6) NDSP TOOLKIT CHECK =="

cd "$BACKEND"

if ./tools/ndsp doctor | tee -a "$REPORT"; then
  log "NDSP_DOCTOR=PASS"
else
  log "NDSP_DOCTOR=FAIL"
  FAIL=1
fi

if ./tools/ndsp validate all | tee -a "$REPORT"; then
  log "NDSP_VALIDATE_ALL=PASS"
else
  log "NDSP_VALIDATE_ALL=FAIL"
  FAIL=1
fi

cd "$ROOT"

log "== 7) FRONTEND BUILD CHECK =="

FRONTEND="$ROOT/frontend/user-portal-vite"

if [ -f "$FRONTEND/package.json" ]; then
  cd "$FRONTEND"
  if command -v npm >/dev/null 2>&1; then
    if npm run build >>"$REPORT" 2>&1; then
      log "FRONTEND_BUILD=PASS"
    else
      log "FRONTEND_BUILD=WARN_FAILED"
      WARN=1
    fi
  else
    log "FRONTEND_BUILD=WARN_NPM_NOT_FOUND"
    WARN=1
  fi
  cd "$ROOT"
else
  log "FRONTEND_BUILD=WARN_PACKAGE_JSON_NOT_FOUND"
  WARN=1
fi

log "== 8) IGNORED LOCAL ARTIFACTS =="

git status --short --ignored \
  backend/runtime runtime ndsp_checkout_plans_package run_local_ndsp.py 2>/dev/null \
  | tee -a "$REPORT" || true

log "== 9) SUMMARY =="

log "FAIL_COUNT=$FAIL"
log "WARN_COUNT=$WARN"

if [ "$FAIL" -ne 0 ]; then
  log "FINAL_STATUS=FAIL"
  exit 1
fi

if [ "$WARN" -ne 0 ]; then
  log "FINAL_STATUS=OK_WITH_WARNINGS"
  exit 0
fi

log "FINAL_STATUS=OK"
