# NDSP Backup and Restore Pack — V1

This pack was generated from the verified July 11, 2026 Backup Readiness Preflight archive with SHA-256:

```text
4076f964a0fb2f2459b8e23e28e62be3e37aab2e107bff22cbcc0dee407268b1
```

It reflects the current project, live paths, systemd and PM2 runtime, local and Docker PostgreSQL, Redis, Nginx, secret-bearing configuration paths, Docker metadata, and a dirty Git worktree.

## Tools

- `ndsp_create_backup_passphrase_v1.sh`: creates a mode-600 passphrase file.
- `ndsp_backup_runtime_precheck_v1.sh`: validates the runtime prerequisites without creating a backup.
- `ndsp_full_backup_v1.sh`: creates an encrypted full backup without restarting services.
- `ndsp_backup_verify_v1.sh`: validates encryption, hashes, nested archives, PostgreSQL dumps, SQLite files, and Redis RDB when tooling exists.
- `ndsp_restore_drill_v1.sh`: performs a non-destructive restore drill and can restore PostgreSQL dumps into an isolated temporary Docker container.
- `NDSP_BACKUP_SCOPE_V1.json`: machine-readable governed scope.

## Backup coverage

The backup includes the full project tree, PM2 state, selected home runtime directories, live `/opt` apps, `/var/www`, Nginx, systemd, `/etc/ndsp`, `/etc/empire`, PostgreSQL and Redis configuration, Cron, Let’s Encrypt, logical database dumps, SQLite online backups, Redis RDB, Docker metadata, eligible Docker volumes, package inventories, and internal SHA-256 manifests.

The final archive is GPG symmetric AES-256 encrypted. The passphrase file is never included.

## Commands

```bash
bash scripts/backup/ndsp_create_backup_passphrase_v1.sh

bash scripts/backup/ndsp_backup_runtime_precheck_v1.sh \
  --passphrase-file "$HOME/.config/ndsp-backup/backup-passphrase.txt"

bash scripts/backup/ndsp_full_backup_v1.sh \
  --passphrase-file "$HOME/.config/ndsp-backup/backup-passphrase.txt"

bash scripts/restore/ndsp_backup_verify_v1.sh \
  --archive /home/nawaf511/ndsp_full_backups_v2/NDSP_FULL_BACKUP_<HOST>_<TS>.tar.gpg \
  --passphrase-file "$HOME/.config/ndsp-backup/backup-passphrase.txt"

bash scripts/restore/ndsp_restore_drill_v1.sh \
  --archive /home/nawaf511/ndsp_full_backups_v2/NDSP_FULL_BACKUP_<HOST>_<TS>.tar.gpg \
  --passphrase-file "$HOME/.config/ndsp-backup/backup-passphrase.txt" \
  --keep
```

The pack intentionally does not overwrite production during restore. A production cutover runbook is created only after a successful drill and must include a fresh rollback snapshot, maintenance window, temporary database restoration, explicit owner approval, and health gates.

**Status:** `NDSP_BACKUP_RESTORE_PACK_V1_READY`
