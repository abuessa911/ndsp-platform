#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="/home/nawaf511/empire-core-new"
APPS="$ROOT/apps"

PUBLIC_SRC="$APPS/public-landing"
MY_SRC="$APPS/user-portal"
ADMIN_SRC="$APPS/admin-console"

PUBLIC_DST="/var/www/ndsp"
MY_DST="/var/www/ndsp-my"
ADMIN_DST="/var/www/ndsp-admin"

REPORT_DIR="/home/nawaf511/ndsp_launch_reports"
BACKUP_DIR="/home/nawaf511/ndsp_backups"

TS="$(date +%Y%m%d_%H%M%S)"
REPORT="$REPORT_DIR/NDSP_DEPLOY_FRONTEND_FROM_APPS_${TS}.md"
BACKUP="$BACKUP_DIR/deploy_frontend_from_apps_${TS}"

mkdir -p "$REPORT_DIR" "$BACKUP"

{
echo "# NDSP Deploy Frontend From Apps"
echo "DATE=$(date -Is)"
echo "BACKUP=$BACKUP"
echo

echo "== 1) Preconditions =="
test -d "$PUBLIC_SRC"
test -d "$MY_SRC"
test -d "$ADMIN_SRC"
echo "PRECONDITIONS_OK=True"
echo

echo "== 2) Backup current deployed outputs =="
mkdir -p "$BACKUP"
cp -a "$PUBLIC_DST" "$BACKUP/ndsp" 2>/dev/null || true
cp -a "$MY_DST" "$BACKUP/ndsp-my" 2>/dev/null || true
cp -a "$ADMIN_DST" "$BACKUP/ndsp-admin" 2>/dev/null || true
echo "BACKUP_OK=True"
echo

echo "== 3) Deploy from apps source =="
rsync -a --delete "$PUBLIC_SRC"/ "$PUBLIC_DST"/
rsync -a --delete "$MY_SRC"/ "$MY_DST"/
rsync -a --delete "$ADMIN_SRC"/ "$ADMIN_DST"/

chown -R www-data:www-data "$PUBLIC_DST" "$MY_DST" "$ADMIN_DST" || true
find "$PUBLIC_DST" "$MY_DST" "$ADMIN_DST" -type d -exec chmod 755 {} \; || true
find "$PUBLIC_DST" "$MY_DST" "$ADMIN_DST" -type f -exec chmod 644 {} \; || true

echo "DEPLOY_DONE=True"
echo

echo "== 4) Verify source and deployed are identical =="
diff -qr "$PUBLIC_SRC" "$PUBLIC_DST" > /tmp/ndsp_diff_public_${TS}.txt || true
diff -qr "$MY_SRC" "$MY_DST" > /tmp/ndsp_diff_my_${TS}.txt || true
diff -qr "$ADMIN_SRC" "$ADMIN_DST" > /tmp/ndsp_diff_admin_${TS}.txt || true

DIFF_PUBLIC_COUNT="$(wc -l < /tmp/ndsp_diff_public_${TS}.txt | tr -d ' ')"
DIFF_MY_COUNT="$(wc -l < /tmp/ndsp_diff_my_${TS}.txt | tr -d ' ')"
DIFF_ADMIN_COUNT="$(wc -l < /tmp/ndsp_diff_admin_${TS}.txt | tr -d ' ')"

echo "DIFF_PUBLIC_COUNT=$DIFF_PUBLIC_COUNT"
echo "DIFF_MY_COUNT=$DIFF_MY_COUNT"
echo "DIFF_ADMIN_COUNT=$DIFF_ADMIN_COUNT"
echo

echo "== 5) Route verification =="
OLD_ROUTE="/api/v6/payments/nowpayments/subscription/create"
NEW_ROUTE="/api/payments/nowpayments/subscription/create"

SOURCE_OLD_ROUTE_COUNT="$(grep -RIl "$OLD_ROUTE" "$PUBLIC_SRC" "$MY_SRC" "$ADMIN_SRC" 2>/dev/null | wc -l | tr -d ' ')"
DEPLOYED_OLD_ROUTE_COUNT="$(grep -RIl "$OLD_ROUTE" "$PUBLIC_DST" "$MY_DST" "$ADMIN_DST" 2>/dev/null | wc -l | tr -d ' ')"
SOURCE_NEW_ROUTE_COUNT="$(grep -RIl "$NEW_ROUTE" "$PUBLIC_SRC" "$MY_SRC" "$ADMIN_SRC" 2>/dev/null | wc -l | tr -d ' ')"
DEPLOYED_NEW_ROUTE_COUNT="$(grep -RIl "$NEW_ROUTE" "$PUBLIC_DST" "$MY_DST" "$ADMIN_DST" 2>/dev/null | wc -l | tr -d ' ')"

echo "SOURCE_OLD_ROUTE_COUNT=$SOURCE_OLD_ROUTE_COUNT"
echo "DEPLOYED_OLD_ROUTE_COUNT=$DEPLOYED_OLD_ROUTE_COUNT"
echo "SOURCE_NEW_ROUTE_COUNT=$SOURCE_NEW_ROUTE_COUNT"
echo "DEPLOYED_NEW_ROUTE_COUNT=$DEPLOYED_NEW_ROUTE_COUNT"
echo

echo "== 6) Nginx and endpoint smoke tests =="
nginx -t
systemctl reload nginx
echo "NGINX_OK=True"

probe_get() {
  name="$1"
  url="$2"
  code="$(curl -k -sS -o "/tmp/${name}_${TS}.out" -w "%{http_code}" "$url" || true)"
  echo "GET_${name}_HTTP=$code URL=$url"
}

probe_post() {
  name="$1"
  url="$2"
  body="$3"
  code="$(curl -k -sS -o "/tmp/${name}_${TS}.out" -w "%{http_code}" \
    -X POST "$url" \
    -H "Content-Type: application/json" \
    -d "$body" || true)"
  echo "POST_${name}_HTTP=$code URL=$url"
  head -c 500 "/tmp/${name}_${TS}.out" | tr '\n' ' ' || true
  echo
}

probe_get public_home "https://ndsp.app/?v=apps-deploy-${TS}"
probe_get my_home "https://my.ndsp.app/?v=apps-deploy-${TS}"
probe_get admin_home "https://admin.ndsp.app/NDSP_Admin_Console.html?v=apps-deploy-${TS}"
probe_post checkout_working "https://my.ndsp.app/api/payments/nowpayments/subscription/create" '{"email":"audit-apps-deploy@example.invalid","plan":"pro","network":"TRC20"}'
probe_post trial_working "https://my.ndsp.app/api/trial/register" '{"email":"audit-apps-deploy@example.invalid","name":"NDSP Audit Apps Deploy"}'
echo

echo "== 7) Final assertions =="
BAD_500_COUNT="$(grep -Eo 'HTTP=[0-9]+' "$REPORT" | awk -F= '$2>=500{c++} END{print c+0}')"
BAD_404_COUNT="$(grep -Eo 'GET_(public_home|my_home|admin_home)_HTTP=404|POST_(checkout_working|trial_working)_HTTP=404' "$REPORT" | wc -l | tr -d ' ')"

echo "BAD_500_COUNT=$BAD_500_COUNT"
echo "BAD_404_COUNT=$BAD_404_COUNT"

ASSERT_OK=True
if [ "$DIFF_PUBLIC_COUNT" != "0" ]; then ASSERT_OK=False; fi
if [ "$DIFF_MY_COUNT" != "0" ]; then ASSERT_OK=False; fi
if [ "$DIFF_ADMIN_COUNT" != "0" ]; then ASSERT_OK=False; fi
if [ "$SOURCE_OLD_ROUTE_COUNT" != "0" ]; then ASSERT_OK=False; fi
if [ "$DEPLOYED_OLD_ROUTE_COUNT" != "0" ]; then ASSERT_OK=False; fi
if [ "$BAD_500_COUNT" != "0" ]; then ASSERT_OK=False; fi
if [ "$BAD_404_COUNT" != "0" ]; then ASSERT_OK=False; fi

echo "ASSERT_OK=$ASSERT_OK"

if [ "$ASSERT_OK" = "True" ]; then
  echo "FINAL_STATUS=NDSP_FRONTEND_DEPLOYED_FROM_APPS_SOURCE_OK"
else
  echo "FINAL_STATUS=NDSP_FRONTEND_DEPLOY_FROM_APPS_NEEDS_REVIEW"
fi

echo "REPORT=$REPORT"
echo "BACKUP=$BACKUP"
} | tee "$REPORT"
