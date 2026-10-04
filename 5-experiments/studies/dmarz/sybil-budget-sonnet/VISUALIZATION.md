# Visualization mapping v1 (sybil-budget-sonnet)

Inherits [sybil-budget-api mapping v1](../sybil-budget-api/VISUALIZATION.md) by version. The renderer `src/render.py` is unchanged apart from the model label (`SONNET 4.6`). The mapping is bound to sybil-budget-sonnet S0/Q0/S1, the runtime hash in every run, and per-row world and cell IDs (`task`, `n`, `arm`, `checks`, `attacker_pass`).

Run-specific bindings:

- The layout is the same as the parent's: random and coverage side by side; N=324 and N=972, accuracy and seats panels vertically; `retention.png` shows retention and accuracy.
- S0 frames say SCRIPTED. Q0 shows N=324 and N=972 competence blocks (8 clean packets each).
- Live `progress.png` is uploaded at most every 20 seconds. Final frame, retention frame and a 25-frame GIF of measured completion-order prefixes are uploaded at stage end. Raw histories (`episodes.jsonl.gz`, `assignments.jsonl.gz`, `worlds.jsonl.gz`) are retained for replay and recomputation.
- Cross-cohort view (post-run reporting only): Sonnet-minus-Haiku accuracy heatmaps over budget × reliability for each size and policy, computed from the saved records of both cohorts. It makes no model calls and is labelled with both run IDs.
- Missing and failed cells are explicit (pending blank, failed counts shown). Nothing is interpolated. Evaluator-only truth never enters actor inputs.
