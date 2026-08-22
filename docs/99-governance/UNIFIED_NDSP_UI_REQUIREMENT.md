# UNIFIED NDSP UI REQUIREMENT

UNIFIED_NDSP_UI_REQUIREMENT=NEW_THEME_ONLY

## PUBLIC_SURFACE
- host: ndsp.app
- theme: NEW_SOVEREIGN_THEME
- role: PUBLIC_INSTITUTIONAL_SURFACE

## AUTHENTICATED_WORKSPACE
- host: my.ndsp.app
- theme: NEW_SOVEREIGN_THEME
- role: FULL_OPERATIONAL_WORKSPACE

## RESTORE_FROM_OLD_PORTAL
- data_bindings: YES
- rich_page_content: YES
- operational_features: YES
- navigation_depth: YES
- old_visual_theme: NO

## CONTRACT_INTEGRATION
- expose_contracts: NO
- bind_contract_outputs_to_ui: YES
- show_user_fields: YES
- show_status_freshness_health_direction_evidence_market_risk: YES

## DESIGN_RULE
NEW_THEME + OLD_PORTAL_CAPABILITIES + REAL_CONTRACT_DATA = FINAL_UNIFIED_NDSP
