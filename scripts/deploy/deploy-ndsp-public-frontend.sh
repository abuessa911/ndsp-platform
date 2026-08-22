#!/usr/bin/env bash

ROOT="/home/nawaf511/empire-core-v5-1-1-clean/ndsp-platform/frontend/public"
DIST="$ROOT/dist"
LIVE_ROOT="/var/www/ndsp"
LIVE_INDEX="$LIVE_ROOT/index.html"
TMP="/tmp/ndsp-public-managed-deploy-$(date -u +%Y%m%dT%H%M%SZ)-$$"
BACKUP="$TMP/backup"

mkdir -p "$BACKUP"

FINAL=1

echo "===== M1 SOURCE BUILD ====="

(
  cd "$ROOT" &&
  npm run build > "$TMP/build.log" 2>&1
)

BUILD_STATUS=$?

if [ "$BUILD_STATUS" -eq 0 ]; then
  echo "SOURCE_BUILD=PASS"
else
  echo "SOURCE_BUILD=FAIL"
  tail -n 30 "$TMP/build.log" 2>/dev/null
fi

echo
echo "===== M2 BUILD CONTRACT ====="

BUILD_GATE=1

if [ "$BUILD_STATUS" -eq 0 ] &&
   [ -f "$DIST/index.html" ] &&
   [ -d "$DIST/assets" ]; then

  DIST_JS_COUNT="$(find "$DIST/assets" -maxdepth 1 -type f -name "*.js" | wc -l)"
  DIST_CSS_COUNT="$(find "$DIST/assets" -maxdepth 1 -type f -name "*.css" | wc -l)"

  echo "DIST_JS_COUNT=$DIST_JS_COUNT"
  echo "DIST_CSS_COUNT=$DIST_CSS_COUNT"

  if [ "$DIST_JS_COUNT" -gt 0 ] &&
     [ "$DIST_CSS_COUNT" -gt 0 ]; then
    BUILD_GATE=0
    echo "BUILD_CONTRACT_GATE=PASS"
  else
    echo "BUILD_CONTRACT_GATE=FAIL"
  fi
else
  echo "BUILD_CONTRACT_GATE=FAIL"
fi

echo
echo "===== M3 SOURCE FEATURE PROOF ====="

FEATURE_GATE=1

LANG_JS_COUNT="$(grep -RFl "ndsp-public-language" "$DIST/assets" --include="*.js" 2>/dev/null | wc -l)"
TOGGLE_JS_COUNT="$(grep -RFl "Switch to English" "$DIST/assets" --include="*.js" 2>/dev/null | wc -l)"
DIAGRAM_CSS_COUNT="$(grep -RFl ".sovereign-evidence-map--desktop" "$DIST/assets" --include="*.css" 2>/dev/null | wc -l)"
MOBILE_LANG_CSS_COUNT="$(grep -RFl ".sovereign-mobile-panel__language" "$DIST/assets" --include="*.css" 2>/dev/null | wc -l)"

echo "LANGUAGE_STORAGE_MARKER=$LANG_JS_COUNT"
echo "LANGUAGE_TOGGLE_MARKER=$TOGGLE_JS_COUNT"
echo "MOBILE_DIAGRAM_CSS_MARKER=$DIAGRAM_CSS_COUNT"
echo "MOBILE_LANGUAGE_CSS_MARKER=$MOBILE_LANG_CSS_COUNT"

if [ "$LANG_JS_COUNT" -gt 0 ] &&
   [ "$TOGGLE_JS_COUNT" -gt 0 ] &&
   [ "$DIAGRAM_CSS_COUNT" -gt 0 ] &&
   [ "$MOBILE_LANG_CSS_COUNT" -gt 0 ]; then
  FEATURE_GATE=0
  echo "SOURCE_FEATURE_GATE=PASS"
else
  echo "SOURCE_FEATURE_GATE=FAIL"
fi

