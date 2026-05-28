cat > ~/ndsp_full_decision_system_test.sh <<'SH'
#!/usr/bin/env bash
set -Eeuo pipefail

TASK_NAME="NDSP_FULL_DECISION_SYSTEM_TEST"
STAMP="$(date +%Y%m%d_%H%M%S)"

ROOT="/home/nawaf511/empire-core-new"
BACKEND="$ROOT/backend"
APP="$BACKEND/app"
TEST_DIR="$ROOT/tests"

REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
BACKUP_DIR="/home/nawaf511/ndsp_backups/${TASK_NAME}_${STAMP}"
REPORT="$REPORT_DIR/${TASK_NAME}_${STAMP}.md"

SERVICE="ndsp-api.service"
LOCAL_API="http://127.0.0.1:9001"

PYTHON_BIN="$BACKEND/venv/bin/python"
[ -x "$PYTHON_BIN" ] || PYTHON_BIN="python3"

mkdir -p "$REPORT_DIR" "$BACKUP_DIR" "$TEST_DIR"

log(){ echo "$@" | tee -a "$REPORT"; }
section(){ echo "" | tee -a "$REPORT"; echo "$1" | tee -a "$REPORT"; echo "------------------------------------------------------------" | tee -a "$REPORT"; }

{
  echo "# $TASK_NAME"
  echo "- STAMP=$STAMP"
  echo "- ROOT=$ROOT"
  echo "- BACKEND=$BACKEND"
  echo "- APP=$APP"
  echo "- BACKUP_DIR=$BACKUP_DIR"
  echo "- REPORT=$REPORT"
  echo "- PYTHON_BIN=$PYTHON_BIN"
} | tee "$REPORT"

section "1) Preconditions"
[ -d "$ROOT" ] || { log "ERROR: ROOT not found: $ROOT"; exit 1; }
[ -d "$BACKEND" ] || { log "ERROR: BACKEND not found: $BACKEND"; exit 1; }
[ -f "$APP/main.py" ] || { log "ERROR: main.py not found"; exit 1; }
log "PRECONDITIONS_OK=True"

section "2) Backup verification snapshots"
cp -a "$APP/main.py" "$BACKUP_DIR/main.py.snapshot"
if [ -f "$APP/middleware/decision_active_response_sanitizer.py" ]; then
  mkdir -p "$BACKUP_DIR/middleware"
  cp -a "$APP/middleware/decision_active_response_sanitizer.py" "$BACKUP_DIR/middleware/decision_active_response_sanitizer.py.snapshot"
fi
log "BACKUP_OK=True"
log "BACKUP_DIR=$BACKUP_DIR"

section "3) Compile and import boot"
cd "$BACKEND"
PYTHONPATH="$BACKEND:$ROOT" "$PYTHON_BIN" -m compileall -q "$APP"
PYTHONPATH="$BACKEND:$ROOT" "$PYTHON_BIN" - <<'PY' | tee -a "$REPORT"
import app.main
assert hasattr(app.main, "app")
print("IMPORT_BOOT_OK=True")
print(f"ROUTE_COUNT={len(app.main.app.routes)}")
PY
log "COMPILE_OK=True"

section "4) Service status"
if systemctl is-active --quiet "$SERVICE"; then
  log "SERVICE_ACTIVE=True"
else
  log "SERVICE_ACTIVE=False"
  sudo systemctl restart "$SERVICE"
  sleep 5
  if systemctl is-active --quiet "$SERVICE"; then
    log "SERVICE_RESTARTED_ACTIVE=True"
  else
    log "SERVICE_RESTARTED_ACTIVE=False"
  fi
fi

sudo systemctl status "$SERVICE" --no-pager -l | head -80 | tee -a "$REPORT" || true

section "5) Core HTTP smoke"
HEALTH_CODE="$(curl -sk -o /tmp/ndsp_full_system_health.json -w '%{http_code}' "$LOCAL_API/health" || true)"
STATUS_CODE="$(curl -sk -o /tmp/ndsp_full_system_status.json -w '%{http_code}' "$LOCAL_API/status" || true)"
DECISION_BTC_CODE="$(curl -sk -o /tmp/ndsp_full_system_decision_btc.json -w '%{http_code}' "$LOCAL_API/decision?symbol=BTCUSDT" || true)"
DECISION_ETH_CODE="$(curl -sk -o /tmp/ndsp_full_system_decision_eth.json -w '%{http_code}' "$LOCAL_API/decision?symbol=ETHUSDT" || true)"
DECISION_XAU_CODE="$(curl -sk -o /tmp/ndsp_full_system_decision_xau.json -w '%{http_code}' "$LOCAL_API/decision?symbol=XAUUSD" || true)"

