#!/usr/bin/env python3
from backend.layers.canonical_v1.runtime_bridge import run_canonical_layers, canonical_nmp_from_legacy, apply_canonical_golden
from backend.app.runtime.ndsp_v200_score_inputs import attach_v200_score_inputs as _ndsp_attach_v200_score_inputs_v200
# NDSP_V200_SCORE_INPUT_CONTRACT_PATCH
from backend.app.runtime.ndsp_v201_launch_completion import (
    attach_v201_governing_inputs as _ndsp_attach_v201_governing_inputs,
    attach_v202_commercial_score as _ndsp_attach_v202_commercial_score,
)
# NDSP_V201_V203_COMMERCIAL_LAUNCH_PATCH
# NDSP_CANONICAL_CONSUMER_V5
import os, json, math, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from datetime import datetime, timezone


# NDSP_NMP_PUBLIC_CONTRACT_REMEDIATION_V143

def _ndsp_public_text_v143(value):
    import re

    text = str(value)
    has_arabic = bool(re.search(r"[\u0600-\u06ff]", text))
    reference = (
        "\u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a \u0627\u0644\u0645\u0631\u062c\u0639\u064a\u0629 \u0627\u0644\u0645\u0624\u0633\u0633\u064a\u0629 \u0627\u0644\u062d\u0627\u0643\u0645\u0629"
        if has_arabic
        else "governed institutional reference data"
    )

    replacements = [
        (r"canonical\s+COT\s+directions\s+are\s+missing", "governed reference directions are incomplete"),
        (r"\bCOT\b", reference),
        (r"commitments?\s+of\s+traders?", reference),
        (r"leveraged\s+funds?", "institutional positioning"),
        (r"asset\s+managers?", "institutional positioning"),
        (r"non[-\s]?commercials?", "institutional positioning"),
        (r"\bcommercials\b|commercial\s+traders?", "institutional positioning"),
    ]

    for pattern,replacement in replacements:
        text = re.sub(pattern,replacement,text,flags=re.I)

    return text


def _ndsp_public_contract_v143(value):
    import json

    if isinstance(value,dict):
        return {key:_ndsp_public_contract_v143(item) for key,item in value.items()}
    if isinstance(value,list):
        return [_ndsp_public_contract_v143(item) for item in value]
    if isinstance(value,tuple):
        return tuple(_ndsp_public_contract_v143(item) for item in value)
    if isinstance(value,set):
        return [_ndsp_public_contract_v143(item) for item in value]
    if isinstance(value,str):
        return _ndsp_public_text_v143(value)

    if hasattr(value,"model_dump"):
        try:
            return _ndsp_public_contract_v143(value.model_dump())
        except Exception:
            pass

    if hasattr(value,"dict") and callable(getattr(value,"dict",None)):
        try:
            return _ndsp_public_contract_v143(value.dict())
        except Exception:
            pass

    class_name=value.__class__.__name__ if value is not None else ""

    if class_name.endswith("JSONResponse") and hasattr(value,"body"):
        try:
            from starlette.responses import JSONResponse
            raw=value.body.decode("utf-8") if isinstance(value.body,(bytes,bytearray)) else str(value.body)
            content=_ndsp_public_contract_v143(json.loads(raw))
            headers=dict(getattr(value,"headers",{}) or {})
            headers.pop("content-length",None)
            headers.pop("content-type",None)
            return JSONResponse(
                content=content,
                status_code=int(getattr(value,"status_code",200)),
                headers=headers,
                media_type=getattr(value,"media_type","application/json"),
                background=getattr(value,"background",None),
            )
        except Exception:
            return value

    return value

UPSTREAM = os.environ.get("NDSP_NMP_WRAPPER_UPSTREAM", "http://127.0.0.1:9067").rstrip("/")
HOST = os.environ.get("NDSP_NMP_WRAPPER_HOST", "127.0.0.1")
PORT = int(os.environ.get("NDSP_NMP_WRAPPER_PORT", "9069"))

