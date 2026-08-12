# NDSP P1 Controlled Auth Functional Test
DATE=2026-07-07T23:32:31+02:00
MODE=CONTROLLED_WRITE_TEST
MODIFICATIONS=One generated test account only if registration succeeds
API_BASE=https://api.ndsp.app
FRONTEND_BASE=https://my.ndsp.app
TEST_EMAIL=ndsp.p1.test.20260707_233231@example.com
TEST_PHONE=0583459951
TEST_PASSWORD=***REDACTED***

## 1) Frontend Auth Pages Sanity
[200] https://my.ndsp.app/login
[200] https://my.ndsp.app/register
[200] https://my.ndsp.app/forgot-password
[200] https://my.ndsp.app/reset-password

## 2) Trial Registration
REGISTER_CODE=200
REGISTER_BODY: 
[OK] Registration accepted

## 3) Duplicate Same Payload Check
DUPLICATE_CODE=409
DUPLICATE_BODY: 
[OK] Duplicate registration appears blocked

## 4) Login Test
LOGIN_EMAIL_CODE=200
LOGIN_EMAIL_BODY: 
[OK] Login with email accepted

## 5) Login Failure Safety Check
BAD_LOGIN_CODE=401
BAD_LOGIN_BODY: 
[OK] Wrong password rejected

## 6) Forgot Password Request Probe
FORGOT_ENDPOINT=https://api.ndsp.app/api/auth/forgot-password
FORGOT_CODE=200
FORGOT_BODY: 
[OK] Forgot password request accepted at https://api.ndsp.app/api/auth/forgot-password

## 7) Runtime Safety Check
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 0  │ ndsp-portal    │ default     │ 0.39.7  │ fork    │ 1099070  │ 2D     │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 9.4% | ram usage: 9.7% | lo: ⇓ 0.011mb/s ⇑ 0.011mb/s | eth0: ⇓ 0.108mb/s ⇑ 0.005mb/s | disk: ⇓ 0mb/s ⇑ 0.233mb/s / 81.99% |

## 8) Final Evaluation
PAGES_OK=1
REGISTER_OK=1
DUPLICATE_OK=1
LOGIN_OK=1
BAD_LOGIN_OK=1
FORGOT_OK=1

FINAL_STATUS=P1_CONTROLLED_AUTH_FUNCTIONAL_TEST_OK
AUTH_FUNCTIONAL_STATUS=OK_WITH_RESET_TOKEN_FLOW_PENDING_IF_FORGOT_NOT_CONFIRMED
REPORT=docs/05-runbooks/NDSP_P1_CONTROLLED_AUTH_FUNCTIONAL_TEST_20260707_233231.md
TEST_ACCOUNT_EMAIL=ndsp.p1.test.20260707_233231@example.com
TEST_ACCOUNT_PHONE=0583459951
TEST_PASSWORD=***REDACTED***
