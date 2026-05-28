# NDSP API Namespace Policy

Approved namespace: /api

Retired namespace: /api/v7

Rules:
1. Do not use /api/v7 in frontend files.
2. Do not create new endpoints under /api/v7.
3. Do not document /api/v7 publicly.
4. Nginx may keep an explicit retired block returning 404.
5. All new API integrations must use /api.

Approved endpoint examples:
- /api/seats/status
- /api/trial/activation-policy
- /api/trial/register/ordinary
- /api/trial/register/professional
- /api/trial/register/private-invite
- /api/trial/invites/validate
- /api/nowpayments/health
- /api/webhooks/nowpayments
- /api/plans

Verification expectations:
- https://ndsp.app/api/seats/status -> 200 GET
- https://my.ndsp.app/api/seats/status -> 200 GET
- https://admin.ndsp.app/api/seats/status -> 200 GET
- https://ndsp.app/api/v7/trial/activation-policy -> 404
- https://my.ndsp.app/api/v7/trial/activation-policy -> 404
- https://admin.ndsp.app/api/v7/trial/activation-policy -> 404

---

## Final API Namespace Closure — 20260527_171503

Official public API namespace:

```text
/api/*
```

Final public OpenAPI status:

```text
API_TOTAL=81
CANONICAL_COUNT=81
VERSIONED_TOTAL=0
NAMESPACE_STATUS=CANONICAL_OPENAPI_ONLY
```

Retired/hidden namespaces:

```text
/api/v1/*
/api/v6/*
/api/v7/*
/api/v8/*
```

Rules:
1. No new public endpoint may be created under /api/v1, /api/v6, /api/v7, or /api/v8.
2. All frontend integrations must use /api/*.
3. Compatibility bridges may remain hidden only until confirmed unused.
4. Public OpenAPI must remain canonical-only.

---

## Final API Namespace Closure — 20260528_093513

Official public API namespace:

```text
/api/*
```

Final public OpenAPI status:

```text
API_TOTAL=81
CANONICAL_COUNT=81
VERSIONED_TOTAL=0
NAMESPACE_STATUS=CANONICAL_OPENAPI_ONLY
```

Retired/hidden namespaces:

```text
/api/v1/*
/api/v6/*
/api/v7/*
/api/v8/*
```

Rules:
1. No new public endpoint may be created under /api/v1, /api/v6, /api/v7, or /api/v8.
2. All frontend integrations must use /api/*.
3. Compatibility bridges may remain hidden only until confirmed unused.
4. Public OpenAPI must remain canonical-only.
