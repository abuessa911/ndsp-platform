# NDSP Telegram Alerting Governance

Approved files:
- /etc/ndsp/ndsp-telegram.env
- /usr/local/bin/ndsp_auto_telegram_health_alert.sh
- /etc/systemd/system/ndsp-telegram-alert.service
- /etc/systemd/system/ndsp-telegram-alert.timer

Approved behavior:
- Telegram token is loaded from secure env.
- Chat ID is loaded from secure env.
- Direct send test must return HTTP 200.
- Timer must be enabled and active.
- Token must not be logged or exposed.
