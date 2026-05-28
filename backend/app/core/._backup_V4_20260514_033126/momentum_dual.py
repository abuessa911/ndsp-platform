from __future__ import annotations

import csv
from pathlib import Path
from statistics import mean


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OHLCV_DIR = PROJECT_ROOT / "data" / "ohlcv"


def _symbol_id(symbol: str) -> str:
    return str(symbol or "").upper().replace("-SPOT", "").strip()


def _safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def _read_ohlcv(symbol: str, limit: int = 120):
    symbol_clean = _symbol_id(symbol)

    candidates = [
        OHLCV_DIR / f"{symbol_clean}.csv",
        OHLCV_DIR / f"{symbol_clean.lower()}.csv",
        OHLCV_DIR / f"{symbol_clean}_ohlcv.csv",
        OHLCV_DIR / f"{symbol_clean.lower()}_ohlcv.csv",
    ]

    path = None
    for c in candidates:
        if c.exists() and c.stat().st_size > 0:
            path = c
            break

    if not path:
        return [], None

    rows = []
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                "time": row.get("time") or row.get("timestamp") or "",
                "open": _safe_float(row.get("open")),
                "high": _safe_float(row.get("high")),
                "low": _safe_float(row.get("low")),
                "close": _safe_float(row.get("close")),
                "volume": _safe_float(row.get("volume")),
            })

    rows = [r for r in rows if r["close"] > 0]
    return rows[-limit:], str(path)


def _ema(values, period: int):
    if not values:
        return []

    k = 2 / (period + 1)
    out = [values[0]]
    for v in values[1:]:
        out.append((v * k) + (out[-1] * (1 - k)))
    return out


def _rsi(values, period: int = 14):
    if len(values) < period + 1:
        return 50.0

    gains = []
    losses = []

    window = values[-(period + 1):]
    for prev, cur in zip(window, window[1:]):
        diff = cur - prev
        if diff >= 0:
            gains.append(diff)
            losses.append(0.0)
        else:
            gains.append(0.0)
            losses.append(abs(diff))

    avg_gain = mean(gains) if gains else 0.0
    avg_loss = mean(losses) if losses else 0.0

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def _macd(values):
    if len(values) < 35:
        return 0.0, 0.0

    ema12 = _ema(values, 12)
    ema26 = _ema(values, 26)

    offset = len(ema12) - len(ema26)
    macd_line = [a - b for a, b in zip(ema12[offset:], ema26)]
    signal = _ema(macd_line, 9)

    if not macd_line or not signal:
        return 0.0, 0.0

    return macd_line[-1], signal[-1]


def run_momentum_dual(symbol: str, governed_direction: str = "neutral"):
    """
    Governed Momentum Dual adapter.

    Governance:
    - does not define direction
    - does not override timing_model
    - does not output raw indicators
    - returns sanitized confirmation/warning context only
    """

    symbol_clean = _symbol_id(symbol)
    rows, source = _read_ohlcv(symbol_clean)

    if len(rows) < 35:
        return {
            "status": "unavailable",
            "signal": "NEUTRAL",
            "alignment": "unknown",
            "confidence_effect": 0,
            "summary": "Momentum context is unavailable.",
            "source": "missing_ohlcv",
        }

    closes = [r["close"] for r in rows]
    volumes = [r["volume"] for r in rows]

    rsi = _rsi(closes, 14)
    macd_value, macd_signal = _macd(closes)

    last_close = closes[-1]
    prev_close = closes[-2] if len(closes) >= 2 else last_close

    volume_ma20 = mean(volumes[-20:]) if len(volumes) >= 20 else mean(volumes)
    last_volume = volumes[-1] if volumes else 0.0

    bullish_score = 0
    bearish_score = 0

    if rsi >= 55:
        bullish_score += 1
    elif rsi <= 45:
        bearish_score += 1

    if macd_value > macd_signal:
        bullish_score += 2
    elif macd_value < macd_signal:
        bearish_score += 2

    if last_close > prev_close:
        bullish_score += 1
    elif last_close < prev_close:
        bearish_score += 1

    if volume_ma20 > 0 and last_volume > volume_ma20:
        if last_close >= prev_close:
            bullish_score += 1
        else:
            bearish_score += 1

    if bearish_score >= 5:
        signal = "BEARISH_CONFIRMATION"
    elif bullish_score >= 5:
        signal = "BULLISH_CONFIRMATION"
    elif bearish_score >= 3:
        signal = "BEARISH_WARNING"
    elif bullish_score >= 3:
        signal = "BULLISH_WARNING"
    else:
        signal = "NEUTRAL"

    governed_direction = str(governed_direction or "neutral").lower()

    if governed_direction == "bearish":
        if signal == "BEARISH_CONFIRMATION":
            alignment = "aligned"
            effect = 6
            summary = "Momentum context confirms the governed bearish state."
        elif signal in ("BULLISH_CONFIRMATION", "BULLISH_WARNING"):
            alignment = "conflict"
            effect = -7
            summary = "Momentum context conflicts with the governed bearish state."
        elif signal == "BEARISH_WARNING":
            alignment = "partial"
            effect = 2
            summary = "Momentum context partially supports the governed bearish state."
        else:
            alignment = "neutral"
            effect = 0
            summary = "Momentum context is neutral."

    elif governed_direction == "bullish":
        if signal == "BULLISH_CONFIRMATION":
            alignment = "aligned"
            effect = 6
            summary = "Momentum context confirms the governed bullish state."
        elif signal in ("BEARISH_CONFIRMATION", "BEARISH_WARNING"):
            alignment = "conflict"
            effect = -7
            summary = "Momentum context conflicts with the governed bullish state."
        elif signal == "BULLISH_WARNING":
            alignment = "partial"
            effect = 2
            summary = "Momentum context partially supports the governed bullish state."
        else:
            alignment = "neutral"
            effect = 0
            summary = "Momentum context is neutral."

    else:
        alignment = "neutral"
        effect = 0
        summary = "No governed directional state is active."

    return {
        "status": "available",
        "signal": signal,
        "alignment": alignment,
        "confidence_effect": effect,
        "summary": summary,
        "source": source or "ohlcv",
    }
