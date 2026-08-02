# PR-070 — Runtime Path Inventory

## Scope

Read-only inventory of `/opt`, `/var/www`, relevant systemd services, Nginx
directives, and repository references to legacy runtime paths.

## Counts

- Path records: 50001
- Relevant systemd services: 93
- Nginx directives: 131
- Repository path references: 583
- Inventory limit reached: true

## Safety

- systemd mutations: 0
- Nginx mutations: 0
- files deleted: 0
- files moved: 0
- production services restarted: 0
- runtime changes: none

## Next step

Human review must classify each path and reference as Active, Legacy,
Duplicate, Unknown, Safe to Migrate, or Unsafe to Remove before PR-071.
