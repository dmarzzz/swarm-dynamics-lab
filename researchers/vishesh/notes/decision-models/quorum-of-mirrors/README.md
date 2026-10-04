# Quorum of Mirrors: when nine reports are only three observations

**Latest: quote-only SP-02 repair passed.** SP-02 quote-only repair qualification passed: 40/40 valid calls; 120/120 source and 280/280 report selections correct; 40/40 decisions; 20/20 exact paired roots. Native quotations and code-derived facts are distinct. New API cost USD0.314064; authored grammar only, not field reliability or swarm efficacy. SP-01's earlier null-selection gate remains failed. [Results and limits](reviews/SP-02-post.md).

**Previous PQ-01:**24/24 final decisions correct, but only11/24 exact fidelity sets, with18 false flags on faithful reports. That adverse finding remains unchanged. [PQ-01 report](reviews/PQ-01-post.md).

**Does a group get better evidence when more agents agree—or can it just repeat the same source more loudly?** Quorum of Mirrors tests whether preserving source ancestry helps a group make better decisions when reports overlap.

Imagine an incident desk receives nine reports: seven copy one inspection saying “safe,” while two independent inspections say “unsafe.” Counting reports says safe, 7–2. Counting independent observations says unsafe, 2–1. Adding judges does not add inspections. This is an illustrative use case; the actual inputs are synthetic binary sensor reports with explicitly declared reliability.

The practical decision is whether to invest in **more judgments, better source tracking, or a simple deduplication rule**.

## What has actually run

The repaired **Q1 context screen completed all 16 calls with valid responses, but got 0/8 full-lineage decisions right** (required: at least 7/8). Every choice matched report majority even when copies should count once. Partial-lineage cases were interface checks, not accuracy tests. The [Q1 repair report](reviews/Q1-02-post.md) distinguishes the fixed output-token bug from this valid negative result. The larger committee experiment remains unrun; trustworthy source deduplication in code remains the practical baseline.

The earlier reader screen, **S0**, completed. One model reads each packet with full source IDs and explicit deduplication instructions. There are eight bit triples at two reliability settings, each requested twice: 16 configurations, 32 calls. No agents talk to each other in S0; the swarm comparison is still pending.

| Method | Correct exact-MAP choices on saved inputs | Evidence type |
|---|---:|---|
| Native reader, with source instructions | 29/32 | Observed model calls |
| Count every report | 24/32 | Retrospective deterministic calculation |
| Count each known source once | 32/32 | Retrospective deterministic calculation |

“Correct” means choosing the more likely hidden state given the evidence, not matching a sampled hidden truth. The two computed references are not randomized model arms. The screen passed its predeclared competence thresholds, but all three non-correct responses occurred in the eight calls where report majority and source majority conflict: **5/8 correct there, versus 24/24 elsewhere**. That diagnostic split is retrospective.

## What these results are useful for

For this simple grammar with complete, trustworthy source IDs, an exact deduplication rule already solves the task without model calls. The evidence supports using that rule as an engineering baseline before paying for a committee. It also identifies conflicting copied evidence as a useful stress case for qualification.

We have not established that source-aware instructions improve a model, that discussion helps, or that a swarm beats one solver. Missing or unreliable ancestry, semantic paraphrases, common-cause errors and real incident decisions remain untested. The model’s raw choice scores are not calibrated truth probabilities. These repeated finite patterns cannot establish general reliability.

**Explore the evidence:** [all 16 saved cases](analysis/iteration-3/cases.html) (download/open the HTML for interaction), [auditable comparison data](analysis/iteration-3/comparisons.json), [results and plan evaluation](RESULTS.md). The explorer shows all nine reports, their three visible roots, both voting rules and both actual model responses; it invents no swarm dialogue.

## Current decision: use the rule and close this cycle

The [saved-data decision audit](analysis/pi-cycle/RESULTS.md) confirms the model's 0/8 result but cannot distinguish copied reports from misleading prior choices: both majorities point to the same wrong answer in all eight graded cases. That mechanism remains unresolved.

For this grammar, source deduplication followed by exact arithmetic already determines the answer. Nine new tests and 5,488 exhaustive software configurations verify the rule's declared scope and refusal boundaries; these are not additional model trials. [Inspect every graded case](analysis/pi-cycle/cases.html).

