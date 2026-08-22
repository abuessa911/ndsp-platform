# ENV Audit Report

- root: `/home/nawaf511/empire-core-new`
- files found: `19`
- unique keys: `148`

## Env Files

- `/home/nawaf511/empire-core-new/.env`
- `/home/nawaf511/empire-core-new/api/.env`
- `/home/nawaf511/empire-core-new/backend/.env`
- `/home/nawaf511/empire-core-new/backend/.env.before_mt4_dir_fix_20260502_021056`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env`
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_active_direction.env`
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_ml_direction.env`
- `/home/nawaf511/empire-core-new/backend/services/bot_execution/config/default.env`
- `/home/nawaf511/empire-core-new/backend/services/completed_decision/config/default.env`
- `/home/nawaf511/empire-core-new/backend/services/decision_governance_core/config/default.env`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-launch-control-v167/.env`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-telegram-notifications-v182/.env`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v163/.env`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/.env`
- `/home/nawaf511/empire-core-new/integrations/airtable-runtime-sync/.env`
- `/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/backend-express/.env`
- `/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/checkout-admin-vite/.env`
- `/home/nawaf511/empire-core-new/research/research-labs.env`

## Duplicate / Conflicting Keys

### `ADMIN_EMAIL` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:89` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:72` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:1` = `ndsp.app@gmail.com`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:72`

### `ADMIN_KEY` — CONFLICT
- `/home/nawaf511/empire-core-new/.env:8` = `<secret len=86 sha256=d341f46d8a>`
- `/home/nawaf511/empire-core-new/backend/.env:16` = `<secret len=64 sha256=f6a9cb988b>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:16` = `<secret len=64 sha256=f6a9cb988b>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:2` = `<secret len=64 sha256=f6a9cb988b>`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:16`

### `ADMIN_UI_KEY` — CONFLICT
- `/home/nawaf511/empire-core-new/.env:10` = `<secret len=72 sha256=86988b0787>`
- `/home/nawaf511/empire-core-new/backend/.env.before_mt4_dir_fix_20260502_021056:18` = `<secret len=25 sha256=f47d934db6>`
- selected: `/home/nawaf511/empire-core-new/.env:10`

### `ALERT_EMAIL_TO` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:28` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/.env:92` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:75` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:3` = `ndsp.app@gmail.com`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:75`

### `DATABASE_URL` — CONFLICT
- `/home/nawaf511/empire-core-new/.env:7` = `<secret len=96 sha256=cab8350b3d>`
- `/home/nawaf511/empire-core-new/backend/.env.before_mt4_dir_fix_20260502_021056:28` = `<secret len=107 sha256=9fe63f18a4>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:19` = `<secret len=96 sha256=cab8350b3d>`
- `/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/backend-express/.env:2` = `<secret len=76 sha256=66f3e83a68>`
- selected: `/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/backend-express/.env:2`

### `DB_DATABASE` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:40` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/.env:34` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:34` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:4` = `ndsp_auth`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:34`

### `DB_HOST` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:37` = `127.0.0.1`
- `/home/nawaf511/empire-core-new/backend/.env:31` = `127.0.0.1`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:31` = `127.0.0.1`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:5` = `127.0.0.1`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:31`

### `DB_NAME` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:39` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/.env:33` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:33` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:6` = `ndsp_auth`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:33`

### `DB_PASSWORD` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:43` = `<secret len=48 sha256=25beede5d0>`
- `/home/nawaf511/empire-core-new/backend/.env:37` = `<secret len=48 sha256=25beede5d0>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:37` = `<secret len=48 sha256=25beede5d0>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:7` = `<secret len=48 sha256=25beede5d0>`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:37`

### `DB_PORT` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:38` = `5432`
- `/home/nawaf511/empire-core-new/backend/.env:32` = `5432`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:32` = `5432`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:8` = `5432`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:32`

### `DB_USER` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:41` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/.env:35` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:35` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:9` = `ndsp_auth`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:35`

### `DB_USERNAME` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:42` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/.env:36` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:36` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:10` = `ndsp_auth`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:36`

### `EMAIL_FROM` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:88` = `NDSP <ndsp.app@gmail.com>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:71` = `NDSP <ndsp.app@gmail.com>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:11` = `NDSP <ndsp.app@gmail.com>`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:71`

