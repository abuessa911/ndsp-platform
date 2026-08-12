# NDSP P2 Root Diagnostics Read-only
DATE=2026-07-08T01:03:19+02:00
MODE=ROOT_READ_ONLY_DIAGNOSTICS
MODIFICATIONS=None

## 1) Nginx sudo config test
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful

## 2) Certbot diagnostics
× certbot.service - Certbot
     Loaded: loaded (/usr/lib/systemd/system/certbot.service; static)
     Active: failed (Result: exit-code) since Tue 2026-07-07 14:36:44 CEST; 10h ago
TriggeredBy: ● certbot.timer
       Docs: file:///usr/share/doc/python-certbot-doc/html/index.html
             https://certbot.eff.org/docs
   Main PID: 3951735 (code=exited, status=1/FAILURE)
        CPU: 10.925s

يوليو 07 14:36:44 vmi2934783 certbot[3951735]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 07 14:36:44 vmi2934783 certbot[3951735]: All renewals failed. The following certificates could not be renewed:
يوليو 07 14:36:44 vmi2934783 certbot[3951735]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 07 14:36:44 vmi2934783 certbot[3951735]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 07 14:36:44 vmi2934783 certbot[3951735]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 07 14:36:44 vmi2934783 certbot[3951735]: 3 renew failure(s), 0 parse failure(s)
يوليو 07 14:36:44 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 07 14:36:44 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 07 14:36:44 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 07 14:36:44 vmi2934783 systemd[1]: certbot.service: Consumed 10.925s CPU time.
● certbot.timer - Run certbot twice daily
     Loaded: loaded (/usr/lib/systemd/system/certbot.timer; enabled; preset: enabled)
     Active: active (waiting) since Sun 2026-07-05 12:00:04 CEST; 2 days ago
    Trigger: Wed 2026-07-08 05:35:07 CEST; 4h 31min left
   Triggers: ● certbot.service

