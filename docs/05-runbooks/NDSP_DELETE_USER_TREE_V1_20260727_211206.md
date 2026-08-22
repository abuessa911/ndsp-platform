
============================================================
NDSP — GUARDED DELETE USER TREE FROM DATABASES V1
============================================================
DATE=2026-07-27T21:12:06+02:00
HOST=vmi2934783.contaboserver.net
PROJECT=/home/nawaf511/empire-core-new
TARGET_EMAIL=she20232030@gmail.com
EXECUTE=YES
ALLOW_ADMIN_DELETE=NO
BACKUP=/home/nawaf511/empire-core-new/backups/delete-user-tree-v1/20260727_211206
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_DELETE_USER_TREE_V1_20260727_211206.md
SOURCE_CODE_CHANGED=NO
NGINX_CHANGED=NO
SYSTEMD_CHANGED=NO

============================================================
0) EXPLICIT CONFIRMATION AND PRIVILEGE GATE
============================================================
EXPLICIT_CONFIRMATION=PASS
SUDO_GATE=PASS

============================================================
1) REQUIRED TOOLS
============================================================
PYTHON_VERSION=Python 3.12.3
PSQL_AVAILABLE=YES
PG_DUMP_AVAILABLE=YES
DOCKER_AVAILABLE=YES
TOOL_GATE=PASS

============================================================
2) WRITE DATABASE DELETE WORKERS
============================================================
WORKERS_CREATED=PASS

============================================================
3) BACKUP PROJECT METADATA SNAPSHOT
============================================================
METADATA_SNAPSHOT=PASS

============================================================
4) LOCAL POSTGRESQL SCAN AND DELETE
============================================================
LOCAL_POSTGRES_AVAILABLE=YES
LOCAL_POSTGRES_DATABASE_COUNT=2

LOCAL_POSTGRES_DATABASE=ndsp_auth
POSTGRES_DATABASE_SCAN_BEGIN=local::ndsp_auth
POSTGRES_TARGET_KEY_COUNT=1
POSTGRES_CANDIDATE_ROW_TOTAL=local::ndsp_auth:0
POSTGRES_NO_MATCHING_ROWS=local::ndsp_auth

LOCAL_POSTGRES_DATABASE=postgres
POSTGRES_DATABASE_SCAN_BEGIN=local::postgres
POSTGRES_NO_TABLES=local::postgres
LOCAL_POSTGRES_STATUS=AVAILABLE

============================================================
5) DOCKER POSTGRESQL SCAN AND DELETE
============================================================
DOCKER_POSTGRES_CONTAINER_COUNT=1

DOCKER_POSTGRES_CONTAINER=ndip_postgres
DOCKER_POSTGRES_USER=ndip_user
DOCKER_POSTGRES_DATABASE_COUNT=0

============================================================
6) SQLITE SCAN AND DELETE
============================================================
SQLITE_CANDIDATE_FILE_COUNT=160

SQLITE_DATABASE=/home/nawaf511/.codex/goals_1.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/.codex/goals_1.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/.codex/goals_1.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/.codex/goals_1.sqlite

SQLITE_DATABASE=/home/nawaf511/.codex/logs_2.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/.codex/logs_2.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/.codex/logs_2.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/.codex/logs_2.sqlite

SQLITE_DATABASE=/home/nawaf511/.codex/memories_1.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/.codex/memories_1.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/.codex/memories_1.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/.codex/memories_1.sqlite

SQLITE_DATABASE=/home/nawaf511/.codex/state_5.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/.codex/state_5.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/.codex/state_5.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/.codex/state_5.sqlite

SQLITE_DATABASE=/home/nawaf511/.config/BraveSoftware/Brave-Browser/Default/ads_service/database.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/.config/BraveSoftware/Brave-Browser/Default/ads_service/database.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/.config/BraveSoftware/Brave-Browser/Default/ads_service/database.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/.config/BraveSoftware/Brave-Browser/Default/ads_service/database.sqlite

SQLITE_DATABASE=/home/nawaf511/.config/BraveSoftware/Brave-Browser/Default/heavy_ad_intervention_opt_out.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/.config/BraveSoftware/Brave-Browser/Default/heavy_ad_intervention_opt_out.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/.config/BraveSoftware/Brave-Browser/Default/heavy_ad_intervention_opt_out.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/.config/BraveSoftware/Brave-Browser/Default/heavy_ad_intervention_opt_out.db

SQLITE_DATABASE=/home/nawaf511/Desktop/backend/ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/Desktop/backend/ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/Desktop/backend/ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/Desktop/backend/ndip.db

