# Post-mortem: fleet-s0-001

- Run: `sybil-specialists-sonnet/368ac432`, batch s0-001, scripted backend. Host sim-dmarz-4 under exclusive claim `dmarz-sybil-specialists-sonnet` (agentops PR 170), operator dmarz/orbital-orchestrator.
- Source: swarm-lab `f7e7ca01a183152dc5650277c965449e537e5e15`; runtime hash `5628db3dd08bd8faf48c3604f9d160ecacfa43c1c87b70a8db890a5d81d2a86e`. Python 3.12.3, Pillow 11.3.0, PyYAML 6.0.3 in the study's own venv.
- Setup: dedicated checkout and venv created; both selftest suites passed on the host (study 13/13, parent 15/15).
- **Result: pass.**
  - Reconciliation: 216 planned, started, terminal, graded and analyzed; 0 invalid; 0 not started.
  - Clean qualification fixtures: 24/24, with field accuracy, exact packets and missing-fact abstention all at 1.0.
  - Elapsed time: 19.4 s.
- **Resources:** 0 model calls, 0 tokens, USD 0. No credentials were sent. The study ledger does not exist yet; Q0 creates it.

## Checks against the Haiku study

- Attacker admission is algorithmic and must not depend on the model. It matches the Haiku pilot: coverage admits 8/108 and degree 4/108 at attacker pass .10 (.074 and .037).
- Scripted rare accuracy at pass .10, masked, is coverage .917 and degree .083. This matches the scripted plurality reference that the Haiku post-mortem reports.
- Assignment hashes were identical in-process before launch: Q0 24 rows, S1 192 rows.

## Artifacts

`verify` checked the hub hashes of 7 artifacts:

- `final_frame.png`, `replay.gif`, `initial_frame.png`, `progress.png`;
- `assignment.json`, `episodes.jsonl`, `summary.json`.

All three images are 1800×1180. The replay has 28 frames, all decoded, and the final frame is listed first. The worker exited (`worker_active` false).

## Issues

None. The only runtime differences from the Haiku S0 are the hub id, the render label and the design's model, prices and cap, as listed in the pre-run assessment.

## Next

Q0 (24 calls) is technically ready at this runtime hash. It stays blocked until dmarz records a review decision for this study, as stated in [q0-001-pre.md](q0-001-pre.md).
