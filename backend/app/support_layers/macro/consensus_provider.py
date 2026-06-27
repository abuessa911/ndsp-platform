"""
NDSP V4.1 Macro Consensus Provider

Purpose:
- Provide expected/consensus values for macro events.
- The first version supports manual/static consensus input.
- Later versions can connect to a paid/official-compatible economic calendar provider.

Governance:
- This provider does not produce direction.
- It only provides expected values needed to compute surprise.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class MacroEventType(str, Enum):
    FED_RATE = "fed_rate"
    CPI = "cpi"
    CORE_CPI = "core_cpi"
    NFP = "nfp"
    UNEMPLOYMENT_RATE = "unemployment_rate"
    PCE = "pce"
    CORE_PCE = "core_pce"
    GDP = "gdp"
    RETAIL_SALES = "retail_sales"
    ISM = "ism"


@dataclass(frozen=True)
class MacroConsensus:
    event_type: MacroEventType
    expected_value: float
    unit: str
    source: str
    timestamp_utc: str | None = None
    confidence: float = 1.0


class MacroConsensusProvider(Protocol):
    def get_consensus(self, event_type: MacroEventType) -> MacroConsensus | None:
        ...


class ManualMacroConsensusProvider:
    """
    Manual consensus provider for V4.1 freezing phase.

    Use this until a production consensus data source is selected.
    """

    def __init__(self, values: dict[MacroEventType | str, MacroConsensus | float]):
        self._values: dict[MacroEventType, MacroConsensus] = {}

        for key, value in values.items():
            event_type = key if isinstance(key, MacroEventType) else MacroEventType(str(key))

            if isinstance(value, MacroConsensus):
                self._values[event_type] = value
            else:
                self._values[event_type] = MacroConsensus(
                    event_type=event_type,
                    expected_value=float(value),
                    unit="unknown",
                    source="manual",
                    confidence=1.0,
                )

    def get_consensus(self, event_type: MacroEventType) -> MacroConsensus | None:
        return self._values.get(event_type)
