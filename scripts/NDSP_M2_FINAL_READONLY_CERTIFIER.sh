#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
export LC_ALL=C

ROOT="${1:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
FE="$ROOT/frontend/ndsp-sovereign-meridian-ui"
BRIDGE="$ROOT/apps/ndsp-ui-bridge-api/main.py"
BRIDGE_GOV="$ROOT/apps/ndsp-ui-bridge-api/main_governed.py"
AUTH_CORE="$ROOT/apps/ndsp-auth-core-clean/server/src/server.ts"
DROPIN_SOURCE="$ROOT/infrastructure/systemd/ndsp-ui-bridge-api-m2-governed.conf"
RECONCILER="$ROOT/scripts/NDSP_NAW27_CAPABILITY_RECONCILE.py"
UI_SERVICE="ndsp-ui-bridge-api.service"
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
printf 'MODE=SOURCE_AND_OPTIONAL_RUNTIME_READ_ONLY\nROOT=%s\nUTC=%s\n' "$ROOT" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

section "1/8 — SOURCE IDENTITY"
if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  pass GIT_ROOT
else
  fail NOT_GIT_ROOT
fi
for file in \
  "$FE/package.json" \
  "$FE/package-lock.json" \
  "$FE/src/analysis/AnalysisContext.tsx" \
  "$FE/src/pages/AnalysisSetupPage.tsx" \
  "$FE/src/pages/AnalysisPage.tsx" \
  "$FE/src/api/decision.ts" \
  "$FE/src/auth/RequireUser.tsx" \
  "$BRIDGE" \
  "$BRIDGE_GOV" \
  "$AUTH_CORE" \
  "$DROPIN_SOURCE" \
  "$RECONCILER"
do
  require_file "$file"
done

section "2/8 — GOVERNED JOURNEY INVARIANTS"
require_grep 'path="analysis/setup"' "$FE/src/App.tsx" ANALYSIS_SETUP_ROUTE
require_grep 'RequireUser' "$FE/src/App.tsx" ANALYSIS_ROUTES_AUTH_GUARDED
require_grep 'AnalysisProvider' "$FE/src/main.tsx" ANALYSIS_PROVIDER_INSTALLED
require_grep 'analysisContext\.clearContext\(\)' "$FE/src/pages/AnalysisSetupPage.tsx" SETUP_INVALIDATES_PRIOR_CONTEXT
for key in market symbol timeframe analysisMode presentationMode; do
  require_grep "$key" "$FE/src/api/decision.ts" "CONTEXT_FIELD_${key}"
done
require_grep '/api/ui-bridge/analysis' "$FE/src/api/decision.ts" FRONTEND_UI_BRIDGE_CONTRACT_PRESENT
require_grep 'credentials: "include"' "$FE/src/api/decision.ts" FRONTEND_CREDENTIALS_INCLUDED
forbid_grep 'https://api\.ndsp\.app' "$FE/src/api/decision.ts" FRONTEND_AUTHENTICATED_ANALYSIS_SAME_ORIGIN
require_grep 'getCapabilityRegistrySummary' "$FE/src/api/decision.ts" FRONTEND_REGISTRY_CLIENT_PRESENT
require_grep 'globalRegistryReconciled' "$FE/src/pages/AnalysisPage.tsx" FRONTEND_RUNTIME_REGISTRY_GATE_PRESENT
require_grep 'runtime_capability_count_claimed' "$FE/src/pages/AnalysisPage.tsx" FRONTEND_REJECTS_311_RUNTIME_COUNT_CLAIM
forbid_grep 'from "\.\./data"|from '\''\.\./data'\''' "$FE/src/pages/AnalysisPage.tsx" LOCAL_ANALYSES_NOT_DECISION_AUTHORITY
forbid_grep 'GLOBAL_CAPABILITY_MAPPING_RECONCILED = false' "$FE/src/pages/AnalysisPage.tsx" MANUAL_GLOBAL_GATE_REMOVED

section "3/8 — AUTHORITATIVE CAP DISCOVERY-RECORD RECONCILIATION"
REGISTRY="$TMP/capability-registry.json"
set +e
python3 "$RECONCILER" --root "$ROOT" --output "$REGISTRY" --expected-count 311 2>&1 | tee "$TMP/reconcile.txt"
RECON_RC=${PIPESTATUS[0]}
set -e
if [[ "$RECON_RC" -eq 0 ]]; then
  pass CAP_311_RECORD_RECONCILIATION
