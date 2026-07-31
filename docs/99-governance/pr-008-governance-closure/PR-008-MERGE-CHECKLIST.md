# PR-008 Merge Checklist

## Automated validation

- [x] PR-004 expected commits exist.
- [x] PR-005 expected commit exists.
- [x] PR-006 expected commit exists.
- [x] PR-007 expected commits exist.
- [x] PR-006 final artifacts exist.
- [x] PR-007 final artifacts exist.
- [x] PR-006 unresolved listeners equal `0`.
- [x] PR-007 unresolved ownership records equal `0`.
- [x] PR-007 review status is `RESOLVED=42`.
- [x] Closure artifacts are checksum-protected.
- [x] Runtime changes equal `none`.
- Commit ancestry status: `PASS`.

## Human merge review

- [ ] Confirm the target branch and merge strategy.
- [ ] Confirm no unrelated commits are included.
- [ ] Confirm governance documents render correctly.
- [ ] Confirm checksum verification passes after checkout.
- [ ] Confirm no runtime implementation is implied by governance classifications.
- [ ] Obtain required repository approval.

## Recommended merge order

1. PR-004 runtime dependency map.
2. PR-005 runtime ownership map.
3. PR-006 network exposure map.
4. PR-007 non-canonical ownership resolution.
5. PR-008 governance closure package.

## Post-merge verification

```bash
git log --oneline --decorate -15

cd docs/99-governance/pr-006-network-exposure-map
sha256sum -c PR006_FINAL_SHA256SUMS.txt

cd ../pr-007-noncanonical-ownership
sha256sum -c PR007_SHA256SUMS.txt

cd ../pr-008-governance-closure
sha256sum -c PR008_SHA256SUMS.txt
```

## Runtime safety

No service start, stop, restart, reload, enable, disable, deployment, firewall, proxy, database, or container action is part of this checklist.
