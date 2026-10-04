# Runbook

One exclusive agentops claim (`dmarz-sybil-budget-sonnet`) on one dedicated dmarz server; one worker, up to two in-flight API requests. The private claim-checked launcher is `scripts/run-sybil-budget-sonnet.py` in swarm-labs-agentops. Public files never contain host addresses or credentials.

1. Offline: `cd src && python3 selftest.py` (includes the parent-pairing test). Local S0: `python3 src/worker.py --stage S0 --attempt local-s0-001`.
2. Commit the plan and pre-run reviews to `main`; set `experiment.yaml` `url` to the immutable blob URL of README.md and check it with `python3 reporting/plan_preflight.py`.
3. Claim the server, push the launcher, then `run-sybil-budget-sonnet.py <rev> setup`, then `S0`, `status`, post-review, `Q0`, `status`, post-review, `S1`.
4. Close-out: `status`/`verify --save`, recompute, cross-cohort analysis against the saved Haiku records, `publish`, post-mortem, release the claim.
