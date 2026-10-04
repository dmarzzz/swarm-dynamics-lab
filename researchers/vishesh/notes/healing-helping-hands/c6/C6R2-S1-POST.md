# C6R2 main: better classifiers, no benefit from agreement routing

TLDR: Haiku 4.5 and Jev completed all 432 synthetic evidence cases and 1,296 calls without an execution failure. Against frozen authored labels, Haiku A scored 419/432 (96.99%), Haiku B 416/432 (96.30%), and Jev 432/432. Agreement routing scored 419/432, equal to the fixed matched-random control. It referred only 3 cases and caught none of A's 13 errors. Its derived API cost was 35.95 times always-Jev. The predeclared utility conjunction fails. This is evidence about a narrow configuration and authored grammar, not general model superiority or a 200-agent swarm.

## Execution, qualification and scientific interpretation

The 60-case qualification passed before the fixed main stage: A60/B57/Jev60, all class floors satisfied. Frozen native source `204cfc5ebeafbc2d8c3ce5be9d169d3577b2fadb` and its [prospective plan](https://github.com/dmarzzz/swarm-lab/blob/204cfc5ebeafbc2d8c3ce5be9d169d3577b2fadb/researchers/vishesh/notes/healing-helping-hands/c6/PLAN.md) governed both stages. Main has no missing cases, retries, exclusions, invalid outputs or truncations. Both earlier interface failures remain separate ([first](C6-S0-POST.md), [second](C6R1-S0-POST.md)); they are not relabeled successful. Strict JSON schema and 64-token output cap succeeded in this cohort; one cohort does not establish universal reliability.

All 1,296 actual payloads, raw labels and scores were reconstructed from stored evidence. A separately implemented same-author reference calculation reproduced all family arithmetic and all 432 grammar labels. The assessor read all 29 individual wrong actor answers, their claim/report evidence, and 9 successful answers covering every class and actor role. This is owning review, not independent adjudication. [Audit](results/C6R2-S1/audit.json), [reference check](results/C6R2-S1/reference-check.json), and [rubric](results/C6R2-S1/scientific-post-mortem.json) retain the evidence.

There is no SUPPORT-label collapse in C6. Both Haiku passes share all 13 A errors; B has three additional errors. Disagreement routes those three cases where A was already correct, so error detection recall is 0/13. Referral reduction is 99.31%, but error versus Jev is +3.01 percentage points (fails the 2-point bound), improvement over the fixed matched control is zero, and error is 0.161 percentage points higher than the analytic same-count random expectation. These are fixed-case descriptive contrasts, not population estimates or powered noninferiority.

## Label quality limits the apparent accuracy gap

Twelve of A's thirteen misses occur in the `subgroup` SUPPORT template: the named task has higher measured accuracy, followed by “A different test showed the opposite result.” The intended gold treats that other test as irrelevant, but the text does not explicitly say it tested a different task or population. Haiku's UNCERTAIN answer is therefore defensible under a conflicting-evidence reading. A matching grammar parser reproduces the author's convention; it does not independently resolve semantic ambiguity. The previous answerability/label-validity assessment was too strong for this wording.

The remaining shared miss labels a withdrawn result with no replacement measurement REFUTE rather than UNCERTAIN. B additionally makes two absent-target-measurement errors in `subgroup` and one withdrawn-result error. These are visible semantic responses, not parser failures. No claim about hidden reasoning is warranted.

Primary results retain all frozen labels. A post-hoc sensitivity that excludes only the 12 ambiguous SUPPORT cases leaves A/cascade419/420 and Jev420/420 (0.238 percentage-point error gap); excluding the entire subgroup family leaves A/cascade395/396 and Jev396/396. Neither sensitivity is a new primary endpoint. The cost failure and absence of demonstrated routing benefit remain. An offline, explicitly scoped replacement-case proposal is recorded in [CASE-REVISION.md](CASE-REVISION.md); it is not native validation or a launched successor.

## Cost, latency and reproducibility

Main collection cost USD0.327131944: Haiku USD0.318277, Jev USD0.008854944. Derived deployment costs for all432 reports: Haiku A USD0.159131; always-Jev USD0.008854944; agreement routing USD0.318337186. The cascade includes BOTH Haiku passes and only its3Jev referrals; collection actually called all models to identify every comparator. Fewer Jev calls do not imply lower dollar cost. Summed call time was Haiku701.120s and Jev91.754s; serial collection is not a randomized production-latency trial.

All C6 attempts, including both failures, cost USD0.376066420. The original study ledger's settled model charges are USD0.428065318, plus USD0.001344 historical unresolved exposure, inside the owner's USD50 cumulative ceiling and USD3 C6 envelope. An existing allocated machine was reused; no new resource was provisioned. Final ledger/allocation reconciliation is linked from the README when complete.

Haiku's actual returned model is the requested `anthropic/claude-haiku-4.5` alias with Anthropic-only routing; the route advertised `anthropic/claude-4.5-haiku-20251001`. These are distinguished, not represented as independent proof of immutable hosted weights. Jev returned `typesafe/jev-1.13-20260917`, TypeSafe-only. Both Haiku passes are dependent order variants with stateless claim/report-only contexts. Legacy score key `qwen` denotes Haiku A here; no Qwen call occurred. Source, exact requests, raw outputs, usage and timestamps are retained.

## PI assessment and disposition

The experiment now executes reliably within its tested contract, exposes actual costs and preserves failure history. Its most useful lesson is that stronger classifiers do not make agreement a useful error detector: the two passes can share the same mistake or interpretation. Always-Jev is the better measured model policy on these fixtures. The same-input grammar parser also solves them, so they do not establish that language models are necessary.

The main design weaknesses are twelve authored, inspected grammar families rather than independent real documents; largely ceiling-level controls; a substantive ambiguity concentrated in the error-bearing family; and label-order variation that provides little diversity. The432nestedcases and1,296calls are not independent real-world samples. Historical Qwen comparisons confound model, interface and cohort; they cannot identify a model-only causal effect.

Decision: **FINISH / PARK this routing policy.** Publish the finite negative result, preserve both failed attempts and complete resource closeout. A useful successor would need explicit target scope, genuinely distinct evidence perspectives, independently adjudicated natural reports and a cost-competitive comparator. No further model calls are justified solely because budget remains. Any materially new successor requires its concrete prospective plan decision.

![Error and cost](results/C6R2-S1/figures/outcomes.png)
![Family sensitivity](results/C6R2-S1/figures/family-errors.png)

[Recorded response replay](results/C6R2-S1/figures/replay.html) shows all1,296 observed responses in arrival order. It animates recorded data, not200concurrentagents or emergent cooperation.
