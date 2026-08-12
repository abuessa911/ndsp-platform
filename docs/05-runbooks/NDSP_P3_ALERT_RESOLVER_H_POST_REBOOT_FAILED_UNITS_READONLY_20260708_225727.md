# NDSP P3 Alert Resolver H — Post-Reboot Failed Unit Diagnostics
DATE=2026-07-08T22:57:27+02:00
MODE=READ_ONLY_POST_REBOOT_FAILED_UNIT_DIAGNOSTICS
TARGETS=ndsp-market-prices-updater.service,ndip-api-new.service
MODIFICATIONS=None
NO_START=1
NO_STOP=1
NO_RESTART=1
NO_ENABLE=1
NO_DISABLE=1
NO_MASK=1
NO_DELETE=1
NO_REBOOT=1
NO_RESET_FAILED=1
NO_NGINX_CHANGE=1
NO_FRONTEND_CHANGE=1
NO_API_CHANGE=1
ARTIFACT_DIR=/tmp/NDSP_P3_ALERT_RESOLVER_H_20260708_225727

## 1) Stabilization wait after reboot
up 7 minutes
         system boot  2026-07-08 22:50
WAIT_SECONDS=45

## 2) Core runtime still safe
nginx=active
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
pm2-nawaf511=active
pm2-nawaf511-enabled=enabled
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 3351     │ 7m     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 73.3mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m12.1%[39m | [1mram usage[22m: [32m7.4%[39m | [1mlo[22m: ⇓ [32m0.011mb/s[39m ⇑ [32m0.011mb/s[39m | [1meth0[22m: ⇓ [32m0.099mb/s[39m ⇑ [32m0.005mb/s[39m | [1mdisk[22m: ⇓ [32m0.003mb/s[39m ⇑ [32m0.199mb/s[39m [90m/[39m [1m[33m82.05%[39m[22m |
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200
MY_NDSP_HTTP=200
ADMIN_NDSP_HTTP=200

## 3) Failed units after wait
  UNIT LOAD ACTIVE SUB DESCRIPTION

0 loaded units listed.
FAILED_UNITS_COUNT_AFTER_WAIT=0

## 4) Deep diagnostics per target

---- SERVICE=ndsp-market-prices-updater.service ----
ENABLED=static
ACTIVE=inactive
FAILED=inactive
UNIT_FILE_STATE=static
LOAD_STATE=loaded
SUB_STATE=dead
RESULT=success
EXEC_MAIN_STATUS=0
MAIN_PID=0
N_RESTARTS=0
FRAGMENT=/etc/systemd/system/ndsp-market-prices-updater.service

### UNIT_FILE
# /etc/systemd/system/ndsp-market-prices-updater.service
[Unit]
Description=NDSP Live Market Prices Updater

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /usr/local/bin/ndsp_live_market_prices_updater.py
User=root
Group=root

# /etc/systemd/system/ndsp-market-prices-updater.service.d/30-ndsp-official-runtime-source.conf
[Service]
EnvironmentFile=/etc/ndsp/ndsp-db.env
EnvironmentFile=/etc/ndsp/ndsp-mail.env
Environment=NDSP_ADMIN_USERS_JSON=/home/nawaf511/empire-core-new/runtime/admin-users.json

### SHOW_KEY_FIELDS
Restart=no
Result=success
NRestarts=0
ExecMainStatus=0
ExecStart={ path=/usr/bin/python3 ; argv[]=/usr/bin/python3 /usr/local/bin/ndsp_live_market_prices_updater.py ; ignore_errors=no ; start_time=[Wed 2026-07-08 22:57:37 CEST] ; stop_time=[Wed 2026-07-08 22:57:39 CEST] ; pid=34726 ; code=exited ; status=0 }
User=root
Group=root
Id=ndsp-market-prices-updater.service
Requires=system.slice sysinit.target
Before=shutdown.target
After=basic.target sysinit.target system.slice ndsp-market-prices-updater.timer systemd-journald.socket
TriggeredBy=ndsp-market-prices-updater.timer
Description=NDSP Live Market Prices Updater
LoadState=loaded
ActiveState=inactive
SubState=dead
FragmentPath=/etc/systemd/system/ndsp-market-prices-updater.service
UnitFileState=static

### JOURNAL_CURRENT_BOOT
يوليو 08 22:50:34 vmi2934783 systemd[1]: Starting ndsp-market-prices-updater.service - NDSP Live Market Prices Updater...
يوليو 08 22:50:35 vmi2934783 sudo[1347]:     root : PWD=/ ; USER=postgres ; COMMAND=/usr/bin/psql -d ndsp_auth -AtF #011 -c '#012SELECT symbol,name_ar,name_en,category,source#012FROM ndsp_assets#012WHERE is_active=true#012ORDER BY category,symbol;#012'
يوليو 08 22:50:35 vmi2934783 sudo[1347]: pam_unix(sudo:session): session opened for user postgres(uid=109) by (uid=0)
يوليو 08 22:50:35 vmi2934783 sudo[1347]: pam_unix(sudo:session): session closed for user postgres
يوليو 08 22:50:36 vmi2934783 python3[1317]: Traceback (most recent call last):
يوليو 08 22:50:36 vmi2934783 python3[1317]:   File "/usr/local/bin/ndsp_live_market_prices_updater.py", line 262, in <module>
يوليو 08 22:50:36 vmi2934783 python3[1317]:     main()
يوليو 08 22:50:36 vmi2934783 python3[1317]:   File "/usr/local/bin/ndsp_live_market_prices_updater.py", line 180, in main
يوليو 08 22:50:36 vmi2934783 python3[1317]:     assets = get_assets()
يوليو 08 22:50:36 vmi2934783 python3[1317]:              ^^^^^^^^^^^^
يوليو 08 22:50:36 vmi2934783 python3[1317]:   File "/usr/local/bin/ndsp_live_market_prices_updater.py", line 86, in get_assets
يوليو 08 22:50:36 vmi2934783 python3[1317]:     out = subprocess.check_output(
يوليو 08 22:50:36 vmi2934783 python3[1317]:           ^^^^^^^^^^^^^^^^^^^^^^^^
يوليو 08 22:50:36 vmi2934783 python3[1317]:   File "/usr/lib/python3.12/subprocess.py", line 466, in check_output
يوليو 08 22:50:36 vmi2934783 python3[1317]:     return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
يوليو 08 22:50:36 vmi2934783 python3[1317]:            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
يوليو 08 22:50:36 vmi2934783 python3[1317]:   File "/usr/lib/python3.12/subprocess.py", line 571, in run
يوليو 08 22:50:36 vmi2934783 python3[1317]:     raise CalledProcessError(retcode, process.args,
يوليو 08 22:50:36 vmi2934783 python3[1317]: subprocess.CalledProcessError: Command '['sudo', '-u', 'postgres', 'psql', '-d', 'ndsp_auth', '-AtF', '\t', '-c', '\nSELECT symbol,name_ar,name_en,category,source\nFROM ndsp_assets\nWHERE is_active=true\nORDER BY category,symbol;\n']' returned non-zero exit status 2.
يوليو 08 22:50:36 vmi2934783 systemd[1]: ndsp-market-prices-updater.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:50:36 vmi2934783 systemd[1]: ndsp-market-prices-updater.service: Failed with result 'exit-code'.
يوليو 08 22:50:36 vmi2934783 systemd[1]: Failed to start ndsp-market-prices-updater.service - NDSP Live Market Prices Updater.
يوليو 08 22:51:35 vmi2934783 systemd[1]: Starting ndsp-market-prices-updater.service - NDSP Live Market Prices Updater...
يوليو 08 22:51:35 vmi2934783 sudo[8973]:     root : PWD=/ ; USER=postgres ; COMMAND=/usr/bin/psql -d ndsp_auth -AtF #011 -c '#012SELECT symbol,name_ar,name_en,category,source#012FROM ndsp_assets#012WHERE is_active=true#012ORDER BY category,symbol;#012'
يوليو 08 22:51:35 vmi2934783 sudo[8973]: pam_unix(sudo:session): session opened for user postgres(uid=109) by (uid=0)
يوليو 08 22:51:35 vmi2934783 sudo[8973]: pam_unix(sudo:session): session closed for user postgres
يوليو 08 22:51:37 vmi2934783 systemd[1]: ndsp-market-prices-updater.service: Deactivated successfully.
يوليو 08 22:51:37 vmi2934783 systemd[1]: Finished ndsp-market-prices-updater.service - NDSP Live Market Prices Updater.
يوليو 08 22:52:35 vmi2934783 systemd[1]: Starting ndsp-market-prices-updater.service - NDSP Live Market Prices Updater...
يوليو 08 22:52:35 vmi2934783 sudo[13313]:     root : PWD=/ ; USER=postgres ; COMMAND=/usr/bin/psql -d ndsp_auth -AtF #011 -c '#012SELECT symbol,name_ar,name_en,category,source#012FROM ndsp_assets#012WHERE is_active=true#012ORDER BY category,symbol;#012'
يوليو 08 22:52:35 vmi2934783 sudo[13313]: pam_unix(sudo:session): session opened for user postgres(uid=109) by (uid=0)
يوليو 08 22:52:35 vmi2934783 sudo[13313]: pam_unix(sudo:session): session closed for user postgres
يوليو 08 22:52:37 vmi2934783 systemd[1]: ndsp-market-prices-updater.service: Deactivated successfully.
يوليو 08 22:52:37 vmi2934783 systemd[1]: Finished ndsp-market-prices-updater.service - NDSP Live Market Prices Updater.
يوليو 08 22:53:36 vmi2934783 systemd[1]: Starting ndsp-market-prices-updater.service - NDSP Live Market Prices Updater...
يوليو 08 22:53:36 vmi2934783 sudo[17605]:     root : PWD=/ ; USER=postgres ; COMMAND=/usr/bin/psql -d ndsp_auth -AtF #011 -c '#012SELECT symbol,name_ar,name_en,category,source#012FROM ndsp_assets#012WHERE is_active=true#012ORDER BY category,symbol;#012'
يوليو 08 22:53:36 vmi2934783 sudo[17605]: pam_unix(sudo:session): session opened for user postgres(uid=109) by (uid=0)
يوليو 08 22:53:36 vmi2934783 sudo[17605]: pam_unix(sudo:session): session closed for user postgres
يوليو 08 22:53:38 vmi2934783 systemd[1]: ndsp-market-prices-updater.service: Deactivated successfully.
يوليو 08 22:53:38 vmi2934783 systemd[1]: Finished ndsp-market-prices-updater.service - NDSP Live Market Prices Updater.
يوليو 08 22:54:36 vmi2934783 systemd[1]: Starting ndsp-market-prices-updater.service - NDSP Live Market Prices Updater...
يوليو 08 22:54:36 vmi2934783 sudo[21945]:     root : PWD=/ ; USER=postgres ; COMMAND=/usr/bin/psql -d ndsp_auth -AtF #011 -c '#012SELECT symbol,name_ar,name_en,category,source#012FROM ndsp_assets#012WHERE is_active=true#012ORDER BY category,symbol;#012'
يوليو 08 22:54:36 vmi2934783 sudo[21945]: pam_unix(sudo:session): session opened for user postgres(uid=109) by (uid=0)
يوليو 08 22:54:36 vmi2934783 sudo[21945]: pam_unix(sudo:session): session closed for user postgres
يوليو 08 22:54:38 vmi2934783 systemd[1]: ndsp-market-prices-updater.service: Deactivated successfully.
يوليو 08 22:54:38 vmi2934783 systemd[1]: Finished ndsp-market-prices-updater.service - NDSP Live Market Prices Updater.
يوليو 08 22:55:36 vmi2934783 systemd[1]: Starting ndsp-market-prices-updater.service - NDSP Live Market Prices Updater...
يوليو 08 22:55:36 vmi2934783 sudo[26282]:     root : PWD=/ ; USER=postgres ; COMMAND=/usr/bin/psql -d ndsp_auth -AtF #011 -c '#012SELECT symbol,name_ar,name_en,category,source#012FROM ndsp_assets#012WHERE is_active=true#012ORDER BY category,symbol;#012'
يوليو 08 22:55:36 vmi2934783 sudo[26282]: pam_unix(sudo:session): session opened for user postgres(uid=109) by (uid=0)
يوليو 08 22:55:36 vmi2934783 sudo[26282]: pam_unix(sudo:session): session closed for user postgres
يوليو 08 22:55:39 vmi2934783 systemd[1]: ndsp-market-prices-updater.service: Deactivated successfully.
يوليو 08 22:55:39 vmi2934783 systemd[1]: Finished ndsp-market-prices-updater.service - NDSP Live Market Prices Updater.
يوليو 08 22:56:36 vmi2934783 systemd[1]: Starting ndsp-market-prices-updater.service - NDSP Live Market Prices Updater...
يوليو 08 22:56:36 vmi2934783 sudo[29629]:     root : PWD=/ ; USER=postgres ; COMMAND=/usr/bin/psql -d ndsp_auth -AtF #011 -c '#012SELECT symbol,name_ar,name_en,category,source#012FROM ndsp_assets#012WHERE is_active=true#012ORDER BY category,symbol;#012'
يوليو 08 22:56:36 vmi2934783 sudo[29629]: pam_unix(sudo:session): session opened for user postgres(uid=109) by (uid=0)
يوليو 08 22:56:37 vmi2934783 sudo[29629]: pam_unix(sudo:session): session closed for user postgres
يوليو 08 22:56:38 vmi2934783 systemd[1]: ndsp-market-prices-updater.service: Deactivated successfully.
يوليو 08 22:56:38 vmi2934783 systemd[1]: Finished ndsp-market-prices-updater.service - NDSP Live Market Prices Updater.
يوليو 08 22:57:37 vmi2934783 systemd[1]: Starting ndsp-market-prices-updater.service - NDSP Live Market Prices Updater...
يوليو 08 22:57:37 vmi2934783 sudo[34731]:     root : PWD=/ ; USER=postgres ; COMMAND=/usr/bin/psql -d ndsp_auth -AtF #011 -c '#012SELECT symbol,name_ar,name_en,category,source#012FROM ndsp_assets#012WHERE is_active=true#012ORDER BY category,symbol;#012'
يوليو 08 22:57:37 vmi2934783 sudo[34731]: pam_unix(sudo:session): session opened for user postgres(uid=109) by (uid=0)
يوليو 08 22:57:37 vmi2934783 sudo[34731]: pam_unix(sudo:session): session closed for user postgres
يوليو 08 22:57:39 vmi2934783 systemd[1]: ndsp-market-prices-updater.service: Deactivated successfully.
يوليو 08 22:57:39 vmi2934783 systemd[1]: Finished ndsp-market-prices-updater.service - NDSP Live Market Prices Updater.

### TIMERS_AND_DEPENDENCIES
Wed 2026-07-08 22:58:37 CEST      20s Wed 2026-07-08 22:57:37 CEST      39s ago ndsp-market-prices-updater.timer            ndsp-market-prices-updater.service
ndsp-market-prices-updater.service
ndsp-market-prices-updater.service
● ├─system.slice
● └─sysinit.target
●   ├─apparmor.service
●   ├─blk-availability.service
●   ├─dev-hugepages.mount
●   ├─dev-mqueue.mount
●   ├─finalrd.service
●   ├─keyboard-setup.service
●   ├─kmod-static-nodes.service
○   ├─ldconfig.service
●   ├─lvm2-lvmpolld.socket
●   ├─lvm2-monitor.service
○   ├─open-iscsi.service
●   ├─plymouth-read-write.service
○   ├─plymouth-start.service
●   ├─proc-sys-fs-binfmt_misc.automount
●   ├─setvtrgb.service
●   ├─sys-fs-fuse-connections.mount
●   ├─sys-kernel-config.mount
●   ├─sys-kernel-debug.mount
●   ├─sys-kernel-tracing.mount
●   ├─systemd-ask-password-console.path
●   ├─systemd-binfmt.service
○   ├─systemd-firstboot.service
○   ├─systemd-hwdb-update.service
○   ├─systemd-journal-catalog-update.service
●   ├─systemd-journal-flush.service
●   ├─systemd-journald.service
○   ├─systemd-machine-id-commit.service
●   ├─systemd-modules-load.service
○   ├─systemd-pcrmachine.service
○   ├─systemd-pcrphase-sysinit.service
○   ├─systemd-pcrphase.service
○   ├─systemd-pstore.service
●   ├─systemd-random-seed.service
○   ├─systemd-repart.service
●   ├─systemd-resolved.service
●   ├─systemd-sysctl.service
○   ├─systemd-sysusers.service
●   ├─systemd-timesyncd.service
●   ├─systemd-tmpfiles-setup-dev-early.service
●   ├─systemd-tmpfiles-setup-dev.service
●   ├─systemd-tmpfiles-setup.service
○   ├─systemd-tpm2-setup-early.service
○   ├─systemd-tpm2-setup.service
●   ├─systemd-udev-trigger.service
●   ├─systemd-udevd.service
○   ├─systemd-update-done.service
●   ├─systemd-update-utmp.service
●   ├─cryptsetup.target
●   ├─integritysetup.target
●   ├─local-fs.target
●   │ ├─-.mount
●   │ ├─boot-efi.mount
●   │ ├─boot.mount
○   │ ├─systemd-fsck-root.service
●   │ └─systemd-remount-fs.service
●   ├─swap.target
●   │ └─swapfile.swap
●   └─veritysetup.target
TIMERS_MATCH_COUNT=1
REVERSE_DEPENDENCIES_COUNT=1

### PROJECT_AND_SYSTEM_REFERENCES
/etc/systemd/system/ndsp-market-prices-updater.timer:8:Unit=ndsp-market-prices-updater.service
/etc/systemd/system/timers.target.wants/ndsp-market-prices-updater.timer:8:Unit=ndsp-market-prices-updater.service
PROJECT_SYSTEM_REFS_COUNT=2

### PORTS_AND_PROCESSES
LISTEN 0      5          127.0.0.1:9093      0.0.0.0:*    users:(("python3",pid=1324,fd=3))                                                                                                                                                                                                       
LISTEN 0      5          127.0.0.1:9092      0.0.0.0:*    users:(("python3",pid=1327,fd=3))                                                                                                                                                                                                       
LISTEN 0      511        127.0.0.1:9001      0.0.0.0:*    users:(("node",pid=1318,fd=32))                                                                                                                                                                                                         
LISTEN 0      5          127.0.0.1:9002      0.0.0.0:*    users:(("python3",pid=1361,fd=3))                                                                                                                                                                                                       
LISTEN 0      511        127.0.0.1:9021      0.0.0.0:*    users:(("node",pid=1323,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9020      0.0.0.0:*    users:(("node",pid=2755,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9023      0.0.0.0:*    users:(("node",pid=2671,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9022      0.0.0.0:*    users:(("node",pid=2666,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9017      0.0.0.0:*    users:(("node",pid=2635,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9019      0.0.0.0:*    users:(("node",pid=2737,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9028      0.0.0.0:*    users:(("node",pid=2733,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9031      0.0.0.0:*    users:(("node",pid=2654,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9030      0.0.0.0:*    users:(("node",pid=2621,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9024      0.0.0.0:*    users:(("node",pid=2611,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9027      0.0.0.0:*    users:(("node",pid=2730,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9033      0.0.0.0:*    users:(("node",pid=1355,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9034      0.0.0.0:*    users:(("node",pid=1363,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9044      0.0.0.0:*    users:(("node",pid=1314,fd=32))                                                                                                                                                                                                         
LISTEN 0      5          127.0.0.1:9047      0.0.0.0:*    users:(("python3",pid=2731,fd=3))                                                                                                                                                                                                       
LISTEN 0      511        127.0.0.1:9041      0.0.0.0:*    users:(("node",pid=2743,fd=32))                                                                                                                                                                                                         
LISTEN 0      2048       127.0.0.1:9061      0.0.0.0:*    users:(("uvicorn",pid=1311,fd=6))                                                                                                                                                                                                       
LISTEN 0      511        127.0.0.1:9062      0.0.0.0:*    users:(("node",pid=2746,fd=32))                                                                                                                                                                                                         
LISTEN 0      2048       127.0.0.1:9057      0.0.0.0:*    users:(("python3",pid=1354,fd=13))                                                                                                                                                                                                      
LISTEN 0      2048       127.0.0.1:9069      0.0.0.0:*    users:(("uvicorn",pid=2702,fd=13))                                                                                                                                                                                                      
LISTEN 0      2048       127.0.0.1:9068      0.0.0.0:*    users:(("python3",pid=2651,fd=13))                                                                                                                                                                                                      
LISTEN 0      511        127.0.0.1:9070      0.0.0.0:*    users:(("node",pid=2742,fd=32))                                                                                                                                                                                                         
LISTEN 0      2048       127.0.0.1:9065      0.0.0.0:*    users:(("uvicorn",pid=1315,fd=13))                                                                                                                                                                                                      
LISTEN 0      511        127.0.0.1:9064      0.0.0.0:*    users:(("node",pid=2745,fd=32))                                                                                                                                                                                                         
LISTEN 0      5          127.0.0.1:9067      0.0.0.0:*    users:(("python3",pid=1319,fd=3))                                                                                                                                                                                                       
LISTEN 0      2048       127.0.0.1:9066      0.0.0.0:*    users:(("python3",pid=1322,fd=13))                                                                                                                                                                                                      
LISTEN 0      511        127.0.0.1:9077      0.0.0.0:*    users:(("node",pid=1302,fd=32))                                                                                                                                                                                                         
LISTEN 0      2048       127.0.0.1:9076      0.0.0.0:*    users:(("uvicorn",pid=1321,fd=13))                                                                                                                                                                                                      
LISTEN 0      511        127.0.0.1:9079      0.0.0.0:*    users:(("node",pid=1312,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9078      0.0.0.0:*    users:(("node",pid=1309,fd=33))                                                                                                                                                                                                         
LISTEN 0      2048       127.0.0.1:9074      0.0.0.0:*    users:(("uvicorn",pid=2712,fd=6))                                                                                                                                                                                                       
LISTEN 0      5          127.0.0.1:9084      0.0.0.0:*    users:(("python3",pid=1326,fd=3))                                                                                                                                                                                                       
LISTEN 0      511        127.0.0.1:9081      0.0.0.0:*    users:(("node",pid=1310,fd=32))                                                                                                                                                                                                         
LISTEN 0      511        127.0.0.1:9080      0.0.0.0:*    users:(("node",pid=1305,fd=32))                                                                                                                                                                                                         
LISTEN 0      5          127.0.0.1:9083      0.0.0.0:*    users:(("python3",pid=1325,fd=3))                                                                                                                                                                                                       
LISTEN 0      5          127.0.0.1:9082      0.0.0.0:*    users:(("python3",pid=1320,fd=3))                                                                                                                                                                                                       
LISTEN 0      511        127.0.0.1:8097      0.0.0.0:*    users:(("node",pid=1356,fd=32))                                                                                                                                                                                                         
   1302 nawaf511       08:15 /usr/bin/node /opt/ndsp16-api/server.js
   1305 nawaf511       08:15 /usr/bin/node /home/nawaf511/empire-core-new/backend/services/bot_execution/main.cjs
   1309 nawaf511       08:15 /usr/bin/node /home/nawaf511/empire-core-new/backend/services/completed_decision/main.cjs
   1310 nawaf511       08:15 /usr/bin/node /home/nawaf511/empire-core-new/backend/services/ctl-001-workspace-identity/main.cjs
   1311 root           08:15 /opt/ndsp-decision-package-v1/venv/bin/python3 /opt/ndsp-decision-package-v1/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9061
   1312 nawaf511       08:15 /usr/bin/node /home/nawaf511/empire-core-new/backend/services/decision_governance_core/main.cjs
   1314 nawaf511       08:15 /usr/bin/node /home/nawaf511/empire-core-new/apps/ndsp-governance-bridge/server.mjs
   1315 nawaf511       08:15 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-layers-api/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9065
   1318 nawaf511       08:15 /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_platform_gateway_9001.cjs
   1321 nawaf511       08:15 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/python3 /home/nawaf511/empire-core-new/apps/ndsp-raw-cot-gateway/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9076
   1322 root           08:15 /usr/bin/python3 -m uvicorn main:app --host 127.0.0.1 --port 9066
   1323 root           08:15 /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_user_dashboard_gateway.cjs
   1355 nawaf511       08:15 /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp_live_market_adapter.cjs
   1356 nawaf511       08:14 /usr/bin/node /opt/ndsp-news-ticker/server.js
   1363 nawaf511       08:14 /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp_scenario_levels_adapter.cjs
   2611 nawaf511       08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp-access-guard-9024/server.js
   2621 nawaf511       08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp-access-guard-final/server.js
   2635 root           08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_admin_actions_gateway.cjs
   2651 root           08:10 /usr/bin/python3 -m uvicorn app:app --host 127.0.0.1 --port 9068
   2654 root           08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/admin_users_official_api/server.js
   2666 root           08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_api_compat_gateway.cjs
   2671 root           08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_admin_ui_proxy.cjs
   2702 postgres       08:10 /opt/ndsp-change-password-gateway/venv/bin/python3 /opt/ndsp-change-password-gateway/venv/bin/uvicorn app:app --host 127.0.0.1 --port 9069
   2712 postgres       08:10 /opt/ndsp-current-user-display/.venv/bin/python3 /opt/ndsp-current-user-display/.venv/bin/uvicorn app:app --host 127.0.0.1 --port 9074
   2730 nawaf511       08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/password_reset_gateway/server.js
   2733 root           08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_register_compat_gateway.cjs
   2737 root           08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_trial_register_gateway.cjs
   2742 nawaf511       08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_trial_fingerprint_guard_proxy.cjs
   2743 nawaf511       08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp-trial-register-canonical-wrapper/server.js
   2745 nawaf511       08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp-trial-seats-api/server.js
   2746 nawaf511       08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp-user-alert-channels/server.js
   2753 nawaf511       08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/ndsp-telegram-link-listener/server.js
   2755 nawaf511       08:10 /usr/bin/node /home/nawaf511/empire-core-new/backend/auth_api/ndsp_user_login_gateway.cjs
   3787 nawaf511       08:06 sh -c node server.js
   3788 nawaf511       08:06 node server.js
  40527 nawaf511       00:00 /home/nawaf511/empire-core-new/backend/venv/bin/python /home/nawaf511/empire-core-new/backend/venv/bin/gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:9002 --workers 4 --timeout 120
  40544 nawaf511       00:00 /usr/bin/node /home/nawaf511/empire-core-new/backend/services/bot_execution/main.cjs
  40551 nawaf511       00:00 /usr/bin/node /home/nawaf511/empire-core-new/backend/services/decision_governance_core/main.cjs
  40576 root           00:00 grep -E ndsp-market-prices-updater|market-prices|ndip-api-new|uvicorn|app.main|platform_gateway|ndsp_platform_gateway|node
  40577 root           00:00 tee /tmp/NDSP_P3_ALERT_RESOLVER_H_20260708_225727/ndsp-market-prices-updater/process_matches.txt

### PRELIMINARY_RECOMMENDATION
PRELIMINARY_RECOMMENDATION=NEEDS_TARGETED_FIX_OR_DISABLE_AFTER_CLASSIFICATION

---- SERVICE=ndip-api-new.service ----
ENABLED=disabled
ACTIVE=activating
FAILED=activating
UNIT_FILE_STATE=disabled
LOAD_STATE=loaded
SUB_STATE=auto-restart
RESULT=exit-code
EXEC_MAIN_STATUS=1
MAIN_PID=0
N_RESTARTS=90
FRAGMENT=/etc/systemd/system/ndip-api-new.service

### UNIT_FILE
# /etc/systemd/system/ndip-api-new.service
[Unit]
Description=NDIP API - New Backend
After=network.target

[Service]
Type=simple
User=nawaf511
WorkingDirectory=/home/nawaf511/empire-core-new/backend
EnvironmentFile=/home/nawaf511/empire-core-new/backend/.env
ExecStart=/home/nawaf511/empire-core-new/backend/venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 9000
Restart=always
RestartSec=5
TimeoutStopSec=20
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target

# /etc/systemd/system/ndip-api-new.service.d/10-mt4-dir.conf
[Service]
Environment=NDIP_MT4_CSV_DIR=/home/nawaf511/empire-core-new/backend/data/mt4
Environment=NDSP_MT4_CSV_DIR=/home/nawaf511/empire-core-new/backend/data/mt4

### SHOW_KEY_FIELDS
Restart=always
Result=exit-code
NRestarts=90
ExecMainStatus=1
ExecStart={ path=/home/nawaf511/empire-core-new/backend/venv/bin/python ; argv[]=/home/nawaf511/empire-core-new/backend/venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 9000 ; ignore_errors=no ; start_time=[Wed 2026-07-08 22:58:49 CEST] ; stop_time=[Wed 2026-07-08 22:58:49 CEST] ; pid=40533 ; code=exited ; status=1 }
WorkingDirectory=/home/nawaf511/empire-core-new/backend
User=nawaf511
Id=ndip-api-new.service
Requires=sysinit.target system.slice -.mount
Before=dsp-elite-trial-expiry.service shutdown.target ndip-health-monitor.service ndip-telegram-decision-worker.service
After=-.mount basic.target sysinit.target network.target system.slice systemd-journald.socket
Description=NDIP API - New Backend
LoadState=loaded
ActiveState=activating
SubState=auto-restart
FragmentPath=/etc/systemd/system/ndip-api-new.service
UnitFileState=disabled

### JOURNAL_CURRENT_BOOT
يوليو 08 22:55:59 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 59.
يوليو 08 22:55:59 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:56:00 vmi2934783 python[27829]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:56:00 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:56:00 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:56:05 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 60.
يوليو 08 22:56:05 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:56:05 vmi2934783 python[27984]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:56:05 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:56:05 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:56:10 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 61.
يوليو 08 22:56:10 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:56:11 vmi2934783 python[28077]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:56:11 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:56:11 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:56:16 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 62.
يوليو 08 22:56:16 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:56:16 vmi2934783 python[28223]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:56:16 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:56:16 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:56:21 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 63.
يوليو 08 22:56:21 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:56:22 vmi2934783 python[29329]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:56:22 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:56:22 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:56:27 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 64.
يوليو 08 22:56:27 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:56:27 vmi2934783 python[29421]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:56:27 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:56:27 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:56:32 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 65.
يوليو 08 22:56:32 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:56:33 vmi2934783 python[29527]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:56:33 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:56:33 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:56:38 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 66.
يوليو 08 22:56:38 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:56:38 vmi2934783 python[29699]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:56:38 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:56:38 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:56:43 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 67.
يوليو 08 22:56:43 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:56:44 vmi2934783 python[30864]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:56:44 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:56:44 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:56:49 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 68.
يوليو 08 22:56:49 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:56:49 vmi2934783 python[30951]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:56:49 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:56:49 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:56:54 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 69.
يوليو 08 22:56:54 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:56:54 vmi2934783 python[31084]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:56:54 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:56:54 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:57:00 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 70.
يوليو 08 22:57:00 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:57:00 vmi2934783 python[31180]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:57:00 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:57:00 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:57:05 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 71.
يوليو 08 22:57:05 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:57:05 vmi2934783 python[32294]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:57:06 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:57:06 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:57:11 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 72.
يوليو 08 22:57:11 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:57:11 vmi2934783 python[32378]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:57:11 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:57:11 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:57:16 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 73.
يوليو 08 22:57:16 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:57:16 vmi2934783 python[32518]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:57:16 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:57:16 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:57:22 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 74.
يوليو 08 22:57:22 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:57:22 vmi2934783 python[33014]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:57:22 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:57:22 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:57:27 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 75.
يوليو 08 22:57:27 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:57:27 vmi2934783 python[34537]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:57:28 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:57:28 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:57:33 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 76.
يوليو 08 22:57:33 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:57:33 vmi2934783 python[34636]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:57:33 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:57:33 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:57:38 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 77.
يوليو 08 22:57:38 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:57:38 vmi2934783 python[34787]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:57:38 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:57:38 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:57:44 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 78.
يوليو 08 22:57:44 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:57:44 vmi2934783 python[35936]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:57:44 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:57:44 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:57:49 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 79.
يوليو 08 22:57:49 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:57:49 vmi2934783 python[36064]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:57:49 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:57:49 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:57:55 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 80.
يوليو 08 22:57:55 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:57:55 vmi2934783 python[36195]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:57:55 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:57:55 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:58:00 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 81.
يوليو 08 22:58:00 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:58:00 vmi2934783 python[36268]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:58:01 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:58:01 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:58:06 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 82.
يوليو 08 22:58:06 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:58:06 vmi2934783 python[37396]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:58:06 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:58:06 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:58:11 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 83.
يوليو 08 22:58:11 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:58:11 vmi2934783 python[37494]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:58:11 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:58:11 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:58:16 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 84.
يوليو 08 22:58:16 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:58:17 vmi2934783 python[37814]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:58:17 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:58:17 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:58:22 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 85.
يوليو 08 22:58:22 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:58:22 vmi2934783 python[37917]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:58:22 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:58:22 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:58:27 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 86.
يوليو 08 22:58:27 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:58:28 vmi2934783 python[39010]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:58:28 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:58:28 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:58:33 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 87.
يوليو 08 22:58:33 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:58:33 vmi2934783 python[39113]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:58:33 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:58:33 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:58:38 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 88.
يوليو 08 22:58:38 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:58:39 vmi2934783 python[39258]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:58:39 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:58:39 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:58:44 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 89.
يوليو 08 22:58:44 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:58:44 vmi2934783 python[39429]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:58:44 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:58:44 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.
يوليو 08 22:58:49 vmi2934783 systemd[1]: ndip-api-new.service: Scheduled restart job, restart counter is at 90.
يوليو 08 22:58:49 vmi2934783 systemd[1]: Started ndip-api-new.service - NDIP API - New Backend.
يوليو 08 22:58:49 vmi2934783 python[40533]: ERROR:    Error loading ASGI app. Could not import module "app.main".
يوليو 08 22:58:49 vmi2934783 systemd[1]: ndip-api-new.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 22:58:49 vmi2934783 systemd[1]: ndip-api-new.service: Failed with result 'exit-code'.

### TIMERS_AND_DEPENDENCIES
ndip-api-new.service
● ├─ndip-health-monitor.service
● └─ndip-telegram-decision-worker.service
ndip-api-new.service
● ├─-.mount
● ├─system.slice
● └─sysinit.target
●   ├─apparmor.service
●   ├─blk-availability.service
●   ├─dev-hugepages.mount
●   ├─dev-mqueue.mount
●   ├─finalrd.service
●   ├─keyboard-setup.service
●   ├─kmod-static-nodes.service
○   ├─ldconfig.service
●   ├─lvm2-lvmpolld.socket
●   ├─lvm2-monitor.service
○   ├─open-iscsi.service
●   ├─plymouth-read-write.service
○   ├─plymouth-start.service
●   ├─proc-sys-fs-binfmt_misc.automount
●   ├─setvtrgb.service
●   ├─sys-fs-fuse-connections.mount
●   ├─sys-kernel-config.mount
●   ├─sys-kernel-debug.mount
●   ├─sys-kernel-tracing.mount
●   ├─systemd-ask-password-console.path
●   ├─systemd-binfmt.service
○   ├─systemd-firstboot.service
○   ├─systemd-hwdb-update.service
○   ├─systemd-journal-catalog-update.service
●   ├─systemd-journal-flush.service
●   ├─systemd-journald.service
○   ├─systemd-machine-id-commit.service
●   ├─systemd-modules-load.service
○   ├─systemd-pcrmachine.service
○   ├─systemd-pcrphase-sysinit.service
○   ├─systemd-pcrphase.service
○   ├─systemd-pstore.service
●   ├─systemd-random-seed.service
○   ├─systemd-repart.service
●   ├─systemd-resolved.service
●   ├─systemd-sysctl.service
○   ├─systemd-sysusers.service
●   ├─systemd-timesyncd.service
●   ├─systemd-tmpfiles-setup-dev-early.service
●   ├─systemd-tmpfiles-setup-dev.service
●   ├─systemd-tmpfiles-setup.service
○   ├─systemd-tpm2-setup-early.service
○   ├─systemd-tpm2-setup.service
●   ├─systemd-udev-trigger.service
●   ├─systemd-udevd.service
○   ├─systemd-update-done.service
●   ├─systemd-update-utmp.service
●   ├─cryptsetup.target
●   ├─integritysetup.target
●   ├─local-fs.target
●   │ ├─-.mount
●   │ ├─boot-efi.mount
●   │ ├─boot.mount
○   │ ├─systemd-fsck-root.service
●   │ └─systemd-remount-fs.service
●   ├─swap.target
●   │ └─swapfile.swap
●   └─veritysetup.target
