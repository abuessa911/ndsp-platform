# NDSP real-auth integration report

## Inputs verified

- Uploaded wrapper ZIP SHA256: `570ede2ad465ebbc2e937b2b1107131d094e203e2de8e35101f3d3d6ec3bc10e`
- Nested project ZIP SHA256: `a4d666896c40993fd42df6320cd9eb39034d99db6b29479cce9be3241634d1c7`
- Server audit SHA256: `770d6a055ffb48e601a2b0c6313edece6f6a84f8e5b5e41e9dbd41926506d84c`
- Audit final status: `REAL_AUTH_INTEGRATION_AUDIT_COMPLETE`

## Implemented

- Replaced the timer-based mock login with `POST /api/auth/login`.
- Added session verification through `GET /api/auth/session` with same-origin cookies.
- Added the login challenge step through `POST /api/auth/2fa/login/verify`.
- Added logout through `POST /api/auth/logout`.
- Added forgot/reset password pages using the audited backend routes.
- Added strict same-origin redirect validation to prevent an external redirect target.
- Added a fail-closed administration guard. A session must be authenticated and its user must carry an explicit administrator or owner role.
- Added host-aware entry behavior: `my.ndsp.app/` goes to login and `admin.ndsp.app/` goes through the protected administration route.
- Preserved the Sovereign Meridian visuals and the public/admin route families.

## Security properties

- No API secret, database credential, JWT secret, SMTP credential, privileged header, or production password is included.
- Passwords are sent only in the login/reset request body and are never written to local storage.
- Authentication requests use `credentials: include`; the backend remains responsible for `HttpOnly`, `Secure`, and `SameSite` cookie enforcement.
- Frontend route protection improves UX but does not replace authorization on every administration API endpoint.

## Production blockers discovered

1. The package has no real user-portal pages. The merge report confirms only public, authentication, and `/admin/cot/*` route families.
2. `src/data.ts` still contains presentation data; analysis and administration pages are not yet connected to their real data APIs.
3. The audit found `80` and `443` owned by Docker proxies while the inspected host Nginx configuration is therefore not proven to be the active edge configuration.
4. During the audit, `my.ndsp.app`, `admin.ndsp.app`, and `api.ndsp.app` returned HTTP `503`.
5. The exact registration request schema was not present in the uploaded contract extraction, so no speculative registration form was implemented.

## Safe decision

Do not delete the current `frontend/user-portal-vite`, deployment releases, archives, or governance roots as part of this package. First collect the Docker edge map, migrate the user pages and real page-data contracts, deploy to a staging release, and verify login/session/logout/2FA plus role enforcement. Only a later, separately approved cleanup should remove superseded frontend trees.
