#!/usr/bin/env bash
# Own-result publication using the pre-existing local hub environment; never print it.
set -euo pipefail
if [[ ! -f /tmp/hub_env.sh ]]; then
  echo 'BLOCKED: existing /tmp/hub_env.sh unavailable; no hub write attempted' >&2
  exit 2
fi
source /tmp/hub_env.sh
export SWARM_SOURCE=shadow/sol-halflife
# Set this to your sanctioned agentops checkout when reproducing publication.
export PYTHONPATH="${SWARM_REPORT_CLIENT_DIR:-$HOME/projects/swarm-labs-agentops/hub}${PYTHONPATH:+:$PYTHONPATH}"
exec python3 "$(dirname "$0")/publish_hub.py"
