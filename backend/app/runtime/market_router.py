from __future__ import annotations

from typing import Dict, Any, List

from app.runtime.package_policy import get_package_policy
from app.runtime.binance_feed import get_binance_pulse
from app.runtime.mt4_feed import get_mt4_pulse


CRYPTO = {
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "SHIBUSDT",
}


def get_unified_market_pulse(package: str) -> Dict[str, Any]:
    policy = get_package_policy(package)
    markets: List[str] = policy.get("markets", [])

    crypto_symbols = [s for s in markets if s in CRYPTO]
    mt4_symbols = [s for s in markets if s not in CRYPTO]

    results: List[Dict[str, Any]] = []

    binance_error = None

    try:
        results.extend(get_binance_pulse(crypto_symbols))
    except Exception as exc:
        binance_error = str(exc)
        for s in crypto_symbols:
            results.append({
                "symbol": s,
                "last_price": None,
                "change_percent": None,
                "state": "WAITING_FEED",
                "source": "binance",
                "live": False,
                "note": "Binance feed unavailable",
            })

    results.extend(get_mt4_pulse(mt4_symbols))

    return {
        "ok": True,
        "system": "NDSP",
        "version": "1.0.0",
        "governance_version": "6.1.0",
        "package": policy.get("plan"),
        "runtime_level": policy.get("runtime_level"),
        "logic_leak": False,
        "protected": True,
        "sanitized": True,
        "source_map": {
            "crypto": "binance",
            "forex_metals_indices_energy": "mt4",
        },
        "errors": {
            "binance": binance_error,
        },
        "markets": results,
    }
