#!/usr/bin/env bash
set -Eeuo pipefail

echo "== NDSP Governance Baseline Verification =="

echo
echo "== Governance Files =="
test -f /home/nawaf511/empire-core-new/governance/README.md && echo "OK governance README"
test -f /home/nawaf511/empire-core-new/governance/approved-adoptions/NDSP_CURRENT_ADOPTIONS_MASTER.md && echo "OK master adoptions"
test -f /home/nawaf511/empire-core-new/governance/policies/API_NAMESPACE_POLICY.md && echo "OK API namespace policy"
test -f /home/nawaf511/empire-core-new/governance/database/POSTGRESQL_SINGLE_DB_POLICY.md && echo "OK PostgreSQL policy"

echo
echo "== Services =="
systemctl is-active nginx || true
systemctl is-active postgresql || true
systemctl is-active ndsp-api.service || true
systemctl is-active ndsp-telegram-alert.timer || true

echo
echo "== Nginx =="
sudo nginx -t

echo
echo "== Runtime URLs =="
for url in \
  https://ndsp.app/ \
  https://my.ndsp.app/ \
  https://admin.ndsp.app/ \
  https://ndsp.app/api/seats/status \
  https://my.ndsp.app/api/seats/status \
  https://admin.ndsp.app/api/seats/status \
  https://ndsp.app/api/v7/trial/activation-policy \
  https://my.ndsp.app/api/v7/trial/activation-policy \
  https://admin.ndsp.app/api/v7/trial/activation-policy
do
  code="$(curl -k -sS -L --max-time 20 -o /tmp/ndsp_governance_verify.out -w "%{http_code}" "$url" || true)"
  echo "$code  $url"
done

echo
echo "== Expected =="
echo "Main pages and /api GET endpoints: 200"
echo "/api/v7 endpoints: 404"
