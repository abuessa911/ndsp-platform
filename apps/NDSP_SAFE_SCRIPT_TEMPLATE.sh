#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/nawaf511/empire-core-new"
source "$ROOT/apps/ndsp_apps_only_guard.sh"
ndsp_scan_script_for_forbidden_var_www_edit "$0"

PUBLIC_SRC="$ROOT/apps/public-landing"
USER_SRC="$ROOT/apps/user-portal"
ADMIN_SRC="$ROOT/apps/admin-console"

# عدّل المصدر داخل apps فقط.
# /var/www مخرجات نشر فقط وليس مصدر تعديل.
