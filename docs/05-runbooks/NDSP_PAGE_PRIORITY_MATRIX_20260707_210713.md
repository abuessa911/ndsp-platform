# NDSP Page Priority Matrix

DATE=2026-07-07
MODE=PLANNING_ONLY
MODIFICATIONS=None

## Current Status

Routes inventory confirmed that all public HTML routes are HTTP 200.

No page should be deleted, renamed, merged, or rebuilt without explicit approval.

## Priority 1 — Core User Journey

These pages are the main user path and should receive polish/content attention first:

1. index.html
   - Purpose: portal entry / command landing
   - Priority: High
   - Action: keep stable, polish later only if needed

2. NDSP_Asset_View.html / asset-selector.html
   - Purpose: choose market and asset
   - Priority: High
   - Action: keep both routes; treat asset-selector.html as alias/working page

3. decision-support.html / decision-center.html
   - Purpose: decision reading and quality explanation
   - Priority: High
   - Action: strengthen explanation content later

4. NDSP_Command_Center.html / decision-radar.html
   - Purpose: command center and radar
   - Priority: High
   - Action: protect radar; visual polish only

5. NDSP_Daily_Brief.html / daily-brief.html
   - Purpose: daily market reading
   - Priority: High
   - Action: improve content density later

6. NDSP_Settings_Alerts.html / settings.html
   - Purpose: monitoring and settings
   - Priority: Medium-High
   - Action: clarify monitoring vs alert logic later

7. disclaimer.html
   - Purpose: legal/user acknowledgement
   - Priority: Locked
   - Action: do not disturb unless legal text update is explicitly approved

## Priority 2 — User Education / Trust Pages

These pages improve credibility and onboarding:

1. decision-guide.html
   - Explain how decisions are read

2. decision-modes-guide.html
   - Explain user decision modes

3. user-guide.html
   - Simple user guide

4. pro-guide.html
   - Advanced user guide

5. support-center.html
   - Help and support

Action:
Improve text and structure later. No runtime changes needed.

## Priority 3 — Market Context Pages

These support the decision room but are not first polish targets:

1. usd-pulse.html
2. dollar-impact.html
3. dollar-news.html
4. nmp.html

Action:
Keep working. Improve content later only after core journey is stable.

## Priority 4 — History / Tracking Pages

Useful but not urgent:

1. my-watchlist.html
2. alerts-log.html
3. completed-decisions.html

Action:
Keep. Later bind to real user state if backend supports it.

## Deferred Issue

Menu visual issue is deferred.

Rule:
Do not continue stacking CSS patches for the menu now.
Future menu work must begin with DOM/Browser audit and one calculated patch only.

## Next Recommended Work

Start with planning content and wording for Priority 1 pages:

- Asset View
- Decision Support
- Command Center
- Daily Brief
- Settings / Alerts

Do not modify API, PM2, Nginx, radar JS, menu JS, or disclaimer JS.

FINAL_STATUS=PAGE_PRIORITY_MATRIX_CREATED
