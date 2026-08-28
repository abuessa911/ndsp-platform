#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
export LC_ALL=C

ROOT="${1:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
FE="$ROOT/frontend/ndsp-sovereign-meridian-ui"
BRIDGE="$ROOT/apps/ndsp-ui-bridge-api/main.py"
AUTH_CORE="$ROOT/apps/ndsp-auth-core-clean/server/src/server.ts"
TMP="$(mktemp -d /tmp/ndsp-m2-cert.XXXXXX)"
trap 'rm -rf "$TMP"' EXIT

FAIL=0
BLOCK=0

section(){ printf '\n============================================================\n%s\n============================================================\n' "$1"; }
pass(){ printf 'PASS|%s\n' "$1"; }
fail(){ printf 'FAIL|%s\n' "$1"; FAIL=1; }
block(){ printf 'BLOCKED|%s\n' "$1"; BLOCK=1; }
require_file(){ [[ -f "$1" ]] && pass "FILE:$1" || fail "FILE_MISSING:$1"; }
require_grep(){ local p="$1" f="$2" n="$3"; grep -Eq "$p" "$f" && pass "$n" || fail "$n"; }
forbid_grep(){ local p="$1" f="$2" n="$3"; if grep -Eq "$p" "$f"; then fail "$n"; else pass "$n"; fi; }

section "NDSP M2 — FINAL READ-ONLY CERTIFIER"
printf 'MODE=SOURCE_AND_PRODUCTION_READ_ONLY\nROOT=%s\nUTC=%s\n' "$ROOT" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

section "1/7 — SOURCE IDENTITY"
[[ -d "$ROOT/.git" ]] && pass GIT_ROOT || fail NOT_GIT_ROOT
require_file "$FE/package.json"
require_file "$FE/package-lock.json"
require_file "$FE/src/analysis/AnalysisContext.tsx"
require_file "$FE/src/pages/AnalysisSetupPage.tsx"
require_file "$FE/src/pages/AnalysisPage.tsx"
require_file "$FE/src/api/decision.ts"
require_file "$FE/src/auth/RequireUser.tsx"
require_file "$BRIDGE"
require_file "$AUTH_CORE"

section "2/7 — GOVERNED JOURNEY INVARIANTS"
require_grep 'path="analysis/setup"' "$FE/src/App.tsx" ANALYSIS_SETUP_ROUTE
require_grep 'RequireUser' "$FE/src/App.tsx" ANALYSIS_ROUTES_AUTH_GUARDED
require_grep 'AnalysisProvider' "$FE/src/main.tsx" ANALYSIS_PROVIDER_INSTALLED
require_grep 'analysisContext\.clearContext\(\)' "$FE/src/pages/AnalysisSetupPage.tsx" SETUP_INVALIDATES_PRIOR_CONTEXT
require_grep 'market.*symbol.*timeframe.*analysisMode.*presentationMode|market:.*symbol:.*timeframe:.*analysisMode:.*presentationMode:' "$FE/src/api/decision.ts" CONTEXT_QUERY_FIELDS_PRESENT
forbid_grep 'from "\.\./data"|from '\''\.\./data'\''' "$FE/src/pages/AnalysisPage.tsx" LOCAL_ANALYSES_NOT_DECISION_AUTHORITY
require_grep 'GLOBAL_CAPABILITY_MAPPING_RECONCILED = false' "$FE/src/pages/AnalysisPage.tsx" GLOBAL_REGISTRY_FAIL_CLOSED_MARKER

section "3/7 — CAPABILITY / SECRET GOVERNANCE"
for state in CONTRIBUTED BLOCKED NOT_APPLICABLE UNAVAILABLE STALE PARTIAL GOVERNANCE_PROTECTED; do
  require_grep "${state}" "$FE/src/analysis/types.ts" "CAPABILITY_STATE_${state}"
done
require_grep 'silent_omission' "$BRIDGE" CURRENT_FAMILY_SILENT_OMISSION_CHECK
require_grep 'LAYER_REGISTRY' "$BRIDGE" SIXTEEN_LAYER_REGISTRY_PRESENT
require_grep 'frontend_recomputes_protected_logic' "$BRIDGE" NO_FRONTEND_PROTECTED_RECOMPUTE_CONTRACT
require_grep 'protected_formulas_exposed' "$BRIDGE" PROTECTED_FORMULA_EXPOSURE_CONTRACT

