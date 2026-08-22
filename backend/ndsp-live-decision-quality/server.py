#!/usr/bin/env python3
# NDSP Live Decision Quality Bridge
# Crypto: Binance public OHLC
# FX / Commodities / Indices: External chart fallback
# No secrets in this file.

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import urllib.request
import urllib.parse
import json
import time
import math

app = FastAPI(title="NDSP Live Decision Quality Bridge", version="20")

BINANCE_BASE = "https://api.binance.com"
YAHOO_BASE = "https://query1.finance.yahoo.com/v8/finance/chart"

EXTERNAL_SYMBOLS = {
    # Forex
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "AUDUSD": "AUDUSD=X",
    "USDJPY": "JPY=X",
    "USDCAD": "CAD=X",
    "USDCHF": "CHF=X",

    # Metals / commodities
    "XAUUSD": "GC=F",
    "XAGUSD": "SI=F",
    "USOIL": "CL=F",
    "UKOIL": "BZ=F",
    "NG": "NG=F",
    "ZC": "ZC=F",
    "ZS": "ZS=F",
    "ZW": "ZW=F",

    # Indices
    "SPX": "^GSPC",
    "NDX": "^NDX",
    "DXY": "DX-Y.NYB",
    "DJI": "^DJI",
    "VIX": "^VIX",
    "CAC": "^FCHI",
    "DAX": "^GDAXI",
}

def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def clean_symbol(symbol: str) -> str:
    return str(symbol or "ETHUSDT").upper().replace("/", "").replace(" ", "").strip()

def market_type(symbol: str) -> str:
    s = clean_symbol(symbol)
    if s.endswith("USDT"):
        return "crypto"
    if s in {"EURUSD","GBPUSD","AUDUSD","USDJPY","USDCAD","USDCHF"}:
        return "forex"
    if s in {"XAUUSD","XAGUSD","USOIL","UKOIL","NG","ZC","ZS","ZW"}:
        return "commodity"
    if s in {"SPX","NDX","DXY","DJI","VIX","CAC","DAX"}:
        return "index"
    return "unknown"

def fetch_json(url: str, timeout: int = 8):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 NDSP-Live-Bridge/20",
            "Accept": "application/json,text/plain,*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode("utf-8", errors="replace")
    return json.loads(raw)

def fmt_price(v):
    try:
        x = float(v)
    except Exception:
        return "غير معلن"

    ax = abs(x)
    if ax >= 1000:
        return f"{x:,.2f}"
    if ax >= 100:
        return f"{x:,.2f}"
    if ax >= 10:
        return f"{x:,.3f}"
    if ax >= 1:
        return f"{x:,.4f}"
    return f"{x:,.6f}"

def safe_float(v):
    try:
        if v is None:
            return None
        x = float(v)
        if math.isfinite(x):
            return x
    except Exception:
        pass
    return None

def closed_binance_rows(rows):
    now_ms = int(time.time() * 1000)
    closed = [k for k in rows if int(k[6]) <= now_ms]
    return closed if len(closed) >= 60 else rows

def get_binance_klines(symbol, interval, limit=180):
    qs = urllib.parse.urlencode({"symbol": symbol, "interval": interval, "limit": limit})
    data = fetch_json(f"{BINANCE_BASE}/api/v3/klines?{qs}", timeout=8)
    data = closed_binance_rows(data)

    highs = [float(k[2]) for k in data]
    lows = [float(k[3]) for k in data]
    closes = [float(k[4]) for k in data]
    vols = [float(k[5]) for k in data]
    close_times = [int(k[6]) for k in data]

    return {"highs": highs, "lows": lows, "closes": closes, "vols": vols, "close_times": close_times, "provider": "binance"}

def aggregate_ohlc(k, group=4):
    highs = k["highs"]
    lows = k["lows"]
    closes = k["closes"]
    vols = k["vols"]
    times = k["close_times"]

    n = len(closes)
    if n < group:
        return k

    ranges = []
    i = n
    while i - group >= 0:
        ranges.append((i - group, i))
        i -= group
    ranges.reverse()

    ah, al, ac, av, at = [], [], [], [], []
    for a, b in ranges:
        ah.append(max(highs[a:b]))
        al.append(min(lows[a:b]))
        ac.append(closes[b - 1])
        av.append(sum(vols[a:b]))
        at.append(times[b - 1])

    return {"highs": ah, "lows": al, "closes": ac, "vols": av, "close_times": at, "provider": k.get("provider", "external_chart")}

