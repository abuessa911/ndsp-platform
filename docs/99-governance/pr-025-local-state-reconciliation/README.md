# PR-025 — Local State Reconciliation

This package inventories the primary repository's local state and recovers
only capability source files explicitly required by PR-023 contracts.

Safety rules:

- the primary worktree is read-only
- no local change is deleted
- no `.env`, key, credential, database, archive, backup, build, or dependency
  artifact is copied
- candidate files are scanned for common secret patterns
- unresolved or blocked paths remain explicit
- a private snapshot is stored outside the repository