يوليو 05 12:00:04 vmi2934783 systemd[1]: Started certbot.timer - Run certbot twice daily.
يوليو 05 06:40:26 vmi2934783 systemd[1]: Starting certbot.service - Certbot...
يوليو 05 06:40:34 vmi2934783 certbot[951716]: Failed to renew certificate api.nawafo.shop with error: Some challenges have failed.
يوليو 05 06:40:41 vmi2934783 certbot[951716]: Failed to renew certificate dashboard.nawafo.shop with error: Some challenges have failed.
يوليو 05 06:40:51 vmi2934783 certbot[951716]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 05 06:40:52 vmi2934783 certbot[951716]: All renewals failed. The following certificates could not be renewed:
يوليو 05 06:40:52 vmi2934783 certbot[951716]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 05 06:40:52 vmi2934783 certbot[951716]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 05 06:40:52 vmi2934783 certbot[951716]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 05 06:40:52 vmi2934783 certbot[951716]: 3 renew failure(s), 0 parse failure(s)
يوليو 05 06:40:52 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 06:40:52 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 05 06:40:52 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 05 06:40:52 vmi2934783 systemd[1]: certbot.service: Consumed 9.988s CPU time.
-- Boot 30171be6091c48feadc15fe5b126358c --
يوليو 05 16:38:43 vmi2934783 systemd[1]: Starting certbot.service - Certbot...
يوليو 05 16:38:51 vmi2934783 certbot[1973622]: Failed to renew certificate api.nawafo.shop with error: Some challenges have failed.
يوليو 05 16:38:58 vmi2934783 certbot[1973622]: Failed to renew certificate dashboard.nawafo.shop with error: Some challenges have failed.
يوليو 05 16:39:08 vmi2934783 certbot[1973622]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 05 16:39:08 vmi2934783 certbot[1973622]: All renewals failed. The following certificates could not be renewed:
يوليو 05 16:39:08 vmi2934783 certbot[1973622]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 05 16:39:08 vmi2934783 certbot[1973622]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 05 16:39:08 vmi2934783 certbot[1973622]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 05 16:39:08 vmi2934783 certbot[1973622]: 3 renew failure(s), 0 parse failure(s)
يوليو 05 16:39:08 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 05 16:39:08 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 05 16:39:08 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 05 16:39:08 vmi2934783 systemd[1]: certbot.service: Consumed 9.938s CPU time.
يوليو 06 11:43:18 vmi2934783 systemd[1]: Starting certbot.service - Certbot...
يوليو 06 11:43:26 vmi2934783 certbot[1822501]: Failed to renew certificate api.nawafo.shop with error: Some challenges have failed.
يوليو 06 11:43:34 vmi2934783 certbot[1822501]: Failed to renew certificate dashboard.nawafo.shop with error: Some challenges have failed.
يوليو 06 11:43:44 vmi2934783 certbot[1822501]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 06 11:43:44 vmi2934783 certbot[1822501]: All renewals failed. The following certificates could not be renewed:
يوليو 06 11:43:44 vmi2934783 certbot[1822501]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 06 11:43:44 vmi2934783 certbot[1822501]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 06 11:43:44 vmi2934783 certbot[1822501]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 06 11:43:44 vmi2934783 certbot[1822501]: 3 renew failure(s), 0 parse failure(s)
يوليو 06 11:43:44 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 06 11:43:44 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 06 11:43:44 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 06 11:43:44 vmi2934783 systemd[1]: certbot.service: Consumed 10.729s CPU time.
يوليو 06 23:22:42 vmi2934783 systemd[1]: Starting certbot.service - Certbot...
يوليو 06 23:22:51 vmi2934783 certbot[2567992]: Failed to renew certificate api.nawafo.shop with error: Some challenges have failed.
يوليو 06 23:22:58 vmi2934783 certbot[2567992]: Failed to renew certificate dashboard.nawafo.shop with error: Some challenges have failed.
يوليو 06 23:23:08 vmi2934783 certbot[2567992]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 06 23:23:08 vmi2934783 certbot[2567992]: All renewals failed. The following certificates could not be renewed:
يوليو 06 23:23:08 vmi2934783 certbot[2567992]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 06 23:23:08 vmi2934783 certbot[2567992]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 06 23:23:08 vmi2934783 certbot[2567992]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 06 23:23:08 vmi2934783 certbot[2567992]: 3 renew failure(s), 0 parse failure(s)
يوليو 06 23:23:08 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 06 23:23:08 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 06 23:23:08 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 06 23:23:08 vmi2934783 systemd[1]: certbot.service: Consumed 10.836s CPU time.
يوليو 07 10:28:46 vmi2934783 systemd[1]: Starting certbot.service - Certbot...
يوليو 07 10:28:54 vmi2934783 certbot[2964364]: Failed to renew certificate api.nawafo.shop with error: Some challenges have failed.
يوليو 07 10:29:01 vmi2934783 certbot[2964364]: Failed to renew certificate dashboard.nawafo.shop with error: Some challenges have failed.
يوليو 07 10:29:11 vmi2934783 certbot[2964364]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 07 10:29:11 vmi2934783 certbot[2964364]: All renewals failed. The following certificates could not be renewed:
يوليو 07 10:29:11 vmi2934783 certbot[2964364]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 07 10:29:11 vmi2934783 certbot[2964364]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 07 10:29:11 vmi2934783 certbot[2964364]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 07 10:29:11 vmi2934783 certbot[2964364]: 3 renew failure(s), 0 parse failure(s)
يوليو 07 10:29:11 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 07 10:29:11 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 07 10:29:11 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 07 10:29:11 vmi2934783 systemd[1]: certbot.service: Consumed 10.271s CPU time.
يوليو 07 14:36:17 vmi2934783 systemd[1]: Starting certbot.service - Certbot...
يوليو 07 14:36:27 vmi2934783 certbot[3951735]: Failed to renew certificate api.nawafo.shop with error: Some challenges have failed.
يوليو 07 14:36:34 vmi2934783 certbot[3951735]: Failed to renew certificate dashboard.nawafo.shop with error: Some challenges have failed.
يوليو 07 14:36:44 vmi2934783 certbot[3951735]: Failed to renew certificate nawafo.shop with error: Some challenges have failed.
يوليو 07 14:36:44 vmi2934783 certbot[3951735]: All renewals failed. The following certificates could not be renewed:
يوليو 07 14:36:44 vmi2934783 certbot[3951735]:   /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem (failure)
يوليو 07 14:36:44 vmi2934783 certbot[3951735]:   /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem (failure)
يوليو 07 14:36:44 vmi2934783 certbot[3951735]:   /etc/letsencrypt/live/nawafo.shop/fullchain.pem (failure)
يوليو 07 14:36:44 vmi2934783 certbot[3951735]: 3 renew failure(s), 0 parse failure(s)
يوليو 07 14:36:44 vmi2934783 systemd[1]: certbot.service: Main process exited, code=exited, status=1/FAILURE
يوليو 07 14:36:44 vmi2934783 systemd[1]: certbot.service: Failed with result 'exit-code'.
يوليو 07 14:36:44 vmi2934783 systemd[1]: Failed to start certbot.service - Certbot.
يوليو 07 14:36:44 vmi2934783 systemd[1]: certbot.service: Consumed 10.925s CPU time.
Saving debug log to /var/log/letsencrypt/letsencrypt.log

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Found the following certs:
  Certificate Name: admin.ndsp.app
    Serial Number: 53c2555386c244e08959a7d03e4fcd1710d
    Key Type: ECDSA
    Domains: admin.ndsp.app
    Expiry Date: 2026-09-14 19:16:28+00:00 (VALID: 68 days)
    Certificate Path: /etc/letsencrypt/live/admin.ndsp.app/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/admin.ndsp.app/privkey.pem
  Certificate Name: api.nawafo.shop
    Serial Number: 596f6ff6c673b9378dcfdec6934ea0ceb1f
    Key Type: ECDSA
    Domains: api.nawafo.shop
    Expiry Date: 2026-07-15 01:22:52+00:00 (VALID: 7 days)
    Certificate Path: /etc/letsencrypt/live/api.nawafo.shop/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/api.nawafo.shop/privkey.pem
  Certificate Name: api.ndsp.app
    Serial Number: 5514b9825a0a0668deff72724b31bd538ef
    Key Type: ECDSA
    Domains: ndsp.app api.ndsp.app bot.ndsp.app my.ndsp.app www.ndsp.app
    Expiry Date: 2026-09-26 16:32:02+00:00 (VALID: 80 days)
    Certificate Path: /etc/letsencrypt/live/api.ndsp.app/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/api.ndsp.app/privkey.pem
  Certificate Name: bot.ndsp.app
    Serial Number: 6c699f94d44ff5f543c07dc8dd5a9d84d38
    Key Type: ECDSA
    Domains: bot.ndsp.app
    Expiry Date: 2026-08-27 16:13:14+00:00 (VALID: 50 days)
    Certificate Path: /etc/letsencrypt/live/bot.ndsp.app/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/bot.ndsp.app/privkey.pem
  Certificate Name: dashboard.nawafo.shop
    Serial Number: 6adc8a241341eca2cafe80d061a8b7106f7
    Key Type: ECDSA
    Domains: dashboard.nawafo.shop
    Expiry Date: 2026-07-15 01:08:12+00:00 (VALID: 7 days)
    Certificate Path: /etc/letsencrypt/live/dashboard.nawafo.shop/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/dashboard.nawafo.shop/privkey.pem
  Certificate Name: my.ndsp.app
    Serial Number: 5750c4826ba90f0d77847aa481e3996a23d
    Key Type: ECDSA
    Domains: my.ndsp.app
    Expiry Date: 2026-09-19 19:03:08+00:00 (VALID: 73 days)
    Certificate Path: /etc/letsencrypt/live/my.ndsp.app/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/my.ndsp.app/privkey.pem
  Certificate Name: nawafo.shop
    Serial Number: 565c144b329dd19d6f8a3a286ec689e3a54
    Key Type: ECDSA
    Domains: nawafo.shop admin.nawafo.shop api.nawafo.shop app.nawafo.shop ws.nawafo.shop www.nawafo.shop
    Expiry Date: 2026-07-31 22:02:27+00:00 (VALID: 23 days)
    Certificate Path: /etc/letsencrypt/live/nawafo.shop/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/nawafo.shop/privkey.pem
  Certificate Name: ndsp.app-0005
    Serial Number: 60606b943519b2d8d2ab57cd34c990b05f5
    Key Type: ECDSA
    Domains: ndsp.app admin.ndsp.app api.ndsp.app my.ndsp.app www.ndsp.app
    Expiry Date: 2026-08-21 15:09:09+00:00 (VALID: 44 days)
    Certificate Path: /etc/letsencrypt/live/ndsp.app-0005/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/ndsp.app-0005/privkey.pem
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

