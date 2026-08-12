#!/usr/bin/env bash

main() {
  ROOT="/home/nawaf511/empire-core-new"
  SRC="$ROOT/frontend/public-landing/assets/ndsp-register-v1.js"
  DST="/var/www/ndsp-my/assets/ndsp-register-v1.js"

  if [ ! -f "$SRC" ]; then
    echo "SOURCE_MISSING=$SRC"
    return 1
  fi

  if [ ! -f "$DST" ]; then
    echo "DESTINATION_MISSING=$DST"
    return 1
  fi

  node --check "$SRC" || return 1

  OWNER="$(stat -c "%U" "$DST")"
  GROUP="$(stat -c "%G" "$DST")"
  MODE="$(stat -c "%a" "$DST")"
  BACKUP="/tmp/ndsp-register-v1.before-deploy.$(date -u +%Y%m%dT%H%M%SZ).js"

  cp "$DST" "$BACKUP" || return 1
  echo "BACKUP=$BACKUP"

  sudo install -o "$OWNER" -g "$GROUP" -m "$MODE" "$SRC" "$DST" || return 1

  SRC_SHA="$(sha256sum "$SRC" | awk "{print \$1}")"
  DST_SHA="$(sha256sum "$DST" | awk "{print \$1}")"

  echo "SOURCE_SHA=$SRC_SHA"
  echo "DEPLOYED_SHA=$DST_SHA"

  if [ "$SRC_SHA" != "$DST_SHA" ]; then
    echo "DEPLOY_HASH_GATE=FAIL"
    return 1
  fi

  echo "DEPLOY_HASH_GATE=PASS"
  return 0
}

main "$@"
