# Governance Update Checklist

## Classification

- [ ] The change class is declared.
- [ ] The governance objective is explicit.
- [ ] The responsible owner is identified.
- [ ] The affected artifacts are listed.

## Isolation

- [ ] The branch starts from current `origin/main`.
- [ ] The work is performed in an independent worktree.
- [ ] Runtime files are not modified.
- [ ] Existing canonical artifacts are not silently rewritten.

## Validation

- [ ] JSON artifacts pass syntax validation.
- [ ] Checksum manifests pass verification.
- [ ] `git diff --check` passes.
- [ ] Changed files remain inside the approved scope.
- [ ] No undocumented file deletion exists.
- [ ] The branch contains only intended commits.

## Pull request

- [ ] The pull request targets `main`.
- [ ] The pull request body records validation results.
- [ ] The pull request is mergeable.
- [ ] Required reviews are complete.
- [ ] Checks pass or the repository explicitly has no configured checks.

## Closure

- [ ] The pull request is merged.
- [ ] The merge commit exists on `origin/main`.
- [ ] Expected governance artifacts exist on `origin/main`.
- [ ] The remote temporary branch is deleted.
- [ ] The local temporary branch is deleted.
- [ ] The temporary worktree is removed.
- [ ] Runtime changes remain `none`.