## 3) Logrotate diagnostics
× logrotate.service - Rotate log files
     Loaded: loaded (/usr/lib/systemd/system/logrotate.service; static)
     Active: failed (Result: exit-code) since Wed 2026-07-08 00:00:05 CEST; 1h 3min ago
TriggeredBy: ● logrotate.timer
       Docs: man:logrotate(8)
             man:logrotate.conf(5)
   Main PID: 2029717 (code=exited, status=1/FAILURE)
        CPU: 1.173s

يوليو 08 00:00:00 vmi2934783 systemd[1]: Starting logrotate.service - Rotate log files...
يوليو 08 00:00:00 vmi2934783 logrotate[2029717]: error: nginx:1 duplicate log entry for /var/log/nginx/nawafo_access.log
يوليو 08 00:00:00 vmi2934783 logrotate[2029717]: error: found error in file nginx, skipping
يوليو 08 00:00:01 vmi2934783 systemctl[2030317]: Warning: The unit file, source configuration file or drop-ins of cups.service changed on disk. Run 'systemctl daemon-reload' to reload units.
يوليو 08 00:00:05 vmi2934783 systemd[1]: logrotate.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 00:00:05 vmi2934783 systemd[1]: logrotate.service: Failed with result 'exit-code'.
يوليو 08 00:00:05 vmi2934783 systemd[1]: Failed to start logrotate.service - Rotate log files.
يوليو 08 00:00:05 vmi2934783 systemd[1]: logrotate.service: Consumed 1.173s CPU time.
● logrotate.timer - Daily rotation of log files
     Loaded: loaded (/usr/lib/systemd/system/logrotate.timer; enabled; preset: enabled)
     Active: active (waiting) since Sun 2026-07-05 12:00:04 CEST; 2 days ago
    Trigger: Thu 2026-07-09 00:00:00 CEST; 22h left
   Triggers: ● logrotate.service
       Docs: man:logrotate(8)
             man:logrotate.conf(5)

