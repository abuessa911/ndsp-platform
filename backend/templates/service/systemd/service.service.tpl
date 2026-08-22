[Unit]
Description=NDSP __SERVICE_ID__ __SERVICE_NAME__
After=network.target

[Service]
Type=simple
User=__USER__
WorkingDirectory=__SERVICE_PATH__
Environment=NODE_ENV=production
Environment=NDSP_PORT=__PORT__
Environment=NDSP_HOST=127.0.0.1
EnvironmentFile=-/home/__USER__/empire-core-new/backend/.env
ExecStart=/usr/bin/node __SERVICE_PATH__/main.cjs
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
