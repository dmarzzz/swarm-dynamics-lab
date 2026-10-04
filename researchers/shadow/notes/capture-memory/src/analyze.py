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
    st = d["stages"].get(a.stage, {})
    arms = [x for x in d["arms"] if x in st.get("arms", d["arms"])]
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

    # ---- capture curves and the dose rule (any stage; the S1b sweep is what this is for)
    rule = d.get("dose_rule", {})
    H, target = rule.get("horizon", 200), rule.get("capture_target", 0.8)
    cap_T = max({int(e["cfg"]["takeover_max_rounds"]) for e in eps})
    horizons = sorted({h for h in (100, 200, 400) if h <= cap_T} | {cap_T})
    lines += ["", f"## Capture rate by dose and memory (within 100 / 200 / {cap_T} takeover rounds; 95% CI at H = {H} is a cluster bootstrap over tasks)", "",
              "Capture is decided before the intervention and is shared by the arms, so one row per cell (read from A1_purge). "
              f"Dose rule (design.yaml): per memory and world, the smallest grid dose with >= {target:.0%} captured within H = {H}.", "",
              "| world | memory | dose | k | n | " + " | ".join(f"cap<={h}" for h in horizons) + f" | 95% CI (H={H}) | median latency |",
              "|---|---|---|---|---|" + "---|" * len(horizons) + "---|---|"]
    curve = {}
    for (world, dose, memory), by_arm in sorted(cells.items(), key=lambda kv: (kv[0][0], mkey(kv[0][2]), kv[0][1])):
        if world == "W0_CLEAN":
            continue
        xs = by_arm.get(arms[1] if len(arms) > 1 else arms[0], []) or next(iter(by_arm.values()), [])
        if not xs:
            continue
        lat = [x["evaluation"]["capture_latency"] for x in xs]
        within = {h: mean([l is not None and l <= h for l in lat]) for h in horizons}
        by_task = defaultdict(list)
        for x in xs:
            l = x["evaluation"]["capture_latency"]
            by_task[x["task_id"]].append(1.0 if (l is not None and l <= H) else 0.0)
        lo, hi = boot_ci({t: mean(v) for t, v in by_task.items()})
        curve[(world, memory, dose)] = (within.get(H, float("nan")), lo, hi)
        lines.append(f"| {world} | {memory} | {dose} | {xs[0]['trajectory']['k']} | {len(xs)} | "
                     + " | ".join(f"{within[h]:.2f}" for h in horizons)
                     + f" | [{lo:.2f}, {hi:.2f}] | {_median([l for l in lat if l is not None])} |")
    lines += ["", f"### Dose rule applied: smallest dose with >= {target:.0%} captured within {H} rounds", "",
              "| world | memory | dose* | captured within H at dose* | 95% CI | note |", "|---|---|---|---|---|---|"]
    dose_table = {}
    for world in sorted({w for w, _, _ in curve}):
        for memory in sorted({m for w, m, _ in curve if w == world}, key=mkey):
            doses = sorted(dd for w, m, dd in curve if (w, m) == (world, memory))
            pick = next((dd for dd in doses if curve[(world, memory, dd)][0] >= target), None)
            dose_table.setdefault(world, {})[memory] = pick
            if pick is None:
                best = max(doses, key=lambda dd: curve[(world, memory, dd)][0]) if doses else None
                lines.append(f"| {world} | {memory} | none on grid | {curve[(world, memory, best)][0]:.2f} at {best} | "
                             f"[{curve[(world, memory, best)][1]:.2f}, {curve[(world, memory, best)][2]:.2f}] | not capturable at this horizon; excluded from removal contrasts |")
            else:
                p, lo, hi = curve[(world, memory, pick)]
                note = "CI lower bound also >= target" if lo >= target else "point estimate clears target, CI lower bound does not"
                lines.append(f"| {world} | {memory} | {pick} | {p:.2f} | [{lo:.2f}, {hi:.2f}] | {note} |")
    (out / f"{a.stage}_dose_rule.json").write_text(json.dumps({"horizon": H, "capture_target": target,
                                                              "takeover_cap": cap_T, "dose_by_world_memory": dose_table}, indent=2))

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

    # ---- per-memory-dose contrast: each memory at its own dose* (dose_rule), vs memory 1 at its dose*, same draws
    lines += ["", "## Memory contrasts at the per-memory dose (dose rule applied; exploratory, doses differ across the pair)", "",
              "| world | arm | metric | memory a @ dose* | memory b @ dose* | mean a | mean b | diff | 95% CI | tasks | n pairs |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for world, per_mem in sorted(dose_table.items()):
        base_m = "1"
        if per_mem.get(base_m) is None:
            continue
        for ma in [m for m in sorted(per_mem, key=mkey) if m != base_m and per_mem[m] is not None]:
            da, db = per_mem[ma], per_mem[base_m]
            for arm in arms:
                for metric in [pc["metric"]] + pc["secondary"]:
                    A = {(e["task_id"], e["seed"]): e["evaluation"] for e in cells[(world, da, ma)].get(arm, [])}
                    B = {(e["task_id"], e["seed"]): e["evaluation"] for e in cells[(world, db, base_m)].get(arm, [])}
                    common = [k for k in A if k in B and A[k]["captured"] and B[k]["captured"]
                              and A[k][metric] is not None and B[k][metric] is not None]
                    if not common:
                        continue
                    by_task = defaultdict(list)
                    for k in common:
                        by_task[k[0]].append(float(A[k][metric]) - float(B[k][metric]))
                    by_task = {t: mean(v) for t, v in by_task.items()}
                    lo, hi = boot_ci(by_task)
                    lines.append(f"| {world} | {arm} | {metric} | {ma} @ {da} | {base_m} @ {db} | "
                                 f"{mean([A[k][metric] for k in common]):.3f} | {mean([B[k][metric] for k in common]):.3f} | "
                                 f"{mean(list(by_task.values())):+.3f} | [{lo:+.3f}, {hi:+.3f}] | {len(by_task)} | {len(common)} |")

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

    # ---- pilot section: per-memory dose from the stage, A0 vs A1, delta_original, traces, cost (model stages)
    if st.get("doses_by_memory"):
        dbm = st["doses_by_memory"]
        H_T = int(next(iter(eps))["cfg"]["eval_round"])
        lines += ["", f"## Pilot summary: each memory at its own dose ({dbm}), {len({e['task_id'] for e in eps})} tasks, cluster bootstrap over tasks", "",
                  "Six tasks is a pilot, not a sample: the CIs below are percentile bootstraps over 6 clusters and are wide by construction. "
                  "Capture is shared by the arms of an episode. `delta_original` = frac_original_T minus frac_original_at_removal "
                  "(positive = came back, about zero = frozen, negative = kept sliding).", "",
                  "| memory | dose | k | n | invalid | captured | latency med | arm | frac_orig_T (captured) | 95% CI | delta_original | 95% CI | recovered |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        pilot = {}
        for memory in sorted(dbm, key=mkey):
            dose = dbm[memory]
            world = st["worlds"][0]
            by_arm = cells.get((world, dose, memory), {})
            for arm in arms:
                xs = by_arm.get(arm, [])
                cap = [x for x in xs if x["evaluation"]["captured"]]
                inv = invalid[((world, dose, memory), arm)]
                def bt(metric, pool):
                    by_task = defaultdict(list)
                    for x in pool:
                        by_task[x["task_id"]].append(float(x["evaluation"][metric]))
                    by_task = {t: mean(v) for t, v in by_task.items()}
                    return mean(list(by_task.values())), boot_ci(by_task)
                fT, (flo, fhi) = bt("frac_original_T", cap) if cap else (float("nan"), (float("nan"), float("nan")))
                dT, (dlo, dhi) = bt("delta_original", cap) if cap else (float("nan"), (float("nan"), float("nan")))
                pilot[(memory, arm)] = {"n": len(xs), "captured": len(cap), "frac_T": fT, "frac_T_ci": (flo, fhi), "delta": dT, "delta_ci": (dlo, dhi)}
                lat = _median([x["evaluation"]["capture_latency"] for x in cap])
                lines.append(f"| {memory} | {dose} | {xs[0]['trajectory']['k'] if xs else '-'} | {len(xs)} | {inv} | {len(cap)}/{len(xs)} | {lat} | {arm} | "
                             f"{fT:.3f} | [{flo:.2f}, {fhi:.2f}] | {dT:+.3f} | [{dlo:+.2f}, {dhi:+.2f}] | "
                             f"{mean([x['evaluation']['recovered'] for x in cap]) if cap else float('nan'):.2f} |")
        # A1 minus A0 per memory, paired per episode (same prefix)
        lines += ["", "### Purge effect, A1_purge minus A0_no_purge, paired per episode (same prefix), captured episodes", "",
                  "| memory | metric | A1 | A0 | diff | 95% CI | tasks |", "|---|---|---|---|---|---|---|"]
        for memory in sorted(dbm, key=mkey):
            dose, world = dbm[memory], st["worlds"][0]
            A = {(e["task_id"], e["seed"]): e["evaluation"] for e in cells.get((world, dose, memory), {}).get("A1_purge", [])}
            B = {(e["task_id"], e["seed"]): e["evaluation"] for e in cells.get((world, dose, memory), {}).get("A0_no_purge", [])}
            common = [k for k in A if k in B and A[k]["captured"]]
            for metric in ("frac_original_T", "delta_original"):
                if not common:
                    lines.append(f"| {memory} | {metric} | - | - | - | - | 0 |")
                    continue
                by_task = defaultdict(list)
                for k in common:
                    by_task[k[0]].append(float(A[k][metric]) - float(B[k][metric]))
                by_task = {t: mean(v) for t, v in by_task.items()}
                lo, hi = boot_ci(by_task)
                lines.append(f"| {memory} | {metric} | {mean([A[k][metric] for k in common]):.3f} | {mean([B[k][metric] for k in common]):.3f} | "
                             f"{mean(list(by_task.values())):+.3f} | [{lo:+.2f}, {hi:+.2f}] | {len(by_task)} |")
        # full minus memory 1 under A1 (different doses, same tasks: between-condition over task clusters)
        mems_p = sorted(dbm, key=mkey)
        if len(mems_p) == 2:
            m_lo, m_hi = mems_p
            lines += ["", f"### Memory contrast under A1_purge: memory {m_hi} @ {dbm[m_hi]} minus memory {m_lo} @ {dbm[m_lo]} (captured under both; doses differ, so this is the per-memory-dose comparison the dose rule calls for)", "",
                      "| metric | memory " + str(m_hi) + " | memory " + str(m_lo) + " | diff | 95% CI | tasks |", "|---|---|---|---|---|---|"]
            world = st["worlds"][0]
            A = {(e["task_id"], e["seed"]): e["evaluation"] for e in cells.get((world, dbm[m_hi], m_hi), {}).get("A1_purge", [])}
            B = {(e["task_id"], e["seed"]): e["evaluation"] for e in cells.get((world, dbm[m_lo], m_lo), {}).get("A1_purge", [])}
            common = [k for k in A if k in B and A[k]["captured"] and B[k]["captured"]]
            for metric in ("frac_original_T", "delta_original", "frac_original_at_removal"):
                if not common:
                    lines.append(f"| {metric} | - | - | - | - | 0 |")
                    continue
                by_task = defaultdict(list)
                for k in common:
                    by_task[k[0]].append(float(A[k][metric]) - float(B[k][metric]))
                by_task = {t: mean(v) for t, v in by_task.items()}
                lo, hi = boot_ci(by_task)
                lines.append(f"| {metric} | {mean([A[k][metric] for k in common]):.3f} | {mean([B[k][metric] for k in common]):.3f} | "
                             f"{mean(list(by_task.values())):+.3f} | [{lo:+.2f}, {hi:+.2f}] | {len(by_task)} |")
        # mean post-removal trace
        pts = [1, 2, 3, 5, 10, 20, 30, 40, H_T]
        lines += ["", "### Mean honest fraction on the original, by round after the intervention (captured episodes; round 0 = at removal)", "",
                  "| memory | arm | n | " + " | ".join(f"r{r}" for r in [0] + pts) + " |", "|---|---|---|" + "---|" * (len(pts) + 1)]
        for memory in sorted(dbm, key=mkey):
            dose, world = dbm[memory], st["worlds"][0]
            for arm in arms:
                xs = [x for x in cells.get((world, dose, memory), {}).get(arm, []) if x["evaluation"]["captured"]]
                if not xs:
                    continue
                vals = []
                for r in [0] + pts:
                    vals.append(mean([x["trajectory"]["series_original"][x["trajectory"]["removal_round"] - 1 + r]
                                      for x in xs if len(x["trajectory"]["series_original"]) > x["trajectory"]["removal_round"] - 1 + r]))
                lines.append(f"| {memory} | {arm} | {len(xs)} | " + " | ".join(f"{v:.2f}" for v in vals) + " |")
        # per-episode rows
        lines += ["", "### Per episode", "", "| task | words (orig / attack) | memory | captured | latency | frac at removal | A0 frac_T | A1 frac_T | A1 delta | calls (prefix + A0 + A1) | USD |", "|---|---|---|---|---|---|---|---|---|---|---|"]
        for memory in sorted(dbm, key=mkey):
            dose, world = dbm[memory], st["worlds"][0]
            by_arm = cells.get((world, dose, memory), {})
            A0 = {e["task_id"]: e for e in by_arm.get("A0_no_purge", [])}
            A1 = {e["task_id"]: e for e in by_arm.get("A1_purge", [])}
            for tid in sorted(set(A0) | set(A1)):
                e = A1.get(tid) or A0.get(tid)
                ev, tr = e["evaluation"], e["trajectory"]
                c0, c1 = (A0.get(tid) or {}).get("cost_actual", {}), (A1.get(tid) or {}).get("cost_actual", {})
                pre = e["cost_actual"].get("prefix", {})
                calls = pre.get("calls", 0) + c0.get("model_calls", 0) + c1.get("model_calls", 0)
                usd = pre.get("cost_usd", 0) + c0.get("cost_usd", 0) + c1.get("cost_usd", 0)
                lines.append(f"| {tid} | {e['words'][str(1)] if str(1) in e['words'] else e['words'].get(1)} / {e['words'][str(-1)] if str(-1) in e['words'] else e['words'].get(-1)} | {memory} | {ev['captured']} | {ev['capture_latency']} | {ev['frac_original_at_removal']:.2f} | "
                             f"{(A0[tid]['evaluation']['frac_original_T'] if tid in A0 else float('nan')):.2f} | {(A1[tid]['evaluation']['frac_original_T'] if tid in A1 else float('nan')):.2f} | "
                             f"{(A1[tid]['evaluation']['delta_original'] if tid in A1 else float('nan')):+.2f} | {calls} | {usd:.5f} |")
    # ---- spend (any non-scripted backend)
    if backends != ["scripted"]:
        calls = toks_in = toks_out = usd = fuzzy = reask = pfail = 0
        seen_prefix = set()
        for e in eps:
            c = e["cost_actual"]
            calls += c.get("model_calls", 0); toks_in += c.get("prompt_tokens", 0); toks_out += c.get("completion_tokens", 0)
            usd += c.get("cost_usd", 0); fuzzy += c.get("fuzzy_parses", 0); reask += c.get("parse_retries", 0); pfail += c.get("parse_failures", 0)
            key = (e["task_id"], e["seed"], e["world"], e["dose"], str(e["memory"]))
            if key not in seen_prefix and c.get("prefix"):
                seen_prefix.add(key)
                pfx = c["prefix"]
                calls += pfx.get("calls", 0); toks_in += pfx.get("prompt_tokens", 0); toks_out += pfx.get("completion_tokens", 0)
                usd += pfx.get("cost_usd", 0); fuzzy += pfx.get("fuzzy_parses", 0); reask += pfx.get("parse_retries", 0); pfail += pfx.get("parse_failures", 0)
        lines += ["", "## Spend (from the provider's usage fields on every call)", "",
                  f"- model calls: {calls} (prefix counted once per episode)",
                  f"- prompt tokens: {toks_in}, completion tokens: {toks_out}, mean prompt {toks_in / max(1, calls):.0f} tokens/call",
                  f"- actual cost: {usd:.4f} USD (OpenRouter `usage.cost`)",
                  f"- parse: {fuzzy} fuzzy accepts (edit distance 1), {reask} re-asks, {pfail} unparseable after re-ask; call-level clean-parse rate {1 - (fuzzy + reask + pfail) / max(1, calls):.4f}",
                  f"- invalid episodes: {sum(invalid.values())} of {len(eps)} records"]

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
        for f in [f"{a.stage}.md", f"{a.stage}_cells.csv", f"{a.stage}_dose_rule.json"]:
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
