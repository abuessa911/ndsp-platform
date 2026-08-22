# ADR-0005 — Repository Hygiene

## Status

Accepted

## Date

20260628_000901

## Context

The NDSP repository contains source code, generated files, runtime files, backups, virtual environments, dependencies, and local secrets.

## Decision

DEV-002 introduces a strict repository hygiene policy:

- Do not track secrets.
- Do not track dependency folders.
- Do not track build outputs.
- Do not track logs.
- Do not track runtime backups.
- Keep source files trackable.
- Keep example environment files trackable.

## Protected examples

The following remain allowed:

- .env.example
- .env.*.example
- backend/.env.example
- backend/.env.telegram.example

## Scope

This task does not delete files. It only controls Git tracking.
