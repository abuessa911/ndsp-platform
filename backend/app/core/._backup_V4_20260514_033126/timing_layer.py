from __future__ import annotations

from datetime import datetime, timezone


def run_timing_layer(now=None) -> dict:
    """
    Weekly behavior timing.

    Mon-Wed => timing_model-S Dominant
    Thu-Fri => timing_model-L&M Dominant
    Sat-Sun => OFF_SESSION
    """
    if now is None:
        now = datetime.now(timezone.utc)

    weekday = now.weekday()

    if weekday in (0, 1, 2):
        timing = "Mon-Wed"
        dominant_window = "timing_model-S"
    elif weekday in (3, 4):
        timing = "Thu-Fri"
        dominant_window = "timing_model-L&M"
    else:
        timing = "Weekend"
        dominant_window = "OFF_SESSION"

    return {
        "timing": timing,
        "dominant_window": dominant_window,
        "weekday": weekday,
        "timestamp": now.isoformat(),
    }
