#!/usr/bin/env bash
# Pilot-only analyses (fast): MP (gpt-4o-mini), MP2 (gemma), figure. Prints the key A1/A2 rows.
cd "$(dirname "$0")"
python3 src/analyze.py --stage MP --local results/pilot-mp > /dev/null
python3 src/analyze.py --stage MP --name MP2 --local results/pilot-mp2 > /dev/null
[ -d results/pilot-mp3 ] && python3 src/analyze.py --stage MP --name MP3 --local results/pilot-mp3 > /dev/null
python3 src/figure.py
for f in MP MP2 MP3; do
  echo "== $f"; sed -n 3p results/$f.md | cut -c1-200
  grep -E "^\| W1_INSIDE \| 0.5 \| (1|full|mix:1/full@0\.[0-9]+) \| A[12]" results/$f.md | cut -c1-170
done
