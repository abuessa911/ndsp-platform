#!/usr/bin/env bash
set -euo pipefail
DATA="/var/www/ndsp-admin/data/admin-ops-summary.json"
TMP="/tmp/admin-ops-summary.$$.json"

sudo -u postgres psql -d ndsp_auth -At <<'SQL' > "$TMP"
WITH u AS (
  SELECT
    id::text AS user_id,
    COALESCE(name,'') AS name,
    CASE
      WHEN email IS NULL OR email='' THEN ''
      ELSE left(email,1)||'***@'||split_part(email,'@',2)
    END AS email,
    CASE
      WHEN phone IS NULL OR phone='' THEN ''
      ELSE left(phone,4)||'*******'
    END AS phone,
    COALESCE(status,'UNKNOWN') AS status,
    COALESCE(trial_segment,requested_segment,approved_segment,account_type,category,'غير محدد') AS segment,
    COALESCE(created_at::date::text,'') AS date,
    'منخفض' AS risk
  FROM public.users
  ORDER BY created_at DESC NULLS LAST
  LIMIT 50
),
m AS (
  SELECT jsonb_build_object(
    'total_users',(SELECT count(*) FROM public.users),
    'active_trials',(SELECT count(*) FROM public.users WHERE COALESCE(status,'') ILIKE '%ACTIVE%'),
    'pending_reviews',(SELECT count(*) FROM public.users WHERE COALESCE(review_status,status,'') ILIKE '%PENDING%'),
    'email_channels',(SELECT count(*) FROM public.user_alert_channels WHERE COALESCE(email,'') <> ''),
    'telegram_channels',(SELECT count(*) FROM public.user_alert_channels WHERE COALESCE(telegram_chat_id,'') <> ''),
    'active_subscriptions',(SELECT count(*) FROM public.saas_subscriptions WHERE COALESCE(status,'') ILIKE '%ACTIVE%'),
    'generated_at',now()
  ) AS metrics
)
SELECT jsonb_pretty(jsonb_build_object(
  'metrics',(SELECT metrics FROM m),
  'recent_users',COALESCE((SELECT jsonb_agg(to_jsonb(u)) FROM u),'[]'::jsonb),
  'subscriptions','[]'::jsonb
));
SQL

install -o www-data -g www-data -m 0644 "$TMP" "$DATA"
rm -f "$TMP"