SQLITE_DATABASE=/home/nawaf511/Desktop/backend/users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/Desktop/backend/users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/Desktop/backend/users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/Desktop/backend/users.db

SQLITE_DATABASE=/home/nawaf511/empire-core-new/backend/services/ndsp-launch-control-v167/data/launch_control.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/empire-core-new/backend/services/ndsp-launch-control-v167/data/launch_control.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/empire-core-new/backend/services/ndsp-launch-control-v167/data/launch_control.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/empire-core-new/backend/services/ndsp-launch-control-v167/data/launch_control.sqlite3

SQLITE_DATABASE=/home/nawaf511/empire-core-new/backend/services/ndsp-telegram-notifications-v182/data/telegram.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/empire-core-new/backend/services/ndsp-telegram-notifications-v182/data/telegram.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/empire-core-new/backend/services/ndsp-telegram-notifications-v182/data/telegram.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/empire-core-new/backend/services/ndsp-telegram-notifications-v182/data/telegram.sqlite3

SQLITE_DATABASE=/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v163/data/trial_clock.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v163/data/trial_clock.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v163/data/trial_clock.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v163/data/trial_clock.sqlite3

SQLITE_DATABASE=/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/data/trial_clock.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/data/trial_clock.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/data/trial_clock.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/empire-core-new/backend/services/ndsp-trial-clock-v164/data/trial_clock.sqlite3

SQLITE_DATABASE=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-decision_btc/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-decision_btc/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-decision_btc/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-decision_btc/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-decision_eth/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-decision_eth/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-decision_eth/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-decision_eth/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_command-center/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_command-center/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_command-center/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_command-center/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_completed/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_completed/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_completed/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_completed/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_data-health/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_data-health/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_data-health/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_data-health/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_markets/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_markets/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_markets/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_markets/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_prices-chart/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_prices-chart/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_prices-chart/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_prices-chart/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_risk/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_risk/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_risk/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_risk/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_scenarios/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_scenarios/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_scenarios/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_COMMERCIAL_DATA_TRUTH_GATE_20260725_194121/profile-page_scenarios/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/.local/share/opencode/opencode.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/.local/share/opencode/opencode.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/.local/share/opencode/opencode.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/.local/share/opencode/opencode.db

SQLITE_DATABASE=/home/nawaf511/.local/share/pki/nssdb/cert9.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/.local/share/pki/nssdb/cert9.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/.local/share/pki/nssdb/cert9.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/.local/share/pki/nssdb/cert9.db

SQLITE_DATABASE=/home/nawaf511/.local/share/pki/nssdb/key4.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/.local/share/pki/nssdb/key4.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/.local/share/pki/nssdb/key4.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/.local/share/pki/nssdb/key4.db

SQLITE_DATABASE=/home/nawaf511/.local/share/pnpm/store/v11/index.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/.local/share/pnpm/store/v11/index.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/.local/share/pnpm/store/v11/index.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/.local/share/pnpm/store/v11/index.db

SQLITE_DATABASE=/home/nawaf511/NDSP-Customer-Agent/.adk/bot/traces/traces.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/NDSP-Customer-Agent/.adk/bot/traces/traces.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/NDSP-Customer-Agent/.adk/bot/traces/traces.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/NDSP-Customer-Agent/.adk/bot/traces/traces.db

