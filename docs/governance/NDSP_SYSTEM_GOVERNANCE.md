# NDSP / NDIP SYSTEM GOVERNANCE

Contract Version: NDSP_GOVERNANCE_V1
Status: AUTHORITATIVE_BASELINE
Purpose: Semantic, data, decision-authority and handoff governance.

---

# 1. GOVERNING PRINCIPLE

No NDSP layer may silently reinterpret data received from another layer.

Every important value must preserve:

- canonical name
- semantic meaning
- data type
- unit
- asset identity
- asset class
- source
- source family
- dataset/report family
- source path
- timeframe
- horizon
- calculation method
- calculated time
- freshness
- completeness
- missing reason
- fallback state
- producer
- consumer
- authority
- exposure class

Missing is not zero.
Unknown is not neutral.
Stale is not fresh.
Fallback is not authoritative.

Semantic changes require a new contract version.

---

# 2. CANONICAL DATA FLOW

SOURCE
  ↓
EXTRACTION
  ↓
NORMALIZATION
  ↓
CALCULATION / DOMAIN LOGIC
  ↓
CANONICAL FIELD
  ↓
HANDOFF CONTRACT
  ↓
NEXT CONSUMER
  ↓
DECISION LOGIC
  ↓
GOVERNANCE GATE
  ↓
PUBLIC / ADMIN / BOT OUTPUT

A layer may transform data only through an explicitly registered
canonical transformation.

---

# 3. ASSET AND SOURCE ROUTING

Different asset classes may require different authoritative sources.

The system must not assume that:

- Gold
- Forex
- Bonds
- Equity indices
- Equities
- Crypto
- Commodities

share identical providers, datasets, report families or market structure.

Required routing identity:

asset
asset_class
provider
dataset
report_family
source_market
source_timeframe
analysis_timeframe

Source routing must be explicit and auditable.

---

# 4. COT / TFF CANONICAL GROUPS

Canonical groups:

ASSET_MANAGERS
LEVERAGED_FUNDS

Required directional fields:

asset_managers_overall
asset_managers_weekly
leveraged_funds_overall
leveraged_funds_weekly

Required source/freshness fields:

report_date
report_age_days
max_age_days
fresh
source
source_family
source_market
raw_cot_connected
raw_cot_status

Required numerical provenance when available:

current_long
current_short
change_long
change_short

A missing weekly field must never be converted to zero or NEUTRAL.

---

# 5. DIRECTION CALCULATION

Overall direction uses current Long and Short values.

Canonical rule:

LONG > SHORT
  => BULLISH

SHORT > LONG
  => BEARISH

LONG == SHORT
  => NEUTRAL

The comparison gap may be exposed for explanation,
but it is not the direction rule itself.

Weekly direction uses weekly Long and Short changes.

Canonical rule:

CHANGE_LONG > CHANGE_SHORT
  => BULLISH

CHANGE_SHORT > CHANGE_LONG
  => BEARISH

CHANGE_LONG == CHANGE_SHORT
  => NEUTRAL

The weekly rule is a direct comparison.
It is not defined as subtraction of the two fields.

---

# 6. INVESTMENT MODE

Mode:

INVESTMENT

Asset Managers Overall Direction:
- canonical name remains overall_direction / asset_managers_overall
- represents the overall / long-term direction
- provides the long-term directional context

Asset Managers Weekly Direction:
- canonical name remains weekly_direction / asset_managers_weekly
- represents the partial / weekly change
- is the final investment decision direction
- governs the investment transitional NMP use

NMP itself does not own decision authority.

The system must keep Overall Direction and Weekly Direction
as separate canonical concepts.

Display descriptions may differ from canonical field names.

Possible descriptive concepts:

Overall / long-term context:
"Long-term pivotal convergence points"

Weekly / transitional context:
"Short-term transitional convergence levels"
"Investment entry validation levels"

These descriptions must not replace canonical field names.

---

# 7. SPECULATION MODE

Mode:

SPECULATION

The Timing Function first determines the Control Day Classification.

Canonical flow:

TIMING FUNCTION
  ↓
CONTROL DAY CLASSIFICATION
  ↓
SELECT CORRESPONDING WEEKLY DIRECTION
  ↓
