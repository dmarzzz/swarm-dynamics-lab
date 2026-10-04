# Deployment record

- Experiment: antsy-verification-v4; owner vishesh/codex-methods.
- Exclusive allocation: sim-test-01; claim vishesh-antsy-verification-v4; merged private allocation PR46; expiry 2026-10-04T03:58:07Z. Refreshed claims immediately before qualification: no competing active claim.
- E0 source: e5d684e; completed100 receipts/300 OCR calls with zero invalid outputs.
- S0/S1 policy and pre-run source: c2dffda. Public immutable plan registered and browser-verified before model launch.
- One worker; CPU 2; pinned public Laya weights, local inference; zero paid calls in this condition.
- Paths on the assigned server: /srv/swarm/antsy-v4/repo, /srv/swarm/antsy-v4/venv, /srv/swarm/antsy-v4/runtime, /srv/swarm/antsy-v4/model-cache. No secret values, network addresses or private inventory are published.
- Per-attempt manifests retain source SHA, measured-corpus SHA, model revision, package versions, actual calls and latency. Output directories are immutable.

## Closed allocation

Both S1 runs and their analysis completed; all final artifacts were verified on the hub. No active Antsy worker remained. The local credential relay and SSH tunnel were stopped and the cumulative ledger archived. Exclusive claim released through agentops PR 67 (merged); machine teardown remains its owner's responsibility. A new run requires a fresh verified allocation.
