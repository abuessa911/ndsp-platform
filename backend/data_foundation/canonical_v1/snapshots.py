from __future__ import annotations
import hashlib, json
from datetime import datetime, timezone

def _hash(payload):
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    return hashlib.sha256(raw).hexdigest()

def build_raw_snapshot(*, source_id, internal_asset_id, observed_at, payload):
    envelope={
        "snapshot_type":"RAW",
        "source_id":source_id,
        "internal_asset_id":internal_asset_id,
        "observed_at":observed_at,
        "ingested_at":datetime.now(timezone.utc).isoformat(),
        "payload":payload,
    }
    envelope["content_hash"]=_hash(envelope)
    return envelope

def build_canonical_snapshot(*, raw_snapshot_ids, internal_asset_id, as_of, payload, quality):
    if not quality.get("decision_use_allowed"):
        return {"status":"DATA_BLOCKED","decision_use_allowed":False}
    envelope={
        "snapshot_type":"CANONICAL_ACCEPTED",
        "raw_snapshot_ids":list(raw_snapshot_ids),
        "internal_asset_id":internal_asset_id,
        "as_of":as_of,
        "payload":payload,
        "quality":quality,
    }
    envelope["content_hash"]=_hash(envelope)
    envelope["decision_use_allowed"]=True
    return envelope
