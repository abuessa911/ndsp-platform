#!/usr/bin/env bash
set -Eeuo pipefail
set +H
umask 077

OUTPUT="${1:-$HOME/.config/ndsp-backup/backup-passphrase.txt}"
mkdir -p "$(dirname "$OUTPUT")"

if [ -e "$OUTPUT" ]; then
  echo "ERROR: passphrase file already exists: $OUTPUT" >&2
  echo "Move it or choose another path. It will not be overwritten." >&2
  exit 1
fi

read -r -s -p "Enter a new NDSP backup passphrase (minimum 20 characters): " P1
echo
read -r -s -p "Confirm the passphrase: " P2
echo

if [ "$P1" != "$P2" ]; then
  echo "ERROR: passphrases do not match." >&2
  exit 1
fi

if [ "${#P1}" -lt 20 ]; then
  echo "ERROR: passphrase must contain at least 20 characters." >&2
  exit 1
fi

printf '%s' "$P1" > "$OUTPUT"
unset P1 P2
chmod 600 "$OUTPUT"

ACTUAL_MODE="$(stat -c '%a' "$OUTPUT")"
[ "$ACTUAL_MODE" = "600" ] || { echo "ERROR: passphrase file mode is not 600." >&2; exit 1; }

echo "============================================================"
echo "NDSP BACKUP PASSPHRASE FILE CREATED"
echo "PATH=$OUTPUT"
echo "MODE=$ACTUAL_MODE"
echo "IMPORTANT=Copy this passphrase securely off the server. Do not place it inside the project or backup directory."
echo "FINAL_STATUS=NDSP_BACKUP_PASSPHRASE_CREATED_OK"
echo "============================================================"
