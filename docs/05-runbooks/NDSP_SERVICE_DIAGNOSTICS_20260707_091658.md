# NDSP Service Diagnostics
DATE=2026-07-07T09:16:58+02:00

## systemd ndsp-api
● ndsp-api.service - NDSP FastAPI Backend
     Loaded: loaded (/etc/systemd/system/ndsp-api.service; enabled; preset: enabled)
    Drop-In: /etc/systemd/system/ndsp-api.service.d
             └─10-admin-key.conf, 10-canonical-env.conf, 10-ndsp-db-env.conf, 20-admin-envfile.conf, 20-ndsp-admin-env.conf, 20-ndsp-mail-env.conf, 30-ndsp-official-runtime-source.conf, 30-unified-admin-key.conf, 40-database-url.conf, 50-bind-9002.conf, 98-telegram-env.conf, 99-ndsp-canonical-env.conf, 99-ndsp-correct-db.env.conf
     Active: active (running) since Tue 2026-07-07 09:16:53 CEST; 4s ago
   Main PID: 2666209 (gunicorn)
      Tasks: 1 (limit: 28792)
     Memory: 17.3M (peak: 17.5M)
        CPU: 187ms
     CGroup: /system.slice/ndsp-api.service
             └─2666209 /home/nawaf511/empire-core-new/backend/venv/bin/python /home/nawaf511/empire-core-new/backend/venv/bin/gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:9002 --workers 4 --timeout 120

يوليو 07 09:16:53 vmi2934783 gunicorn[2666209]: [2026-07-07 09:16:53 +0200] [2666209] [ERROR] connection to ('127.0.0.1', 9002) failed: [Errno 98] Address already in use
يوليو 07 09:16:54 vmi2934783 gunicorn[2666209]: [2026-07-07 09:16:54 +0200] [2666209] [ERROR] Connection in use: ('127.0.0.1', 9002)
يوليو 07 09:16:54 vmi2934783 gunicorn[2666209]: [2026-07-07 09:16:54 +0200] [2666209] [ERROR] connection to ('127.0.0.1', 9002) failed: [Errno 98] Address already in use
يوليو 07 09:16:55 vmi2934783 gunicorn[2666209]: [2026-07-07 09:16:55 +0200] [2666209] [ERROR] Connection in use: ('127.0.0.1', 9002)
يوليو 07 09:16:55 vmi2934783 gunicorn[2666209]: [2026-07-07 09:16:55 +0200] [2666209] [ERROR] connection to ('127.0.0.1', 9002) failed: [Errno 98] Address already in use
يوليو 07 09:16:56 vmi2934783 gunicorn[2666209]: [2026-07-07 09:16:56 +0200] [2666209] [ERROR] Connection in use: ('127.0.0.1', 9002)
يوليو 07 09:16:56 vmi2934783 gunicorn[2666209]: [2026-07-07 09:16:56 +0200] [2666209] [ERROR] connection to ('127.0.0.1', 9002) failed: [Errno 98] Address already in use
يوليو 07 09:16:57 vmi2934783 gunicorn[2666209]: [2026-07-07 09:16:57 +0200] [2666209] [ERROR] Connection in use: ('127.0.0.1', 9002)
يوليو 07 09:16:57 vmi2934783 gunicorn[2666209]: [2026-07-07 09:16:57 +0200] [2666209] [ERROR] connection to ('127.0.0.1', 9002) failed: [Errno 98] Address already in use
يوليو 07 09:16:58 vmi2934783 gunicorn[2666209]: [2026-07-07 09:16:58 +0200] [2666209] [ERROR] Can't connect to ('127.0.0.1', 9002)

## systemd ndip-api-new
× ndip-api-new.service - NDIP API - New Backend
     Loaded: loaded (/etc/systemd/system/ndip-api-new.service; disabled; preset: enabled)
    Drop-In: /etc/systemd/system/ndip-api-new.service.d
             └─10-mt4-dir.conf
     Active: failed (Result: exit-code) since Sun 2026-07-05 13:08:33 CEST; 1 day 20h ago
   Duration: 280ms
   Main PID: 496467 (code=exited, status=1/FAILURE)
        CPU: 269ms

## PM2 list
┌────┬─────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name            │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼─────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ 1  │ ndsp-backend    │ default     │ N/A     │ fork    │ 2666668  │ 0s     │ 372… │ online    │ 0%       │ 80.7mb   │ nawaf511 │ disabled │
│ 0  │ ndsp-portal     │ default     │ 0.39.7  │ fork    │ 1099070  │ 42h    │ 0    │ online    │ 0%       │ 79.1mb   │ nawaf511 │ disabled │
└────┴─────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
host metrics | cpu: 22.9% | ram usage: 9.4% | lo: ⇓ 0.004mb/s ⇑ 0.004mb/s | eth0: ⇓ 0.012mb/s ⇑ 0.001mb/s | disk: ⇓ 0mb/s ⇑ 0.199mb/s / 81.33% |

