import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.contracts.canonical.semantic_contract import (
    CanonicalValue,
    validate_missing_semantics,
)

from backend.app.contracts.assets.source_routing_contract import (
    SourceRoute,
    validate_source_route,
)

from backend.app.contracts.market_data.market_data_contract import (
    Freshness,
    validate_freshness,
)

from backend.app.contracts.cot.cot_tff_contract import (
    BULLISH,
    BEARISH,
    direction_from_long_short,
    weekly_direction_from_changes,
    extract_group_numbers,
)


def test_missing_is_not_silent():
    x = CanonicalValue(
        field_id="x",
        value=None,
        data_type="number",
        semantic_role="TEST",
        complete=False,
        missing_reason="SOURCE_MISSING",
    )
    validate_missing_semantics(x)


def test_unknown_asset_class_blocked():
    route = SourceRoute(
        asset="X",
        asset_class="unknown",
        source_market=None,
        source_timeframe="weekly",
        analysis_timeframe="weekly",
    )

    try:
        validate_source_route(route)
    except ValueError:
        return

    raise AssertionError("UNKNOWN asset_class must be blocked")


def test_overall_direction():
    d, _ = direction_from_long_short(120, 100)
    assert d == BULLISH

    d, _ = direction_from_long_short(80, 100)
    assert d == BEARISH


def test_weekly_direction():
    d, _ = weekly_direction_from_changes(25, -10)
    assert d == BULLISH

    d, _ = weekly_direction_from_changes(-20, 5)
    assert d == BEARISH


def test_alias_extraction():
    payload = {
        "asset_managers_positions_long": "1,200",
        "asset_managers_positions_short": "900",
        "asset_managers_weekly_change_long": 50,
        "asset_managers_weekly_change_short": -20,
    }

    x = extract_group_numbers(
        payload,
        "asset_managers",
    )

    assert x.long == "1,200"
    assert x.short == "900"
    assert x.change_long == 50
    assert x.change_short == -20
    assert x.has_current_totals is True
    assert x.has_weekly_changes is True


def test_freshness():
    x = Freshness(
        report_date="2026-08-01",
        report_age_days=7,
        max_age_days=10,
        fresh=True,
    )
    validate_freshness(x)
