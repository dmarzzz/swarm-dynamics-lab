#!/usr/bin/env bash
# Real-model pilot MP: one process per cell, all sharing results/spend-ledger.json (hard cap USD 5 in src/model.py).
# usage: ./run_pilot.sh [model] ; logs in results/pilot-mp/<cell>.log
set -e
cd "$(dirname "$0")"
MODEL="${1:-openai/gpt-4o-mini}"
OUT=results/pilot-mp
mkdir -p "$OUT"
COMMON='"n_agents":16,"entrench_rounds":5,"takeover_max_rounds":60,"recovery_rounds":40,"eval_round":30'
i=0
for MEM in "1" "full" "mix:1/full@0.5" "mix:1/full@0.75" "mix:1/full@0.875"; do
  i=$((i+1))
  CELLS="[{\"world\":\"W1_INSIDE\",\"dose\":0.5,\"memory\":\"$MEM\",\"tasks\":\"0-5\",\"seeds\":[1],\"arms\":[\"A0_no_purge\",\"A1_purge\",\"A2_purge_wipe\"],\"cfg_overrides\":{$COMMON}}]"
  CFG="{\"model\":\"$MODEL\",\"max_cost_usd\":5,\"concurrency\":8,\"input_usd_per_million\":0.15,\"output_usd_per_million\":0.6,\"timeout\":60,\"call_log\":\"$OUT/calls-$i.jsonl\"}"
  SWARM_MODEL_CONFIG="$CFG" nohup python3 -u src/worker.py --pilot "$OUT" --backend http --pilot-cells "$CELLS" > "$OUT/cell-$i.log" 2>&1 &
  echo "started cell $i ($MEM) pid $!"
done
