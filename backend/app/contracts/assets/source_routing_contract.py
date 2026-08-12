"""
NDSP Asset / Source Routing Contract
عقد الأصل وتوجيه المصادر
"""

from dataclasses import dataclass
from typing import Optional


CONTRACT_VERSION = "NDSP_ASSET_SOURCE_ROUTING_V1"


@dataclass(frozen=True)
class SourceRoute:
    asset: str
    asset_class: str

    source_market: Optional[str]

    source_timeframe: Optional[str]
    analysis_timeframe: Optional[str]

    provider: Optional[str] = None
    dataset: Optional[str] = None
    report_family: Optional[str] = None

    contract_version: str = CONTRACT_VERSION


def validate_source_route(
    route: SourceRoute,
    *,
    require_provider: bool = False,
    require_dataset: bool = False,
) -> None:

    if not route.asset:
        raise ValueError("asset (الأصل) is required")

    if not route.asset_class:
        raise ValueError("asset_class (فئة الأصل) is required")

    if route.asset_class.upper() == "UNKNOWN":
        raise ValueError(
            "asset_class UNKNOWN (فئة الأصل غير معروفة) "
            "cannot pass an authoritative route"
        )

    # VERIFIED GAP (فجوة متحققة):
    # provider/dataset were not explicit in the targeted implementation.
    # Therefore they are NOT fabricated here.
    if require_provider and not route.provider:
        raise ValueError(
            "provider (المزوّد) is required but unresolved"
        )

    if require_dataset and not route.dataset:
        raise ValueError(
            "dataset (مجموعة البيانات) is required but unresolved"
        )

    if (
        route.source_timeframe
        and route.analysis_timeframe
        and route.source_timeframe != route.analysis_timeframe
    ):
        # اختلاف الإطار ليس خطأ تلقائيًا،
        # لكنه يجب أن يبقى ظاهرًا ولا يُخفى.
        pass
