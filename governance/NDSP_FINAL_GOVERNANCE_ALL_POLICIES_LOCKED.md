# NDSP FINAL GOVERNANCE — ALL POLICIES LOCKED

Project: NDSP — منصة نواف لدعم القرار
English: NDSP — Nawaf Decision Support Platform
Status: AUTHORITATIVE_FINAL_LOCKED
Server Governance Path: /home/nawaf511/empire-core-new/governance
Local Preparation Path: /home/nawaf/Desktop/g

---

## 1) Master Operating Mode

NDSP is a governed decision-support SaaS.

Mandatory constants:

- MODE=DECISION_ACTIVE
- EXECUTION_POLICY=EXECUTION_SANITIZED
- ALL_LAYERS_PARTICIPATE=True
- NO_LAYER_DISABLED=True
- DIRECT_TRADE_EXECUTION=False
- PUBLIC_OUTPUT_SANITIZED=True
- NO_FINANCIAL_ADVICE=True
- NO_GUARANTEED_RESULTS=True
- NO_SECRET_EXPOSURE=True
- FRONTEND_IS_DISPLAY_ONLY=True
- BACKEND_IS_DECISION_AUTHORITY=True

The backend creates governed decision outputs.
The frontend displays backend-governed outputs only.
The user sees value, not the internal recipe.

NDSP is not:

- trading bot
- signal provider
- financial advisor
- automated execution platform
- guaranteed-profit system
- portfolio manager
- fund manager

---

## 2) Official Paths

Official root:

- /home/nawaf511/empire-core-new

Official backend:

- /home/nawaf511/empire-core-new/backend

Official governance folder:

- /home/nawaf511/empire-core-new/governance

Official frontend source folders:

- /home/nawaf511/empire-core-new/apps/public-landing
- /home/nawaf511/empire-core-new/apps/user-portal
- /home/nawaf511/empire-core-new/apps/admin-console

Shared packages:

- /home/nawaf511/empire-core-new/packages/ui
- /home/nawaf511/empire-core-new/packages/i18n
- /home/nawaf511/empire-core-new/packages/config
- /home/nawaf511/empire-core-new/packages/governance

Published output paths:

- /var/www/ndsp
- /var/www/ndsp-my
- /var/www/ndsp-admin

Rule:

- /var/www is deployment output only.
- Permanent frontend source must stay under apps.

---

## 3) Canonical Domains

- ndsp.app = public landing only
- my.ndsp.app = user portal only
- admin.ndsp.app = admin operations center only
- api.ndsp.app = backend API only

Forbidden:

- duplicate dashboards
- duplicate admin consoles
- public /admin page under ndsp.app
- old pages left published
- frontend decision logic
- secrets inside frontend files

---

## 4) Trial To Package Dashboard Mode

The user portal supports:

- TRIAL_EXPERIENCE
- PACKAGE_BASED_EXPERIENCE

Rule:

- If trial_active is true and trial_days_remaining is greater than 0, dashboard_mode is TRIAL_EXPERIENCE.
- Otherwise dashboard_mode is PACKAGE_BASED_EXPERIENCE.

Trial duration:

- 16 days

Final trial seat distribution:

- Total: 50
- Ordinary beginner users: 25
- Specialist / academic users: 10
- Private / premium users: 15

Cancelled old distribution:

- Ordinary: 20
- Specialist: 10
- Featured: 20

The old distribution is cancelled and replaced by the final 25 / 10 / 15 distribution.

---

## 5) SaaS Packages

Active packages:

- Free
- Pro
- Elite
- Institutional Suite

### Free

- Markets: 1
- Assets: 2
- Daily analyses: 1
- Visible named layers: none
- Alerts: none
- API: no
- Webhooks: no
- Teams: no
- Reports: no

### Pro

- Markets: 2
- Assets: 20
- Daily analyses: 15
- Visible named layers:
  - TDL
  - NMP
- Devil's Advocate: hidden by name, sanitized output allowed
- Nawaf Golden Alignment: hidden by name, sanitized output allowed
- Alerts: basic limited
- API: no
- Webhooks: no

### Elite

- Markets: all supported markets
- Assets: 100
- Daily analyses: 250
- Visible named layers:
  - TDL
  - NMP
  - Devil's Advocate
  - Nawaf Golden Alignment
- Advanced Telegram alerts: yes
- Comparison: yes
- Decision journal: yes
- Scenario follow-up: yes

