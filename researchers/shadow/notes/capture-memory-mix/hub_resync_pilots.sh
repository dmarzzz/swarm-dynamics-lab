#!/usr/bin/env bash
# Re-push the corrected pilot summaries + tables to the hub (CORRECTIONS.md C4). Creds via /tmp/hub_env.sh, never printed.
set -e
cd "$(dirname "$0")"
source /tmp/hub_env.sh
export SWARM_SOURCE=shadow/sol-cm2
python3 src/hub_push.py pilot results/pilot-mp MP gpt-4o-mini
python3 src/hub_push.py pilot results/pilot-mp2 MP2 gemma-3-27b-it
python3 src/hub_push.py pilot results/pilot-mp3 MP3 qwen3-235b
