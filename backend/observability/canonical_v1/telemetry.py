from __future__ import annotations

def decision_trace_attributes(*, decision_id, internal_asset_id, analysis_mode,
                              engine_version, layer_id=None, data_status=None):
    return {
        "ndsp.decision_id":decision_id,
        "ndsp.asset_id":internal_asset_id,
        "ndsp.analysis_mode":analysis_mode,
        "ndsp.engine_version":engine_version,
        "ndsp.layer_id":layer_id,
        "ndsp.data_status":data_status,
    }
