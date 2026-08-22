set -Eeuo pipefail

echo "NDSP SSL setup"

echo "1) Check nginx..."
sudo nginx -t

echo
echo "2) Check port 80 locally..."
curl -I http://ndsp.app || true
curl -I http://my.ndsp.app || true

echo
echo "3) Existing certificates..."
sudo certbot certificates || true

echo
echo "4) Request/expand certificate..."
sudo certbot --nginx \
  --expand \
  -d ndsp.app \
  -d www.ndsp.app \
  -d my.ndsp.app \
  --redirect \
  --agree-tos \
  -m admin@ndsp.app \
  --non-interactive

echo
echo "5) Test nginx after certbot..."
sudo nginx -t

echo
echo "6) Reload nginx..."
sudo systemctl reload nginx

echo
echo "7) Verify HTTPS..."
curl -I https://ndsp.app || true
curl -I https://www.ndsp.app || true
curl -I https://my.ndsp.app || true

echo
echo "8) Verify no old public name leaks..."
curl -sL https://ndsp.app | grep -E "نواف|Nawaf|NAWAF|nawaf" || echo "https://ndsp.app clean"
curl -sL https://my.ndsp.app | grep -E "نواف|Nawaf|NAWAF|nawaf" || echo "https://my.ndsp.app clean or no static hit"

echo
echo "DONE"
