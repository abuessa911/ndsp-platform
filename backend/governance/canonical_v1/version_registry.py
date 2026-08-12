from __future__ import annotations

REQUIRED_VERSION_FIELDS = (
    "engine_version","layer_registry_version","contract_version",
    "data_policy_version","nmp_engine_version","cot_gate_version",
)

def validate_version_manifest(manifest):
    missing=[x for x in REQUIRED_VERSION_FIELDS if not manifest.get(x)]
    return {
        "status":"VALID" if not missing else "VERSION_BLOCKED",
        "decision_use_allowed":not missing,
        "missing":missing,
    }
