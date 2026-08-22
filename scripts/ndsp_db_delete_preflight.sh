#!/usr/bin/env bash
set -Eeuo pipefail
cd /home/nawaf511/empire-core-v5-1-1-clean
echo "===== NDSP DB DELETE PREFLIGHT ====="
date
echo
echo "Protected assets:"
cat .ndsp_protected_assets
echo
echo "Database sizes:"
sudo -u postgres psql -d postgres -P pager=off -c "SELECT datname, pg_size_pretty(pg_database_size(datname)) AS size FROM pg_database WHERE datistemplate = false ORDER BY pg_database_size(datname) DESC;"
echo
echo "ndsp_auth status:"
sudo -u postgres psql -d ndsp_auth -P pager=off -c "SELECT current_database() AS database_name, pg_size_pretty(pg_database_size(current_database())) AS database_size;"
sudo -u postgres psql -d ndsp_auth -P pager=off -c "SELECT COUNT(*) AS ledger_rows FROM public.ndsp_decision_ledger;"
echo
echo "WARNING: Do not run DROP / TRUNCATE / DELETE / ALTER DROP without owner approval and fresh verified backup."
