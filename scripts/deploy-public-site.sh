#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/home/nawaf511/empire-core-new"
APP="$ROOT/apps/public-site"
DIST="$APP/dist"
WEBROOT="/var/www/ndsp/landing"
BACKUP="/var/www/ndsp/landing_backup_$(date +%Y%m%d_%H%M%S)"

cd "$APP"
npm run build

if [ ! -d "$DIST" ]; then
  echo "ERROR: Astro dist not found: $DIST"
  exit 1
fi

if [ -d "$WEBROOT" ]; then
  sudo cp -a "$WEBROOT" "$BACKUP"
fi

sudo mkdir -p "$WEBROOT"
sudo rsync -a --delete "$DIST"/ "$WEBROOT"/
sudo chown -R www-data:www-data "$WEBROOT"

sudo nginx -t
sudo systemctl reload nginx

curl -kI https://ndsp.app | head -20 || true

echo "Published public site to $WEBROOT"
echo "Backup: $BACKUP"
