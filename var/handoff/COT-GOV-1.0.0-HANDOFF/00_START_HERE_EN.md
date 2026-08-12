# Start Here — COT-GOV-1.0.0

## Purpose

This is a governance, handoff, and reference implementation package for updating the COT direction and timing layers under:

`/home/nawaf511/empire-core-new`

The package does not automatically replace production files, modify Nginx or systemd, or delete legacy paths. The existing backend must first be audited, mapped, tested, and shadow-run.

## Approved decisions

1. Dominance delta is the numerical difference between Long and Short values within the same dataset. It is not a time-series delta.
2. Long greater than Short is bullish, even by one contract.
3. Short greater than Long is bearish, even by one contract.
4. Neutral exists only when Long equals Short exactly.
5. Every result includes direction, explicitness, and horizon.
6. Investment mode:
   - Official total direction uses Asset Manager Positions only.
   - Asset Manager Changes are used only for weekly support.
   - Day control, TDL-M&L, TDL-S, and speculation timing are disabled.
   - On disagreement, the total direction remains visible with:
     “Weekly support is not confirmed.”
7. Speculation mode:
   - Uses Changes only.
   - Uses day-control logic.
   - TDL-M&L and TDL-S are permitted only in speculation mode.
8. UTC is the only canonical timezone.
9. A Tuesday report becomes effective at 00:00 UTC on the following Monday and remains effective until the next Monday, using a half-open interval.
10. CORE is the official single-category output.
11. EXPANDED is a hidden shadow model using combined categories.
12. Canonical project root:
    `/home/nawaf511/empire-core-new`
13. Dependency on `/opt/empire-core`, `/root/empire-core`, and `/var/www` must be retired gradually.
14. No legacy path may be deleted before dry run, backup, acceptance tests, and rollback approval.

## Not yet resolved

- Existing TDL-M&L rule semantics.
- Existing TDL-S rule semantics.
- Exact legacy files implementing direction and timing.
- Official and experimental storage/database details.
- Exact integration points in the current main.cjs.

The package therefore exposes configurable adapters and contracts and does not invent undocumented TDL behavior.