### `FRONTEND_ORIGIN` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:11` = `https://ndsp.app`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:11` = `https://ndsp.app`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:12` = `https://ndsp.app`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:11`

### `JWT_SECRET` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:14` = `<secret len=64 sha256=14e3c8efd4>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:14` = `<secret len=64 sha256=14e3c8efd4>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:14` = `<secret len=64 sha256=14e3c8efd4>`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:14`

### `LEDGER_DB` — CONFLICT
- `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v163/.env:2` = `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v163/data/trial_clock.sqlite3`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/.env:2` = `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/data/trial_clock.sqlite3`
- selected: `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/.env:2`

### `LOG_LEVEL` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:25` = `INFO`
- `/home/nawaf511/empire-core-new/backend/.env:10` = `INFO`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:10` = `INFO`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:17` = `INFO`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:10`

### `MAIL_FROM` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:87` = `NDSP <ndsp.app@gmail.com>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:70` = `NDSP <ndsp.app@gmail.com>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:18` = `NDSP <ndsp.app@gmail.com>`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:70`

### `NDSP_ADMIN_KEY` — CONFLICT
- `/home/nawaf511/empire-core-new/.env:9` = `<secret len=64 sha256=b05d770498>`
- `/home/nawaf511/empire-core-new/backend/.env:15` = `<secret len=64 sha256=f6a9cb988b>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:15` = `<secret len=64 sha256=f6a9cb988b>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:21` = `<secret len=64 sha256=f6a9cb988b>`
- `/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/backend-express/.env:3` = `<secret len=64 sha256=f6a9cb988b>`
- selected: `/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/backend-express/.env:3`

### `NDSP_EXECUTION_MIN_CONFIDENCE` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:69` = `80`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:23` = `80`
- selected: `/home/nawaf511/empire-core-new/backend/.env:69`

### `NDSP_EXECUTION_NOTIONAL_USDT` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:68` = `10`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:24` = `10`
- selected: `/home/nawaf511/empire-core-new/backend/.env:68`

### `NDSP_EXECUTION_USER_EMAIL` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:67` = `ops@ndsp.app`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:25` = `ops@ndsp.app`
- selected: `/home/nawaf511/empire-core-new/backend/.env:67`

### `NDSP_EXECUTION_WEBHOOK_ENABLED` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:64` = `true`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:26` = `true`
- selected: `/home/nawaf511/empire-core-new/backend/.env:64`

### `NDSP_EXECUTION_WEBHOOK_SECRET` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:66` = `<secret len=69 sha256=63080c8f25>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:27` = `<secret len=69 sha256=63080c8f25>`
- selected: `/home/nawaf511/empire-core-new/backend/.env:66`

### `NDSP_EXECUTION_WEBHOOK_URL` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:65` = `https://bot.ndsp.app/api/webhooks/ndsp-signal`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:28` = `https://bot.ndsp.app/api/webhooks/ndsp-signal`
- selected: `/home/nawaf511/empire-core-new/backend/.env:65`

### `NDSP_HOST` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/services/bot_execution/config/default.env:1` = `127.0.0.1`
- `/home/nawaf511/empire-core-new/backend/services/completed_decision/config/default.env:1` = `127.0.0.1`
- `/home/nawaf511/empire-core-new/backend/services/decision_governance_core/config/default.env:1` = `127.0.0.1`
- selected: `/home/nawaf511/empire-core-new/backend/services/decision_governance_core/config/default.env:1`

### `NDSP_INTERNAL_DEBUG_KEY` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:93` = `<secret len=48 sha256=49201077fc>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:29` = `<secret len=48 sha256=49201077fc>`
- selected: `/home/nawaf511/empire-core-new/backend/.env:93`

### `NDSP_ORDINARY_TRIAL_LIMIT` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:76` = `25`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:30` = `25`
- selected: `/home/nawaf511/empire-core-new/backend/.env:76`

### `NDSP_PORT` — CONFLICT
- `/home/nawaf511/empire-core-new/backend/services/bot_execution/config/default.env:2` = `9080`
- `/home/nawaf511/empire-core-new/backend/services/completed_decision/config/default.env:2` = `9078`
- `/home/nawaf511/empire-core-new/backend/services/decision_governance_core/config/default.env:2` = `9079`
- selected: `/home/nawaf511/empire-core-new/backend/services/decision_governance_core/config/default.env:2`

