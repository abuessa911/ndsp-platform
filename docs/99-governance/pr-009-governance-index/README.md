# NDSP Governance Index

This package provides a single entry point for the completed 
runtime-governance documentation delivered through PR-004 to PR-008.

## Scope

- Documentation and governance artifacts only.
- No application, deployment, configuration, or runtime changes.
- Source packages remain unchanged.

## Governance packages

| Package | Area | Status | Files | Primary artifact |
|---|---|---:|---:|---|
| PR-004 | Runtime Dependency Map | COMPLETE | 8 | [FINAL_RUNTIME_DEPENDENCY_MAP.json](../pr-004-runtime-dependency-map/FINAL_RUNTIME_DEPENDENCY_MAP.json) |
| PR-005 | Runtime Ownership Map | COMPLETE | 5 | [FINAL_RUNTIME_OWNERSHIP_MAP.json](../pr-005-runtime-ownership-map/FINAL_RUNTIME_OWNERSHIP_MAP.json) |
| PR-006 | Network Exposure Map | COMPLETE | 5 | [FINAL_NETWORK_EXPOSURE_MAP.json](../pr-006-network-exposure-map/FINAL_NETWORK_EXPOSURE_MAP.json) |
| PR-007 | Noncanonical Ownership Review | COMPLETE | 5 | [FINAL_NONCANONICAL_OWNERSHIP_MAP.json](../pr-007-noncanonical-ownership/FINAL_NONCANONICAL_OWNERSHIP_MAP.json) |
| PR-008 | Governance Closure | COMPLETE | 4 | [PR-008-COMMIT-MANIFEST.json](../pr-008-governance-closure/PR-008-COMMIT-MANIFEST.json) |

## Package descriptions

### PR-004 — Runtime Dependency Map

Canonical map of runtime components, dependencies, configuration evidence, and noncanonical edges.

Directory: [pr-004-runtime-dependency-map](../pr-004-runtime-dependency-map/)

### PR-005 — Runtime Ownership Map

Ownership classification for runtime components and supporting ownership-review evidence.

Directory: [pr-005-runtime-ownership-map](../pr-005-runtime-ownership-map/)

### PR-006 — Network Exposure Map

Documented listener, binding, protocol, ownership, and network exposure inventory.

Directory: [pr-006-network-exposure-map](../pr-006-network-exposure-map/)

### PR-007 — Noncanonical Ownership Review

Final ownership decisions for noncanonical components, including promotion, shared infrastructure, and deprecation.

Directory: [pr-007-noncanonical-ownership](../pr-007-noncanonical-ownership/)

### PR-008 — Governance Closure

Closure summary, commit manifest, merge checklist, and validation evidence for PR-004 through PR-008.

Directory: [pr-008-governance-closure](../pr-008-governance-closure/)

## Machine-readable index

See [`GOVERNANCE_INDEX.json`](GOVERNANCE_INDEX.json) for the 
complete package and file inventory.

## Integrity

See [`PR009_SHA256SUMS.txt`](PR009_SHA256SUMS.txt) for SHA-256 
checksums covering the PR-009 index artifacts.

## Final status

- PR-004 through PR-008: complete
- PR-009 governance index: complete
- Runtime changes: none
