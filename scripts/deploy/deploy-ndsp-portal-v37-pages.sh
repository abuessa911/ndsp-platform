#!/usr/bin/env bash

ROOT="/home/nawaf511/empire-core-v5-1-1-clean/frontend/user-portal-vite"
LIVE="/var/www/ndsp-my/portal"
TMP="/tmp/ndsp-portal-managed-deploy-$(date -u +%Y%m%dT%H%M%SZ)-$$"
BUILD="$TMP/build"
BACKUP="$TMP/backup"

mkdir -p "$BUILD" "$BACKUP"

echo "===== M1 SOURCE BUILD ====="

(
  cd "$ROOT" &&
  npm run build -- --outDir "$BUILD" > "$TMP/build.log" 2>&1
)

BUILD_STATUS=$?

if [ "$BUILD_STATUS" -ne 0 ]; then
  echo "SOURCE_BUILD=FAIL"
  tail -n 25 "$TMP/build.log"
else
  echo "SOURCE_BUILD=PASS"
fi

BUILD_JS=""
BUILD_INDEX="$BUILD/index.html"

if [ "$BUILD_STATUS" -eq 0 ]; then
  BUILD_JS="$(find "$BUILD/assets" -maxdepth 1 -type f -name "index-*.js" 2>/dev/null | head -n 1)"
fi

echo
echo "===== M2 SECURITY + PAGE GATE ====="

SECURITY_GATE=1

if [ -f "$BUILD_JS" ] && [ -f "$BUILD_INDEX" ]; then
  INTERNAL_IDS="$(grep -Eoc "NDSP-CORE-L[0-9][0-9]" "$BUILD_JS")"
  RAW_TABLE="$(grep -Foc "v37LayerTable" "$BUILD_JS")"
  HOME="$(grep -Foc "مساحة القرار" "$BUILD_JS")"
  DECISION="$(grep -Foc "الأنظمة العامة" "$BUILD_JS")"
  MARKETS="$(grep -Foc "واجهة الأسواق" "$BUILD_JS")"
  BRIEF="$(grep -Foc "الموجز التنفيذي" "$BUILD_JS")"
  COMPLETED="$(grep -Foc "سجل مستقل للقرارات" "$BUILD_JS")"
  SETTINGS="$(grep -Foc "إعدادات الواجهة والحساب" "$BUILD_JS")"

  echo "INTERNAL_LAYER_IDS=$INTERNAL_IDS"
  echo "RAW_LAYER_TABLE=$RAW_TABLE"
  echo "HOME_MARKER=$HOME"
  echo "DECISION_MARKER=$DECISION"
  echo "MARKETS_MARKER=$MARKETS"
  echo "BRIEF_MARKER=$BRIEF"
  echo "COMPLETED_MARKER=$COMPLETED"
  echo "SETTINGS_MARKER=$SETTINGS"

  if [ "$INTERNAL_IDS" -eq 0 ] &&
     [ "$RAW_TABLE" -eq 0 ] &&
     [ "$HOME" -gt 0 ] &&
     [ "$DECISION" -gt 0 ] &&
     [ "$MARKETS" -gt 0 ] &&
     [ "$BRIEF" -gt 0 ] &&
     [ "$COMPLETED" -gt 0 ] &&
     [ "$SETTINGS" -gt 0 ]; then
    SECURITY_GATE=0
    echo "BUILD_SECURITY_GATE=PASS"
  else
    echo "BUILD_SECURITY_GATE=FAIL"
  fi
else
  echo "BUILD_ASSET_GATE=FAIL"
fi

echo
echo "===== M3 BACKUP LIVE INDEX ====="

if [ "$SECURITY_GATE" -eq 0 ]; then
  cp "$LIVE/index.html" "$BACKUP/index.before.html"
  BACKUP_STATUS=$?
else
  BACKUP_STATUS=1
fi

if [ "$BACKUP_STATUS" -eq 0 ]; then
  echo "LIVE_INDEX_BACKUP=PASS"
  echo "BACKUP=$BACKUP/index.before.html"
else
  echo "LIVE_INDEX_BACKUP=FAIL"
fi

echo
echo "===== M4 INSTALL HASHED BUILD ASSETS ====="

ASSET_GATE=1

if [ "$BACKUP_STATUS" -eq 0 ]; then
  ASSET_GATE=0

  grep -Eo "/portal/assets/[^\"']+\.(js|css)" "$BUILD_INDEX" | sort -u > "$TMP/assets.txt"

  while read -r rel
  do
    [ -n "$rel" ] || continue

    name="$(basename "$rel")"
    source="$BUILD/assets/$name"
    target="$LIVE/assets/$name"

    if [ ! -f "$source" ]; then
      echo "BUILD_ASSET_MISSING=$name"
      ASSET_GATE=1
      continue
    fi

    sudo install -o www-data -g www-data -m 664 "$source" "$target"
    STATUS=$?

    if [ "$STATUS" -ne 0 ]; then
      echo "ASSET_INSTALL_FAIL=$name"
      ASSET_GATE=1
    else
      echo "ASSET_INSTALL_PASS=$name"
    fi
  done < "$TMP/assets.txt"
