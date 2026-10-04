# Run and reproduce

Start from Python 3.12 with `requirements.txt` installed. `python3 src/selftest.py` runs offline checks. `python3 src/worker.py --stage S0 --attempt s0-local-001` creates an exclusive output directory and makes zero model calls. Never reuse an attempt directory.

The parent operator handles the current exclusive fleet claim, frozen source push, remote setup and confidential credential injection. The standard interface is `coordinator.enqueue(sr, 'S0')`, then `python3 src/worker.py --hub`. After the successful exact-runtime S0 and post-mortem, enqueue Q0 similarly; only a successful exact-runtime Q0 permits S1. The local offline S0 is additional engineering evidence and does not bypass the server qualification gate. `study.params(stage)` provides the code and source fingerprints. No S2 API exists.

Credentials reach runtime only through `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID`, injected through the authorized private launcher. `SYBIL_API_BUDGET_LEDGER` points to the persistent study ledger; the parent supplies shared bundle guard environment separately. This document intentionally contains no credential values or private endpoint.

Each attempt writes assignment, world, history, episode, summary, and analysis records plus supported image artifacts. Raw JSONL/gzip records stay in the authorized store; public images are allowlisted by the live site. Parent uploads artifacts, verifies durable receipts and source/packet hashes, reconciles every assignment, writes API post-mortems, and releases its claim after completion.

## Allocation correction — 2026-10-04 UTC

The owner's updated inbox requires a dedicated host for each experiment. S0 and Q0 historically completed on sim-dmarz-4 under dmarz-sybil-followups; those completed results and runtime fingerprints are preserved. Before S1, this study moves to the dedicated host sim-dmarz-sybil-newcomer under claim dmarz-sybil-newcomer. Provisioning, claim exclusivity, migration and ledger continuity remain pending the parent operator's verification. S1 is not launched by this correction. No simulator, assignment, model, evaluator or source/configuration fingerprint changes.

Across the separate hosts, the existing $60 bundle cap is partitioned into at most $50 total for sybil-budget-api and $10 total for sybil-newcomer-api. Both hosts retain the same settled 52-call checkpoint ($0.366548). The budget host permanently reserves the $10 peer allocation; the newcomer host permanently reserves the $50 peer allocation. Historical charges are not reset. Duplicating the settled checkpoint in both guard copies makes the aggregate bound stricter, rather than creating extra spending authority.

These permanent peer reservations are inter-host allocations, not API charges, model calls or unknown-billing failures. Do not count them as actual experiment spending. Final actual cost is the sum of the separate per-study usage ledgers. Existing per-study conservative reservation/call limits still apply, with the new partition providing the tighter real-spend limit. The parent must verify the guard state and exclusive allocation before launch; this document does not claim that provisioning or migration is complete.
