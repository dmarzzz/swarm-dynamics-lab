#!/usr/bin/env bash
# Start one worker per core (or N) in a tmux session on this server. Claim the server first (README step 5).
#   SWARM_SOURCE=vishesh/codex-1 ./run-workers.sh [N]          # start
#   SWARM_SOURCE=vishesh/codex-1 ./run-workers.sh [N] --at-boot  # also restart them after a reboot (crontab)
#   tmux attach -t workers            # watch;  tmux kill-session -t workers   # stop (and: crontab -e to drop --at-boot)
#
# Each worker restarts itself 10 s after it exits or crashes. If a worker or the whole box dies mid-run,
# the hub puts that run back in the queue after 20 min of silence, so another worker re-runs it.
set -euo pipefail
cd "$(dirname "$0")"
: "${SWARM_SOURCE:?set SWARM_SOURCE=<you>/<tool>-<n>}"
N=$(nproc); AT_BOOT=0
for a in "$@"; do case $a in --at-boot) AT_BOOT=1 ;; *) N=$a ;; esac; done
tmux has-session -t workers 2>/dev/null && { echo "tmux session 'workers' already running"; exit 1; }
loop() { echo "while true; do SWARM_SOURCE=$SWARM_SOURCE-w$1 python3 src/worker.py --forever; echo \"worker exited (\$?); restarting in 10s\"; sleep 10; done"; }
tmux new-session -d -s workers -n w1 "$(loop 1)"
for i in $(seq 2 "$N"); do tmux new-window -t workers -n "w$i" "$(loop "$i")"; done
echo "started $N self-restarting workers in tmux session 'workers' as $SWARM_SOURCE-w1..w$N"
if [ "$AT_BOOT" = 1 ]; then
  line="@reboot cd $PWD && SWARM_SOURCE=$SWARM_SOURCE PYTHONPATH=/usr/local/lib/swarm $PWD/run-workers.sh $N"
  (crontab -l 2>/dev/null | grep -vF "$PWD/run-workers.sh"; echo "$line") | crontab -
  echo "installed @reboot entry (crontab -l to see it)"
fi
