# NDSP System Build & Readiness Catalog
## Full English Version

**Project Name:** NDSP — Nawaf Decision Support Platform  
**System Type:** Multi-layer decision-support and market-analysis platform  
**System Owner:** Nawaf  
**Document Status:** Foundational / Execution / Governance Reference  
**Version:** v1.0  
**Release Date:** 2026-07-06  
**Confidentiality Level:** Internal — do not share with external developers unless sensitive engine logic and intellectual-property details are removed.

---

## 0. Purpose of This Catalog

This catalog is the operational reference that defines how NDSP should be built, prepared, deployed, governed, monitored, and maintained. Its purpose is to prevent randomness, page duplication, broken design, exposed system secrets, and inconsistent development behavior across developers and AI tools.

Any new change, feature, integration, or refactor inside NDSP must be checked against this catalog before execution. Code alone is not the final authority. The final authority is: **identity + map + governance + software contracts + tests + change report**.

---

## 1. System Definition

NDSP is not a direct buy/sell recommendation platform. It is not merely a price page, and it is not only a visual dashboard. NDSP is a decision-support system that uses internal analytical layers and decision engines to produce a governed reading of market condition, scenario state, risk, decision quality, and follow-up status.

The platform converts complex internal analysis into user-understandable outputs without exposing sensitive internal logic or issuing direct financial execution commands.

### 1.1 Short Definition

NDSP — Nawaf Decision Support Platform is a decision-support platform that presents governed market readings through internal engines, scenario levels, risk layers, and time-aware logic, producing a final state that explains monitoring status and decision quality without providing direct financial advice.

### 1.2 Governing Principles

1. The system does not output direct buy or sell orders.
2. The user interface shows understandable value, not sensitive internal formulas.
3. Every page has a clear purpose and a clear data source.
4. Every API has a documented contract.
5. Every change requires a backup and rollback report.
6. Every decision engine has inputs, outputs, and tests.
7. Scripts must not be stacked randomly without governance.
8. Official page names must not be changed randomly.
9. Protected layers and sensitive calculation details must not be exposed.
10. Real operation matters more than appearance, but appearance must communicate trust, clarity, and premium quality.

---

## 2. System Scope

### 2.1 In Scope for the Core Version

- Main landing page.
- User registration.
- User login.
- 16-day free trial.
- Mandatory disclaimer before entering the portal.
- User portal.
- Asset reading page.
- Command Center.
- Daily Brief / Decision Journal.
- Settings and alerts page.
- Decision Support page.
- Basic Admin Console.
- Live decision API.
- Live market-price binding.
- Internal decision engines.
- Risk layer.
- Devil’s Advocate layer.
- Decision quality output.
- Scenario state output.
- Logs and reports.
- Backup and rollback process.

### 2.2 Out of Scope for Now

- Trade execution bot.
- Direct buy/sell execution.
- Direct broker integration.
- Full exposure of protected engine names.
- Full native mobile application.
- Complex production payment stack before the core version is stable.
- Explicit financial recommendations.
- Owner permissions granted to non-owner users.

### 2.3 Scope Prohibitions

- NDSP must not become a direct signal-selling platform.
- The UI must not display “buy now” or “sell now”.
- Sensitive engine formulas must not be exposed.
- Backend changes must not be made to solve purely visual problems unless the backend is truly the cause.
- A new page must not be created with a confusingly similar name to an official page without documentation.
- A menu, radar, or existing panel must not be removed while applying a partial patch.

---

## 3. Product Identity

### 3.1 Official Name

NDSP — Nawaf Decision Support Platform

### 3.2 Visual Identity

NDSP should look institutional, dark, premium, and close to a Bloomberg or trading-terminal environment, while remaining clearer for regular users. The base color is deep black, the accent is gold, and neutral shades should be used for borders, cards, and supporting text.

### 3.3 Text Tone

- Clear.
- Firm.
- Not exaggerated.
- No profit promises.
- No “guaranteed trade” language.
- It explains decision state; it does not command the user.

### 3.4 UI Terms Allowed