SQLITE_DATABASE=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/data/ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_full_backups/NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556/project/empire-core-new/backend/users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_backups/NDSP_SOFT_LAUNCH_COMPLETION_HOTFIX_V167_20260719_131341/current_v164_service/data/trial_clock.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_backups/NDSP_SOFT_LAUNCH_COMPLETION_HOTFIX_V167_20260719_131341/current_v164_service/data/trial_clock.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_backups/NDSP_SOFT_LAUNCH_COMPLETION_HOTFIX_V167_20260719_131341/current_v164_service/data/trial_clock.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_backups/NDSP_SOFT_LAUNCH_COMPLETION_HOTFIX_V167_20260719_131341/current_v164_service/data/trial_clock.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_backups/NDSP_SOFT_LAUNCH_COMPLETION_V166_20260719_130759/current_v164_service/data/trial_clock.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_backups/NDSP_SOFT_LAUNCH_COMPLETION_V166_20260719_130759/current_v164_service/data/trial_clock.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_backups/NDSP_SOFT_LAUNCH_COMPLETION_V166_20260719_130759/current_v164_service/data/trial_clock.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_backups/NDSP_SOFT_LAUNCH_COMPLETION_V166_20260719_130759/current_v164_service/data/trial_clock.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_DECISION_SCORE_PROVENANCE_V189_20260719_194825/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_DECISION_SCORE_PROVENANCE_V189_20260719_194825/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_DECISION_SCORE_PROVENANCE_V189_20260719_194825/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_DECISION_SCORE_PROVENANCE_V189_20260719_194825/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_DECISION_SCORE_PROVENANCE_V189_20260719_194825/raw/chrome-profile/first_party_sets.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_DECISION_SCORE_PROVENANCE_V189_20260719_194825/raw/chrome-profile/first_party_sets.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_DECISION_SCORE_PROVENANCE_V189_20260719_194825/raw/chrome-profile/first_party_sets.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_DECISION_SCORE_PROVENANCE_V189_20260719_194825/raw/chrome-profile/first_party_sets.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_DECISION_SCORE_PROVENANCE_V189_20260719_194825/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_DECISION_SCORE_PROVENANCE_V189_20260719_194825/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_DECISION_SCORE_PROVENANCE_V189_20260719_194825/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_DECISION_SCORE_PROVENANCE_V189_20260719_194825/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-closed-dom/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-closed-dom/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-closed-dom/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-closed-dom/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-closed-shot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-closed-shot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-closed-shot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-closed-shot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-open-dom/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-open-dom/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-open-dom/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-open-dom/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-open-shot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-open-shot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-open-shot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_MOBILE_V93_FINALIZE_20260717_093715/browser/profile-open-shot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_PORTAL_RUNTIME_SURGICAL_RECOVERY_V187_20260719_191455/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_PORTAL_RUNTIME_SURGICAL_RECOVERY_V187_20260719_191455/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_PORTAL_RUNTIME_SURGICAL_RECOVERY_V187_20260719_191455/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_PORTAL_RUNTIME_SURGICAL_RECOVERY_V187_20260719_191455/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_PORTAL_RUNTIME_SURGICAL_RECOVERY_V187_20260719_191455/raw/chrome-profile/first_party_sets.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_PORTAL_RUNTIME_SURGICAL_RECOVERY_V187_20260719_191455/raw/chrome-profile/first_party_sets.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_PORTAL_RUNTIME_SURGICAL_RECOVERY_V187_20260719_191455/raw/chrome-profile/first_party_sets.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_PORTAL_RUNTIME_SURGICAL_RECOVERY_V187_20260719_191455/raw/chrome-profile/first_party_sets.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_PORTAL_RUNTIME_SURGICAL_RECOVERY_V187_20260719_191455/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_PORTAL_RUNTIME_SURGICAL_RECOVERY_V187_20260719_191455/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_PORTAL_RUNTIME_SURGICAL_RECOVERY_V187_20260719_191455/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_PORTAL_RUNTIME_SURGICAL_RECOVERY_V187_20260719_191455/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V195_20260720_004037/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V195_20260720_004037/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V195_20260720_004037/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V195_20260720_004037/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V195_20260720_004037/raw/chrome-profile/first_party_sets.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V195_20260720_004037/raw/chrome-profile/first_party_sets.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V195_20260720_004037/raw/chrome-profile/first_party_sets.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V195_20260720_004037/raw/chrome-profile/first_party_sets.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V195_20260720_004037/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V195_20260720_004037/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V195_20260720_004037/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V195_20260720_004037/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V196_20260720_020248/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V196_20260720_020248/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V196_20260720_020248/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V196_20260720_020248/raw/chrome-profile/Default/heavy_ad_intervention_opt_out.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V196_20260720_020248/raw/chrome-profile/first_party_sets.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V196_20260720_020248/raw/chrome-profile/first_party_sets.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V196_20260720_020248/raw/chrome-profile/first_party_sets.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V196_20260720_020248/raw/chrome-profile/first_party_sets.db

