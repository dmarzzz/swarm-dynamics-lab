# QM-2 design review and issue ledger

2026-10-04. Author: vishesh/codex-quorum-mirrors. This is the implementing agent's assessment, not independent review. Status: **offline contracts validated; native experiment blocked**. No run was attempted, so this is not a model-run post-mortem and is not retrospective preregistration.

## Inputs and freshness

Pulled dmarzzz/swarm-lab main successfully; initial inspected commit c1aca0b29b7f5fca0e84f32aef0373563341fde3. Read AGENTS.md, researcher directives/inbox, status/task matches, DM-02 handoff, REIMAGINING, RD-1 plan, run-review and visualization requirements, and the decision-models survey. Also used the workspace review `review-2026-10-04/scientific-phantom-quorum.json`, specifically SCI-QUORUM-OF-MIRRORS. The critique's concrete requirements are reproduced in the ledger below so the design does not depend on access to that local file. No new literature search/full reading or novelty certification is claimed. Feedback outside the fetched repository and supplied workspace was not audited.

The existing handoff explicitly states that this project has no native qualification or scientific outcome. Searches found adaptive-quorum work but no DM-02 outcome to rescore. Therefore the request to resolve previous run failures becomes design/instrument repair here; no other project's results are repurposed.

## Assessment against the earlier plan

The prior handoff had the right distinctions—source count, decision-maker count and rounds—but left their actual comparison undefined. QM-2 fixes three roots, nine reports, five judges and two rounds; balanced versus skewed repetition isolates multiplicity. Changing the number of independent sources is now reserved for the separate acquisition study.

The biggest new design correction arose during offline review: hiding only one root makes capping its descendants reproduce that root's exact likelihood term. The partial-lineage condition now hides two roots. The cap then trades off suppressing repetition against suppressing real evidence; its failure is visible in a negative-control fixture. This change was made before any model calls or reserved seed generation. The plan's original pre-implementation commit is f4e8aff; the amendment is dated in the plan. Neither version is a registered run.

The revised design deliberately distinguishes a source-aware instruction experiment from a deterministic deduplication benchmark. Both native arms use the same committee rule and factual packet. Exact accumulation is a comparator, not hidden assistance to the model. The pooled reference uses fewer calls and is labelled accordingly.

## Issue ledger

| ID | Evidence / gap | Change and acceptance evidence | Status |
|---|---|---|---|
| QM-01 | Proposal had no source-dependence generator | Explicit conditional Bernoulli roots, report ancestry and multiplicities; hand-derived posterior and duplicate-invariance tests | Specified and narrow reference validated; generator/manifest not implemented |
| QM-02 | Overlap change could also buy new evidence | Three roots and nine slots in both repetition conditions; budgets stated independently | Design resolved; native budget audit pending |
| QM-03 | A defense could receive oracle-only ancestry | Actor serializer allowlist, hidden-root renaming invariance, rejected evaluator fields, indistinguishable visible packets | Offline reference validated; full native prompt boundary pending |
| QM-04 | Full ancestry makes defense trivial; partial case underspecified | Two concealed roots, visible-only and capped baselines, ambiguity and harmful-capping fixtures | Design/reference validated; real model behavior unknown |
| QM-05 | Source labels mistaken for independence | Disclose conditional independence assumption; exact oracle limited to it; common-cause robustness deferred explicitly | Scope bounded; external validity unresolved |
| QM-06 | Abstention or failure could improve selected-answer scores | All-assigned denominator, fixed five-slot quorum, missing probabilities remain unavailable, wrong unanimity requires five valid responses | Offline scoring checks pass; operational status/usage instrumentation pending |
| QM-07 | Confidence treated as calibration | Separate raw probability diagnostics and Brier denominator; independent calibration split reserved | Design only; calibration not performed |
| QM-08 | Pooled/no-discussion budget parity unclear | Round-0 no-discussion diagnostic; pooled actual two-call cost, main arms ten calls; 88 calls/world ledger | Design only; latency/token accounting pending |
| QM-09 | A designated right dissenter would reveal truth | Fresh evidence naturally noisy; correct/incorrect branches require natural sampling or proper weighting; no truth label to actor | Deferred extension, not claimed repaired implementation |
| QM-10 | Attractive replay could substitute for complete results | Versioned field-to-visual mapping, all-assigned counters, failure states and saved-event-only rendering | Specified; native renderer/playback unavailable |
| QM-11 | No documented previous DM-02 runs | Preserve unrun status; distinguish adaptive-quorum | Evidence identity resolved |
| QM-12 | Launch preregistration/research/host/budget absent | No live entry point; gates listed explicitly; zero spend | Blocked for native execution |

## Validation and limits

Fourteen standard-library unit tests pass after the two-hidden-root amendment. They check hand-derived probabilities; naive duplicate amplification; full-lineage invariance; opaque-lineage tradeoffs and observational ambiguity; actor-field isolation; invalid ancestry; label/order symmetry; strict responses; fixed quorum; all-assigned scoring; unavailable probability handling. An alternative-ancestry ambiguity fixture intentionally changes true root count and is labelled outside the QM-2 generator. These are manually constructed development fixtures, not stochastic worlds or scientific observations.

No qualification, calibration or held-out seeds were generated. No model, fleet host or credentials were used; paid calls and spend are zero. Reference code has no native launch function. The artifact does not yet implement world sampling, prompt serialization, provider retries, frozen manifests, receipt enforcement or replay. Passing these tests cannot authorize a model run.

Repository validation: `scripts/lab.py check` reports zero errors and five pre-existing missing-library-link warnings. Exact code hashes and final test output are retained in VALIDATION.json. Plan commit precedes reference implementation; the in-development amendment precedes any native execution.

## Next action

Continue with the decision-models prior-art survey: the actual gate reports 0/5 full-paper reads and 0/8 structured search rounds, with search-category coverage absent. Complete honest reading/search records, then obtain the required independent survey/hypothesis review. This session has not manufactured those records or impersonated another researcher. A bounded diagnostic exception, if explicitly authorized later, must remain separate from formal study approval.

Before dispatch, implement and review the generator, prompt adapter, assigned-case ledger, request-boundary tests, immutable public-plan registration enforcement and saved-event renderer. Then freeze a concrete qualification manifest with model identity, counts, retries, timeout, token/call ceilings and dedicated host receipt. Request an experiment-specific spending cap for that concrete manifest. Neither another experiment's cap nor the handoff's phrase “a hundred” supplies one. Publish/register/verify the condition-specific plan and obtain an exclusive allocation before any run. Each actual attempt then receives a pre-run assessment and post-mortem.

The practical result of this iteration is a reviewable comparison with verified elementary contracts. Scientific value remains contingent on qualification and native outcomes; null effects, simple deduplication success or harmful capping are acceptable findings.
