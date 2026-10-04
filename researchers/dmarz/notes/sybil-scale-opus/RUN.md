# Runbook

One exclusive claim `dmarz-sybil-scale-opus` on sim-dmarz-12; one finite worker, at most 4 in-flight API requests. The private claim-checked launcher (agentops `scripts/run-sybil-scale-opus.py`) supplies the pinned public revision, credential aliases and persistent ledger path; public code never contains host addresses or credentials.

1. Offline: `python3 src/selftest.py` (10 tests, including the Opus request/response contract on a mocked transport) and `python3 src/worker.py --stage S0 --attempt <fresh-name>`.
2. Commit plan and pre-run reviews; push to main.
3. Claim sim-dmarz-12 exclusively; launcher `setup` at the exact commit; `S0`, `status`, `publish`, `verify`; post-review.
4. `Q0` at the same runtime (coordinator refuses unless S0 passed at this source hash); `status`/`publish`/`verify`; post-review. Stop if any size fails or any interface failure occurs.
5. `S1` at the same runtime; monitor with `status`; at completion `publish`, `verify`, `--save` records, recompute, compare with the Haiku and Sonnet cohorts, RESULTS.md and post-review.
6. Confirm worker exit; release the claim. Do not destroy the server.
