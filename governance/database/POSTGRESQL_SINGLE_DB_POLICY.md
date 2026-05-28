# NDSP PostgreSQL Single Database Policy

Approved runtime DB: ndsp_auth

Archived DBs:
- archived_mdip_20260526_203226
- archived_nawafo_db_20260526_203226
- archived_ndip_20260526_203226
- archived_ndsp_20260526_203226

Approved env file:
- /etc/ndsp/ndsp-db.env

Required verification:
- EXPECTED_DB_EXISTS=True
- OLD_ACTIVE_DB_NOT_PRESENT=mdip
- OLD_ACTIVE_DB_NOT_PRESENT=nawafo_db
- OLD_ACTIVE_DB_NOT_PRESENT=ndip
- OLD_ACTIVE_DB_NOT_PRESENT=ndsp
- ACTIVE_CONNECTIONS_TO_ARCHIVED_OR_OLD_DB=False
- CANONICAL_DB_LOGIN_OK=True
- CANONICAL_DB_IS_NDSP_AUTH=True
- RUNTIME_HEALTH_DB_IS_NDSP_AUTH=True
- SEATS_DB_IS_NDSP_AUTH=True
- BAD_DB_ASSIGNMENTS_FOUND=False

Patched old scripts:
- /home/nawaf511/empire-core-new/backend/ndsp_trial_seat_status.sh
- /home/nawaf511/empire-core-new/backend/ndsp-trial-seats.sh
