FORBIDDEN_PUBLIC_KEYS = {
    "admin_key",
    "token_secret",
    "database_url",
    "raw_formula",
    "internal_weight",
    "stack_trace",
}

def sanitize_public_payload(payload: dict) -> dict:
    safe = {}
    for key, value in payload.items():
        if key in FORBIDDEN_PUBLIC_KEYS:
            continue
        if isinstance(value, dict):
            safe[key] = sanitize_public_payload(value)
        else:
            safe[key] = value
    return safe
