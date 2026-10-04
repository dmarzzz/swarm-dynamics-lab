#!/usr/bin/env python3
"""Analysis for capture-memory-mix: per-cell table over f, the declared primary (delta_original at f = 0.5 vs 0),
the rescue threshold, the wipe bridge per f, and per-kind (short / long) traces.

    python3 src/analyze.py --stage M1 --local results/local-m1
    python3 src/analyze.py --stage MP --local results/pilot-mp          # real-model pilot, same tables

Unit = episode; cluster = task; contrasts paired per (task, seed) draw; 95% CI = percentile bootstrap over tasks.
Writes results/<stage>.md and results/<stage>_cells.csv.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import ROOT, load  # noqa: E402


def mean(xs):
    xs = [x for x in xs if x is not None and x == x]
    return sum(xs) / len(xs) if xs else float("nan")


def boot_ci(by_task: dict, n_boot=2000, seed=7):
    tasks = list(by_task)
    if not tasks:
        return float("nan"), float("nan")
    r = random.Random(seed)
    stats = sorted(mean([by_task[r.choice(tasks)] for _ in tasks]) for _ in range(n_boot))
    return stats[int(0.025 * n_boot)], stats[int(0.975 * n_boot) - 1]


def ci_of(vals_by_task: dict) -> str:
    lo, hi = boot_ci(vals_by_task)
    return f"[{lo:+.3f}, {hi:+.3f}]"


def read_local(d: Path) -> list:
    eps = []
    for f in sorted(d.glob("*.jsonl")):
        eps += [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
    return eps


def fkey(mem: str) -> float:
    return float(mem.split("@")[1]) if mem.startswith("mix:") else (-1.0 if mem == "full" else -2.0 - 1.0 / (1 + int(mem)))


def family(mem: str) -> str:
    return mem.split("@")[0] if mem.startswith("mix:") else mem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="M1")
    ap.add_argument("--local", required=True)
    a = ap.parse_args()
    d = load("design.yaml")
    eps = [e for e in read_local(Path(a.local)) if e.get("stage") == a.stage]
    if not eps:
        sys.exit(f"no {a.stage} episodes")
    arms = sorted({e["arm"] for e in eps}, key=d["arms"].index)
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    backends = sorted({e.get("backend") for e in eps})
    spend = sum(e["cost_actual"].get("cost_usd", 0.0) for e in eps if e["arm"] == arms[-1])
    calls = sum(e["cost_actual"].get("model_calls", 0) for e in eps)

    cells = defaultdict(lambda: defaultdict(list))
    invalid = defaultdict(int)
    for e in eps:
        key = (e["world"], e["dose"], e["memory"])
        if e["validity"]["ok"]:
            cells[key][e["arm"]].append(e)
        else:
            invalid[(key, e["arm"])] += 1

    rows = []
    for (world, dose, mem), by_arm in sorted(cells.items(), key=lambda kv: (kv[0][0], kv[0][1], family(kv[0][2]), fkey(kv[0][2]))):
        for arm in arms:
            xs = by_arm.get(arm, [])
            ev = [x["evaluation"] for x in xs]
            cap = [x for x in ev if x["captured"]]
            rows.append({"world": world, "dose": dose, "memory": mem, "f": (fkey(mem) if mem.startswith("mix:") else ""),
                         "arm": arm, "episodes": len(xs), "tasks": len({x["task_id"] for x in xs}),
                         "invalid": invalid[((world, dose, mem), arm)],
                         "captured": round(mean([x["captured"] for x in ev]), 4),
                         "capture_latency_med": _median([x["capture_latency"] for x in cap]),
                         "frac_at_removal_c": round(mean([x["frac_original_at_removal"] for x in cap]), 4),
                         "frac_T_c": round(mean([x["frac_original_T"] for x in cap]), 4),
                         "delta_c": round(mean([x["delta_original"] for x in cap]), 4),
                         "short_T_c": round(mean([x["short_T"] for x in cap]), 4),
                         "long_T_c": round(mean([x["long_T"] for x in cap]), 4),
                         "delta_long_c": round(mean([x["delta_long"] for x in cap]), 4),
                         "recovered_c": round(mean([x["recovered"] for x in cap]), 4),
                         "half_time_med": _median([x["half_time"] for x in cap if x["half_time"] is not None])})
    with open(out / f"{a.stage}_cells.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    L = [f"# capture-memory-mix: {a.stage} results", "",
         f"{len(eps)} episode records, backends {backends}, {calls} model calls, provider-reported spend {spend:.4f} USD. "
         + ("Scripted policy: these numbers describe the tanh rule in sim.py, not LLM agents. " if backends == ["scripted"] else "")
         + f"Code commits: {sorted({str(e.get('code')) for e in eps})}.", "",
         "Columns: captured = capture rate (shared by arms); frac@rem / frac_T = honest fraction on the original at removal "
         "and 50 rounds later (captured episodes); delta = frac_T minus frac@rem (0 = frozen, > 0 = returning); short_T / long_T = "
         "the same at round T split by memory kind; delta_long = return among the long-memory agents only.", "",
         "## Cells (captured episodes unless noted)", "",
         "| world | dose | memory | arm | n | inv | captured | lat | frac@rem | frac_T | delta | short_T | long_T | delta_long | recovered | half-time |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['world']} | {r['dose']} | {r['memory']} | {r['arm']} | {r['episodes']} | {r['invalid']} | {r['captured']:.2f} | "
                 f"{r['capture_latency_med']} | {r['frac_at_removal_c']:.3f} | {r['frac_T_c']:.3f} | {r['delta_c']:+.3f} | "
                 f"{r['short_T_c']:.3f} | {r['long_T_c']:.3f} | {r['delta_long_c']:+.3f} | {r['recovered_c']:.2f} | {r['half_time_med']} |")

    # ---- paired contrasts over f within a family (same world, dose, short/long), arm A1 and A2, vs f = 0
    pc = d["primary_contrast"]
    L += ["", "## Contrasts over the short-memory fraction f (paired per draw, vs f = 0 of the same family; captured under both)", "",
          f"Declared primary: {pc['stage']}, {pc['world']}, arm {pc['arm']}, metric {pc['metric']}, family mix:{pc['mix']['short']}/{pc['mix']['long']} "
          f"at dose {pc['mix']['dose']}, f = {pc['compare_f'][0]} minus f = {pc['compare_f'][1]}. Everything else is exploratory.", "",
          "| world | dose | family | arm | metric | f | mean(f) | mean(f=0) | diff | 95% CI | tasks | pairs |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    fams = sorted({(w, dd, family(m)) for (w, dd, m) in cells if m.startswith("mix:")})
    rescue = {}
    for world, dose, fam in fams:
        base = cells.get((world, dose, f"{fam}@0"), {})
        fs = sorted({fkey(m) for (w, dd, m) in cells if (w, dd, family(m)) == (world, dose, fam)})
        for arm in arms:
            if arm == "A0_no_purge":
                continue
            for metric in [pc["metric"]] + pc["secondary"]:
                for f in fs:
                    if f == 0:
                        continue
                    A = {(e["task_id"], e["seed"]): e["evaluation"] for e in cells[(world, dose, f"{fam}@{f:g}")].get(arm, [])}
                    B = {(e["task_id"], e["seed"]): e["evaluation"] for e in base.get(arm, [])}
                    common = [k for k in A if k in B and A[k]["captured"] and B[k]["captured"]
                              and A[k][metric] is not None and B[k][metric] is not None]
                    if not common:
                        continue
                    by_task = defaultdict(list)
                    for k in common:
                        by_task[k[0]].append(float(A[k][metric]) - float(B[k][metric]))
                    by_task = {t: mean(v) for t, v in by_task.items()}
                    lo, hi = boot_ci(by_task)
                    is_p = (a.stage == pc["stage"] and world == pc["world"] and arm == pc["arm"] and metric == pc["metric"]
                            and fam == f"mix:{pc['mix']['short']}/{pc['mix']['long']}" and dose == pc["mix"]["dose"] and f == pc["compare_f"][0])
                    L.append(f"| {'**PRIMARY** ' if is_p else ''}{world} | {dose} | {fam} | {arm} | {metric} | {f:g} | "
                             f"{mean([A[k][metric] for k in common]):.3f} | {mean([B[k][metric] for k in common]):.3f} | "
                             f"{mean(list(by_task.values())):+.3f} | [{lo:+.3f}, {hi:+.3f}] | {len(by_task)} | {len(common)} |")
                    if metric == pc["metric"] and arm == "A1_purge":
                        mA = mean([A[k][metric] for k in common])
                        loA, _ = boot_ci({t: mean([A[k][metric] for k in common if k[0] == t]) for t in by_task})
                        if (world, dose, fam) not in rescue and mA > 0.10 and loA > 0:
                            rescue[(world, dose, fam)] = (f, mA, loA)

    L += ["", "### Rescue threshold (design: smallest f with delta_original under A1_purge > +0.10 and CI lower bound > 0)", "",
          "| world | dose | family | f* | delta at f* | CI lower |", "|---|---|---|---|---|---|"]
    for world, dose, fam in fams:
        r = rescue.get((world, dose, fam))
        L.append(f"| {world} | {dose} | {fam} | {r[0]:g} | {r[1]:+.3f} | {r[2]:+.3f} |" if r else f"| {world} | {dose} | {fam} | none on grid | | |")

    # ---- wipe bridge per cell
    L += ["", "## Wipe bridge: A2_purge_wipe minus A1_purge on frac_original_T, per cell (captured episodes, paired)", "",
          "| world | dose | memory | mean wipe | mean purge | diff | 95% CI | tasks |", "|---|---|---|---|---|---|---|---|"]
    for (world, dose, mem), by_arm in sorted(cells.items(), key=lambda kv: (kv[0][0], kv[0][1], family(kv[0][2]), fkey(kv[0][2]))):
        A = {(e["task_id"], e["seed"]): e["evaluation"] for e in by_arm.get("A2_purge_wipe", [])}
        B = {(e["task_id"], e["seed"]): e["evaluation"] for e in by_arm.get("A1_purge", [])}
        common = [k for k in A if k in B and A[k]["captured"]]
        if not common:
            continue
        by_task = defaultdict(list)
        for k in common:
            by_task[k[0]].append(A[k]["frac_original_T"] - B[k]["frac_original_T"])
        by_task = {t: mean(v) for t, v in by_task.items()}
        lo, hi = boot_ci(by_task)
        L.append(f"| {world} | {dose} | {mem} | {mean([A[k]['frac_original_T'] for k in common]):.3f} | "
                 f"{mean([B[k]['frac_original_T'] for k in common]):.3f} | {mean(list(by_task.values())):+.3f} | [{lo:+.3f}, {hi:+.3f}] | {len(by_task)} |")

    # ---- mean post-removal traces per cell (A1), coarse
    L += ["", "## Mean honest fraction on the original after removal, A1_purge, captured episodes (rounds 1, 5, 10, 20, 30, 50, 80 after removal)", "",
          "| world | dose | memory | r1 | r5 | r10 | r20 | r30 | r50 | r80 | long r50 | short r50 |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for (world, dose, mem), by_arm in sorted(cells.items(), key=lambda kv: (kv[0][0], kv[0][1], family(kv[0][2]), fkey(kv[0][2]))):
        xs = [x for x in by_arm.get("A1_purge", []) if x["evaluation"]["captured"]]
        if not xs:
            continue
        def at(i, key="series_original"):
            return mean([x["trajectory"][key][x["trajectory"]["removal_round"] + i - 1]
                         for x in xs if len(x["trajectory"][key]) >= x["trajectory"]["removal_round"] + i])
        R = sorted({x["cfg"]["recovery_rounds"] for x in xs})[0]
        pts = [i for i in (1, 5, 10, 20, 30, 50, 80) if i <= R]
        L.append(f"| {world} | {dose} | {mem} | " + " | ".join(f"{at(i):.3f}" for i in pts) + " |" * (7 - len(pts))
                 + f" | {at(min(50, R), 'series_long'):.3f} | {at(min(50, R), 'series_short'):.3f} |")

    L += ["", "Invalid episodes per cell and arm are in the CSV; none are dropped or retried. Capture is decided before removal and shared by the arms."]
    (out / f"{a.stage}.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


def _median(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


if __name__ == "__main__":
    main()
