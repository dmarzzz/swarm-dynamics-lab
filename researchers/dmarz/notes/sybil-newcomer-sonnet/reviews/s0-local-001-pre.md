# Pre-run assessment: s0-local-001

- Experiment / owner / stage: sybil-newcomer-sonnet / dmarz / local scripted S0 (offline, zero model calls).
- Parent attempt and previous post-mortem: first attempt of this study; parent study [sybil-newcomer-api s0-local-003 post](../../sybil-newcomer-api/reviews/s0-local-003-post.md) and [S1 post](../../sybil-newcomer-api/reviews/s1-001-post.md).
- Status: ready.
- Question and practical decision this run informs: is the copied instrument intact after the replication edits (identifier, model id, prices, banner, own ledger)?
- Expected finding: 198/198 valid scripted observations and passed scripted qualification, as in the parent. Uninformative if the edits touched the simulator or assignments; checked separately by assignment digests.

## Design and assessment

- Closest evidence: the parent's passing local and fleet S0 on identical simulator code.
- Units: engineering worlds 6900–6901 plus the 36 qualification packets; the scripted plurality synthesizer stands in for the model.
- Truth separation and controls: unchanged; selftests cover policy blindness, deterministic resources, observed-state updates and malformed billed answers.
- Primary metric: structural validity and scripted qualification pass; no scientific interpretation.
- Timing: simulated rounds only.

## Changes and unresolved issues

| Issue / prior evidence | Change or diagnostic | Expected effect | Acceptance check | Owner |
|---|---|---|---|---|
| Model replication | model id, prices, identifier, banner | none on scripted path | 8/8 selftests; 198/198 valid | dmarz/newcomer-sonnet |
| Shared two-study partition belonged to the parent's allocation | removed; own ledger | none on scripted path | selftest duplicate call refused by study ledger | dmarz/newcomer-sonnet |
| A pre-commit smoke run of the same command was executed before this assessment was written and discarded | rerun under this assessment | identical outputs | summary counts and source hash match | dmarz/newcomer-sonnet |

## Frozen execution plan

- Code at the commit carrying this file; Python 3.12 venv with pinned requirements; `python3 src/worker.py --stage S0 --attempt s0-local-001`.
- 0 model calls, $0. Any invalid observation fails the attempt.
- Local runtime only; outputs stay in git-ignored `results/`.
- If it fails: diagnose against the parent source diff; no fleet stage until it passes.

## Visualization mapping

Inherited mapping v1 ([VISUALIZATION.md](../VISUALIZATION.md)), bound to attempt s0-local-001 and its source hash. Inspect initial, final and 8-frame replay for the SONNET banner change only.
