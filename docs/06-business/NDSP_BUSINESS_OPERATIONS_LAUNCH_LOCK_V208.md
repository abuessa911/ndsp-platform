# NDSP Business Operations Launch Lock V208

DATE=2026-07-20T18:42:31+02:00
STATUS=LIVE_AND_STABILIZED
FINALIZED_BY=V208
RECOVERY_CONTEXT=V204_ROLLED_BACK__V205_PARTIAL__V206_DIGEST_HANG__V207_STAGE_MARKER_FAILURE

## Live operational surfaces
- Onboarding: https://my.ndsp.app/start/
- Subscription requests: https://my.ndsp.app/subscribe/
- Support: https://my.ndsp.app/support/
- Marketing launch: https://my.ndsp.app/launch/
- Protected operations dashboard: https://my.ndsp.app/ops-admin/

## Runtime
- Operations service: ndsp-business-ops.service on 127.0.0.1:9094
- Production monitor timer: every 5 minutes
- Daily digest timer: 08:00 Asia/Riyadh
- Digest reports: /home/nawaf511/ndsp_launch_reports
- Durable notification outbox: /var/lib/ndsp-business-ops/outbox

## Subscription governance
- Trial duration: 16 days
- Payment auto-activation: NO
- Activation mode: manual review after payment verification
- Existing authentication database modified: NO

## V208 correction
- Blocking Postfix invocation removed from monitor and digest.
- Alerts and digests are written atomically as local .eml files.
- Oneshot services have bounded start and stop timeouts.
- V203 commercial decision runtime regression gate passed.

## Safety
- Existing frontend bundles modified: NO
- Nginx files modified: NO
- PM2 modified: NO
- Decision engines modified: NO
- Payment records modified: NO
