from __future__ import annotations
import hashlib, json

def workflow_event(*, event_type, aggregate_id, payload, contract_version):
    body={
        "event_type":event_type,
        "aggregate_id":aggregate_id,
        "payload":payload,
        "contract_version":contract_version,
    }
    body["idempotency_key"]=hashlib.sha256(
        json.dumps(body,sort_keys=True,separators=(",",":")).encode()
    ).hexdigest()
    return body

def recovery_manifest(*, backup_id, included_snapshots, included_ledgers, verified):
    return {
        "backup_id":backup_id,
        "included_snapshots":list(included_snapshots),
        "included_ledgers":list(included_ledgers),
        "restore_test_required":True,
        "verified":bool(verified),
    }
