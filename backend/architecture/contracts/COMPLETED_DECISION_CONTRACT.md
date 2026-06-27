# Completed Decision Contract

Completed Decision is the only official decision object shared between products.

## Required Fields

- id
- symbol
- market
- decision_state
- decision_quality
- scenario_state
- direction_context
- levels.activation
- levels.arrival
- levels.review_zone
- levels.invalidation
- levels.nmp_zone
- risk_status
- devil_advocate_status
- visibility
- completed_at
- published_at
- expires_at
- disclaimer
- payload

## Consumer Rule

Consumers may read completed decisions.

Consumers may not mutate completed decisions.