يوليو 05 12:00:04 vmi2934783 systemd[1]: Started logrotate.timer - Daily rotation of log files.
يوليو 06 00:00:00 vmi2934783 systemd[1]: Starting logrotate.service - Rotate log files...
يوليو 06 00:00:00 vmi2934783 logrotate[944025]: error: nginx:1 duplicate log entry for /var/log/nginx/nawafo_access.log
يوليو 06 00:00:00 vmi2934783 logrotate[944025]: error: found error in file nginx, skipping
يوليو 06 00:00:05 vmi2934783 systemd[1]: logrotate.service: Main process exited, code=exited, status=1/FAILURE
يوليو 06 00:00:05 vmi2934783 systemd[1]: logrotate.service: Failed with result 'exit-code'.
يوليو 06 00:00:05 vmi2934783 systemd[1]: Failed to start logrotate.service - Rotate log files.
يوليو 06 00:00:05 vmi2934783 systemd[1]: logrotate.service: Consumed 1.246s CPU time.
يوليو 07 00:00:00 vmi2934783 systemd[1]: Starting logrotate.service - Rotate log files...
يوليو 07 00:00:00 vmi2934783 logrotate[2836798]: error: nginx:1 duplicate log entry for /var/log/nginx/nawafo_access.log
يوليو 07 00:00:00 vmi2934783 logrotate[2836798]: error: found error in file nginx, skipping
يوليو 07 00:00:04 vmi2934783 systemd[1]: logrotate.service: Main process exited, code=exited, status=1/FAILURE
يوليو 07 00:00:04 vmi2934783 systemd[1]: logrotate.service: Failed with result 'exit-code'.
يوليو 07 00:00:04 vmi2934783 systemd[1]: Failed to start logrotate.service - Rotate log files.
يوليو 07 00:00:04 vmi2934783 systemd[1]: logrotate.service: Consumed 1.144s CPU time.
يوليو 08 00:00:00 vmi2934783 systemd[1]: Starting logrotate.service - Rotate log files...
يوليو 08 00:00:00 vmi2934783 logrotate[2029717]: error: nginx:1 duplicate log entry for /var/log/nginx/nawafo_access.log
يوليو 08 00:00:00 vmi2934783 logrotate[2029717]: error: found error in file nginx, skipping
يوليو 08 00:00:01 vmi2934783 systemctl[2030317]: Warning: The unit file, source configuration file or drop-ins of cups.service changed on disk. Run 'systemctl daemon-reload' to reload units.
يوليو 08 00:00:05 vmi2934783 systemd[1]: logrotate.service: Main process exited, code=exited, status=1/FAILURE
يوليو 08 00:00:05 vmi2934783 systemd[1]: logrotate.service: Failed with result 'exit-code'.
يوليو 08 00:00:05 vmi2934783 systemd[1]: Failed to start logrotate.service - Rotate log files.
يوليو 08 00:00:05 vmi2934783 systemd[1]: logrotate.service: Consumed 1.173s CPU time.
warning: logrotate in debug mode does nothing except printing debug messages!  Consider using verbose mode (-v) instead if this is not what you want.