# 311 is the authoritative discovered CAP-record count from NAW-22, but it is
# not equivalent to 311 independent runtime capabilities. Final READY remains
# blocked until NAW-27 writes an evidence-backed reconciliation and flips the UI gate.
if grep -q 'GLOBAL_CAPABILITY_MAPPING_RECONCILED = false' "$FE/src/pages/AnalysisPage.tsx"; then
  block AUTHORITATIVE_311_CAPABILITY_RECONCILIATION_PENDING
else
  pass AUTHORITATIVE_311_CAPABILITY_RECONCILIATION_COMPLETE
fi

section "4/7 — SERVER-SIDE AUTH GATE"
require_grep 'app\.get\("/api/auth/session"|/api/auth/session' "$AUTH_CORE" AUTH_SESSION_PROVIDER_EXISTS
# React RequireUser is necessary but insufficient. New UI-Bridge analysis routes
# must independently validate the authenticated session server-side or be protected
# by an equivalent verified gateway/auth_request contract.
if grep -Eq 'AUTH_SESSION|auth/session|require.*session|authenticated.*session|Authorization|Cookie|cookie' "$BRIDGE"; then
  pass UI_BRIDGE_SERVER_AUTH_EVIDENCE_PRESENT
else
  block UI_BRIDGE_SERVER_AUTH_EVIDENCE_MISSING
fi

section "5/7 — PYTHON SYNTAX"
if command -v python3 >/dev/null 2>&1; then
  if PYTHONPYCACHEPREFIX="$TMP/pycache" python3 -m py_compile "$BRIDGE"; then
    pass UI_BRIDGE_PYTHON_COMPILE
  else
    fail UI_BRIDGE_PYTHON_COMPILE
  fi
else
  fail PYTHON3_NOT_AVAILABLE
fi

section "6/7 — ISOLATED FRONTEND TYPECHECK / BUILD"
if ! command -v npm >/dev/null 2>&1; then
  fail NPM_NOT_AVAILABLE
else
  mkdir -p "$TMP/frontend"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete --exclude node_modules --exclude dist "$FE/" "$TMP/frontend/"
  else
    cp -a "$FE/." "$TMP/frontend/"
    rm -rf "$TMP/frontend/node_modules" "$TMP/frontend/dist"
  fi
  (
    cd "$TMP/frontend"
    npm ci --ignore-scripts --no-audit --no-fund
    npm run typecheck
    npm run build
  ) && pass FRONTEND_TYPECHECK_AND_BUILD || fail FRONTEND_TYPECHECK_AND_BUILD
fi

section "7/7 — OPTIONAL LIVE CONTRACT PROBES"
LIVE_BASE="${NDSP_M2_LIVE_BASE:-}"
if [[ -n "$LIVE_BASE" ]]; then
  if ! command -v curl >/dev/null 2>&1; then
    fail CURL_NOT_AVAILABLE_FOR_LIVE_PROBE
  else
    code="$(curl -ksS -o "$TMP/unauth.json" -w '%{http_code}' "$LIVE_BASE/api/ui-bridge/analysis/setup/options" || true)"
    printf 'UNAUTH_SETUP_HTTP=%s\n' "$code"
    if [[ "$code" == "401" || "$code" == "403" ]]; then
      pass UNAUTHENTICATED_ANALYSIS_API_FAILS_CLOSED
    else
      block UNAUTHENTICATED_ANALYSIS_API_NOT_PROVEN_CLOSED
    fi
  fi
else
  printf 'LIVE_PROBES=SKIPPED_NO_NDSP_M2_LIVE_BASE\n'
fi

printf '\nPROJECT_FILES_MODIFIED=0\nPRODUCTION_FILES_MODIFIED=0\nSERVICES_RESTARTED=0\nDATABASE_MODIFIED=0\nNGINX_MODIFIED=0\nSYSTEMD_MODIFIED=0\n'
if (( FAIL )); then
  printf 'FINAL_STATUS=NDSP_M2_CERTIFICATION_FAIL\n'
  exit 1
fi
if (( BLOCK )); then
  printf 'FINAL_STATUS=NDSP_M2_CERTIFICATION_BLOCKED\n'
  exit 2
fi
printf 'FINAL_STATUS=NDSP_M2_CERTIFICATION_PASS\n'