TF_MAP = {
    "1m": "1m", "5m": "5m", "15m": "15m", "30m": "30m",
    "1H": "1h", "4H": "4h", "1D": "1d", "1W": "1w", "1M": "1M",
    "1h": "1h", "4h": "4h", "1d": "1d", "1w": "1w",
    "weekly": "1w", "daily": "1d", "monthly": "1M"
}

def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def safe_float(v):
    try:
        n = float(str(v).replace(",", "").strip())
        if math.isfinite(n):
            return n
    except Exception:
        pass
    return None

def http_json(url, timeout=10):
    req = urllib.request.Request(url, headers={"User-Agent": "NDSP-NMP-Wrapper/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read().decode("utf-8", "replace")
        return json.loads(raw)

def rsi_values(closes, period=14):
    if len(closes) < period + 2:
        return [None] * len(closes)

    rsis = [None] * len(closes)
    gains, losses = [], []

    for i in range(1, period + 1):
        d = closes[i] - closes[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    def calc_rsi(g, l):
        if l == 0:
            return 100.0
        rs = g / l
        return 100.0 - (100.0 / (1.0 + rs))

    rsis[period] = calc_rsi(avg_gain, avg_loss)

    for i in range(period + 1, len(closes)):
        d = closes[i] - closes[i - 1]
        gain = max(d, 0.0)
        loss = max(-d, 0.0)
        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period
        rsis[i] = calc_rsi(avg_gain, avg_loss)

    return rsis

def direction_from_quality(data):
    txt = json.dumps(_ndsp_public_contract_v143(data.get("scenario") or {}), ensure_ascii=False).lower()
    txt += " " + json.dumps(_ndsp_public_contract_v143(data.get("allowed_public_outputs") or {}), ensure_ascii=False).lower()

    bearish_words = ["هابط", "ضغط هابط", "bearish", "down", "negative"]
    bullish_words = ["صاعد", "دعم صاعد", "bullish", "up", "positive"]

    if any(w in txt for w in bearish_words):
        return "BEARISH"
    if any(w in txt for w in bullish_words):
        return "BULLISH"
    return "NEUTRAL"

def binance_symbol_ok(symbol):
    s = str(symbol or "").upper().strip()
    if not s.endswith("USDT"):
        return False
    base = s.replace("USDT", "")
    return bool(base) and base.isalnum()

def compute_nmp(symbol, timeframe, data):
    symbol = str(symbol or "").upper().strip()
    tf = str(timeframe or "1D").strip()
    interval = TF_MAP.get(tf, tf)

    if not binance_symbol_ok(symbol):
        return {
            "status": "UNAVAILABLE",
            "value": None,
            "level": None,
            "source": "quality-live-nmp-wrapper",
            "timeframe": tf,
            "note": "NMP غير متاح لهذا الأصل عبر Binance klines."
        }

    url = "https://api.binance.com/api/v3/klines?" + urllib.parse.urlencode({
        "symbol": symbol,
        "interval": interval,
        "limit": 220
    })

    try:
        rows = http_json(url, timeout=8)
    except Exception as e:
        return {
            "status": "UNAVAILABLE",
            "value": None,
            "level": None,
            "source": "quality-live-nmp-wrapper",
            "timeframe": tf,
            "note": "تعذر جلب شموع NMP من مزود السوق.",
            "error": str(e)[:160]
        }

    if not isinstance(rows, list) or len(rows) < 40:
        return {
            "status": "UNAVAILABLE",
            "value": None,
            "level": None,
            "source": "quality-live-nmp-wrapper",
            "timeframe": tf,
            "note": "عدد الشموع غير كافٍ لحساب NMP."
        }

    closes = [safe_float(r[4]) for r in rows]
    opens = [safe_float(r[1]) for r in rows]
    highs = [safe_float(r[2]) for r in rows]
    lows = [safe_float(r[3]) for r in rows]

    if any(v is None for v in closes[-40:]) or any(v is None for v in opens[-40:]):
        return {
            "status": "UNAVAILABLE",
            "value": None,
            "level": None,
            "source": "quality-live-nmp-wrapper",
            "timeframe": tf,
            "note": "بيانات الشموع غير صالحة لحساب NMP."
        }

    rsis = rsi_values(closes, 14)
    valid = [(i, v) for i, v in enumerate(rsis) if v is not None and i < len(rows)]

    if not valid:
        return {
            "status": "UNAVAILABLE",
            "value": None,
            "level": None,
            "source": "quality-live-nmp-wrapper",
            "timeframe": tf,
            "note": "تعذر حساب RSI لاستخراج شمعة الزخم."
        }

    direction = direction_from_quality(data)

    # NDSP_CANONICAL_NMP_SELECTION_V5
    _canonical_nmp = canonical_nmp_from_legacy(
        opens=opens,
        valid=valid,
        direction=direction,
        timeframe=timeframe,
        indicator_name=str(data.get('nmp_indicator_name') or 'RSI'),
    )
    if _canonical_nmp.get('status') != 'AVAILABLE':
        return _canonical_nmp
    idx = _canonical_nmp['candle_index']
    rsi = _canonical_nmp['indicator_value']
    level = _canonical_nmp['value']
    candle_time_ms = int(rows[idx][0]) if rows[idx] and rows[idx][0] is not None else None

    return {
        "status": "AVAILABLE",
        "value": level,
        "level": level,
        "source": "quality-live-nmp-wrapper",
        "provider": "binance_klines",
        "method": "RSI_EXTREME_MOMENTUM_CANDLE_OPEN",
        "rule": "NMP = opening price of the momentum candle",
        "symbol": symbol,
        "timeframe": tf,
        "source_interval": interval,
        "direction": direction,
        "rsi": round(float(rsi), 4),
        "momentum_candle": {
            "open_time_ms": candle_time_ms,
            "open": opens[idx],
            "high": highs[idx],
            "low": lows[idx],
            "close": closes[idx]
        },
        "note": "NMP محسوب في الباك إند من شمعة الزخم، وليس من الواجهة.",
        "updated_at": now_iso()
    }

# NDSP_PUBLIC_QUALITY_CONTRACT_V9
def _ndsp_finalize_public_contract_v9(payload):
    if not isinstance(payload, dict):
        return payload

    def _clean_value(value):
        if isinstance(value, dict):
            cleaned = {}

            for key, child in value.items():
                key_text = str(key)

                if key_text.startswith("_ndsp_"):
                    continue

                cleaned[key] = _clean_value(child)

            return cleaned

        if isinstance(value, list):
            return [
                _clean_value(item)
                for item in value
            ]

        return value

    data = _clean_value(payload)

    scenario = data.get("scenario")
    if not isinstance(scenario, dict):
        scenario = {}
        data["scenario"] = scenario

    allowed = data.get("allowed_public_outputs")
    if not isinstance(allowed, dict):
        allowed = {}
        data["allowed_public_outputs"] = allowed

    analysis = data.get("live_market_analysis")
    if not isinstance(analysis, dict):
        analysis = {}
        data["live_market_analysis"] = analysis

    golden = data.get("golden_alignment")
    if not isinstance(golden, dict):
        golden = {}
        data["golden_alignment"] = golden

    missing_inputs = golden.get("missing_inputs")
    if not isinstance(missing_inputs, list):
        missing_inputs = []

    reason_code = str(
        golden.get("reason_code")
        or data.get("golden_reason_code")
        or ""
    ).strip()

    inputs_incomplete = (
        reason_code == "MISSING_CANONICAL_COT_DIRECTIONS"
        or bool(missing_inputs)
    )

    if inputs_incomplete:
        reason = (
            "تعذر تقييم إشارة نواف الذهبية لأن بيانات "
            "COT الحاكمة المطلوبة غير مكتملة."
        )

        label = (
            "غير مقيّمة — بيانات المحاذاة غير مكتملة"
        )

        evidence = [
            {
                "label": "حالة التقييم",
                "value": (
                    "لم تُقيّم الإشارة لعدم اكتمال "
                    "بيانات COT الحاكمة"
                ),
            }
        ]

        data["golden_signal"] = False
        data["golden_alignment_active"] = False
        data["enhanced_golden_signal"] = False
        data["enhanced_golden_alignment_active"] = False
        data["golden_status"] = "inputs_incomplete"
        data["golden_reason_public"] = reason
        data["golden_evidence_public"] = evidence

        golden["golden_signal"] = False
        golden["enhanced_golden_signal"] = False
        golden["golden_alignment_active"] = False
        golden["enhanced_golden_alignment_active"] = False
        golden["golden_status"] = "inputs_incomplete"
        golden["decision_authority"] = False
        golden["not_recommendation"] = True
        golden["no_buy_sell"] = True

        spotlight = data.get("golden_spotlight")
        if not isinstance(spotlight, dict):
            spotlight = {}
            data["golden_spotlight"] = spotlight

        spotlight["title"] = (
            spotlight.get("title")
            or "إشارة نواف الذهبية"
        )
        spotlight["status"] = "inputs_incomplete"
        spotlight["label"] = label
        spotlight["summary"] = reason
        spotlight["quality_effect"] = (
            "لم تُحتسب الإشارة ضمن سلطة القرار بسبب "
            "نقص بيانات المحاذاة الحاكمة."
        )
        spotlight["evidence"] = evidence

        explainability = data.get("explainability")
        if not isinstance(explainability, dict):
            explainability = {}
            data["explainability"] = explainability

        explainability["golden_signal_exposed"] = True
        explainability["golden_signal"] = False
        explainability["golden_status"] = "inputs_incomplete"
        explainability["golden_reason_public"] = reason
        explainability["not_recommendation"] = True

        public_explainability = data.get(
            "public_explainability"
        )

        if not isinstance(public_explainability, dict):
            public_explainability = {}
            data["public_explainability"] = (
                public_explainability
            )

        public_golden = public_explainability.get(
            "golden_alignment"
        )

        if not isinstance(public_golden, dict):
            public_golden = {}
            public_explainability["golden_alignment"] = (
                public_golden
            )

        public_golden["title"] = "إشارة نواف الذهبية"
        public_golden["status"] = "inputs_incomplete"
        public_golden["label"] = label
        public_golden["reason"] = reason
        public_golden["evidence"] = evidence
        public_golden["notice"] = (
            "الإشارة غير مقيّمة حاليًا بسبب نقص "
            "المدخلات الحاكمة، وليست توصية مالية."
        )

    activation = scenario.get(
        "scenario_activation_level"
    )

    review = scenario.get(
        "scenario_review_zone"
    )

    context = str(
        scenario.get("scenario_directional_context")
        or ""
    )

    caution = None

    if activation not in (None, "") and review not in (None, ""):
        if "هابط" in context:
            caution = (
                "تبقى القراءة الهابطة تحت المتابعة؛ "
                f"لا يتفعّل السيناريو إلا بعد كسر مستوى "
                f"التفعيل {activation}، بينما تستدعي "
                f"العودة فوق منطقة المراجعة {review} "
                "إعادة تقييم القراءة."
            )

        elif "صاعد" in context:
            caution = (
                "تبقى القراءة الصاعدة تحت المتابعة؛ "
                f"لا يتفعّل السيناريو إلا بعد اختراق مستوى "
                f"التفعيل {activation}، بينما يستدعي "
                f"الهبوط دون منطقة المراجعة {review} "
                "إعادة تقييم القراءة."
            )

        else:
            caution = (
                "يبقى السيناريو تحت المتابعة؛ "
                f"مستوى التفعيل {activation} هو شرط "
                f"الانتقال، ومنطقة المراجعة {review} "
                "تستدعي إعادة تقييم القراءة."
            )

    if caution:
        scenario["scenario_risk_note"] = caution
        allowed["caution_reason"] = caution

    h1 = str(
        analysis.get("h1_direction")
        or ""
    ).lower()

    h4 = str(
        analysis.get("h4_direction")
        or ""
    ).lower()

    selected = str(
        analysis.get("selected_timeframe_direction")
        or ""
    ).lower()

    short_direction = None

    if h1 == h4 and h1 in ("bullish", "bearish"):
        short_direction = h1

    if (
        short_direction
        and selected in ("bullish", "bearish")
        and short_direction != selected
    ):
        data["cross_timeframe_divergence"] = True
        data["cross_timeframe_state"] = (
            "SHORT_TERM_"
            + short_direction.upper()
            + "_WITHIN_SELECTED_"
            + selected.upper()
        )

    elif (
        short_direction
        and selected in ("bullish", "bearish")
        and short_direction == selected
    ):
        data["cross_timeframe_divergence"] = False
        data["cross_timeframe_state"] = (
            "SHORT_TERM_ALIGNED_WITH_SELECTED"
        )

    else:
        data["cross_timeframe_divergence"] = False
        data["cross_timeframe_state"] = (
            "MIXED_OR_UNCONFIRMED"
        )

    data["public_contract_version"] = (
        "quality-live-public-v9"
    )

    return data

def enrich_with_nmp(data, symbol, timeframe):
    if not isinstance(data, dict):
        return _ndsp_finalize_public_contract_v9(data)

    existing = data.get("nmp")
    if isinstance(existing, dict) and existing.get("status") == "AVAILABLE" and existing.get("value") is not None:
        return _ndsp_finalize_public_contract_v9(data)

    nmp = compute_nmp(symbol, timeframe, data)

    data["nmp"] = nmp
    data["nmp_status"] = nmp.get("status")
    data["nmp_level"] = nmp.get("value")
    data["nmp_value"] = nmp.get("value")
    data["nmp_source"] = nmp.get("source")
    data["nmp_timeframe"] = timeframe
    # NDSP_V12_SCENARIO_LEVELS_CONTRACT_CALL
    data = _ndsp_v12_inject_scenario_levels_contract(data)

    scenario = data.get("scenario")
    if isinstance(scenario, dict):
        scenario["nmp_status"] = nmp.get("status")
        scenario["nmp_level"] = nmp.get("value")
        scenario["nmp_source"] = nmp.get("source")
        scenario["nmp_timeframe"] = timeframe

    apo = data.get("allowed_public_outputs")
    if isinstance(apo, dict):
        apo["nmp_status"] = nmp.get("status")
        apo["nmp_level"] = nmp.get("value")
        apo["nmp_note"] = nmp.get("note")

    data["_ndsp_nmp_injected_at"] = now_iso()
    data["_ndsp_nmp_contract"] = "quality-live-nmp-wrapper-v1"
    return _ndsp_finalize_public_contract_v9(data)

# NDSP_FULL_44_V26_START
from backend.app.runtime.ndsp_public_governance_projection_v1 import attach_governance_projection as _ndsp_attach_governance_projection_v26
_ndsp_enrich_with_nmp_before_governance_v26 = enrich_with_nmp
def enrich_with_nmp(*args, **kwargs):
    return _ndsp_attach_governance_projection_v26(_ndsp_enrich_with_nmp_before_governance_v26(*args, **kwargs))
# NDSP_FULL_44_V26_END

class Handler(BaseHTTPRequestHandler):
    server_version = "NDSPQualityLiveNMPWrapper/1.0"

    def _send(self, code, payload, ctype="application/json; charset=utf-8"):
        raw = json.dumps(_ndsp_public_contract_v143(payload), ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store, no-cache, max-age=0, must-revalidate")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(raw)

    def do_HEAD(self):
        return self.do_GET()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)

        if parsed.path in ("/health", "/api/decision/quality-live/health"):
            return self._send(200, {
                "ok": True,
                "service": "ndsp-quality-live-nmp-wrapper",
                "port": PORT,
                "upstream": UPSTREAM,
                "updated_at": now_iso()
            })

        if parsed.path != "/api/decision/quality-live":
            return self._send(404, {"ok": False, "error": "NOT_FOUND", "path": parsed.path})

        symbol = (qs.get("symbol") or ["ETHUSDT"])[0]
        timeframe = (qs.get("timeframe") or ["1D"])[0]
        upstream_url = UPSTREAM + self.path

        try:
            data = http_json(upstream_url, timeout=15)
            data = enrich_with_nmp(data, symbol, timeframe)
            requested_mode = (
                (qs.get("analysis_mode") or qs.get("mode")
                 or qs.get("reading") or qs.get("reading_mode")
                 or qs.get("analysis_type") or [""])[0]
            )
            data = _ndsp_attach_v201_governing_inputs(
                data,
                symbol=symbol,
                timeframe=timeframe,
                analysis_mode=requested_mode,
            )
            data = _ndsp_attach_v200_score_inputs_v200(
                data,
                symbol=symbol,
                timeframe=timeframe,
                analysis_mode=requested_mode,
            )
            data = _ndsp_attach_v202_commercial_score(
                data,
                symbol=symbol,
                timeframe=timeframe,
                analysis_mode=requested_mode,
            )
            return self._send(200, data)
        except Exception as e:
            return self._send(502, {
                "ok": False,
                "error": "NMP_WRAPPER_UPSTREAM_FAILED",
                "upstream": upstream_url,
                "detail": str(e)[:300],
                "updated_at": now_iso()
            })

    def log_message(self, fmt, *args):
        return

def main():
    srv = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"[NDSP] quality-live NMP wrapper listening on http://{HOST}:{PORT} upstream={UPSTREAM}", flush=True)
    srv.serve_forever()


# NDSP_V12_SCENARIO_LEVELS_CONTRACT_PATCH_START
def _ndsp_v12_parse_scenario_price(value):
    # Convert existing scenario flat level values into numeric prices without inventing values.
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        try:
            return float(value)
        except Exception:
            return None

    if isinstance(value, str):
        s = value.strip()
        if not s:
            return None

        lowered = s.lower()
        if lowered in {"none", "null", "nan", "unavailable", "n/a", "na", "-"}:
            return None

        compact = s.replace(",", "").replace("٬", "").strip()

        if "-" in compact.replace("—", "-") and not compact.startswith("-"):
            try:
                return float(compact)
            except Exception:
                return None

        try:
            return float(compact)
        except Exception:
            return None

    return None


def _ndsp_v12_level_object(raw_value, label_ar, label_en):
    price = _ndsp_v12_parse_scenario_price(raw_value)
    source = "computed" if price is not None else "unavailable"
    return {
        "price": price,
        "label_ar": label_ar,
        "label_en": label_en,
        "source": source,
        "raw_value": raw_value,
    }


def _ndsp_v12_inject_scenario_levels_contract(data):
    if not isinstance(data, dict):
        return data

    scenario = data.get("scenario")
    if not isinstance(scenario, dict):
        return data

    if isinstance(data.get("scenario_levels"), dict):
        return data

    levels = {
        "activation": _ndsp_v12_level_object(
            scenario.get("scenario_activation_level"),
            "مستوى التفعيل",
            "Activation level",
        ),
        "arrival": _ndsp_v12_level_object(
            scenario.get("scenario_arrival_level"),
            "مستوى الوصول",
            "Arrival level",
        ),
        "review": _ndsp_v12_level_object(
            scenario.get("scenario_review_zone"),
            "مستوى المراجعة",
            "Review level",
        ),
        "invalidation": _ndsp_v12_level_object(
            scenario.get("scenario_invalidation_level"),
            "مستوى الإلغاء",
            "Invalidation level",
        ),
    }

    data["scenario_levels"] = levels
    scenario.setdefault("scenario_levels", levels)

    data["_ndsp_v12_scenario_levels_contract"] = {
        "status": "injected",
        "source": "quality-live-nmp-wrapper",
        "rule": "derived_from_existing_scenario_flat_fields_without_inventing_numbers",
    }

    return data
# NDSP_V12_SCENARIO_LEVELS_CONTRACT_PATCH_END

if __name__ == "__main__":
    main()
