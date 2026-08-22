#!/usr/bin/env bash

main() {
  ROOT="/home/nawaf511/empire-core-v5-1-1-clean"
  PY="$ROOT/apps/ndsp-layers-api/.venv/bin/python"
  SERVICE="ndsp-layers-api.service"

  echo "VERIFY: source files"
  [ -f "$ROOT/apps/ndsp-layers-api/app.py" ] || { echo "DEPLOY_ABORT_APP_MISSING"; return 1; }
  [ -f "$ROOT/apps/ndsp-layers-api/canonical_runtime.py" ] || { echo "DEPLOY_ABORT_RUNTIME_MISSING"; return 1; }
  [ -x "$PY" ] || { echo "DEPLOY_ABORT_PYTHON_MISSING"; return 1; }

  echo "VERIFY: syntax"
  "$PY" -m py_compile "$ROOT/apps/ndsp-layers-api/app.py" "$ROOT/apps/ndsp-layers-api/canonical_runtime.py" || {
    echo "DEPLOY_ABORT_SYNTAX_FAILED"
    return 1
  }

  echo "VERIFY: canonical tests"
  cd "$ROOT" || { echo "DEPLOY_ABORT_ROOT_CD_FAILED"; return 1; }
  "$PY" -m unittest discover -s backend/layers/canonical_v1/tests -p "test_*.py" || {
    echo "DEPLOY_ABORT_CANONICAL_TESTS_FAILED"
    return 1
  }

  echo "VERIFY: API compatibility tests"
  cd "$ROOT/apps/ndsp-layers-api" || { echo "DEPLOY_ABORT_API_CD_FAILED"; return 1; }
  "$PY" -m unittest test_canonical_routes.py test_canonical_runtime.py || {
    echo "DEPLOY_ABORT_API_TESTS_FAILED"
    return 1
  }

  EXEC_START="$(SYSTEMD_PAGER=cat systemctl --no-pager show "$SERVICE" -p ExecStart --value 2>/dev/null)"
  case "$EXEC_START" in
    *"$ROOT/apps/ndsp-layers-api/.venv/bin/uvicorn"*) ;;
    *) echo "DEPLOY_ABORT_SERVICE_BINDING_MISMATCH"; return 1 ;;
  esac

  OLD_PID="$(SYSTEMD_PAGER=cat systemctl --no-pager show "$SERVICE" -p MainPID --value 2>/dev/null)"

  echo "ACTIVATE: $SERVICE"
  sudo systemctl restart "$SERVICE" || {
    echo "DEPLOY_ABORT_RESTART_FAILED"
    return 1
  }

  sleep 2

  ACTIVE="$(SYSTEMD_PAGER=cat systemctl --no-pager is-active "$SERVICE" 2>/dev/null)"
  NEW_PID="$(SYSTEMD_PAGER=cat systemctl --no-pager show "$SERVICE" -p MainPID --value 2>/dev/null)"

  echo "SERVICE_STATE=$ACTIVE"
  echo "OLD_PID=$OLD_PID"
  echo "NEW_PID=$NEW_PID"

  [ "$ACTIVE" = "active" ] || { echo "DEPLOY_ABORT_SERVICE_NOT_ACTIVE"; return 1; }
  [ -n "$NEW_PID" ] || { echo "DEPLOY_ABORT_NO_PID"; return 1; }
  [ "$NEW_PID" != "0" ] || { echo "DEPLOY_ABORT_NO_PID"; return 1; }

  echo "PROOF: local compatibility endpoint"
  curl -fsS --max-time 20 http://127.0.0.1:9065/api/admin/layers/run | "$PY" -c "import json,sys; d=json.load(sys.stdin); ok=d.get(\"ok\") is True and d.get(\"total_layers_expected\")==16 and d.get(\"total_layers_executed\")==16 and d.get(\"total_errors\")==0; print(\"ok =\", d.get(\"ok\")); print(\"expected =\", d.get(\"total_layers_expected\")); print(\"executed =\", d.get(\"total_layers_executed\")); print(\"errors =\", d.get(\"total_errors\")); print(\"state =\", d.get(\"single_truth_state\")); print(\"A_LOCAL_PROOF=\" + (\"PASS\" if ok else \"FAIL\")); raise SystemExit(0 if ok else 1)" || {
    echo "DEPLOY_ABORT_LOCAL_PROOF_FAILED"
    return 1
  }

  echo "DEPLOY_NDSP_LAYERS_API=PASS"
  return 0
}

main "$@"
