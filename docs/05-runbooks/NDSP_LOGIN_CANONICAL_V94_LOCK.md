# NDSP Login Canonical V94 Lock

- Canonical live page: /var/www/ndsp-my/login/index.html
- Canonical source: /home/nawaf511/empire-core-new/frontend/ndsp-auth-canonical-v94/login/index.html
- Success target: /portal-v50/
- Login endpoint: /api/auth/login
- Session endpoint: /api/auth/session
- Design: institutional dark, black/gold, responsive Arabic RTL and English LTR
- Old login design dependencies: none
- Floating controls: forbidden
- Legacy access design markers: forbidden
- Nginx changes: none
- Database changes: none
- Generated: 20260717_151841

## Change rule

Do not patch the login page with additive experimental UI scripts.
Make future changes in the canonical source file, verify mobile and desktop, then deploy the complete standalone page.

## V95 final certification

- V94 responsive rendering: PASS
- V94 real login to /portal-v50/: PASS
- Static validator false positives removed:
  - background pseudo-element changed from fixed to absolute
  - legitimate authentication-state wording no longer matches the retired design signature scanner
- Certified: 20260717_152631
