#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
: "${SWARM_SOURCE:?Set the registered agent id}"
# One bounded worker; no background provider process and no automatic restart.
python3 src/worker.py --hub
