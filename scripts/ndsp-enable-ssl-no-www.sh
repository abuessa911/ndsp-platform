set -Eeuo pipefail

sudo nginx -t

sudo certbot --nginx \
  --expand \
  -d ndsp.app \
  -d my.ndsp.app \
  --redirect \
  --agree-tos \
  -m admin@ndsp.app \
  --non-interactive

sudo nginx -t
sudo systemctl reload nginx

curl -I https://ndsp.app || true
curl -I https://my.ndsp.app || true

curl -sL https://ndsp.app | grep -E "نواف|Nawaf|NAWAF|nawaf" || echo "https://ndsp.app clean"
curl -sL https://my.ndsp.app | grep -E "نواف|Nawaf|NAWAF|nawaf" || echo "https://my.ndsp.app clean or no static hit"
