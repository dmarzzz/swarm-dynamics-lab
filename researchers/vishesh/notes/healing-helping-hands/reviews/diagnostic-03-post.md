# Post-mortem: diagnostic-03

- Experiment Healing Helping Hands / vishesh/codex-regrowth-docs / S0 diagnostic / 2026-10-04.
- Parent pilot-02; pre-run assessment diagnostic-03-pre.md; source d94aca856ec7e4d7469774dd5241d4a511d5dc0f.
- Disposition: diagnostic. No interface met the declared development acceptance criterion.

## What ran and what happened

54 planned calls, 54 started/terminal/graded/analyzed. Qwen neutral codes: 16/18 with class counts 6/6, 4/6, 6/6. Qwen thinking: 15/18 with 6/6, 6/6, 3/6. Laya explicit criteria: 14/18 with 6/6, 5/6, 3/6. No transport/schema failures or missing cells. Thirty-six Qwen and eighteen Laya calls; no paid API. Isolated host sim-vishesh, exclusive claim vishesh-healing-helping-hands. Exact runtime/tokens remain in the retained call journal and manifest.

Enabling reasoning recovered all negative development cases, but confused absent evidence with refutation. Neither model qualified for a broader sweep. Correct format and successful execution were insufficient.

## Visualization review

All classification records retained; a confusion matrix is the appropriate final view, not swarm motion. The measured exact-control replay from pilot-02 is separately available; it is not evidence from these diagnostic calls.

## Experiment-quality assessment

These are reused development probes. They diagnose interface sensitivity and cannot serve as held-out generalization evidence. The two-input claim/report presentation may anchor judgments on the asserted claim, especially when the report has no observation. This is a suspected cause, not established. A report-only outcome task is valid for this narrow corpus because every claim asks whether a measured accuracy improved; it would be invalid for arbitrary claims.

The 40 scattered memory erasures in pilot-02 were too easily repaired to discriminate robustness: erasure and no-event accuracy matched after the first exchange. Retain those observations; a later plan will add contiguous erasure and record post-erasure state before exchange to verify damage occurred.

## Failure and repair ledger

| ID | Evidence | Next diagnostic | Acceptance | Status |
|---|---|---|---|---|
| Q3 | Reasoning fixes negation but unknown 3/6 | Report-only measured-outcome interface | >=16/18 and >=5/6 per class; then fresh qualification | Open |
| L3 | Explicit criteria unknown 3/6 | Remove asserted claim from outcome classifier | Same | Open |
| S3 | Random erasure control is easy | Contiguous block erasure + pre-exchange measurements | Measured loss and delayed recovery relative to no-event | Plan required |

## Next run

Diagnostic-04 tests the report-only interface on the same development probes with the same unchanged acceptance threshold. If either fails, retain it as unsuitable and do not silently substitute a larger model. A further architecture change would require a distinct plan. The held-out corpus seeds remain untouched.