def get_external_klines(symbol, interval, limit=180):
    s = clean_symbol(symbol)
    ys = EXTERNAL_SYMBOLS.get(s)
    if not ys:
        raise ValueError(f"NO_EXTERNAL_SYMBOL_MAPPING:{s}")

    if interval == "1d":
        y_interval = "1d"
        y_range = "5y" if int(limit or 0) > 400 else "1y"
    elif interval == "4h":
        y_interval = "1h"
        y_range = "60d"
    else:
        y_interval = "1h"
        y_range = "30d"

    enc = urllib.parse.quote(ys, safe="")
    qs = urllib.parse.urlencode({
        "range": y_range,
        "interval": y_interval,
        "includePrePost": "false",
        "events": "div,splits",
    })

    data = fetch_json(f"{YAHOO_BASE}/{enc}?{qs}", timeout=10)
    result = (((data or {}).get("chart") or {}).get("result") or [None])[0]
    if not result:
        raise ValueError(f"EXTERNAL_PROVIDER_EMPTY:{s}")

    timestamps = result.get("timestamp") or []
    quote = (((result.get("indicators") or {}).get("quote") or [None])[0]) or {}

    opens = quote.get("open") or []
    highs0 = quote.get("high") or []
    lows0 = quote.get("low") or []
    closes0 = quote.get("close") or []
    vols0 = quote.get("volume") or []

    highs, lows, closes, vols, close_times = [], [], [], [], []

    for t, o, h, l, c, v in zip(timestamps, opens, highs0, lows0, closes0, vols0):
        h = safe_float(h)
        l = safe_float(l)
        c = safe_float(c)
        if h is None or l is None or c is None:
            continue

        highs.append(h)
        lows.append(l)
        closes.append(c)
        vols.append(float(v or 0))
        close_times.append(int(t) * 1000)

    if len(closes) < 40:
        raise ValueError(f"EXTERNAL_PROVIDER_INSUFFICIENT_BARS:{s}:{len(closes)}")

    out = {
        "highs": highs[-limit:],
        "lows": lows[-limit:],
        "closes": closes[-limit:],
        "vols": vols[-limit:],
        "close_times": close_times[-limit:],
        "provider": "external_chart",
    }

    if interval == "4h":
        out = aggregate_ohlc(out, group=4)

    return out

def get_klines(symbol, interval, limit=180):
    s = clean_symbol(symbol)
    if s.endswith("USDT"):
        return get_binance_klines(s, interval, limit)
    return get_external_klines(s, interval, limit)

def ema(values, period):
    values = [float(x) for x in values if x is not None]
    if not values:
        return 0.0
    if len(values) < period:
        return sum(values) / len(values)

    k = 2 / (period + 1)
    e = sum(values[:period]) / period
    for x in values[period:]:
        e = (x * k) + (e * (1 - k))
    return e

def rsi(values, period=14):
    values = [float(x) for x in values if x is not None]
    if len(values) <= period:
        return 50.0

    gains = []
    losses = []
    start = len(values) - period
    for i in range(start, len(values)):
        d = values[i] - values[i - 1]
        if d >= 0:
            gains.append(d)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(d))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def atr(highs, lows, closes, period=14):
    if len(closes) <= period:
        return 0.0

    trs = []
    for i in range(1, len(closes)):
        h = highs[i]
        l = lows[i]
        pc = closes[i - 1]
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))

    use = trs[-period:]
    if not use:
        return 0.0
    return sum(use) / len(use)

def analyze_interval(symbol, interval):
    k = get_klines(symbol, interval, limit=180)
    closes = k["closes"]
    highs = k["highs"]
    lows = k["lows"]

    close = float(closes[-1])
    e20 = ema(closes, 20)
    e50 = ema(closes, 50)
    rrsi = rsi(closes, 14)
    aatr = atr(highs, lows, closes, 14)

    if close > e20 > e50 and rrsi >= 50:
        direction = "bullish"
    elif close < e20 < e50 and rrsi <= 50:
        direction = "bearish"
    else:
        direction = "neutral"

    prev_24 = closes[-25] if len(closes) >= 25 else None

    return {
        "interval": interval,
        "close": close,
        "ema20": e20,
        "ema50": e50,
        "rsi": rrsi,
        "atr": aatr,
        "direction": direction,
        "provider": k.get("provider", "unknown"),
        "momentum_price": close,
        "momentum_close_time": (k.get("close_times") or [None])[-1],
        "prev_24_close": prev_24,
    }

def direction_ar(direction):
    if direction == "bullish":
        return "زخم صاعد"
    if direction == "bearish":
        return "ضغط هابط"
    return "تذبذب بيني"

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