elif [[ "$RECON_RC" -eq 2 ]]; then
  block CAP_311_RECORD_RECONCILIATION
else
  fail CAP_311_RECORD_RECONCILIATION
fi
python3 - "$REGISTRY" <<'PY' || fail CAP_REGISTRY_SEMANTICS
import json, sys
p=json.load(open(sys.argv[1],encoding='utf-8'))
assert p['contract']=='NDSP_CAPABILITY_DISCOVERY_RECONCILIATION_V1'
assert p['expected_record_count']==311
assert p['record_count']==311
assert p['parsed_record_count']==311
assert p['silent_omission_count']==0
assert p['parse_error_count']==0
assert p['global_reconciled'] is True
assert p['semantics']['record_count_is_runtime_capability_count'] is False
assert p['semantics']['activation_claim'] is False
assert len(p['entries'])==311
assert all(x['governed_state'] in {'CONTRIBUTED','BLOCKED','NOT_APPLICABLE','UNAVAILABLE','STALE','PARTIAL','GOVERNANCE_PROTECTED'} for x in p['entries'])
print('PASS|CAP_REGISTRY_SEMANTICS')
PY

section "4/8 — CAPABILITY / SECRET GOVERNANCE"
for state in CONTRIBUTED BLOCKED NOT_APPLICABLE UNAVAILABLE STALE PARTIAL GOVERNANCE_PROTECTED; do
  require_grep "${state}" "$FE/src/analysis/types.ts" "CAPABILITY_STATE_${state}"
done
require_grep 'silent_omission' "$BRIDGE" CURRENT_FAMILY_SILENT_OMISSION_CHECK
require_grep 'LAYER_REGISTRY' "$BRIDGE" SIXTEEN_LAYER_REGISTRY_PRESENT
require_grep 'frontend_recomputes_protected_logic' "$BRIDGE" NO_FRONTEND_PROTECTED_RECOMPUTE_CONTRACT
require_grep 'protected_formulas_exposed' "$BRIDGE" PROTECTED_FORMULA_EXPOSURE_CONTRACT

section "5/8 — SERVER-SIDE AUTH + SAFE REGISTRY SOURCE GATE"
require_grep '/api/auth/session' "$AUTH_CORE" AUTH_SESSION_PROVIDER_EXISTS
require_grep 'authenticated: true' "$AUTH_CORE" AUTH_SESSION_POSITIVE_CONTRACT
require_grep 'AUTH_SESSION_URL' "$BRIDGE_GOV" UI_BRIDGE_AUTH_PROVIDER_BOUND
require_grep '127\.0\.0\.1:19091/api/auth/session' "$BRIDGE_GOV" UI_BRIDGE_AUTH_CANONICAL_LOCAL_DEFAULT
forbid_grep '127\.0\.0\.1:9020/api/auth/session' "$BRIDGE_GOV" UI_BRIDGE_STALE_AUTH_DEFAULT_REMOVED
require_grep 'with_name\("capability_registry\.json"\)' "$BRIDGE_GOV" UI_BRIDGE_PORTABLE_REGISTRY_DEFAULT
require_grep 'ANALYSIS_PREFIX' "$BRIDGE_GOV" UI_BRIDGE_ANALYSIS_SCOPE_ONLY
require_grep 'Cookie' "$BRIDGE_GOV" UI_BRIDGE_FORWARDS_SESSION_COOKIE
require_grep 'payload\.get\("authenticated"\) is not True' "$BRIDGE_GOV" UI_BRIDGE_REQUIRES_AUTHENTICATED_TRUE
require_grep 'AUTH_SESSION_UNAVAILABLE' "$BRIDGE_GOV" UI_BRIDGE_AUTH_UPSTREAM_FAIL_CLOSED
require_grep 'AUTHENTICATION_REQUIRED' "$BRIDGE_GOV" UI_BRIDGE_UNAUTHENTICATED_FAIL_CLOSED
require_grep 'capability-registry' "$BRIDGE_GOV" SAFE_REGISTRY_ENDPOINT_PRESENT
require_grep 'runtime_capability_count_claimed' "$BRIDGE_GOV" SAFE_REGISTRY_REFUSES_RUNTIME_COUNT_CLAIM
require_grep '19091/api/auth/session' "$DROPIN_SOURCE" GOVERNED_SYSTEMD_AUTH_ENDPOINT_DECLARED
require_grep 'venv/bin/uvicorn main_governed:app' "$DROPIN_SOURCE" GOVERNED_SYSTEMD_ENTRYPOINT_DECLARED
require_grep 'NDSP_CAPABILITY_REGISTRY_PATH' "$DROPIN_SOURCE" GOVERNED_REGISTRY_PATH_DECLARED
forbid_grep '/opt/ndsp-ui-bridge-api' "$DROPIN_SOURCE" STALE_UI_RUNTIME_PATH_REMOVED