- TDL
- NMP
- Nawaf Golden Signal
- Enhanced Nawaf Golden Signal
- Devil’s Advocate Layer
- Command Center
- Decision Quality
- Scenario State
- Under Monitoring
- Under Review
- Allowed with Caution
- Blocked
- Directional Context
- Caution Reason
- Activation Level
- Arrival Level
- Review Level
- Invalidation Level

### 3.5 Terms Prohibited or Strictly Controlled

- Buy.
- Sell.
- Enter the trade.
- Exit the trade.
- Guaranteed profit.
- Direct recommendation.
- Exposure of all internal engine names.
- Protected-layer details.
- Any language implying that NDSP replaces a licensed financial advisor.

### 3.6 Identity Signature

A subtle visual signature may be used in backgrounds or selected interface areas:

`HUNTER_KSA1`

It must remain light, transparent, and non-intrusive.

---

## 4. User Journey Map

### 4.1 Visitor Journey

Visitor → Landing page → Understand value → Review general methodology → Read short disclaimer → Start trial registration → Confirm account → Enter portal.

### 4.2 Trial User Journey

Trial user → Accept disclaimer → Select asset → View simplified reading → Follow scenario state → Use Command Center → Try limited alerts → Optional upgrade.

### 4.3 Advanced User Journey

Advanced user → Enable advanced mode → View expanded details → Compare assets → Read Daily Brief → Configure alerts → Monitor decision quality.

### 4.4 Admin Journey

Admin → Secure login → Review users → Review logs → Monitor system errors → Check API status → Manage general alerts.

### 4.5 Owner Journey

Owner → Full authority → Review governance → Use Manual Override when needed → Approve releases → Approve what can be shown or hidden → Review sensitive logs.

---

## 5. Page Map

### 5.1 Landing Page

**Suggested route:** `/` or `/index.html`  
**Purpose:** Communicate value and sell the idea without overwhelming the visitor.  
**Audience:** Visitors and new users.

#### Must Display

- NDSP name.
- Short definition.
- Core value proposition.
- General methodology.
- 16-day trial.
- Plans/packages.
- Short disclaimer.
- Register button.
- Login button.
- Optional market summary or ticker if available.

#### Must Not Display

- Engine secrets.
- Buy/sell commands.
- Protected-layer details.

#### Acceptance Criteria

- Fully localized in Arabic for Arabic version.
- Mobile responsive.
- No unnecessary duplicate buttons.
- Dark/gold NDSP identity applied.

---

### 5.2 Registration Page

**Purpose:** Create a user account and activate a 16-day trial.  
**Inputs:** name, email, phone, password.  
**Rules:** prevent duplicated email and phone, hash password, accept terms.

#### Error States

- Email already used.
- Phone already used.
- Weak password.
- Invalid email format.
- Server connection failure.

---

### 5.3 Login Page

**Purpose:** Authenticate users.  
**Rules:** avoid unsafe account-discovery messages, protect against repeated attempts, use secure sessions.

#### Must Display

- Email or phone field.
- Password field.
- Login button.
- Forgot password link.

---

### 5.4 Mandatory Disclaimer Page

**Purpose:** Prevent portal entry until the user confirms understanding of the platform’s nature.

#### Governance Text

NDSP is a decision-support and analytical platform. It is not a direct financial recommendation or execution platform. All displayed outputs are analytical readings and monitoring indicators, not instructions to buy, sell, or hold. The user remains responsible for all financial decisions and should seek professional advice when needed.

#### Rule

The user cannot enter the portal until the disclaimer is accepted.

---

### 5.5 User Dashboard

**Purpose:** Give the user a fast overview of account and reading status.  
**Displays:** trial status, favorite assets, latest reading, alerts, system quality, page shortcuts.

---

### 5.6 Asset View Page

**Purpose:** Display the reading for a selected asset.  
**Data Source:** `/api/decision/quality-live?symbol=...`

#### Must Display

- Asset name.
- Live price.
- Scenario state.
- Directional context.
- Decision quality.
- Caution reason.
- Activation level.
- Arrival level.
- Review level.
- Invalidation level.
- “Not financial advice” notice.

#### Must Not Display

- Protected-layer names.
- Exact NMP calculation details.
- Execution commands.

