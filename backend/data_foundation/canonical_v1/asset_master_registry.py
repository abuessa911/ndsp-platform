from __future__ import annotations
import json, re
from pathlib import Path
from typing import Any

def _key(value: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(value or "").upper())

class AssetMasterRegistry:
    def __init__(self, registry_path):
        data = json.loads(Path(registry_path).read_text(encoding="utf-8"))
        self.assets = data.get("assets") or []
        self.by_id = {}
        self.alias_index = {}
        self.provider_index = {}
        for asset in self.assets:
            asset_id = asset["internal_asset_id"]
            if asset_id in self.by_id:
                raise ValueError(f"duplicate internal_asset_id: {asset_id}")
            self.by_id[asset_id] = asset
            aliases = set(asset.get("aliases") or [])
            aliases.add(asset.get("canonical_symbol"))
            for alias in aliases:
                k = _key(alias)
                previous = self.alias_index.get(k)
                if previous and previous != asset_id:
                    raise ValueError(f"ambiguous alias {alias}: {previous}, {asset_id}")
                self.alias_index[k] = asset_id
            for provider, symbol in (asset.get("provider_symbols") or {}).items():
                k = (provider.strip().lower(), _key(symbol))
                previous = self.provider_index.get(k)
                if previous and previous != asset_id:
                    raise ValueError(f"ambiguous provider symbol {k}")
                self.provider_index[k] = asset_id

    def resolve(self, symbol: str, provider: str | None = None) -> dict[str, Any]:
        asset_id = None
        if provider:
            asset_id = self.provider_index.get((provider.strip().lower(), _key(symbol)))
        if asset_id is None:
            asset_id = self.alias_index.get(_key(symbol))
        if asset_id is None:
            return {
                "ok": False,
                "status": "UNKNOWN_ASSET_IDENTITY",
                "input_symbol": symbol,
                "provider": provider,
                "decision_use_allowed": False,
            }
        asset = self.by_id[asset_id]
        return {
            "ok": True,
            "status": "RESOLVED",
            "input_symbol": symbol,
            "provider": provider,
            "internal_asset_id": asset_id,
            "canonical_symbol": asset["canonical_symbol"],
            "asset_class": asset["asset_class"],
            "decision_use_allowed": asset.get("status") == "active",
        }