FINAL WEEKLY DECISION
  ↓
NDSP DECISION / SEPARATE SPECULATION BOT ENTRY

If:

control_day = SPECULATORS

then use:

leveraged_funds_weekly

Meaning:
Leveraged Funds Weekly Direction
= الاتجاه الأسبوعي للرافعات المالية

If:

control_day = INVESTORS

then use:

asset_managers_weekly

Meaning:
Asset Managers Weekly Direction
= الاتجاه الأسبوعي لمدراء الأصول

The Timing Function determines who controls the day.

The selected weekly direction determines the final directional
decision after the timing classification.

Do not swap these mappings.

---

# 8. NMP CANONICAL DEFINITION

Canonical name:

NMP

Canonical semantic type:

PRICE_LEVEL

Official definition:

NMP = Price Level (Open ↔ Close)

Arabic semantic definition:

نقطة التقاء نواف هي مستوى سعري ممتد بين سعر افتتاح
الشمعة وسعر إغلاق الشمعة المرجعية.

Open ↔ Close describes the two boundaries of the price level.

It MUST NOT be interpreted as arithmetic subtraction.

Required canonical NMP fields:

open_price
close_price
lower_price
upper_price
reference_candle
reference_indicator
reference_timeframe
momentum_metric
selection_rule
direction_context
source
calculated_at

lower_price = min(open_price, close_price)
upper_price = max(open_price, close_price)

NMP definition and NMP interaction interpretation are separate concerns.

---

# 9. INVESTMENT NMP

For Investment Mode:

Asset Managers Weekly Direction governs calculation/use of
the investment NMP transitional level.

The NMP represents a transitional price level related to the
weekly positioning transition.

Asset Managers Overall Direction remains the long-term context.

NMP is a decision input / validation level.

NMP does not independently issue the investment decision.

---

# 10. NMP INTERACTION LOGIC

NMP interaction rules must be represented separately from
the NMP price-level definition.

The system must preserve:

- direction context
- overall direction
- weekly direction
- which boundary was tested
- which boundary was breached
- close position
- persistence / confirmation state
- interpretation
- warning state

For corrective conditions, price behavior around Open and Close
may provide warnings concerning continuation or possible ending
of the correction.

Such warnings are evidence/context and must not silently replace
the authorized weekly directional decision.

---

# 11. DECISION AUTHORITY

The system must distinguish:

DATA PRODUCER
EVIDENCE PRODUCER
DECISION INPUT
DECISION AUTHORITY
GOVERNANCE AUTHORITY
PUBLICATION AUTHORITY
BOT EXECUTION CONSUMER

Investment:

Asset Managers Weekly Direction
is the final investment directional decision source.

Speculation:

Timing Function
determines Control Day.

Then:

SPECULATORS
  -> leveraged_funds_weekly

INVESTORS
  -> asset_managers_weekly

The selected weekly direction becomes the directional decision source.

NMP, momentum, macro, scenarios and supporting indicators
must not silently claim final decision authority.

Governance may ALLOW or WITHHOLD an output.
Governance must not fabricate the underlying direction.

---

# 12. HANDOFF INTEGRITY

Every governed handoff should preserve, where applicable:

contract_version
field_id
value
data_type
unit
semantic_role
asset
asset_class
producer
consumer
source
source_family
source_path
method_id
timeframe
horizon
observed_at
calculated_at
report_date
report_age_days
fresh
complete
missing_reason
fallback_used
quality_status
authority
exposure_class

A consumer must not infer a missing semantic attribute when
the producer is required to provide it.

---

# 13. MISSING DATA POLICY

Forbidden implicit conversions:

None -> 0
Missing -> NEUTRAL
Unknown -> NEUTRAL
Stale -> Fresh
Fallback -> Authoritative
Cross-timeframe -> Same-timeframe

Missing values must remain explicitly missing.

Required metadata:

complete
missing_components
missing_reason

Decision/publication gates may withhold output when required
canonical inputs are unavailable.

Synthetic pass values are forbidden.

---

# 14. FRESHNESS POLICY

Freshness must be computed, not guessed.

Required fields:

report_date
report_age_days
max_age_days
fresh

If report_date exists and freshness is required,
report_age_days must be calculated.

A missing report_age_days must not silently pass freshness.

