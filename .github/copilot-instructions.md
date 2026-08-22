<!-- BEGIN NDSP ROOT GOVERNANCE -->
# NDSP Repository Instructions for GitHub Copilot

MANDATORY: Before any work that can change this repository or its runtime, read:

- `governance/change-control/NDSP_ROOT_CHANGE_GOVERNANCE.md`
- `governance/change-control/NDSP_ROOT_POLICY.json`
- `governance/change-control/NDSP_CURRENT_PRELAUNCH_STATE.env`

Required mutation sequence:

READ → CLASSIFY → DISCOVER → SCOPE → BACKUP/ROLLBACK → CHANGE → VERIFY → RECORD → SEAL.

Never expose secrets.

Nested instructions may refine but MUST NOT weaken root governance.

PUBLIC_LAUNCH is currently NO.

Coolify/Traefik is transitional and must not be treated as the final NDSP deployment authority.
<!-- END NDSP ROOT GOVERNANCE -->

<!-- NDSP_FULL_CAPABILITY_UI_GOVERNANCE_START -->

# NDSP capability instructions

Read `AGENTS.md` and the PR-018 governance package before modifying product
logic or UI.

Do not assume the current interface exposes all NDSP capabilities. Trace every
affected capability from source logic to service, endpoint, real data, role,
screen, visible component, and evidence. Update the canonical traceability
register for material product changes. Unknown mappings must be recorded as
`DISCOVERY_REQUIRED`.

<!-- NDSP_FULL_CAPABILITY_UI_GOVERNANCE_END -->
