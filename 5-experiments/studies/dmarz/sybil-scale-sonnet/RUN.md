# Runbook

One exclusive claim `dmarz-sybil-scale-sonnet` on sim-dmarz-3; one finite worker, at most 4 in-flight API requests. The private claim-checked launcher (agentops `scripts/run-sybil-scale-sonnet.py`) supplies the pinned public revision, the credential aliases and the persistent ledger path; public code never contains host addresses or credentials.

1. Offline: `python3 src/selftest.py` (9 tests) and `python3 src/worker.py --stage S0 --attempt <fresh-name>`.
2. Commit plan and pre-run reviews; push to main.
3. Claim sim-dmarz-3 exclusively; launcher `setup` at the exact commit; then `S0`, `status`, `publish`, `verify`; post-review.
4. `Q0` at the same runtime; `status`/`verify`; post-review. Stop if any size fails.
5. `S1` at the same runtime; monitor with `status`; at completion `publish`, `verify`, fetch saved records with `--save`, recompute, compare with the Haiku cohort, write RESULTS.md and the post-review.
6. Confirm worker exit; release the claim. Do not destroy the server.