def dynamic_quality_score(direction, bull, bear, h1, h4, d1, atr_pct):
    """
    نموذج جودة موسّع 0-95:
    - لا يحوّل القراءة إلى توصية تنفيذ.
    - يوسّع الفروقات بين الأصول بدل ضغطها حول 50.
    - يرفع الجودة عند اتفاق الإطارات والزخم والتماسك.
    - يخفض الجودة عند التضارب أو التذبذب العالي.
    """
    rsi4 = float(h4.get("rsi") or 50)
    close4 = float(h4.get("close") or 0)
    ema20_4 = float(h4.get("ema20") or close4 or 0)
    ema50_4 = float(h4.get("ema50") or close4 or 0)

    dirs = [h1.get("direction"), h4.get("direction"), d1.get("direction")]
    agreement = max(bull, bear)

    score = 48.0

    # 1) اتفاق الإطارات
    if agreement == 3:
        score += 22
    elif agreement == 2:
        score += 13
    elif agreement == 1:
        score -= 5

    # 2) ترتيب الاتجاه
    if direction == "bullish":
        score += 7
        if rsi4 >= 52:
            score += min(12, (rsi4 - 52) * 0.75)
        if rsi4 >= 76:
            score -= 8
    elif direction == "bearish":
        score += 7
        if rsi4 <= 48:
            score += min(12, (48 - rsi4) * 0.75)
        if rsi4 <= 24:
            score -= 8
    else:
        # الحياد لا يبقى رقمًا واحدًا؛ يتذبذب حسب بعد الزخم عن 50.
        score += min(8, abs(rsi4 - 50) * 0.45)
        score -= 4

    # 3) تماسك المتوسطات على 4H
    if close4 and ema20_4 and ema50_4:
        ema_gap = abs(ema20_4 - ema50_4) / close4 * 100
        price_gap = abs(close4 - ema20_4) / close4 * 100

        score += min(10, ema_gap * 2.8)
        score += min(7, price_gap * 1.6)

        if direction == "bullish" and close4 > ema20_4 > ema50_4:
            score += 6
        elif direction == "bearish" and close4 < ema20_4 < ema50_4:
            score += 6

    # 4) توافق 4H مع D1 أهم من توافق H1 وحده
    if h4.get("direction") == d1.get("direction") and h4.get("direction") in ("bullish", "bearish"):
        score += 7
    elif h1.get("direction") != d1.get("direction"):
        score -= 4

    # 5) التذبذب
    atr_pct = float(atr_pct or 0)
    if atr_pct >= 6:
        score -= 12
    elif atr_pct >= 4:
        score -= 8
    elif atr_pct >= 2.5:
        score -= 4
    elif 0.35 <= atr_pct <= 1.8:
        score += 3
    elif atr_pct > 0 and atr_pct < 0.25:
        score -= 2

    return int(round(clamp(score, 20, 95)))

def quality_labels(score):
    if score >= 83:
        return "عالية جدًا", "عالية جدًا"
    if score >= 72:
        return "مرتفع", "قوية"
    if score >= 62:
        return "متوسط", "متوسطة"
    if score >= 54:
        return "منخفض", "ضعيفة/متوسطة"
    if score >= 40:
        return "منخفض", "تحتاج تأكيد"
    return "غير ناضجة", "غير ناضجة"

