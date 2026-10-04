#!/usr/bin/env python3
"""Reconcile the local spend ledger against OpenRouter's account usage, which is the authoritative number.

Baseline: OpenRouter total_usage was 499.244934 USD when this goal started (03:50Z, before any call). Spend for the
goal = current total_usage - baseline. The local ledger is set to max(ledger, that), per-model shares kept
proportional, so the hard cap in src/model.py can never be lower than true spend. The key is read from the secrets
file inside this script; nothing is printed except the numbers.

    python3 src/ledger_sync.py
"""
import fcntl, json, os, urllib.request
from pathlib import Path

BASELINE = 499.244934
p = Path(__file__).resolve().parent.parent / "results" / "spend-ledger.json"
key = Path(os.path.expanduser("~/.moltbot/secrets/openrouter.key")).read_text().strip()
req = urllib.request.Request("https://openrouter.ai/api/v1/credits", headers={"Authorization": "Bearer " + key})
with urllib.request.urlopen(req, timeout=30) as r:
    usage = json.loads(r.read())["data"]["total_usage"]
true_spend = round(usage - BASELINE, 6)
with open(p, "r+") as f:
    fcntl.flock(f, fcntl.LOCK_EX)
    d = json.load(f)
    local = d["spent_usd"]
    if true_spend > local:
        scale = true_spend / local if local > 0 else 1.0
        for m in d["by_model"].values():
            m["usd"] = round(m["usd"] * scale, 8)
        d["spent_usd"] = true_spend
        d["synced_to_openrouter"] = {"usage": usage, "baseline": BASELINE, "was_local": local}
        f.seek(0); f.truncate(); json.dump(d, f)
print(json.dumps({"openrouter_usage": usage, "goal_spend_true": true_spend, "ledger_before": local, "ledger_now": d["spent_usd"]}))