### `NDSP_PRIVATE_INVITE_LIMIT` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:78` = `15`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:31` = `15`
- selected: `/home/nawaf511/empire-core-new/backend/.env:78`

### `NDSP_PROFESSIONAL_TRIAL_LIMIT` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:77` = `10`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:32` = `10`
- selected: `/home/nawaf511/empire-core-new/backend/.env:77`

### `NDSP_TELEGRAM_CHAT_ID` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:58` = `302572192`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:58` = `302572192`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:33` = `302572192`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:58`

### `NODE_ENV` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:9` = `production`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:9` = `production`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:34` = `production`
- `/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/backend-express/.env:5` = `production`
- selected: `/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/backend-express/.env:5`

### `NOWPAYMENTS_API_KEY` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:23` = `<secret len=31 sha256=7c1eb98d19>`
- `/home/nawaf511/empire-core-new/backend/.env:51` = `<secret len=31 sha256=7c1eb98d19>`
- `/home/nawaf511/empire-core-new/backend/.env.before_mt4_dir_fix_20260502_021056:21` = `<secret len=31 sha256=7c1eb98d19>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:51` = `<secret len=31 sha256=7c1eb98d19>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:35` = `<secret len=31 sha256=7c1eb98d19>`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:51`

### `NOWPAYMENTS_IPN_SECRET` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:24` = `<secret len=32 sha256=9c43c979ef>`
- `/home/nawaf511/empire-core-new/backend/.env:52` = `<secret len=32 sha256=9c43c979ef>`
- `/home/nawaf511/empire-core-new/backend/.env.before_mt4_dir_fix_20260502_021056:22` = `<secret len=32 sha256=9c43c979ef>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:52` = `<secret len=32 sha256=9c43c979ef>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:36` = `<secret len=32 sha256=9c43c979ef>`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:52`

### `OWNER_EMAIL` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:29` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/.env:48` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:48` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:37` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-launch-control-v167/.env:4` = `ndsp.app@gmail.com`
- selected: `/home/nawaf511/empire-core-new/backend/services/ndsp-launch-control-v167/.env:4`

### `PGDATABASE` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:33` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/.env:26` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:26` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:39` = `ndsp_auth`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:26`

### `PGHOST` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:31` = `127.0.0.1`
- `/home/nawaf511/empire-core-new/backend/.env:24` = `127.0.0.1`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:24` = `127.0.0.1`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:40` = `127.0.0.1`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:24`

### `PGPASSWORD` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:35` = `<secret len=48 sha256=25beede5d0>`
- `/home/nawaf511/empire-core-new/backend/.env:28` = `<secret len=48 sha256=25beede5d0>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:28` = `<secret len=48 sha256=25beede5d0>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:41` = `<secret len=48 sha256=25beede5d0>`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:28`

### `PGPORT` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:32` = `5432`
- `/home/nawaf511/empire-core-new/backend/.env:25` = `5432`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:25` = `5432`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:42` = `5432`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:25`

### `PGUSER` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:34` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/.env:27` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:27` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:43` = `ndsp_auth`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:27`

### `PORT` — CONFLICT
- `/home/nawaf511/empire-core-new/backend/.env:8` = `9001`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:8` = `9001`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:44` = `9001`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-launch-control-v167/.env:1` = `9090`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v163/.env:1` = `9089`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/.env:1` = `9089`
- `/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/backend-express/.env:1` = `8088`
- selected: `/home/nawaf511/empire-core-new/ndsp_checkout_plans_package/backend-express/.env:1`

### `POSTGRES_DATABASE` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:47` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/.env:43` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:43` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:45` = `ndsp_auth`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:43`

### `POSTGRES_DB` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:46` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/.env:42` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:42` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:46` = `ndsp_auth`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:42`

