<!-- NDSP_FULL_CAPABILITY_UI_GOVERNANCE_START -->

# NDSP Full-Capability Product Contract

The visible frontend is not the complete definition of NDSP.

Before changing algorithms, services, APIs, data contracts, frontend code,
product flows, or interface design, every human or automated agent must inspect:

- `docs/99-governance/pr-018-full-capability-ui-governance/`
- `CAPABILITY_UI_TRACEABILITY.csv`
- relevant canonical runtime governance artifacts
- the actual source logic, service, endpoint, data, and frontend consumer

Every material capability must be traceable through:

`capability -> source_or_algorithm -> service -> endpoint_or_contract ->
real_data -> user_role -> screen -> visible_component -> evidence`

Mandatory rules:

- Never omit a verified capability merely because it is absent from the UI.
- Never replace real calculations with mock or decorative values.
- Never claim complete coverage without machine-verifiable evidence.
- Mark unknown mappings as `DISCOVERY_REQUIRED`.
- Update traceability when product logic, APIs, or UI behavior changes.
- Internal formulas may remain protected, but user-relevant capabilities must
  have an accurate product representation or a governed exclusion.

<!-- NDSP_FULL_CAPABILITY_UI_GOVERNANCE_END -->