fi

echo
echo "===== M5 INSTALL MANAGED PUBLIC CSS ====="

CSS_GATE=0

for css in v37-mobile-fix.css v37-page-identity.css
do
  source="$ROOT/public/$css"
  target="$LIVE/$css"

  if [ ! -f "$source" ]; then
    echo "SOURCE_CSS_MISSING=$css"
    CSS_GATE=1
    continue
  fi

  sudo install -o www-data -g www-data -m 664 "$source" "$target"
  STATUS=$?

  if [ "$STATUS" -ne 0 ]; then
    echo "CSS_INSTALL_FAIL=$css"
    CSS_GATE=1
  else
    echo "CSS_INSTALL_PASS=$css"
  fi
done

echo
echo "===== M6 ATOMIC INDEX DEPLOY ====="

INDEX_GATE=1

if [ "$ASSET_GATE" -eq 0 ] && [ "$CSS_GATE" -eq 0 ]; then
  sudo install -o www-data -g www-data -m 664 "$BUILD_INDEX" "$LIVE/index.html.next"
  NEXT_STATUS=$?

  if [ "$NEXT_STATUS" -eq 0 ]; then
    sudo mv "$LIVE/index.html.next" "$LIVE/index.html"
    MOVE_STATUS=$?
  else
    MOVE_STATUS=1
  fi

  if [ "$MOVE_STATUS" -eq 0 ]; then
    INDEX_GATE=0
    echo "INDEX_DEPLOY=PASS"
  else
    echo "INDEX_DEPLOY=FAIL"
  fi
else
  echo "INDEX_DEPLOY=SKIPPED"
fi

echo
echo "===== M7 LOCAL PRODUCTION PROOF ====="

LOCAL_GATE=1

if [ "$INDEX_GATE" -eq 0 ]; then
  LIVE_JS_REL="$(grep -Eo "src=\"[^\"]+/assets/[^\"]+\.js\"" "$LIVE/index.html" | head -n 1 | sed "s/^src=\"//;s/\"$//")"
  LIVE_JS="/var/www/ndsp-my${LIVE_JS_REL}"

  echo "LIVE_JS_REL=$LIVE_JS_REL"

  if [ -f "$LIVE_JS" ]; then
    LIVE_INTERNAL="$(grep -Eoc "NDSP-CORE-L[0-9][0-9]" "$LIVE_JS")"
    LIVE_TABLE="$(grep -Foc "v37LayerTable" "$LIVE_JS")"
    LIVE_HOME="$(grep -Foc "مساحة القرار" "$LIVE_JS")"
    LIVE_MARKETS="$(grep -Foc "واجهة الأسواق" "$LIVE_JS")"
    LIVE_BRIEF="$(grep -Foc "الموجز التنفيذي" "$LIVE_JS")"

    echo "LIVE_INTERNAL_LAYER_IDS=$LIVE_INTERNAL"
    echo "LIVE_RAW_LAYER_TABLE=$LIVE_TABLE"
    echo "LIVE_HOME_MARKER=$LIVE_HOME"
    echo "LIVE_MARKETS_MARKER=$LIVE_MARKETS"
    echo "LIVE_BRIEF_MARKER=$LIVE_BRIEF"

    if [ "$LIVE_INTERNAL" -eq 0 ] &&
       [ "$LIVE_TABLE" -eq 0 ] &&
       [ "$LIVE_HOME" -gt 0 ] &&
       [ "$LIVE_MARKETS" -gt 0 ] &&
       [ "$LIVE_BRIEF" -gt 0 ]; then
      LOCAL_GATE=0
      echo "LOCAL_PRODUCTION_GATE=PASS"
    else
      echo "LOCAL_PRODUCTION_GATE=FAIL"
    fi
  else
    echo "LIVE_JS=NOT_FOUND"
  fi
fi

echo
echo "===== M8 HTTPS ROUTE PROOF ====="

HTTPS_GATE=0

