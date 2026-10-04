# Run and reproduce

Python 3.12 with `requirements.txt`. `python3 src/selftest.py` runs offline checks. `python3 src/worker.py --stage S0 --attempt <fresh-name>` writes an exclusive output directory and makes zero model calls. Never reuse an attempt directory.

The private launcher (`scripts/run-sybil-newcomer-opus.py` in the operator's infrastructure repository) checks the exclusive merged claim and the immutable public plan, sets up the host checkout at an exact public commit, and enqueues stages through `coordinator.enqueue(sr, stage)`. Its `chain` action runs, in one background process on the host: S0 worker → `src/probe.py` (one Opus call on an engineering packet, recorded in `results/p0-001-probe.json`, counted in the study ledger) → Q0 worker → S1 worker, each only if the previous step exited cleanly with its gate passed. Q0 requires a successful exact-runtime S0; S1 a successful exact-runtime Q0. No S2 path exists.

Credentials reach the runtime only through `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID`, passed by the launcher over SSH stdin into process memory. `SYBIL_API_BUDGET_LEDGER` points at this study's persistent ledger. This document contains no credential values or private endpoints.

`reporting/build_report.py`, `reporting/verify_results.py` and `reporting/compare_haiku.py` rebuild and recompute results from saved records without model calls.
