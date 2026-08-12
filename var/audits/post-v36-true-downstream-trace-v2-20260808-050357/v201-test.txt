from backend.app.runtime.ndsp_v201_launch_completion import (
    _weekly_direction_from_real_changes,
    attach_v201_governing_inputs,
)


def test_weekly_direction_bearish():
    assert _weekly_direction_from_real_changes(-303, 711) == "bearish"


def test_weekly_direction_bullish():
    assert _weekly_direction_from_real_changes(-691, -1599) == "bullish"


def test_weekly_direction_neutral():
    assert _weekly_direction_from_real_changes(10, 10) == "neutral"


def test_weekly_direction_missing_is_not_synthetic():
    assert _weekly_direction_from_real_changes(None, 10) is None
    assert _weekly_direction_from_real_changes(10, None) is None


def test_explicit_weekly_direction_has_precedence():
    raw = {
        "raw_cot_connected": True,
        "raw_cot_status": "CONNECTED_MATCHED",
        "raw_cot_governing_inputs_complete": True,
        "source_family": "TFF",
        "market_name": "TEST",
        "report_date": "2026-08-08",
        "asset_managers_bias": "bearish",
        "leveraged_funds_bias": "bearish",

        # Explicit direction must win over numeric fallback.
        "asset_managers_weekly_direction": "bullish",
        "asset_managers_change_long": -100,
        "asset_managers_change_short": 100,

        "leveraged_funds_weekly_direction": "bearish",
        "leveraged_funds_change_long": 100,
        "leveraged_funds_change_short": -100,
    }

    out = attach_v201_governing_inputs(
        {},
        symbol="ETHUSDT",
        timeframe="weekly",
        raw_cot_override=raw,
    )

    d = out["governing_inputs"]["directions"]

    assert d["asset_managers_weekly"] == "bullish"
    assert d["leveraged_funds_weekly"] == "bearish"


def test_real_9076_numeric_fallback_contract():
    raw = {
        "raw_cot_connected": True,
        "raw_cot_status": "CONNECTED_MATCHED",
        "raw_cot_governing_inputs_complete": True,
        "source_family": "TFF",
        "market_name": "ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE",
        "report_date": "2026-08-08",

        "asset_managers_bias": "bearish",
        "asset_managers_change_long": -303,
        "asset_managers_change_short": 711,

        "leveraged_funds_bias": "bearish",
        "leveraged_funds_change_long": -691,
        "leveraged_funds_change_short": -1599,
    }

    out = attach_v201_governing_inputs(
        {},
        symbol="ETHUSDT",
        timeframe="weekly",
        raw_cot_override=raw,
    )

    g = out["governing_inputs"]
    d = g["directions"]

    assert d["asset_managers_overall"] == "bearish"
    assert d["asset_managers_weekly"] == "bearish"

    assert d["leveraged_funds_overall"] == "bearish"
    assert d["leveraged_funds_weekly"] == "bullish"

    assert g["missing_inputs"] == []
    assert g["report_age_days"] == 0.0
    assert g["fresh"] is True
    assert g["status"] == "COMPLETE"
