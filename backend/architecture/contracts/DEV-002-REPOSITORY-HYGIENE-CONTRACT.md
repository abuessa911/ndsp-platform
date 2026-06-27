# DEV-002 — Repository Hygiene Contract

## Responsibilities

- Maintain .gitignore.
- Prevent secrets from entering Git.
- Prevent heavy generated files from entering Git.
- Preserve source code visibility.
- Produce repository hygiene report.

## Non-responsibilities

- Does not delete local files.
- Does not clean server runtime directories.
- Does not migrate legacy source code.
- Does not rewrite Git history.

## Rule

Never use `git add .` in this repository until hygiene is fully stabilized.
