#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import time
import traceback
import urllib.parse
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except Exception:
    requests = None

PORT = 9093
ROOT = Path("/var/www/ndsp-my")
DATA_DIR = ROOT / "data"

PROJECT = "NDSP — منصة نواف لدعم القرار"
VERSION = "v3.3.lazy-timeframes"

TIMEFRAMES_V32 = ["1m", "5m", "15m", "30m", "1H", "4H", "1D", "1W", "1M"]

# واجهة المستخدم تفضل H/D/W/M، وبعض مزودي البيانات يفضلون h/d/w.
SOURCE_TF_MAP = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1H": "1h",
    "4H": "4h",
    "1D": "1d",
    "1W": "1w",
    "1M": "1M",
}

FALLBACK_ASSETS = [
    ("BTCUSDT", "بيتكوين", "Bitcoin", "CRYPTO"),
    ("ETHUSDT", "إيثريوم", "Ethereum", "CRYPTO"),
    ("SOLUSDT", "سولانا", "Solana", "CRYPTO"),
    ("XRPUSDT", "ريبل", "XRP", "CRYPTO"),
    ("BNBUSDT", "BNB", "BNB", "CRYPTO"),
    ("ADAUSDT", "كاردانو", "Cardano", "CRYPTO"),
    ("DOGEUSDT", "دوجكوين", "Dogecoin", "CRYPTO"),
    ("AVAXUSDT", "أفالانش", "Avalanche", "CRYPTO"),
    ("LINKUSDT", "تشين لينك", "Chainlink", "CRYPTO"),
    ("DOTUSDT", "بولكادوت", "Polkadot", "CRYPTO"),
    ("LTCUSDT", "لايتكوين", "Litecoin", "CRYPTO"),
    ("BCHUSDT", "بيتكوين كاش", "Bitcoin Cash", "CRYPTO"),

    ("XAUUSD", "الذهب", "Gold", "METAL"),
    ("XAGUSD", "الفضة", "Silver", "METAL"),

    ("EURUSD", "اليورو / دولار", "EUR/USD", "FX"),
    ("GBPUSD", "الإسترليني / دولار", "GBP/USD", "FX"),
    ("USDJPY", "الدولار / ين", "USD/JPY", "FX"),
    ("USDCHF", "الدولار / فرنك", "USD/CHF", "FX"),
    ("USDCAD", "الدولار / كندي", "USD/CAD", "FX"),
    ("AUDUSD", "الأسترالي / دولار", "AUD/USD", "FX"),

    ("USOIL", "النفط الأمريكي", "WTI Crude Oil", "COMMODITY"),
    ("UKOIL", "برنت", "Brent Crude Oil", "COMMODITY"),

    ("US500", "إس آند بي 500", "S&P 500", "INDEX"),
    ("NAS100", "ناسداك 100", "Nasdaq 100", "INDEX"),
    ("US30", "داو جونز", "Dow Jones", "INDEX"),
    ("GER40", "داكس الألماني", "DAX 40", "INDEX"),
    ("DXY", "مؤشر الدولار", "US Dollar Index", "INDEX"),
]

CACHE = {}
CACHE_TTL = 25

def now_iso():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")

def cache_get(key):
    item = CACHE.get(key)
    if not item:
        return None
    ts, data = item
    if time.time() - ts > CACHE_TTL:
        return None
    return data

def cache_set(key, data):
    CACHE[key] = (time.time(), data)
    return data

def safe_read_json(path: Path, default):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default

def normalize_asset_row(row):
    if not isinstance(row, dict):
        return None
    symbol = str(row.get("symbol") or row.get("asset") or "").upper().strip()
    if not symbol:
        return None
    return {
        "symbol": symbol,
        "name_ar": row.get("name_ar") or row.get("name") or symbol,
        "name_en": row.get("name_en") or row.get("english_name") or symbol,
        "market": row.get("market") or row.get("category") or "UNSPECIFIED",
        "live_data": bool(row.get("live_data", True)),
        "live_price": row.get("live_price") or row.get("price"),
        "decision_quality": row.get("decision_quality"),
        "scenario_state": row.get("scenario_state") or row.get("state") or "UNDER_MONITORING",
        "directional_context": row.get("directional_context") or row.get("directional_bias") or "غير مرسل من المصدر الحي",
        "nmp_status": ((row.get("nmp") or {}).get("status") if isinstance(row.get("nmp"), dict) else row.get("nmp_status")) or "UNAVAILABLE",
        "updated_at": row.get("updated_at") or now_iso(),
    }

