# NDSP P2 Monitoring & Startup Safety Audit Read-only
DATE=2026-07-08T00:52:54+02:00
MODE=READ_ONLY_MONITORING_STARTUP_SAFETY
MODIFICATIONS=None

## 1) Host Snapshot
 Static hostname: vmi2934783
       Icon name: computer-vm
         Chassis: vm 🖴
      Machine ID: 6f6a9637030949db96865b94f221ba1d
         Boot ID: 30171be6091c48feadc15fe5b126358c
  Virtualization: kvm
Operating System: Ubuntu 24.04.4 LTS
          Kernel: Linux 6.8.0-134-generic
    Architecture: x86-64
 Hardware Vendor: QEMU
  Hardware Model: Standard PC _i440FX + PIIX, 1996_
Firmware Version: rel-1.16.3-0-ga6ed6b701f0a-prebuilt.qemu.org
   Firmware Date: Tue 2014-04-01
    Firmware Age: 12y 3month 6d
 00:52:54 up 2 days, 12:53,  3 users,  load average: 1.79, 1.08, 0.93
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       387G  317G   70G  82% /
               total        used        free      shared  buff/cache   available
Mem:            23Gi       2.3Gi        19Gi        29Mi       1.8Gi        21Gi
Swap:          2.0Gi          0B       2.0Gi

## 2) Core systemd Services Status

### SERVICE=nginx
ACTIVE=active
ENABLED=enabled
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; preset: enabled)
     Active: active (running) since Sun 2026-07-05 12:00:09 CEST; 2 days ago
       Docs: man:nginx(8)
   Main PID: 1564 (nginx)
      Tasks: 9 (limit: 28792)
     Memory: 30.3M (peak: 48.9M)
        CPU: 3min 21.295s
     CGroup: /system.slice/nginx.service
             ├─   1564 "nginx: master process /usr/sbin/nginx -g daemon on; master_process on;"
             ├─3953328 "nginx: worker process"
             ├─3953329 "nginx: worker process"
             ├─3953330 "nginx: worker process"
             ├─3953331 "nginx: worker process"
             ├─3953332 "nginx: worker process"
             ├─3953333 "nginx: worker process"
             ├─3953334 "nginx: worker process"
             └─3953335 "nginx: worker process"

Warning: some journal files were not opened due to insufficient permissions.

### SERVICE=ndsp-quality-live-nmp-wrapper.service
ACTIVE=active
ENABLED=enabled
● ndsp-quality-live-nmp-wrapper.service - NDSP quality-live NMP wrapper 9082
     Loaded: loaded (/etc/systemd/system/ndsp-quality-live-nmp-wrapper.service; enabled; preset: enabled)
     Active: active (running) since Wed 2026-07-08 00:32:03 CEST; 20min ago
   Main PID: 2165089 (python3)
      Tasks: 1 (limit: 28792)
     Memory: 12.1M (peak: 12.9M)
        CPU: 2.462s
     CGroup: /system.slice/ndsp-quality-live-nmp-wrapper.service
             └─2165089 /usr/bin/python3 /home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_nmp_wrapper.py

### SERVICE=ndsp-quality-live-golden-wrapper.service
ACTIVE=active
ENABLED=enabled
● ndsp-quality-live-golden-wrapper.service - NDSP quality-live golden explainability API wrapper
     Loaded: loaded (/etc/systemd/system/ndsp-quality-live-golden-wrapper.service; enabled; preset: enabled)
     Active: active (running) since Sun 2026-07-05 12:00:07 CEST; 2 days ago
   Main PID: 1348 (python3)
      Tasks: 1 (limit: 28792)
     Memory: 13.8M (peak: 14.8M)
        CPU: 3min 54.298s
     CGroup: /system.slice/ndsp-quality-live-golden-wrapper.service
             └─1348 /usr/bin/python3 /home/nawaf511/empire-core-new/backend/app/runtime/ndsp_quality_live_golden_wrapper.py

Warning: some journal files were not opened due to insufficient permissions.

