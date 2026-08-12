"""
NDSP COT / TFF Contract
عقد COT / TFF

Rules are aligned with verified source functions:
_ndsp_direction_from_long_short
_ndsp_weekly_direction_from_changes
_ndsp_extract_group_numbers
"""

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Tuple


CONTRACT_VERSION = "NDSP_COT_TFF_V1"

BULLISH = "BULLISH"
BEARISH = "BEARISH"
NEUTRAL = "NEUTRAL"


GROUP_ALIASES = {
    "asset_managers": [
        "asset_managers",
        "asset_manager",
        "asset_manager_institutional",
        "am",
        "long_term",
        "ml",
    ],
    "leveraged_funds": [
        "leveraged_funds",
        "leveraged",
        "lev_funds",
        "speculative",
        "short_term",
        "s",
    ],
    "dealer_intermediary": [
        "dealer_intermediary",
        "dealer",
        "dealers",
    ],
}


CURRENT_LONG_ALIASES = [
    "long",
    "longs",
    "current_long",
    "positions_long",
]

CURRENT_SHORT_ALIASES = [
    "short",
    "shorts",
    "current_short",
    "positions_short",
]

CHANGE_LONG_ALIASES = [
    "change_long",
    "long_change",
    "change_in_long",
    "weekly_change_long",
]

CHANGE_SHORT_ALIASES = [
    "change_short",
    "short_change",
    "change_in_short",
    "weekly_change_short",
]


@dataclass(frozen=True)
class COTGroupNumbers:
    long: Optional[float]
    short: Optional[float]

    change_long: Optional[float]
    change_short: Optional[float]

    has_current_totals: bool
    has_weekly_changes: bool


@dataclass(frozen=True)
class COTDirectionSet:
    asset_managers_overall: Optional[str]
    asset_managers_weekly: Optional[str]

    leveraged_funds_overall: Optional[str]
    leveraged_funds_weekly: Optional[str]

    report_date: Optional[str]
    report_age_days: Optional[int]
    max_age_days: Optional[int]
    fresh: Optional[bool]

    source_market: Optional[str]
    source_timeframe: Optional[str]
    analysis_timeframe: Optional[str]

    report_family: Optional[str] = None
    provider: Optional[str] = None
    dataset: Optional[str] = None

    contract_version: str = CONTRACT_VERSION


def _num(value: Any) -> float:
    if value is None or value == "":
        raise ValueError("numeric COT value is missing")

    if isinstance(value, str):
        value = value.replace(",", "").strip()

    return float(value)


def direction_from_long_short(
    long_value: Any,
    short_value: Any,
) -> Tuple[str, dict]:

    long_value = _num(long_value)
    short_value = _num(short_value)

    if long_value > short_value:
        return BULLISH, {
            "dominant_side": "LONG",
            "long_value": long_value,
            "short_value": short_value,
            "comparison_rule": "LONG_GREATER_THAN_SHORT",
            "comparison_gap_for_display_only":
                abs(long_value - short_value),
        }

    if short_value > long_value:
        return BEARISH, {
            "dominant_side": "SHORT",
            "long_value": long_value,
            "short_value": short_value,
            "comparison_rule": "SHORT_GREATER_THAN_LONG",
            "comparison_gap_for_display_only":
                abs(short_value - long_value),
        }

    return NEUTRAL, {
        "dominant_side": "EQUAL",
        "long_value": long_value,
        "short_value": short_value,
        "comparison_rule": "LONG_EQUALS_SHORT",
        "comparison_gap_for_display_only": 0,
    }


