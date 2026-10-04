#!/usr/bin/env bash
# Re-run every local analysis (scripted stages + pilot if present). Writes results/<stage>.md and _cells.csv.
set -e
cd "$(dirname "$0")"
for st in M0 M1 M2; do
  [ -d results/local-$(echo $st | tr A-Z a-z) ] && python3 src/analyze.py --stage $st --local results/local-$(echo $st | tr A-Z a-z) > /dev/null
done
[ -d results/pilot-mp ] && python3 src/analyze.py --stage MP --local results/pilot-mp > /dev/null
ls -la results/*.md