## PM2 describe ndsp-backend
 Describing process with id 1 - name ndsp-backend 
┌───────────────────┬─────────────────────────────────────────────────┐
│ status            │ online                                          │
│ name              │ ndsp-backend                                    │
│ namespace         │ default                                         │
│ version           │ N/A                                             │
│ restarts          │ 372173                                          │
│ uptime            │ 0s                                              │
│ script path       │ /usr/bin/npm                                    │
│ script args       │ run start                                       │
│ error log path    │ /home/nawaf511/.pm2/logs/ndsp-backend-error.log │
│ out log path      │ /home/nawaf511/.pm2/logs/ndsp-backend-out.log   │
│ pid path          │ /home/nawaf511/.pm2/pids/ndsp-backend-1.pid     │
│ interpreter       │ /usr/bin/node                                   │
│ interpreter args  │ N/A                                             │
│ script id         │ 1                                               │
│ exec cwd          │ /home/nawaf511/empire-core-new/backend          │
│ exec mode         │ fork_mode                                       │
│ node.js version   │ 22.22.2                                         │
│ node env          │ N/A                                             │
│ watch & reload    │ ✘                                               │
│ unstable restarts │ 0                                               │
│ created at        │ 2026-05-22T19:24:49.009Z                        │
└───────────────────┴─────────────────────────────────────────────────┘
 Actions available 
┌────────────────────────┐
│ km:heapdump            │
│ km:cpu:profiling:start │
│ km:cpu:profiling:stop  │
│ km:heap:sampling:start │
│ km:heap:sampling:stop  │
└────────────────────────┘
 Trigger via: pm2 trigger ndsp-backend <action_name>

 Divergent env variables from local env 
┌────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PWD            │ /home/nawaf511/empire-core-new/backend                                                                                                                                                                                                           │
│ SSH_CONNECTION │ 109.83.85.169 37202 161.97.144.189 22                                                                                                                                                                                                            │
│ XDG_SESSION_ID │ 4220                                                                                                                                                                                                                                             │
│ SSH_CLIENT     │ 109.83.85.169 37202 22                                                                                                                                                                                                                           │
│ PATH           │ /home/nawaf511/.npm/_npx/5f7878ce38f1eb13/node_modules/.bin:/home/nawaf511/empire-core-new/backend/node_modules/.bin:/home/nawaf511/empire-core-new/node_modules/.bin:/home/nawaf511/node_modules/.bin:/home/node_modules/.bin:/node_modules/.bi │
│ SSH_TTY        │ /dev/pts/2                                                                                                                                                                                                                                       │
│ OLDPWD         │ /home/nawaf511                                                                                                                                                                                                                                   │
│ _              │ /usr/bin/npx                                                                                                                                                                                                                                     │
└────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

 Add your own code metrics: http://bit.ly/code-metrics
 Use `pm2 logs ndsp-backend [--lines 1000]` to display logs
 Use `pm2 env 1` to display environment variables
 Use `pm2 monit` to monitor CPU and Memory usage ndsp-backend

## PM2 backend logs
[TAILING] Tailing last 80 lines for [ndsp-backend] process (change the value with --lines option)
/home/nawaf511/.pm2/logs/ndsp-backend-out.log last 80 lines:
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 
1|ndsp-bac | 
1|ndsp-bac | > ndsp-auth-api@1.0.0 start
1|ndsp-bac | > node server.js
1|ndsp-bac | 

