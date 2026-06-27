#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/home/nawaf511/empire-core-new"
LAB="$ROOT/research/nmp-lab"
ADMIN="$ROOT/apps/admin-console"
OUT="$ADMIN/nmp-lab-summary.json"
TMP="$(mktemp)"

python3 - "$LAB/results" "$TMP" <<'PY'
import sys, json, csv
from pathlib import Path

results = Path(sys.argv[1])
out = Path(sys.argv[2])

items = []
for f in sorted(results.glob("*_nmp_lab_summary.csv")):
    with f.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            row["source_file"] = f.name
            if not row.get("nmp_formula"):
                detector = row.get("detector", "")
                ref = row.get("reference_price_type", "")
                row["opposite_candle_rule"] = row.get("opposite_candle_rule") or "last_opposite_candle_before_momentum"
                row["nmp_formula"] = f"{detector} + Opposite Candle + {ref}".strip()
            for k in ["tests","touch_rate","bounce_rate","false_break_rate","avg_reaction_pct","score"]:
                if k in row:
                    try:
                        row[k] = float(row[k])
                    except Exception:
                        pass
            items.append(row)

items.sort(key=lambda r: float(r.get("score") or 0), reverse=True)

payload = {
    "ok": True,
    "files_count": len(list(results.glob("*_nmp_lab_summary.csv"))),
    "items_count": len(items),
    "items": items[:500]
}

out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
PY

mv "$TMP" "$OUT"
echo "PUBLISHED=$OUT"
