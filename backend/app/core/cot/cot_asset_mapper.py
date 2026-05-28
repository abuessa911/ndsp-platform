from __future__ import annotations

from app.core.market_positioning.cot_contracts import CotAssetClass, CotAssetMapping, CotReportFamily


FOREX = {
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "USDCAD",
    "AUDUSD", "NZDUSD", "EURJPY", "GBPJPY",
}

INDICES = {
    "US30", "US500", "US100", "GER40", "UK100",
    "FRA40", "EU50", "JP225", "HK50", "AUS200",
    "CHINA50", "ES35",
}

METALS = {"GOLD", "XAUUSD", "SILVER", "XAGUSD", "GC", "SI"}
ENERGY = {"OIL", "USOIL", "UKOIL", "BRENT", "CL", "BZ", "NG"}
CRYPTO = {"BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT", "ADAUSDT", "DOGEUSDT", "SHIBUSDT"}


def normalize_symbol(symbol: str) -> str:
    return str(symbol or "").strip().upper().replace("/", "").replace("-", "")


def resolve_cot_asset_mapping(symbol: str) -> CotAssetMapping:
    s = normalize_symbol(symbol)

    if s in FOREX or s in INDICES:
        asset_class = CotAssetClass.FOREX if s in FOREX else CotAssetClass.INDICES
        return CotAssetMapping(
            symbol=s,
            asset_class=asset_class,
            report_family=CotReportFamily.TFF,
            lm_categories=("institutional direction/Institutional", "market activity"),
            s_categories=("market momentum", "Dealer/Intermediary"),
            fallback_allowed=True,
            notes="Financial market: TFF market_positioning family is primary.",
        )

    if s in METALS or s in ENERGY:
        asset_class = CotAssetClass.METALS if s in METALS else CotAssetClass.ENERGY
        return CotAssetMapping(
            symbol=s,
            asset_class=asset_class,
            report_family=CotReportFamily.DISAGGREGATED,
            lm_categories=("Producer/Merchant/Processor/User", "Swap Dealers", "market activity"),
            s_categories=("Managed Money",),
            fallback_allowed=True,
            notes="Physical commodity: Disaggregated market_positioning family is primary.",
        )

    if s in CRYPTO or s.endswith("USDT"):
        return CotAssetMapping(
            symbol=s,
            asset_class=CotAssetClass.CRYPTO,
            report_family=CotReportFamily.LEGACY,
            lm_categories=("institutional_positioning",),
            s_categories=("Noncommercials",),
            fallback_allowed=True,
            notes="Crypto market_positioning is fallback only when matching futures data exists.",
        )

    return CotAssetMapping(
        symbol=s,
        asset_class=CotAssetClass.UNKNOWN,
        report_family=CotReportFamily.LEGACY,
        lm_categories=("institutional_positioning",),
        s_categories=("Noncommercials",),
        fallback_allowed=False,
        notes="Unknown symbol. Manual production mapping required.",
    )
