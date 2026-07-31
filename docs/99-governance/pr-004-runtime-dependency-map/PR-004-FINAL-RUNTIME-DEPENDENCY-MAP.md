# PR-004 Final Runtime Dependency Map

## Status

`FINAL`

- Schema version: `1.0.0`
- Runtime dependencies: `13`
- Non-canonical local component edges: `8`
- Configuration evidence records: `90`
- Runtime changes: `none`

## Runtime dependency counts

| Class | Count |
|---|---:|
| `DATABASE` | 6 |
| `EXTERNAL_DATA_PROVIDER` | 3 |
| `LOCAL_SERVICE` | 4 |

## Governance status counts

| Status | Count |
|---|---:|
| `ACCEPTED` | 12 |
| `ACCEPTED_WITH_WARNING` | 1 |

## Final runtime dependencies

| Source | Class | Target | Target kind | Protocol | Port | Status |
|---|---|---|---|---|---:|---|
| `bot-execution` | `LOCAL_SERVICE` | `completed-decision` | `CANONICAL_SERVICE` | `HTTP` | `9078` | `ACCEPTED` |
| `completed-decision` | `DATABASE` | `PostgreSQL` | `DATA_INFRASTRUCTURE` | `POSTGRESQL` | `5432_or_configured` | `ACCEPTED` |
| `decision-governance-core` | `LOCAL_SERVICE` | `completed-decision` | `CANONICAL_SERVICE` | `HTTP` | `9078` | `ACCEPTED` |
| `ndsp-launch-control-v167` | `LOCAL_SERVICE` | `ndsp-platform-backend` | `CANONICAL_SOURCE_ONLY_SERVICE` | `http` | `9020` | `ACCEPTED_WITH_WARNING` |
| `ndsp-layers-api` | `LOCAL_SERVICE` | `ndsp-live-decision-quality` | `CANONICAL_SERVICE` | `HTTP` | `9057` | `ACCEPTED` |
| `ndsp-live-decision-quality` | `EXTERNAL_DATA_PROVIDER` | `api.binance.com` | `THIRD_PARTY_SERVICE` | `https` | `443` | `ACCEPTED` |
| `ndsp-live-decision-quality` | `EXTERNAL_DATA_PROVIDER` | `query1.finance.yahoo.com` | `THIRD_PARTY_SERVICE` | `https` | `443` | `ACCEPTED` |
| `ndsp-live-decision-quality` | `EXTERNAL_DATA_PROVIDER` | `stooq.com` | `THIRD_PARTY_SERVICE` | `https` | `443` | `ACCEPTED` |
| `ndsp-platform-backend` | `DATABASE` | `PostgreSQL` | `DATA_INFRASTRUCTURE` | `POSTGRESQL` | `5432_or_configured` | `ACCEPTED` |
| `ndsp-trial-register-canonical-wrapper` | `DATABASE` | `PostgreSQL` | `DATA_INFRASTRUCTURE` | `POSTGRESQL` | `5432_or_configured` | `ACCEPTED` |
| `ndsp-trial-seats-api` | `DATABASE` | `PostgreSQL` | `DATA_INFRASTRUCTURE` | `POSTGRESQL` | `5432_or_configured` | `ACCEPTED` |
| `ndsp-user-alert-channels` | `DATABASE` | `PostgreSQL` | `DATA_INFRASTRUCTURE` | `POSTGRESQL` | `5432_or_configured` | `ACCEPTED` |
| `password-reset-gateway` | `DATABASE` | `PostgreSQL` | `DATA_INFRASTRUCTURE` | `POSTGRESQL` | `5432_or_configured` | `ACCEPTED` |

## Excluded NDSP endpoint semantics

NDSP URLs were excluded from the runtime map unless an outbound HTTP call was demonstrated.

| Semantic class | Excluded records |
|---|---:|
| `CONFIGURATION_DEFAULT` | 3 |
| `GENERATED_URL_ONLY` | 2 |
| `SEMANTICS_UNRESOLVED` | 6 |

## Scope decisions

- Environment references and file paths are retained only in the configuration evidence appendix.
- Local components absent from PR-003 are retained in a separate non-canonical component appendix.
- Generated reset links, CORS origins, incomplete localhost URLs, and unproven configuration defaults are excluded.
- The `ndsp-platform-backend` target is retained with a `SOURCE_ONLY` warning.
