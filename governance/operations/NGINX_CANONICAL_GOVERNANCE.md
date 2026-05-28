# NDSP Nginx Canonical Governance

Approved active files:
- /etc/nginx/sites-available/00-ndsp-active.conf
- /etc/nginx/sites-enabled/00-ndsp-active.conf

Approved domains:
- ndsp.app
- my.ndsp.app
- admin.ndsp.app
- api.ndsp.app

Approved roots:
- /var/www/ndsp
- /var/www/ndsp-my
- /var/www/ndsp-admin
- /var/www/html

Policy:
1. Only one active Nginx site should be enabled.
2. All NDSP domains must be served through the canonical config.
3. Nginx must pass nginx -t before reload.
4. /api must proxy to approved backend runtime.
5. /api/v7 must be retired and return 404.
