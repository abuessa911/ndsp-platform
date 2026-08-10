#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/nawaf511/empire-core-new"
SOURCE="$ROOT/infrastructure/nginx/000-ndsp-app-public-canonical-only.conf"
TARGET="/etc/nginx/conf.d/000-ndsp-app-public-canonical-only.conf"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$ROOT/ndsp-platform/var/backups/nginx-canonical-$STAMP"
BACKUP="$BACKUP_DIR/000-ndsp-app-public-canonical-only.conf.before"

if [ ! -f "$SOURCE" ]; then
    echo "ERROR: source not found: $SOURCE" >&2
    exit 1
fi

if [ ! -f "$TARGET" ]; then
    echo "ERROR: target not found: $TARGET" >&2
    exit 1
fi

mkdir -p "$BACKUP_DIR"
sudo cp -a "$TARGET" "$BACKUP"

echo "BACKUP=$BACKUP"
echo "DEPLOY_SOURCE=$SOURCE"
echo "DEPLOY_TARGET=$TARGET"

sudo install -m 0644 "$SOURCE" "$TARGET"

if ! sudo nginx -t; then
    echo "NGINX_TEST=FAIL"
    sudo cp -a "$BACKUP" "$TARGET"
    sudo nginx -t
    echo "ROLLBACK=PASS"
    exit 1
fi

echo "NGINX_TEST=PASS"

SOURCE_HASH="$(sha256sum "$SOURCE" | cut -d " " -f1)"
TARGET_HASH="$(sudo sha256sum "$TARGET" | cut -d " " -f1)"

echo "SOURCE_HASH=$SOURCE_HASH"
echo "TARGET_HASH=$TARGET_HASH"

if [ "$SOURCE_HASH" != "$TARGET_HASH" ]; then
    echo "SOURCE_PRODUCTION_MATCH=FAIL"
    sudo cp -a "$BACKUP" "$TARGET"
    sudo nginx -t
    echo "ROLLBACK=PASS"
    exit 1
fi

echo "SOURCE_PRODUCTION_MATCH=PASS"

if ! sudo systemctl reload nginx; then
    echo "NGINX_RELOAD=FAIL"
    sudo cp -a "$BACKUP" "$TARGET"
    sudo nginx -t
    sudo systemctl reload nginx
    echo "ROLLBACK=PASS"
    exit 1
fi

echo "NGINX_RELOAD=PASS"
