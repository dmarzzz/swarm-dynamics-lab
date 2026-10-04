#!/usr/bin/env python3
"""Register capture-memory-mix on the hub and attach local result files (tables, episodes, call logs) as runs.

    python3 src/hub_push.py register
    python3 src/hub_push.py stage M1 results/local-m1      # one hub run per cell file + an analysis run with M1.md
    python3 src/hub_push.py pilot results/pilot-mp          # one run per pilot cell (episodes + calls), analysis run with MP.md

Needs swarm_report on PYTHONPATH and SWARM_HUB_URL/TOKEN/SOURCE in the environment (never written here).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from common import ROOT, load  # noqa: E402

import swarm_report as sr  # noqa: E402

EXP = load("experiment.yaml")["id"]


def push_cells(stage: str, d: Path, tag: str):
    n = 0
    for f in sorted(d.glob("*.jsonl")):
        if f.name.startswith("calls-"):
            continue
        summ = f.with_suffix(".summary.json")
        meta = json.loads(summ.read_text()) if summ.exists() else {}
        p = meta.get("params", {})
        run = sr.start(EXP, run=f"{EXP}/{stage}-{f.stem}", params={**{k: p.get(k) for k in ("stage", "world", "dose", "memory", "tasks", "backend")}, "kind": "cell"},
                       message=f"{stage} cell {f.stem} ({tag})")
        run.artifact(f, "episodes.jsonl")
        if summ.exists():
            run.artifact(summ, "summary.json")
        m = meta.get("metrics", {})
        run.done(message=f"{m.get('episodes')} episodes, {m.get('invalid')} invalid, {m.get('model_calls')} calls, {m.get('cost_usd')} USD", **{k: v for k, v in m.items() if isinstance(v, (int, float))})
        n += 1
    return n


def push_analysis(stage: str, extra: list):
    out = ROOT / "results"
    run = sr.start(EXP, run=f"{EXP}/analysis-{stage}", params={"stage": stage, "kind": "analysis"}, message=f"analysis {stage}")
    for name in [f"{stage}.md", f"{stage}_cells.csv"] + extra:
        p = out / name if not str(name).startswith("results/") else ROOT / name
        if p.exists():
            run.artifact(p, Path(name).name)
    run.done(message=f"{stage} tables")


def main():
    cmd = sys.argv[1]
    if cmd == "register":
        spec = load("experiment.yaml")
        sr.register(EXP, **{k: spec[k] for k in ("title", "description", "params", "metrics", "primary_metric", "owner", "url")})
        print("registered", EXP)
    elif cmd == "stage":
        stage, d = sys.argv[2], Path(sys.argv[3])
        n = push_cells(stage, d, "scripted")
        push_analysis(stage, [])
        print(f"{stage}: {n} cell runs + analysis")
    elif cmd == "pilot":
        # usage: pilot <dir> <stage-name> <model-tag>   e.g. pilot results/pilot-mp MP gpt-4o-mini
        d, stage, tag = Path(sys.argv[2]), sys.argv[3], sys.argv[4]
        n = push_cells(stage, d, tag)
        extra = [f"{d}/{f.name}" for f in sorted(d.glob("calls-*.jsonl"))] + [f"{d}/cells.json", "results/spend-ledger.json", "results/priors-4omini.json", "results/calib-llama8b.json", "results/rescue-vs-f.svg"]
        push_analysis(stage, extra)
        print(f"{stage}: {n} cell runs + analysis")


if __name__ == "__main__":
    main()
