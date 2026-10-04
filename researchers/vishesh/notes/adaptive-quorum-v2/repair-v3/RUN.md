# Reproduce Antsy repair v3

Read SPEC, agent-spec and previous post-mortem. Obtain an exclusive authorized fleet allocation before any model run; offline unit tests need none. Record claim/expiry and exact commit. Never reuse another experiment's host or put credentials in artifacts.

Pinned source: https://github.com/NandhaKishorM/laya at `2e4d9c87e8b1621deb344eac7de5c7258f32f849`. Python3.12 CPU environment: torch2.14.1+cpu, transformers4.57.6, safetensors0.8.0, huggingface-hub0.36.2, numpy2.5.3, Pillow12.3.0, PyYAML6.0.3. Import Laya from its pinned source via PYTHONPATH; the earlier wheel omitted backend modules. Checkpoint and revision are in agent-spec. Download into an approved local cache once, then run with HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1 and HF_HUB_DISABLE_IMPLICIT_TOKEN=1. No private token is required for this public checkpoint.

From this directory:

```sh
python -m unittest discover -s src -p test_engine.py
python src/qualify.py --out /path/to/new-Q2-attempt
python src/sweep.py --qualification /path/to/passed-Q2-attempt --out /path/to/new-S1-attempt --report
```

`--report` requires the existing server `swarm_report` module and authorized local credential mechanism. Do not print or copy its secret configuration. SWARM_SOURCE is `vishesh/codex-methods`. The stable experiment is `adaptive-quorum-api-v2`. The first sweep ID is frozen in source; change it explicitly and pre-register a fresh attempt before rerunning. Never overwrite directories or resubmit outcomes as a new scientific replicate.

Q1 code is frozen at commit4247d1f; Q2 at6d98eac. Use exact commits to reproduce a historical architecture, not today's amended adapter. D0 was run at5e735fb. Preserve all failed outputs. Rendering uses Pillow only and can be repeated without models. The public hub embeds PNG/GIF, while full JSON/receipts remain downloadable team artifacts and compact results in git. Register the plan URL to this folder. Do not label a failed scientific gate as an infrastructure crash.

After execution: reconcile assignment counts, inspect outputs and initial/intermediate/final frames, run analysis, upload artifacts, write post-mortem, fix operational defects without outcome rerolls, commit/push checked paths, stop own worker and release claim after upload verification.
