#!/usr/bin/env bash
# Re-run every local analysis (scripted stages + pilots if present). Writes results/<stage>.md and _cells.csv + figure.
set -e
cd "$(dirname "$0")"
for st in M0 M1 M2; do
  d=results/local-$(echo $st | tr A-Z a-z)
  [ -d $d ] && python3 src/analyze.py --stage $st --local $d > /dev/null
done
[ -d results/pilot-mp ] && python3 src/analyze.py --stage MP --local results/pilot-mp > /dev/null
[ -d results/pilot-mp2 ] && python3 src/analyze.py --stage MP --name MP2 --local results/pilot-mp2 > /dev/null
[ -d results/pilot-mp3 ] && python3 src/analyze.py --stage MP --name MP3 --local results/pilot-mp3 > /dev/null
python3 src/figure.py
ls -la results/*.md results/*.svg
