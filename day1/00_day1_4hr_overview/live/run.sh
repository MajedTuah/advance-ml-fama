#!/usr/bin/env bash
# Start the Day 1 live session. Uses the repo's .venv (Homebrew Python refuses global pip installs).
set -euo pipefail
LIVE_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$LIVE_DIR/../../.." && pwd)"
VENV="$REPO/.venv"

if [ ! -x "$VENV/bin/python" ]; then
  echo "Creating virtualenv at $VENV"
  python3 -m venv "$VENV"
fi
if ! "$VENV/bin/python" -c "import fastapi, uvicorn, segno" 2>/dev/null; then
  echo "Installing live server packages into $VENV"
  "$VENV/bin/python" -m pip install -q -r "$LIVE_DIR/requirements.txt"
fi
exec "$VENV/bin/python" -u "$LIVE_DIR/server.py"
