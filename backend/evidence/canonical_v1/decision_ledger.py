from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone

def append_record(*, payload, previous_hash=None):
    canonical=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False)
    payload_hash=hashlib.sha256(canonical.encode()).hexdigest()
    chain_input=f"{previous_hash or 'GENESIS'}:{payload_hash}".encode()
    record_hash=hashlib.sha256(chain_input).hexdigest()
    return {
        "append_only":True,
        "created_at":datetime.now(timezone.utc).isoformat(),
        "previous_hash":previous_hash,
        "payload_hash":payload_hash,
        "record_hash":record_hash,
        "payload":payload,
    }

def verify_record(record):
    payload=record.get("payload")
    canonical=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False)
    payload_hash=hashlib.sha256(canonical.encode()).hexdigest()
    expected=hashlib.sha256(
        f"{record.get('previous_hash') or 'GENESIS'}:{payload_hash}".encode()
    ).hexdigest()
    return payload_hash==record.get("payload_hash") and expected==record.get("record_hash")
