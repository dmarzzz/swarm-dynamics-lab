#!/usr/bin/env python3
"""Analysis: pull every finished run's episodes from the hub, then report per cell and the primary contrast.

    python3 src/analyze.py [--stage S2] [--no-upload]

Follows the design rules: the episode is the unit, the task is the cluster. Arm contrasts are paired
per task (same draws). CIs come from a bootstrap over whole task clusters. The paired binary primary
outcome also gets an exact McNemar test on the first seed of each task (one pair per cluster, so the
pairs are independent). Invalid episodes are counted per arm and never dropped silently. Writes
results/<stage>.md, results/<stage>_cells.csv and, if matplotlib is available, results/<stage>_tradeoff.png,
then attaches them to the hub run `<exp>/analysis-<stage>`.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
try:
    import swarm_report as sr
except ImportError:
    sys.exit("swarm_report not found: run on a fleet server, or copy hub/swarm_report.py from swarm-labs-agentops")
import yaml


def fetch(exp: str, stage: str) -> list:
    cache = ROOT / "results" / "pulled"
    eps = []
    for r in sr.runs(exp, status="done", limit=5000):
        if r["params"].get("stage") != stage or r["params"].get("kind") == "analysis":
            continue
        local = cache / (r["run"].replace("/", "__") + ".jsonl")
        if not local.exists():
            art = next((a for a in sr.get_run(r["run"])["artifacts"] if a["name"] == "episodes.jsonl"), None)
            if not art:
                print(f"warning: {r['run']} is done but has no episodes.jsonl")
                continue
            sr.download(art["url"], local)
        eps += [json.loads(line) for line in local.read_text().splitlines() if line.strip()]
    return eps


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def cluster_bootstrap(diff_by_task: dict, n_boot=2000, seed=7):
    """95% CI for the mean of per-task mean differences, resampling whole tasks."""
    tasks = list(diff_by_task)
    r = random.Random(seed)
    stats = sorted(mean([diff_by_task[r.choice(tasks)] for _ in tasks]) for _ in range(n_boot))
    return stats[int(0.025 * n_boot)], stats[int(0.975 * n_boot) - 1]


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact McNemar p-value from discordant counts b, c."""
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    p = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * p)


