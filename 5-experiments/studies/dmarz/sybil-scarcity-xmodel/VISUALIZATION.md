# Visualization mapping v1: sybil-scarcity-xmodel

Follows [RUN-VISUALIZATION.md](../../../../tooling/agent-experiments/RUN-VISUALIZATION.md). Renderer: `src/render.py` (PIL only, 1800×1200 RGB). Nothing has been rendered from a model run; frames checked so far come from the scripted stage and the stubbed rehearsal.

- Mapping version / source: v1, part of the hashed source; code commit and source hash in [reviews/chain-001-pre.md](reviews/chain-001-pre.md). Adapted from the parent's mapping (carrier count on the x axis).
- Run binding: one hub run per stage under the model's hub experiment, `sybil-scarcity-xmodel-<tag>/<run id>`; params `stage`, `backend`, `model`, `batch`, `source_hash`, `code`. Each row binds root, policy, checks, attacker pass rate and carriers, and carries its model.
- Behavior to make visible: whether this model's specialist accuracy falls as truthful carriers become scarce, against the parent's Opus 5.5 curve on the same packets.

| Recorded signal / exact field | Unit, denominator or derivation | Visual encoding / legend / scale | Actor-visible or evaluator-only | Missing/failure display |
|---|---|---|---|---|
| `evaluation.rare_accuracy` | rare facts answered exactly right / 3; cell mean over completed calls | four panels (random or coverage auditing × attacker pass 10% or 90%); x = carriers 1, 3, 9, 27, 81 (evenly spaced); y 0 to 100%; one line per check count (4 gray, 64 violet, 108 teal) | evaluator-only | a cell with no completed call is not drawn; never zero |
| parent's `rare_accuracy` (pinned rows) | Opus 5.5 on the same packets, primary cell only | dashed gold line in the random / 10% panel (S1 frames only) | evaluator-only | absent if the pinned parent rows are unavailable |
| primary contrast | 1 minus 81 carriers, random, 108 checks, pass 10%; mean over complete roots, bootstrap interval, bounds over all assigned roots | text line under the panels; the parent's primary on the next line | evaluator-only | "no root complete yet" |
| status counts | completed / failed / not started / pending of the assigned total; elapsed seconds | header | operational | always shown |
| accounting | stage calls, tokens, dollars; this model's ledger: calls, settled dollars, dollars against the cap | footer | operational | zeros before the first call |
| qualification (Q0) | per carrier profile: valid, field accuracy, exact rate, null on withheld | text table with the thresholds | evaluator-only | counts show what is missing |
| probe (P0) | interface checks, exactness, tokens per byte | text | operational | "not passed or not finished" |

- Time axis: completion order of recorded calls; no simulated time.
- Cadence: progress image at most every 20 s and at the end; replay of at most 11 frames, 500 ms each and 2.5 s on the last.
- History for replay: `episodes.jsonl.gz` (every row with `completion_index`, `elapsed_seconds`, ledger totals), `assignments.jsonl.gz`, `audits.jsonl.gz`.
- Artifacts per run: `initial_frame.png`, `progress.png`, `final_frame.png`, `replay.gif`, data files.
- Scripted frames carry "SCRIPTED PLURALITY RULE - NOT MODEL EVIDENCE".
- Validation (selftest): frames for empty, partial and complete scripted stages, Q0 and P0, and without truetype fonts; the replay GIF is decoded. After a run the operator compares the final frame with `analysis.json`.
- Rendering failure policy: a rendering error is recorded under `reporting_errors` in `summary.json` and changes no row or outcome.
