from __future__ import annotations

import json
from datetime import date
from pathlib import Path

########################################
# NDSP timing_model DATA PROVIDER
# FINAL FIXED VERSION 🔥
########################################

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANUAL_TDL_FILE = PROJECT_ROOT / "config" / "manual_tdl_weekly.json"


# =========================
# HELPERS
# =========================
def _safe_dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def _symbol_id(symbol: str) -> str:
    return str(symbol or "").upper().replace("-SPOT", "").strip()


def _num(value, default=0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def _net(group: dict) -> float:
    group = _safe_dict(group)
    return _num(group.get("long")) - _num(group.get("short"))


# =========================
# GROUP CALCULATION
# =========================
def _lm_total_from_groups(groups: dict, report_type: str = "disaggregated") -> float:
    groups = _safe_dict(groups)
    report_type = str(report_type or "disaggregated").lower().strip()

    if report_type == "legacy":
        return _net(groups.get("commercial"))

    return (
        _net(groups.get("asset_managers"))
        + _net(groups.get("other_reportables"))
    )


def _s_total_from_groups(groups: dict, report_type: str = "disaggregated") -> float:
    groups = _safe_dict(groups)
    report_type = str(report_type or "disaggregated").lower().strip()

    if report_type == "legacy":
        return _net(groups.get("non_commercial"))

    return (
        _net(groups.get("leveraged_funds"))
        + _net(groups.get("dealers"))
    )


def _direction(score: float) -> str:
    if score > 0:
        return "bullish"
    if score < 0:
        return "bearish"
    return "neutral"


# =========================
# DATE CHECK
# =========================
def _date_in_range(valid_from: str | None, valid_to: str | None) -> bool:
    today = date.today()

    try:
        if valid_from and today < date.fromisoformat(valid_from):
            return False
    except Exception:
        pass

    try:
        if valid_to and today > date.fromisoformat(valid_to):
            return False
    except Exception:
        pass

    return True


# =========================
# LOAD MANUAL FILE
# =========================
def _load_manual_weekly(symbol: str) -> dict:
    symbol_clean = _symbol_id(symbol)

    if not MANUAL_TDL_FILE.exists():
        return {}

    try:
        data = json.loads(MANUAL_TDL_FILE.read_text())
    except Exception:
        return {}

    row = _safe_dict(data.get(symbol_clean))
    if not row:
        return {}

    if not _date_in_range(row.get("valid_from"), row.get("valid_to")):
        row = dict(row)
        row["expired"] = True
        return row

    return row


# =========================
# CONVERT TO timing_model 🔥
# =========================
def _manual_weekly_to_tdl_fields(row: dict) -> dict:
    row = _safe_dict(row)

    current = _safe_dict(row.get("current"))
    previous = _safe_dict(row.get("previous"))
    report_type = str(row.get("report_type", "disaggregated")).lower().strip()

    lm_current_total = _lm_total_from_groups(current, report_type)
    lm_previous_total = _lm_total_from_groups(previous, report_type)
    lm_change = lm_current_total - lm_previous_total if previous else 0.0

    s_current_total = _s_total_from_groups(current, report_type)
    s_previous_total = _s_total_from_groups(previous, report_type)
    s_change = s_current_total - s_previous_total if previous else 0.0

    return {
        "manual_lm": {
            "tdl_lm_score_total": lm_current_total,
            "tdl_lm_score_change": lm_change,
            "tdl_lm_direction": _direction(lm_current_total),
            "tdl_lm_change_direction": _direction(lm_change),
        },
        "manual_s": {
            "tdl_s_score_total": s_current_total,
            "tdl_s_score_change": s_change,
            "tdl_s_direction": _direction(s_current_total),
            "tdl_s_change_direction": _direction(s_change),
        },
    }


# =========================
# MAIN FUNCTION
# =========================
def build_tdl_data(symbol: str, market: dict = None, manual: dict = None):

    symbol_clean = _symbol_id(symbol)

    # =========================
    # LOAD MANUAL
    # =========================
    manual_weekly = _load_manual_weekly(symbol_clean)

    # 🔥 FIX الأساسي هنا
    if manual_weekly:
        if "current" in manual_weekly:
            # JSON مباشر (وضعك الحالي)
            manual_weekly_fields = _manual_weekly_to_tdl_fields(manual_weekly)
        else:
            # wrapper
            manual_weekly_fields = _manual_weekly_to_tdl_fields(
                _safe_dict(manual_weekly.get("manual_weekly"))
            )
    else:
        manual_weekly_fields = {}

    # =========================
    # OUTPUT
    # =========================
    return {
        "symbol": symbol_clean,
        "market": market or {},
        **manual_weekly_fields,
    }
