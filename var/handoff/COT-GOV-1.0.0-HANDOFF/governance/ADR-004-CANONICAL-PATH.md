# ADR-004 — Canonical project root

The canonical application root is:

`/home/nawaf511/empire-core-new`

Project dependency on `/opt/empire-core`, `/root/empire-core`, and project-specific `/var/www` paths must be retired through controlled migration.

OS-managed runtime configuration may remain under `/etc`.

Secrets must not be stored in the repository.