SQLITE_DATABASE=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V196_20260720_020248/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V196_20260720_020248/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V196_20260720_020248/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_launch_reports/NDSP_SCORE_INTEGRITY_GUARD_V196_20260720_020248/raw/chrome-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_082850/browser-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_082850/browser-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_082850/browser-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_082850/browser-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_082850/browser-profile-screenshot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_082850/browser-profile-screenshot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_082850/browser-profile-screenshot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_082850/browser-profile-screenshot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_084559/browser-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_084559/browser-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_084559/browser-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_084559/browser-profile/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_084559/browser-profile-screenshot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_084559/browser-profile-screenshot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_084559/browser-profile-screenshot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/NDSP_PORTAL_V50_BLACK_SCREEN_FOCUS_20260717_084559/browser-profile-screenshot/GPUPersistentCache/GPUCache/7WE2TYRSGLNGHXRXWS7GUPWSQLGIQULP/cache.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_goals_1.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_goals_1.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_goals_1.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_goals_1.sqlite

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_logs_2.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_logs_2.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_logs_2.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_logs_2.sqlite

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_memories_1.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_memories_1.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_memories_1.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_memories_1.sqlite

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_state_5.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_state_5.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_state_5.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.codex_state_5.sqlite

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.config_BraveSoftware_Brave-Browser_Default_ads_service_database.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.config_BraveSoftware_Brave-Browser_Default_ads_service_database.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.config_BraveSoftware_Brave-Browser_Default_ads_service_database.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.config_BraveSoftware_Brave-Browser_Default_ads_service_database.sqlite

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.config_BraveSoftware_Brave-Browser_Default_heavy_ad_intervention_opt_out.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.config_BraveSoftware_Brave-Browser_Default_heavy_ad_intervention_opt_out.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.config_BraveSoftware_Brave-Browser_Default_heavy_ad_intervention_opt_out.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.config_BraveSoftware_Brave-Browser_Default_heavy_ad_intervention_opt_out.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_Desktop_backend_ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_Desktop_backend_ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_Desktop_backend_ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_Desktop_backend_ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_Desktop_backend_users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_Desktop_backend_users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_Desktop_backend_users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_Desktop_backend_users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_opencode_opencode.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_opencode_opencode.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_opencode_opencode.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_opencode_opencode.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_pki_nssdb_cert9.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_pki_nssdb_cert9.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_pki_nssdb_cert9.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_pki_nssdb_cert9.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_pki_nssdb_key4.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_pki_nssdb_key4.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_pki_nssdb_key4.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_pki_nssdb_key4.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_pnpm_store_v11_index.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_pnpm_store_v11_index.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_pnpm_store_v11_index.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_.local_share_pnpm_store_v11_index.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_NDSP-Customer-Agent_.adk_bot_traces_traces.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_NDSP-Customer-Agent_.adk_bot_traces_traces.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_NDSP-Customer-Agent_.adk_bot_traces_traces.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_NDSP-Customer-Agent_.adk_bot_traces_traces.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_full_backups_NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556_project_empire-core-new_backend_ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_full_backups_NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556_project_empire-core-new_backend_ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_full_backups_NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556_project_empire-core-new_backend_ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_full_backups_NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556_project_empire-core-new_backend_ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_full_backups_NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556_project_empire-core-new_backend_users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_full_backups_NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556_project_empire-core-new_backend_users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_full_backups_NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556_project_empire-core-new_backend_users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_full_backups_NDSP_FULL_BACKUP_AFTER_LAUNCH_READY_20260610_084556_project_empire-core-new_backend_users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_data_ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_070656_backend_users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_data_ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071449_backend_users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_data_ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071526_backend_users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_data_ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071732_backend_users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_bundle_20260602_071838_backend_users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_data_ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_ndsp_upgrade_work_ndsp_upgrade_bundle_20260602_071838_backend_users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_snap_codex_34_logs_1.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_snap_codex_34_logs_1.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_snap_codex_34_logs_1.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_snap_codex_34_logs_1.sqlite

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_snap_codex_34_state_5.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_snap_codex_34_state_5.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_snap_codex_34_state_5.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_snap_codex_34_state_5.sqlite

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_legacy_sqlite_backups_ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_data_ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_prechange_backups/NDSP_PRECHANGE_BACKUP_20260705_005359/tree/detected_db_files/home_nawaf511_upgrade_review_empire-core-new_backend_users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/data/ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_070656/backend/users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/data/ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071449/backend/users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/data/ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071526/backend/users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/data/ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071732/backend/users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade_bundle_20260602_071838/backend/users.db

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/data/ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/ndip.db

SQLITE_DATABASE=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/ndsp_upgrade/work/ndsp_upgrade_bundle_20260602_071838/backend/users.db

SQLITE_DATABASE=/home/nawaf511/snap/chromium/3491/.local/share/pki/nssdb/cert9.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/snap/chromium/3491/.local/share/pki/nssdb/cert9.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/snap/chromium/3491/.local/share/pki/nssdb/cert9.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/snap/chromium/3491/.local/share/pki/nssdb/cert9.db

