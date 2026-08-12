# NDSP V1.4 / P4 Implementation Plan — 20260709_082445

## Baseline

- V1.3 D5 lock reconciled if missing.
- Current runtime is clean.
- First practical problem: completed-decisions API/source discovery.

## Sequence

### V14-A — Completed Decisions Source Discovery READ ONLY
Find the real service/path/data source. No runtime changes.

### V14-B — Read-only Adapter
Only after V14-A. One small adapter/proxy/static JSON. No DB mutation.

### V14-C — Portal Link Integration
Add safe links/hub without touching protected assets.

### V14-D — Copy/Error State Polish
Arabic UX copy only. No engine logic.

### V14-E — Final Audit + Package
Create final package and SHA256.

## Stop conditions

Stop if:
- systemctl --failed > 0
- nginx -t fails
- PM2 not active/enabled
- core endpoints fail
- protected asset checksum changes