### Institutional Suite

- Markets: all supported markets
- Assets: 250+ or contract-based
- Daily analyses: contract-based
- Visible named layers:
  - TDL
  - NMP
  - Devil's Advocate
  - Nawaf Golden Alignment
- API Decision Output: enabled
- Webhooks: enabled
- Teams: enabled
- Reports: enabled
- Custom assets: contract-based
- Usage limits: contract-based

---

## 6) Layer Name Masking

Total internal layers: 16
Visible named layers: 4
Hidden named layers: 12

Only these four names may appear according to package:

- TDL — منطق البعد الزمني
- NMP — نقطة التقاء نواف
- Devil's Advocate — محامي الشيطان
- Nawaf Golden Alignment — إشارة نواف الذهبية

The other 12 layer names are always hidden.

Hidden layers may participate in outputs, but must not expose:

- names
- internal IDs
- order
- formulas
- weights
- raw logic
- source categories
- contract sums
- buy/sell raw signs
- raw scoring
- calculation method
- internal sequence

Allowed public output categories:

- directional bias
- reading horizon
- horizon strength
- market state
- liquidity state
- risk state
- volatility state
- sentiment state
- decision quality
- scenario follow-up
- caution reason
- sanitized summary

---

## 7) TDL v2 Governance

TDL is:

- Timed Direction Logic
- منطق البعد الزمني

TDL is one of the four approved visible named layers.

### L&M

Primary source:

- Asset Managers

Fallback source:

- Commercials

Authority days:

- Monday
- Friday

### S

Primary source:

- Leveraged Funds

Fallback source:

- Non-Commercials

Authority days:

- Tuesday
- Wednesday
- Thursday
- Saturday
- Sunday

Forbidden public exposure:

- raw COT categories
- contract sums
- plus/minus signs
- exact formulas
- exact thresholds
- weights
- raw scoring
- authority switching formula

### TDL Add-on 01 — Trade Horizon Alignment

If L&M weekly direction agrees with S direction:

- horizon_style = SWING
- public label = أفق متابعة ممتد

If L&M weekly direction disagrees with S direction:

- horizon_style = SCALPING
- public label = أفق متابعة قصير

No public execution wording is allowed.

Forbidden:

- enter swing
- scalp now
- buy
- sell
- execute

### TDL Add-on 02 — Strength Filter

Inputs:

- L&M direction
- S direction
- liquidity
- buy-side contract-sum sign
- sell-side contract-sum sign

Rule:

If buy-side sign is similar to sell-side sign:

- direction clarity = non-explicit
- strength = WEAK
- public label = الأفق قصير

If buy-side sign is different from sell-side sign:

- direction clarity = exposed / clearer
- strength = STRONG
- public label = الأفق ممتد

This applies whether direction is bullish or bearish.

Forbidden public exposure:

- raw plus/minus comparison
- contract sums
- source categories
- exact logic
- formula
- weights

---


### TDL_PRIMARY_SOURCE_REVISION_20260603

Final TDL primary source revision:

- L&M primary source: Asset Managers only.
- L&M fallback source remains: Commercials.
- S primary source: Leveraged Funds only.
- S fallback source remains: Non-Commercials.

Other Reportables and Dealer Intermediary are not primary authority sources under the final TDL source priority policy.
Public output remains sanitized and must not expose raw source names, contract sums, raw signs, formulas, weights, or calculation methods.

---

## 8) NMP Governance

NMP:

- Nawaf Meeting Point
- نقطة التقاء نواف

Visibility:

- Free: hidden by name
- Pro: visible by name
- Elite: visible by name
- Institutional Suite: visible by name

Allowed public value:

- convergence context
- agreement quality
- decision alignment
- contextual confirmation
- safe summary

Forbidden:

- exact formula
- internal scoring
- hidden layer mapping
- raw weights
- raw recipe

---

## 9) Devil's Advocate Governance

Devil's Advocate:

- محامي الشيطان

Visibility:

- Free: hidden by name
- Pro: hidden by name; sanitized output allowed
- Elite: visible by name
- Institutional Suite: visible by name

Allowed public value:

- challenge scenario
- caution reason
- weakness review
- contradiction check
- decision-quality warning

Forbidden:

- raw adversarial scoring
- internal prompt
- hidden dependency
- private calculation
- direct trading command

---

## 10) Nawaf Golden Alignment Governance