echo
echo "===== M4 BACKUP LIVE INDEX ====="

INDEX_GATE=1

if [ "$BUILD_GATE" -eq 0 ] &&
   [ "$FEATURE_GATE" -eq 0 ] &&
   [ -f "$LIVE_INDEX" ]; then

  cp "$LIVE_INDEX" "$BACKUP/index.before.html"

  if [ -f "$BACKUP/index.before.html" ]; then
    INDEX_GATE=0
    echo "LIVE_INDEX_BACKUP=PASS"
    echo "BACKUP=$BACKUP/index.before.html"
  else
    echo "LIVE_INDEX_BACKUP=FAIL"
  fi
else
  echo "LIVE_INDEX_BACKUP=SKIPPED"
fi

echo
echo "===== M5 INSTALL HASHED ASSETS ====="

ASSET_GATE=1

if [ "$INDEX_GATE" -eq 0 ]; then

  mkdir -p "$LIVE_ROOT/assets"

  cp -a "$DIST/assets/." "$LIVE_ROOT/assets/"
  ASSET_STATUS=$?

  if [ "$ASSET_STATUS" -eq 0 ]; then
    ASSET_GATE=0
    echo "ASSET_INSTALL=PASS"
  else
    echo "ASSET_INSTALL=FAIL"
  fi
else
  echo "ASSET_INSTALL=SKIPPED"
fi

echo
echo "===== M6 INSTALL PUBLIC STATIC FILES ====="

STATIC_GATE=1

if [ "$ASSET_GATE" -eq 0 ]; then

  find "$DIST" -maxdepth 1 -type f ! -name "index.html" -print0 |
  while IFS= read -r -d "" file
  do
    cp "$file" "$LIVE_ROOT/$(basename "$file")"
  done

  STATIC_GATE=0
  echo "STATIC_INSTALL=PASS"
else
  echo "STATIC_INSTALL=SKIPPED"
fi

echo
echo "===== M7 ATOMIC INDEX DEPLOY ====="

DEPLOY_GATE=1

if [ "$STATIC_GATE" -eq 0 ]; then

  cp "$DIST/index.html" "$LIVE_ROOT/index.html.next"

  if [ -f "$LIVE_ROOT/index.html.next" ]; then
    mv "$LIVE_ROOT/index.html.next" "$LIVE_INDEX"
    DEPLOY_GATE=0
    echo "INDEX_DEPLOY=PASS"
  else
    echo "INDEX_DEPLOY=FAIL"
  fi
else
  echo "INDEX_DEPLOY=SKIPPED"
fi

echo
echo "===== M8 LOCAL PRODUCTION PROOF ====="

LOCAL_GATE=1

if [ "$DEPLOY_GATE" -eq 0 ]; then

  LIVE_JS_REL="$(grep -Eo "src=\"[^\"]+/assets/[^\"]+\\.js\"" "$LIVE_INDEX" | head -n 1 | sed "s/^src=\"//;s/\"$//")"
  LIVE_CSS_REL="$(grep -Eo "href=\"[^\"]+/assets/[^\"]+\\.css\"" "$LIVE_INDEX" | head -n 1 | sed "s/^href=\"//;s/\"$//")"

  echo "LIVE_JS_REL=$LIVE_JS_REL"
  echo "LIVE_CSS_REL=$LIVE_CSS_REL"

  LIVE_JS="$LIVE_ROOT$LIVE_JS_REL"
  LIVE_CSS="$LIVE_ROOT$LIVE_CSS_REL"

  LIVE_LANG_STORAGE="$(grep -Fc "ndsp-public-language" "$LIVE_JS" 2>/dev/null)"
  LIVE_TOGGLE="$(grep -Fc "Switch to English" "$LIVE_JS" 2>/dev/null)"
  LIVE_DIAGRAM="$(grep -Fc ".sovereign-evidence-map--desktop" "$LIVE_CSS" 2>/dev/null)"
  LIVE_MOBILE_LANG="$(grep -Fc ".sovereign-mobile-panel__language" "$LIVE_CSS" 2>/dev/null)"

  echo "LIVE_LANGUAGE_STORAGE_MARKER=$LIVE_LANG_STORAGE"
  echo "LIVE_LANGUAGE_TOGGLE_MARKER=$LIVE_TOGGLE"
  echo "LIVE_DIAGRAM_CSS_MARKER=$LIVE_DIAGRAM"
  echo "LIVE_MOBILE_LANGUAGE_CSS_MARKER=$LIVE_MOBILE_LANG"

  if [ -f "$LIVE_JS" ] &&
     [ -f "$LIVE_CSS" ] &&
     [ "$LIVE_LANG_STORAGE" -gt 0 ] &&
     [ "$LIVE_TOGGLE" -gt 0 ] &&
     [ "$LIVE_DIAGRAM" -gt 0 ] &&
     [ "$LIVE_MOBILE_LANG" -gt 0 ]; then
    LOCAL_GATE=0
    echo "LOCAL_PRODUCTION_GATE=PASS"
  else
    echo "LOCAL_PRODUCTION_GATE=FAIL"
  fi
