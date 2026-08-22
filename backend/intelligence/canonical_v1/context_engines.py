from __future__ import annotations

def context_envelope(*, context_type, internal_asset_id, as_of, items):
    return {
        "context_type":context_type,
        "internal_asset_id":internal_asset_id,
        "as_of":as_of,
        "items":list(items),
        "decision_authority":False,
        "role":"context_only",
    }

def cross_asset_influence(*, source_asset_id, target_asset_id, direction,
                          strength, lag, evidence_type="observed_relationship"):
    return {
        "source_asset_id":source_asset_id,
        "target_asset_id":target_asset_id,
        "direction":direction,
        "strength":float(strength),
        "lag":lag,
        "evidence_type":evidence_type,
        "causality_claimed":False,
        "decision_authority":False,
    }
