# NDSP NOWPayments And Trial Payment Governance

NOWPayments integration exists and health/webhook endpoints are active.

Approved endpoints:
- /api/nowpayments/health
- /api/webhooks/nowpayments
- /api/plans

Policy:
1. NOWPayments keys must remain server-side only.
2. Public frontend must not expose payment secrets.
3. Paid launch must not be activated automatically unless approved.
4. Trial messaging must not imply guaranteed paid access.
5. Manual/admin review remains valid for activation-sensitive flows.
