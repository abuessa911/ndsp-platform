# DEV-012B — Controlled Production Rollout Plan

Generated: 20260628_152255
Branch: feature/ndsp-os
Head: a3a80ff test(DEV-012A): check production rollout readiness
Release Tag: v0.3-ndsp-core-services
Source Readiness Report: /home/nawaf511/empire-core-new/backend/architecture/reports/DEV-012A-PRODUCTION-ROLLOUT-READINESS-CHECK-20260628_152033.md

## Result From DEV-012A

FAIL_COUNT=0
WARN_COUNT=0
READINESS=READY_WITH_REVIEW

## Safety Policy

This plan does not start, stop, reload, or modify production services.

NO_SERVICE_START=YES
NO_SERVICE_STOP=YES
NO_SYSTEMD_CHANGE=YES
NO_NGINX_CHANGE=YES
NO_PRODUCTION_WRITE=YES

## Core Service Rollout Order

1. CTL-001 Workspace Identity — reference service / port 9081
2. CDS-001 Completed Decision Service — SSOT / port 9078
3. DGC-001 Decision Governance Core — governance layer / port 9079
4. BOT-001 NDSP Bot Execution Service — last boundary / port 9080

## Required Production Rollout Gates

Gate 1: Verify service unit files exist for all four services.
Gate 2: Verify each service has an environment file outside git.
Gate 3: Start or restart one service at a time only after config review.
Gate 4: Validate local endpoints after each service:
- GET /health
- GET /version
- GET /about
Gate 5: Validate dependency order:
- CDS before DGC
- DGC before BOT
- BOT remains last
Gate 6: Validate nginx only after local ports are healthy.
Gate 7: Run final public smoke tests only after nginx test passes.

## DEV-012A Warnings To Review

- WARN=BOT-001_about_HTTP_NOT_READY http://127.0.0.1:9080/about
- WARN=BOT-001_SYSTEMD_NOT_ACTIVE
- WARN=BOT-001_SYSTEMD_NOT_ENABLED
- WARN=BOT-001_SYSTEMD_UNIT_FILE_QUERY_FAILED_OR_NOT_INSTALLED
- WARN=BOT-001_version_HTTP_NOT_READY http://127.0.0.1:9080/version
- WARN=CDS-001_SYSTEMD_NOT_ACTIVE
- WARN=CDS-001_SYSTEMD_NOT_ENABLED
- WARN=CDS-001_SYSTEMD_UNIT_FILE_QUERY_FAILED_OR_NOT_INSTALLED
- WARN=CTL-001_SYSTEMD_UNIT_FILE_QUERY_FAILED_OR_NOT_INSTALLED
- WARN=DGC-001_about_HTTP_NOT_READY http://127.0.0.1:9079/about
- WARN=DGC-001_SYSTEMD_NOT_ACTIVE
- WARN=DGC-001_SYSTEMD_NOT_ENABLED
- WARN=DGC-001_SYSTEMD_UNIT_FILE_QUERY_FAILED_OR_NOT_INSTALLED
- WARN=DGC-001_version_HTTP_NOT_READY http://127.0.0.1:9079/version
- WARN=NGINX_CONFIG_TEST_FAILED

## Warnings Interpretation

Warnings do not block rollout because FAIL_COUNT=0.
Most warnings usually mean services are not currently active under systemd, ports are not listening yet, or nginx routes are not enabled.
These are expected before a controlled production rollout.

## Do Not Do

- Do not bulk restart all services.
- Do not reload nginx before nginx -t passes.
- Do not expose BOT before CDS and DGC pass local health.
- Do not enable real order routing during rollout.
- Do not store real secrets in git.

## Recommended Next Step

DEV-012C — systemd unit installation and local-only activation plan.
This next step should still be conservative and should not expose public routes yet.