### `POSTGRES_HOST` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:44` = `127.0.0.1`
- `/home/nawaf511/empire-core-new/backend/.env:40` = `127.0.0.1`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:40` = `127.0.0.1`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:47` = `127.0.0.1`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:40`

### `POSTGRES_PASSWORD` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:49` = `<secret len=48 sha256=25beede5d0>`
- `/home/nawaf511/empire-core-new/backend/.env:45` = `<secret len=48 sha256=25beede5d0>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:45` = `<secret len=48 sha256=25beede5d0>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:48` = `<secret len=48 sha256=25beede5d0>`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:45`

### `POSTGRES_PORT` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:45` = `5432`
- `/home/nawaf511/empire-core-new/backend/.env:41` = `5432`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:41` = `5432`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:49` = `5432`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:41`

### `POSTGRES_URL` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:36` = `postgresql://ndsp_auth:d75089ca7527c0e97664fbd53f5628b781f16084b01d351e@127.0.0.1:5432/ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:21` = `postgresql://ndsp_auth:d75089ca7527c0e97664fbd53f5628b781f16084b01d351e@127.0.0.1:5432/ndsp_auth`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:21`

### `POSTGRES_USER` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:48` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/.env:44` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:44` = `ndsp_auth`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:50` = `ndsp_auth`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:44`

### `REGISTER_URL` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/services/ndsp-launch-control-v167/.env:9` = `http://127.0.0.1:9028/api/register`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v163/.env:4` = `http://127.0.0.1:9028/api/register`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/.env:4` = `http://127.0.0.1:9028/api/register`
- selected: `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/.env:4`

### `SESSION_URL` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/services/ndsp-launch-control-v167/.env:8` = `https://api.ndsp.app/api/auth/session`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v163/.env:3` = `https://api.ndsp.app/api/auth/session`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/.env:3` = `https://api.ndsp.app/api/auth/session`
- selected: `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/.env:3`

### `SMTP_ADMIN_TO` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:22` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/.env:90` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:73` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:52` = `ndsp.app@gmail.com`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:73`

### `SMTP_FROM` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:21` = `NDSP <ndsp.app@gmail.com>`
- `/home/nawaf511/empire-core-new/backend/.env:86` = `NDSP <ndsp.app@gmail.com>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:69` = `NDSP <ndsp.app@gmail.com>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:53` = `NDSP <ndsp.app@gmail.com>`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:69`

### `SMTP_HOST` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:16` = `smtp.gmail.com`
- `/home/nawaf511/empire-core-new/backend/.env:81` = `smtp.gmail.com`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:64` = `smtp.gmail.com`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:54` = `smtp.gmail.com`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:64`

### `SMTP_PASS` — CONFLICT
- `/home/nawaf511/empire-core-new/.env:20` = `<secret len=19 sha256=cff8bf538e>`
- `/home/nawaf511/empire-core-new/backend/.env:84` = `<secret len=16 sha256=4ebfd23613>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:67` = `<secret len=16 sha256=4ebfd23613>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:55` = `<secret len=16 sha256=4ebfd23613>`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:67`

### `SMTP_PASSWORD` — CONFLICT
- `/home/nawaf511/empire-core-new/.env:19` = `<secret len=19 sha256=cff8bf538e>`
- `/home/nawaf511/empire-core-new/backend/.env:85` = `<secret len=16 sha256=4ebfd23613>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:68` = `<secret len=16 sha256=4ebfd23613>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:56` = `<secret len=16 sha256=4ebfd23613>`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:68`

### `SMTP_PORT` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:17` = `587`
- `/home/nawaf511/empire-core-new/backend/.env:82` = `587`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:65` = `587`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:57` = `587`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:65`

### `SMTP_TO` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:27` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/.env:91` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:74` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:58` = `ndsp.app@gmail.com`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:74`

### `SMTP_USER` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:18` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/.env:83` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:66` = `ndsp.app@gmail.com`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:59` = `ndsp.app@gmail.com`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:66`

### `STATUS_URL` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v163/.env:5` = `http://127.0.0.1:9001/api/trial/status`
- `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/.env:5` = `http://127.0.0.1:9001/api/trial/status`
- selected: `/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/.env:5`

