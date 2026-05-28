cat > ~/ndsp_fix_layer16_safe_text_test.sh <<'SH'
#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${ROOT:-/home/nawaf511/empire-core-new}"
BACKEND="$ROOT/backend"
TEST_FILE="$ROOT/test_layer16_scenarios.py"
REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
BACKUP_DIR="/home/nawaf511/ndsp_backups/fix_layer16_safe_text_test_$(date +%Y%m%d_%H%M%S)"
REPORT="$REPORT_DIR/NDSP_FIX_LAYER16_SAFE_TEXT_TEST_$(date +%Y%m%d_%H%M%S).md"

PYTHON_BIN="$BACKEND/venv/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
  PYTHON_BIN="python3"
fi

mkdir -p "$REPORT_DIR" "$BACKUP_DIR"

log() { echo "$@" | tee -a "$REPORT"; }
section() {
  echo "" | tee -a "$REPORT"
  echo "$1" | tee -a "$REPORT"
  echo "------------------------------------------------------------" | tee -a "$REPORT"
}

{
  echo "# NDSP Fix Layer 16 Safe Text Test"
  echo ""
  echo "- ROOT=$ROOT"
  echo "- BACKEND=$BACKEND"
  echo "- TEST_FILE=$TEST_FILE"
  echo "- BACKUP_DIR=$BACKUP_DIR"
  echo "- REPORT=$REPORT"
  echo "- PYTHON_BIN=$PYTHON_BIN"
} | tee "$REPORT"

section "1) Validate"

if [ ! -d "$ROOT" ]; then
  log "ERROR: ROOT not found: $ROOT"
  exit 1
fi

if [ ! -f "$TEST_FILE" ]; then
  log "ERROR: TEST_FILE not found: $TEST_FILE"
  exit 1
fi

log "VALIDATE_OK=True"

section "2) Backup"

mkdir -p "$BACKUP_DIR"
cp -a "$TEST_FILE" "$BACKUP_DIR/test_layer16_scenarios.py.bak"
log "BACKUP_OK=True"
log "BACKUP_FILE=$BACKUP_DIR/test_layer16_scenarios.py.bak"

section "3) Patch safe text validator"

"$PYTHON_BIN" - <<PY
from pathlib import Path

path = Path("$TEST_FILE")
text = path.read_text(encoding="utf-8")

old = '''def assert_safe_text(payload: dict) -> bool:
    forbidden = [
        "BUY NOW",
        "SELL NOW",
        "EXECUTE TRADE",
        "GUARANTEED PROFIT",
        "FINANCIAL ADVICE",
        "ENTRY CONFIRMED",
    ]
    raw = json.dumps(payload, ensure_ascii=False).upper()
    return not any(term in raw for term in forbidden)
'''

new = '''def assert_safe_text(payload: dict) -> bool:
    """
    Validate that Layer 16 does not produce unsafe direct-action language.

    Important:
    Neutral disclaimers such as "not financial advice" and
    "not an execution instruction" are allowed because they reduce legal
    and compliance risk. The forbidden list below focuses on direct
    action/guarantee wording, not protective disclaimers.
    """
    forbidden = [
        "BUY NOW",
        "SELL NOW",
        "EXECUTE TRADE",
        "EXECUTE NOW",
        "GUARANTEED PROFIT",
        "GUARANTEED WIN",
        "HIGH WIN RATE",
        "ENTRY CONFIRMED",
        "TAKE THIS TRADE",
        "OPEN POSITION",
        "CLOSE POSITION",
    ]
    raw = json.dumps(payload, ensure_ascii=False).upper()
    return not any(term in raw for term in forbidden)
'''

if old not in text:
    raise SystemExit("ERROR: expected assert_safe_text block not found")

path.write_text(text.replace(old, new), encoding="utf-8")
print("PATCHED=True")
PY

log "PATCH_OK=True"
log "PATCHED=$TEST_FILE"

section "4) Compile"

PYTHONPATH="$ROOT" "$PYTHON_BIN" -m py_compile "$TEST_FILE"
log "COMPILE_OK=True"

section "5) Re-run Layer 16 simulation test"

cd "$ROOT"
PYTHONPATH="$ROOT" "$PYTHON_BIN" "$TEST_FILE" | tee -a "$REPORT"

section "6) Final Assertions"

if grep -q "OVERALL_LAYER16_ASSERT_OK=True" "$REPORT" \
  && ! grep -q "ASSERT_OK=False" "$REPORT" \
  && ! grep -q "Traceback" "$REPORT" \
  && ! grep -q "ERROR:" "$REPORT"; then
  log "OVERALL_LAYER16_ASSERT_OK=True"
  log "FINAL_STATUS=LAYER16_SAFE_TEXT_TEST_FIXED"
else
  log "OVERALL_LAYER16_ASSERT_OK=False"
  log "FINAL_STATUS=LAYER16_SAFE_TEXT_TEST_FAILED"
  log "ROLLBACK_HINT=cp -a $BACKUP_DIR/test_layer16_scenarios.py.bak $TEST_FILE"
  exit 1
fi

log "REPORT=$REPORT"
log "BACKUP_DIR=$BACKUP_DIR"
log "ROLLBACK_HINT=cp -a $BACKUP_DIR/test_layer16_scenarios.py.bak $TEST_FILE"
log "DONE"
SH

chmod +x ~/ndsp_fix_layer16_safe_text_test.sh
bash ~/ndsp_fix_layer16_safe_text_test.sh
