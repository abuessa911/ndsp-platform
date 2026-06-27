# NDSP Deployment Architecture

Known public domains:

- ndsp.app
- www.ndsp.app
- my.ndsp.app
- admin.ndsp.app
- api.ndsp.app
- bot.ndsp.app

Known internal service pattern:

- 127.0.0.1:9001 Platform Gateway
- 127.0.0.1:9019 Trial Service
- 127.0.0.1:9020 Auth Service
- 127.0.0.1:9023 Admin UI Proxy
- 127.0.0.1:9024 Admin Users Readonly
- 127.0.0.1:9057 Live Market / Decision Quality Bridge
- 127.0.0.1:9061 Decision Package Service
- 127.0.0.1:9066 UI Bridge
- 127.0.0.1:9067 Decision Quality Live

Ports must be documented before adding any new service.
