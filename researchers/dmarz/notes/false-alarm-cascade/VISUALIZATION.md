# Visualization mapping v1: false-alarm-cascade

- Mapping version: v1, bound to the source hash in [READY.yaml](READY.yaml). Renderer: `src/render.py` (Pillow only). No parent mapping; the layout is specific to this study.
- Run bindings: each stage is one hub run of experiment `false-alarm-cascade` with params `stage`, `batch` (`s0-001`, `p0-001`, `q0-001`, `s1-001`), `source_hash` and `code`. Each row binds root, condition, member, round and, in S0, the scripted actor.
- Behaviour to show: whether use of the falsely accused real resource X falls after the alarm, and whether it comes back after the correction; the same for the truly accused honeypot H; whether avoidance spreads to other real resources; and whether the agents get better at telling honeypots from real resources or only skip more.
- Status: the renderer is implemented and tested offline on scripted rows. No frame of a paid stage exists, because nothing has run.

## Stage frame (`initial_frame.png`, `progress.png`, `final_frame.png`)

| Recorded signal / exact field | Unit, denominator or derivation | Visual encoding | Actor-visible or evaluator-only | Missing / failure display |
|---|---|---|---|---|
| `evaluation.use_x` by condition and round | agent decisions that used X / completed agent calls of that condition and round, pooled over roots | upper left panel: y is the use rate, x is the round 1 to 6; one line per condition `C0`, `FA`, `FA+C` (colour and legend label) | evaluator-only (X is hidden truth) | a round with no completed call has no point and the line breaks |
| `evaluation.use_h` by condition and round | the same for H | upper right panel: lines for `C0`, `TA`, `TA+C` | evaluator-only | as above |
| alarm and correction | fixed by the design: posted at the end of round 1 and of round 3 | dashed vertical lines between rounds 1-2 and 3-4, labelled | the posts themselves are actor-visible from the next round; their being planted is evaluator-only | always drawn |
| `evaluation.use_mates`, `evaluation.use_other_real` | paired by root: `C0` minus `FA` and `C0` minus `FA+C`, rounds 2-3 and 4-6; mean over roots whose decisions are complete | lower left panel: eight bars in points, zero line in the middle, value printed above each bar | evaluator-only | no bar when no root is complete; outlined bar when some roots are incomplete |
| `used_real`, `skipped_real`, `used_honeypot`, `skipped_honeypot` | per condition and window (1; 2-3; 4-6): hit rate = honeypots skipped / honeypots, false-alarm rate = real skipped / real, d′ and criterion c with the log-linear correction | two lower middle panels: d′ (0 to 3) and c (−1.5 to 1.5), one line per condition | evaluator-only | no point without completed calls |
| row `status` per episode | rounds whose five calls completed, per root and condition | right column: a grid of roots × conditions, cell shade and number 0 to 6 | — | red cell when a call of the episode failed; dark cell with 0 when nothing completed |
| primary contrast | use of X in rounds 4-6, `C0` minus `FA+C`, paired by root | header line: estimate and bootstrap interval when all roots are complete, otherwise complete roots and all-assigned bounds | evaluator-only | "pending" or "incomplete" with bounds, never a zero |
| stage and study accounting | actual dollars from usage; ledger committed dollars and calls | footer line | — | zero until the first call |
| Q0 groups | per depth: valid packets, gated decisions matched / total, use-gated and skip-gated counts, contested (not gated) | text panel in the Q0 frame; one compact line in the S0 frame | evaluator-only | counts show what is recorded so far |
| P0 probe | parsed, unanimous decisions matched, input and output tokens, latency, cost | text panel in the P0 frame | evaluator-only | "pending" or the failure category in red |

In S0 the two upper panels show the credulous script (the positive control); the frame says "SCRIPTED - NOT MODEL EVIDENCE".

## Replay (`replay.gif`)

The run has real temporal structure, so the replay follows logical rounds, not completion order.

- Episode set: prespecified in `design.yaml` (`analysis.representative_root`): the lowest S1 root, 8400, in all five conditions. In S0: engineering root 8390 under the credulous script.
- Frames: one before round 1, one per round 1 to 6, then the final stage frame: 8 frames, 1800×1200, 0.9 s for the first, 1.4 s per round, 3 s on the last.
- Each round frame has one row per condition and one cell per resource (ordered by family): the cell shows how many of the five agents used the resource in that round (`answer.decisions`), as a number and a shade. To the right: how many entries the board held when the agents decided (`packet.board`) and the entries about the alarm subject, with round, author and `retracts`.
- Viewer layer only: a red outline marks honeypots, `X` and `H` mark the alarm subjects, `*` marks the planted author. None of this is in any actor input; S0 and a selftest check the actor inputs for it.
- A cell with no completed call shows a dash; a condition row whose round has failed or missing calls shows the count of completed calls in red.

For P0 and Q0 the GIF is the initial and the final stage frame.

## Rules

- Time axis: logical rounds. Wall-clock seconds since stage start are printed in the header of the stage frame. Conditions are aligned by round.
- Cadence and bounds: one `initial_frame.png` before the first call; `progress.png` at most every 20 s and once when the stage stops; `final_frame.png`; `replay.gif` with 8 frames (2 for P0 and Q0). All images are 1800×1200 RGB. Rendering a stage's frames takes a few seconds locally.
- History for replay: `episodes.jsonl.gz` (every call row with its packet, answer, grade and usage, in completion order), `assignments.jsonl.gz` (each episode's fixed inputs, each fixture's packet), `worlds.jsonl.gz` (truth, evaluator-only) and `analysis.json`. Any frame can be rebuilt from these without a model call.
- Destination: PNG and GIF artifacts of the hub run; `final_frame.png` is uploaded first for the contact sheet. No custom player is assumed. The PNG is the static fallback.
- Public-safe fields: frames show synthetic resource ids, counts and board claims. No credential, address or free text of an agent appears (rationales are not drawn).
- Honesty rules: no interpolation between rounds; no smoothing; a point or a cell is drawn only from completed calls; failed and not-started calls are shown as such. No model call is made for animation. Uncertainty is shown only for the root-level primary contrast.
- Synthetic-trace validation (selftest `test_frames_initial_progress_failure_final_and_replay`): empty frames for S1, Q0 and P0; a partial S1 frame with a failed and a missing call; probe frames for success and refusal; a Q0 frame; an 8-frame GIF whose frames are all decoded; replay with a failed and a missing call; replay frames of different rounds differ; initial and final PNG sizes.
- Acceptance checks after a run: initial frame shows 0 completed; final frame counts equal `summary.json`; the primary line equals `analysis.json` `primary`; the per-round lines equal `analysis.json` `by_round`; the completion grid equals `completeness`; the GIF plays on the hub page; `chain.py verify` confirms artifact checksums.
- Rendering failure policy: a failed progress frame is recorded in `summary.json` `reporting_errors` and does not stop calls. A failure of the final replay fails the hub run with usage reported; the saved rows stay intact and frames can be rebuilt offline.
- Post-run artifact owner: the operator of the chain and dmarz/pipeline.
