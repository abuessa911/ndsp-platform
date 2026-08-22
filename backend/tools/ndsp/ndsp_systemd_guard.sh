#!/usr/bin/env bash
set -euo pipefail

FAILS=0
WARNS=0

fail(){ echo "FAIL=$*"; FAILS=$((FAILS+1)); }
warn(){ echo "WARN=$*"; WARNS=$((WARNS+1)); }
pass(){ echo "PASS=$*"; }

echo "# NDSP Systemd Guard"

check_service(){
  local id="$1"
  local unit="$2"
  local port="$3"

  echo ""
  echo "== CHECK $id =="

  if systemctl is-active --quiet "$unit"; then
    pass "${id}_ACTIVE"
  else
    fail "${id}_NOT_ACTIVE"
  fi

  if systemctl is-enabled --quiet "$unit"; then
    pass "${id}_ENABLED"
  else
    fail "${id}_NOT_ENABLED"
  fi

  local pid=""
  pid="$(systemctl show "$unit" -p MainPID --value 2>/dev/null || true)"
  echo "${id}_MAINPID=$pid"

  if [ -n "$pid" ] && [ "$pid" != "0" ]; then
    local owner=""
    owner="$(ps -o user= -p "$pid" 2>/dev/null | awk '{print $1}' || true)"
    echo "${id}_OWNER=${owner:-UNKNOWN}"
    if [ "$owner" = "$USER" ]; then
      pass "${id}_OWNERSHIP_OK"
    else
      warn "${id}_OWNER_NOT_CURRENT_USER_${owner:-UNKNOWN}"
    fi
  else
    fail "${id}_NO_MAINPID"
  fi

  for ep in health version about; do
    if curl -fsS "http://127.0.0.1:$port/$ep" >/dev/null; then
      pass "${id}_${ep}_HTTP_OK"
    else
      fail "${id}_${ep}_HTTP_FAIL"
    fi
  done
}

check_service "CTL-001" "ndsp-ctl-001-workspace-identity.service" "9081"
check_service "CDS-001" "ndsp-completed_decision.service" "9078"
check_service "DGC-001" "ndsp-decision_governance_core.service" "9079"
check_service "BOT-001" "ndsp-bot_execution.service" "9080"

echo ""
echo "== SUMMARY =="
echo "FAIL_COUNT=$FAILS"
echo "WARN_COUNT=$WARNS"

if [ "$FAILS" -eq 0 ]; then
  echo "NDSP_SYSTEMD_GUARD=PASS"
  exit 0
else
  echo "NDSP_SYSTEMD_GUARD=FAIL"
  exit 1
fi
