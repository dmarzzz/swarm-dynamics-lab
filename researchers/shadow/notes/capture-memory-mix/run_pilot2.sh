#!/usr/bin/env bash
# Second-model pilot (sample mode, no logprobs): gemma-3-27b-it. One process per cell, shared ledger + hard cap.
# usage: ./run_pilot2.sh [model] [tasks] [mems...]
set -e
cd "$(dirname "$0")"
MODEL="${1:-google/gemma-3-27b-it}"
TASKS="${2:-0-5}"
shift 2 2>/dev/null || true
MEMS=("$@")
[ ${#MEMS[@]} -eq 0 ] && MEMS=("1" "full" "mix:1/full@0.5" "mix:1/full@0.75" "mix:1/full@0.875")
OUT=results/pilot-mp2
mkdir -p "$OUT"
COMMON='"n_agents":16,"entrench_rounds":5,"takeover_max_rounds":60,"recovery_rounds":40,"eval_round":30'
for MEM in "${MEMS[@]}"; do
  TAG=$(echo "$MEM" | sed 's#[/:@]#-#g')
  CELLS="[{\"world\":\"W1_INSIDE\",\"dose\":0.5,\"memory\":\"$MEM\",\"tasks\":\"$TASKS\",\"seeds\":[1],\"arms\":[\"A0_no_purge\",\"A1_purge\",\"A2_purge_wipe\"],\"cfg_overrides\":{$COMMON}}]"
  CFG="{\"model\":\"$MODEL\",\"max_cost_usd\":10,\"concurrency\":8,\"input_usd_per_million\":0.1,\"output_usd_per_million\":0.5,\"timeout\":90,\"mode\":\"sample\",\"call_log\":\"$OUT/calls-$TAG.jsonl\"}"
  SWARM_MODEL_CONFIG="$CFG" setsid nohup python3 -u src/worker.py --pilot "$OUT" --backend http --pilot-cells "$CELLS" > "$OUT/cell-$TAG.log" 2>&1 < /dev/null &
  echo "started cell $MEM tasks $TASKS pid $!"
done
