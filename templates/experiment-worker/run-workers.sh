#!/usr/bin/env bash
# Start one worker per core (or N) in a tmux session on this server. Claim the server first (README step 4).
#   SWARM_SOURCE=vishesh/codex-1 ./run-workers.sh [N]
#   tmux attach -t workers            # watch;  tmux kill-session -t workers   # stop
set -euo pipefail
cd "$(dirname "$0")"
: "${SWARM_SOURCE:?set SWARM_SOURCE=<you>/<tool>-<n>}"
N=${1:-$(nproc)}
tmux has-session -t workers 2>/dev/null && { echo "tmux session 'workers' already running"; exit 1; }
tmux new-session -d -s workers -n w1 "SWARM_SOURCE=$SWARM_SOURCE-w1 python3 src/worker.py --forever; read"
for i in $(seq 2 "$N"); do
  tmux new-window -t workers -n "w$i" "SWARM_SOURCE=$SWARM_SOURCE-w$i python3 src/worker.py --forever; read"
done
echo "started $N workers in tmux session 'workers' as $SWARM_SOURCE-w1..w$N"