def load_assets():
    """
    يدمج أصول المصدر الحي مع قائمة NDSP الأساسية.
    لا يولّد أسعارًا وهمية:
    - إذا كان الأصل موجودًا في /data/command-center-real.json نستخدم بياناته الحية.
    - إذا لم يكن موجودًا نعرضه كأصل قابل للاختيار live_data=False حتى يطلبه المستخدم.
    """
    data = safe_read_json(DATA_DIR / "command-center-real.json", {})
    rows = data.get("items") if isinstance(data, dict) else None

    by_symbol = {}
    live_order = []

    if isinstance(rows, list):
        for r in rows:
            a = normalize_asset_row(r)
            if not a:
                continue
            sym = a["symbol"]
            by_symbol[sym] = a
            if sym not in live_order:
                live_order.append(sym)

    fallback_order = []
    for sym, ar, en, market in FALLBACK_ASSETS:
        fallback_order.append(sym)
        if sym not in by_symbol:
            by_symbol[sym] = {
                "symbol": sym,
                "name_ar": ar,
                "name_en": en,
                "market": market,
                "live_data": False,
                "live_price": None,
                "decision_quality": None,
                "scenario_state": "UNDER_MONITORING",
                "directional_context": "الأصل موجود في كتالوج NDSP، وتُحمّل قراءته عند الاختيار.",
                "nmp_status": "UNAVAILABLE",
                "updated_at": now_iso(),
            }
        else:
            # ثبّت الاسم/السوق من الكتالوج إذا كانت ناقصة، ولا تلمس السعر الحي.
            by_symbol[sym].setdefault("name_ar", ar)
            by_symbol[sym].setdefault("name_en", en)
            by_symbol[sym].setdefault("market", market)

    ordered = []

    # نعرض الكتالوج الأساسي أولًا بترتيب مؤسسي ثابت.
    for sym in fallback_order:
        if sym in by_symbol:
            ordered.append(by_symbol[sym])

    # ثم نضيف أي أصول إضافية جاءت من المصدر الحي ولم تكن في الكتالوج.
    for sym in live_order:
        if sym not in fallback_order and sym in by_symbol:
            ordered.append(by_symbol[sym])

    return ordered


def http_get_json(url, timeout=4):
    key = "url:" + url
    cached = cache_get(key)
    if cached is not None:
        return cached

    if requests is None:
        return None

    try:
        r = requests.get(
            url,
            timeout=timeout,
            headers={"User-Agent": "NDSP-V3-Lazy-Gateway/1.0"},
            verify=False,
        )
        if r.status_code != 200:
            return None
        data = r.json()
        return cache_set(key, data)
    except Exception:
        return None

def extract_quality_payload(raw):
    if not isinstance(raw, dict):
        return {}
    if isinstance(raw.get("data"), dict):
        return raw["data"]
    return raw

def find_nested(d, keys):
    if not isinstance(d, dict):
        return None
    for k in keys:
        if k in d and d.get(k) not in (None, ""):
            return d.get(k)
    for v in d.values():
        if isinstance(v, dict):
            found = find_nested(v, keys)
            if found not in (None, ""):
                return found
    return None

def nmp_from_payload(payload):
    nmp = payload.get("nmp") if isinstance(payload, dict) else None
    if isinstance(nmp, dict):
        value = nmp.get("value") or nmp.get("level") or nmp.get("price")
        status = nmp.get("status") or ("AVAILABLE" if value not in (None, "") else "UNAVAILABLE")
        return {
            "status": status,
            "value": value,
            "source": nmp.get("source") or "quality-live",
            "note": nmp.get("note") or ("قيمة NMP مرسلة من المصدر الحي." if value not in (None, "") else "قيمة NMP غير مرسلة من المصدر الحي. لم يتم توليدها من الواجهة."),
        }

    value = find_nested(payload, ["nmp_value", "nmp_level", "nawaf_meet_point", "nmp"])
    return {
        "status": "AVAILABLE" if value not in (None, "") else "UNAVAILABLE",
        "value": value,
        "source": "quality-live",
        "note": "قيمة NMP مرسلة من المصدر الحي." if value not in (None, "") else "قيمة NMP غير مرسلة من المصدر الحي. لم يتم توليدها من الواجهة.",
    }

def scenario_from_payload(payload):
    scenario = payload.get("scenario") if isinstance(payload, dict) else {}
    if not isinstance(scenario, dict):
        scenario = {}
    return {
        "scenario_state": scenario.get("scenario_state") or payload.get("scenario_state") or "UNDER_MONITORING",
        "directional_context": scenario.get("scenario_directional_context") or payload.get("directional_context") or payload.get("directional_bias") or "غير مرسل من المصدر الحي",
        "activation_level": scenario.get("scenario_activation_level") or payload.get("activation_level"),
        "arrival_level": scenario.get("scenario_arrival_level") or payload.get("arrival_level"),
        "review_zone": scenario.get("scenario_review_zone") or payload.get("review_zone"),
        "invalidation_level": scenario.get("scenario_invalidation_level") or payload.get("invalidation_level"),
        "confidence_band": scenario.get("scenario_confidence_band") or payload.get("confidence_band"),
        "time_horizon": scenario.get("scenario_time_horizon") or payload.get("time_horizon"),
        "risk_note": scenario.get("scenario_risk_note") or payload.get("risk_note"),
    }