def dynamic_decision_texts(direction, bull, bear, h1, h4, d1, atr_pct, quality):
    rsi4 = float(h4.get("rsi") or 50)
    h1d = h1.get("direction")
    h4d = h4.get("direction")
    d1d = d1.get("direction")

    mixed = len(set([h1d, h4d, d1d])) >= 2

    if direction == "bullish":
        if quality >= 72:
            return "زخم صاعد مؤكد", "أفق صاعد نشط", "استمرار المتابعة بشرط ثبات السعر فوق منطقة المراجعة."
        return "ميل صاعد تحت التحقق", "مراقبة اختراق", "انتظار اختراق التفعيل قبل رفع جودة القراءة."

    if direction == "bearish":
        if quality >= 72:
            return "ضغط هابط مؤكد", "أفق هابط نشط", "استمرار المتابعة بشرط بقاء السعر دون منطقة المراجعة."
        return "ميل هابط تحت التحقق", "مراقبة كسر", "انتظار كسر التفعيل قبل رفع جودة القراءة."

    # حالة محايدة، لكن بوصف مختلف حسب السبب.
    if mixed:
        if h4d == "bullish":
            state = "تذبذب بيني · زخم 4H صاعد"
            horizon = "مراقبة اختراق"
            caution = "الإطار 4H يميل للصعود لكن باقي الإطارات غير مصطفة."
        elif h4d == "bearish":
            state = "تذبذب بيني · ضغط 4H هابط"
            horizon = "مراقبة كسر"
            caution = "الإطار 4H يميل للهبوط لكن باقي الإطارات غير مصطفة."
        else:
            state = "تذبذب بيني · تضارب الإطارات"
            horizon = "مراقبة حيادية"
            caution = "لا يوجد اصطفاف كاف بين H1 و4H وD1."
    elif rsi4 >= 58:
        state = "تذبذب بيني · زخم علوي"
        horizon = "مراقبة اختراق"
        caution = "الزخم مرتفع نسبيًا لكن الاتجاه لم يتأكد بعد."
    elif rsi4 <= 42:
        state = "تذبذب بيني · ضغط سفلي"
        horizon = "مراقبة كسر"
        caution = "الزخم منخفض نسبيًا لكن الاتجاه لم يتأكد بعد."
    elif float(atr_pct or 0) >= 2.5:
        state = "تذبذب واسع · مخاطرة أعلى"
        horizon = "مراقبة موسعة"
        caution = "التذبذب مرتفع؛ لا توجد قراءة اتجاهية كافية."
    else:
        state = "تذبذب بيني · قرب المتوسط"
        horizon = "مراقبة توازن"
        caution = "السعر قريب من نطاق التوازن ولا يوجد اصطفاف اتجاهي واضح."

    return state, horizon, caution

def build_error(symbol, reason):
    s = clean_symbol(symbol)
    return {
        "ok": True,
        "source_mode": "python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality",
        "project": "NDSP — منصة نواف لدعم القرار",
        "package": "free",
        "instrument": {
            "symbol": s,
            "market": market_type(s).upper(),
            "timeframe": "UNSPECIFIED",
            "live_price": 0,
        },
        "scenario": {
            "scenario_state": "DATA_SOURCE_UNAVAILABLE",
            "scenario_directional_context": "غير معلن",
            "scenario_activation_level": None,
            "scenario_arrival_level": None,
            "scenario_review_zone": "",
            "scenario_invalidation_level": None,
            "scenario_confidence_band": "غير معلن",
            "scenario_time_horizon": "أفق مراقبة",
            "scenario_risk_note": "تعذر جلب السعر الحي من مزود السوق.",
            "scenario_last_updated": now_iso(),
        },
        "allowed_public_outputs": {
            "directional_bias": "غير معلن",
            "reading_horizon": "أفق مراقبة",
            "horizon_strength": "تحتاج تأكيد",
            "market_state": "غير معلن",
            "decision_quality": 50,
            "caution_reason": "تعذر جلب السعر الحي من مزود السوق.",
            "sanitized_summary": "قراءة سياقية صادرة من الباك إند؛ مصدر البيانات غير متصل لهذا الأصل.",
        },
        "live_price_bound": False,
        "data_provider": "unavailable",
        "provider_error": str(reason),
        "generated_at": now_iso(),
    }

