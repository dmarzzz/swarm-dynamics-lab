"""Shared helpers: design loading and the run plan for a stage. Standard library only."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name: str) -> dict:
    return json.loads((ROOT / name).read_text())


def task_range(spec: str) -> list:
    lo, hi = (int(x) for x in spec.split("-"))
    return list(range(lo, hi + 1))


def stage_cfg(d: dict, stage: str) -> dict:
    return {**d["cfg"], **d["stages"][stage].get("cfg_overrides", {})}


def memory_param(memory) -> str:
    """Hub-safe string form of a memory spec; parse back with parse_memory."""
    if isinstance(memory, dict):
        return f"mix:{memory.get('short', 1)}/{memory['long']}@{float(memory['f']):g}"
    return str(memory)


def parse_memory(s: str):
    if s.startswith("mix:"):
        body = s[4:]
        lw, f = body.split("@")
        short, long = lw.split("/")
        return {"short": short if short == "full" else int(short),
                "long": long if long == "full" else int(long), "f": float(f)}
    return s if s == "full" else int(s)


def runs_for_stage(d: dict, stage: str, backend: str) -> list:
    """One run = one block of tasks in one cell (stage x world x dose x memory-spec). All arms run inside."""
    st = d["stages"][stage]
    lo, hi = d["splits"][st["split"]]
    last = min(hi, lo + st["tasks"] - 1)
    block = st.get("block", d["block"])
    cfg = stage_cfg(d, stage)
    cells = []
    for c in st.get("cells", []):
        for w in c.get("worlds", st["worlds"]):
            cells.append((w, c["dose"], memory_param(c["memory"])))
    for mx in st.get("mixes", []):
        for w in mx.get("worlds", st["worlds"]):
            for f in mx.get("fractions", d["fractions"]):
                cells.append((w, mx["dose"], memory_param({"short": mx["short"], "long": mx["long"], "f": f})))
    out = []
    for world, dose, mem in cells:
        for b in range(lo, last + 1, block):
            e = min(b + block - 1, last)
            out.append({"stage": stage, "split": st["split"], "world": world, "dose": dose, "memory": mem,
                        "tasks": f"{b}-{e}", "seeds": st["seeds"], "arms": st.get("arms", d["arms"]),
                        "cfg": cfg, "backend": backend})
    return out


SCRIPTED_STAGES = ("M0", "M1", "M2")
