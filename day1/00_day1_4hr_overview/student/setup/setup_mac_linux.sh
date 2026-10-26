#!/usr/bin/env bash
# One-time setup for macOS and Linux. Run from the repo root:   bash setup/setup_mac_linux.sh
set -euo pipefail
cd "$(dirname "$0")/.."

echo "▶ Creating .venv with Python 3.11"
if command -v uv >/dev/null 2>&1; then
  uv venv --python 3.11 .venv                       # uv downloads Python 3.11 if you do not have it
  VIRTUAL_ENV="$PWD/.venv" uv pip install -r requirements.txt
else
  PY=""
  for candidate in python3.11 python3.12 python3; do
    if command -v "$candidate" >/dev/null 2>&1 &&
       "$candidate" -c 'import sys; sys.exit(sys.version_info[:2] not in ((3, 11), (3, 12)))'; then
      PY="$candidate"; break
    fi
  done
  if [ -z "$PY" ]; then
    echo "✖ Python 3.11 not found. Easiest fix, then run this script again:"
    echo "    curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  (or install Python 3.11 from https://www.python.org/downloads/)"
    exit 1
  fi
  "$PY" -m venv .venv
  .venv/bin/python -m pip install --upgrade pip
  .venv/bin/python -m pip install -r requirements.txt
fi

echo "▶ Checking the environment"
.venv/bin/python setup/check_env.py || true
echo
echo "Next time, start with:"
echo "    source .venv/bin/activate"
echo "    jupyter lab"