SQLITE_DATABASE=/home/nawaf511/snap/chromium/3491/.local/share/pki/nssdb/key4.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/snap/chromium/3491/.local/share/pki/nssdb/key4.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/snap/chromium/3491/.local/share/pki/nssdb/key4.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/snap/chromium/3491/.local/share/pki/nssdb/key4.db

SQLITE_DATABASE=/home/nawaf511/snap/chromium/3499/.local/share/pki/nssdb/cert9.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/snap/chromium/3499/.local/share/pki/nssdb/cert9.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/snap/chromium/3499/.local/share/pki/nssdb/cert9.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/snap/chromium/3499/.local/share/pki/nssdb/cert9.db

SQLITE_DATABASE=/home/nawaf511/snap/chromium/3499/.local/share/pki/nssdb/key4.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/snap/chromium/3499/.local/share/pki/nssdb/key4.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/snap/chromium/3499/.local/share/pki/nssdb/key4.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/snap/chromium/3499/.local/share/pki/nssdb/key4.db

SQLITE_DATABASE=/home/nawaf511/snap/codex/34/logs_1.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/snap/codex/34/logs_1.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/snap/codex/34/logs_1.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/snap/codex/34/logs_1.sqlite

SQLITE_DATABASE=/home/nawaf511/snap/codex/34/state_5.sqlite
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/snap/codex/34/state_5.sqlite
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/snap/codex/34/state_5.sqlite:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/snap/codex/34/state_5.sqlite

SQLITE_DATABASE=/home/nawaf511/upgrade_review/empire-core-new/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/upgrade_review/empire-core-new/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/upgrade_review/empire-core-new/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/upgrade_review/empire-core-new/backend/data/legacy_sqlite_backups/ndip_saas_legacy_20260502_111653.sqlite3

SQLITE_DATABASE=/home/nawaf511/upgrade_review/empire-core-new/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/upgrade_review/empire-core-new/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/upgrade_review/empire-core-new/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/upgrade_review/empire-core-new/backend/data/ndip_saas_before_test_cleanup_20260502_012247.sqlite3

SQLITE_DATABASE=/home/nawaf511/upgrade_review/empire-core-new/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/upgrade_review/empire-core-new/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/upgrade_review/empire-core-new/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/upgrade_review/empire-core-new/backend/data/ndip_saas_before_test_cleanup_v2_20260502_012410.sqlite3

SQLITE_DATABASE=/home/nawaf511/upgrade_review/empire-core-new/backend/data/ndip_saas.sqlite3
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/upgrade_review/empire-core-new/backend/data/ndip_saas.sqlite3
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/upgrade_review/empire-core-new/backend/data/ndip_saas.sqlite3:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/upgrade_review/empire-core-new/backend/data/ndip_saas.sqlite3

SQLITE_DATABASE=/home/nawaf511/upgrade_review/empire-core-new/backend/ndip.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/upgrade_review/empire-core-new/backend/ndip.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/upgrade_review/empire-core-new/backend/ndip.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/upgrade_review/empire-core-new/backend/ndip.db

SQLITE_DATABASE=/home/nawaf511/upgrade_review/empire-core-new/backend/users.db
SQLITE_DATABASE_SCAN_BEGIN=/home/nawaf511/upgrade_review/empire-core-new/backend/users.db
SQLITE_CANDIDATE_ROW_TOTAL=/home/nawaf511/upgrade_review/empire-core-new/backend/users.db:0
SQLITE_NO_MATCHING_ROWS=/home/nawaf511/upgrade_review/empire-core-new/backend/users.db

============================================================
7) POST-DELETE PUBLIC OWNER PAGE CACHE HINT
============================================================
OWNER_PAGE_URL=https://my.ndsp.app/owner/
BROWSER_REFRESH_REQUIRED=Ctrl+Shift+R
NOTE=If owner page still shows stale data after successful database deletion, clear browser cache or inspect owner API response.

============================================================
8) FINAL RESULT
============================================================
TARGET_EMAIL=she20232030@gmail.com
EXECUTE=YES
BACKUP=/home/nawaf511/empire-core-new/backups/delete-user-tree-v1/20260727_211206
REPORT=/home/nawaf511/empire-core-new/docs/05-runbooks/NDSP_DELETE_USER_TREE_V1_20260727_211206.md
SOURCE_CODE_CHANGED=NO
NGINX_CHANGED=NO
SYSTEMD_CHANGED=NO
FRONTEND_BUILD_CHANGED=NO
FINAL_STATUS=NDSP_DELETE_USER_TREE_V1_EXECUTED_AND_VERIFIED_BY_DATABASE_SCANS
