# PR-034 — Restore TDL v2 Policy Source

This package inventories local worktrees, PR-025 snapshots, backups, Git
reflog/stash trees, and unreachable blobs for the real implementation defining
both `read_tdl_v2_policy` and `write_tdl_v2_policy`.

The selected source is AST-valid, SHA-256-deduplicated, secret-scanned, and
restored to the canonical `app/core` package path. No local source or snapshot
is deleted.
