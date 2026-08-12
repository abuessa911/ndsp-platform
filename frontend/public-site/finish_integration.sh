#!/usr/bin/env bash
set -euo pipefail
TARGET_DIR="$HOME/empire-core-new/frontend/public-site"
cd "$TARGET_DIR"

if [ -f "index.html" ]; then
  sed -i 's/src="\/ndsp-live-trial-counters.js/type="module" src="\/ndsp-live-trial-counters.js/g' index.html
fi

npm run build
