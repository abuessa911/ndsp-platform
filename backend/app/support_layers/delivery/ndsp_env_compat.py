import os

def env_any(*names: str, default: str = "") -> str:
    for name in names:
        value = os.getenv(name, "").strip()
        if value:
            return value
    return default

def telegram_token() -> str:
    return env_any(
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_TOKEN",
        "BOT_TOKEN"
    )

def telegram_chat_id() -> str:
    return env_any(
        "TELEGRAM_CHAT_ID",
        "OWNER_TELEGRAM_CHAT_ID",
        "CHAT_ID"
    )

def telegram_chat_ids() -> str:
    return env_any(
        "TELEGRAM_CHAT_IDS",
        "TELEGRAM_CHAT_ID",
        "OWNER_TELEGRAM_CHAT_ID",
        "CHAT_ID"
    )

def smtp_host() -> str:
    return env_any("SMTP_HOST", "EMAIL_HOST")

def smtp_port() -> str:
    return env_any(
        "SMTP_PORT",
        "EMAIL_PORT",
        default="587"
    )

def smtp_user() -> str:
    return env_any("SMTP_USER", "EMAIL_USER")

def smtp_password() -> str:
    return env_any(
        "SMTP_PASSWORD",
        "SMTP_PASS",
        "EMAIL_PASSWORD",
        "EMAIL_PASS"
    )

def smtp_from() -> str:
    return env_any(
        "SMTP_FROM",
        "EMAIL_FROM",
        "SMTP_USER",
        "EMAIL_USER"
    )

def smtp_to() -> str:
    return env_any(
        "SMTP_TO",
        "ALERT_EMAIL_TO",
        "OWNER_EMAIL"
    )