def value(e, metric):
    if metric == "delay":
        return e["decision"]["delay"]
    return float(e["evaluation"][metric])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="S2")
    ap.add_argument("--no-upload", action="store_true")
    a = ap.parse_args()
    exp = yaml.safe_load((ROOT / "experiment.yaml").read_text())["id"]
    d = yaml.safe_load((ROOT / "design.yaml").read_text())
    eps = fetch(exp, a.stage)
    if not eps:
        sys.exit(f"no finished {a.stage} episodes on the hub for {exp}")
    arms = d["arms"]
    out = ROOT / "results"
    out.mkdir(exist_ok=True)

    # ---- per cell, per arm
    cells = defaultdict(lambda: defaultdict(list))
    invalid = defaultdict(int)
    for e in eps:
        key = (e["world"], e["dose"])
        if e["validity"]["ok"]:
            cells[key][e["arm"]].append(e)
        else:
            invalid[(key, e["arm"])] += 1
    rows = []
    for (world, dose), by_arm in sorted(cells.items()):
        for arm in arms:
            xs = by_arm.get(arm, [])
            rows.append({"world": world, "dose": dose, "arm": arm, "episodes": len(xs),
                         "tasks": len({x["task_id"] for x in xs}), "invalid": invalid[((world, dose), arm)],
                         "commit": round(mean([x["evaluation"]["committed"] for x in xs]), 4),
                         "false_commit": round(mean([x["evaluation"]["false_commit"] for x in xs]), 4),
                         "correct": round(mean([x["evaluation"]["correct"] for x in xs]), 4),
                         "delay": round(mean([x["decision"]["delay"] for x in xs]), 3),
                         "regret": round(mean([x["evaluation"]["regret"] for x in xs]), 4)})
    with open(out / f"{a.stage}_cells.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # ---- paired contrasts in every cell (the declared one is primary, the rest exploratory)
    pc = d["primary_contrast"]
    treat, ctrl = pc["compare"]
    lines = [f"# {exp}: {a.stage} results", "",
             f"{len(eps)} episode records from the hub ({len({e['run'] for e in eps})} runs). "
             f"Pre-registration commit: {sorted({str(e.get('prereg')) for e in eps})}.", "",
             f"Contrast = {treat} - {ctrl}, paired per task; 95% CI from a bootstrap over task clusters (2000 resamples). "
             "McNemar: exact, first seed per task.", "",
             "| cell | metric | " + " | ".join(arms) + f" | diff | 95% CI | McNemar p | tasks |",
             "|---|---|" + "---|" * len(arms) + "---|---|---|---|"]
    primary_line = None
    for (world, dose), by_arm in sorted(cells.items()):
        for metric in [pc["metric"]] + pc["secondary"]:
            per = {arm: defaultdict(dict) for arm in arms}
            for arm in arms:
                for e in by_arm.get(arm, []):
                    per[arm][e["task_id"]][e["seed"]] = value(e, metric)
            common = [t for t in per[treat] if t in per[ctrl]]
            diff_by_task = {t: mean([per[treat][t][s] - per[ctrl][t][s] for s in per[treat][t] if s in per[ctrl][t]])
                            for t in common}
            if not diff_by_task:
                continue
            lo, hi = cluster_bootstrap(diff_by_task)
            p = ""
            if metric == pc["metric"]:
                b = c = 0
                for t in common:
                    s0 = min(per[treat][t])
                    x, y = per[treat][t][s0], per[ctrl][t].get(s0)
                    b += (x == 1 and y == 0)
                    c += (x == 0 and y == 1)
                p = f"{mcnemar_exact(b, c):.2g} ({b}/{c})"
            is_primary = (a.stage == pc["stage"] and world == pc["world"] and dose == pc["dose"] and metric == pc["metric"])
            means = " | ".join(f"{mean([value(e, metric) for e in by_arm.get(arm, [])]):.3f}" for arm in arms)
            line = (f"| {'**PRIMARY** ' if is_primary else ''}{world} dose {dose} | {metric} | {means} | "
                    f"{mean(list(diff_by_task.values())):+.3f} | [{lo:+.3f}, {hi:+.3f}] | {p} | {len(common)} |")
            lines.append(line)
            if is_primary:
                primary_line = line
    lines += ["", "Invalid episodes per cell/arm are in the CSV (`invalid`); none are dropped or retried.",
              "Everything except the PRIMARY row is exploratory."]
    if a.stage == pc["stage"] and not primary_line:
        lines.insert(2, "**The pre-registered primary cell has no data yet.**")
    (out / f"{a.stage}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

    # ---- figure: false commits vs delay per arm (the speed-accuracy tradeoff), one point per cell
    fig = None
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=150)
        for arm, marker in zip(arms, "os^v"):
            pts = [r for r in rows if r["arm"] == arm]
            ax.scatter([r["delay"] for r in pts], [r["false_commit"] for r in pts], marker=marker, label=arm)
            for r in pts:
                ax.annotate(f"{r['world'][:2]} {r['dose']}", (r["delay"], r["false_commit"]), fontsize=7,
                            xytext=(4, 2), textcoords="offset points")
        ax.set_xlabel("mean delay (reports until commit)")
        ax.set_ylabel("false-commit rate")
        ax.set_title(f"{exp} {a.stage}: false commits vs delay, per cell")
        ax.legend(frameon=False)
        ax.spines[["top", "right"]].set_visible(False)
        fig.tight_layout()
        fig.savefig(out / f"{a.stage}_tradeoff.png")
    except ImportError:
        print("(matplotlib not installed: no figure; `uv run --with matplotlib --with pyyaml src/analyze.py`)")

    if not a.no_upload:
        run = sr.start(exp, run=f"{exp}/analysis-{a.stage}", params={"stage": a.stage, "kind": "analysis"},
                       message=f"analysis of {len(eps)} episode records")
        for f in [f"{a.stage}.md", f"{a.stage}_cells.csv"] + ([f"{a.stage}_tradeoff.png"] if fig else []):
            run.artifact(out / f, f)
        run.done(message=(primary_line or "exploratory stage").replace("|", " ").strip())
        print(f"attached to hub run {exp}/analysis-{a.stage}")


if __name__ == "__main__":
    main()
