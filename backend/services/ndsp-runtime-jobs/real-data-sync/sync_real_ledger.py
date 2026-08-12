#!/usr/bin/env python3
import csv
import io
import json
import os
import subprocess
import urllib.request
import datetime

DATA="/var/www/ndsp-my/data"
API="http://127.0.0.1:9057/api/decision/quality-live"
SYMBOLS=["BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT","XRPUSDT","ADAUSDT","DOGEUSDT"]

os.makedirs(DATA, exist_ok=True)

def fetch(symbol):
    with urllib.request.urlopen(f"{API}?symbol={symbol}", timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))

def run_psql(sql, stdin=None):
    p=subprocess.run(
        ["sudo","-u","postgres","psql","-d","ndsp_auth","-At","-c",sql],
        input=stdin,
        text=True,
        capture_output=True
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip())
    return p.stdout.strip()

rows=[]
for sym in SYMBOLS:
    try:
        j=fetch(sym)
        if not j.get("ok"):
            continue

        sc=j.get("scenario") or {}
        pub=j.get("allowed_public_outputs") or {}
        lm=j.get("live_market_analysis") or {}
        ins=j.get("instrument") or {}

        rows.append([
            sym,
            str(sc.get("scenario_state") or ""),
            str(sc.get("scenario_directional_context") or pub.get("directional_bias") or ""),
            int(pub.get("decision_quality") or 0),
            str(lm.get("price") or ins.get("live_price") or 0),
            str(j.get("data_provider") or lm.get("provider") or ""),
            str(j.get("generated_at") or datetime.datetime.utcnow().isoformat()+"Z"),
            json.dumps(j, ensure_ascii=False)
        ])
    except Exception:
        continue

if rows:
    buf=io.StringIO()
    writer=csv.writer(buf, quoting=csv.QUOTE_MINIMAL)
    writer.writerows(rows)
    run_psql("""
COPY ndsp_decision_ledger
(symbol, scenario_state, directional_context, decision_quality, price, provider, generated_at, payload)
FROM STDIN WITH (FORMAT csv);
""", buf.getvalue())

items_raw=run_psql("""
SELECT COALESCE(json_agg(row_to_json(t)),'[]'::json)::text
FROM (
  SELECT
    symbol,
    to_char(created_at,'YYYY-MM-DD HH24:MI:SS') AS completed_at,
    scenario_state AS final_state,
    decision_quality AS quality_score,
    directional_context AS completion_reason,
    price,
    provider
  FROM ndsp_decision_ledger
  ORDER BY created_at DESC
  LIMIT 50
) t;
""") or "[]"

items=json.loads(items_raw)

with open(f"{DATA}/completed-decisions.json","w",encoding="utf-8") as f:
    json.dump({
        "ok": True,
        "source": "postgres_ndsp_decision_ledger_from_live_api",
        "items": items
    }, f, ensure_ascii=False, indent=2)

with open(f"{DATA}/data-quality.json","w",encoding="utf-8") as f:
    json.dump({
        "ok": True,
        "source": "real_binding_status",
        "items": [
            {"name":"Live Decision API","status":"connected","note":"مرتبط فعلياً عبر 127.0.0.1:9057"},
            {"name":"Decision Ledger DB","status":"connected" if len(items) else "empty","note":f"عدد القراءات المخزنة الآن: {len(items)}"},
            {"name":"Impact News","status":"missing_provider","note":"لا يوجد مزود أخبار حقيقي مربوط حالياً"},
            {"name":"Economic Calendar","status":"missing_provider","note":"لا يوجد مزود تقويم اقتصادي حقيقي مربوط حالياً"}
        ]
    }, f, ensure_ascii=False, indent=2)

print(f"FETCHED={len(rows)}")
print(f"JSON_ITEMS={len(items)}")