---

# 15. TIMEFRAME INTEGRITY

source_timeframe and analysis_timeframe must be explicit.

Cross-timeframe substitution must not occur silently.

If cross-timeframe fallback is ever permitted, it must expose:

cross_timeframe_fallback_used = true

and identify the source timeframe.

Same-timeframe evidence must remain distinguishable from
cross-timeframe evidence.

---

# 16. ALIAS GOVERNANCE

Raw/external aliases may be accepted only at extraction boundaries.

Examples may include:

asset_managers
asset_manager
asset_manager_institutional
am

leveraged_funds
leveraged
lev_funds

After normalization, downstream contracts must use canonical names.

Aliases must never change semantic meaning.

---

# 17. PUBLIC / ADMIN EXPOSURE

Public and Admin projections are separate contracts.

Internal fields must not become public merely because they exist
in the runtime payload.

Exposure classes:

PUBLIC
ADMIN
INTERNAL
EXPERIMENTAL
WITHHELD

Exposure must be allowlisted.

---

# 18. NMP EXPOSURE

NMP may be represented publicly only according to the current
approved exposure policy.

Its canonical semantic definition remains:

PRICE_LEVEL
Open ↔ Close

Any Experimental/Admin representation must be explicitly labeled
and must not acquire decision authority through presentation.

---

# 19. BOT HANDOFF

Bots are consumers of governed decisions.

The bot handoff must identify:

analysis_mode
control_day when applicable
selected_weekly_direction
selected_weekly_direction_source
decision_direction
decision_source
decision_contract_version
freshness
quality_status
governance_status

A bot must not independently reinterpret raw COT fields when a
governed canonical decision is required.

---

# 20. LINEAGE

Every material decision field should be traceable backward:

OUTPUT
  ↓
DECISION
  ↓
SELECTED DIRECTION
  ↓
NORMALIZED INPUT
  ↓
EXTRACTED VALUE
  ↓
SOURCE DATASET

Lineage must identify the calculation method and source path.

---

# 21. CONTRACT VERSIONING

Every governed contract requires a version.

Breaking semantic changes require a new version.

Changing a field's meaning without changing its contract version
is forbidden.

Compatibility must be explicit.

---

# 22. CONTRACT CLOSURE RULE

A contract is CLOSED only when all required checks pass:

1. Source identified
2. Extraction verified
3. Normalization verified
4. Calculation verified
5. Semantic meaning verified
6. Data type verified
7. Timeframe verified
8. Horizon verified
9. Freshness verified
10. Missing-data behavior verified
11. Fallback behavior verified
12. Producer verified
13. Consumer verified
14. Decision authority verified
15. Exposure verified
16. Lineage verified
17. Runtime output verified
18. Tests/audit evidence recorded

Existence of a field alone is not sufficient for closure.

---

# 23. CURRENT CLOSURE ORDER

1. Canonical Semantic Contract
2. Asset / Source Routing Contract
3. Market Data / Candle / Timeframe Contract
4. COT / TFF Contract
5. Governing Inputs Contract
6. TDL Investment Contract
7. TDL Speculation / Control Day Contract
8. NMP Definition Contract
9. NMP Interaction Contract
10. Direction / Decision Authority Contract
11. Bot Handoff Contract
12. Score Inputs Contract
13. Evidence / Lineage / Quality Contracts
14. Governance Gate Contract
15. Public Projection Contract
16. Admin Projection Contract
17. Frontend binding validation

---

# 24. KNOWN CURRENT COT ITEMS REQUIRING VERIFICATION

Previously observed runtime state included:

asset_managers_overall = available
asset_managers_weekly = missing
leveraged_funds_weekly = missing
report_date = available
report_age_days = missing
fresh = false

These are verification targets, not permanent desired values.

The implementation must be inspected and corrected from source
rather than bypassed with synthetic values.

---

# 25. GOVERNANCE CHANGE RULE

When a new architectural or semantic rule is agreed:

1. Update this governance document.
2. Update governance_manifest.json.
3. Update affected executable contracts.
4. Add/modify tests.
5. Record audit evidence.
6. Increment version when semantics break compatibility.

Conversation-only decisions must eventually be promoted into
repository governance before being considered permanently closed.

