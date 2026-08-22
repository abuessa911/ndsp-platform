# NDSP Canonical Live Consumer V5.2

- Timestamp: 20260712_152819
- Backup: /home/nawaf511/ndsp_backend_backups/canonical-live-consumer-v5-2-20260712_152819
- Canonical source: backend/layers/canonical_v1
- Legacy orchestrator: converted to canonical run_all_layers consumer
- NMP wrapper: canonical NMP extreme-selection consumer
- Golden wrapper: canonical AM/LF direction-rule consumer
- Confirmed live chain: 9057 -> 9067 -> 9082
- Systemd PYTHONPATH: /home/nawaf511/empire-core-new
- Systemd WorkingDirectory: /home/nawaf511/empire-core-new
- Restart order: Golden 9067, then NMP 9082
- Port 9083: unrelated ndsp-v52-contract, not modified
- Golden legacy quality heuristic: overridden
- Enhanced Golden uses LF overall: NO
- Unit tests: 11
- NMP service restarted: YES
- Golden service restarted: YES
- API gateway modified: NO
- API gateway restarted: NO
- Database modified: NO
- Nginx modified: NO

## SHA-256 after integration

- layer_orchestrator.py: 553792bb37f4d2ca5db6bb634c2c44c5818695d2812949c0b615c20373f9da11
- ndsp_quality_live_nmp_wrapper.py: d3f066f0f5b3c0d74dd4d29057e92b97dc539a4b4a3aa802711fb4ef478dfd68
- ndsp_quality_live_golden_wrapper.py: 2e0333d65d952f96b67f5d331cfa566ff9289697c45e6e2050ffe49ab6cc0b79
- runtime_bridge.py: f9ac19acd4f7e79d5e4c60f69bb9c32c104fc838324bf831b24ca715737ac85e

## Rollback

Restore the four files from:
/home/nawaf511/ndsp_backend_backups/canonical-live-consumer-v5-2-20260712_152819/project

Then restart:
- ndsp-quality-live-nmp-wrapper.service
- ndsp-quality-live-golden-wrapper.service

FINAL_STATUS=NDSP_CANONICAL_LIVE_CONSUMER_V5_2_OK