reading config file /etc/logrotate.conf
including /etc/logrotate.d
reading config file alternatives
reading config file apport
reading config file apt
reading config file bootlog
reading config file btmp
reading config file certbot
reading config file cloud-init
reading config file cups-daemon
reading config file dpkg
reading config file fail2ban
reading config file nawafo
reading config file ndip
reading config file nginx
error: nginx:1 duplicate log entry for /var/log/nginx/nawafo_access.log
error: found error in file nginx, skipping
reading config file postgresql-common
reading config file ppp
reading config file preload
reading config file redis-server
reading config file rsyslog
reading config file sane-utils
reading config file ubuntu-pro-client
reading config file ufw
reading config file unattended-upgrades
reading config file vsftpd
reading config file wtmp
reading config file xrdp
Reading state from file: /var/lib/logrotate/status
Allocating hash table for state file, size 64 entries
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state
Creating new state

Handling 26 logs

rotating pattern: /var/log/alternatives.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 2294729)
considering log /var/log/alternatives.log
  Now: 2026-07-08 01:03
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 2294729)

rotating pattern: /var/log/apport.log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 2294729)
considering log /var/log/apport.log
  Now: 2026-07-08 01:03
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log is empty)
switching euid from 0 to 0 and egid from 4 to 0 (pid 2294729)

rotating pattern: /var/log/apt/term.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 2294729)
considering log /var/log/apt/term.log
  Now: 2026-07-08 01:03
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 2294729)

rotating pattern: /var/log/apt/history.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 2294729)
considering log /var/log/apt/history.log
  Now: 2026-07-08 01:03
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 2294729)

rotating pattern: /var/log/boot.log
 after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 2294729)
considering log /var/log/boot.log
  log /var/log/boot.log does not exist -- skipping
switching euid from 0 to 0 and egid from 4 to 0 (pid 2294729)

rotating pattern: /var/log/btmp  monthly (1 rotations)
empty log files are rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 2294729)
considering log /var/log/btmp
  Now: 2026-07-08 01:03
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 2294729)