### `SYMBOL` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_active_direction.env:1` = `XAUUSD`
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_ml_direction.env:1` = `XAUUSD`
- selected: `/home/nawaf511/empire-core-new/backend/runtime/tdl_ml_direction.env:1`

### `TDL_DOMINANT` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_active_direction.env:11` = `L&M_S_CONFLICT`
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_ml_direction.env:7` = `L&M_S_CONFLICT`
- selected: `/home/nawaf511/empire-core-new/backend/runtime/tdl_ml_direction.env:7`

### `TDL_GOLDEN_NAME` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_active_direction.env:10` = ``
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_ml_direction.env:6` = ``
- selected: `/home/nawaf511/empire-core-new/backend/runtime/tdl_ml_direction.env:6`

### `TDL_GOLDEN_SIGNAL` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_active_direction.env:9` = `FALSE`
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_ml_direction.env:5` = `FALSE`
- selected: `/home/nawaf511/empire-core-new/backend/runtime/tdl_ml_direction.env:5`

### `TDL_LM_DIRECTION` — CONFLICT
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_active_direction.env:7` = `BEARISH`
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_ml_direction.env:3` = `bearish`
- selected: `/home/nawaf511/empire-core-new/backend/runtime/tdl_ml_direction.env:3`

### `TDL_S_DIRECTION` — CONFLICT
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_active_direction.env:8` = `BULLISH`
- `/home/nawaf511/empire-core-new/backend/runtime/tdl_ml_direction.env:4` = `bullish`
- selected: `/home/nawaf511/empire-core-new/backend/runtime/tdl_ml_direction.env:4`

### `TELEGRAM_ADMIN_CHAT_ID` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:59` = `302572192`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:59` = `302572192`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:60` = `302572192`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:59`

### `TELEGRAM_BOT_TOKEN` — CONFLICT
- `/home/nawaf511/empire-core-new/.env:11` = `<secret len=46 sha256=6c17592f92>`
- `/home/nawaf511/empire-core-new/backend/.env:55` = `<secret len=46 sha256=f2d91f340a>`
- `/home/nawaf511/empire-core-new/backend/.env.before_mt4_dir_fix_20260502_021056:1` = `<secret len=25 sha256=f47d934db6>`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:55` = `<secret len=46 sha256=f2d91f340a>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:61` = `<secret len=46 sha256=f2d91f340a>`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:55`

### `TELEGRAM_CHAT_ID` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:56` = `302572192`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:56` = `302572192`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:62` = `302572192`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:56`

### `TELEGRAM_CHAT_IDS` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/.env:13` = `-1003491841685,-1003793881886,-1003918395339`
- `/home/nawaf511/empire-core-new/backend/.env.before_mt4_dir_fix_20260502_021056:2` = `-1003491841685,-1003793881886,-1003918395339`
- selected: `/home/nawaf511/empire-core-new/.env:13`

### `TELEGRAM_CHAT_ID_1` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:60` = `-1003491841685`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:60` = `-1003491841685`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:63` = `-1003491841685`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:60`

### `TELEGRAM_CHAT_ID_2` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:61` = `-1003793881886`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:61` = `-1003793881886`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:64` = `-1003793881886`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:61`

### `TG_CHAT_ID` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:57` = `302572192`
- `/home/nawaf511/empire-core-new/backend/auth_api/.env:57` = `302572192`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:65` = `302572192`
- selected: `/home/nawaf511/empire-core-new/backend/auth_api/.env:57`

### `x_Admin_Key` — DUPLICATE_SAME_VALUE
- `/home/nawaf511/empire-core-new/backend/.env:17` = `<secret len=64 sha256=f6a9cb988b>`
- `/home/nawaf511/empire-core-new/backend/runtime/systemd-env/core-services.env:67` = `<secret len=64 sha256=f6a9cb988b>`
- selected: `/home/nawaf511/empire-core-new/backend/.env:17`


## Token Matrix

### PASS
- No working token found.

### FAIL
- ADMIN_KEY | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_KEY | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- ADMIN_UI_KEY | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- JWT_SECRET | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_ADMIN_KEY | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_EXECUTION_WEBHOOK_SECRET | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | authorization_bearer | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | authorization_raw | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | x_admin_key_lower | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | x_admin_key_mixed | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | x_ndsp_admin_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | x_internal_debug_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
- NDSP_INTERNAL_DEBUG_KEY | x_api_key | status=401 | body={"ok":false,"error":"AUTH_REQUIRED","service":"ndsp-platform-gateway"}
