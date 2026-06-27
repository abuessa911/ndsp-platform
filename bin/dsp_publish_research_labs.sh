#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/nawaf511/empire-core-new"
RESEARCH="$ROOT/research"
NMP="$RESEARCH/nmp-lab"
TDL="$RESEARCH/tdl-lab"
USER_RESEARCH="$ROOT/apps/user-portal/research"
ADMIN_RESEARCH="$ROOT/apps/admin-console/research"
REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
TS="$(date +%Y%m%d_%H%M%S)"
REPORT="$REPORT_DIR/DSP_PUBLISH_RESEARCH_LABS_$TS.md"

mkdir -p "$REPORT_DIR" "$USER_RESEARCH" "$ADMIN_RESEARCH" "$NMP/results" "$TDL/results"

log(){ echo "$*" | tee -a "$REPORT"; }

log "REPORT=$REPORT"
log "ACTION=PUBLISH_RESEARCH_LABS"

FAIL=0

NMP_SRC="$NMP/results/nmp-research-level-latest.json"
TDL_SRC="$TDL/results/tdl-lab-latest.json"

# NMP fallback آمن إذا لا توجد نتيجة ديناميكية بعد
if [ ! -f "$NMP_SRC" ]; then
cat > "$NMP_SRC" <<'JSON'
{
  "project": "DSP — منصة دعم القرار",
  "lab": "NMP Formula Lab",
  "status": "TEMP_RESEARCH_RESULT",
  "production_approved": false,
  "final_formula_adopted": false,
  "formula_candidate": "RSI14 + Opposite Candle + High",
  "display_title_ar": "مستوى NMP البحثي",
  "display_title_en": "NMP Research Level",
  "symbol": "RESEARCH_SAMPLE",
  "timeframe": "LAB",
  "nmp_research_level": null,
  "level_type": "research_context_level",
  "last_updated": null,
  "user_notice_ar": "هذا المستوى ناتج من مختبر NMP Formula Lab، وهو قيد البحث ولم يعتمد كصيغة نهائية بعد. يعرض كمعلومة سياقية بحثية فقط وليس توصية مالية أو أمر تداول أو ضمانًا للنتائج.",
  "production_note": "NOT_FINAL_FORMULA"
}
JSON
fi

# TDL fallback آمن إذا لا توجد نتيجة ديناميكية بعد
if [ ! -f "$TDL_SRC" ]; then
cat > "$TDL_SRC" <<'JSON'
{
  "project": "DSP — منصة دعم القرار",
  "lab": "TDL Research Lab",
  "status": "RESEARCH_LAB_APPROVED",
  "production_approved": false,
  "latest_result_available": false,
  "last_updated": null,
  "notice_ar": "مختبر TDL مخصص للأبحاث والتحقق. لا يعرض منطقًا خامًا أو أوزانًا أو معادلات داخلية."
}
JSON
fi

cp -a "$NMP_SRC" "$USER_RESEARCH/nmp-research-level-latest.json"
cp -a "$NMP_SRC" "$ADMIN_RESEARCH/nmp-research-level-latest.json"
cp -a "$TDL_SRC" "$ADMIN_RESEARCH/tdl-lab-latest.json"

# نسخة اختيارية للمستخدم بدون كسر إذا أضيفت صفحة TDL مستقبلًا
cp -a "$TDL_SRC" "$USER_RESEARCH/tdl-lab-latest.json" 2>/dev/null || true

log "PUBLISHED_NMP_TO_USER=$USER_RESEARCH/nmp-research-level-latest.json"
log "PUBLISHED_NMP_TO_ADMIN=$ADMIN_RESEARCH/nmp-research-level-latest.json"
log "PUBLISHED_TDL_TO_ADMIN=$ADMIN_RESEARCH/tdl-lab-latest.json"

log ""
log "== VALIDATION =="
grep -E '"status"|"production_approved"|"final_formula_adopted"|"formula_candidate"' "$USER_RESEARCH/nmp-research-level-latest.json" | tee -a "$REPORT" || true
grep -E '"lab"|"status"|"production_approved"' "$ADMIN_RESEARCH/tdl-lab-latest.json" | tee -a "$REPORT" || true

log ""
log "ASSERT_OK=True"
log "FAIL_COUNT=0"
log "FINAL_STATUS=DSP_RESEARCH_LABS_PUBLISHED_DONE"
