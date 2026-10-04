# Run and reproduce

Start from Python 3.12 with `requirements.txt` installed. `python3 src/selftest.py` runs offline checks. `python3 src/worker.py --stage S0 --attempt s0-local-001` creates an exclusive output directory and makes zero model calls. Never reuse an attempt directory.

The parent operator handles the current exclusive fleet claim, frozen source push, remote setup and confidential credential injection. The standard interface is `coordinator.enqueue(sr, 'S0')`, then `python3 src/worker.py --hub`. After the successful exact-runtime S0 and post-mortem, enqueue Q0 similarly; only a successful exact-runtime Q0 permits S1. The local offline S0 is additional engineering evidence and does not bypass the server qualification gate. `study.params(stage)` provides the code and source fingerprints. No S2 API exists.

Credentials reach runtime only through `SWARM_MODEL_API_KEY` and `SWARM_MODEL_WORKSPACE_ID`, injected through the authorized private launcher. `SYBIL_API_BUDGET_LEDGER` points to the persistent study ledger; the parent supplies shared bundle guard environment separately. This document intentionally contains no credential values or private endpoint.

Each attempt writes assignment, world, history, episode, summary, and analysis records plus supported image artifacts. Raw JSONL/gzip records stay in the authorized store; public images are allowlisted by the live site. Parent uploads artifacts, verifies durable receipts and source/packet hashes, reconciles every assignment, writes API post-mortems, and releases its claim after completion.
