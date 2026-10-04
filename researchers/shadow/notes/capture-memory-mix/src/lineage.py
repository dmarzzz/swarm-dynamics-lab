#!/usr/bin/env python3
"""Attempt lineage and record selection for pilot episode files (added 2026-10-04 by shadow/sol-cm2, CORRECTIONS.md).

Episode files are append-only. A resumed worker re-runs every (task, seed) episode that does not already have all arms
valid, so one episode can have several ATTEMPTS in the file. An attempt is a maximal consecutive group of records for
one (memory, task, seed) with distinct arms; a repeated arm starts a new attempt.

Selection rule (episode level, outcome-blind, arms stay paired): the LAST attempt whose arms are all valid; if no
attempt is fully valid, the last attempt, whose invalid arms are then counted as invalid. On the saved MP, MP2 and MP3
records this selects exactly the same records as the per-arm "keep the last valid record" dedup that analyze.py used
before (check: `python3 src/lineage.py --check results/pilot-mp3`), so no published number changes from the rule
itself; what changes is that the rule and its accounting are now stated and printed.

    python3 src/lineage.py results/pilot-mp3                 # per-cell lineage table (markdown)
    python3 src/lineage.py --check results/pilot-mp results/pilot-mp2 results/pilot-mp3
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def read_records(d: Path, pattern: str = "MP_*.jsonl") -> list:
    out = []
    for f in sorted(Path(d).glob(pattern)):
        for i, l in enumerate(f.read_text().splitlines()):
            if l.strip():
                r = json.loads(l)
                r["_file"], r["_line"] = f.name, i
                out.append(r)
    return out


def attempts(records: list) -> dict:
    """(world, dose, memory, task, seed) -> [attempt, ...], attempt = [record, ...] in file order."""
    att = defaultdict(list)
    for r in records:
        k = (r["world"], r["dose"], r["memory"], r["task_id"], r["seed"])
        if not att[k] or r["arm"] in {x["arm"] for x in att[k][-1]}:
            att[k].append([])
        att[k][-1].append(r)
    return att


def select(records: list, policy: str = "last") -> tuple:
    """Return (selected records, lineage stats). policy 'last' (default, the published rule) or 'first' (sensitivity:
    the FIRST fully valid attempt)."""
    att = attempts(records)
    sel, stats = [], defaultdict(Counter)
    for k, v in att.items():
        cell = k[:3]
        full = [a for a in v if all(x["validity"]["ok"] for x in a)]
        chosen = (full[-1] if policy == "last" else full[0]) if full else v[-1]
        sel += chosen
        s = stats[cell]
        s["episodes"] += 1
        s["raw_records"] += sum(len(a) for a in v)
        s["raw_invalid"] += sum(not x["validity"]["ok"] for a in v for x in a)
        s["attempts"] += len(v)
        s["episodes_rerun"] += len(v) > 1
        s["episodes_fully_valid"] += bool(full)
        s["episodes_multi_valid"] += len(full) > 1
        s["selected_records"] += len(chosen)
        s["selected_invalid"] += sum(not x["validity"]["ok"] for x in chosen)
        s["superseded_records"] += sum(len(a) for a in v) - len(chosen)
    return sel, stats


def legacy_select(records: list) -> list:
    """The pre-correction analyze.py rule: per (cell, task, seed, arm) keep the last valid record, else the last."""
    by = {}
    for r in records:
        k = (r["world"], r["dose"], r["memory"], r["task_id"], r["seed"], r["arm"])
        if k in by and by[k]["validity"]["ok"] and not r["validity"]["ok"]:
            continue
        by[k] = r
    return list(by.values())


def lineage_table(stats: dict) -> list:
    cols = ["episodes", "attempts", "episodes_rerun", "episodes_multi_valid", "raw_records", "raw_invalid",
            "superseded_records", "selected_records", "selected_invalid"]
    L = ["| world | dose | memory | " + " | ".join(c.replace("_", " ") for c in cols) + " |",
         "|---|---|---|" + "---|" * len(cols)]
    tot = Counter()
    for cell in sorted(stats, key=str):
        s = stats[cell]
        tot.update(s)
        L.append(f"| {cell[0]} | {cell[1]} | {cell[2]} | " + " | ".join(str(s[c]) for c in cols) + " |")
    L.append("| **total** | | | " + " | ".join(f"**{tot[c]}**" for c in cols) + " |")
    return L


def sensitivity(recs: list) -> list:
    """A1_purge captured mean frac_T and recovered count per cell under policy 'last' vs 'first'."""
    out = []
    res = {}
    for pol in ("last", "first"):
        sel, _ = select(recs, pol)
        by = defaultdict(list)
        for r in sel:
            if r["arm"] == "A1_purge" and r["validity"]["ok"] and r["evaluation"]["captured"]:
                by[r["memory"]].append(r["evaluation"])
        res[pol] = by
    out.append("| memory | n | mean frac_T (last) | mean frac_T (first) | recovered (last) | recovered (first) |")
    out.append("|---|---|---|---|---|---|")
    for m in sorted(res["last"]):
        a, b = res["last"][m], res["first"][m]
        out.append(f"| {m} | {len(a)} | {sum(x['frac_original_T'] for x in a) / len(a):.3f} | "
                   f"{sum(x['frac_original_T'] for x in b) / len(b):.3f} | {sum(x['recovered'] for x in a)} | {sum(x['recovered'] for x in b)} |")
    return out


def main():
    args = sys.argv[1:]
    if args and args[0] == "--sensitivity":
        for d in args[1:]:
            print(f"## {d}\n")
            print("\n".join(sensitivity(read_records(Path(d)))))
        return
    check = args and args[0] == "--check"
    for d in args[1:] if check else args:
        recs = read_records(Path(d))
        sel, stats = select(recs)
        if check:
            a = {(r["_file"], r["_line"]) for r in sel}
            b = {(r["_file"], r["_line"]) for r in legacy_select(recs)}
            print(f"{d}: raw {len(recs)}, selected {len(sel)}, legacy-selected {len(b)}, identical: {a == b}")
        else:
            print(f"## {d}\n")
            print("\n".join(lineage_table(stats)))


if __name__ == "__main__":
    main()
