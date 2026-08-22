#!/usr/bin/env python3
import json
import subprocess
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("/var/www/ndsp/admin/market-prices.json")
ENV_FILE = Path("/etc/ndsp/ndsp-market-data.env")
STATE_FILE = Path("/var/lib/ndsp/alpha_vantage_fx_state.json")

BINANCE_URL = "https://api.binance.com/api/v3/ticker/24hr"
FINNHUB_QUOTE_URL = "https://finnhub.io/api/v1/quote?symbol={symbol}&token={token}"
ALPHA_FX_URL = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={base}&to_currency={quote}&apikey={key}"

FINNHUB_MAP = {
    "SPX": "SPY",
    "NDX": "QQQ",
    "DJI": "DIA",
}

FX_PAIRS = [
    ("EURUSD", "EUR", "USD"),
    ("GBPUSD", "GBP", "USD"),
    ("USDJPY", "USD", "JPY"),
    ("USDCHF", "USD", "CHF"),
    ("USDCAD", "USD", "CAD"),
    ("AUDUSD", "AUD", "USD"),
    ("NZDUSD", "NZD", "USD"),
    ("EURJPY", "EUR", "JPY"),
    ("GBPJPY", "GBP", "JPY"),
    ("EURGBP", "EUR", "GBP"),
]

SNAPSHOT_FALLBACK = {
    "BTCUSDT":68000,"ETHUSDT":3600,"BNBUSDT":590,"SOLUSDT":160,"XRPUSDT":0.52,"ADAUSDT":0.45,
    "DOGEUSDT":0.16,"AVAXUSDT":38,"LINKUSDT":17,"DOTUSDT":7,"TRXUSDT":0.12,"LTCUSDT":85,
    "BCHUSDT":470,"ATOMUSDT":8,"NEARUSDT":7,"APTUSDT":9,"ARBUSDT":1.1,"OPUSDT":2.3,
    "INJUSDT":28,"UNIUSDT":10,"AAVEUSDT":95,
    "EURUSD":1.08,"GBPUSD":1.27,"USDJPY":157,"USDCHF":0.91,"USDCAD":1.37,"AUDUSD":0.66,
    "NZDUSD":0.61,"EURJPY":170,"GBPJPY":199,"EURGBP":0.85,
    "XAUUSD":2350,"XAGUSD":30,"USOIL":78,"UKOIL":82,"NG":2.7,"HG":4.5,"ZC":450,"ZW":620,"ZS":1180,
    "SPX":5300,"NDX":18500,"DJI":39000,"RUT":2100,"VIX":13.5,"DXY":105,"FTSE":8300,
    "DAX":18500,"CAC":8000,"N225":39000,"HSI":18500,
}

def load_env():
    data = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data

def load_state():
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text(errors="ignore"))
    except Exception:
        pass
    return {"idx": 0, "fx": {}}

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
    tmp.replace(STATE_FILE)

