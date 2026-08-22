#!/usr/bin/env bash

main() {
  ROOT="/home/nawaf511/empire-core-v5-1-1-clean"
  FILE="$ROOT/backend/auth_api/ndsp_user_login_gateway.cjs"
  SERVICE="ndsp-user-login.service"

  echo "VERIFY: source"
  [ -f "$FILE" ] || { echo "DEPLOY_ABORT_SOURCE_MISSING"; return 1; }

  echo "VERIFY: node syntax"
  node --check "$FILE" || { echo "DEPLOY_ABORT_SYNTAX"; return 1; }

  ROUTE_COUNT="$(grep -cF "/api/auth/decision-room-access" "$FILE")"
  ENTITLEMENT_COUNT="$(grep -cF "function decisionEntitlement(user)" "$FILE")"

  if [ "$ROUTE_COUNT" -ne 1 ] || [ "$ENTITLEMENT_COUNT" -ne 1 ]; then
    echo "DEPLOY_ABORT_STATIC_INTEGRITY"
    return 1
  fi

  EXEC_START="$(SYSTEMD_PAGER=cat systemctl --no-pager show "$SERVICE" -p ExecStart --value 2>/dev/null)"

  case "$EXEC_START" in
    *"$FILE"*) ;;
    *) echo "DEPLOY_ABORT_SOURCE_BINDING"; return 1 ;;
  esac

  OLD_PID="$(SYSTEMD_PAGER=cat systemctl --no-pager show "$SERVICE" -p MainPID --value 2>/dev/null)"

  echo "ACTIVATE: $SERVICE"
  sudo systemctl restart "$SERVICE" || { echo "DEPLOY_ABORT_RESTART"; return 1; }
  sleep 2

  ACTIVE="$(SYSTEMD_PAGER=cat systemctl --no-pager is-active "$SERVICE" 2>/dev/null)"
  NEW_PID="$(SYSTEMD_PAGER=cat systemctl --no-pager show "$SERVICE" -p MainPID --value 2>/dev/null)"

  echo "SERVICE_STATE=$ACTIVE"
  echo "OLD_PID=$OLD_PID"
  echo "NEW_PID=$NEW_PID"

  [ "$ACTIVE" = "active" ] || { echo "DEPLOY_ABORT_NOT_ACTIVE"; return 1; }
  [ -n "$NEW_PID" ] || { echo "DEPLOY_ABORT_PID"; return 1; }
  [ "$NEW_PID" != "0" ] || { echo "DEPLOY_ABORT_PID"; return 1; }

  sudo ss -lntp 2>/dev/null | grep -E ":9020[[:space:]]" >/dev/null || {
    echo "DEPLOY_ABORT_9020_NOT_LISTENING"
    return 1
  }

  echo "DEPLOY_SERVICE_PROOF=PASS"
  return 0
}

main "$@"
