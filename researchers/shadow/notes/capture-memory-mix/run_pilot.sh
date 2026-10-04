#!/usr/bin/env bash
# Real-model pilot MP: one process per cell, all sharing results/spend-ledger.json (hard cap in src/model.py).
# Resumable: completed (task, seed) episodes in an existing cell file are skipped.
# usage: ./run_pilot.sh [model] [tasks] [fractions...] ; logs in results/pilot-mp/cell-<mem>.log
set -e
cd "$(dirname "$0")"
MODEL="${1:-openai/gpt-4o-mini}"
TASKS="${2:-0-5}"
shift 2 2>/dev/null || true
MEMS=("$@")
[ ${#MEMS[@]} -eq 0 ] && MEMS=("1" "full" "mix:1/full@0.5" "mix:1/full@0.75" "mix:1/full@0.875")
OUT=results/pilot-mp
mkdir -p "$OUT"
COMMON='"n_agents":16,"entrench_rounds":5,"takeover_max_rounds":60,"recovery_rounds":40,"eval_round":30'
for MEM in "${MEMS[@]}"; do
  TAG=$(echo "$MEM" | sed 's#[/:@]#-#g')
  CELLS="[{\"world\":\"W1_INSIDE\",\"dose\":0.5,\"memory\":\"$MEM\",\"tasks\":\"$TASKS\",\"seeds\":[1],\"arms\":[\"A0_no_purge\",\"A1_purge\",\"A2_purge_wipe\"],\"cfg_overrides\":{$COMMON}}]"
  CFG="{\"model\":\"$MODEL\",\"max_cost_usd\":10,\"concurrency\":8,\"input_usd_per_million\":0.15,\"output_usd_per_million\":0.6,\"timeout\":60,\"call_log\":\"$OUT/calls-$TAG.jsonl\"}"
  SWARM_MODEL_CONFIG="$CFG" nohup python3 -u src/worker.py --pilot "$OUT" --backend http --pilot-cells "$CELLS" > "$OUT/cell-$TAG.log" 2>&1 &
  echo "started cell $MEM tasks $TASKS pid $!"
done
