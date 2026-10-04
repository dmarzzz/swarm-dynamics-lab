# Pre-run assessment: s1-a1

- Experiment / owner / stage: sybil-scale-xl A1 / dmarz (operator dmarz/scale-xl) / S1, claude-opus-5-5, effort low.
- Parent: q0-a1 must pass at every size at the same source hash; its post-mortem must restate the S1 cost from measured Opus tokens before launch. If that estimate exceeds the remaining shared allowance, stop and ask dmarz.
- Design: 24 world clusters (6000–6023) × 3 sizes × 8 conditions = 576 calls. The primary contrast and secondary items are in preregistration.md as amended by A1. Units are worlds; calls, identities and skills are not independent samples.
- Plan: 4 in flight, 300 s timeout, 30,000 s stage limit, no retries, first failure stops dispatch and records the rest as not started. Preparation on sim-dmarz takes about 1–2 h before the first call (fleet-s0-001 timing).
- Budget: estimate USD 175–236 input plus USD 3–20 output (AMENDMENT-A1.md); the ledger stops at USD 330 settled plus open.
- Visualization: mapping v1 with A1 changes; final frame, progress frames, ≤33-frame replay; after collection the combined parent+XL figure (Haiku 36–972 and Opus 972–8,748 as separate marks).