def weekly_direction_from_changes(
    change_long: Any,
    change_short: Any,
) -> Tuple[str, dict]:

    change_long = _num(change_long)
    change_short = _num(change_short)

    if change_long > change_short:
        return BULLISH, {
            "dominant_side": "LONG_CHANGE",
            "change_long": change_long,
            "change_short": change_short,
            "comparison_rule":
                "CHANGE_LONG_GREATER_THAN_CHANGE_SHORT",
            "comparison_gap_for_display_only":
                abs(change_long - change_short),
        }

    if change_short > change_long:
        return BEARISH, {
            "dominant_side": "SHORT_CHANGE",
            "change_long": change_long,
            "change_short": change_short,
            "comparison_rule":
                "CHANGE_SHORT_GREATER_THAN_CHANGE_LONG",
            "comparison_gap_for_display_only":
                abs(change_short - change_long),
        }

    return NEUTRAL, {
        "dominant_side": "EQUAL_CHANGE",
        "change_long": change_long,
        "change_short": change_short,
        "comparison_rule":
            "CHANGE_LONG_EQUALS_CHANGE_SHORT",
        "comparison_gap_for_display_only": 0,
    }


def extract_group_numbers(
    payload: Mapping[str, Any],
    group: str,
) -> COTGroupNumbers:

    g = str(group or "").lower()
    prefixes = GROUP_ALIASES.get(g, [g])

    def find_value(suffixes):
        for pref in prefixes:
            for suf in suffixes:
                for key in (
                    f"{pref}_{suf}",
                    f"{pref}.{suf}",
                    f"{pref}:{suf}",
                ):
                    if (
                        key in payload
                        and payload.get(key) not in (None, "")
                    ):
                        return payload.get(key)

        if g == "asset_managers":
            for suffix in suffixes:
                for key in (
                    f"raw_cot_asset_managers_{suffix}",
                    f"context_asset_managers_{suffix}",
                    f"asset_managers_{suffix}",
                ):
                    if (
                        key in payload
                        and payload.get(key) not in (None, "")
                    ):
                        return payload.get(key)

        if g == "leveraged_funds":
            for suffix in suffixes:
                for key in (
                    f"raw_cot_leveraged_funds_{suffix}",
                    f"context_leveraged_funds_{suffix}",
                    f"leveraged_funds_{suffix}",
                ):
                    if (
                        key in payload
                        and payload.get(key) not in (None, "")
                    ):
                        return payload.get(key)

        return None

    long_value = find_value(CURRENT_LONG_ALIASES)
    short_value = find_value(CURRENT_SHORT_ALIASES)

    change_long = find_value(CHANGE_LONG_ALIASES)
    change_short = find_value(CHANGE_SHORT_ALIASES)

    return COTGroupNumbers(
        long=long_value,
        short=short_value,
        change_long=change_long,
        change_short=change_short,
        has_current_totals=(
            long_value is not None and short_value is not None
        ),
        has_weekly_changes=(
            change_long is not None and change_short is not None
        ),
    )


def validate_direction(value: Optional[str], field: str) -> None:
    # Missing (مفقود) stays missing.
    if value is None:
        return

    if value not in {BULLISH, BEARISH, NEUTRAL}:
        raise ValueError(
            f"{field}: invalid direction {value!r}"
        )


def validate_cot_direction_set(c: COTDirectionSet) -> None:

    validate_direction(
        c.asset_managers_overall,
        "asset_managers_overall",
    )
    validate_direction(
        c.asset_managers_weekly,
        "asset_managers_weekly",
    )
    validate_direction(
        c.leveraged_funds_overall,
        "leveraged_funds_overall",
    )
    validate_direction(
        c.leveraged_funds_weekly,
        "leveraged_funds_weekly",
    )

    # لا نحول البيانات المفقودة إلى نجاح اصطناعي.
    freshness_parts = (
        c.report_date,
        c.report_age_days,
        c.max_age_days,
        c.fresh,
    )

    present = sum(x is not None for x in freshness_parts)

    if present not in (0, len(freshness_parts)):
        raise ValueError(
            "partial freshness metadata: "
            "report_date/report_age_days/max_age_days/fresh "
            "must remain explicitly complete or incomplete"
        )

    if present == len(freshness_parts):
        if c.report_age_days < 0:
            raise ValueError("report_age_days cannot be negative")

        expected = c.report_age_days <= c.max_age_days

        if c.fresh != expected:
            raise ValueError(
                "fresh disagrees with report age policy"
            )
