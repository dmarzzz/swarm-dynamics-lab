#!/usr/bin/env bash
# Push local results to the swarm hub. Sources hub creds from the agentops sops secret via /tmp/hub_env.sh
# (shadow's age key); never prints them. usage: ./hub_sync.sh [register|M0|M1|M2|pilot]
set -e
cd "$(dirname "$0")"
if [ ! -f /tmp/hub_env.sh ]; then echo "no /tmp/hub_env.sh (re-create from agentops secrets/hub.sops.env)"; exit 1; fi
source /tmp/hub_env.sh
export SWARM_SOURCE=shadow/sol-goal
case "${1:-all}" in
  register) python3 src/hub_push.py register ;;
  M0|M1|M2) python3 src/hub_push.py stage "$1" "results/local-$(echo $1 | tr A-Z a-z)" ;;
  pilot) python3 src/hub_push.py pilot results/pilot-mp ;;
  all) python3 src/hub_push.py register; for s in M0 M1 M2; do python3 src/hub_push.py stage $s results/local-$(echo $s | tr A-Z a-z); done; python3 src/hub_push.py pilot results/pilot-mp ;;
esac
