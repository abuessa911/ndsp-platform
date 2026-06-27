TDL_DAY_LOGIC_V2 = {
    "version": "TDL_WEEKLY_DAY_LOGIC_V2",
    "status": "ACTIVE_BASELINE",
    "days": {
        "monday": {"controller": "ASSET_MANAGERS", "mode": "weekly_anchor"},
        "tuesday": {"controller": "LEVERAGED_FUNDS", "mode": "tactical_structure"},
        "wednesday": {"controller": "LEVERAGED_FUNDS", "mode": "tactical_structure"},
        "thursday": {"controller": "LEVERAGED_FUNDS", "mode": "tactical_structure"},
        "friday": {"controller": "ASSET_MANAGERS", "mode": "weekly_anchor"},
        "saturday": {"controller": "LEVERAGED_FUNDS", "mode": "crypto_only", "applies_to": ["CRYPTO"]},
        "sunday": {"controller": "LEVERAGED_FUNDS", "mode": "crypto_only", "applies_to": ["CRYPTO"]},
    },
}

DAY_MAP = {
    "mon": "monday", "monday": "monday", "الاثنين": "monday",
    "tue": "tuesday", "tues": "tuesday", "tuesday": "tuesday", "الثلاثاء": "tuesday",
    "wed": "wednesday", "wednesday": "wednesday", "الأربعاء": "wednesday", "الاربعاء": "wednesday",
    "thu": "thursday", "thur": "thursday", "thurs": "thursday", "thursday": "thursday", "الخميس": "thursday",
    "fri": "friday", "friday": "friday", "الجمعة": "friday",
    "sat": "saturday", "saturday": "saturday", "السبت": "saturday",
    "sun": "sunday", "sunday": "sunday", "الأحد": "sunday", "الاحد": "sunday",
}

def normalize_day_name(value):
    return DAY_MAP.get(str(value or "").strip().lower(), str(value or "").strip().lower())

def get_tdl_day_controller(day_name, asset_class=""):
    day = normalize_day_name(day_name)
    cls = str(asset_class or "").strip().upper()
    row = TDL_DAY_LOGIC_V2["days"].get(day)

    if not row:
        return {"ok": False, "controller": "UNKNOWN", "mode": "unknown_day", "day": day, "asset_class": cls}

    if day in ("saturday", "sunday") and cls != "CRYPTO":
        return {"ok": True, "controller": "MARKET_CLOSED_OR_IGNORED", "mode": "non_crypto_weekend", "day": day, "asset_class": cls}

    return {"ok": True, "controller": row["controller"], "mode": row["mode"], "day": day, "asset_class": cls, "version": TDL_DAY_LOGIC_V2["version"]}
