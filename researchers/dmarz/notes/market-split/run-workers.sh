#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
: "${SWARM_SOURCE:?set SWARM_SOURCE to your registered agent ID}"
# One finite process. Do not start one worker per core or poll forever.
exec python3 src/worker.py
