#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/nawaf511/empire-core-new"
RESEARCH="$ROOT/research"
USER_RESEARCH="$ROOT/apps/user-portal/research"
ADMIN_RESEARCH="$ROOT/apps/admin-console/research"
REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
TS="$(date +%Y%m%d_%H%M%S)"
REPORT="$REPORT_DIR/DSP_RESEARCH_LABS_READINESS_$TS.md"

mkdir -p "$REPORT_DIR"
log(){ echo "$*" | tee -a "$REPORT"; }

FAIL=0

log "REPORT=$REPORT"
log "ROOT=$ROOT"

check_file(){
  local f="$1"
  if [ -f "$f" ]; then
    log "FILE_OK=$f"
  else
    log "FILE_MISSING=$f"
    FAIL=$((FAIL+1))
  fi
}

check_file "$RESEARCH/RESEARCH_LABS_REFERENCE.md"
check_file "$RESEARCH/research_labs_reference.json"
check_file "$RESEARCH/research-labs.env"
check_file "$RESEARCH/nmp-lab/results/nmp-research-level-latest.json"
check_file "$USER_RESEARCH/NMP_Research_Level.html"
check_file "$USER_RESEARCH/nmp-research-level-latest.json"
check_file "$ADMIN_RESEARCH/NMP_Research_Level.html"
check_file "$ADMIN_RESEARCH/nmp-research-level-latest.json"
check_file "$ADMIN_RESEARCH/TDL_Research_Lab.html"
check_file "$ADMIN_RESEARCH/tdl-lab-latest.json"

log ""
log "== HTTP_CHECKS =="
for url in \
  "https://my.ndsp.app/" \
  "https://my.ndsp.app/NDSP_Command_Center.html" \
  "https://my.ndsp.app/research/" \
  "https://my.ndsp.app/research/NMP_Research_Level.html" \
  "https://my.ndsp.app/research/nmp-research-level-latest.json" \
  "https://admin.ndsp.app/" \
  "https://admin.ndsp.app/research/" \
  "https://admin.ndsp.app/research/NMP_Research_Level.html" \
  "https://admin.ndsp.app/research/nmp-research-level-latest.json" \
  "https://admin.ndsp.app/research/TDL_Research_Lab.html" \
  "https://admin.ndsp.app/research/tdl-lab-latest.json"
do
  code="$(curl -k -L -s -o /tmp/dsp_research_http.out -w "%{http_code}" "$url" || true)"
  log "URL_CHECK $url HTTP=$code"
  [ "$code" = "200" ] || FAIL=$((FAIL+1))
done

log ""
log "== NMP_STATUS =="
grep -E '"status"|"production_approved"|"final_formula_adopted"|"formula_candidate"' "$USER_RESEARCH/nmp-research-level-latest.json" | tee -a "$REPORT" || true

if grep -q '"final_formula_adopted": true' "$USER_RESEARCH/nmp-research-level-latest.json"; then
  log "ERROR=NMP_FINAL_FORMULA_UNEXPECTEDLY_ADOPTED"
  FAIL=$((FAIL+1))
fi

if grep -q '"production_approved": true' "$USER_RESEARCH/nmp-research-level-latest.json"; then
  log "ERROR=NMP_PRODUCTION_APPROVED_UNEXPECTEDLY_TRUE"
  FAIL=$((FAIL+1))
fi

log ""
if [ "$FAIL" -eq 0 ]; then
  log "ASSERT_OK=True"
  log "FAIL_COUNT=0"
  log "FINAL_STATUS=DSP_RESEARCH_LABS_READINESS_PASSED"
else
  log "ASSERT_OK=False"
  log "FAIL_COUNT=$FAIL"
  log "FINAL_STATUS=DSP_RESEARCH_LABS_READINESS_FAILED"
  exit 1
fi
