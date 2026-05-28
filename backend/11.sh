cat > ~/ndsp_patch_public_sanitization.sh <<'SH'
#!/usr/bin/env bash
set -Eeuo pipefail

TASK_NAME="NDSP_PATCH_PUBLIC_SANITIZATION"
STAMP="$(date +%Y%m%d_%H%M%S)"

ROOT="/home/nawaf511/empire-core-new"
BACKEND="$ROOT/backend"
APP="$BACKEND/app"

REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
BACKUP_DIR="/home/nawaf511/ndsp_backups/${TASK_NAME}_${STAMP}"
REPORT="$REPORT_DIR/${TASK_NAME}_${STAMP}.md"

PY="$BACKEND/venv/bin/python"
[ -x "$PY" ] || PY="python3"

mkdir -p "$REPORT_DIR" "$BACKUP_DIR"

log() {
  echo "$@" | tee -a "$REPORT"
}

section() {
  echo "" | tee -a "$REPORT"
  echo "$1" | tee -a "$REPORT"
  echo "------------------------------------------------------------" | tee -a "$REPORT"
}

{
  echo "# $TASK_NAME"
  echo "- ROOT=$ROOT"
  echo "- BACKEND=$BACKEND"
  echo "- REPORT=$REPORT"
  echo "- BACKUP_DIR=$BACKUP_DIR"
} | tee "$REPORT"

section "1) Backup candidate files"

find "$APP" -type f \( -name "*.py" -o -name "*.json" \) \
| while read -r f; do
    if grep -qiE 'TDL|NMP|Black Layer|COT|Asset Manager|Leveraged Funds|Dealer Intermediary|Other Reportables|Commercials|Non-Commercials' "$f"; then
      mkdir -p "$BACKUP_DIR$(dirname "$f")"
      cp -a "$f" "$BACKUP_DIR$f"
      log "BACKED_UP=$f"
    fi
done

section "2) Patch sensitive public terminology"

"$PY" <<'PY'
from pathlib import Path
import re

ROOT = Path("/home/nawaf511/empire-core-new/backend/app")

targets = []

for p in ROOT.rglob("*"):
    if p.suffix.lower() not in [".py", ".json"]:
        continue

    try:
        text = p.read_text(errors="ignore")
    except Exception:
        continue

    if re.search(r"TDL|NMP|Black Layer|COT|Asset Manager|Leveraged Funds|Dealer Intermediary|Other Reportables|Commercials|Non-Commercials", text, re.I):
        targets.append(p)

replacements = {
    r"\bTDL\b": "timing model",
    r"\bNMP\b": "market alignment",
    r"\bBlack Layer\b": "risk shield",
    r"\bCOT\b": "market positioning",
    r"\bCommitment of Traders\b": "market positioning",
    r"\bAsset Manager\b": "institutional direction",
    r"\bLeveraged Funds\b": "market momentum",
    r"\bDealer Intermediary\b": "market structure",
    r"\bOther Reportables\b": "market activity",
    r"\bCommercials\b": "institutional positioning",
    r"\bNon-Commercials\b": "market momentum",
}

patched = 0

for p in targets:
    try:
        s = p.read_text(errors="ignore")
        original = s

        for old, new in replacements.items():
            s = re.sub(old, new, s, flags=re.I)

        if s != original:
            p.write_text(s)
            print(f"PATCHED={p}")
            patched += 1

    except Exception as e:
        print(f"PATCH_FAILED={p} error={e}")

print(f"PATCH_COUNT={patched}")
PY

section "3) Compile backend"

cd "$BACKEND"

PYTHONPATH="$BACKEND" \
"$PY" -m compileall -q "$APP"

log "COMPILE_OK=True"

section "4) Restart API"

sudo systemctl restart ndsp-api.service
sleep 4

systemctl is-active ndsp-api.service | sed 's/^/NDSP_API_ACTIVE=/' | tee -a "$REPORT"

section "5) Quick sanitization verification"

OUT="/tmp/ndsp_sanitize_check.json"

curl -sk \
"$(
printf "%s?symbol=BTCUSDT" "http://127.0.0.1:9001/decision"
)" \
-o "$OUT"

FAILS=0

TERMS=(
  "TDL"
  "NMP"
  "Black Layer"
  "COT"
  "Asset Manager"
  "Leveraged Funds"
  "Dealer Intermediary"
  "Other Reportables"
  "Commercials"
  "Non-Commercials"
)

for t in "${TERMS[@]}"; do

  if grep -qi "$t" "$OUT"; then
    log "FORBIDDEN_TERM_FOUND=$t"
    FAILS=$((FAILS+1))
  fi

done

log "FORBIDDEN_COUNT=$FAILS"

section "6) Final"

if [ "$FAILS" = "0" ]; then
  log "ASSERT_OK=True"
  log "FINAL_STATUS=PUBLIC_OUTPUT_SANITIZATION_LOCKED"
else
  log "ASSERT_OK=False"
  log "FINAL_STATUS=SANITIZATION_NEEDS_MORE_REVIEW"
  exit 1
fi

log "REPORT=$REPORT"
log "BACKUP_DIR=$BACKUP_DIR"
log "DONE"
SH

chmod +x ~/ndsp_patch_public_sanitization.sh
bash ~/ndsp_patch_public_sanitization.sh
