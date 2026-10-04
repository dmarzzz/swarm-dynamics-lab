# Visualization mapping v1: sybil-scarcity-opus

- Mapping version: v1, bound to the source hash in [READY.yaml](READY.yaml). Renderer: `src/render.py` (Pillow only). No parent mapping; the layout is specific to this study.
- Run bindings: each stage is one hub run of experiment `sybil-scarcity-opus` with params `stage`, `batch` (`s0-001`, `p0-001`, `q0-001`, `s1-001`), `source_hash` and `code`. Each row binds root, policy, checks, attacker check-pass, carrier count and, for clean packets, the withheld skill.
- Behaviour to show: how the synthesizer's specialist accuracy falls or holds as the truthful carriers of each rare fact go from 81 to 1, next to whether the truth survived admission at all.
- Status: the renderer is implemented and tested offline on scripted rows. No frame of a paid stage exists, because nothing has run.

| Recorded signal / exact field | Unit, denominator or derivation | Visual encoding | Actor-visible or evaluator-only | Missing / failure display |
|---|---|---|---|---|
| `evaluation.rare_accuracy` | correct answers for skills 3, 4, 5 divided by 3; mean over completed rows of a cell | y position in the two upper panels (one per attacker check-pass 10% and 90%); x is carrier count 1, 3, 9, 27, 81, evenly spaced (log scale); colour is policy (random gold, coverage teal); line style is checks (4 dotted, 64 dashed, 108 solid) | evaluator-only (grading uses hidden truth) | a cell with no completed row has no point and the line breaks there |
| root bootstrap interval of a cell | 10,000 draws over roots, seed 20261004; only when all roots of the cell are valid and there are at least 8 | thin vertical bar at the 108-check points | evaluator-only | not drawn for incomplete cells |
| `scripted_evaluation.rare_accuracy` | plurality rule on the same packet | hollow square at the 108-check points | evaluator-only | drawn only where the cell has a completed row |
| `diagnostics.truth_available` | share of the three rare facts with a truthful carrier admitted; mean over recorded rows | y position in the two lower panels, same axes and encodings | evaluator-only | no point for cells with no recorded row |
| `diagnostics.attacker_seat_share` | attacker-owned admitted reports / 486 | thin lines against carrier count in the right lower panel, scale 0 to 30%; must be flat | evaluator-only | no line segment for cells with no recorded row |
| `admitted_hash`, `audit_hash`, `order_hash` | identical across carrier counts within root, policy, checks and strength | text count of mismatching cells under the invariance panel (expected 0) | evaluator-only | counted over recorded rows |
| row `status` per cell | valid / assigned roots | 60-cell table at the upper right | — | grey when incomplete, red when the cell has a failed row |
| primary contrast | 1 carrier minus 81 carriers, random, 108 checks, pass 10%, paired by root | header line: estimate and interval when all roots are complete, otherwise complete roots and all-assigned bounds | evaluator-only | says "pending" or "incomplete" and shows bounds, never a zero |
| stage and study accounting | actual dollars from usage; ledger committed dollars and calls | footer line | — | zero until the first call |
| Q0 groups | per carrier profile: valid packets, matched fields, exact packets, withheld-fact abstentions | text panel in the Q0 frame; one compact line in the S0 frame | evaluator-only | counts show what is recorded so far |
| P0 probe | parsed, matched fields, input and output tokens, latency, cost | text panel in the P0 frame | evaluator-only | "pending" or the failure category in red |

- Time axis: completion order of calls, from 0 to the stage's assignment count. It is not agent-interaction time: every call is an independent synthesis with no memory. Wall-clock seconds since stage start are printed in the header.
- Event markers: none inside a stage. Stage boundaries are separate runs with their own frames.
- Cadence and bounds: one `initial_frame.png` before the first call; `progress.png` at most every 20 s and once when the stage stops; `final_frame.png`; `replay.gif` with at most 33 frames (prefixes at 32 equal steps of the recorded rows plus the empty frame), 550 ms per frame and 2.5 s on the last. All images are 1800×1200 RGB. Rendering 33 frames took a few seconds locally.
- History for replay: `episodes.jsonl.gz` in completion order, `assignments.jsonl.gz`, `worlds.jsonl.gz` (graphs, truth and carrier permutations, evaluator-only) and `analysis.json`. Any frame can be rebuilt from these without a model call.
- Destination: PNG and GIF artifacts of the hub run; `final_frame.png` is uploaded first for the contact sheet. No custom player is assumed. The PNG is the static fallback.
- Optional scripted audit trace: not implemented. The retained `verification_events` would allow it later from saved records.
- Public-safe fields: frames show aggregates only. No credential, address or packet text appears. Actor inputs never contain the evaluator-only fields above; a selftest and an S0 invariant check that.
- Honesty rules: S0 frames say "SCRIPTED - NOT MODEL EVIDENCE" and label the upper panels "scripted answer". No interpolation between the three sampled check budgets. No model call is made for animation.
- Synthetic-trace validation (selftest `test_frames_initial_progress_failure_final_and_replay`): empty frames for S1, Q0 and P0; a partial frame with a failed and a not-started row; probe frames for success and refusal; a 33-frame GIF whose frames are all decoded; initial and final PNG sizes.
- Acceptance checks after a run: initial frame shows 0 completed; final frame counts equal `summary.json`; table counts equal `analysis.json` cells; the primary line equals `analysis.json` `primary`; the GIF plays in the hub page; `chain.py verify` confirms artifact checksums.
- Rendering failure policy: a failed progress frame is recorded in `summary.json` `reporting_errors` and does not stop calls. A failure of the final replay fails the hub run with usage reported; the saved rows stay intact and frames can be rebuilt offline.
- Post-run artifact owner: the operator of the chain and dmarz/pipeline.