def build_response(symbol):
    s = clean_symbol(symbol)

    try:
        h1 = analyze_interval(s, "1h")
        h4 = analyze_interval(s, "4h")
        d1 = analyze_interval(s, "1d")

        provider = h4.get("provider") or h1.get("provider") or "unknown"

        live_price = h1["close"] or h4["close"]
        momentum_price_4h = h4["momentum_price"]
        momentum_close_time_4h = h4["momentum_close_time"]

        atr4 = h4["atr"] or (live_price * 0.01)
        rsi4 = h4["rsi"]

        dirs = [h1["direction"], h4["direction"], d1["direction"]]
        bull = dirs.count("bullish")
        bear = dirs.count("bearish")

        if bull >= 2:
            direction = "bullish"
        elif bear >= 2:
            direction = "bearish"
        else:
            direction = "neutral"

        if h1.get("prev_24_close"):
            change_24 = ((live_price - h1["prev_24_close"]) / h1["prev_24_close"]) * 100
        else:
            change_24 = 0.0

        if direction == "bullish":
            activation = live_price + (atr4 * 0.95)
            arrival = live_price + (atr4 * 1.90)
            review = live_price
            invalidation = live_price - (atr4 * 0.95)
            horizon = "أفق قصير/متوسط"
            caution = "انتظار اختراق التفعيل مع مراقبة التذبذب."
        elif direction == "bearish":
            activation = live_price - (atr4 * 0.95)
            arrival = live_price - (atr4 * 1.90)
            review = live_price
            invalidation = live_price + (atr4 * 0.95)
            horizon = "أفق قصير/متوسط"
            caution = "انتظار كسر التفعيل مع مراقبة التذبذب."
        else:
            activation = live_price + (atr4 * 0.95)
            arrival = live_price + (atr4 * 1.90)
            review = live_price
            invalidation = live_price - (atr4 * 0.95)
            horizon = "أفق مراقبة"
            caution = "انتظار اختراق التفعيل."

        atr_pct = (atr4 / live_price * 100) if live_price else 0

        quality = dynamic_quality_score(direction, bull, bear, h1, h4, d1, atr_pct)
        confidence, strength = quality_labels(quality)

        market_state, horizon, caution = dynamic_decision_texts(
            direction, bull, bear, h1, h4, d1, atr_pct, quality
        )

        summary = (
            f"قراءة سعرية حية على {s}: السعر {fmt_price(live_price)}، "
            f"تغير 24 ساعة {change_24:.3f}%. "
            f"زخم 4H عند سعر {fmt_price(momentum_price_4h)}، "
            f"والسياق {market_state}."
        )

        return {
            "ok": True,
            "source_mode": "python_decision_governed_tdl_v2 + live_price_technical_bridge_v23_expanded_quality",
            "project": "NDSP — منصة نواف لدعم القرار",
            "package": "free",
            "instrument": {
                "symbol": s,
                "market": market_type(s).upper(),
                "timeframe": "UNSPECIFIED",
                "live_price": live_price,
            },
            "scenario": {
                "scenario_state": "UNDER_MONITORING",
                "scenario_directional_context": market_state,
                "scenario_activation_level": fmt_price(activation),
                "scenario_arrival_level": fmt_price(arrival),
                "scenario_review_zone": fmt_price(review),
                "scenario_invalidation_level": fmt_price(invalidation),
                "scenario_confidence_band": confidence,
                "scenario_time_horizon": horizon,
                "scenario_risk_note": caution,
                "scenario_last_updated": now_iso(),
            },
            "allowed_public_outputs": {
                "directional_bias": market_state,
                "reading_horizon": horizon,
                "horizon_strength": strength,
                "market_state": market_state,
                "decision_quality": quality,
                "caution_reason": caution,
                "sanitized_summary": summary,
            },
            "live_market_analysis": {
                "provider": provider,
                "price": live_price,
                "price_change_24h_pct": change_24,
                "atr_4h": atr4,
                "atr_4h_pct": atr_pct,
                "rsi_4h": rsi4,
                "momentum_price_4h": momentum_price_4h,
                "momentum_close_time_4h": momentum_close_time_4h,
                "direction": direction,
                "market_state": market_state,
                "horizon_strength": strength,
                "confidence_band": confidence,
                "h1_direction": h1["direction"],
                "h4_direction": h4["direction"],
                "d1_direction": d1["direction"],
            },
            "live_price_bound": True,
            "data_provider": provider,
            "generated_at": now_iso(),
        }

    except Exception as e:
        return build_error(s, e)


# NDSP_ASSET_TIMEFRAME_READING_V27
# Adds timeframe-specific reading for Asset View.
# Supported: daily / weekly / monthly.
# Keeps the old endpoint compatible when timeframe is omitted.
def _ndsp_tf_norm(tf):
    tf = str(tf or "weekly").strip().lower()
    if tf in ("1d", "d", "day", "daily", "يومي"):
        return "daily"
    if tf in ("1w", "w", "week", "weekly", "اسبوعي", "أسبوعي"):
        return "weekly"
    if tf in ("1m", "m", "month", "monthly", "شهري"):
        return "monthly"
    return "weekly"

def _ndsp_tf_label(tf):
    tf = _ndsp_tf_norm(tf)
    if tf == "daily":
        return "يومي"
    if tf == "monthly":
        return "شهري"
    return "أسبوعي"

def _ndsp_tf_horizon(tf):
    tf = _ndsp_tf_norm(tf)
    if tf == "daily":
        return "أفق يومي"
    if tf == "monthly":
        return "أفق شهري"
    return "أفق أسبوعي"

def _ndsp_tf_group(tf):
    tf = _ndsp_tf_norm(tf)
    if tf == "daily":
        return 1
    if tf == "monthly":
        return 21
    return 5

