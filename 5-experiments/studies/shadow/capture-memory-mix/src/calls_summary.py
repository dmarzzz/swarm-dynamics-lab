#!/usr/bin/env python3
"""Summarise the pilot's per-call log: the model's measured response P(original | window) by (window length bucket,
fraction of original in window), plus a per-round trace of mean P(original) per (task, arm, kind).

    python3 src/calls_summary.py results/pilot-mp/calls-*.jsonl
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


def main():
    rows = []
    for f in sys.argv[1:]:
        rows += [json.loads(l) for l in Path(f).read_text().splitlines() if l.strip()]
    rows = [r for r in rows if r.get("p_orig") is not None]
    print(f"{len(rows)} calls with usable two-word mass")

    # response curve by window length bucket x share of original
    def bucket(n):
        return "n=0" if n == 0 else "n=1" if n == 1 else "n=2-5" if n <= 5 else "n=6-15" if n <= 15 else "n=16-30" if n <= 30 else "n>30"
    curve = defaultdict(list)
    for r in rows:
        share = round(r["n_orig"] / r["n"], 1) if r["n"] else None
        curve[(bucket(r["n"]), share)].append(r["p_orig"])
    print("\nP(original | window): rows = window length, cols = share of original in window (count of calls in brackets)")
    shares = sorted({s for _, s in curve if s is not None})
    print("bucket   " + " ".join(f"{s:>12}" for s in shares) + "   empty")
    for b in ("n=0", "n=1", "n=2-5", "n=6-15", "n=16-30", "n>30"):
        cells = []
        for s in shares:
            xs = curve.get((b, s), [])
            cells.append(f"{sum(xs)/len(xs):.2f} ({len(xs):4d})" if xs else "      .     ")
        e = curve.get((b, None), [])
        print(f"{b:8s} " + " ".join(f"{c:>12}" for c in cells) + (f"   {sum(e)/len(e):.2f} ({len(e)})" if e else ""))

    # recency: for long windows, does the last-5 share predict better than the whole-window share?
    long = [r for r in rows if r["n"] >= 10]
    if long:
        by_last = defaultdict(list)
        for r in long:
            by_last[(round(r["n_orig"] / r["n"], 1), r["last5_orig"])].append(r["p_orig"])
        print("\nLong windows (n >= 10): P(original) by (whole-window share, originals in last 5)")
        for k in sorted(by_last):
            xs = by_last[k]
            if len(xs) >= 5:
                print(f"  share {k[0]:.1f}, last5 {k[1]}: {sum(xs)/len(xs):.2f} ({len(xs)})")

    # per-round mean P(original) per task/arm/kind, A1 only, compact
    tr = defaultdict(list)
    for r in rows:
        tr[(r["task"], r["arm"], r["kind"], r["round"])].append(r["p_orig"])
    print("\nMean P(original) per round, A1_purge, by task and kind (rounds after removal only shown every 5)")
    for task in sorted({k[0] for k in tr}):
        for kind in ("short", "long"):
            pts = sorted(k[3] for k in tr if k[0] == task and k[1] == "A1_purge" and k[2] == kind)
            if not pts:
                continue
            line = " ".join(f"r{rd}:{sum(tr[(task,'A1_purge',kind,rd)])/len(tr[(task,'A1_purge',kind,rd)]):.2f}" for rd in pts if rd % 5 == 0 or rd == pts[-1])
            print(f"  task {task} {kind:5s} {line}")


if __name__ == "__main__":
    main()