log "HEALTH_HTTP_CODE=$HEALTH_CODE"
log "STATUS_HTTP_CODE=$STATUS_CODE"
log "DECISION_BTC_HTTP_CODE=$DECISION_BTC_CODE"
log "DECISION_ETH_HTTP_CODE=$DECISION_ETH_CODE"
log "DECISION_XAU_HTTP_CODE=$DECISION_XAU_CODE"

section "6) Sanitizer exposure check"
"$PYTHON_BIN" - <<'PY' | tee -a "$REPORT"
import json
from pathlib import Path

files = {
    "BTCUSDT": Path("/tmp/ndsp_full_system_decision_btc.json"),
    "ETHUSDT": Path("/tmp/ndsp_full_system_decision_eth.json"),
    "XAUUSD": Path("/tmp/ndsp_full_system_decision_xau.json"),
}

forbidden_fields = [
    '"tdl"', '"tdl_v2"', '"nmp"', '"nmp_context"', '"timing_authority"',
    '"dominant_direction"', '"decision_authority"', '"timing_controller"',
    '"raw_score"', '"layer_score"', '"weights"', '"internal_bias"',
    '"governance_runtime"', '"governance_engine"', '"black_layer"',
    '"weekly_open_gravity"', '"golden_alignment"', '"raw_signal"',
    '"raw_intelligence"', '"institutional_mapping"', '"participant_mapping"',
    '"execution_logic"', '"authority_source"', '"risk_formula"', '"scoring_formula"'
]

forbidden_terms = [
    "commitment of traders", "tdl", "nmp", "timing authority",
    "decision authority", "black layer", "decision quality stack",
    "buy signal", "sell signal", "trade execution", "automated trading",
    "financial advice", "take profit", "stop loss"
]

overall = True

for symbol, path in files.items():
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        text = json.dumps(payload, ensure_ascii=False).lower()
        field_hits = [x for x in forbidden_fields if x in text]
        term_hits = [x for x in forbidden_terms if x in text]
        ok = not field_hits and not term_hits
        overall = overall and ok
        print(f"{symbol}_JSON_READABLE=True")
        print(f"{symbol}_FORBIDDEN_FIELD_HITS={field_hits}")
        print(f"{symbol}_FORBIDDEN_TERM_HITS={term_hits}")
        print(f"{symbol}_PUBLIC_EXPOSURE_OK={ok}")
        if isinstance(payload, dict):
            print(f"{symbol}_TOP_LEVEL_KEYS={','.join(sorted(payload.keys())[:80])}")
    except Exception as exc:
        overall = False
        print(f"{symbol}_JSON_READABLE=False")
        print(f"{symbol}_ERROR={type(exc).__name__}:{exc}")

print("PUBLIC_SANITIZER_ALL_SYMBOLS_OK=" + ("True" if overall else "False"))
PY

section "7) Decision contract check"
"$PYTHON_BIN" - <<'PY' | tee -a "$REPORT"
import json
from pathlib import Path

files = {
    "BTCUSDT": Path("/tmp/ndsp_full_system_decision_btc.json"),
    "ETHUSDT": Path("/tmp/ndsp_full_system_decision_eth.json"),
    "XAUUSD": Path("/tmp/ndsp_full_system_decision_xau.json"),
}

overall = True

for symbol, path in files.items():
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        text = json.dumps(payload, ensure_ascii=False).lower()
        has_dict = isinstance(payload, dict)
        has_public_contract = has_dict and ("status" in payload or "message" in payload or "decision" in payload)
        no_direct_execution = all(term not in text for term in ["execute trade", "trade execution", "automated trading"])
        ok = bool(has_dict and has_public_contract and no_direct_execution)
        overall = overall and ok
        print(f"{symbol}_CONTRACT_OK={ok}")
        print(f"{symbol}_HAS_STATUS={'status' in payload if has_dict else False}")
        print(f"{symbol}_HAS_MESSAGE={'message' in payload if has_dict else False}")
        print(f"{symbol}_HAS_DECISION={'decision' in payload if has_dict else False}")
        print(f"{symbol}_NO_DIRECT_EXECUTION={no_direct_execution}")
    except Exception as exc:
        overall = False
        print(f"{symbol}_CONTRACT_OK=False")
        print(f"{symbol}_CONTRACT_ERROR={type(exc).__name__}:{exc}")