def _ndsp_tf_aggregate(k, group):
    if group <= 1:
        return k

    highs = k.get("highs") or []
    lows = k.get("lows") or []
    closes = k.get("closes") or []
    vols = k.get("vols") or []
    times = k.get("close_times") or []

    n = len(closes)
    if n < group:
        return k

    ranges = []
    i = n
    while i - group >= 0:
        ranges.append((i - group, i))
        i -= group
    ranges.reverse()

    ah, al, ac, av, at = [], [], [], [], []

    for a, b in ranges:
        ah.append(max(highs[a:b]))
        al.append(min(lows[a:b]))
        ac.append(closes[b - 1])
        av.append(sum(vols[a:b]) if vols else 0)
        at.append(times[b - 1] if times else None)

    return {
        "highs": ah,
        "lows": al,
        "closes": ac,
        "vols": av,
        "close_times": at,
        "provider": k.get("provider", "unknown"),
    }

def _ndsp_tf_analyze(symbol, timeframe):
    tf = _ndsp_tf_norm(timeframe)
    group = _ndsp_tf_group(tf)

    # نستخدم بيانات يومية ونحوّلها إلى أسبوعي/شهري بالتجميع.
    # الشهري يحتاج تاريخ أطول حتى لا يرجع خطأً إلى قراءة يومية.
    limit = 1000 if tf == "monthly" else 360 if tf == "weekly" else 260
    k = get_klines(symbol, "1d", limit=limit)
    k = _ndsp_tf_aggregate(k, group)

    closes = k.get("closes") or []
    highs = k.get("highs") or []
    lows = k.get("lows") or []

    if len(closes) < 8:
        # fallback فقط عند نقص حاد في البيانات، وليس لمجرد أن الشهري عدد شمعاته أقل.
        return analyze_interval(symbol, "1d")

    close = float(closes[-1])
    e20 = ema(closes, 20)
    e50 = ema(closes, 50)
    rrsi = rsi(closes, 14)
    aatr = atr(highs, lows, closes, 14)

    if close > e20 > e50 and rrsi >= 50:
        direction = "bullish"
    elif close < e20 < e50 and rrsi <= 50:
        direction = "bearish"
    else:
        direction = "neutral"

    return {
        "interval": tf,
        "close": close,
        "ema20": e20,
        "ema50": e50,
        "rsi": rrsi,
        "atr": aatr,
        "direction": direction,
        "provider": k.get("provider", "unknown"),
        "momentum_price": close,
        "momentum_close_time": (k.get("close_times") or [None])[-1],
    }

def _ndsp_tf_float(v):
    try:
        if v is None:
            return None
        x = float(str(v).replace(",", ""))
        if math.isfinite(x):
            return x
    except Exception:
        pass
    return None

def _ndsp_tf_quality(a, live_price):
    direction = a.get("direction") or "neutral"
    rsi_v = float(a.get("rsi") or 50)
    close = float(a.get("close") or live_price or 0)
    e20 = float(a.get("ema20") or close or 0)
    e50 = float(a.get("ema50") or close or 0)
    atr_v = float(a.get("atr") or 0)

    score = 48.0

    if direction == "bullish":
        score += 13
        if rsi_v >= 52:
            score += min(14, (rsi_v - 52) * 0.8)
    elif direction == "bearish":
        score += 13
        if rsi_v <= 48:
            score += min(14, (48 - rsi_v) * 0.8)
    else:
        score -= 3
        score += min(8, abs(rsi_v - 50) * 0.45)

    if close and e20 and e50:
        ema_gap = abs(e20 - e50) / close * 100
        price_gap = abs(close - e20) / close * 100
        score += min(9, ema_gap * 2.4)
        score += min(6, price_gap * 1.4)

        if direction == "bullish" and close > e20 > e50:
            score += 7
        if direction == "bearish" and close < e20 < e50:
            score += 7

    atr_pct = (atr_v / close * 100) if close else 0

    if atr_pct >= 6:
        score -= 10
    elif atr_pct >= 4:
        score -= 7
    elif atr_pct >= 2.5:
        score -= 4
    elif 0.35 <= atr_pct <= 1.8:
        score += 3

    return int(round(clamp(score, 20, 95)))

def _ndsp_tf_state_text(a, timeframe):
    tf_label = _ndsp_tf_label(timeframe)
    direction = a.get("direction") or "neutral"
    rsi_v = float(a.get("rsi") or 50)

    if direction == "bullish":
        return f"قراءة {tf_label} · ميل صاعد", f"متابعة اختراق {tf_label}", "انتظار ثبات السعر فوق منطقة المراجعة."
    if direction == "bearish":
        return f"قراءة {tf_label} · ضغط هابط", f"متابعة كسر {tf_label}", "انتظار ثبات السعر دون منطقة المراجعة."

    if rsi_v >= 58:
        return f"قراءة {tf_label} · زخم علوي", f"مراقبة اختراق {tf_label}", "الزخم مرتفع نسبيًا لكن الاتجاه لم يتأكد."
    if rsi_v <= 42:
        return f"قراءة {tf_label} · ضغط سفلي", f"مراقبة كسر {tf_label}", "الزخم منخفض نسبيًا لكن الاتجاه لم يتأكد."

    return f"قراءة {tf_label} · توازن", f"مراقبة {tf_label}", "السعر داخل نطاق توازن؛ لا توجد قراءة اتجاهية كافية."

