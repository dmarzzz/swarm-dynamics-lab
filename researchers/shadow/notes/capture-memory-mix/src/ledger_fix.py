#!/usr/bin/env python3
"""One-off repair 05:59Z: a `git stash` with live workers reverted results/spend-ledger.json to the committed value
(0.34099172 / 15940 calls) while workers kept adding to it. Restore = stashed value + increments since the revert.
Everything is recorded here so the ledger stays auditable. Run once; refuses if already applied."""
import fcntl, json, sys
from pathlib import Path
p = Path(__file__).resolve().parent.parent / "results" / "spend-ledger.json"
stashed = {"spent_usd": 0.64846812, "calls": 30905, "by_model": {
    "meta-llama/llama-3.1-8b-instruct": {"usd": 0.00125912, "calls": 398},
    "openai/gpt-4o-mini": {"usd": 0.6321702, "calls": 29148},
    "google/gemma-3-27b-it": {"usd": 0.01503879, "calls": 1359}}}
reverted_to = {"spent_usd": 0.34099172, "calls": 15940, "by_model": {
    "meta-llama/llama-3.1-8b-instruct": {"usd": 0.00125912, "calls": 398},
    "openai/gpt-4o-mini": {"usd": 0.3397326, "calls": 15542}}}
with open(p, "r+") as f:
    fcntl.flock(f, fcntl.LOCK_EX)
    cur = json.load(f)
    if cur.get("repaired_05_59Z"):
        sys.exit("already repaired")
    new = {"spent_usd": 0.0, "calls": 0, "by_model": {}, "repaired_05_59Z": True,
           "repair_note": "git stash reverted this file during live runs; restored as stashed + increments since revert (src/ledger_fix.py)"}
    for m in set(cur["by_model"]) | set(stashed["by_model"]):
        c, s, r = cur["by_model"].get(m, {"usd": 0, "calls": 0}), stashed["by_model"].get(m, {"usd": 0, "calls": 0}), reverted_to["by_model"].get(m, {"usd": 0, "calls": 0})
        new["by_model"][m] = {"usd": round(s["usd"] + (c["usd"] - r["usd"]), 8), "calls": s["calls"] + (c["calls"] - r["calls"])}
    new["spent_usd"] = round(sum(v["usd"] for v in new["by_model"].values()), 8)
    new["calls"] = sum(v["calls"] for v in new["by_model"].values())
    f.seek(0); f.truncate(); json.dump(new, f)
print(json.dumps(new))