---

### 5.7 Command Center

**Purpose:** Present the overall decision and risk picture.  
**Displays:** radar, decision quality, risk state, Devil’s Advocate result, macro state, scenario summary.

#### Special Rules

- The radar must not disappear when new data binding is added.
- Page names in the side menu must not be changed randomly.
- Internal engines must not all be exposed.
- Green = allowed or stable.
- Yellow = caution or monitoring.
- Red = blocked or high risk.

---

### 5.8 Daily Brief / Decision Journal

**Purpose:** Display the daily or weekly decision history.  
**Displays:** latest changes, reason for state change, caution notes, data readiness.

---

### 5.9 Settings & Alerts

**Purpose:** Manage user preferences and alerts.  
**Displays:** asset list, alert type, delivery channel, language, alert thresholds, subscription status.

---

### 5.10 Decision Support Page

**Purpose:** Present a focused decision-support reading.  
**Displays:** decision quality, scenario state, context, caution reason, horizon, scenario levels.

---

### 5.11 Admin Console

**Purpose:** Manage and monitor the system.  
**Access:** Admin and Owner only.

#### Must Display

- Users.
- Subscriptions.
- Logs.
- API errors.
- Service health.
- Live-data status.
- Release reports.

---

## 6. Frontend Map

### 6.1 Suggested Structure

```txt
/frontend
├── index.html
├── decision-support.html
├── NDSP_Asset_View.html
├── NDSP_Command_Center.html
├── NDSP_Daily_Brief.html
├── NDSP_Settings_Alerts.html
├── login.html
├── register.html
├── disclaimer.html
├── admin.html
├── assets/
│   ├── images/
│   ├── icons/
│   └── fonts/
├── styles/
│   ├── ndsp-theme.css
│   ├── layout.css
│   └── mobile.css
└── scripts/
    ├── ndsp-api-client.js
    ├── ndsp-auth.js
    ├── ndsp-radar.js
    ├── ndsp-market-live.js
    └── ndsp-ui-state.js
```

### 6.2 Frontend Rules

1. The side menu is the main navigation model, not a crowded top menu.
2. Buttons must not be duplicated without purpose.
3. Every card must have a defined data source or explicit static status.
4. Every loading state must be clear.
5. Every API error must display a user-understandable message.
6. One failed component must not hide another critical component.
7. The radar must have a fallback when data fails.
8. Mobile experience has priority.
9. Arabic text must not overlap.
10. Scripts must not be placed randomly in every page; shared libraries are preferred.

---

## 7. Backend Map

### 7.1 Suggested Structure

```txt
/backend
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── decisions.py
│   │   ├── assets.py
│   │   ├── alerts.py
│   │   └── admin.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   └── rate_limit.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── engines/
│   └── database/
├── migrations/
├── tests/
└── scripts/
```

### 7.2 Backend Responsibilities

- User management.
- Registration and login.
- Password handling.
- Free-trial logic.
- Subscriptions.
- Live market-price retrieval.
- Decision engine execution.
- API output production.
- Permission enforcement.
- Error logging.
- Alert management.
- Health checks.

---

## 8. API Map

### 8.1 General Rules

Every API must define:

- Route.
- Request method.
- Inputs.
- Outputs.
- Errors.
- Permissions.
- Pages using it.
- Acceptance test.

### 8.2 Core API Contracts

#### User Registration

```txt
POST /api/auth/register
```

**Inputs:** name, email, phone, password.  
**Outputs:** user_id, trial_ends_at, token or confirmation message.  
**Errors:** duplicated email, duplicated phone, weak password.

#### Login

```txt
POST /api/auth/login
```

**Inputs:** email/phone, password.  
**Outputs:** token, user profile, role.  
**Errors:** invalid credentials, suspended account, too many attempts.

#### Live Decision Reading

```txt
GET /api/decision/quality-live?symbol=ETHUSDT
```

**Required Output:**

