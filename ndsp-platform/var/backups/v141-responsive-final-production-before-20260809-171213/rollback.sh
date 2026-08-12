#!/usr/bin/env bash
set -euo pipefail

LIVE="/var/www/ndsp"
BACKUP="/home/nawaf511/empire-core-new/ndsp-platform/var/backups/v141-responsive-final-production-before-20260809-171213"

echo "Restoring NDSP production..."

sudo mkdir -p "$LIVE/assets"

if [ -d "$BACKUP/assets" ]; then
  sudo rsync     -av     --delete     "$BACKUP/assets/"     "$LIVE/assets/"
fi

if [ -f "$BACKUP/index.html" ]; then
  sudo cp     "$BACKUP/index.html"     "$LIVE/index.html"
fi

for file in favicon.svg robots.txt; do
  if [ -f "$BACKUP/$file" ]; then
    sudo cp       "$BACKUP/$file"       "$LIVE/$file"
  fi
done

sudo chown -R   www-data:www-data   "$LIVE"

echo "Rollback complete."
