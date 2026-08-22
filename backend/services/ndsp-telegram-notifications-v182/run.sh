#!/usr/bin/env bash
set +H
DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$DIR/server.py"