### SERVICE=ndsp-live-decision-quality.service
ACTIVE=active
ENABLED=enabled
● ndsp-live-decision-quality.service - NDSP Live Decision Quality Bridge
     Loaded: loaded (/etc/systemd/system/ndsp-live-decision-quality.service; enabled; preset: enabled)
     Active: active (running) since Sun 2026-07-05 12:00:08 CEST; 2 days ago
   Main PID: 1387 (python3)
      Tasks: 7 (limit: 28792)
     Memory: 43.7M (peak: 53.1M)
        CPU: 48min 47.980s
     CGroup: /system.slice/ndsp-live-decision-quality.service
             └─1387 /usr/bin/python3 /home/nawaf511/empire-core-new/backend/ndsp-live-decision-quality/server.py

Warning: some journal files were not opened due to insufficient permissions.

### SERVICE=ndsp-scenario-levels-adapter.service
ACTIVE=active
ENABLED=enabled
● ndsp-scenario-levels-adapter.service - NDSP Scenario Levels Adapter
     Loaded: loaded (/etc/systemd/system/ndsp-scenario-levels-adapter.service; enabled; preset: enabled)
     Active: active (running) since Sun 2026-07-05 12:00:08 CEST; 2 days ago
   Main PID: 1400 (node)
      Tasks: 8 (limit: 28792)
     Memory: 18.2M (peak: 22.8M)
        CPU: 4min 783ms
     CGroup: /system.slice/ndsp-scenario-levels-adapter.service
             └─1400 /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp_scenario_levels_adapter.cjs

يوليو 05 12:00:10 vmi2934783 node[1400]: [NDSP] scenario levels adapter listening on 127.0.0.1:9034
Warning: journal has been rotated since unit was started and some journal files were not opened due to insufficient permissions, output may be incomplete.

## 3) Failed systemd Units
  UNIT                              LOAD   ACTIVE SUB    DESCRIPTION
● certbot.service                   loaded failed failed Certbot
● fanno-comments.service            loaded failed failed Fanno Comment Service
● logrotate.service                 loaded failed failed Rotate log files
● marketpulse.service               loaded failed failed MarketPulse Backend Service
● ndip-api-new.service              loaded failed failed NDIP API - New Backend
● ndsp-real-feeds-sync.service      loaded failed failed NDSP Real Feeds Sync
● ndsp-tradingview-calendar.service loaded failed failed NDSP TradingView Live Economic Calendar
● redis-replica.service             loaded failed failed Redis Replica
● redis-sentinel.service            loaded failed failed Redis Sentinel
● signal-engine.service             loaded failed failed Empire Core Signal Engine
● subscription-watcher.service      loaded failed failed Subscription Expiry Watcher
● testapp.service                   loaded failed failed testapp Service

Legend: LOAD   → Reflects whether the unit definition was properly loaded.
        ACTIVE → The high-level unit activation state, i.e. generalization of SUB.
        SUB    → The low-level unit activation state, values depend on unit type.

12 loaded units listed.