/home/nawaf511/.pm2/logs/ndsp-backend-error.log last 80 lines:
1|ndsp-bac |     at defaultResolveImpl (node:internal/modules/cjs/loader:1042:19)
1|ndsp-bac |     at resolveForCJSWithHooks (node:internal/modules/cjs/loader:1047:22)
1|ndsp-bac |     at Function._load (node:internal/modules/cjs/loader:1209:37)
1|ndsp-bac |     at TracingChannel.traceSync (node:diagnostics_channel:328:14)
1|ndsp-bac |     at wrapModuleLoad (node:internal/modules/cjs/loader:239:24)
1|ndsp-bac |     at Module.require (node:internal/modules/cjs/loader:1480:12)
1|ndsp-bac |     at require (node:internal/modules/helpers:147:16)
1|ndsp-bac |     at Object.<anonymous> (/home/nawaf511/empire-core-new/backend/server.js:19:49)
1|ndsp-bac |     at Module._compile (node:internal/modules/cjs/loader:1722:14) {
1|ndsp-bac |   code: 'MODULE_NOT_FOUND',
1|ndsp-bac |   requireStack: [ '/home/nawaf511/empire-core-new/backend/server.js' ]
1|ndsp-bac | }
1|ndsp-bac | 
1|ndsp-bac | Node.js v22.22.2
1|ndsp-bac | node:internal/modules/cjs/loader:1403
1|ndsp-bac |   throw err;
1|ndsp-bac |   ^
1|ndsp-bac | 
1|ndsp-bac | Error: Cannot find module 'otplib'
1|ndsp-bac | Require stack:
1|ndsp-bac | - /home/nawaf511/empire-core-new/backend/server.js
1|ndsp-bac |     at Function._resolveFilename (node:internal/modules/cjs/loader:1400:15)
1|ndsp-bac |     at defaultResolveImpl (node:internal/modules/cjs/loader:1042:19)
1|ndsp-bac |     at resolveForCJSWithHooks (node:internal/modules/cjs/loader:1047:22)
1|ndsp-bac |     at Function._load (node:internal/modules/cjs/loader:1209:37)
1|ndsp-bac |     at TracingChannel.traceSync (node:diagnostics_channel:328:14)
1|ndsp-bac |     at wrapModuleLoad (node:internal/modules/cjs/loader:239:24)
1|ndsp-bac |     at Module.require (node:internal/modules/cjs/loader:1480:12)
1|ndsp-bac |     at require (node:internal/modules/helpers:147:16)
1|ndsp-bac |     at Object.<anonymous> (/home/nawaf511/empire-core-new/backend/server.js:19:49)
1|ndsp-bac |     at Module._compile (node:internal/modules/cjs/loader:1722:14) {
1|ndsp-bac |   code: 'MODULE_NOT_FOUND',
1|ndsp-bac |   requireStack: [ '/home/nawaf511/empire-core-new/backend/server.js' ]
1|ndsp-bac | }
1|ndsp-bac | 
1|ndsp-bac | Node.js v22.22.2
1|ndsp-bac | node:internal/modules/cjs/loader:1403
1|ndsp-bac |   throw err;
1|ndsp-bac |   ^
1|ndsp-bac | 
1|ndsp-bac | Error: Cannot find module 'otplib'
1|ndsp-bac | Require stack:
1|ndsp-bac | - /home/nawaf511/empire-core-new/backend/server.js
1|ndsp-bac |     at Function._resolveFilename (node:internal/modules/cjs/loader:1400:15)
1|ndsp-bac |     at defaultResolveImpl (node:internal/modules/cjs/loader:1042:19)
1|ndsp-bac |     at resolveForCJSWithHooks (node:internal/modules/cjs/loader:1047:22)
1|ndsp-bac |     at Function._load (node:internal/modules/cjs/loader:1209:37)
1|ndsp-bac |     at TracingChannel.traceSync (node:diagnostics_channel:328:14)
1|ndsp-bac |     at wrapModuleLoad (node:internal/modules/cjs/loader:239:24)
1|ndsp-bac |     at Module.require (node:internal/modules/cjs/loader:1480:12)
1|ndsp-bac |     at require (node:internal/modules/helpers:147:16)
1|ndsp-bac |     at Object.<anonymous> (/home/nawaf511/empire-core-new/backend/server.js:19:49)
1|ndsp-bac |     at Module._compile (node:internal/modules/cjs/loader:1722:14) {
1|ndsp-bac |   code: 'MODULE_NOT_FOUND',
1|ndsp-bac |   requireStack: [ '/home/nawaf511/empire-core-new/backend/server.js' ]
1|ndsp-bac | }
1|ndsp-bac | 
1|ndsp-bac | Node.js v22.22.2
1|ndsp-bac | node:internal/modules/cjs/loader:1403
1|ndsp-bac |   throw err;
1|ndsp-bac |   ^
1|ndsp-bac | 
1|ndsp-bac | Error: Cannot find module 'otplib'
1|ndsp-bac | Require stack:
1|ndsp-bac | - /home/nawaf511/empire-core-new/backend/server.js
1|ndsp-bac |     at Function._resolveFilename (node:internal/modules/cjs/loader:1400:15)
1|ndsp-bac |     at defaultResolveImpl (node:internal/modules/cjs/loader:1042:19)
1|ndsp-bac |     at resolveForCJSWithHooks (node:internal/modules/cjs/loader:1047:22)
1|ndsp-bac |     at Function._load (node:internal/modules/cjs/loader:1209:37)
1|ndsp-bac |     at TracingChannel.traceSync (node:diagnostics_channel:328:14)
1|ndsp-bac |     at wrapModuleLoad (node:internal/modules/cjs/loader:239:24)
1|ndsp-bac |     at Module.require (node:internal/modules/cjs/loader:1480:12)
1|ndsp-bac |     at require (node:internal/modules/helpers:147:16)
1|ndsp-bac |     at Object.<anonymous> (/home/nawaf511/empire-core-new/backend/server.js:19:49)
1|ndsp-bac |     at Module._compile (node:internal/modules/cjs/loader:1722:14) {
1|ndsp-bac |   code: 'MODULE_NOT_FOUND',
1|ndsp-bac |   requireStack: [ '/home/nawaf511/empire-core-new/backend/server.js' ]
1|ndsp-bac | }
1|ndsp-bac | 
1|ndsp-bac | Node.js v22.22.2


## Nginx syntax
