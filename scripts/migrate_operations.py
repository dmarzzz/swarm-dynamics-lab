#!/usr/bin/env python3
"""Rewrite old-layout path fields in the experiment operations registry (idempotent).

operations.json sits in the toolkit, where migrate_prose_paths.py only reports data files, but its
study_path / setup_path / postmortem_path fields are repo paths that scripts/experiment.py opens.
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip())
REGISTRY = ROOT / "5-experiments/toolkit/agent-experiments/operations.json"
RULES = [
    (r'(?<![\w./-])researchers/shadow/(factory|qa)(?=[/"\s]|$)', r"5-experiments/studies/shadow/\1"),
    (r'(?<![\w./-])researchers/([a-z0-9_-]+)/notes(?=[/"\s]|$)', r"5-experiments/studies/\1"),
    (r'(?<![\w./-])researchers/', "lab/researchers/"),
    (r'(?<![\w./-])tooling/', "5-experiments/toolkit/"),
    (r'(?<![\w./-])experiments/(?=EVIDENCE|evidence-metadata)', "5-experiments/"),
    (r'(?<![\w./-])(templates|tasks|candidates)/', r"lab/\1/"),
]


def main():
    text = REGISTRY.read_text(encoding="utf-8")
    new = text
    for pat, rep in RULES:
        new = re.sub(pat, rep, new)
    json.loads(new)
    if new != text:
        REGISTRY.write_text(new, encoding="utf-8")
    print(f"operations.json: {'rewritten' if new != text else 'nothing to do'}")


if __name__ == "__main__":
    main()
