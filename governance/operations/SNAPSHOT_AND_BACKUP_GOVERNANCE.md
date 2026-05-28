# NDSP Snapshot And Backup Governance

Current gold snapshot:
- /home/nawaf511/ndsp_snapshots/NDSP_FIX_OLD_DB_SCRIPTS_ENV_CANONICAL_20260526_210427.tar.gz
- /home/nawaf511/ndsp_snapshots/NDSP_FIX_OLD_DB_SCRIPTS_ENV_CANONICAL_20260526_210427.tar.gz.sha256
- /home/nawaf511/ndsp_snapshots/NDSP_FIX_OLD_DB_SCRIPTS_ENV_CANONICAL_20260526_210427.manifest.txt

Policy:
1. Every major governance phase must generate a report.
2. Critical runtime changes must generate a backup.
3. Production-ready milestones must generate a snapshot.
4. Snapshots must include .tar.gz, .sha256, and .manifest.txt.
5. Snapshot verification must include sha256sum -c and tar -tzf.
