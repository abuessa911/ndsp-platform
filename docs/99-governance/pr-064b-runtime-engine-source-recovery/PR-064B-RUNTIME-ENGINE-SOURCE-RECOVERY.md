# PR-064B — Runtime Engine Source Recovery

## Purpose

Recover the currently running Decision Governance Core source into Git without
changing its bytes, behavior, routes, configuration semantics, systemd unit,
database, Nginx, or production runtime.

## Source

- Runtime source:
  `/home/nawaf511/empire-core-new/backend/services/decision_governance_core`
- Recovered repository path:
  `backend/services/decision_governance_core/`
- Base commit: `5d84640e0273547186c846459079a4534cae4ed2`

## Recovery controls

- Recovered files: **14**
- Excluded files: **633**
- Source/recovered byte identity: **PASS**
- Secret scan: **PASS**
- Runtime data excluded: **PASS**
- `node_modules` excluded: **PASS**
- Symlinks excluded: **PASS**

## Expected recovered routes

- `GET /health`
- `POST /api/governance/evaluate`
- `POST /api/governance/submit`

## Explicit non-goals

This PR does not:

- correct direction logic;
- change timing logic;
- create CORE or EXPANDED stores;
- modify systemd;
- modify Nginx;
- restart services;
- execute HTTP mutations;
- install dependencies;
- deploy recovered source.

## Safety invariants

- Behavior changes: **0**
- Direction logic changes: **0**
- systemd changes: **0**
- Nginx changes: **0**
- Database changes: **0**
- Production services restarted: **0**
- Runtime changes: **none**

## Next step

After merge and review, PR-064 may change direction behavior in a separate
shadow-only implementation with PR-063 contracts and regression fixtures.