rotating pattern: /var/log/letsencrypt/*.log  weekly (12 rotations)
empty log files are rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 2294729)
considering log /var/log/letsencrypt/letsencrypt.log
  Now: 2026-07-08 01:03
  Last rotated at 2026-07-05 00:00
  log does not need rotating (log has been rotated at 2026-07-05 00:00, which is less than a week ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 2294729)

rotating pattern: /var/log/cloud-init*.log
 1048576 bytes (6 rotations)
empty log files are not rotated, old logs are removed
considering log /var/log/cloud-init.log
  Now: 2026-07-08 01:03
  Last rotated at 2025-11-28 00:00
  log does not need rotating (log size is below the 'size' threshold)
considering log /var/log/cloud-init-output.log
  Now: 2026-07-08 01:03
  Last rotated at 2025-11-28 00:00
  log does not need rotating (log size is below the 'size' threshold)

rotating pattern: /var/log/cups/*log  after 1 days (7 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 2294729)
considering log /var/log/cups/access_log
  Now: 2026-07-08 01:03
  Last rotated at 2026-07-08 00:00
  log does not need rotating (log has been rotated at 2026-07-08 00:00, which is less than a day ago)
considering log /var/log/cups/error_log
  Now: 2026-07-08 01:03
  Last rotated at 2026-07-03 00:00
  log does not need rotating (log is empty)
not running postrotate script, since no logs were rotated
switching euid from 0 to 0 and egid from 4 to 0 (pid 2294729)

rotating pattern: /var/log/dpkg.log  monthly (12 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 2294729)
considering log /var/log/dpkg.log
  Now: 2026-07-08 01:03
  Last rotated at 2026-07-01 00:00
  log does not need rotating (log has been rotated at 2026-07-01 00:00, which is less than a month ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 2294729)

rotating pattern: /var/log/fail2ban.log  weekly (4 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 2294729)
considering log /var/log/fail2ban.log
  Now: 2026-07-08 01:03
  Last rotated at 2026-07-05 00:00
  log does not need rotating (log has been rotated at 2026-07-05 00:00, which is less than a week ago)
switching euid from 0 to 0 and egid from 4 to 0 (pid 2294729)

rotating pattern: /var/log/nginx/nawafo_*.log  after 1 days (14 rotations)
empty log files are not rotated, old logs are removed
switching euid from 0 to 0 and egid from 0 to 4 (pid 2294729)
considering log /var/log/nginx/nawafo_access.log
  Now: 2026-07-08 01:03
  Last rotated at 2026-01-10 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/nawafo_api_access.log
  Now: 2026-07-08 01:03
  Last rotated at 2026-01-10 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/nawafo_api_error.log
  Now: 2026-07-08 01:03
  Last rotated at 2026-01-08 00:00
  log does not need rotating (log is empty)
considering log /var/log/nginx/nawafo_error.log

## 4) Real feeds permissions diagnostics
drwxrwxr-x 8 nawaf511 nawaf511 4096 يوليو   7 22:50 /var/www/ndsp-my
drwxr-xr-x 2 root     root     4096 يوليو   8 01:03 /var/www/ndsp-my/data
total 48
-rw-r--r-- 1 root root 46023 يوليو   8 01:03 command-center-real.json
OWNER=root GROUP=root MODE=755 PATH=/var/www/ndsp-my/data
stat: cannot statx '/var/www/ndsp-my/data/news-impact.json': No such file or directory
stat: cannot statx '/var/www/ndsp-my/data/economic-calendar.json': No such file or directory

## 5) Unit users for failed real data timers
# /etc/systemd/system/ndsp-real-feeds-sync.service
[Unit]
Description=NDSP Real Feeds Sync

[Service]
Type=oneshot
User=nawaf511
ExecStart=/usr/bin/python3 /home/nawaf511/ndsp-portal-real-data-sync/sync_real_feeds.py
# /etc/systemd/system/ndsp-tradingview-calendar.service
[Unit]
Description=NDSP TradingView Live Economic Calendar

[Service]
Type=oneshot
User=nawaf511
ExecStart=/usr/bin/python3 /home/nawaf511/ndsp-portal-real-data-sync/tradingview_live_calendar.py
# /etc/systemd/system/ndsp-real-feeds-sync.timer
[Unit]
Description=Run NDSP Real Feeds Sync every 5 minutes

[Timer]
OnBootSec=30
OnUnitActiveSec=5min
Unit=ndsp-real-feeds-sync.service

[Install]
WantedBy=timers.target
# /etc/systemd/system/ndsp-tradingview-calendar.timer
[Unit]
Description=Run NDSP TradingView Calendar every 5 minutes

[Timer]
OnBootSec=30
OnUnitActiveSec=5min
Persistent=true

[Install]
WantedBy=timers.target

## 6) PM2 startup diagnostics
# /etc/systemd/system/pm2-nawaf511.service
[Unit]
Description=PM2 process manager
Documentation=https://pm2.keymetrics.io/
After=network.target

[Service]
Type=forking
User=nawaf511
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
Environment=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/usr/bin:/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
Environment=PM2_HOME=/home/nawaf511/.pm2
PIDFile=/home/nawaf511/.pm2/pm2.pid
Restart=on-failure

ExecStart=/home/nawaf511/.npm/_npx/5f7878ce38f1eb13/node_modules/pm2/bin/pm2 resurrect
ExecReload=/home/nawaf511/.npm/_npx/5f7878ce38f1eb13/node_modules/pm2/bin/pm2 reload all
ExecStop=/home/nawaf511/.npm/_npx/5f7878ce38f1eb13/node_modules/pm2/bin/pm2 kill

[Install]
WantedBy=multi-user.target
○ pm2-nawaf511.service - PM2 process manager
     Loaded: loaded (/etc/systemd/system/pm2-nawaf511.service; enabled; preset: enabled)
     Active: inactive (dead) since Sun 2026-07-05 14:32:49 CEST; 2 days ago
   Duration: 2h 32min 32.986s
       Docs: https://pm2.keymetrics.io/
   Main PID: 3004 (code=exited, status=0/SUCCESS)
        CPU: 2h 59min 421ms

يوليو 05 12:00:15 vmi2934783 pm2[1358]: │ 0  │ ndsp-portal     │ default     │ 0.39.7  │ fork    │ 3883     │ 0s     │ 0    │ online    │ 0%       │ 19.8mb   │ nawaf511 │ disabled │
يوليو 05 12:00:15 vmi2934783 pm2[1358]: └────┴─────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
يوليو 05 12:00:16 vmi2934783 systemd[1]: Started pm2-nawaf511.service - PM2 process manager.
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] Applying action deleteProcessId on app [all](ids: [ 0, 1 ])
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [ndsp-portal](0) ✓
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [ndsp-backend](1) ✓
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [v] All Applications Stopped
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [v] PM2 Daemon Stopped
يوليو 05 14:32:49 vmi2934783 systemd[1]: pm2-nawaf511.service: Deactivated successfully.
يوليو 05 14:32:49 vmi2934783 systemd[1]: pm2-nawaf511.service: Consumed 2h 59min 421ms CPU time.
يوليو 05 11:59:02 vmi2934783 systemd[1]: Stopping pm2-nawaf511.service - PM2 process manager...
يوليو 05 11:59:05 vmi2934783 pm2[3274842]: [PM2] Applying action deleteProcessId on app [all](ids: [ 0, 1 ])
يوليو 05 11:59:05 vmi2934783 pm2[3274842]: [PM2] [ndsp-backend](1) ✓
يوليو 05 11:59:05 vmi2934783 pm2[3274842]: [PM2] [ndsp-portal](0) ✓
يوليو 05 11:59:05 vmi2934783 pm2[3274842]: [PM2] [v] All Applications Stopped
يوليو 05 11:59:05 vmi2934783 pm2[3274842]: [PM2] [v] PM2 Daemon Stopped
يوليو 05 11:59:05 vmi2934783 systemd[1]: pm2-nawaf511.service: Deactivated successfully.
يوليو 05 11:59:05 vmi2934783 systemd[1]: Stopped pm2-nawaf511.service - PM2 process manager.
يوليو 05 11:59:05 vmi2934783 systemd[1]: pm2-nawaf511.service: Consumed 12h 41min 22.385s CPU time.
-- Boot 30171be6091c48feadc15fe5b126358c --
يوليو 05 12:00:07 vmi2934783 systemd[1]: Starting pm2-nawaf511.service - PM2 process manager...
يوليو 05 12:00:14 vmi2934783 pm2[1358]: [PM2] Spawning PM2 daemon with pm2_home=/home/nawaf511/.pm2
يوليو 05 12:00:15 vmi2934783 pm2[1358]: [PM2] PM2 Successfully daemonized
يوليو 05 12:00:15 vmi2934783 pm2[1358]: [PM2] Resurrecting
يوليو 05 12:00:15 vmi2934783 pm2[1358]: [PM2] Restoring processes located in /home/nawaf511/.pm2/dump.pm2
يوليو 05 12:00:15 vmi2934783 pm2[1358]: [PM2] Process /home/nawaf511/.nvm/versions/node/v24.15.0/bin/npm restored
يوليو 05 12:00:15 vmi2934783 pm2[1358]: [PM2] Process /usr/bin/npm restored
يوليو 05 12:00:15 vmi2934783 pm2[1358]: ┌────┬─────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
يوليو 05 12:00:15 vmi2934783 pm2[1358]: │ id │ name            │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
يوليو 05 12:00:15 vmi2934783 pm2[1358]: ├────┼─────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
يوليو 05 12:00:15 vmi2934783 pm2[1358]: │ 1  │ ndsp-backend    │ default     │ N/A     │ fork    │ 3895     │ 0s     │ 0    │ online    │ 0%       │ 40.8mb   │ nawaf511 │ disabled │
يوليو 05 12:00:15 vmi2934783 pm2[1358]: │ 0  │ ndsp-portal     │ default     │ 0.39.7  │ fork    │ 3883     │ 0s     │ 0    │ online    │ 0%       │ 19.8mb   │ nawaf511 │ disabled │
يوليو 05 12:00:15 vmi2934783 pm2[1358]: └────┴─────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
يوليو 05 12:00:16 vmi2934783 systemd[1]: Started pm2-nawaf511.service - PM2 process manager.
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] Applying action deleteProcessId on app [all](ids: [ 0, 1 ])
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [ndsp-portal](0) ✓
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [ndsp-backend](1) ✓
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [v] All Applications Stopped
يوليو 05 14:32:49 vmi2934783 pm2[1093998]: [PM2] [v] PM2 Daemon Stopped
يوليو 05 14:32:49 vmi2934783 systemd[1]: pm2-nawaf511.service: Deactivated successfully.
يوليو 05 14:32:49 vmi2934783 systemd[1]: pm2-nawaf511.service: Consumed 2h 59min 421ms CPU time.
┌────┬────────────────┬─────────────┬─────────┬─────────┬──────────┬────────┬──────┬───────────┬──────────┬──────────┬──────────┬──────────┐
│ id │ name           │ namespace   │ version │ mode    │ pid      │ uptime │ ↺    │ status    │ cpu      │ mem      │ user     │ watching │
├────┼────────────────┼─────────────┼─────────┼─────────┼──────────┼────────┼──────┼───────────┼──────────┼──────────┼──────────┼──────────┤
│ [1m[36m0[39m[22m  │ ndsp-portal    │ default     │ 0.39.7  │ [7m[1mfork[22m[27m    │ 1099070  │ 2D     │ 0    │ [32m[1monline[22m[39m    │ 0%       │ 79.1mb   │ [1mnawaf511[22m │ [90mdisabled[39m │
└────┴────────────────┴─────────────┴─────────┴─────────┴──────────┴────────┴──────┴───────────┴──────────┴──────────┴──────────┴──────────┘
[1m[36mhost metrics[39m[22m | [1mcpu[22m: [32m8.4%[39m | [1mram usage[22m: [32m9.8%[39m | [1mlo[22m: ⇓ [32m0.007mb/s[39m ⇑ [32m0.007mb/s[39m | [1meth0[22m: ⇓ [32m0.051mb/s[39m ⇑ [32m0.003mb/s[39m | [1mdisk[22m: ⇓ 0mb/s ⇑ [32m0.23mb/s[39m [90m/[39m [1m[33m81.99%[39m[22m |

  error: unknown option `--dry-run'


## 7) Critical runtime still OK
nginx=active
ndsp-quality-live-nmp-wrapper=active
API_HEALTH_HTTP=200
QUALITY_LIVE_HTTP=200

FINAL_STATUS=P2_ROOT_DIAGNOSTICS_READONLY_DONE
REPORT=docs/05-runbooks/NDSP_P2_ROOT_DIAGNOSTICS_READONLY_20260708_010319.md
