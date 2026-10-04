# Pre-run assessment: s0-local-001

- Experiment / owner / stage: sybil-budget-sonnet / dmarz (operator dmarz/budget-sonnet) / local scripted S0 on orbital-one, offline, no model calls.
- Parent attempt: none for this study. The parent study's [s0-local-002-post](../../sybil-budget-api/reviews/s0-local-002-post.md) and [fleet S0 post](../../sybil-budget-api/reviews/fleet-s0-001-post.md) passed on the identical simulator, packet code and evaluator.
- Status: ready (software check of the copied instrument).
- Question: does the copied instrument, restricted to N=972, generate the full scripted grid and clean controls without invalid rows, and render frames?

## Design and assessment

S0 assigns 2 engineering worlds (6800–6801) × 60 cells, plus 8 clean controls at N=972. The scripted plurality backend replaces the model. Acceptance: every row valid, the clean controls pass the qualification thresholds, and initial, final and replay frames render with the SCRIPTED label. Low attack-cell accuracy is not a failure. The selftests, including the parent-pairing test, must pass first.

## Changes and unresolved issues

| Issue | Change | Expected effect | Acceptance check | Owner |
|---|---|---|---|---|
| Sonnet cohort | model/prices/caps, sizes=[972], own ledger | none on scripted S0 | selftests pass; S0 grid all valid | dmarz/budget-sonnet |

## Frozen execution plan

Source as committed; `python3 src/worker.py --stage S0 --attempt local-s0-001`. 0 calls, $0. Outputs go to the git-ignored `results/local-s0-001/`.

## Visualization mapping

[Mapping v1](../VISUALIZATION.md). S0 frames are labelled SCRIPTED. Initial, final and replay frames are checked for size and decodability.
