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


def runs_for_stage(d: dict, stage: str, backend: str) -> list:
    """One hub run = one block of tasks in one cell (stage x world x dose x memory). All arms run inside."""
    st = d["stages"][stage]
    lo, hi = d["splits"][st["split"]]
    last = min(hi, lo + st["tasks"] - 1)
    out = []
    for world in st["worlds"]:
        for dose in st["doses"]:
            for memory in d["memories"]:
                for b in range(lo, last + 1, d["block"]):
                    e = min(b + d["block"] - 1, last)
                    out.append({"stage": stage, "split": st["split"], "world": world, "dose": dose,
                                "memory": str(memory), "tasks": f"{b}-{e}", "seeds": st["seeds"],
                                "arms": d["arms"], "cfg": d["cfg"], "backend": backend})
    return out


def memory_value(s):
    return s if s == "full" else int(s)
