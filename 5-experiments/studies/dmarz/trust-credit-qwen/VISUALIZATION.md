# Visualization mapping v1: trust-credit-qwen

Follows [RUN-VISUALIZATION.md](../../../toolkit/agent-experiments/RUN-VISUALIZATION.md). Renderer: `src/render.py` (PIL only, 1800×1200 RGB). Nothing has been rendered from a model run; the frames checked so far come from the scripted stage and say so.

- Mapping version / source: v1, part of the hashed source; code commit and source hash in [reviews/chain-001-pre.md](reviews/chain-001-pre.md).
- Run binding: one hub run per stage, `trust-credit-qwen/<run id>`, params `stage`, `batch`, `source_hash`, `code`; a continuation after a billing stop is its own run (`s1-001-r1`) and its frames show the original run's rows and its own together. Each row binds root, rule, check budget and check strength.
- Behavior to make visible: where the credit of a passed check goes decides how many attacker identities are seated as the budget grows (the trust-flow figure), and what the model answers from those seats.

| Recorded signal / exact field | Unit, denominator or derivation | Visual encoding / legend / scale | Actor-visible or evaluator-only | Missing/failure display |
|---|---|---|---|---|
| `admission.attacker_seats` | controller identities among the 162 seats, from scripted admission | two panels (controller check pass 10%, 90%); x = 32, 64, 108 checks; y = 0 to 60 seats; colour by rule (propagated violet, direct teal, anchors gold); thin line per root, thick line and dots for the mean over recorded roots | evaluator-only | a root appears once its rows are recorded (also for failed calls: the seat outcome does not depend on the model) |
| primary contrast per root | (propagated 108 − 32) − (direct 108 − 32), strong checks, from `analyze.seat_contrast` | right panel, one dot per root on a −60 to +60 seat axis, white line at the mean; estimate, bootstrap interval and count of positive roots as text | evaluator-only | roots without all four rows recorded are not drawn; the count is printed |
| `evaluation.rare_correct`, `rare_wrong`, `rare_abstain` | mean over completed calls of a cell | stacked bars (teal, red, gray) per rule and budget, in three groups: strong checks, weak checks, clean endpoints | evaluator-only | a cell with no completed call is an empty outline, never zero |
| status counts | completed / failed / not started / pending of the assigned total; elapsed seconds | header line | operational | always shown |
| accounting and ledger totals | stage calls, tokens, dollars; study calls, settled dollars, dollars committed against the cap | footer line | operational | zeros before the first call |
| qualification cells (Q0; S0 fixtures) | per shape: valid, exactly right, null on the withheld fact | text table | evaluator-only | counts show what is missing |
| probe (P0) | input tokens, request bytes, tokens per byte | text | operational | "not passed or not finished" |

- Time axis: completion order of recorded calls; no simulated time and no within-model telemetry.
- Cadence and bounds: progress image at most every 20 s and at the end; replay of at most 11 frames (initial, 9 prefixes, final), 500 ms per frame and 2.5 s on the last.
- History for replay: `episodes.jsonl.gz` (every row with `completion_index`, `elapsed_seconds`, ledger totals), `assignments.jsonl.gz`, `audits.jsonl.gz` (the frozen audit sequences).
- Artifacts per run: `initial_frame.png`, `progress.png`, `final_frame.png`, `replay.gif`, and the data files. PNG and GIF are the public types.
- Why a completion replay: each assignment is one independent call; what evolves is how much has been recorded. The frame says so.
- Public-safe content: no secret or address is drawn. Ownership and truth appear only as aggregate outcomes, never in what the model receives.
- The scripted frame carries "SCRIPTED REFERENCE POLICY - NOT MODEL EVIDENCE" and titles the answer panel "Reference-policy answers".
- Validation (selftest): frames for an empty run, a partial run with a failed and not-started rows, a complete scripted run, empty and filled qualification and probe stages, and without truetype fonts; plotted seat means compared with a recomputation; the replay GIF decoded frame by frame.
- Acceptance after a run: the final frame's primary and seat means equal `analysis.json`; header counts equal `summary.json`; `chain.py verify` confirms the uploaded image checksums.
- Rendering failure policy: a rendering error is recorded under `reporting_errors` in `summary.json` and changes no row and no outcome; missing frames show up in `verify`. The operator who closes the run owns the visual audit.
