#!/usr/bin/env python3
import json
import urllib.request
from pathlib import Path
from datetime import datetime

REPORT_DIR = Path("/home/nawaf511/ndsp_launch_reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

symbols = ["BTC", "ETH", "XRP"]
failed = []
results = []

for symbol in symbols:
    url = f"http://127.0.0.1:9001/decision?symbol={symbol}"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        if data.get("source_mode") != "http_decision":
            failed.append(symbol)
        results.append(data)
    except Exception as exc:
        failed.append(symbol)
        results.append({"symbol": symbol, "error": str(exc)})

stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
report = REPORT_DIR / f"NDSP_E2E_LAYER1_TO_LAYER16_{stamp}.md"

status = "E2E_LAYER1_TO_LAYER16_DONE" if not failed else "E2E_LAYER1_TO_LAYER16_FAILED"

report.write_text(
    "# NDSP E2E Layer1 To Layer16 Report\n\n"
    "SOURCE_MODE=http_decision\n\n"
    f"FAILED_SYMBOLS={failed}\n\n"
    f"FINAL_STATUS={status}\n\n"
    "```json\n"
    + json.dumps(results, ensure_ascii=False, indent=2)
    + "\n```\n",
    encoding="utf-8"
)

print(f"SOURCE_MODE=http_decision")
print(f"FAILED_SYMBOLS={failed}")
print(f"FINAL_STATUS={status}")
print(f"REPORT={report}")

if failed:
    raise SystemExit(1)
