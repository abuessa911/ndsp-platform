#!/usr/bin/env bash

# NDSP canonical DB env loader
if [ -f /etc/ndsp/ndsp-db.env ]; then
  set -a
  . /etc/ndsp/ndsp-db.env
  set +a
fi
DB_NAME="${DB_NAME:-ndsp_auth}"
PGDATABASE="${PGDATABASE:-ndsp_auth}"
# /NDSP canonical DB env loader

set -Eeuo pipefail
DB_NAME="${DB_NAME:-ndsp_auth}"

sudo -u postgres psql -d "$DB_NAME" -P pager=off -c "
SELECT
  cohort_code,
  cohort_label_ar,
  max_seats,
  used_seats,
  remaining_seats
FROM ndsp_trial_seat_status
ORDER BY sort_order;
"
