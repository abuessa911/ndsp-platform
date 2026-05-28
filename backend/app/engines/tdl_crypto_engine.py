########################################
# NDSP CRYPTO HYBRID timing_model ENGINE
# timing_model = Time Dimension Logic
#
# L&M = Long & Medium term direction
# S   = Short term direction / entry timing
########################################


def _num(value, default=0.0):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _direction_from_score(score: float, threshold: float = 0.0) -> str:
    if score > threshold:
        return "bullish"
    if score < -threshold:
        return "bearish"
    return "neutral"


def calculate_crypto_tdl(data: dict):
    data = data if isinstance(data, dict) else {}

    market_positioning = data.get("market_positioning", {}) if isinstance(data.get("market_positioning", {}), dict) else {}
    onchain = data.get("onchain", {}) if isinstance(data.get("onchain", {}), dict) else {}
    market = data.get("market", {}) if isinstance(data.get("market", {}), dict) else {}

    ########################################
    # L&M: Long + Medium term direction
    # يعتمد على market_positioning + Onchain كاتجاه رئيسي
    ########################################

    asset_managers = market_positioning.get("asset_managers", {}) if isinstance(market_positioning.get("asset_managers", {}), dict) else {}
    other_reportables = market_positioning.get("other_reportables", {}) if isinstance(market_positioning.get("other_reportables", {}), dict) else {}
    nonreportable = market_positioning.get("nonreportable", {}) if isinstance(market_positioning.get("nonreportable", {}), dict) else {}

    lm_score = (
        _num(asset_managers.get("long")) - _num(asset_managers.get("short"))
    ) + (
        _num(other_reportables.get("long")) - _num(other_reportables.get("short"))
    ) + (
        _num(nonreportable.get("long")) - _num(nonreportable.get("short"))
    )

    lm_score += (
        _num(onchain.get("whales")) +
        _num(onchain.get("lth")) +
        _num(onchain.get("accumulation_wallets"))
    )

    ########################################
    # S: Short term direction / timing
    # يعتمد على بيانات السوق قصيرة المدى
    ########################################

    price_change_pct = (
        market.get("price_change_pct")
        or market.get("change_pct")
        or market.get("change_percent")
        or market.get("priceChangePercent")
        or 0
    )

    funding_rate = market.get("funding_rate") or market.get("fundingRate") or 0
    liquidations = market.get("liquidations") or 0
    retail_traders = market.get("retail_traders") or 0

    s_score = (
        _num(price_change_pct) -
        _num(funding_rate) -
        _num(liquidations) -
        _num(retail_traders)
    )

    ########################################
    # Optional manual overrides from market
    ########################################

    manual_lm = (
        market.get("tdl_lm_direction")
        or market.get("lm_direction")
        or data.get("tdl_lm_direction")
        or data.get("lm_direction")
    )

    manual_s = (
        market.get("tdl_s_direction")
        or market.get("s_direction")
        or data.get("tdl_s_direction")
        or data.get("s_direction")
    )

    lm_direction = str(manual_lm).lower().strip() if manual_lm else _direction_from_score(lm_score)
    s_direction = str(manual_s).lower().strip() if manual_s else _direction_from_score(s_score)

    if lm_direction not in ("bullish", "bearish", "neutral"):
        lm_direction = "neutral"

    if s_direction not in ("bullish", "bearish", "neutral"):
        s_direction = "neutral"

    golden_signal = (
        lm_direction in ("bullish", "bearish")
        and lm_direction == s_direction
    )

    if golden_signal and lm_direction == "bullish":
        golden_name = "NDSP_GOLDEN_LONG"
    elif golden_signal and lm_direction == "bearish":
        golden_name = "NDSP_GOLDEN_SHORT"
    else:
        golden_name = None

    # dominant محفوظ للتوافق القديم فقط، وليس معناه شراء/بيع بذاته.
    if golden_signal:
        dominant = "L&M_S_ALIGNED"
    elif lm_direction != "neutral" and s_direction != "neutral" and lm_direction != s_direction:
        dominant = "L&M_S_CONFLICT"
    else:
        dominant = "NEUTRAL"

    return {
        "tdl_lm_score": round(lm_score, 6),
        "tdl_s_score": round(s_score, 6),

        "tdl_lm_direction": lm_direction,
        "tdl_s_direction": s_direction,

        "golden_signal": golden_signal,
        "golden_name": golden_name,

        "dominant": dominant,
        "model": "crypto_hybrid_time_dimension_logic",
        "version": "1.0.0-ndsp-golden",
    }
