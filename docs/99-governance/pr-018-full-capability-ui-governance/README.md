# PR-018 — Full Capability-to-UI Governance

## Binding principle

The current frontend is not the authoritative definition of NDSP.

The product scope is the union of verified algorithms, economic and trading
rules, runtime services, API contracts, real datasets and calculations, user
and administrator workflows, and approved internal capabilities.

## Required traceability

```text
Capability
→ Source or algorithm
→ Runtime service
→ Endpoint or contract
→ Data and calculation mode
→ User role
→ Screen
→ Visible component
→ Validation evidence
```

## Initial truth state

- Policy status: `DISCOVERY_REQUIRED`
- Complete coverage claimed: `false`
- Initial traceability records: `0`
- Runtime changes: `none`

No person or tool may claim full UI coverage until the repository-wide
capability audit is complete and every material capability has evidence or a
governed exclusion.

## Enforcement

`AGENTS.md`, Copilot instructions, the machine-readable policy, the canonical
CSV register, the Python validator, and GitHub Actions collectively enforce
this contract.
