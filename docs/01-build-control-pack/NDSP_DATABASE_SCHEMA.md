# NDSP Database Schema Map

> NDSP لا تبني شاشة؛ NDSP تبني غرفة قرار.

## Core Tables
- users
- subscriptions
- trial_sessions
- assets
- market_prices
- cot_data
- decision_readings
- scenario_levels
- alerts
- audit_logs
- admin_actions
- password_resets
- api_errors
- release_reports

## Required Rules
- email unique
- phone unique after digit normalization
- password_hash only, never plain password
- admin actions recorded
- migrations require backup