## 4) PM2 Startup Safety as nawaf511
PM2_HOME=/home/nawaf511/.pm2
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m10.6%[39m | [1mram usage[22m: [32m9.8%[39m | [1mlo[22m: ⇓ [32m0.014mb/s[39m ⇑ [32m0.014mb/s[39m | [1meth0[22m: ⇓ [32m0.114mb/s[39m ⇑ [32m0.006mb/s[39m | [1mdisk[22m: ⇓ [32m1.098mb/s[39m ⇑ [32m0.195mb/s[39m [90m/[39m [1m[33m81.98%[39m[22m |

### PM2 saved dump
PM2_DUMP_EXISTS=1
PM2_DUMP_SIZE=11196 PM2_DUMP_UPDATED=2026-07-07 09:26:49.733544741 +0200 PATH=/home/nawaf511/.pm2/dump.pm2

### PM2 startup service candidates
pm2-nawaf511.service                                                          enabled         enabled
systemd-tpm2-setup-early.service                                              static          -
systemd-tpm2-setup.service                                                    static          -
  pm2-nawaf511.service                                loaded    inactive   dead               PM2 process manager
  systemd-pcrmachine.service                          loaded    inactive   dead               TPM2 PCR Machine ID Measurement
  systemd-pcrphase-initrd.service                     loaded    inactive   dead               TPM2 PCR Barrier (initrd)
  systemd-pcrphase-sysinit.service                    loaded    inactive   dead               TPM2 PCR Barrier (Initialization)
  systemd-pcrphase.service                            loaded    inactive   dead               TPM2 PCR Barrier (User)
  systemd-tpm2-setup-early.service                    loaded    inactive   dead               TPM2 SRK Setup (Early)
  systemd-tpm2-setup.service                          loaded    inactive   dead               TPM2 SRK Setup

## 5) Nginx Config and Routes
2026/07/08 00:52:59 [warn] 2252070#2252070: the "user" directive makes sense only if the master process runs with super-user privileges, ignored in /etc/nginx/nginx.conf:1
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
2026/07/08 00:52:59 [emerg] 2252070#2252070: open() "/run/nginx.pid" failed (13: Permission denied)
nginx: configuration file /etc/nginx/nginx.conf test failed
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:28:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:85:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042.bak_pkg_v2_route_20260625_100732:129:    location = /api/decision/quality-live {
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:43:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:100:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_package_live_20260625_094042:144:    location = /api/decision/quality-live {
/etc/nginx/conf.d/050-ndsp-completed-governance-public-api.conf.disabled_20260627_215043:7:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:43:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:100:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_fix_completed_routes_20260627_215130:144:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:28:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:85:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_pkg_v2_route_20260625_100732:129:    location = /api/decision/quality-live {
/etc/nginx/conf.d/777-ndsp-ui-bridge-api.conf.disabled_20260622_142426.disabled_20260625_090629.bak_package_route_20260625_094003:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:5:    server_name my.ndsp.app;
/etc/nginx/conf.d/000-my.ndsp.app-final.conf:64:    server_name my.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:43:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:100:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_completed_routes_20260627_215043:144:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:9:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:51:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:52:        proxy_pass http://127.0.0.1:9082/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:140:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:186:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf:187:        proxy_pass http://127.0.0.1:9082/api/decision/quality-live$is_args$args;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:43:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:100:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624:144:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:28:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:85:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.disabled_20260625_090629:129:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:4:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:28:    location = /api/decision/quality-live {
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:85:    server_name api.ndsp.app;
/etc/nginx/conf.d/000-api-ndsp-app-canonical.conf.bak_v2_governance_20260625_100624.bak_pkg_v2_route_20260625_100732:129:    location = /api/decision/quality-live {

## 6) Public HTTP Checks
https://my.ndsp.app/index.html HTTP_CODE=200 BYTES=913
https://my.ndsp.app/decision-support.html HTTP_CODE=200 BYTES=6933
https://my.ndsp.app/NDSP_Asset_View.html HTTP_CODE=200 BYTES=7179
https://my.ndsp.app/disclaimer.html HTTP_CODE=200 BYTES=4677
https://api.ndsp.app/api/health HTTP_CODE=200 BYTES=183
https://api.ndsp.app/api/decision/quality-live?symbol=ETHUSDT HTTP_CODE=200 BYTES=8478

## 7) V1.2 API Contract Quick Check
ETHUSDT: V12_SCENARIO_LEVELS=OK
BTCUSDT: V12_SCENARIO_LEVELS=OK
XAUUSD: V12_SCENARIO_LEVELS=OK
USOIL: V12_SCENARIO_LEVELS=OK
V12_API_CONTRACT_STATUS=OK

## 8) Certificate Snapshot

## 9) Release Package Presence
-rw-rw-r-- 1 nawaf511 nawaf511 22K يوليو   8 00:44 /home/nawaf511/ndsp_release_packages/NDSP_V12_RELEASE_PACKAGE_20260708_004432.tar.gz
-rw-rw-r-- 1 nawaf511 nawaf511 151 يوليو   8 00:44 /home/nawaf511/ndsp_release_packages/NDSP_V12_RELEASE_PACKAGE_20260708_004432.tar.gz.sha256
bb84349c8fa0c5c43c7345aa1608a1167cb48aeddb0abbd14fef5535b43e5eb3  /home/nawaf511/ndsp_release_packages/NDSP_V12_RELEASE_PACKAGE_20260708_004432.tar.gz

## 10) Final Evaluation
FINAL_STATUS=P2_MONITORING_STARTUP_SAFETY_AUDIT_READONLY_DONE
REPORT=docs/05-runbooks/NDSP_P2_MONITORING_STARTUP_SAFETY_AUDIT_READONLY_20260708_005254.md
