#!/usr/bin/env python3
import json, os, time, urllib.request, urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(os.getenv("NDSP_V52_PORT", "9083"))
FRAMES = {"W1":"1w","D1":"1d","H4":"4h","H1":"1h","M15":"15m"}
CACHE = {}

def get_json(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent":"NDSP-V52"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))

def safe_float(x):
    try:
        return float(str(x).replace(",", ""))
    except Exception:
        return None

def quality(symbol):
    for url in [
        f"http://127.0.0.1:9082/api/decision/quality-live?symbol={symbol}",
        f"http://127.0.0.1:9067/api/decision/quality-live?symbol={symbol}",
    ]:
        try:
            d = get_json(url, 6)
            if isinstance(d, dict):
                d["v52_upstream_quality"] = url
                return d
        except Exception:
            pass
    return {"ok": False, "symbol": symbol, "error": "quality_live_unavailable"}

def rsi(values, period=14):
    out = [None] * len(values)
    if len(values) <= period:
        return out
    gains, losses = [], []
    for i in range(1, period + 1):
        diff = values[i] - values[i-1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    ag = sum(gains) / period
    al = sum(losses) / period
    out[period] = 100 if al == 0 else 100 - (100 / (1 + ag / al))
    for i in range(period + 1, len(values)):
        diff = values[i] - values[i-1]
        ag = (ag * (period - 1) + max(diff, 0)) / period
        al = (al * (period - 1) + max(-diff, 0)) / period
        out[i] = 100 if al == 0 else 100 - (100 / (1 + ag / al))
    return out

def nmp_one(symbol, tf, interval):
    cache_key = (symbol, tf, int(time.time() // 60))
    if cache_key in CACHE:
        return CACHE[cache_key]

    if not symbol.endswith("USDT"):
        return {
            "status": "UNSUPPORTED_SYMBOL",
            "symbol": symbol,
            "timeframe": tf,
            "level": None,
            "reason": "only Binance USDT symbols are supported in this V5.2 bridge"
        }

    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=260"
        kl = get_json(url, 12)
        closes = [float(x[4]) for x in kl]
        rs = rsi(closes)
        valid = [(i, v) for i, v in enumerate(rs) if v is not None]
        if not valid:
            return {"status":"NO_RSI", "symbol":symbol, "timeframe":tf, "level":None}

        lookback = valid[-120:]
        first = closes[max(0, len(closes)-80)]
        last = closes[-1]

        if last < first:
            idx, rv = min(lookback, key=lambda x: x[1])
            direction = "BEARISH"
        else:
            idx, rv = max(lookback, key=lambda x: x[1])
            direction = "BULLISH"

        c = kl[idx]
        res = {
            "status": "AVAILABLE",
            "symbol": symbol,
            "timeframe": tf,
            "source_interval": interval,
            "level": float(c[1]),
            "value": float(c[1]),
            "direction": direction,
            "rsi": round(float(rv), 4),
            "method": "RSI_EXTREME_MOMENTUM_CANDLE_OPEN",
            "rule": "NMP = opening price of selected momentum candle on the same timeframe",
            "source": "v52_independent_binance_klines",
            "momentum_candle": {
                "open_time_ms": int(c[0]),
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4])
            },
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        CACHE[cache_key] = res
        return res
    except Exception as e:
        return {
            "status": "ERROR",
            "symbol": symbol,
            "timeframe": tf,
            "level": None,
            "error": str(e)[:180]
        }

def nmp_all(symbol):
    return {tf: nmp_one(symbol, tf, interval) for tf, interval in FRAMES.items()}

def horizon_contract(q):
    sc = q.get("scenario") or {}
    txt = (str(sc.get("scenario_time_horizon","")) + " " + str(sc.get("scenario_directional_context",""))).lower()
    if "أسبوع" in txt or "weekly" in txt:
        return {
            "reading_horizon": "EXTENDED_WEEKLY",
            "horizon_label_ar": "أفق ممتد / أسبوعي",
            "horizon_strength": 70,
            "horizon_source": "derived_from_quality_scenario_text"
        }
    if "يومي" in txt or "daily" in txt:
        return {
            "reading_horizon": "DAILY_MEDIUM",
            "horizon_label_ar": "أفق متوسط / يومي",
            "horizon_strength": 60,
            "horizon_source": "derived_from_quality_scenario_text"
        }
    return {
        "reading_horizon": "NOT_PROVIDED",
        "horizon_label_ar": "غير مرسل من المصدر",
        "horizon_strength": None,
        "horizon_source": "missing_backend_field"
    }

def tdl_contract(q):
    sc = q.get("scenario") or {}
    corr = (
        q.get("correction_type")
        or q.get("correction_visibility")
        or sc.get("correction_type")
        or sc.get("correction_visibility")
    )
    if corr:
        return {
            "tdl_source_status": "CONNECTED",
            "correction_type": corr,
            "correction_visibility": corr,
            "correction_source": "quality-live"
        }
    return {
        "tdl_source_status": "MISSING_IN_QUALITY_LIVE",
        "correction_type": "NOT_PROVIDED",
        "correction_visibility": "NOT_PROVIDED",
        "correction_source": "missing_tdl_backend_contract",
        "note_ar": "لا يتم اختراع التصحيح من الواجهة. يحتاج الباك إند إرسال correction_type/correction_visibility."
    }

def contract(symbol):
    q = quality(symbol)
    q["nmp_timeframes"] = nmp_all(symbol)
    q["nmp_timeframes_source"] = "v52_independent_per_timeframe_no_copying"
    q.update(horizon_contract(q))
    q["tdl_contract"] = tdl_contract(q)
    q["correction_type"] = q["tdl_contract"]["correction_type"]
    q["correction_visibility"] = q["tdl_contract"]["correction_visibility"]
    q["v52_contract"] = {
        "ok": True,
        "version": "V5.2",
        "symbol": symbol,
        "governance": "NMP مستقل لكل فريم. لا نسخ بين الفريمات."
    }
    return q

class Handler(BaseHTTPRequestHandler):
    def send_json(self, code, obj):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(u.query)
        symbol = qs.get("symbol", ["BTCUSDT"])[0].upper().replace("/", "")

        if u.path == "/health":
            return self.send_json(200, {"ok": True, "service": "ndsp-v52-contract", "port": PORT})

        if u.path == "/api/decision/nmp-timeframes-live":
            return self.send_json(200, {
                "ok": True,
                "symbol": symbol,
                "nmp_timeframes": nmp_all(symbol),
                "rule": "each timeframe is computed independently"
            })

        if u.path == "/api/decision/quality-contract-v52":
            return self.send_json(200, contract(symbol))

        return self.send_json(404, {"ok": False, "error": "not_found", "path": u.path})

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
