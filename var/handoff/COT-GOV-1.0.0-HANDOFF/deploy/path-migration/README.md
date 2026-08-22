# Path Migration Safety

These scripts do not delete or rewrite legacy paths automatically.

Recommended order:

1. `audit-cot-logic.sh`
2. `inventory-legacy-paths.sh`
3. Review generated reports.
4. Create the canonical deployment layout.
5. Generate a migration plan.
6. Migrate one service at a time.
7. Validate and monitor.
8. Retire old paths only after approval.

Never run bulk search-and-replace across `/etc/systemd/system` or `/etc/nginx` without reviewing each service and route.