def fetch_quality(symbol, timeframe=None):
    symbol = (symbol or "BTCUSDT").upper().strip()
    tf = SOURCE_TF_MAP.get(timeframe, timeframe)

    params = {"symbol": symbol}
    if tf:
        params["timeframe"] = tf

    qs = urllib.parse.urlencode(params)
    url = "https://api.ndsp.app/api/decision/quality-live?" + qs
    raw = http_get_json(url, timeout=4)
    payload = extract_quality_payload(raw)

    if not payload:
        return {
            "ok": False,
            "symbol": symbol,
            "timeframe": timeframe,
            "source_timeframe": None,
            "source_status": "UNAVAILABLE",
            "source_note": "تعذر جلب قراءة المصدر الحي ضمن المهلة.",
            "scenario": scenario_from_payload({}),
            "nmp": nmp_from_payload({}),
            "raw_available": False,
            "updated_at": now_iso(),
        }

    instrument = payload.get("instrument") if isinstance(payload.get("instrument"), dict) else {}
    scenario = scenario_from_payload(payload)
    nmp = nmp_from_payload(payload)

    return {
        "ok": True,
        "symbol": symbol,
        "timeframe": timeframe,
        "source_timeframe": instrument.get("timeframe") or payload.get("source_timeframe") or "UNSPECIFIED",
        "source_status": "LIVE",
        "source_note": "قراءة مباشرة من quality-live. إذا ظهر UNSPECIFIED فهذا يعني أن المصدر لم يثبت الفريم صراحة.",
        "live_price": instrument.get("live_price") or payload.get("live_price") or payload.get("price"),
        "decision_quality": payload.get("decision_quality") or payload.get("quality"),
        "scenario": scenario,
        "nmp": nmp,
        "raw_available": True,
        "updated_at": payload.get("updated_at") or now_iso(),
    }

def selected_asset(symbol):
    assets = load_assets()
    symbol = (symbol or "BTCUSDT").upper().strip()
    for a in assets:
        if a["symbol"] == symbol:
            return a
    return assets[0] if assets else {"symbol": symbol, "name_ar": symbol, "name_en": symbol, "market": "UNSPECIFIED"}

def snapshot(symbol, timeframe):
    symbol = (symbol or "BTCUSDT").upper().strip()
    timeframe = timeframe if timeframe in TIMEFRAMES_V32 else "1D"

    assets = load_assets()
    asset = selected_asset(symbol)
    q = fetch_quality(symbol, timeframe)

    tf_rows = []
    for tf in TIMEFRAMES_V32:
        if tf == timeframe:
            tf_rows.append({
                "timeframe": tf,
                "status": q.get("source_status"),
                "source_timeframe": q.get("source_timeframe"),
                "source_note": q.get("source_note"),
                "nmp": q.get("nmp"),
                "scenario": q.get("scenario"),
                "lazy_loaded": True,
            })
        else:
            tf_rows.append({
                "timeframe": tf,
                "status": "LAZY",
                "source_timeframe": None,
                "source_note": "لا يتم تحميل هذا الفريم داخل snapshot. يتم تحميله عند اختياره فقط.",
                "nmp": {
                    "status": "NOT_REQUESTED",
                    "value": None,
                    "source": "lazy-loading",
                    "note": "الفريم لم يطلب بعد.",
                },
                "scenario": None,
                "lazy_loaded": False,
            })

    return {
        "ok": True,
        "version": VERSION,
        "project": PROJECT,
        "generated_at": now_iso(),
        "selected_symbol": symbol,
        "selected_timeframe": timeframe,
        "catalog_count": len(assets),
        "live_assets_count": len([a for a in assets if a.get("live_data")]),
        "assets": assets,
        "selected_asset": asset,
        "selected_reading": q,
        "nmp": q.get("nmp"),
        "scenario": q.get("scenario"),
        "timeframes": tf_rows,
        "timeframe_options": TIMEFRAMES_V32,
        "architecture": {
            "mode": "lazy_timeframes",
            "snapshot_policy": "loads_selected_symbol_and_selected_timeframe_only",
            "no_fanout_all_timeframes": True,
            "no_fake_nmp": True,
        },
    }

