#!/usr/bin/env python3
"""Per-episode table for the pilot: one line per (memory, task, arm)."""
import json, sys
from pathlib import Path
d = Path(sys.argv[1] if len(sys.argv) > 1 else "results/pilot-mp")
rows = []
for f in sorted(d.glob("MP_*.jsonl")):
    for l in f.read_text().splitlines():
        e = json.loads(l)
        ev, tr = e["evaluation"], e["trajectory"]
        if not e["validity"]["ok"]:
            rows.append((e["memory"], e["task_id"], e["arm"], "INVALID " + e["validity"].get("error", "")))
            continue
        rows.append((e["memory"], e["task_id"], e["arm"],
                     f"cap={int(ev['captured'])} lat={ev['capture_latency']} rem={ev['frac_original_at_removal']:.3f} "
                     f"T={ev['frac_original_T']:.3f} end={ev['frac_original_end']:.3f} short_T={ev['short_T']} long_T={ev['long_T']} "
                     f"rec={int(ev['recovered'])} half={ev['half_time']} calls={e['cost_actual']['model_calls']} usd={e['cost_actual']['cost_usd']:.4f}"))
for r in rows:
    print(f"{r[0]:18s} task {r[1]} {r[2]:14s} {r[3]}")
