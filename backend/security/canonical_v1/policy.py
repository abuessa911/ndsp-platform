from __future__ import annotations

def validate_secret_reference(value):
    raw=str(value or "")
    embedded=raw.startswith(("sk-","api_","token_")) or len(raw)>120
    return {
        "status":"REJECTED_EMBEDDED_SECRET" if embedded else "REFERENCE_ACCEPTED",
        "accepted":not embedded,
        "rule":"secrets_must_use_environment_or_secret_manager_references",
    }
