#!/usr/bin/env bash
# Pilot run 2: finish tasks 0-5 on the five run-1 cells (resume skips done episodes), extend all cells to tasks 0-11,
# add f=5/8 and f=15/16. Detached from the calling shell.
cd "$(dirname "$0")"
setsid nohup ./run_pilot.sh openai/gpt-4o-mini 0-11 "1" "full" "mix:1/full@0.5" "mix:1/full@0.625" "mix:1/full@0.75" "mix:1/full@0.875" "mix:1/full@0.9375" > results/pilot-mp/launch_run2.log 2>&1 < /dev/null &
sleep 2
cat results/pilot-mp/launch_run2.log
