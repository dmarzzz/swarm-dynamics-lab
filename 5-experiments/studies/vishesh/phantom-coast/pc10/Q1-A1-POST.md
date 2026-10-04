# PC10 Q1-A1: clarification did not change inspection choices

2026-10-04; owning assessment vishesh/codex-phantom-coast. **FINISH / PARK this qualification path.** Execution completed, clarified qualification failed, scientific review complete. All16 calls returned valid responses, no missingness/retry/fallback. The owner-approved paired diagnostic used source `32ad01d2c11e1bd997728e04a071ba1b10cc3d0b`. No population rollout or S1 pilot occurred.

## Result against the plan

| Measure | Original wording | Explicit individual control |
|---|---:|---:|
| Valid responses |8/8|8/8|
| Correct map labels |32/32|32/32|
| Optimal inspections |4/6|4/6|
| Mean expected regret across six proposals |.0041667|.0041667|
| Clarified qualification gate |Not the gate arm|Failed|

All six matched inspection choices were identical, including the two misses. No wrong-to-right or right-to-wrong transitions occurred; four action pairs were correct in both conditions and two wrong in both. Both no-action final-map cases were correct in both conditions. Individual map labels were identical across all eight pairs, not merely equal in count.

The positive and negative private-report cases selected the reported site rather than a wholly unknown one under both wordings. Mean expected regret was.0125 for each such choice: report verification leaves optimal expected total loss.50 versus.45 after choosing an unknown site first (.125 versus.1125 across four sites). This is the finite-horizon individual reference's expected loss, not observed rollout loss. All tied optima were accepted. Independent world/action-tree enumeration agrees with the reference for every first action.

Every one of the16 effective request/answer records was inspected, including all four wrong-action responses. In the positive pair, chosen-site probability/confidence changed from.59/.45 to.65/.53; in the negative pair, from.74/.65 to.64/.52. Probabilities changed while actions did not. These are visible output fields, not hidden reasons or calibrated confidence measurements. Corrections, uncertainty and nonrepeat choices remained correct under both wordings.

## Interpretation and PI critique

The explicit individual-control wording did not rescue the observed action errors. The original ambiguity is repaired in the clarified arm, and this run does not support ambiguity alone as the explanation for the previous mistakes on these templates. It also provides a useful negative finding: this model interpreted the evidence accurately yet did not choose the loss-optimal next observation in the two privately reported cases.

Do not overstate the null. Eight author-known templates, six action pairs, two report-sign mechanism cases and one response per condition cannot establish general wording invariance, an equivalence bound or intrinsic planning incapacity. The added text simultaneously specifies control, whose loss matters and future evidence arrivals; it is a composite clarification, not an isolation of each clause. Conditions were counterbalanced4/4 and evidence matched, with independent calls, but hosted execution is not guaranteed deterministic. Known templates and deterministic public seeds are not independently authored holdouts.

The model actively verified the report under both signs; these observations do not show a self-sealing avoidance trap. Neither snapshot qualification nor the scripted population replay establishes truth poisoning in a free-running swarm. All eight pairs are now released development data. Keep the failed PC9 and PC10 gates intact; do not tune repeatedly until qualification passes or interpret correct maps as optimal exploration.

## Process, accounting and reporting

A zero-call public-plan preflight stopped on a heading mismatch: the shared checker requires “Metrics,” while the draft used “Metrics and stopping.” The heading was corrected and a public-contract regression test added before dispatch. Scientific scope, inputs, thresholds and spending envelope were unchanged. The new immutable plan was registered, fetched/hash-checked and verified on the rendered public page; all14 tests passed on the deployed clean Python3.12.3 runtime. The initial preflight was not a model attempt and consumed no API cost.

The previous approved-account host was verified idle and exclusively claimed. The closed PC9 ledger bytes matched the pinned digest; its old canonical path was fenced before creating the sole continuation. Model credentials remained in the authorized local consumer; the dedicated worker exchanged only requests/responses through verified SSH stdin. Safe typed outputs, original response digests,32 START/terminal events and all16 assignments reconcile with the saved audit. No arbitrary provider error bodies were published. Researcher review was not required by owner direction.

New API cost USD0.001016736; cumulative known USD0.847742490; conservative exposure USD0.859838490 including unchanged nine historical uncertain calls totaling.012096. No new uncertain charges, machine or incremental infrastructure. Original total5/API4/infra1 unchanged. Operational reporting/readback, ledger backup, worker stop and allocation release are recorded separately in CLOSEOUT.json. Offline finalize supplies an operational scaffold; QUALITY.json supplies the authored scientific review.

## Next-session disposition

Park this clean-planning qualification path and do not launch the existing pilot. The ambiguity-only diagnostic is answered narrowly: no decision improvement on these matched cases. Further prompt polishing has no demonstrated value. If the owner wants to pursue population misinformation, first choose a new scientific objective offline: descriptive population behavior without optimal-planning claims, or evidence interpretation with an exact inspection controller. Those are different experiments with different estimands; neither is a continuation automatically admitted by remaining budget. No successor, model switch or retry is queued.
