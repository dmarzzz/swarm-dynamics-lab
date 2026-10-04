# Another reviewer did not reliably turn a recommendation into a valid purchase

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-experiments; source `518d4412` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — Targeted approval-review instructions were insufficient to repair this six-case procurement workflow. Basis: All 30 outputs valid; matched targeted review 3/6 acceptable versus general review 4/6, with one unfavorable paired difference. Six authored template variants, inconsistent checklist coverage and failed competence prevent broad efficacy claims.
- **sample_size_summary:** D2:6 fresh authored dossier configurations ×5 dependent workflows =30/30 valid decisions,17 acceptable;108 calls. Shared team prefixes. Targeted/general review pairs:0 improved,1 worsened,5 equal. Main external-influence comparison unrun.
<!-- experiment-evidence:end -->

The cheapest workflow did best on this six-case diagnostic. The generalist made five acceptable decisions; adding a general review to the team made four, and directing that reviewer to check each candidate's approval made three. **The targeted review instruction failed the predeclared six-of-six repair screen.** It did not improve any paired case relative to a general second look and worsened one.

This is a useful negative result about this workflow, not a claim that specialists or checklists generally fail. All cases are authored synthetic procurement records, with reused document templates and some reused pilot rates. They are not independent real-world procurement tasks.

## What was improved and tested

We pulled the latest feedback, incorporated Dmarz's independent Q4 answerability PASS, and preserved Q4/D1. The new prospective design added a matched extra-call control, six fresh numeric configurations, required-deferral and approved-alternative controls, all three supplier labels, measured workflow cost, a full 30-cell live grid and a replay of actual reviewer/chair responses. The two reviewers had byte-identical observations, equal model/schema/output limits and identical access to primary documents. They differed in instructions. Their chairs received the same original evidence plus the respective new report; no earlier chair answer and no evaluator were supplied.

The practical question is whether extra diligence changes the action a buyer can take. Recognizing a missing approval is not enough if the final choice still authorizes an unsuitable deployment. Conversely, rejecting an attractive blocked supplier should not prevent buying a supported alternative.

## Measured results

| Workflow | Acceptable / 6 | Purchases violating constraints | Avoidable deferrals | Calls if run alone | Model cost if run alone |
|---|---:|---:|---:|---:|---:|
| Team with ballots | 2 | 4 | 0 | 54 | $0.139794 |
| Team without ballot fields | 3 | 1 | 1 | 54 | $0.140273 |
| Generalist | 5 | 0 | 1 | 24 | $0.064474 |
| Team + general second look | 4 | 1 | 0 | 60 | $0.180665 |
| Team + targeted approval instruction | 3 | 1 | 2 | 60 | $0.180415 |

Standalone totals reuse the recorded shared prefix for each alternative; do not sum them as collection spend. Actual collection used **108 calls, 279,584 input tokens, 22,415 output tokens, $0.391659 and 353.55 seconds**. All 30 assigned decisions were started, terminal, valid, graded and analyzed; no duplicates, missing usage or reporting errors. There are six case clusters, not thirty independent samples. The single unfavorable paired difference is descriptive, not evidence of a population effect.

| Case | Supported action | Main lesson |
|---|---|---|
| Regional no approval | DEFER | Generalist and general-review chair deferred. Both original chairs and targeted-review chair bought Birch despite unconfirmed processing. |
| Outsourced no approval | DEFER | All except the team-with-ballots chair deferred. |
| Renewal approved option | Aster | Generalist bought Aster. Other workflows bought an unsuitable/too-expensive option or deferred. |
| Export approved option | Birch | Every workflow failed: two bought export-incomplete Aster; three deferred despite supported Birch. |
| Sponsored service value | Cobalt | All five correctly accepted the genuinely valuable sponsored option. |
| Seasonal usage cost | Aster | All five selected the supported low-total-cost option. |

## Why the proposed repair failed its test

The intervention was an instruction to perform a candidate checklist, not an enforced checklist. In three targeted reviews, at least one candidate was not even named in any finding. On the renewal case, all three findings concerned blocked Cobalt and none discussed supported Aster. On the export case, all concerned Aster and none discussed supported Birch. These are concrete failures to perform the requested candidate coverage. Name mentions alone are not proof of a complete review; the full records remain inspectable.

The regional targeted review acknowledged missing processing approval but its chair still chose Birch. On other cases, detecting the preferred supplier's blocker led to blanket deferral instead of considering the valid alternative. Several explanations also confused the software-only ceiling with total annual cost or made false percentage comparisons. Correct final choices on the two positive controls therefore do not certify faithful reasoning.

The source audit recomputed feasibility and costs from rendered documents using Decimal arithmetic adapted from Dmarz's separate Q4 probe. It agrees with every saved terminal grade and selected-cost scorecard. Applying that probe to D2 is the owning author's audit, not a new independent researcher review. Saved requests confirm matched review observations and no evaluator fields in actor inputs. Actual response usage reconciles exactly to the run summary.

## Assessment against the plan

Execution and reporting succeeded; the proposed behavioral repair did not. Positive controls ruled out indiscriminate sponsor rejection, and the approved-alternative cases exposed overcautious deferral. The matched review control makes the practical inference stronger than a before/after prompt tweak: targeted instructions were no better on five pairs and worse on one. However, inconsistent execution of the requested checklist means this is evidence about the **instruction-based intervention**, not evidence that a faithfully performed checklist is useless.

No S1 external-influence comparison was run. The old qualification remains failed. We do not lower its threshold, overwrite adverse decisions, pool successive diagnostic cohorts, or repeat this batch until it passes.

Next design should require a model-generated, cited assessment for every candidate in the output schema, while leaving the final purchase action unconstrained. Compare that workflow on new cases with the generalist and a structurally matched control. A deterministic deployment guard may be valuable operationally, but enforced choices must be reported separately from model reasoning. A realistic external-validity extension still needs independently authored cases or appropriately shareable real procurement records; neither is claimed here.

## Evidence and replay

- [Swarm Lab run](https://swarm-live.pages.dev/#/r/influence-swarms%2F1004-044202-3747f4): source-bound plan, raw records and live/final frames.
- [Frozen prospective plan](https://github.com/dmarzzz/swarm-lab/blob/518d4412bc566a388dd4dc022118ade8dd637fa3/researchers/vishesh/notes/influence-swarms/scenario/ITERATION-03.md).
- [Audit](reviews/native-D2-01-audit.json), [summary](reviews/native-D2-01-summary.json), [post-mortem](reviews/native-D2-01-post.md), and [prior Q4/D1 results](RESULTS-Q4-D1.md).

Measured HTML and 31-frame GIF show the initial pending grid and each of 30 terminal transitions. The HTML replay exposes all requests, findings, replies and terminal judgments by case. Playback cadence is fixed; recorded elapsed time is retained. No simulated agent activity is inserted.