print("DECISION_CONTRACT_ALL_OK=" + ("True" if overall else "False"))
PY

section "8) Ops endpoints smoke"
ALERTS_STATUS_CODE="$(curl -sk -o /tmp/ndsp_full_system_alerts_status.json -w '%{http_code}' "$LOCAL_API/ops/alerts-status" || true)"
ASSISTANT_STATUS_CODE="$(curl -sk -o /tmp/ndsp_full_system_assistant_status.json -w '%{http_code}' "$LOCAL_API/ops/assistant-status" || true)"
WS_STATUS_CODE="$(curl -sk -o /tmp/ndsp_full_system_ws_status.json -w '%{http_code}' "$LOCAL_API/ops/ws-status" || true)"
CACHE_STATUS_CODE="$(curl -sk -o /tmp/ndsp_full_system_cache_status.json -w '%{http_code}' "$LOCAL_API/ops/cache-status" || true)"

log "ALERTS_STATUS_HTTP_CODE=$ALERTS_STATUS_CODE"
log "ASSISTANT_STATUS_HTTP_CODE=$ASSISTANT_STATUS_CODE"
log "WS_STATUS_HTTP_CODE=$WS_STATUS_CODE"
log "CACHE_STATUS_HTTP_CODE=$CACHE_STATUS_CODE"

section "9) Ghost path check"
GHOSTS=(
"$ROOT/ndsp_launch_reports"
"$BACKEND/test_e2e_pipeline.py"
"$BACKEND/ndsp_launch_reports"
"$BACKEND/reports"
"$ROOT/reports"
"$ROOT/tests_e2e"
"$BACKEND/tests_e2e"
)

FOUND_GHOSTS=0
for g in "${GHOSTS[@]}"; do
  if [ -e "$g" ]; then
    FOUND_GHOSTS=$((FOUND_GHOSTS+1))
    log "GHOST_FOUND=$g"
  else
    log "GHOST_NOT_FOUND=$g"
  fi
done
log "FOUND_GHOSTS=$FOUND_GHOSTS"

section "10) Final Assertions"
ASSERT_OK=True

[[ "$HEALTH_CODE" =~ ^2|3 ]] || ASSERT_OK=False
[[ "$STATUS_CODE" =~ ^2|3 ]] || ASSERT_OK=False
[[ "$DECISION_BTC_CODE" =~ ^2|3 ]] || ASSERT_OK=False
[[ "$DECISION_ETH_CODE" =~ ^2|3 ]] || ASSERT_OK=False
[[ "$DECISION_XAU_CODE" =~ ^2|3 ]] || ASSERT_OK=False

grep -q "IMPORT_BOOT_OK=True" "$REPORT" || ASSERT_OK=False
grep -q "COMPILE_OK=True" "$REPORT" || ASSERT_OK=False
grep -q "PUBLIC_SANITIZER_ALL_SYMBOLS_OK=True" "$REPORT" || ASSERT_OK=False
grep -q "DECISION_CONTRACT_ALL_OK=True" "$REPORT" || ASSERT_OK=False

if [ "$FOUND_GHOSTS" -gt 0 ]; then
  log "WARNING_GHOST_PATHS_FOUND=True"
else
  log "WARNING_GHOST_PATHS_FOUND=False"
fi

if [ "$ASSERT_OK" = "True" ]; then
  log "ASSERT_OK=True"
  log "BACKEND_HEALTHY=True"
  log "PUBLIC_SANITIZER_VERIFIED=True"
  log "FULL_DECISION_SYSTEM_TEST_OK=True"
  log "FINAL_STATUS=FULL_DECISION_SYSTEM_TEST_DONE"
else
  log "ASSERT_OK=False"
  log "FULL_DECISION_SYSTEM_TEST_OK=False"
  log "FINAL_STATUS=FULL_DECISION_SYSTEM_TEST_FAILED"
  exit 1
fi

log "REPORT=$REPORT"
log "BACKUP_DIR=$BACKUP_DIR"
log "NEXT_PHASE=UI_ADMIN_USER_PORTAL_PHASE"
log "DONE"
SH

chmod +x ~/ndsp_full_decision_system_test.sh
bash ~/ndsp_full_decision_system_test.sh
