# NDSP Binding Table

## Creative pages

| Page | URL | Server path | Status |
|---|---|---|---|
| Dashboard | https://my.ndsp.app/pages/dashboard.html | /var/www/ndsp-my/pages/dashboard.html | Bound |
| User-side admin | https://my.ndsp.app/pages/admin.html | /var/www/ndsp-my/pages/admin.html | Bound |

## Legal acknowledgment assets

| Asset | URL | Server path |
|---|---|---|
| JS — الرئيسي | https://ndsp.app/assets/ndsp-entry-ack/ndsp-entry-ack.js | /var/www/ndsp/assets/ndsp-entry-ack/ndsp-entry-ack.js |
| CSS — الرئيسي | https://ndsp.app/assets/ndsp-entry-ack/ndsp-entry-ack.css | /var/www/ndsp/assets/ndsp-entry-ack/ndsp-entry-ack.css |
| JS — بوابة المستخدم | https://my.ndsp.app/assets/ndsp-entry-ack/ndsp-entry-ack.js | /var/www/ndsp-my/assets/ndsp-entry-ack/ndsp-entry-ack.js |
| CSS — بوابة المستخدم | https://my.ndsp.app/assets/ndsp-entry-ack/ndsp-entry-ack.css | /var/www/ndsp-my/assets/ndsp-entry-ack/ndsp-entry-ack.css |

## Backend

| Item | Path | Binding |
|---|---|---|
| server.js الرئيسي | /home/nawaf511/empire-core-new/backend/server.js | Audited |
| auth_api | /home/nawaf511/empire-core-new/backend/auth_api/server.js | Audited |
| routes المضافة | /home/nawaf511/empire-core-new/backend/ndsp_extra_routes.js | Audited |
| API logic | /home/nawaf511/empire-core-new/backend/app/api/ | Bound through ndsp-api.service on port 9001 |
| DB env | /etc/ndsp/ndsp-db.env | Audited masked |
| Telegram env | /etc/ndsp/ndsp-telegram.env | Audited masked |
| Backend .env | /home/nawaf511/empire-core-new/backend/.env | Audited masked |

## Core rules

- Official DB: ndsp_auth
- Official API base: /api
- Retired API namespace: /api/v7 returns 404
