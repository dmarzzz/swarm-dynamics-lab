#!/usr/bin/env python3
"""Rebuild each pilot cell's <cell>.summary.json from the SELECTED records (lineage.select) with the fixed capture-rate
formula in worker.metrics (CORRECTIONS.md C4), so the hub's per-cell metrics stop reporting an impossible capture
fraction and carry the retry accounting. Params are preserved; the pre-correction summaries are in git history (commit e10201d2).

    python3 src/resummarize.py results/pilot-mp results/pilot-mp2 results/pilot-mp3
    then re-sync the hub: src/hub_push.py pilot <dir> <stage> <model-tag>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import lineage  # noqa: E402
from worker import metrics  # noqa: E402


def main():
    for d in map(Path, sys.argv[1:]):
        for f in sorted(d.glob("MP_*.jsonl")):
            summ = f.with_suffix(".summary.json")
            old = json.loads(summ.read_text()) if summ.exists() else {}
            raw = lineage.read_records(f.parent, f.name)
            sel, lin = lineage.select(raw)
            arms = old.get("params", {}).get("arms") or sorted({r["arm"] for r in raw})
            stats = {a: {"n": 0, "captured": 0, "frac_T": 0.0, "delta": 0.0, "invalid": 0, "calls": 0, "usd": 0.0} for a in arms}
            for r in sel:
                a = stats[r["arm"]]
                if r["validity"]["ok"]:
                    e = r["evaluation"]
                    a["n"] += 1; a["captured"] += e["captured"]; a["frac_T"] += e["frac_original_T"]; a["delta"] += e["delta_original"]
                else:
                    a["invalid"] += 1
            # cost_actual counters are cumulative over an episode's arms: the last arm of an attempt holds the attempt total
            att = lineage.attempts(raw)
            sel_ids = {(r["_file"], r["_line"]) for r in sel}
            calls_sel = calls_all = usd_sel = usd_all = 0
            for v in att.values():
                for at in v:
                    last = at[-1]["cost_actual"]
                    calls_all += last["model_calls"]; usd_all += last.get("cost_usd", 0.0)
                    if (at[-1]["_file"], at[-1]["_line"]) in sel_ids:
                        calls_sel += last["model_calls"]; usd_sel += last.get("cost_usd", 0.0)
            m = metrics(stats)
            for a in stats.values():   # per-arm call/usd split is not recoverable (counters are cumulative per attempt)
                a.pop("calls", None); a.pop("usd", None)
            ls = next(iter(lin.values()))
            m.update({"model_calls": calls_sel, "cost_usd": round(usd_sel, 4),
                      "model_calls_all_attempts": calls_all, "cost_usd_all_attempts": round(usd_all, 4),
                      "raw_records": ls["raw_records"], "raw_invalid": ls["raw_invalid"],
                      "superseded_records": ls["superseded_records"], "episodes_rerun": ls["episodes_rerun"],
                      "attempts": ls["attempts"], "selected_records": ls["selected_records"],
                      "selected_valid": ls["selected_valid"], "first_observed_valid": ls["first_observed_valid"]})
            new = {**old, "stats": stats, "metrics": m, "selection": "lineage.select: last fully valid attempt per episode, else last attempt",
                   "corrected": "2026-10-04 shadow/sol-cm2, CORRECTIONS.md"}
            summ.write_text(json.dumps(new, indent=2))
            print(f"{f.name}: captured {old.get('metrics', {}).get('captured')} -> {m['captured']}, "
                  f"episodes {old.get('metrics', {}).get('episodes')} -> {m['episodes']}, invalid {old.get('metrics', {}).get('invalid')} -> {m['invalid']}, "
                  f"superseded {m['superseded_records']}")


if __name__ == "__main__":
    main()
