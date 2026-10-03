#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
: "${SWARM_SOURCE:?set SWARM_SOURCE to researcher/agent}"
# One bounded worker; do not spawn one paid API worker per CPU.
exec python3 src/worker.py --hub --backend "${SWARM_BACKEND:-scripted}"