def _ndsp_apply_timeframe_response(base, symbol, timeframe):
    try:
        tf = _ndsp_tf_norm(timeframe)
        a = _ndsp_tf_analyze(symbol, tf)

        instrument = base.setdefault("instrument", {})
        live_price = _ndsp_tf_float(instrument.get("live_price"))
        if live_price is None or live_price <= 0:
            live_price = _ndsp_tf_float(a.get("close")) or 0

        atr_v = _ndsp_tf_float(a.get("atr")) or (live_price * 0.01)
        if atr_v <= 0:
            atr_v = live_price * 0.01

        direction = a.get("direction") or "neutral"
        rsi_v = float(a.get("rsi") or 50)

        # المستويات مبنية على السعر الحي لكن بسعة ATR للإطار المختار.
        if direction == "bullish":
            activation = live_price + (atr_v * 0.55)
            arrival = live_price + (atr_v * 1.35)
            review = _ndsp_tf_float(a.get("ema20")) or (live_price - atr_v * 0.30)
            invalidation = live_price - (atr_v * 0.95)
        elif direction == "bearish":
            activation = live_price - (atr_v * 0.55)
            arrival = live_price - (atr_v * 1.35)
            review = _ndsp_tf_float(a.get("ema20")) or (live_price + atr_v * 0.30)
            invalidation = live_price + (atr_v * 0.95)
        else:
            if rsi_v >= 50:
                activation = live_price + (atr_v * 0.55)
                arrival = live_price + (atr_v * 1.25)
                review = _ndsp_tf_float(a.get("ema20")) or (live_price - atr_v * 0.25)
                invalidation = live_price - (atr_v * 0.85)
            else:
                activation = live_price - (atr_v * 0.55)
                arrival = live_price - (atr_v * 1.25)
                review = _ndsp_tf_float(a.get("ema20")) or (live_price + atr_v * 0.25)
                invalidation = live_price + (atr_v * 0.85)

        quality = _ndsp_tf_quality(a, live_price)
        confidence, strength = quality_labels(quality)
        state, horizon, caution = _ndsp_tf_state_text(a, tf)

        scenario = base.setdefault("scenario", {})
        scenario["scenario_directional_context"] = state
        scenario["scenario_activation_level"] = fmt_price(activation)
        scenario["scenario_arrival_level"] = fmt_price(arrival)
        scenario["scenario_review_zone"] = fmt_price(review)
        scenario["scenario_invalidation_level"] = fmt_price(invalidation)
        scenario["scenario_confidence_band"] = confidence
        scenario["scenario_time_horizon"] = horizon
        scenario["scenario_risk_note"] = caution

        out = base.setdefault("allowed_public_outputs", {})
        out["directional_bias"] = state
        out["reading_horizon"] = horizon
        out["horizon_strength"] = strength
        out["market_state"] = state
        out["decision_quality"] = quality
        out["caution_reason"] = caution
        out["sanitized_summary"] = (
            f"قراءة {_ndsp_tf_label(tf)} على {clean_symbol(symbol)}: "
            f"السعر {fmt_price(live_price)}، "
            f"جودة القراءة {quality}، "
            f"الحالة {state}."
        )

        la = base.setdefault("live_market_analysis", {})
        la["selected_timeframe"] = tf
        la["selected_timeframe_label"] = _ndsp_tf_label(tf)
        la["selected_timeframe_close"] = a.get("close")
        la["selected_timeframe_rsi"] = a.get("rsi")
        la["selected_timeframe_atr"] = a.get("atr")
        la["selected_timeframe_direction"] = direction
        la["timeframe_model"] = "asset_view_timeframe_v27"
        la["scenario_levels_model"] = "timeframe_atr_ema_v27"

        base["source_mode"] = str(base.get("source_mode", "")) + f" + asset_timeframe_{tf}_v27"

    except Exception as e:
        base["timeframe_warning"] = str(e)

    return base

