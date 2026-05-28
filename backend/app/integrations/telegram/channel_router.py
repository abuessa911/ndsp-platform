from __future__ import annotations

import os


def get_channel_id(channel: str | None) -> str | None:
    if not channel:
        return None

    channel = channel.lower()

    if channel == "pro":
        return os.getenv("TELEGRAM_PRO_CHANNEL") or os.getenv("TELEGRAM_CHAT_ID")

    if channel in ("vip", "elite"):
        return os.getenv("TELEGRAM_VIP_CHANNEL")

    if channel == "free":
        return os.getenv("TELEGRAM_FREE_CHANNEL")

    return None
