#!/usr/bin/env bash
set -Eeuo pipefail

cd /home/nawaf511/empire-core-new

echo "NDSP STRUCTURE"
echo "=============="
find apps packages backend/app scripts docs deployment -maxdepth 3 -type d 2>/dev/null | sort
