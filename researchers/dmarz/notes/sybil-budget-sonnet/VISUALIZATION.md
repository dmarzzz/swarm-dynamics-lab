# Visualization mapping v1 (sybil-budget-sonnet)

Inherits [sybil-budget-api mapping v1](../sybil-budget-api/VISUALIZATION.md) by version, with the renderer `src/render.py` unchanged apart from the model label (`SONNET 4.6`). Bound to sybil-budget-sonnet S0/Q0/S1, the runtime hash in every run, and per-row world/cell IDs (`task`, `n`=972, `arm`, `checks`, `attacker_pass`).

Run-specific bindings and differences from the parent mapping:

- Only N=972 exists, so the main frame has two panel rows (accuracy and attacker seats) instead of four; the lower half of the 1920×1440 frame is empty by design. `retention.png` shows retention and accuracy.
- S0 frames say SCRIPTED. Q0 shows one N=972 competence block (8 clean packets).
- Live `progress.png` is uploaded at most every 20 seconds. Final frame, retention frame and a 25-frame GIF of measured completion-order prefixes are uploaded at stage end. Raw histories (`episodes.jsonl.gz`, `assignments.jsonl.gz`, `worlds.jsonl.gz`) are retained for replay and recomputation.
- Cross-cohort view (post-run, reporting only): a Sonnet-minus-Haiku accuracy heatmap over budget × reliability for each policy, computed from saved records of both cohorts. It is produced by `reporting/` after S1, makes no model calls, and is labelled with both run IDs.
- Missing and failed cells are explicit (pending blank, failed counts shown). Nothing is interpolated. Evaluator-only truth never enters actor inputs.
