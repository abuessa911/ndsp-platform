# PR-006 Network Exposure Review Notes

## Review result

`ACCEPTED_WITH_OWNERSHIP_WARNINGS`

- Evidence validation: `PASS`
- Unresolved listeners: `0`
- Runtime changes: `none`

## Accepted findings

- All canonical application listeners are loopback-bound.
- SSH, SMTP, Nginx, XRDP, PostgreSQL, Redis, Docker proxy, and other host dependencies are documented separately from canonical NDSP ownership.
- IPv4 and IPv6 listeners are retained as separate observed records.
- Wildcard binding is not equated with confirmed internet access.

## Ownership warnings

`42` non-canonical NDSP application listener records remain outside the PR-005 canonical ownership map.

These records have identified processes or supervisors and therefore are not unresolved. A later governance PR should decide whether each component becomes canonical, shared infrastructure, deprecated, or source-only.

## Critical network-bound ports

| Protocol | Address | Port | Process | Unit | Category |
|---|---|---:|---|---|---|
| `tcp` | `0.0.0.0` | `22` | `-` | `-` | `HOST_INFRASTRUCTURE` |
| `tcp` | `::` | `22` | `-` | `-` | `HOST_INFRASTRUCTURE` |
| `tcp` | `0.0.0.0` | `25` | `master` | `postfix@-.service` | `HOST_INFRASTRUCTURE` |
| `tcp` | `::` | `25` | `master` | `postfix@-.service` | `HOST_INFRASTRUCTURE` |
| `tcp` | `0.0.0.0` | `80` | `-` | `-` | `EDGE_PROXY` |
| `tcp` | `::` | `80` | `-` | `-` | `EDGE_PROXY` |
| `tcp` | `0.0.0.0` | `443` | `-` | `-` | `EDGE_PROXY` |
| `tcp` | `::` | `443` | `-` | `-` | `EDGE_PROXY` |
| `tcp` | `0.0.0.0` | `3000` | `node` | `pm2-nawaf511.service` | `NON_CANONICAL_APPLICATION` |
| `tcp` | `*` | `3389` | `xrdp` | `xrdp.service` | `HOST_INFRASTRUCTURE` |
| `tcp` | `0.0.0.0` | `5433` | `docker-proxy` | `docker.service` | `CONTAINER_INFRASTRUCTURE` |
| `tcp` | `::` | `5433` | `docker-proxy` | `docker.service` | `CONTAINER_INFRASTRUCTURE` |

## Required follow-up

A future firewall and ingress-policy governance review should determine effective external reachability for the `16` wildcard-bound listener records.
