from __future__ import annotations

def build_lineage(*, decision_id, input_snapshot_ids, source_hashes,
                  transform_versions, layer_versions, model_versions):
    return {
        "decision_id":decision_id,
        "input_snapshot_ids":list(input_snapshot_ids),
        "source_hashes":list(source_hashes),
        "transform_versions":list(transform_versions),
        "layer_versions":list(layer_versions),
        "model_versions":list(model_versions),
    }
