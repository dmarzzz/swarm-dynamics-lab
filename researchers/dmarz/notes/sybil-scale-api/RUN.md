# Runbook

One exclusive claim on sim-dmarz-4, dmarz-sybil-scale-api; one worker process, up to4 inflight API requests. Use the private claim-checked launcher; public code never contains host addresses or credentials.

1. Run `python3 src/selftest.py`; commit source, plan and engineering pre-review.
2. `python3 src/worker.py --stage S0 --attempt local-s0-001` runs offline; inspect all assertions and visuals. Record post-review.
3. Claim and verify exclusive host; push public source; private launcher setup at exact commit. Register/run fleet S0; reconcile and post-review.
4. Commit Q0 pre-review; launch exact-source Q0 with aliases SWARM_MODEL_API_KEY and SWARM_MODEL_WORKSPACE_ID loaded from SOPS into environment only. Persistent SYBIL_API_BUDGET_LEDGER remains on dedicated host. Inspect per-size qualification before S1.
5. Commit S1 pre-review; run bounded S1. Status and measured frames show progress. No automatic retries or restart. Preserve all unsuccessful attempts before repair.
6. Fetch sanitized summary/analysis and raw compressed outputs; independently recompute evaluator and all aggregates; inspect UI and artifact hashes. File final figures with Flight Deck provenance; write post-mortem, results and actual spend.
7. Verify worker exit, release claim; do not destroy an existing shared fleet machine. Final repository check and Flight Deck strict check, then sync.
