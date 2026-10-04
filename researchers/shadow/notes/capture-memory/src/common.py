"""Shared helpers: design loading and the run plan for a stage. Standard library only."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name: str) -> dict:
    """design.yaml / experiment.yaml hold JSON (as in discussion-dose), so no YAML library is needed."""
    return json.loads((ROOT / name).read_text())


def task_range(spec: str) -> list:
    lo, hi = (int(x) for x in spec.split("-"))
    return list(range(lo, hi + 1))


def stage_cfg(d: dict, stage: str) -> dict:
    """Design cfg with the stage's declared overrides applied (S1b lengthens the takeover cap only)."""
    return {**d["cfg"], **d["stages"][stage].get("cfg_overrides", {})}


def runs_for_stage(d: dict, stage: str, backend: str) -> list:
    """One hub run = one block of tasks in one cell (stage x world x dose x memory). All arms run inside.
    A stage may narrow `memories`, change `block`, or override cfg keys; everything else is the frozen design."""
    st = d["stages"][stage]
    lo, hi = d["splits"][st["split"]]
    last = min(hi, lo + st["tasks"] - 1)
    block = st.get("block", d["block"])
    cfg = stage_cfg(d, stage)
    out = []
    for world in st["worlds"]:
        for dose in st["doses"]:
            for memory in st.get("memories", d["memories"]):
                for b in range(lo, last + 1, block):
                    e = min(b + block - 1, last)
                    out.append({"stage": stage, "split": st["split"], "world": world, "dose": dose,
                                "memory": str(memory), "tasks": f"{b}-{e}", "seeds": st["seeds"],
                                "arms": d["arms"], "cfg": cfg, "backend": backend})
    return out


SCRIPTED_STAGES = ("S0", "S1", "S1b")      # the only stages this coordinator/worker will run; no S2 here


def memory_value(s):
    return s if s == "full" else int(s)
