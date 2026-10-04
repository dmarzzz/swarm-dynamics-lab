# Pre-run assessment: s0-a1

- Experiment / owner / stage: sybil-scale-xl amendment A1 / dmarz (operator dmarz/scale-xl) / S0, scripted, 0 model calls.
- Parent: fleet-s0-001 (Haiku manifest, pass). A1 changes the runtime source hash, so S0 reruns to give Q0 an exact-runtime prerequisite.
- Design: engineering worlds 4900–4901 × 2 attacker rates × 4 checkpoints (random/coverage × 4 and N/9 checks) × visible badges, plus 4 qualification worlds × 2 packets × visible, per size: 72 rows.
- Command: `run-sybil-scale-xl.py <commit> setup`, `S0`, `status`, `publish`, `verify` (agentops). Expected ~10 min, dominated by N=8,748 preparation.
- Visualization: mapping v1 with A1 changes: OPUS 5.5 label on paid stages, only random/coverage curves, hidden-badge image states the condition is not in A1.