```json
{
  "symbol": "ETHUSDT",
  "live_price": 0,
  "decision_quality": 0,
  "scenario_state": "UNDER_MONITORING",
  "directional_context": "NEUTRAL",
  "market_state": "RANGING",
  "reading_horizon": "WATCH",
  "horizon_strength": 0,
  "caution_reason": "Data under review",
  "scenario_levels": {
    "activation": 0,
    "arrival": 0,
    "review": 0,
    "invalidation": 0
  },
  "disclaimer": "Decision support only. Not financial advice."
}
```

#### Service Health

```txt
GET /api/health
```

**Outputs:** API status, database status, price provider status, decision-engine status, last update.

---

## 9. Database Map

### 9.1 Core Tables

```txt
users
subscriptions
trial_sessions
assets
market_prices
cot_data
decision_readings
scenario_levels
alerts
audit_logs
admin_actions
password_resets
api_errors
release_reports
```

### 9.2 users Table

```txt
id
full_name
email
phone
password_hash
role
status
trial_started_at
trial_ends_at
created_at
updated_at
last_login_at
```

#### Constraints

- email unique.
- phone unique after digit normalization.
- password_hash never stores the original password.
- role limited to user, admin, owner.

### 9.3 decision_readings Table

```txt
id
symbol
live_price
decision_quality
scenario_state
directional_context
market_state
reading_horizon
horizon_strength
caution_reason
engine_version
created_at
```

### 9.4 audit_logs Table

```txt
id
actor_id
action
resource_type
resource_id
ip_address
user_agent
metadata
created_at
```

---

## 10. Decision Engine Map

### 10.1 Engine Order

```txt
TDL
→ Market Direction
→ Scenario Levels
→ NMP
→ Momentum
→ Macro USD
→ Risk
→ Devil’s Advocate
→ Decision Quality
→ Final State
```

### 10.2 TDL Engine

**Purpose:** Determine the time-aware and logical decision context.  
**Can its name be displayed?** Yes.  
**Can it block?** Not by itself unless data is invalid or outdated.  
**Inputs:** COT data, asset, timeframe, classification.  
**Outputs:** time context, initial bias, monitoring state.

### 10.3 NMP Engine

**Purpose:** Identify a critical meeting zone without exposing exact calculation logic.  
**Can its name be displayed?** Yes.  
**Can it block?** No, but it may be required for certain automated confirmation states.  
**Outputs:** near/far status, simplified or hidden reference zone.

### 10.4 Market Direction Engine

**Purpose:** Determine broad direction or neutrality.  
**Can its name be displayed?** Not required; result can be displayed.  
**Outputs:** bullish, bearish, neutral, mixed.

### 10.5 Scenario Levels Engine

**Purpose:** Produce activation, arrival, review, and invalidation levels.  
**Can it display?** Yes, as user-friendly values.  
**Constraint:** Do not display fake levels; if data is unavailable, show “under verification”.

### 10.6 Momentum Engine

**Purpose:** Measure movement strength and contradictions.  
**Can it display?** Display only the summary result, not full internal details.

### 10.7 Macro USD Engine

**Purpose:** Read USD pressure or support for inverse assets.  
**Position in chain:** Before Risk and Devil’s Advocate.  
**Can it display?** As support/pressure/neutral.

### 10.8 Risk Engine

**Purpose:** Evaluate risk before final objection.  
**Can it display?** Yes, in plain language.  
**Colors:** green, yellow, red.

### 10.9 Devil’s Advocate Layer

**Purpose:** Challenge the decision against objections and risks.  
**Authority:** The only layer that can perform final blocking.  
**Can its name be displayed?** Yes, as “Devil’s Advocate Layer”.  
**Displayed to user:** General objection result and brief caution reason.  
**Not displayed:** Sensitive internal rules.

### 10.10 Decision Quality Engine

**Purpose:** Convert layer results into a decision-quality score.  
**Outputs:** score from 0 to 100, confidence level, quality state.

### 10.11 Final State Engine

**Purpose:** Produce the final state.  
**States:**

```txt
UNDER_MONITORING
CAUTION
ALLOWED_WITH_CAUTION
BLOCKED
DATA_NOT_READY
```

---

## 11. Governance Map

### 11.1 Change Rules