Nawaf Golden Alignment:

- إشارة نواف الذهبية

Visibility:

- Free: hidden by name
- Pro: hidden by name; sanitized output allowed
- Elite: visible by name
- Institutional Suite: visible by name

Allowed public value:

- high alignment condition
- decision-quality enhancement
- contextual strength marker
- confirmation narrative
- safe quality label

Forbidden:

- guarantee
- profit certainty
- raw formula
- secret scoring
- hidden sequence
- execution instruction

---

## 11) Scenario Reference Levels

Allowed fields:

- scenario_state
- scenario_directional_context
- scenario_activation_level
- scenario_arrival_level
- scenario_invalidation_level
- scenario_review_zone
- scenario_time_horizon
- scenario_confidence_band
- scenario_risk_note
- scenario_follow_up_note
- scenario_last_updated
- scenario_status_label
- governance_note

Arabic labels:

- مستوى تفعيل السيناريو
- مستوى وصول السيناريو
- مستوى إلغاء السيناريو
- منطقة مراجعة السيناريو
- أفق متابعة السيناريو
- نطاق ثقة السيناريو
- ملاحظة المتابعة

Scenario activation level:

- A contextual reference level where the scenario becomes active for monitoring.

Scenario arrival level:

- A contextual reference zone where the monitored scenario may be considered to have reached its expected area.

Scenario invalidation level:

- A contextual reference level where the current scenario is no longer supported and requires cancellation or reassessment.

Scenario review zone:

- A zone where the scenario should be re-evaluated because market behavior may be changing.

Required Arabic disclaimer:

- مستويات السيناريو هي مراجع سياقية لدعم القرار فقط، وليست نصيحة مالية أو أمر تداول أو توجيه تنفيذ أو ضمانًا للنتائج.

Required English disclaimer:

- Scenario levels are contextual decision-support references only. They are not financial advice, trade instructions, execution orders, or guaranteed outcomes.

Forbidden terms:

- entry
- take profit
- stop loss
- buy now
- sell now
- open position
- close position
- execute
- guaranteed target
- financial advice
- signal provider
- trading bot
- دخول
- جني ربح
- وقف خسارة
- شراء الآن
- بيع الآن
- افتح صفقة
- أغلق صفقة
- نفذ
- هدف مضمون
- نصيحة مالية
- مزود توصيات
- بوت تداول

---

## 12) Backend Feature Audit

Every backend feature, endpoint, route, service, engine, and output must be classified as one of:

- VISIBLE_BY_PACKAGE
- INTERNAL_PROTECTED
- ROADMAP_DEFERRED
- NEEDS_FRONTEND_BINDING
- ADMIN_ONLY
- LEGAL_ONLY
- DEPRECATED
- QUARANTINED

Audit targets:

- API routes
- Auth routes
- User dashboard routes
- Admin routes
- Payment routes
- Trial routes
- Telegram routes
- Email routes
- Webhook routes
- WebSocket routes
- Live alerts
- Market data engine
- Decision engine
- TDL
- NMP
- Devil's Advocate
- Nawaf Golden Alignment
- Public sanitizer
- Layer output processors
- Health endpoints
- Reports
- Audit logs

---

## 13) Registration Anti-Abuse

Registration must check:

- email uniqueness
- phone uniqueness
- device fingerprint hash
- IP hash
- IP risk score
- browser signature
- invite token
- registration velocity
- repeated attempts
- suspicious patterns

Backend decisions:

- ALLOW
- PENDING_REVIEW
- BLOCK_DUPLICATE
- RATE_LIMITED
- HIGH_RISK_DUPLICATE

The frontend may collect safe signals only.
The backend must enforce the decision.

---

## 14) Legal Entry Acknowledgment

Before entry, user must acknowledge:

- NDSP is decision-support and contextual analysis.
- NDSP is not an investment firm.
- NDSP does not provide binding financial recommendations.
- NDSP does not manage funds.
- NDSP does not guarantee profits or results.
- Trial period is 16 days.
- User accepts the legal notice explicitly.

---

## 15) Admin Operations Center

The admin console is a general NDSP Operations Center.

It manages:

- users
- trials
- packages
- subscriptions
- payments
- manual review
- markets
- assets
- alerts
- Telegram status
- email status
- webhooks
- engines
- layer governance status
- reports
- backups
- snapshots
- health checks
- audit logs
- registration review
- UX analytics
- security review
- translation controls

