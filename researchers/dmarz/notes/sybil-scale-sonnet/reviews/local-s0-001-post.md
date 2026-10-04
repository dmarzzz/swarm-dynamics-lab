# Post-mortem: local-s0-001

2026-10-04 / sybil-scale-sonnet / dmarz/scale-sonnet / offline S0 engineering check on orbital-one, zero API calls. No separate pre-run file was written for this offline scripted check; it ran before the plan commit and is recorded here as engineering evidence only. It is not the fleet S0 gate, which is assessed in [fleet-s0-001-pre.md](fleet-s0-001-pre.md).

Source: worktree at swarm-lab 57c020ad plus the uncommitted copy of this study; runtime source hash `a1a619f7e39bb608ba48871766e8d1366d923db2df0cb00524dd5a65faffb230` (Python 3.12.3). Command: `python3 src/worker.py --stage S0 --attempt local-s0-001`.

264 planned, 264 started, 264 terminal, 264 graded, 264 analyzed; 0 invalid, 0 not started. Qualification fixtures: every size 16/16, field accuracy, exact packets and required abstentions all 1.0. Elapsed 21.6 s plus replay rendering; 33-frame replay. Output hashes: summary.json `94372da9…`, analysis.json `9b9cc7e2…`, episodes.jsonl.gz `ceb0aeb7…`; the 2.8 MB output was kept outside the repository (operator scratch), since fleet S0 is the retained run.

Selftest: 9/9 pass, including the ledger cap test, which now derives the over-cap reservation from the design cap instead of the original hard-coded 181 USD (needed because the cap is now 240).

Equivalence check against the Haiku study, recomputed in-process from both directories: ordered (assignment id, packet hash) digests are identical for Q0 (64 rows) and S1 (2,400 rows); the system prompt + schema digest is identical. The source hash differs from the Haiku runtime only through design.yaml (model, prices, cap, experiment name), experiment.yaml, coordinator/worker hub ids, the render title label and the selftest cap line.

Disposition: advance to fleet S0.