for route in /portal/ /portal/command /portal/asset /portal/brief /portal/completed /portal/settings
do
  headers="$TMP/route.headers"
  body="$TMP/route.body"

  curl -sS -D "$headers" -o "$body" "https://ndsp.app$route"

  CODE="$(grep -E "^HTTP/" "$headers" | tail -n 1 | cut -d" " -f2 | tr -d "\r")"
  LOCATION="$(grep -i "^location:" "$headers" | tail -n 1 | cut -d" " -f2- | tr -d "\r")"
  EXPECTED="https://ndsp.app/login/?next=$route"

  if [ "$CODE" = "302" ] && [ "$LOCATION" = "$EXPECTED" ]; then
    echo "ROUTE=$route HTTP=302 AUTH_REDIRECT=PASS"
  elif [ "$CODE" = "200" ] && grep -q "/portal/assets/" "$body"; then
    echo "ROUTE=$route HTTP=200 AUTHENTICATED_CONTENT=PASS"
  else
    echo "ROUTE=$route HTTP=$CODE LOCATION=$LOCATION FAIL"
    HTTPS_GATE=1
  fi
done

echo "--- PROTECTED CSS CONTRACT ---"

for asset in "/portal/v37-page-identity.css?v=20260811-1" "/portal/v37-mobile-fix.css?v=20260811-1"
do
  headers="$TMP/css.headers"
  body="$TMP/css.body"

  curl -sS -D "$headers" -o "$body" "https://ndsp.app$asset"

  CODE="$(grep -E "^HTTP/" "$headers" | tail -n 1 | cut -d" " -f2 | tr -d "\r")"
  LOCATION="$(grep -i "^location:" "$headers" | tail -n 1 | cut -d" " -f2- | tr -d "\r")"
  EXPECTED="https://ndsp.app/login/?next=$asset"

  if [ "$CODE" = "302" ] && [ "$LOCATION" = "$EXPECTED" ]; then
    echo "ASSET=$asset HTTP=302 AUTH_REDIRECT=PASS"
  elif [ "$CODE" = "200" ] && [ -s "$body" ]; then
    echo "ASSET=$asset HTTP=200 AUTHENTICATED_CONTENT=PASS"
  else
    echo "ASSET=$asset HTTP=$CODE LOCATION=$LOCATION FAIL"
    HTTPS_GATE=1
  fi
done

LOGIN_CODE="$(curl -sS -o "$TMP/login.html" -w "%{http_code}" "https://ndsp.app/login/?next=/portal/")"
LOGIN_MARKERS="$(grep -Eic "login|sign.?in|تسجيل الدخول|البريد|email|password|كلمة المرور" "$TMP/login.html" 2>/dev/null)"

echo "LOGIN_HTTP=$LOGIN_CODE"
echo "LOGIN_FORM_MARKERS=$LOGIN_MARKERS"

if [ "$LOGIN_CODE" != "200" ] || [ "$LOGIN_MARKERS" -le 0 ]; then
  HTTPS_GATE=1
fi

if [ "$HTTPS_GATE" -eq 0 ]; then
  echo "HTTPS_AUTH_CONTRACT_GATE=PASS"
  echo "HTTPS_PRODUCTION_GATE=PASS"
else
  echo "HTTPS_AUTH_CONTRACT_GATE=FAIL"
  echo "HTTPS_PRODUCTION_GATE=FAIL"
fi

echo
echo "===== M9 ROLLBACK GATE ====="

if [ "$INDEX_GATE" -ne 0 ] ||
   [ "$LOCAL_GATE" -ne 0 ] ||
   [ "$HTTPS_GATE" -ne 0 ]; then

  if [ -f "$BACKUP/index.before.html" ]; then
    sudo install -o www-data -g www-data -m 664 "$BACKUP/index.before.html" "$LIVE/index.html"
    echo "ROLLBACK_INDEX=PASS"
  else
    echo "ROLLBACK_INDEX=BACKUP_MISSING"
  fi

  FINAL=1
else
  echo "ROLLBACK=NOT_REQUIRED"
  FINAL=0
fi

echo
echo "===== M10 FINAL VERDICT ====="

if [ "$FINAL" -eq 0 ]; then
  echo "MANAGED_PORTAL_DEPLOY=PASS"
  echo "PUBLIC_LAYER_SANITIZATION=PASS"
  echo "DISTINCT_PORTAL_PAGES=PASS"
  echo "PRODUCTION_STYLE_ACTIVE=YES"
  echo "PRODUCTION_JS_ACTIVE=YES"
  echo "NEXT=IPHONE_VISUAL_PROOF"
else
  echo "MANAGED_PORTAL_DEPLOY=FAIL_ROLLED_BACK"
  echo "NEXT=REVIEW_FAILED_GATE"
fi

echo "NGINX_CHANGE=NO"
echo "NGINX_RELOAD=NO"
echo "SERVICE_RESTART=NO"
echo "DATABASE_WRITE=NO"
echo "GIT_COMMIT=NO"
echo "PUSH=NO"
echo "EVIDENCE_DIR=$TMP"