section "6/8 — PYTHON + FRONTEND BUILD"
if command -v python3 >/dev/null 2>&1; then
  PYTHONPYCACHEPREFIX="$TMP/pycache" python3 -m py_compile "$BRIDGE" "$BRIDGE_GOV" "$RECONCILER" \
    && pass PYTHON_COMPILE \
    || fail PYTHON_COMPILE
else
  fail PYTHON3_NOT_AVAILABLE
fi

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
    node --test tests/governed-analysis-state-machine.test.mjs
    npm run typecheck
    npm run build
  ) && pass FRONTEND_TYPECHECK_AND_BUILD || fail FRONTEND_TYPECHECK_AND_BUILD
fi

section "7/8 — OPTIONAL LIVE CONTRACT PROBES"
LIVE_BASE="${NDSP_M2_LIVE_BASE:-}"
if [[ -n "$LIVE_BASE" ]]; then
  if ! command -v curl >/dev/null 2>&1; then
    fail CURL_NOT_AVAILABLE_FOR_LIVE_PROBE
  else
    auth_code="$(curl -ksS -o "$TMP/auth.json" -w '%{http_code}' "$LIVE_BASE/api/auth/session" || true)"
    printf 'AUTH_UNAUTH_HTTP|CODE=%s\n' "$auth_code"
    if [[ "$auth_code" == "200" || "$auth_code" == "401" || "$auth_code" == "403" ]]; then
      pass AUTH_ROUTE_REACHABLE
    else
      block AUTH_ROUTE_NOT_REACHABLE
    fi

    for path in \
      /api/ui-bridge/analysis/setup/options \
      /api/ui-bridge/analysis/context/validate \
      /api/ui-bridge/analysis/capability-coverage \
      /api/ui-bridge/analysis/capability-registry
    do
      code="$(curl -ksS -o "$TMP/unauth.json" -w '%{http_code}' "$LIVE_BASE$path" || true)"
      printf 'UNAUTH_HTTP|PATH=%s|CODE=%s\n' "$path" "$code"
      if [[ "$code" == "401" || "$code" == "403" ]]; then
        pass "UNAUTH_FAIL_CLOSED:$path"
      else
        block "UNAUTH_NOT_PROVEN_CLOSED:$path"
      fi
    done
  fi
else
  printf 'LIVE_PROBES=SKIPPED_NO_NDSP_M2_LIVE_BASE\n'
fi

section "8/8 — OPTIONAL RUNTIME ENTRYPOINT PROOF"
if [[ "${NDSP_M2_EXPECT_RUNTIME_GOVERNED:-NO}" == "YES" ]]; then
  if ! command -v systemctl >/dev/null 2>&1; then
    fail SYSTEMCTL_NOT_AVAILABLE_FOR_RUNTIME_PROOF
  else
    exec_line="$(systemctl show "$UI_SERVICE" -p ExecStart --value 2>/dev/null || true)"
    printf 'RUNTIME_EXECSTART=%s\n' "$exec_line"
    grep -q 'main_governed:app' <<<"$exec_line" \
      && pass GOVERNED_RUNTIME_ENTRYPOINT_ACTIVE \
      || block GOVERNED_RUNTIME_ENTRYPOINT_NOT_ACTIVE
  fi
else
  printf 'RUNTIME_ENTRYPOINT_PROOF=SKIPPED_NOT_REQUESTED\n'
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
