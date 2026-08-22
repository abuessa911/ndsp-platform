#!/usr/bin/env bash

main() {
  ROOT="/home/nawaf511/empire-core-v5-1-1-clean"
  SRC_INDEX="$ROOT/frontend/user-portal-vite/index.html"
  SRC_CSS="$ROOT/frontend/user-portal-vite/public/v37-mobile-fix.css"
  DST_ROOT="/var/www/ndsp-my/portal"
  DST_INDEX="$DST_ROOT/index.html"
  DST_CSS="$DST_ROOT/v37-mobile-fix.css"
  VERSION="20260811-1"
  LINK="<link rel=\"stylesheet\" href=\"/portal/v37-mobile-fix.css?v=$VERSION\">"
  TMP="/tmp/ndsp-v37-live-$(date -u +%Y%m%dT%H%M%SZ)-$$"

  mkdir -p "$TMP" || return 1

  if [ ! -f "$SRC_INDEX" ] || [ ! -f "$SRC_CSS" ] || [ ! -f "$DST_INDEX" ]; then
    echo "DEPLOY_INPUT_GATE=FAIL"
    return 1
  fi

  if ! grep -Fq "/portal/v37-mobile-fix.css?v=$VERSION" "$SRC_INDEX"; then
    echo "SOURCE_INDEX_LINK_GATE=FAIL"
    return 1
  fi

  if ! grep -Fq ".v37ReasonGrid" "$SRC_CSS"; then
    echo "SOURCE_CSS_GATE=FAIL"
    return 1
  fi

  if [ -e "$DST_CSS" ]; then
    echo "LIVE_CSS_ALREADY_EXISTS=REVIEW_REQUIRED"
    return 1
  fi

  cp "$DST_INDEX" "$TMP/index.before.html" || return 1
  cp "$DST_INDEX" "$TMP/index.candidate.html" || return 1

  if grep -Fq "v37-mobile-fix.css" "$TMP/index.candidate.html"; then
    echo "LIVE_LINK_ALREADY_EXISTS=REVIEW_REQUIRED"
    return 1
  fi

  sed -i "0,/<\/head>/s#</head>#$LINK\n</head>#" "$TMP/index.candidate.html" || return 1

  COUNT="$(grep -Fc "/portal/v37-mobile-fix.css?v=$VERSION" "$TMP/index.candidate.html")"

  if [ "$COUNT" -ne 1 ]; then
    echo "CANDIDATE_LINK_GATE=FAIL"
    return 1
  fi

  OWNER="$(stat -c "%U" "$DST_INDEX")"
  GROUP="$(stat -c "%G" "$DST_INDEX")"
  MODE="$(stat -c "%a" "$DST_INDEX")"

  sudo install -o "$OWNER" -g "$GROUP" -m "$MODE" "$SRC_CSS" "$DST_CSS" || return 1

  sudo install -o "$OWNER" -g "$GROUP" -m "$MODE" "$TMP/index.candidate.html" "$DST_INDEX"
  INDEX_INSTALL=$?

  if [ "$INDEX_INSTALL" -ne 0 ]; then
    sudo rm -f "$DST_CSS"
    echo "LIVE_INDEX_INSTALL=FAIL"
    return 1
  fi

  VERIFY=0

  cmp -s "$SRC_CSS" "$DST_CSS" || VERIFY=1
  grep -Fq "/portal/v37-mobile-fix.css?v=$VERSION" "$DST_INDEX" || VERIFY=1

  if [ "$VERIFY" -ne 0 ]; then
    sudo install -o "$OWNER" -g "$GROUP" -m "$MODE" "$TMP/index.before.html" "$DST_INDEX"
    sudo rm -f "$DST_CSS"
    echo "DEPLOY_VERIFY=FAIL_ROLLBACK_COMPLETE"
    return 1
  fi

  echo "BACKUP=$TMP/index.before.html"
  echo "PORTAL_CSS_DEPLOY=PASS"
  echo "PORTAL_INDEX_LINK_DEPLOY=PASS"
  return 0
}

main "$@"
