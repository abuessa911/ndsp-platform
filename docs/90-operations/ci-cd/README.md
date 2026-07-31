# CI/CD Foundation

## Continuous integration

The Node CI workflow validates:

- Root dependency installation and build.
- User portal dependency installation and build.
- Production dependency audit as an advisory check.
- Required pipeline file presence.

The workflow runs on relevant pull requests, relevant pushes to `main`, and
manual dispatch.

## Release artifacts

The release workflow builds and stores:

- Root `dist/`.
- `frontend/user-portal-vite/dist/`.

It does not deploy to a runtime server. Deployment remains a separate,
explicitly approved stage because the production directory, rollback process,
health checks, and service-reload contract must be defined first.

## Node version

CI uses Node.js 22 to match the validated server toolchain.

## Runtime declaration

These pipelines build and package repository content only. They do not restart
services, modify system configuration, or deploy to production.
