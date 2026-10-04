# Post-mortem: fleet-s1-001

Experiment sybil-specialists / dmarz/sybil-specialists / S1 / 2026-10-04 UTC. Parent: fleet-s0-001. Pre-run: fleet-s1-001-pre.md. Disposition: complete-valid-result for the scripted exploratory pilot. No model-backed or confirmatory study has run.

## What ran and what happened

All 18 assigned S1 cells completed once: 864 planned → started → terminal → graded → analyzed arm outcomes, zero invalid, missing or duplicate attempts. Twelve paired world clusters (200–211), with dependent parameter cells; no holdout world used. Fleet S0 adds 256 repeated engineering outcomes, giving 34 runs and 1,120 arm records. Local S0 is a separate 256-record rehearsal and is excluded from the S1 estimate.

Frozen simulation revision e3caaf3d77bc46474f2b02145799c5f534adf225; design digest b7d0aa0ab82b03c9ec5ae705ec90a990c5e29e98c9fe5aa3859c2efcbecb210d. Analysis source d81c629bd6d09f930a7ea38d5e3a6642110812da. Runtime versions, all run IDs and claim metadata are in deployment.json. S0 occupied 47.1 seconds between first start and last finish; S1 occupied 123.3 seconds, excluding setup and later reporting/analysis. One worker, zero model calls/tokens and zero API spend.

The primary development difference (coverage minus degree, one bridge, attacker pass .10, budget four) is +.8333 rare accuracy and +.0833 malicious admission. The 12-cluster descriptive bootstrap interval for rare accuracy is [.5833, 1.0000]; this is not a powered confirmatory interval. Coverage means are .8611 rare accuracy and .1204 malicious admission; degree means are .0278 and .0370. At attacker pass .90 the coverage means become .2222 and .7685. The complete cell matrix and paired differences are in results-summary.json, including adverse outcomes. The risk increase exceeds the proposed .05 margin; there is no adoption recommendation.

## Visualization review

Mapping v1 produced 36 S1 PNG images and 18 GIFs (3, 5 or 9 logical frames). With S0 there are 68 PNGs and 26 GIFs. All images are 1800 × 1180. Every stored GIF frame count matches budget+1, every episode's final trace equals its final metric record, and every assigned world/arm tuple appears exactly once. All 230 copied run-artifact SHA256 digests match the authenticated hub.

The actual live browser loaded initial PNG, final PNG and animated GIF at full resolution. Playback was visibly observed; final-image ordering was checked for every run. The four-panel replay shows the first assigned world, not the cell average. The separate six-panel tradeoff figure uses means from every S1 cell, displays all four arms and labels synthetic status, 12 paired worlds and zero API calls. Nearby budget labels were separated after visual inspection, without changing values. Raw history remains on the hub and in the dedicated server checkout; the public live site exposes supported images only.

## Experiment-quality assessment

Execution completed and the scripted instrument passed qualification. The clean all-admitted ceiling, identical zero-check comparisons, degree preservation, matched communities, equal check budgets and uninformative-verifier control passed. The observed risk increase is a valid outcome, not a bug or a reason to tune away the result. Results depend on a small symmetric graph family, privileged honest seeds, fixed fabricated reports and externally specified probe reliability. Model clean competence is untested; no novelty or faithful published-defense comparison is claimed.

## Failure and repair ledger

No S1 execution or scoring failures occurred. Post-run code inspection found a latent orchestration mismatch: the generic reporter loop continued after a failed cell. The replacement loop propagates failure after the Run context records it. An injected-failure control verifies that no second assignment is taken. All 15 tests pass locally and remotely at installed revision dd99268244e3d48ce8750ea1e336709cfd0089c8 in verify-only mode; no replacement observations were queued. Existing 34 observations are unchanged. See worker-stop-diagnostic.md. S0 setup and display repairs remain documented in its own post-mortem.

## Next run

Scripted plan, simulator, UI replay, fleet deployment and aggregate analysis are complete. Stop workers after upload verification and release the claim. Any later batch at the revised worker commit must requalify exact-source S0. A model-backed extension requires the user's declared spending cap, a frozen model/prompt/packet-ordering plan and a fresh clean competence screen; it must remain separate from scripted results. Complete and independently review the prior-art survey, accept a reviewed hypothesis, add faithful published comparators and a second graph family before formal S2. These are scientific promotion requirements, not unreported execution failures.

## Closure

All 34 cell runs plus analysis-scripted-001 are done. The five analysis-file checksums also match the hub. The live UI displays the finished 34/34 experiment and loads the summary chart at 1800 × 1180. No worker process remained before the exclusive claim was released and merged as done. Reusable fleet hardware was returned to the owner’s pool; outputs remain on the hub and dedicated checkout.
