# NDSP Governance Registry

Official internal governance registry for NDSP — Nawaf Decision Support Platform.

## Canonical Runtime Model

- Public site: /var/www/ndsp
- User portal: /var/www/ndsp-my
- Admin console: /var/www/ndsp-admin
- Nginx config: /etc/nginx/sites-available/00-ndsp-active.conf
- Enabled Nginx link: /etc/nginx/sites-enabled/00-ndsp-active.conf
- API service: ndsp-api.service
- API runtime port: 9001
- Official API namespace: /api
- Retired API namespace: /api/v7 returns 404
- PostgreSQL runtime DB: ndsp_auth
- DB env: /etc/ndsp/ndsp-db.env
- Telegram env: /etc/ndsp/ndsp-telegram.env

## Mandatory Rules

1. Do not expose secrets in public roots.
2. Do not use /api/v7 in UI or new integrations.
3. Do not create additional PostgreSQL runtime databases for NDSP.
4. Do not bypass the canonical Nginx file.
5. Do not modify quarantined /var/www paths except for emergency recovery.
6. Do not describe NDSP as a trading bot, execution platform, or financial recommendation system.
7. Legal acknowledgment must appear before entering the system unless accepted in browser.
8. Snapshots must include SHA256 and manifest verification.