It must not expose:

- admin action keys
- Telegram bot token
- SMTP password
- NOWPayments secret
- database credentials
- raw hidden formulas
- internal weights
- private runtime equations
- hidden layer internals

---

## 16) Telegram / Alerts Governance

Package policy:

- Free: no alerts
- Pro: basic limited alerts
- Elite: advanced Telegram alerts
- Institutional Suite: multi-channel alerts and webhooks by contract

Admin may show:

- configured / not configured
- last test status
- last sent time
- channel status
- Telegram helper status

Admin must not show:

- bot token
- raw chat secrets
- SMTP secret
- webhook secret
- unmasked API key

---

## 17) Payments / Subscriptions Governance

Payment and subscription logic must remain server-side.

Allowed payment states:

- pending
- pending_review
- confirmed
- rejected
- expired
- refunded
- manual_review_required

Rules:

- no auto activation without backend approval
- manual review allowed
- admin confirmation required where configured
- secrets remain server-side
- frontend displays state only

---

## 18) Frontend Source Architecture

Official source folders:

- /home/nawaf511/empire-core-new/apps/public-landing
- /home/nawaf511/empire-core-new/apps/user-portal
- /home/nawaf511/empire-core-new/apps/admin-console

Recommended stack:

- public-landing = Astro + TypeScript + Tailwind
- user-portal = Next.js App Router + TypeScript + Tailwind
- admin-console = Next.js App Router + TypeScript + Tailwind

Rules:

- /var/www is output only
- permanent UI source belongs under apps
- emergency patches must be backported
- duplicate frontend sources are forbidden
- frontend must not replace backend decision logic

---

## 19) Flexible Maximum Security

Required:

- server-side secrets only
- admin gateway only
- no admin keys in localStorage
- no public Telegram tokens
- no public SMTP secrets
- no public NOWPayments secrets
- no database URLs in frontend
- rate limiting
- abuse scoring
- session protection
- audit logs
- safe error messages
- public output sanitization
- hidden layer name enforcement
- backup before patch
- report after patch
- health checks

Frontend files must not contain:

- X-NDSP-ADMIN-KEY
- NDSP_ADMIN_ACTION_KEY
- TELEGRAM_BOT_TOKEN
- SMTP_PASS
- NOWPAYMENTS secret/key
- DATABASE_URL
- postgres://
- redis:// with credentials
- raw tokens

---

## 20) Global Translation + Hebrew Block

Primary languages:

- Arabic
- English

Arabic supports RTL.
English supports LTR.

Hebrew is blocked.

Blocked identifiers:

- he
- he-IL
- iw
- Hebrew

NDSP must not:

- provide Hebrew selector
- create Hebrew locale files
- generate Hebrew public pages
- add Hebrew routing
- accept Hebrew through i18n APIs
- produce public decision output in Hebrew

External translation defense:

- translate=no
- class=notranslate
- meta google notranslate
- protected output wrappers
- no Hebrew files
- no Hebrew selectors

NDSP cannot guarantee control over external browser tools, but must not support or facilitate Hebrew internally.

---

## 21) UX Intelligence

Allowed UX signals:

- page view
- feature usage
- navigation flow
- form completion
- trial activation status
- survey response
- feedback rating
- tooltip interaction
- package interest
- support request category
- device category
- browser category
- drop-off point
- registration flow
- login success/failure
- dashboard navigation
- asset selection
- market selection
- analyze success/failure
- API errors
- button interactions
- trial progress
- feedback completion
- upgrade intent
- language selection
- plan-limit friction
- alert setup flow

Forbidden UX data:

- passwords
- secrets
- tokens
- payment keys
- admin keys
- raw hidden formulas
- layer weights
- private runtime equations
- raw device fingerprint shown publicly
- unmasked IP risk formula
- unmasked abuse score
- hidden layer names

---

## 22) AI Integration Law 16

Official paths:

- OFFICIAL_ROOT=/home/nawaf511/empire-core-new
- OFFICIAL_BACKEND=/home/nawaf511/empire-core-new/backend
- OFFICIAL_TEST_DIR=/home/nawaf511/empire-core-new/tests
- OFFICIAL_REPORT_DIR=/home/nawaf511/ndsp_launch_reports
- OFFICIAL_BACKUP_DIR=/home/nawaf511/ndsp_backups
- OFFICIAL_SNAPSHOT_DIR=/home/nawaf511/ndsp_snapshots

