# NDSP Deployment Runbook

> NDSP لا تبني شاشة؛ NDSP تبني غرفة قرار.

## Known Production Values
- PROJECT=/home/nawaf511/empire-core-new
- LIVE_FRONTEND=/var/www/ndsp-my
- FRONTEND_BASE=https://my.ndsp.app
- API_BASE=https://api.ndsp.app
- PM2_SERVICE=ndsp-portal

## Deployment Rule
No production change without:
1. Backup
2. Patch report
3. Post patch test
4. Reality lock update
5. Rollback path

## Protected Runtime
Nginx, PM2, API, backend, radar JS, menu JS, disclaimer JS must not be touched without explicit approval.