1. Every change starts with a backup.
2. Every change ends with a report.
3. Multiple scopes must not be changed unless planned.
4. Random script stacking is prohibited.
5. When a change fails, rollback before adding more patches.
6. Official pages must not be deleted without Owner approval.
7. Menu page names must not change unless the map is updated.
8. Every new API must be documented.
9. Every new JSON field must be documented.
10. Every new engine must be added to the engine map.

### 11.2 Display and Hiding Rules

- Only approved names appear to users.
- Protected layers appear as states or quality, not as internal names.
- Sensitive calculation details are hidden.
- The UI must not display raw debug output.
- Error messages must not expose secrets or sensitive internal paths.

### 11.3 Decision Rules

- NDSP does not recommend buying or selling.
- Outputs are decision-support only.
- Devil’s Advocate is the final blocking layer.
- A decision is not final if data is outdated.
- If a key data provider fails, show DATA_NOT_READY or UNDER_MONITORING.

---

## 12. Permission Map

```txt
Visitor
- Views landing page.
- Views packages.
- Registers an account.

Trial User
- Enters portal after accepting disclaimer.
- Views basic reading.
- Tries limited alerts.

Subscriber
- Views expanded reading.
- Configures more alerts.
- Uses advanced mode.

Admin
- Manages users.
- Reviews logs.
- Monitors services.

Owner
- Approves governance.
- Holds Manual Override authority.
- Views sensitive settings.
- Approves releases.
```

---

## 13. Security Map

### 13.1 Security Basics

- Hash passwords using an appropriate algorithm.
- Never store original passwords.
- Use secure sessions.
- Enforce HTTPS.
- Configure CORS safely.
- Apply rate limiting.
- Prevent brute force attempts.
- Protect reset password tokens.
- Prevent duplicated email and phone.
- Keep API keys only in backend environment variables.
- Never print secrets in logs.

### 13.2 Admin Console Security

- Only Admin and Owner can access it.
- Every admin action is logged.
- Bulk destructive actions require confirmation.
- Sensitive data is not exposed unless needed.

### 13.3 API Protection

- Every sensitive API requires a token.
- Every token has permissions and expiration.
- Every admin request is logged.
- Error messages do not expose internal architecture.

---

## 14. Testing Map

### 14.1 Functional Tests

- Registration works.
- Duplicate email is blocked.
- Duplicate phone is blocked.
- Login works.
- Password reset works.
- Disclaimer is mandatory.
- Asset page displays data.
- Command Center displays radar.
- Daily Brief text does not overlap.
- Settings save correctly.

### 14.2 API Tests

- `/api/health` returns OK.
- `/api/decision/quality-live` returns valid JSON.
- Required fields exist.
- Invalid symbol returns 400 or 404.
- Price-provider failure returns 503 or a clear fallback state.

### 14.3 Security Tests

- Regular users cannot access Admin.
- API keys are not exposed in frontend.
- Reset tokens expire.
- Passwords are never visible.
- CORS is configured.

### 14.4 UI Tests

- Mobile layout.
- Desktop layout.
- Arabic RTL.
- No text overlap.
- Menu does not disappear.
- Radar does not disappear.
- Loading and error states.

### 14.5 Regression Tests

Every change must confirm that it did not break:

- Landing page.
- Login.
- Registration.
- Asset page.
- Command Center.
- Radar.
- Decision API.
- Side menu.

---

## 15. Deployment Map

### 15.1 Environments

```txt
local       personal development
development shared development
staging     pre-production testing
production  live operation
```

### 15.2 Production Elements

```txt
Domains:
- ndsp.app
- my.ndsp.app
- api.ndsp.app

Services:
- frontend service
- backend API service
- market data bridge
- decision engine service
- database
- nginx
- SSL certificates
```

### 15.3 Standard Deployment Steps

1. Take a backup.
2. Review git diff or file list.
3. Apply the change in staging if available.
4. Run tests.
5. Build frontend.
6. Restart only the required service.
7. Run health check.
8. Test core pages.
9. Test decision API.
10. Save deployment report.

### 15.4 Rollback Plan

Every deployment must include:

- Backup path.
- Rollback command.
- Modified files.
- Restarted services.
- Test result.

---