**The prepared D1 diagnostic is parked, with zero new calls.** Whether deduplication helps the model, priors harm it, or qualification fails, the practical choice remains exact source arithmetic. D1 would add explanation without changing that decision. No M1/C1 or replacement qualification is launched. Unknown/false provenance, semantic matching and real-world generalization remain outside the evidence; native swarm-efficacy confidence remains 1/4.

## Robustness improvement: verify the source mapping

[The new provenance gate](provenance/RESULTS.md) closes an important engineering assumption: claimed labels can split one observation into several apparent sources or merge distinct acquisitions. It checks each observation against an externally authenticated receipt registry, counts actual acquisition IDs, and abstains on missing or conflicting evidence. **23 relevant software tests pass; this is not additional native model evidence.** [Inspect the six constructed cases](provenance/examples.html).

A useful future native task is matching ambiguous natural-language reports to authenticated receipts. It needs a validated corpus, held-out acquisition families and strong exact-lookup/string-matching controls before model qualification. Those requirements are not met yet, so no machine or new model run was launched. The gate does not itself authenticate the registry or establish statistical independence.

## Trace-grounded reassessment

Trace audit reconciles all 96 assigned slots: 49 started, 48 retained answers, one discarded response and 47 unstarted. S0/Q1 schema and instruction changes prevent causal attribution to priors alone. The strongest simple baseline resolves all 15 answerable bundles in 24 authored development fixtures, with nine correct abstentions; this is in-sample, not generalization. The conditional semantic proposal stops at the unmet corpus/headroom gate. No native calls, allocation or spending. [Read the review](trace-review/RESULTS.md) and [concrete conditional next-run design](trace-review/PROPOSAL.md). The proposed eight qualification and 24 evaluation calls are neither admitted nor launched.

## Improved test cases

Completed 24 paired development cases across 12 authored roots; nine checks pass. The revised contract separates authenticated origin from untrusted text/reference claims and dependency admission. Exact graph traversal solves all 24; frozen legacy failures reflect changed trust assumptions, not model headroom. No new native calls, allocation or budget mutation. [Good versus bad cases and assessment](case-design/RESULTS.md); [inspect all 24 cases](case-design/CASEBOOK.md). Origin does not certify content fidelity or statistical independence. These cases remain development-only.

## Does a copied report preserve the finding?

Added 32 claim-fidelity development cases across eight authored source scenarios, separating SUPPORTED, CONTRADICTED and NOT_ESTABLISHED while holding source binding fixed. Eight checks pass. Literal matching and lexical overlap both score 16/32, but overlap falsely supports seven claims. Limited lexical diagnostics do not establish semantic model headroom; a capable compositional baseline and independently varied cases remain necessary. [Inspect the cases](claim-cases/CASEBOOK.md) and [assessment](claim-cases/RESULTS.md). These synthetic cases are inspected development data, not native results or held-out evidence.

## Cases ready for a controlled repetition/distortion experiment

