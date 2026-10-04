#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
: "${SWARM_SOURCE:?Set the registered researcher/agent identity}"
study="${1:?Choose external-influence or immune-response}"
exec python3 src/runner.py "$study" work --backend "${SWARM_BACKEND:-scripted}"
