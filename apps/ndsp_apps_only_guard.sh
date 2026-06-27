#!/usr/bin/env bash
set -euo pipefail

ndsp_assert_apps_source_only() {
  local target="${1:-}"
  case "$target" in
    /var/www/*)
      echo "GOVERNANCE_FAIL: /var/www is deployment output only. Edit apps source first."
      exit 91
      ;;
  esac
}

ndsp_scan_script_for_forbidden_var_www_edit() {
  local script="${1:-$0}"
  if grep -nE '(sed -i|python3|perl -pi|cat >|tee|cp -a|mv|rm -f|truncate).*\/var\/www' "$script" 2>/dev/null | grep -vE 'deploy|publish|DEPLOY_OUT|OUTPUT_ONLY'; then
    echo "GOVERNANCE_FAIL: direct /var/www edit detected in script."
    exit 92
  fi
}
