# NDSP Active /opt Services Staging

Generated: 2026-08-06T10:43:40+02:00

Canonical project:

`/home/nawaf511/empire-core-new`

Staging root:

`/home/nawaf511/empire-core-new/runtime/opt-services`

## Important

- لم يتم إيقاف أي خدمة.
- لم يتم تعديل systemd.
- لم يتم حذف أي مسار من /opt.
- هذه مرحلة نسخ وتحقق فقط.

## Services

```text
service                                       source                                     destination                                                                                          active  copy_status  verification
ndsp-16-layers.service                        /opt/ndsp16-api                            /home/nawaf511/empire-core-new/runtime/opt-services/ndsp16-api-98114d2615                            active  copied       rsync-dry-run-clean
ndsp-admin-user-ops.service                   /opt/ndsp-admin-user-ops                   /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-admin-user-ops-56dc62c37f                   active  copied       rsync-dry-run-clean
ndsp-auth-core-clean.service                  /opt/ndsp-auth-core-clean/current          /home/nawaf511/empire-core-new/runtime/opt-services/current-e13df671b8                               active  copied       rsync-dry-run-clean
ndsp-change-password-gateway.service          /opt/ndsp-change-password-gateway          /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-change-password-gateway-04d5fbac32          active  copied       rsync-dry-run-clean
ndsp-commercial-auth-payment-staging.service  /opt/ndsp-commercial-auth-payment-staging  /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-commercial-auth-payment-staging-e9587598ba  active  copied       rsync-dry-run-clean
ndsp-current-user-display.service             /opt/ndsp-current-user-display             /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-current-user-display-446734503e             active  copied       rsync-dry-run-clean
ndsp-decision-package-v1.service              /opt/ndsp-decision-package-v1              /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-decision-package-v1-7db4e1e2c9              active  copied       rsync-dry-run-clean
ndsp-market-data-bridge-v2.service            /opt/ndsp-market-data-bridge-v2            /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-market-data-bridge-v2-0fa8009bd7            active  copied       rsync-dry-run-clean
ndsp-news-ticker.service                      /opt/ndsp-news-ticker                      /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-news-ticker-fd8c508f6b                      active  copied       rsync-dry-run-clean
ndsp-platform-gateway-9002.service            /opt/ndsp-platform-gateway-9002            /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-platform-gateway-9002-55c51a91c1            active  copied       rsync-dry-run-clean
ndsp-public-summary-v548.service              /opt/ndsp-public-summary-v548              /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-public-summary-v548-189d4a05bc              active  copied       rsync-dry-run-clean
ndsp-registration-consent-v42.service         /opt/ndsp/legal-v42                        /home/nawaf511/empire-core-new/runtime/opt-services/legal-v42-729774de5b                             active  copied       rsync-dry-run-clean
ndsp-ui-bridge-api.service                    /opt/ndsp-ui-bridge-api                    /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-ui-bridge-api-706e22e798                    active  copied       rsync-dry-run-clean
ndsp-v3-portal-gateway.service                /opt/ndsp-v3-portal-gateway                /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-v3-portal-gateway-b0c8082879                active  copied       rsync-dry-run-clean
ndsp-v52-contract.service                     /opt/ndsp-v52-contract                     /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-v52-contract-901f5d55ee                     active  copied       rsync-dry-run-clean
ndsp-v53-bridge.service                       /opt/ndsp-v53-bridge                       /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-v53-bridge-273e3a75bc                       active  copied       rsync-dry-run-clean
```

## Next gate

لا يتم Cutover إلا للخدمات التي تحقق:

`copy_status=copied`

و

`verification=count-and-size-match`
