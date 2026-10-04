# Run and reproduce

Python 3.12 with `requirements.txt`. `python3 src/selftest.py` runs offline checks. `python3 src/worker.py --stage S0 --attempt <fresh-name>` writes an exclusive output directory and makes zero model calls. Never reuse an attempt directory.

The private launcher (`scripts/run-sybil-newcomer-sonnet.py` in the operator's infrastructure repository) checks the exclusive merged claim and the immutable public plan, sets up the host checkout at an exact public commit, and enqueues stages through `coordinator.enqueue(sr, stage)`, then runs `python3 src/worker.py --hub`. Q0 requires a successful exact-runtime S0; S1 requires a successful exact-runtime Q0. No S2 path exists.

Credentials reach the runtime only through `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID`, passed by the launcher over SSH stdin into process memory. `SYBIL_API_BUDGET_LEDGER` points at this study's persistent ledger on the dedicated host. This document contains no credential values or private endpoints.

Each attempt writes assignments, worlds, history, episodes, summary and analysis records plus the mapped images. `reporting/build_report.py` and `reporting/verify_results.py` rebuild and recompute results from saved records without model calls.
