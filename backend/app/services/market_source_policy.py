from __future__ import annotations

from typing import Dict, Any


CRYPTO_BASES = {
    "BTC", "ETH", "SOL", "BNB", "XRP", "ADA", "DOGE", "AVAX", "LINK",
    "DOT", "MATIC", "LTC", "BCH", "TRX", "TON", "NEAR", "ATOM", "UNI",
}


def normalize_symbol(symbol: str) -> str:
    return (symbol or "").strip().upper().replace("/", "").replace("-", "").replace("_", "")


def is_crypto_symbol(symbol: str) -> bool:
    s = normalize_symbol(symbol)

    if s.endswith("USDT"):
        base = s[:-4]
        return base in CRYPTO_BASES

    if s.endswith("USD"):
        base = s[:-3]
        return base in CRYPTO_BASES

    return s in CRYPTO_BASES


def to_binance_symbol(symbol: str) -> str:
    s = normalize_symbol(symbol)

    if s.endswith("USDT"):
        return s

    if s.endswith("USD"):
        base = s[:-3]
        if base in CRYPTO_BASES:
            return base + "USDT"

    if s in CRYPTO_BASES:
        return s + "USDT"

    return s


def preferred_market_source(symbol: str) -> str:
    return "binance" if is_crypto_symbol(symbol) else "mt4_fxcm"


def market_source_policy(symbol: str) -> Dict[str, Any]:
    s = normalize_symbol(symbol)
    source = preferred_market_source(s)
    return {
        "input_symbol": symbol,
        "normalized_symbol": s,
        "preferred_source": source,
        "binance_symbol": to_binance_symbol(s) if source == "binance" else None,
        "mt4_symbol": s if source == "mt4_fxcm" else None,
    }
