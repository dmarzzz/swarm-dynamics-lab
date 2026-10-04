# Pre-run assessment: s0-local-002

- Experiment / owner / stage: sybil-budget-sonnet / dmarz (operator dmarz/budget-sonnet) / local scripted S0 on orbital-one, offline, no model calls.
- Parent attempt: [s0-local-001](s0-local-001-post.md), which passed on the superseded N=972-only design.
- Status: ready (software check of the amended full-grid instrument).
- Question: does the full 120-cell instrument generate the scripted grid and clean controls at both sizes without invalid rows, and render frames?

## Design and assessment

S0 assigns 2 engineering worlds (6800–6801) × 120 cells plus 16 clean controls. The scripted plurality backend replaces the model. Acceptance: every row valid; clean controls pass per size; initial, final and replay frames render with the SCRIPTED label; selftests (10/10) pass.

## Changes and unresolved issues

| Issue | Change | Expected effect | Acceptance check | Owner |
|---|---|---|---|---|
| N972-only subset | sizes restored to [324, 972]; caps 3,200 calls / $400 | full parent grid | selftests; S0 256 rows all valid; parity receipt | dmarz/budget-sonnet |

## Frozen execution plan

`python3 src/worker.py --stage S0 --attempt local-s0-002`. 0 calls, $0. Outputs go to the git-ignored `results/local-s0-002/`.

## Visualization mapping

[Mapping v1](../VISUALIZATION.md). S0 frames are labelled SCRIPTED and checked for size and decodability.
