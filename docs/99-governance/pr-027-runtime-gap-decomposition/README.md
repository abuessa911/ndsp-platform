# PR-027 — Runtime Gap Decomposition

This package decomposes all PR-026 pending runtime capabilities into exact
missing-evidence categories and prioritized remediation batches.

It distinguishes likely machine-matching false negatives from implementation
gaps, exports the 50 closest capabilities to closure, and preserves every
unresolved capability.

No runtime service is changed and no capability is marked `UI_COMPLETE`.