else
  echo "LOCAL_PRODUCTION_GATE=SKIPPED"
fi

echo
echo "===== M9 HTTPS PROOF ====="

HTTPS_GATE=1

if [ "$LOCAL_GATE" -eq 0 ]; then

  HTTP_CODE="$(curl -sS -o "$TMP/home.html" -w "%{http_code}" https://ndsp.app/)"

  echo "HOME_HTTP=$HTTP_CODE"

  if [ "$HTTP_CODE" = "200" ]; then
    HTTPS_GATE=0
    echo "HTTPS_PRODUCTION_GATE=PASS"
  else
    echo "HTTPS_PRODUCTION_GATE=FAIL"
  fi
else
  echo "HTTPS_PRODUCTION_GATE=SKIPPED"
fi

echo
echo "===== M10 ROLLBACK GATE ====="

if [ "$BUILD_GATE" -ne 0 ] ||
   [ "$FEATURE_GATE" -ne 0 ] ||
   [ "$INDEX_GATE" -ne 0 ] ||
   [ "$ASSET_GATE" -ne 0 ] ||
   [ "$STATIC_GATE" -ne 0 ] ||
   [ "$DEPLOY_GATE" -ne 0 ] ||
   [ "$LOCAL_GATE" -ne 0 ] ||
   [ "$HTTPS_GATE" -ne 0 ]; then

  if [ -f "$BACKUP/index.before.html" ]; then
    cp "$BACKUP/index.before.html" "$LIVE_INDEX"
    echo "ROLLBACK_INDEX=PASS"
  else
    echo "ROLLBACK_INDEX=NOT_AVAILABLE"
  fi

  FINAL=1
else
  echo "ROLLBACK=NOT_REQUIRED"
  FINAL=0
fi

echo
echo "===== M11 FINAL VERDICT ====="

if [ "$FINAL" -eq 0 ]; then
  echo "MANAGED_PUBLIC_FRONTEND_DEPLOY=PASS"
  echo "MOBILE_HERO_SOURCE_FIX=ACTIVE"
  echo "LANGUAGE_TOGGLE_SOURCE_FIX=ACTIVE"
  echo "NEXT=IPHONE_VISUAL_PROOF"
else
  echo "MANAGED_PUBLIC_FRONTEND_DEPLOY=FAIL_ROLLED_BACK"
  echo "NEXT=REVIEW_FAILED_GATE"
fi

echo "NGINX_CHANGE=NO"
echo "NGINX_RELOAD=NO"
echo "SERVICE_RESTART=NO"
echo "DATABASE_WRITE=NO"
echo "GIT_COMMIT=NO"
echo "PUSH=NO"
echo "EVIDENCE_DIR=$TMP"
