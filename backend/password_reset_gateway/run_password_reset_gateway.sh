#!/usr/bin/env bash
set -euo pipefail
set +H

ROOT="$HOME/empire-core-new/backend"
RESET_DIR="$ROOT/password_reset_gateway"

for f in \
  "$RESET_DIR/.env" \
  "$ROOT/auth_api/.env" \
  "$ROOT/.env" \
  "$HOME/empire-core-new/.env" \
  "$HOME/.env"
do
  if [ -f "$f" ]; then
    set -a
    . "$f" || true
    set +a
  fi
done

cd "$RESET_DIR"
exec /usr/bin/node server.js
