#!/usr/bin/env bash
set -euo pipefail

FAILS=0
WARNS=0

fail(){ echo "FAIL=$*"; FAILS=$((FAILS+1)); }
warn(){ echo "WARN=$*"; WARNS=$((WARNS+1)); }
pass(){ echo "PASS=$*"; }

check_http(){
  local name="$1"
  local url="$2"
  if curl -fsS --max-time 8 "$url" >/dev/null; then
    pass "${name}_HTTP_OK=$url"
  else
    fail "${name}_HTTP_FAIL=$url"
  fi
}

check_public_warn(){
  local name="$1"
  local url="$2"
  if curl -fsS --max-time 10 "$url" >/dev/null; then
    pass "${name}_PUBLIC_OK=$url"
  else
    warn "${name}_PUBLIC_NOT_READY_OR_BLOCKED=$url"
  fi
}

echo "# NDSP Gateway Readiness"
echo "Generated=$(date +%Y%m%d_%H%M%S)"

echo ""
echo "== 1) LOCAL CORE SERVICES =="
check_http "CTL-001_health" "http://127.0.0.1:9081/health"
check_http "CTL-001_version" "http://127.0.0.1:9081/version"
check_http "CTL-001_about" "http://127.0.0.1:9081/about"
check_http "CTL-001_identity" "http://127.0.0.1:9081/identity"
check_http "CDS-001_health" "http://127.0.0.1:9078/health"
check_http "CDS-001_latest" "http://127.0.0.1:9078/api/completed/latest"
check_http "DGC-001_health" "http://127.0.0.1:9079/health"
check_http "BOT-001_health" "http://127.0.0.1:9080/health"

echo ""
echo "== 2) CURRENT PUBLIC READ-ONLY ROUTES =="
check_public_warn "COMPLETED_LATEST" "https://api.ndsp.app/api/completed/latest"
check_public_warn "GOVERNANCE_HEALTH" "https://api.ndsp.app/api/governance/health"

echo ""
echo "== 3) NGINX CONFIG TEST =="
if command -v nginx >/dev/null 2>&1; then
  if sudo nginx -t >/tmp/ndsp_nginx_test.out 2>&1; then
    cat /tmp/ndsp_nginx_test.out
    pass "NGINX_TEST_OK"
  else
    cat /tmp/ndsp_nginx_test.out
    fail "NGINX_TEST_FAILED"
  fi
else
  warn "NGINX_NOT_FOUND"
fi

echo ""
echo "== 4) SUMMARY =="
echo "FAIL_COUNT=$FAILS"
echo "WARN_COUNT=$WARNS"

if [ "$FAILS" -eq 0 ]; then
  echo "NDSP_GATEWAY_READINESS=PASS"
  exit 0
else
  echo "NDSP_GATEWAY_READINESS=FAIL"
  exit 1
fi