Packet-study v2 cases are ready for the declared bounded synthetic repetition/distortion experiment: 48 development packets/12 roots, 24 sealed qualification packets/6 roots and 96 sealed evaluation packets/24 roots. Strong text parsing plus source counting agrees with every construction label; ten tests pass. V1 qualification imbalance was caught and retired before native use. Fixed grammar and same-operator authorship limit generalization; native qualification and run admission remain separate and not granted. [Inspect development packets](packet-study/DEVELOPMENT.md) and [read the readiness assessment](packet-study/RESULTS.md). This is case preparation, not a new model result or swarm-efficacy finding.

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-quorum-mirrors; source `567cda03` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — Quote-only evidence selection plus deterministic normalization passes authored qualification; field reliability and swarm efficacy remain untested. Basis: S0 passed its narrow reader screen. The repaired Q1 produced 16 valid responses but 0/8 correct full-lineage choices; all choices aligned with report majority. Finite scripted fixtures do not establish causal peer influence or swarm efficacy. Saved-data audit confirms report/prior-majority confounding in all eight graded cases. Exact-rule software verification is not native evidence; D1 is parked because its outcomes do not change the current engineering decision. A receipt-grounded gate now has adversarial software checks; this neither authenticates provenance nor adds native evidence. Full native trace audit covers 96 assigned slots and identifies additional schema/instruction confounds. A tuned hybrid solves all 24 authored development bundles in-sample; no semantic model headroom or new native evidence is demonstrated. A second 24-case development suite separates authenticated origin from similarity and untrusted references; exact graph traversal solves all cases. This is software contract validation, not native headroom or generalization. Another 32 authored claim-fidelity variants across eight source scenarios expose lexical false support; these limited controls do not establish semantic model headroom or add native evidence. Packet-study v2 now passes scoped offline case-quality checks with a strong source-text parser and sealed qualification/evaluation corpora. This adds no native evidence or generalization claim; retired v1 qualification imbalance is preserved. Separate Sonnet packet qualification QM-PQ-01 returned 24 valid/correct final decisions and 72 correct source votes but failed fidelity at 11/24 exact distortion sets, with 18 false-positive faithful report flags. Six synthetic roots; no evaluation or causal cross-model improvement claim. Separate PQ-02 explicit-fact follow-up stopped at HTTP400:24 assigned,2 started,1 fully correct valid response,22 unstarted. Native qualification remains unestablished; safe-error telemetry gap documented. No completed pairs or new efficacy claim. Separate PQ-03 fixed-array qualification completed24/24 with noHTTPerrors and passed declared gates:24 decisions/classification sets correct,72 source facts,119/120 report facts. Twelve authored paired roots, one report assertion/status error; no causal transport diagnosis or generalization claim. Separate PQ-04 tightened component/quote gates and separated report assertions from source evidence.8/8 calls passed:24 sourcefacts,32 reportclaims,all labels/decisions;four paired roots preserved claims and correctly switched toDEFER without decisive evidence. Four authored roots and a perfect grammar parser do not establish general reliability or model superiority. R1 passed all ten qualification calls, then stopped after 25 of 40 evaluation calls: 24 valid, one unknown/value contract failure, 15 unstarted. All 24 scored decisions were correct, but one concealed a source-value error; 23/24 scored packets were fully exact. New API cost USD0.458142. The larger test did not establish robustness; original failures and missing cases remain intact. SP-01 span-selection qualification did not pass: 40/40 valid calls, 105/120 source selections, 280/280 report selections, 40/40 decisions and 11/20 exact paired roots. New API cost USD0.310122. Values/status/modes are derived by code from native selected clauses, not predicted by the model. Controlled authored grammar only; no field or swarm efficacy claim. SP-01:40 correct decoded outcomes but15 null-selection misses; strict gate remains failed. SP-02 quote-only repair qualification passed: 40/40 valid calls; 120/120 source and 280/280 report selections correct; 40/40 decisions; 20/20 exact paired roots. Native quotations and code-derived facts are distinct. New API cost USD0.314064; authored grammar only, not field reliability or swarm efficacy.
- **sample_size_summary:** S0:29/32 correct. Q1-02:0/8 graded. PQ-01:11/24 fidelity sets. PQ-02:1 valid/1 HTTP400/22 unstarted. PQ-03:119/120 reportfacts. PQ-04:8 exact calls. R1:10 qualification exact;24 valid evaluation/23 exact/1 invalid/15 unstarted. SP-01:40 valid,all decoded facts/decisions,25 exact packets under null rule. SP-02:20 paired roots/40 assigned,40 valid,20 exact pairs,source120/120/report280/280. Old96 evaluation unused.
<!-- experiment-evidence:end -->

## Reproduce and inspect

From this directory, `python3 reassess_s0.py` regenerates the retrospective data and explorer using only saved inputs; `python3 -m unittest discover -p 'test_*.py'` checks the instruments. Neither command calls a model or accesses credentials.

- [Iteration 3 analysis plan](ITERATION-3.md), written before its implementation, explicitly retrospective.
- [Original QM-2 plan](PLAN.md), historical design; current S1 amendments and gates are in S1-PLAN.md and SETUP.md.
- [S0 prospective plan](reviews/S0-02-pre.md), [post-mortem](reviews/S0-02-post.md), [zero-call failed attempt](reviews/S0-01-post.md).
- [Review history](REVIEW.md), [required setup runbook](../../../../../tooling/agent-experiments/EXPERIMENT-SETUP.md).

## Design transfer — 2026-10-04

[Lessons from Dmarz’s recent studies](DESIGN-TRANSFER.md): specific controls, measurements and next-design options. Prospective only; current run contracts and approval status are unchanged.

## External study-review proposals — 2026-10-04

[Recommendation dispositions and next-step acceptance checks](EXTERNAL-REVIEW-PROPOSALS.md). These reconcile the external review with newer evidence; they are proposals, not completed fixes or changes to frozen runs. Use the latest owning post-mortem and current diagnostic authority before acting.
