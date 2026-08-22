# NDSP Frontend Source Of Truth

Official source:
- /home/nawaf511/empire-core-new/apps/public-landing -> /var/www/ndsp
- /home/nawaf511/empire-core-new/apps/user-portal -> /var/www/ndsp-my
- /home/nawaf511/empire-core-new/apps/admin-console -> /var/www/ndsp-admin

Policy:
- /var/www is deployment output only.
- Do not edit /var/www directly.
- Edit apps/* then run:
  sudo /home/nawaf511/empire-core-new/deploy_frontend_from_apps.sh
