# NDSP Rollback Plan

> NDSP لا تبني شاشة؛ NDSP تبني غرفة قرار.

## Backup Locations
- /home/nawaf511/ndsp_backups
- /home/nawaf511/ndsp_release_packages

## Rollback Rules
- Roll back the exact modified scope only.
- Do not stack new patches over a failed patch.
- After rollback, run page checks and post patch test.
- Record rollback in docs/05-runbooks.

## Protected Recovery
Runtime services are not restarted unless the failed patch touched runtime.
