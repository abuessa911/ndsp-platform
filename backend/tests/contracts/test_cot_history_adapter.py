from pathlib import Path

from app.support_layers.cot.cot_history_adapter import (
    CotMarketIdentity,
    build_governed_history_payload,
)


RAW_DIR = Path(
    "/home/nawaf511/empire-core-new/backend/data/raw_cot"
)

ETH = CotMarketIdentity(
    market_name=(
        "ETHER CASH SETTLED - "
        "CHICAGO MERCANTILE EXCHANGE"
    ),
    market_code="146021",
    exchange="CME",
)


def test_exact_same_market_history():
    payload = build_governed_history_payload(
        RAW_DIR,
        ETH,
    )

    assert payload["report_date"] == "2026-07-21"
    assert payload["previous_report_date"] == "2026-07-14"


def test_current_values_are_real():
    payload = build_governed_history_payload(
        RAW_DIR,
        ETH,
    )

    assert payload["asset_managers_long"] == 1634
    assert payload["asset_managers_short"] == 4054

    assert payload["leveraged_funds_long"] == 2223
    assert payload["leveraged_funds_short"] == 9276


def test_weekly_changes_are_exact():
    payload = build_governed_history_payload(
        RAW_DIR,
        ETH,
    )

    assert payload["asset_managers_change_long"] == -303
    assert payload["asset_managers_change_short"] == 711

    assert payload["leveraged_funds_change_long"] == -691
    assert payload["leveraged_funds_change_short"] == -1599


def test_no_synthetic_values():
    payload = build_governed_history_payload(
        RAW_DIR,
        ETH,
    )

    assert payload["synthetic_values_used"] is False

    assert (
        payload["weekly_change_source"]
        == "REAL_SAME_MARKET_CONSECUTIVE_CFTC_REPORTS"
    )


def test_micro_ether_not_mixed():
    payload = build_governed_history_payload(
        RAW_DIR,
        ETH,
    )

    assert payload["market_code"] == "146021"

    assert payload["market_name"] == (
        "ETHER CASH SETTLED - "
        "CHICAGO MERCANTILE EXCHANGE"
    )

    assert all(
        report_date != ""
        for report_date in payload["history_dates"]
    )