Forbidden:

- inventing paths
- creating alternate runtimes
- creating private reports folders
- creating tests outside official paths
- using non-approved endpoints
- creating ungoverned logic

---

## 23) PostgreSQL / Data Source Rule

Rules:

- frontend does not connect directly to database
- backend is database authority
- PostgreSQL is the active production direction
- secrets remain server-side
- legacy databases are not source of truth unless explicitly re-adopted

---

## 24) Public Output Contract

Allowed:

- market context
- directional bias
- reading horizon
- horizon strength
- scenario state
- scenario reference levels
- risk note
- caution reason
- decision quality
- sanitized summary
- package-aware visible named layers
- safe explanation

Forbidden:

- buy now
- sell now
- entry
- take profit
- stop loss
- open position
- close position
- execute
- guaranteed target
- guaranteed direction
- risk-free
- financial advice
- signal provider
- trading bot
- portfolio instruction
- order placement
- raw formulas
- raw weights
- internal scoring
- hidden layer names

---

## 25) Final Exclusions Embedded

The following are cancelled and excluded from the final governance package:

- old trial seat distribution 20 / 10 / 20
- /my/elite-trial
- /my/elite-feedback
- /my/elite-discount
- /my/elite-lab
- /elite-trial
- Elite Trial Intelligence Center
- in-trial feedback governance
- Post-Trial Operations governance
- detailed UI design system requirement
- Elite Trial API routes
- Post-Trial API routes
- proposed Elite Trial and Post-Trial database schemas
- Incident Response section from previous list

Everything else remains active.

---

## 26) Final Governance Contract

- NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED=True
- DECISION_ACTIVE=True
- EXECUTION_SANITIZED=True
- ALL_LAYERS_PARTICIPATE=True
- NO_LAYER_DISABLED=True
- HIDDEN_LAYERS_PROTECTED=True
- APPROVED_LAYER_NAMES_ONLY=True
- FRONTEND_IS_DISPLAY_ONLY=True
- BACKEND_IS_DECISION_AUTHORITY=True
- VAR_WWW_IS_OUTPUT_ONLY=True
- OFFICIAL_SOURCE_REQUIRED=True
- PACKAGE_LIMITS_BACKEND_ENFORCED=True
- TRIAL_LIMITS_BACKEND_ENFORCED=True
- REGISTRATION_ABUSE_PROTECTION=True
- ADMIN_OPERATIONS_CENTER=True
- SECRETS_MASKED=True
- HEBREW_BLOCK=True
- UX_SAFE_ANALYTICS=True
- DUPLICATE_PAGES_FORBIDDEN=True
- TDL_V2_GOVERNED=True
- TDL_ADDON_01_TRADE_HORIZON_ALIGNMENT=True
- TDL_ADDON_02_STRENGTH_FILTER=True
- SCENARIO_REFERENCE_LEVELS_ALLOWED=True
- PUBLIC_OUTPUT_SANITIZED=True
- RAW_LOGIC_EXPOSED=False
- FORMULAS_EXPOSED=False
- WEIGHTS_EXPOSED=False
- HIDDEN_LAYER_NAMES_EXPOSED=False

Final rule:

Expose the governed decision value.
Hide the internal recipe.

FINAL_STATUS=NDSP_FINAL_GOVERNANCE_ALL_POLICIES_LOCKED

---

## Frontend Source Enforcement Addendum

Status: AUTHORITATIVE_LOCKED_ADDENDUM

Frontend source of truth:

- /home/nawaf511/empire-core-new/apps/public-landing
- /home/nawaf511/empire-core-new/apps/user-portal
- /home/nawaf511/empire-core-new/apps/admin-console

Deployment mapping:

- /var/www/ndsp -> /home/nawaf511/empire-core-new/apps/public-landing
- /var/www/ndsp-my -> /home/nawaf511/empire-core-new/apps/user-portal
- /var/www/ndsp-admin -> /home/nawaf511/empire-core-new/apps/admin-console

Rule:

- /var/www is not a source folder.
- /var/www must only point to the official apps frontend sources.
- Any frontend edit must be applied to apps first.
- Old standalone files under /var/www are forbidden.
- Nginx may serve /var/www paths only when they are symlinked to official apps sources.

FINAL_STATUS=NDSP_FRONTEND_SOURCE_ENFORCEMENT_LOCKED