def timeframe_matrix(symbol):
    symbol = (symbol or "BTCUSDT").upper().strip()
    rows = []

    # endpoint منفصل، لذلك مسموح يجيب كل الفريمات، لكن بالتوازي وبمهلة قصيرة.
    with ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(fetch_quality, symbol, tf): tf for tf in TIMEFRAMES_V32}
        for fut in as_completed(futs, timeout=20):
            tf = futs[fut]
            try:
                rows.append(fut.result(timeout=1))
            except Exception:
                rows.append({
                    "ok": False,
                    "symbol": symbol,
                    "timeframe": tf,
                    "source_status": "TIMEOUT",
                    "source_note": "انتهت مهلة تحميل هذا الفريم.",
                    "scenario": scenario_from_payload({}),
                    "nmp": nmp_from_payload({}),
                    "updated_at": now_iso(),
                })

    order = {tf: i for i, tf in enumerate(TIMEFRAMES_V32)}
    rows.sort(key=lambda x: order.get(x.get("timeframe"), 999))

    return {
        "ok": True,
        "version": VERSION,
        "symbol": symbol,
        "generated_at": now_iso(),
        "timeframes": rows,
        "timeframe_options": TIMEFRAMES_V32,
        "mode": "separate_matrix_endpoint",
    }

def completed_decisions():
    data = safe_read_json(DATA_DIR / "completed-decisions.json", {"ok": True, "items": []})
    if not isinstance(data, dict):
        data = {"ok": True, "items": []}
    data.setdefault("ok", True)
    data.setdefault("items", [])
    return data

def health():
    return {
        "ok": True,
        "service": "ndsp-v3-portal-gateway",
        "version": VERSION,
        "port": PORT,
        "timeframes": TIMEFRAMES_V32,
        "mode": "lazy_timeframes",
        "updated_at": now_iso(),
    }

def send_json(handler, data, status=200, head_only=False):
    body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Cache-Control", "no-store, no-cache, max-age=0, must-revalidate")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    if not head_only:
        handler.wfile.write(body)

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def do_HEAD(self):
        self.handle_request(head_only=True)

    def do_GET(self):
        self.handle_request(head_only=False)

    def handle_request(self, head_only=False):
        try:
            parsed = urllib.parse.urlparse(self.path)
            path = parsed.path
            qs = urllib.parse.parse_qs(parsed.query)
            symbol = (qs.get("symbol") or ["BTCUSDT"])[0].upper().strip()
            timeframe = (qs.get("timeframe") or ["1D"])[0].strip()

            if path in ("/api/v3/portal/health", "/health"):
                return send_json(self, health(), head_only=head_only)

            if path == "/api/v3/portal/assets":
                assets = load_assets()
                return send_json(self, {
                    "ok": True,
                    "version": VERSION,
                    "catalog_count": len(assets),
                    "live_assets_count": len([a for a in assets if a.get("live_data")]),
                    "assets": assets,
                    "updated_at": now_iso(),
                }, head_only=head_only)

            if path == "/api/v3/portal/snapshot":
                return send_json(self, snapshot(symbol, timeframe), head_only=head_only)

            if path in ("/api/v3/portal/timeframe", "/api/v3/portal/timeframe-snapshot"):
                if timeframe not in TIMEFRAMES_V32:
                    return send_json(self, {
                        "ok": False,
                        "error": "UNSUPPORTED_TIMEFRAME",
                        "allowed": TIMEFRAMES_V32,
                    }, status=400, head_only=head_only)
                return send_json(self, {
                    "ok": True,
                    "version": VERSION,
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "reading": fetch_quality(symbol, timeframe),
                    "updated_at": now_iso(),
                }, head_only=head_only)

            if path == "/api/v3/portal/timeframe-matrix":
                return send_json(self, timeframe_matrix(symbol), head_only=head_only)

            if path == "/api/v3/portal/nmp":
                if timeframe not in TIMEFRAMES_V32:
                    timeframe = "1D"
                q = fetch_quality(symbol, timeframe)
                return send_json(self, {
                    "ok": True,
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "nmp": q.get("nmp"),
                    "updated_at": now_iso(),
                }, head_only=head_only)

            if path == "/api/v3/portal/completed":
                return send_json(self, completed_decisions(), head_only=head_only)

            return send_json(self, {
                "ok": False,
                "error": "NOT_FOUND",
                "path": path,
                "version": VERSION,
            }, status=404, head_only=head_only)

        except Exception as e:
            return send_json(self, {
                "ok": False,
                "error": "GATEWAY_EXCEPTION",
                "message": str(e),
                "trace": traceback.format_exc()[-2000:],
                "version": VERSION,
            }, status=500, head_only=head_only)

def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    print(f"NDSP V3.3 Lazy Gateway listening on 127.0.0.1:{PORT}", flush=True)
    server.serve_forever()

if __name__ == "__main__":
    main()
