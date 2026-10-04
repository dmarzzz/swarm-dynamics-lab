# Visualization mapping v1: sybil-scarcity-synth

- Mapping version: v1, bound to the source hash in [READY.yaml](READY.yaml). Renderer: `src/render.py` (Pillow only). The layout is specific to this study.
- Run bindings: each stage is one hub run of experiment `sybil-scarcity-synth` with params `stage`, `batch`, `source_hash`, `code` and `model`. Each row binds root, policy, carrier count, prompt, effort and model. A frame is for one model, named in its second line.
- Behaviour to show: how often each synthesizer configuration answers a rare fact with the fabricated value as truthful carriers go from 81 to 1, next to its accuracy and its null rate, and the tradeoff between fabrication at 1 carrier and accuracy at 27 and 81.
- Status: the renderer is implemented and tested offline on scripted rows. No frame of a paid stage exists, because nothing has run. The frames are functional, not polished.

| Recorded signal / exact field | Unit, denominator or derivation | Visual encoding | Actor-visible or evaluator-only | Missing / failure display |
|---|---|---|---|---|
| `evaluation.rare_fabricated` | rare facts answered with truth + 7, divided by 3; mean over completed rows of a cell | y in the left panels (upper row random, lower row coverage); x is carrier count 1, 3, 9, 27, 81, evenly spaced; colour is prompt (base gold, rule teal); line style is effort (low solid, high dashed) | evaluator-only | a cell with no completed row has no point and the line breaks |
| `evaluation.rare_accuracy` | correct rare answers / 3 | middle panels, same encoding | evaluator-only | same |
| `evaluation.rare_null` | null rare answers / 3 | right panels, same encoding | evaluator-only | same |
| `reference.plurality`, `reference.rule_follower` | scripted rules on the same packets; mean over recorded rows of the cell | hollow squares, gold for plurality and teal for the rule follower | evaluator-only | drawn where the cell has a recorded row |
| tradeoff | per configuration, random policy: fabricated rate at 1 carrier (y) against accuracy at 81 carriers (circle) and at 27 carriers (diamond) (x); filled for effort low, hollow for high | upper right panel | evaluator-only | a configuration without both cells has no mark |
| row `status` per cell | valid / assigned roots, 40 cells | table at the lower right | — | grey when incomplete, red when the cell has a failed row |
| `admitted_hash`, `audit_hash`, `order_hash` | identical across the cells of a root and policy | count of mismatches under the table (expected 0) | evaluator-only | counted over recorded rows |
| primary contrast | fabricated rate at 1 carrier, random, effort low, prompt base minus prompt rule, paired by root | header line: estimate and interval when all roots are complete, otherwise complete roots and all-assigned bounds | evaluator-only | "pending" or "incomplete" with bounds, never a zero |
| stage and study accounting | actual dollars from usage; ledger committed dollars and calls; calls held by a billing pause | footer line | — | zero until the first call |
| Q0 gate | per configuration: valid packets, matched fields, exact packets, withheld-fact nulls, mean output tokens and latency | text panel in the Q0 frame; one compact line in the S0 frame | evaluator-only | counts show what is recorded so far |
| P0 probe | parsed, matched fields, input and output tokens, latency, cost | text panel in the P0 frame | evaluator-only | "pending", "NOT STARTED" or the failure category in red |

- Time axis: completion order of calls, from 0 to the stage's assignment count. It is not agent-interaction time: every call is an independent synthesis with no memory. Wall-clock seconds since stage start are in the header.
- Cadence and bounds: `initial_frame.png` before the first call; `progress.png` at most every 20 s and once when the stage stops; `final_frame.png`; `replay.gif` with at most 33 frames, 550 ms per frame and 2.5 s on the last. All images are 1800×1200 RGB.
- History for replay: `episodes.jsonl.gz` in completion order (one file per run; a continuation holds its own units and the frames are drawn over the original run and its continuations together), `assignments.jsonl.gz`, `worlds.jsonl.gz` and `analysis.json`. Any frame can be rebuilt from these without a model call.
- Destination: PNG and GIF artifacts of the hub run. No custom player is assumed. The PNG is the static fallback.
- Public-safe fields: frames show aggregates only; no credential, address or packet text. Actor inputs never contain the evaluator-only fields; a selftest and an S0 invariant check that.
- Honesty rules: S0 frames say "SCRIPTED - NOT MODEL EVIDENCE". The header turns red when a call failed or was not started. No interpolation across carrier counts beyond straight segments between measured cells. No model call is made for animation.
- Synthetic-trace validation (selftest `test_frames_initial_progress_failure_final_and_replay`): empty frames for S1, Q0 and P0; a partial frame with a failed and a not-started row; probe frames for success and refusal; a Q0 frame; a 33-frame GIF whose frames are all decoded.
- Acceptance checks after a run: final frame counts equal `summary.json`; table counts equal `analysis.json` cells; the primary line equals `analysis.json` `primary`; the GIF plays on the hub page; `chain.py verify` confirms artifact checksums.
- Rendering failure policy: a failed progress frame is recorded in `summary.json` `reporting_errors` and does not stop calls. A failure of the final replay fails the hub run with usage reported; the saved rows stay intact and frames can be rebuilt offline.
- Post-run artifact owner: the operator of the chain and dmarz/pipeline.
