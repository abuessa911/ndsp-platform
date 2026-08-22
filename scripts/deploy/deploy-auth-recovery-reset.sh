#!/usr/bin/env bash

ROOT="/home/nawaf511/empire-core-v5-1-1-clean"
SOURCE="$ROOT/frontend/auth-recovery/reset-password.html"
TARGET="/var/www/html/reset-password.html"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$ROOT/ndsp-platform/var/backups/auth-recovery-reset-$STAMP"

if [ ! -f "$SOURCE" ]; then
    echo "SOURCE_NOT_FOUND=$SOURCE"
    exit 1
fi

mkdir -p "$BACKUP"

if sudo test -f "$TARGET"; then
    sudo cp "$TARGET" "$BACKUP/reset-password.html.before"
fi

echo "BACKUP=$BACKUP"
echo "DEPLOY_SOURCE=$SOURCE"
echo "DEPLOY_TARGET=$TARGET"

sudo install -o root -g root -m 0644 "$SOURCE" "$TARGET"

SOURCE_HASH="$(sha256sum "$SOURCE" | awk '{print $1}')"
TARGET_HASH="$(sudo sha256sum "$TARGET" | awk '{print $1}')"

echo "SOURCE_HASH=$SOURCE_HASH"
echo "TARGET_HASH=$TARGET_HASH"

if [ "$SOURCE_HASH" != "$TARGET_HASH" ]; then
    echo "SOURCE_PRODUCTION_MATCH=FAIL"
    exit 1
fi

echo "SOURCE_PRODUCTION_MATCH=PASS"

PAGE="$(curl -sS https://ndsp.app/reset-password.html)"

if printf "%s" "$PAGE" | grep -Fq 'fetch("/ndsp-rp/reset", {'; then
    echo "PRODUCTION_RESET_ENDPOINT=PASS"
else
    echo "PRODUCTION_RESET_ENDPOINT=FAIL"
    exit 1
fi

BRIDGE_BODY="$(mktemp)"
BRIDGE_HTTP="$(curl -sS -o "$BRIDGE_BODY" -w "%{http_code}" -H "Content-Type: application/json" --data "{}" https://ndsp.app/ndsp-rp/reset)"

echo "RESET_BRIDGE_HTTP=$BRIDGE_HTTP"
cat "$BRIDGE_BODY"

if [ "$BRIDGE_HTTP" = "400" ] && grep -Fq "Email is required" "$BRIDGE_BODY"; then
    echo "RESET_BRIDGE_ROUTING=PASS"
else
    echo "RESET_BRIDGE_ROUTING=FAIL"
    rm -f "$BRIDGE_BODY"
    exit 1
fi

rm -f "$BRIDGE_BODY"

echo "AUTH_RECOVERY_RESET_DEPLOY=PASS"
echo "NO_NGINX_RELOAD"
echo "NO_SERVICE_RESTART"
