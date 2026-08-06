from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Collection
from ..core.contracts import CotValidity, DataGateStatus

@dataclass(frozen=True)
class ExpectedCotCycle:
    report_as_of_date: str
    expected_release_at: datetime
    grace_minutes: int = 90
    official_delay_confirmed: bool = False
    delay_note: str | None = None

@dataclass(frozen=True)
class LatestCotReport:
    report_as_of_date: str
    integrity_passed: bool
    available_markets: frozenset[str]
    business_hash: str | None = None
    previous_business_hash: str | None = None
    source_matches_official: bool = True
    backlog_mode: bool = False

def _aware(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)

def evaluate_cot_validity(
    *, now: datetime, expected_cycle: ExpectedCotCycle,
    latest_report: LatestCotReport | None,
    required_markets: Collection[str] = (),
) -> CotValidity:
    now = _aware(now)
    release_at = _aware(expected_cycle.expected_release_at)
    grace_deadline = release_at.timestamp() + expected_cycle.grace_minutes * 60
    common = {
        "expected_report_as_of_date": expected_cycle.report_as_of_date,
        "expected_release_at": release_at.isoformat(),
    }

    if now < release_at:
        return CotValidity(
            DataGateStatus.EXPECTED_NOT_YET_DUE, True, True,
            latest_report.report_as_of_date if latest_report else None,
            reason_code="CFTC_EXPECTED_NOT_YET_DUE", **common,
        )
    if expected_cycle.official_delay_confirmed:
        return CotValidity(
            DataGateStatus.DELAY_CONFIRMED, False, True,
            latest_report.report_as_of_date if latest_report else None,
            reason_code="CFTC_OFFICIAL_DELAY_CONFIRMED",
            details={"delay_note": expected_cycle.delay_note}, **common,
        )
    if latest_report is None:
        status = (
            DataGateStatus.EXPECTED_RELEASE_WINDOW
            if now.timestamp() <= grace_deadline
            else DataGateStatus.EXPECTED_REPORT_MISSING
        )
        return CotValidity(status, False, True, reason_code=f"CFTC_{status.value}", **common)
    if latest_report.backlog_mode and latest_report.report_as_of_date != expected_cycle.report_as_of_date:
        return CotValidity(
            DataGateStatus.BACKLOG_MODE, False, True, latest_report.report_as_of_date,
            reason_code="CFTC_BACKLOG_NOT_CURRENT_CYCLE", **common,
        )
    if latest_report.report_as_of_date != expected_cycle.report_as_of_date:
        return CotValidity(
            DataGateStatus.STALE, False, True, latest_report.report_as_of_date,
            reason_code="CFTC_REPORT_DATE_DOES_NOT_MATCH_EXPECTED_CYCLE", **common,
        )
    if not latest_report.source_matches_official:
        return CotValidity(
            DataGateStatus.SOURCE_MISMATCH, False, True, latest_report.report_as_of_date,
            reason_code="CFTC_SOURCE_MISMATCH", **common,
        )
    if not latest_report.integrity_passed:
        return CotValidity(
            DataGateStatus.INTEGRITY_FAILED, False, True, latest_report.report_as_of_date,
            reason_code="CFTC_INTEGRITY_FAILED", **common,
        )
    missing = sorted(set(required_markets) - set(latest_report.available_markets))
    if missing:
        return CotValidity(
            DataGateStatus.INCOMPLETE_MARKETS, False, True, latest_report.report_as_of_date,
            reason_code="CFTC_REQUIRED_MARKETS_MISSING",
            details={"missing_markets": missing}, **common,
        )
    if (
        latest_report.business_hash
        and latest_report.previous_business_hash
        and latest_report.business_hash == latest_report.previous_business_hash
    ):
        return CotValidity(
            DataGateStatus.DUPLICATE_PAYLOAD, False, True, latest_report.report_as_of_date,
            reason_code="CFTC_DUPLICATE_BUSINESS_PAYLOAD", **common,
        )
    return CotValidity(
        DataGateStatus.CURRENT, True, True, latest_report.report_as_of_date,
        details={"atomic_snapshot_required": True}, **common,
    )
