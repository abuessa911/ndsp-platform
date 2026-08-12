from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class CotMarketIdentity:
    market_name: str
    market_code: str
    exchange: str


@dataclass(frozen=True)
class CotPositionSnapshot:
    identity: CotMarketIdentity
    report_date: date

    asset_managers_long: int
    asset_managers_short: int

    leveraged_funds_long: int
    leveraged_funds_short: int

    source_file: str


@dataclass(frozen=True)
class CotWeeklyChange:
    current_report_date: date
    previous_report_date: date

    asset_managers_change_long: int
    asset_managers_change_short: int

    leveraged_funds_change_long: int
    leveraged_funds_change_short: int

    source: str = "REAL_SAME_MARKET_CONSECUTIVE_CFTC_REPORTS"
    synthetic_values_used: bool = False


class CotHistoryError(RuntimeError):
    pass


def _int(value: str) -> int:
    return int(str(value).replace(",", "").strip())


def _date(value: str) -> date:
    return datetime.strptime(
        str(value).strip(),
        "%Y-%m-%d",
    ).date()


def _read_snapshot(
    path: Path,
    target: CotMarketIdentity,
) -> Optional[CotPositionSnapshot]:

    with path.open(
        "r",
        errors="replace",
        newline="",
    ) as fh:

        reader = csv.reader(fh)

        for row in reader:

            if len(row) <= 15:
                continue

            market_name = str(row[0]).strip()
            market_code = str(row[3]).strip()
            exchange = str(row[4]).strip()

            if market_name != target.market_name:
                continue

            if market_code != target.market_code:
                continue

            if exchange != target.exchange:
                continue

            try:
                report_date = _date(row[2])

                return CotPositionSnapshot(
                    identity=target,
                    report_date=report_date,

                    asset_managers_long=_int(row[11]),
                    asset_managers_short=_int(row[12]),

                    leveraged_funds_long=_int(row[14]),
                    leveraged_funds_short=_int(row[15]),

                    source_file=str(path),
                )

            except (ValueError, IndexError):
                continue

    return None


def discover_same_market_history(
    raw_dir: Path,
    target: CotMarketIdentity,
) -> list[CotPositionSnapshot]:

    if not raw_dir.exists():
        raise CotHistoryError(
            "RAW_COT_DIRECTORY_NOT_FOUND"
        )

    candidates = sorted(
        path
        for path in raw_dir.glob("*FinFutWk*.txt")
        if path.is_file()
    )

    snapshots: list[CotPositionSnapshot] = []

    for path in candidates:

        snapshot = _read_snapshot(
            path,
            target,
        )

        if snapshot is not None:
            snapshots.append(snapshot)

    # One canonical record for each distinct report date.
    by_date: dict[date, CotPositionSnapshot] = {}

    for snapshot in snapshots:

        existing = by_date.get(
            snapshot.report_date
        )

        if existing is None:
            by_date[snapshot.report_date] = snapshot
            continue

        current_name = Path(
            snapshot.source_file
        ).name

        existing_name = Path(
            existing.source_file
        ).name

        # If the same report exists in both an archived file
        # and the canonical current file, prefer the current file.
        if (
            current_name
            == "current_tff_futures_only_FinFutWk.txt"
            and existing_name != current_name
        ):
            by_date[snapshot.report_date] = snapshot

    history = [
        by_date[report_date]
        for report_date in sorted(
            by_date.keys(),
            reverse=True,
        )
    ]

    return history


def derive_weekly_change(
    history: list[CotPositionSnapshot],
) -> CotWeeklyChange:

    if len(history) < 2:
        raise CotHistoryError(
            "NO_TWO_DISTINCT_REPORT_DATES_FOR_EXACT_SAME_MARKET"
        )

    current = history[0]
    previous = history[1]

    if current.identity != previous.identity:
        raise CotHistoryError(
            "MARKET_IDENTITY_MISMATCH"
        )

    if current.report_date == previous.report_date:
        raise CotHistoryError(
            "REPORT_DATES_NOT_DISTINCT"
        )

    return CotWeeklyChange(
        current_report_date=current.report_date,
        previous_report_date=previous.report_date,

        asset_managers_change_long=(
            current.asset_managers_long
            - previous.asset_managers_long
        ),

        asset_managers_change_short=(
            current.asset_managers_short
            - previous.asset_managers_short
        ),

        leveraged_funds_change_long=(
            current.leveraged_funds_long
            - previous.leveraged_funds_long
        ),

        leveraged_funds_change_short=(
            current.leveraged_funds_short
            - previous.leveraged_funds_short
        ),
    )


def build_governed_history_payload(
    raw_dir: Path,
    target: CotMarketIdentity,
) -> dict:

    history = discover_same_market_history(
        raw_dir,
        target,
    )

    if not history:
        raise CotHistoryError(
            "NO_EXACT_MARKET_HISTORY"
        )

    current = history[0]

    weekly = derive_weekly_change(
        history
    )

    return {
        "market_name": target.market_name,
        "market_code": target.market_code,
        "exchange": target.exchange,

        "report_date": str(
            current.report_date
        ),

        "previous_report_date": str(
            weekly.previous_report_date
        ),

        "asset_managers_long":
            current.asset_managers_long,

        "asset_managers_short":
            current.asset_managers_short,

        "asset_managers_change_long":
            weekly.asset_managers_change_long,

        "asset_managers_change_short":
            weekly.asset_managers_change_short,

        "leveraged_funds_long":
            current.leveraged_funds_long,

        "leveraged_funds_short":
            current.leveraged_funds_short,

        "leveraged_funds_change_long":
            weekly.leveraged_funds_change_long,

        "leveraged_funds_change_short":
            weekly.leveraged_funds_change_short,

        "weekly_change_source":
            weekly.source,

        "synthetic_values_used":
            weekly.synthetic_values_used,

        "history_depth":
            len(history),

        "history_dates": [
            str(snapshot.report_date)
            for snapshot in history
        ],

        "current_source_file":
            current.source_file,
    }