def http_json(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 NDSP","Accept":"application/json,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", errors="ignore"))

def get_assets():
    sql = """
SELECT symbol,name_ar,name_en,category,source
FROM ndsp_assets
WHERE is_active=true
ORDER BY category,symbol;
"""
    out = subprocess.check_output(
        ["sudo","-u","postgres","psql","-d","ndsp_auth","-AtF","\t","-c",sql],
        text=True,
        stderr=subprocess.DEVNULL
    )
    rows = []
    for line in out.splitlines():
        p = line.split("\t")
        if len(p) >= 5:
            rows.append({"symbol":p[0],"name_ar":p[1],"name_en":p[2],"category":p[3],"source":p[4]})
    return rows

def fetch_binance():
    data = http_json(BINANCE_URL)
    out = {}
    for x in data if isinstance(data, list) else []:
        try:
            price = float(x.get("lastPrice") or 0)
            if price <= 0:
                continue
            out[x["symbol"]] = {
                "price": price,
                "change_24h": float(x.get("priceChange") or 0),
                "change_pct": float(x.get("priceChangePercent") or 0),
                "provider": "binance_live",
            }
        except Exception:
            pass
    return out

def fetch_finnhub(symbol, token):
    url = FINNHUB_QUOTE_URL.format(
        symbol=urllib.parse.quote(symbol, safe=":"),
        token=urllib.parse.quote(token, safe="")
    )
    d = http_json(url)
    price = float(d.get("c") or 0)
    if price <= 0:
        return None
    return {
        "price": price,
        "change_24h": float(d.get("d") or 0),
        "change_pct": float(d.get("dp") or 0),
        "provider": "finnhub_live_proxy",
    }

def update_one_alpha_fx(state, key, errors):
    if not key:
        return state

    idx = int(state.get("idx", 0)) % len(FX_PAIRS)
    symbol, base, quote = FX_PAIRS[idx]
    state["idx"] = (idx + 1) % len(FX_PAIRS)
    state.setdefault("fx", {})

    url = ALPHA_FX_URL.format(
        base=urllib.parse.quote(base),
        quote=urllib.parse.quote(quote),
        key=urllib.parse.quote(key)
    )

    try:
        d = http_json(url, timeout=20)
        block = d.get("Realtime Currency Exchange Rate")
        if not block:
            info = d.get("Information") or d.get("Note") or d.get("Error Message") or "unknown_alpha_response"
            errors.append(f"alpha:{symbol}:{str(info)[:120]}")
            return state

        price = float(block.get("5. Exchange Rate") or 0)
        bid = float(block.get("8. Bid Price") or price)
        ask = float(block.get("9. Ask Price") or price)
        if price <= 0:
            return state

        state["fx"][symbol] = {
            "price": price,
            "change_24h": 0.0,
            "change_pct": 0.0,
            "provider": "alpha_vantage_fx_live_cached",
            "bid": bid,
            "ask": ask,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        errors.append(f"alpha:{symbol}:{str(e)[:120]}")

    return state

def main():
    env = load_env()
    finnhub_key = env.get("FINNHUB_API_KEY", "")
    alpha_key = env.get("ALPHAVANTAGE_API_KEY", "")
    now = datetime.now(timezone.utc).isoformat()
    assets = get_assets()
    errors = []

    try:
        binance = fetch_binance()
    except Exception as e:
        binance = {}
        errors.append("binance:" + str(e)[:120])

    state = load_state()
    state = update_one_alpha_fx(state, alpha_key, errors)
    save_state(state)

    finnhub_cache = {}
    prices = []
    live_count = 0
    fallback_count = 0

    for a in assets:
        sym = a["symbol"]
        item = None

        if a["category"] == "crypto":
            item = binance.get(sym)

        if item is None and finnhub_key and sym in FINNHUB_MAP:
            fh_symbol = FINNHUB_MAP[sym]
            if fh_symbol not in finnhub_cache:
                try:
                    finnhub_cache[fh_symbol] = fetch_finnhub(fh_symbol, finnhub_key)
                    time.sleep(0.15)
                except Exception as e:
                    finnhub_cache[fh_symbol] = None
                    errors.append(f"finnhub:{fh_symbol}:{str(e)[:100]}")
            item = finnhub_cache.get(fh_symbol)

        if item is None and sym in state.get("fx", {}):
            item = state["fx"][sym]

        if item and float(item.get("price") or 0) > 0:
            price = float(item["price"])
            change_24h = float(item.get("change_24h") or 0)
            change_pct = float(item.get("change_pct") or 0)
            provider_status = item["provider"]
            live_count += 1
        else:
            price = float(SNAPSHOT_FALLBACK.get(sym, 0))
            change_24h = 0.0
            change_pct = 0.0
            provider_status = "fallback_snapshot"
            fallback_count += 1

        prices.append({
            "symbol": sym,
            "name_ar": a["name_ar"],
            "name_en": a["name_en"],
            "category": a["category"],
            "source": a["source"],
            "price": price,
            "change_24h": change_24h,
            "change_pct": change_pct,
            "status": "active",
            "provider_status": provider_status,
            "updated_at": now,
        })

    payload = {
        "ok": True,
        "source": "ndsp_live_market_updater_binance_finnhub_alpha_safe_fx",
        "count": len(prices),
        "live_count": live_count,
        "fallback_count": fallback_count,
        "errors": errors[:20],
        "updated_at": now,
        "prices": prices,
    }

    tmp = OUT.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    tmp.replace(OUT)

if __name__ == "__main__":
    main()
