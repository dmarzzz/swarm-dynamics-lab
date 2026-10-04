#!/usr/bin/env python3
"""Per-cell distribution of frac_original_T under A1_purge (captured episodes): the pilot outcomes are bimodal, so the
mean hides it. Prints sorted values per memory spec, for one or more pilot dirs."""
import json, sys
from collections import defaultdict
from pathlib import Path
for d in sys.argv[1:]:
    print(f"== {d}")
    by = defaultdict(list)
    for f in sorted(Path(d).glob("MP_*.jsonl")):
        for l in f.read_text().splitlines():
            e = json.loads(l)
            if e["arm"] == "A1_purge" and e["validity"]["ok"] and e["evaluation"]["captured"]:
                by[e["memory"]].append((e["task_id"], e["evaluation"]["frac_original_T"], e["evaluation"]["frac_original_end"], e["evaluation"]["recovered"]))
    def k(m):
        return (float(m.split("@")[1]) if m.startswith("mix") else (-1 if m == "full" else 2))
    for m in sorted(by, key=k):
        xs = sorted(by[m], key=lambda t: t[1])
        vals = " ".join(f"{v:.2f}" for _, v, _, _ in xs)
        ends = " ".join(f"{v:.2f}" for _, _, v, _ in sorted(xs, key=lambda t: t[2]))
        print(f"  {m:18s} n={len(xs):2d} T30: {vals}")
        print(f"  {'':18s}       T40: {ends}   recovered {sum(r for *_, r in xs)}/{len(xs)}")
