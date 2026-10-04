#!/usr/bin/env bash
set -euo pipefail
source /tmp/hub_env.sh
export SWARM_SOURCE=shadow/sol-factory
python3 "$(dirname "$0")/closeout.py" "${1:-hub}"