@app.get("/api/decision/quality-live")
def quality_live(symbol: str = Query("ETHUSDT"), timeframe: str = Query("weekly")):
    base = build_response(symbol)
    base = _ndsp_apply_timeframe_response(base, symbol, timeframe)
    return JSONResponse(base)

@app.get("/api/decision/quality-live/health")
def health():
    return {
        "ok": True,
        "service": "ndsp-live-decision-quality",
        "version": "23",
        "providers": ["binance", "external_chart"],
        "supported_external_symbols": sorted(EXTERNAL_SYMBOLS.keys()),
        "generated_at": now_iso(),
    }

# NDSP_BACKEND_ONLY_DYNAMIC_LEVELS_SAFE
# Backend-only patch: changes scenario level values only.
# Does not touch frontend, HTML, JS, CSS, nginx, or page layout.
if "_ndsp_original_build_response_backend_levels_safe" not in globals():
    _ndsp_original_build_response_backend_levels_safe = build_response

    def _ndsp_safe_float(v):
        try:
            if v is None:
                return None
            x = float(str(v).replace(",", ""))
            if math.isfinite(x):
                return x
        except Exception:
            pass
        return None

    def _ndsp_pick_review_price(live, atr4, direction, h4):
        ema20 = _ndsp_safe_float(h4.get("ema20"))
        ema50 = _ndsp_safe_float(h4.get("ema50"))
        momentum = _ndsp_safe_float(h4.get("momentum_price"))
        rsi4 = _ndsp_safe_float(h4.get("rsi")) or 50.0

        min_sep = max(abs(atr4) * 0.15, abs(live) * 0.0008)

        candidates = []
        if ema20 is not None:
            candidates.append(ema20)
        if ema20 is not None and ema50 is not None:
            candidates.append((ema20 + ema50) / 2)
        if momentum is not None:
            candidates.append(momentum)
        if ema50 is not None:
            candidates.append(ema50)

        for c in candidates:
            if c is not None and abs(c - live) >= min_sep:
                return c

        if direction == "bullish":
            return live - (atr4 * 0.30)
        if direction == "bearish":
            return live + (atr4 * 0.30)

        if rsi4 >= 50:
            return live - (atr4 * 0.25)
        return live + (atr4 * 0.25)

    def build_response(symbol):
        base = _ndsp_original_build_response_backend_levels_safe(symbol)

        try:
            if base.get("live_price_bound") is not True:
                return base

            s = clean_symbol(symbol)
            live = _ndsp_safe_float((base.get("instrument") or {}).get("live_price"))
            if live is None or live <= 0:
                return base

            live_analysis = base.setdefault("live_market_analysis", {})
            direction = live_analysis.get("direction") or "neutral"

            h4 = analyze_interval(s, "4h")

            atr4 = (
                _ndsp_safe_float(live_analysis.get("atr_4h"))
                or _ndsp_safe_float(h4.get("atr"))
                or (live * 0.01)
            )

            if atr4 <= 0:
                atr4 = live * 0.01

            review = _ndsp_pick_review_price(live, atr4, direction, h4)

            if direction == "bullish":
                activation = live + (atr4 * 0.55)
                arrival = live + (atr4 * 1.35)
                invalidation = min(live - (atr4 * 0.95), review - (atr4 * 0.30))
            elif direction == "bearish":
                activation = live - (atr4 * 0.55)
                arrival = live - (atr4 * 1.35)
                invalidation = max(live + (atr4 * 0.95), review + (atr4 * 0.30))
            else:
                rsi4 = _ndsp_safe_float(h4.get("rsi")) or 50.0
                if rsi4 >= 50:
                    activation = live + (atr4 * 0.55)
                    arrival = live + (atr4 * 1.25)
                    invalidation = live - (atr4 * 0.85)
                else:
                    activation = live - (atr4 * 0.55)
                    arrival = live - (atr4 * 1.25)
                    invalidation = live + (atr4 * 0.85)

            scenario = base.setdefault("scenario", {})
            scenario["scenario_activation_level"] = fmt_price(activation)
            scenario["scenario_arrival_level"] = fmt_price(arrival)
            scenario["scenario_review_zone"] = fmt_price(review)
            scenario["scenario_invalidation_level"] = fmt_price(invalidation)

            live_analysis["technical_review_price"] = review
            live_analysis["scenario_levels_model"] = "backend_only_dynamic_atr_ema_safe"

            base["source_mode"] = str(base.get("source_mode", "")) + " + backend_only_dynamic_levels_safe"

        except Exception as e:
            base["scenario_levels_warning"] = str(e)

        return base

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9057, log_level="warning")

