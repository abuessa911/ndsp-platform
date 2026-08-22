"""Governed asset identity and provider routing for the public decision bridge."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path


REGISTRY_PATH = Path(
    os.environ.get(
        "NDSP_ASSET_REGISTRY_PATH",
        Path(__file__).resolve().parents[2] / "docs" / "03-contracts" / "NDSP_ASSET_MASTER_REGISTRY_V1.json",
    )
)


def normalize_alias(value: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(value or "").upper())


def _load_registry() -> tuple[dict, list[dict]]:
    metadata = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    assets = [item for item in metadata.get("assets", []) if item.get("status") == "active"]
    decision_symbols = [str(item.get("decision_symbol") or "").upper() for item in assets]

    if len(assets) < 50:
        raise RuntimeError(f"ASSET_REGISTRY_UNDERSIZED:{len(assets)}")
    if any(not symbol for symbol in decision_symbols):
        raise RuntimeError("ASSET_REGISTRY_EMPTY_DECISION_SYMBOL")
    if len(decision_symbols) != len(set(decision_symbols)):
        raise RuntimeError("ASSET_REGISTRY_DUPLICATE_DECISION_SYMBOL")
    if any(not item.get("provider_symbols") for item in assets):
        raise RuntimeError("ASSET_REGISTRY_PROVIDER_MAPPING_MISSING")
    if any(len(item.get("provider_symbols") or {}) < 2 for item in assets):
        raise RuntimeError("ASSET_REGISTRY_MULTIPLE_PROVIDER_MAPPING_MISSING")

    return metadata, assets


REGISTRY_METADATA, ASSETS = _load_registry()
ASSET_BY_DECISION = {str(item["decision_symbol"]).upper(): item for item in ASSETS}
ALIAS_TO_DECISION: dict[str, str] = {}

for asset in ASSETS:
    decision = str(asset["decision_symbol"]).upper()
    values = [
        decision,
        asset.get("canonical_symbol"),
        asset.get("internal_asset_id"),
        *(asset.get("aliases") or []),
        *(asset.get("provider_symbols") or {}).values(),
    ]
    for value in values:
        alias = normalize_alias(value)
        if alias:
            ALIAS_TO_DECISION.setdefault(alias, decision)


def resolve_symbol(value: str) -> str:
    normalized = normalize_alias(value or "ETHUSDT")
    return ALIAS_TO_DECISION.get(normalized, normalized)


def asset_for(value: str) -> dict | None:
    return ASSET_BY_DECISION.get(resolve_symbol(value))


def provider_symbol(value: str, provider: str) -> str | None:
    asset = asset_for(value)
    if not asset:
        return None
    return (asset.get("provider_symbols") or {}).get(provider)


def provider_priority(value: str) -> list[str]:
    asset = asset_for(value)
    if not asset:
        return []
    configured = asset.get("provider_symbols") or {}
    ordered = [item for item in (asset.get("provider_priority") or []) if item in configured]
    return ordered or list(configured.keys())


def provider_scope(value: str, provider: str) -> str | None:
    asset = asset_for(value)
    if not asset:
        return None
    return (asset.get("provider_scopes") or {}).get(provider)


def market_type_for(value: str) -> str:
    asset = asset_for(value)
    if not asset:
        return "unknown"
    group = asset.get("group")
    return {
        "crypto": "crypto",
        "forex": "forex",
        "commodities": "commodity",
        "indices": "index",
    }.get(group, "unknown")


def external_symbols() -> dict[str, str]:
    return {
        str(item["decision_symbol"]).upper(): item["provider_symbols"]["yahoo"]
        for item in ASSETS
        if (item.get("provider_symbols") or {}).get("yahoo")
    }


def binance_symbols() -> dict[str, str]:
    return {
        str(item["decision_symbol"]).upper(): item["provider_symbols"]["binance"]
        for item in ASSETS
        if (item.get("provider_symbols") or {}).get("binance")
    }


EXTERNAL_SYMBOLS = external_symbols()
BINANCE_SYMBOLS = binance_symbols()
YAHOO_SYMBOLS = EXTERNAL_SYMBOLS
STOOQ_SYMBOLS = {
    str(item["decision_symbol"]).upper(): item["provider_symbols"]["stooq"]
    for item in ASSETS
    if (item.get("provider_symbols") or {}).get("stooq")
}