## 16. Operations and Monitoring Map

### 16.1 What to Monitor

- Website status.
- API status.
- Database status.
- Price provider status.
- 500 errors.
- Login failures.
- Registration failures.
- SSL expiration.
- Disk usage.
- Memory usage.
- Stopped services.
- Slow responses.

### 16.2 Core Health Checks

```txt
GET /api/health
GET /api/decision/quality-live?symbol=ETHUSDT
GET /api/assets
GET /login
GET /register
GET /NDSP_Command_Center.html
```

### 16.3 Monitoring Reports

- Simple daily report.
- Weekly status report.
- Immediate critical-error report.
- Usage and user-experience report.

---

## 17. Maintenance Map

### 17.1 Daily

- Check services.
- Check 500 errors.
- Check live prices.
- Check disk usage.

### 17.2 Weekly

- Review logs.
- Test registration and login.
- Test live decision API.
- Clean temporary files.
- Review backups.

### 17.3 Monthly

- Security review.
- Safe package updates.
- Performance review.
- Governance review.
- User-experience review.

---

## 18. Required Documentation Map

```txt
README.md
SYSTEM_BUILD_AND_READINESS_CATALOG.md
API_CONTRACT.md
DATABASE_SCHEMA.md
DECISION_ENGINE_MAP.md
FRONTEND_PAGE_MAP.md
GOVERNANCE_RULES.md
DEPLOYMENT_GUIDE.md
ROLLBACK_GUIDE.md
TESTING_PLAN.md
SECURITY_POLICY.md
USER_GUIDE.md
ADMIN_GUIDE.md
CHANGELOG.md
```

---

## 19. Change Report Template

Every change must produce a report in this format:

```txt
Change title:
Date:
Executor:
Scope:
Reason:
Modified files:
Affected services:
Backup path:
Execution steps:
Test results:
Issues:
Rollback method:
Final status:
```

---

## 20. Release Gates

No release is approved unless it passes:

1. Page works.
2. API works.
3. Registration and login work.
4. Radar does not disappear.
5. Menu does not disappear.
6. Live data appears or a clear fallback state appears.
7. No direct buy/sell recommendation exists.
8. No secrets are exposed.
9. Mobile layout is acceptable.
10. Release report is saved.
11. Rollback plan exists.
12. Mandatory disclaimer is active.

---

## 21. Suggested Roadmap

### v1.0 — Platform Foundation

- Landing page.
- Registration and login.
- User portal.
- Disclaimer acceptance.
- Live decision API.
- Asset page.
- Command Center.

### v1.1 — Governance and Consistency

- Standardize page names.
- Remove duplication.
- Document API.
- Stabilize side menu.
- Stabilize radar.

### v1.2 — Scenario Levels

- Activate activation, arrival, review, and invalidation levels.
- Bind them to real data.
- Add under-verification states.

### v1.3 — Alerts

- User alerts.
- Alert channels.
- Asset settings.

### v1.4 — Administration

- Admin dashboard.
- Logs.
- Service monitoring.

### v2.0 — Subscriptions and Production Growth

- Plans and packages.
- Advanced permissions.
- Usage reports.
- User-experience improvements.

---

## 22. Short Checklist Before Assigning Work to a Developer or AI Tool

Before asking any developer or AI tool to modify NDSP, provide:

- Target page name.
- Correct route/path.
- Exact issue.
- Files allowed to be touched.
- Files prohibited from being touched.
- Data source.
- Governance rules.
- Required test.
- Condition not to break design.
- Backup condition.
- Execution report condition.

### Safe Prompt Format

```txt
Modify only the specific scope below. Do not rename pages, do not remove the menu, do not touch the backend unless explicitly stated, and do not stack new scripts if an existing shared file can be used. Take a backup before execution, write an execution report after completion, and test the page and its related API.
```

---

## 23. Executive Summary

This catalog is the safety system for NDSP. The project does not only need code; it needs a map that prevents chaos. Every page must know its role, every API must know its contract, every engine must know its position, and every change must leave a documented trace.

If this catalog is followed, NDSP becomes a buildable, maintainable, marketable system instead of a collection of pages and patches.
