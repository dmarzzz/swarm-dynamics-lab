# Feedback incorporated into C5

This records the owning assessment of existing feedback; it is not an independent reviewer sign-off. Sources: [design transfer](../c4/DESIGN-TRANSFER.md), [case-quality assessment](CASE-QUALITY.md), [C4 trace failure](../c4/S0-POST.md), and [C5 S0 trace review](S0-POST.md).

| Feedback | Disposition and evidence |
|---|---|
| Qualification must lead to a main run within the approved scope | Implemented `advance.py`, source-bound authored review, no duplicate dispatch and no additional approval prompt. S0 qualified and S1 was actually dispatched once. |
| Register the plan before collection and preserve process failures | Immutable C5 plan publicly registered before S0; inherited C4 URL predicate was caught and repaired before dispatch. C4 leakage and historical transport/archive failures remain separately recorded. |
| Agreement is not calibrated correctness | Main endpoints include wrong accepted answers and error-detection recall. S0 directly shows23 wrong agreements and0/23 A errors detected; no claim that two variants are independent votes. |
| Use strong, resource-matched controls | Always-Jev, Qwen A, same-count per-family random referrals and analytic uniform-random expectation. No extra capacity sweep or added evidence hidden in the contrast. |
| Measure absolute quality and both cheap passes | Assigned error, confusion, per-family safety/matched deltas and both Qwen calls/time/tokens; counterfactual referrals distinguished from all-controls collection. Local compute is not assigned a zero dollar cost. |
| Test enough meaningful cases without inflating independent n | Twelve authored semantic families with36 nested instances each; fresh main assignments. This is finite feasibility, not432 independent language tasks or a powered2pp noninferiority study. |
| Prevent context leakage and preserve exact traces | Opaque names; complete serialized payload mutation tests; actual S0 requests and72 visible responses across all24 miss instances reviewed. Pinned Qwen and Jev snapshots, no fallback or response retry. |
| Make visualizations truthful and inspectable | Per-family error heatmap, all-arm tradeoff, exact saved-input/answer inspector. Reviewed tile reveal wording states family grouping and does not imply autonomous cooperation or chronological diffusion. |

Remaining limits do not justify changing this running main stage: synthetic realism, same-author scoring/audit, dependent templates, poor Qwen performance and uncertain total production cost. The main result may reject this routing rule. A later real-document transfer, learned router, different model or larger independent sample would be a materially new design requiring its own concrete decision, not an automatic retry.
