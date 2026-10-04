#!/usr/bin/env bash
# One finite batch claimant; the worker owns the bounded two-thread API pool.
set -euo pipefail
cd "$(dirname "$0")"
exec python3 src/worker.py --hub
