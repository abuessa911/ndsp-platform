#!/usr/bin/env bash
set +H

EVENT_TYPE="${1:-decision_complete}"
PAYLOAD="${2:-{}}"
ENV_FILE="$HOME/empire-core-new/backend/services/ndsp-telegram-notifications-v176/.env"
URL="https://my.ndsp.app/api/telegram/events"

if [ ! -f "$ENV_FILE" ]; then
  echo "ENV_NOT_FOUND=$ENV_FILE"
else
  SECRET="$(sed -n 's/^NDSP_TELEGRAM_INTERNAL_SECRET=//p' "$ENV_FILE" | tail -n 1)"
  BODY="$(python3 - "$EVENT_TYPE" "$PAYLOAD" <<'PY'
import json
import sys
try:
    payload=json.loads(sys.argv[2])
except Exception:
    payload={"message":sys.argv[2]}
print(json.dumps({"event_type":sys.argv[1],"payload":payload},ensure_ascii=False,separators=(",",":")))
PY
)"
  SIGNATURE="$(python3 - "$SECRET" "$BODY" <<'PY'
import hashlib
import hmac
import sys
print("sha256="+hmac.new(sys.argv[1].encode(),sys.argv[2].encode(),hashlib.sha256).hexdigest())
PY
)"
  curl -ksS \
    -H 'Content-Type: application/json' \
    -H "X-NDSP-Telegram-Signature: $SIGNATURE" \
    -X POST \
    --data "$BODY" \
    "$URL"
  echo
fi

echo "SSH_SESSION_OPEN=YES"
