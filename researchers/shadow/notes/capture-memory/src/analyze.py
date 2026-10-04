#!/usr/bin/env python3
"""Analysis: per-cell table and the declared primary contrast, from local episodes or the hub.

    python3 src/analyze.py --stage S1 --local results/local-s1        # read *.jsonl in a directory
    python3 src/analyze.py --stage S1 [--no-upload]                    # pull finished runs from the hub

Unit = episode (one arm, one memory, one task x seed draw). Cluster = task. Contrasts are paired per task x seed
because every arm and every memory length ran on the same draws. CIs are a percentile bootstrap over whole
tasks (2000 resamples). The primary contrast (design.yaml) is frac_original_T under A1_purge, memory 20
minus memory 1, in W1_INSIDE at dose 0.42, restricted to episodes captured under both memory lengths.
Invalid episodes are counted per cell and never dropped silently. Writes results/<stage>.md and
results/<stage>_cells.csv, and (hub mode) attaches them to run `<exp>/analysis-<stage>`.
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
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else float("nan")


def boot_ci(by_task: dict, n_boot=2000, seed=7):
    tasks = list(by_task)
    if not tasks:
        return float("nan"), float("nan")
    r = random.Random(seed)
    stats = sorted(mean([by_task[r.choice(tasks)] for _ in tasks]) for _ in range(n_boot))
    return stats[int(0.025 * n_boot)], stats[int(0.975 * n_boot) - 1]


def read_local(d: Path) -> list:
    eps = []
    for f in sorted(d.glob("*.jsonl")):
        eps += [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
    return eps


def fetch_hub(exp: str, stage: str) -> list:
    import swarm_report as sr
    cache = ROOT / "results" / "pulled"
    cache.mkdir(parents=True, exist_ok=True)
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
        eps += [json.loads(l) for l in local.read_text().splitlines() if l.strip()]
    return eps


def mkey(m):
    return (0, int(m)) if str(m) != "full" else (1, 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="S1")
    ap.add_argument("--local", help="directory of episode jsonl files (skips the hub)")
    ap.add_argument("--no-upload", action="store_true")
    a = ap.parse_args()
    exp, d = load("experiment.yaml")["id"], load("design.yaml")
    eps = read_local(Path(a.local)) if a.local else fetch_hub(exp, a.stage)
    eps = [e for e in eps if e.get("stage") == a.stage]
    if not eps:
        sys.exit(f"no {a.stage} episodes")
    arms = d["arms"]
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    backends = sorted({e.get("backend") for e in eps})

    # ---- per cell (world, dose, memory) per arm
    cells = defaultdict(lambda: defaultdict(list))
    invalid = defaultdict(int)
    for e in eps:
        key = (e["world"], e["dose"], str(e["memory"]))
        if e["validity"]["ok"]:
            cells[key][e["arm"]].append(e)
        else:
            invalid[(key, e["arm"])] += 1
    rows = []
    for (world, dose, memory), by_arm in sorted(cells.items(), key=lambda kv: (kv[0][0], kv[0][1], mkey(kv[0][2]))):
        for arm in arms:
            xs = by_arm.get(arm, [])
            ev = [x["evaluation"] for x in xs]
            cap = [x for x in ev if x["captured"]]
            rows.append({"world": world, "dose": dose, "memory": memory, "arm": arm, "episodes": len(xs),
                         "tasks": len({x["task_id"] for x in xs}), "invalid": invalid[((world, dose, memory), arm)],
                         "captured": round(mean([x["captured"] for x in ev]), 4),
                         "capture_latency_med": _median([x["capture_latency"] for x in cap]),
                         "frac_original_T": round(mean([x["frac_original_T"] for x in ev]), 4),
                         "frac_original_T_captured": round(mean([x["frac_original_T"] for x in cap]), 4),
                         "recovered": round(mean([x["recovered"] for x in ev]), 4),
                         "recovered_captured": round(mean([x["recovered"] for x in cap]), 4),
                         "half_time_med": _median([x["half_time"] for x in cap if x["half_time"] is not None]),
                         "entrench_frac_original": round(mean([x["entrench_frac_original"] for x in ev]), 4)})
    with open(out / f"{a.stage}_cells.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    lines = [f"# {exp}: {a.stage} results", "",
             f"{len(eps)} episode records, backends {backends}. "
             + ("Scripted policy: these numbers describe the tanh rule in sim.py, not LLM agents. " if backends == ["scripted"] else "")
             + f"Code commits: {sorted({str(e.get('code')) for e in eps})}.", "",
             "## Cells", "",
             "| world | dose | memory | arm | n | invalid | captured | lat | frac_orig_T (all / captured) | recovered (all / captured) | half-time |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['world']} | {r['dose']} | {r['memory']} | {r['arm']} | {r['episodes']} | {r['invalid']} | "
                     f"{r['captured']:.2f} | {r['capture_latency_med']} | {r['frac_original_T']:.3f} / {r['frac_original_T_captured']:.3f} | "
                     f"{r['recovered']:.3f} / {r['recovered_captured']:.3f} | {r['half_time_med']} |")

    # ---- primary contrast: memory a vs memory b, same arm, same world/dose, captured under both
    pc = d["primary_contrast"]
    m_hi, m_lo = (str(m) for m in pc["compare_memory"])
    lines += ["", "## Memory contrasts (paired per task x seed, cluster bootstrap over tasks)", "",
              f"Declared primary: stage {pc['stage']}, {pc['world']} dose {pc['dose']}, arm {pc['arm']}, "
              f"{pc['metric']}, memory {m_hi} minus memory {m_lo}, episodes captured under both. Everything else is exploratory.", "",
              "| cell | arm | metric | memory pair | mean a | mean b | diff (a - b) | 95% CI | tasks | n pairs |",
              "|---|---|---|---|---|---|---|---|---|---|"]
    primary_line = None
    worlds_doses = sorted({(k[0], k[1]) for k in cells if k[0] != "W0_CLEAN"})
    mems = sorted({k[2] for k in cells}, key=mkey)
    for world, dose in worlds_doses:
        for arm in arms:
            for metric in [pc["metric"]] + pc["secondary"]:
                for ma, mb in [(m_hi, m_lo)] + [(m, "1") for m in mems if m not in ("1", m_hi)]:
                    A = {(e["task_id"], e["seed"]): e["evaluation"] for e in cells[(world, dose, ma)].get(arm, [])}
                    B = {(e["task_id"], e["seed"]): e["evaluation"] for e in cells[(world, dose, mb)].get(arm, [])}
                    common = [k for k in A if k in B and A[k]["captured"] and B[k]["captured"]]
                    if not common:
                        continue
                    vals = [(A[k][metric], B[k][metric]) for k in common]
                    vals = [(x, y) for x, y in vals if x is not None and y is not None]
                    if not vals:
                        continue
                    by_task = defaultdict(list)
                    for k, (x, y) in zip([k for k in common if A[k][metric] is not None and B[k][metric] is not None], vals):
                        by_task[k[0]].append(float(x) - float(y))
                    by_task = {t: mean(v) for t, v in by_task.items()}
                    lo, hi = boot_ci(by_task)
                    is_primary = (a.stage == pc["stage"] and world == pc["world"] and dose == pc["dose"]
                                  and arm == pc["arm"] and metric == pc["metric"] and (ma, mb) == (m_hi, m_lo))
                    line = (f"| {'**PRIMARY** ' if is_primary else ''}{world} dose {dose} | {arm} | {metric} | {ma} vs {mb} | "
                            f"{mean([x for x, _ in vals]):.3f} | {mean([y for _, y in vals]):.3f} | {mean(list(by_task.values())):+.3f} | "
                            f"[{lo:+.3f}, {hi:+.3f}] | {len(by_task)} | {len(vals)} |")
                    lines.append(line)
                    if is_primary:
                        primary_line = line

    # ---- bridge: A2 wipe minus A1 purge, per memory (same draws)
    br = pc["bridge"]
    t_arm, c_arm = br["arms"]
    lines += ["", f"## Bridge to vishesh's repair arms: {t_arm} minus {c_arm}, per memory (exploratory)", "",
              "| cell | memory | metric | mean wipe | mean purge | diff | 95% CI | tasks |", "|---|---|---|---|---|---|---|---|"]
    for world, dose in worlds_doses:
        for m in mems:
            A = {(e["task_id"], e["seed"]): e["evaluation"] for e in cells[(world, dose, m)].get(t_arm, [])}
            B = {(e["task_id"], e["seed"]): e["evaluation"] for e in cells[(world, dose, m)].get(c_arm, [])}
            common = [k for k in A if k in B and A[k]["captured"]]
            if not common:
                continue
            by_task = defaultdict(list)
            for k in common:
                by_task[k[0]].append(A[k][br["metric"]] - B[k][br["metric"]])
            by_task = {t: mean(v) for t, v in by_task.items()}
            lo, hi = boot_ci(by_task)
            lines.append(f"| {world} dose {dose} | {m} | {br['metric']} | {mean([A[k][br['metric']] for k in common]):.3f} | "
                         f"{mean([B[k][br['metric']] for k in common]):.3f} | {mean(list(by_task.values())):+.3f} | [{lo:+.3f}, {hi:+.3f}] | {len(by_task)} |")

    lines += ["", "Invalid episodes per cell and arm are in the CSV; none are dropped or retried.",
              "Capture is decided before removal and shared by all arms of an episode, so 'captured' is the same across arms of a cell.",
              "Everything except the PRIMARY row is exploratory."]
    if a.stage == pc["stage"] and not primary_line:
        lines.insert(2, "**The declared primary cell has no captured pairs yet.**")
    (out / f"{a.stage}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

    if not a.local and not a.no_upload:
        import swarm_report as sr
        run = sr.start(exp, run=f"{exp}/analysis-{a.stage}", params={"stage": a.stage, "kind": "analysis"},
                       message=f"analysis of {len(eps)} episode records")
        for f in [f"{a.stage}.md", f"{a.stage}_cells.csv"]:
            run.artifact(out / f, f)
        run.done(message=(primary_line or "exploratory stage").replace("|", " ").strip())
        print(f"attached to hub run {exp}/analysis-{a.stage}")


def _median(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


if __name__ == "__main__":
    main()
