# NDSP Active /opt Services Staging

Generated: 2026-08-06T23:45:21+02:00

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
ndsp-commercial-auth-payment-staging.service  /opt/ndsp-commercial-auth-payment-staging  /home/nawaf511/empire-core-new/runtime/opt-services/ndsp-commercial-auth-payment-staging-e9587598ba  active  copied       rsync-dry-run-clean
ndsp-registration-consent-v42.service         /opt/ndsp/legal-v42                        /home/nawaf511/empire-core-new/runtime/opt-services/legal-v42-729774de5b                             active  copied       rsync-dry-run-clean
```

## Next gate

لا يتم Cutover إلا للخدمات التي تحقق:

`copy_status=copied`

و

`verification=count-and-size-match`
