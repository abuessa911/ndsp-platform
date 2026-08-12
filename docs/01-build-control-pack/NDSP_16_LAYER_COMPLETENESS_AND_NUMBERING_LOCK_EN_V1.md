# NDSP 16-Layer Completeness and Numbering Lock — V1

No layer package may be installed, executed, or integrated unless:

1. Exactly 16 layers exist.
2. IDs are contiguous from NDSP-CORE-L01 through NDSP-CORE-L16.
3. Each ID has one canonical name matching the governing registry.
4. Each layer has one canonical source module.
5. No layer is hidden inside a generic file or replaced by another number.
6. Missing L07, L09, or any other layer fails the build immediately.
7. The governing registry is authoritative; memory and legacy filenames are not.

Governing source:
`docs/03-contracts/NDSP_16_LAYER_CORE_REGISTRY_V1.json`

Failure state:
`LAYER_REGISTRY_LOCK_FAILED`
