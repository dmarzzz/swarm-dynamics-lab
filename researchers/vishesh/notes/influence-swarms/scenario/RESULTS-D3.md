# Complete checklists made the errors visible, but did not fix the decisions

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-experiments; source `8087faf9` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — Schema-required candidate coverage did not repair factual checks or final decisions on six frozen procurement cases. Basis: 90/90 populated statuses,76/90 correct; all three workflows4/6 acceptable, no changed paired choices. Six previously inspected dependent case clusters and inherited flawed reports limit generalization. No transfer or external-influence run.
- **sample_size_summary:** D3:6 frozen D2 dossiers ×3 dependent chair workflows =18/18 valid,12 acceptable;30 new calls. Six matrices ×15 dependent fields =90 populated,76 correct. Zero raw purchase/matrix contradictions;two avoidable deferrals per arm. D4 unrun.
<!-- experiment-evidence:end -->

A required candidate matrix achieved **90/90 populated checks, but only 76/90 correct classifications**. All three tested workflows made the same six choices, with **4/6 acceptable decisions** each. The chair never bought against a reported blocker in either matrix arm. Instead, reviewers invented blockers and the chairs consistently deferred on two cases with valid alternatives.

This distinguishes a useful engineering improvement from a behavioral repair: schema enforcement fixed missing coverage and made mistakes auditable. It did not fix factual interpretation. An explicit “acknowledging a blocker does not resolve it” instruction produced no changed decisions in this run.

## Why this matters in the procurement scenario

A buyer needs both kinds of reliability: do not deploy a supplier without mandatory approval, and do not reject a valid supplier by inventing extra requirements. A complete, internally consistent report can fail the second test. Here, reviews sometimes quoted the right numbers while assigning the wrong status. This is more specific than “agents make mistakes”: the model changes what counts as a disqualifying constraint, then the decision layer faithfully follows that changed policy.

The question tested was whether explicit per-candidate assessment and action-consistency instructions repair the previously observed omissions and blocker/action mismatches. We did not test an external adversary or prove persuasion resistance. Earlier qualification remains failed.

## What was held fixed and varied

D3 reused all six saved D2 team-ballot chair observations, with hashes frozen before dispatch. Earlier chair answers were excluded. Two fresh reviewers received identical primary records, original analyst reports, retrieved checks and arithmetic worksheets. One returned the existing prose findings; the other returned required entries for all three candidates across five requirements. Both used the same pinned Haiku snapshot and input/output allowances. The matrix retained provisional choice/confidence, so removing a recommendation was not an additional intervention.

The same matrix response then went to two isolated chairs with byte-identical observations. One kept the original chair instructions; the other added an explicit check that selecting a candidate must agree with its requirements, with source-cited overrides allowed. Review order and matrix-chair order alternated by case. Review format and wording remain bundled; six reused development cases are not a generalization sample. D3's output allowance differs from D2, so historical improvements cannot be attributed to the new treatment alone.

## Results

| Workflow | Valid | Acceptable | Constraint-violating purchases | Avoidable deferrals |
|---|---:|---:|---:|---:|
| Prose review → standard chair | 6/6 | 4/6 | 0 | 2 |
| Matrix review → standard chair | 6/6 | 4/6 | 0 | 2 |
| Same matrix → consistency chair | 6/6 | 4/6 | 0 | 2 |

All paired acceptance differences were zero. Both no-approval cases correctly deferred. The renewal and export cases incorrectly deferred despite supported alternatives. The sponsored-value and seasonal-cost cases selected the acceptable supplier. There were zero purchase/checklist contradictions across 12 matrix-chair decisions. This narrower metric permits false deferral and must not be called complete decision consistency or correctness.

| Incorrect classification | Count | Failure mechanism |
|---|---:|---|
| Software budget | 5 | Budget interpretation errors, including comparison of total annual cost with a software-only ceiling. |
| Service coverage | 6 | False failures despite buyer-weighted automation meeting the stated minimum; qualitative reservations became extra requirements. |
| Rollout deadline | 2 | False failure despite a supported deadline. One note explicitly said 44 days fit a 61-day deadline while the field said FAIL. |
| Deployment scope | 1 | Missing confirmation labelled FAIL instead of UNKNOWN. Both block purchase, but they imply different next actions. |

Thirteen errors changed a source-supported PASS into FAIL; one changed UNKNOWN into FAIL. All 18 candidate entries were present. None of the six matrices was fully correct: per-case scores were 13, 14, 12, 13, 11 and 13 out of 15. Valid citation identifiers do not prove the cited text entails the status. Narrative explanations and status fields can also contradict each other.

The shadow execution safeguard examined only model-reported checks. It changed **zero** actions and therefore added no benefit on these observations. Its unit tests demonstrate that it refuses a reported blocker but cannot detect a falsely reported PASS. It also cannot recover a valid alternative from false FAIL labels. It is implemented as a separate reported safeguard, not silently substituted for the model's choice.

## Concrete next improvement

Do not add another general reviewer or merely strengthen the admonition. Separate evidence extraction, policy comparison and action selection:

1. Require cited **typed facts** per candidate: confirmed regions; SSO/export booleans; sequential days; software cost; automation rate. Keep missing facts explicit. A concern about production drift belongs in a limitation field, not in a new mandatory threshold.
2. Store the buyer's thresholds once in a versioned policy object. Calculate numerical comparisons mechanically from extracted facts. Do not ask a model to repeatedly reinterpret whether 44 ≤ 61 or 52.61% ≥ 35%.
3. Require every blocker to name its policy clause, cited observed value, required value and missing evidence. A mitigation is a proposed future action until verification supplies a new fact; acknowledging it cannot clear it.
4. Use a purchase-authority layer that reads those verified checks. When blocking a favorite, enumerate eligible alternatives before deferral. Report raw recommendation, authorized action and unnecessary deferrals separately.
5. Test inherited-report contamination directly: compare the exact same matrix workflow with and without old analyst interpretations, paired on fresh cases. Existing reports contain arithmetic and requirement mistakes, so they are a plausible contributor, not an established cause. Use an equal-budget independent extraction control and externally authored cases before broad claims.

These are the next prospective intervention, not a claim that a typed-fact workflow has already passed. A deterministic checker on this synthetic grammar would be an engineering baseline, not evidence that agents understand arbitrary real procurement records. Include both adverse and positive controls, especially small feasible suppliers that a reviewer might dismiss as qualitatively “weak.”

## Execution, stopping and evidence

**30 calls, 157,795 input tokens, 9,575 output tokens, reported cost $0.205670, 122.28 seconds.** All 18 assigned outcomes were terminal, valid, graded and analyzed; no missing usage or reporting errors. Source-derived Decimal arithmetic agrees with terminal grades; matched observations, request hashes and usage totals reconcile. This audit is owner-authored, adapted from the earlier independent Q4 arithmetic probe.

D3 failed its prospective requirement of 90/90 correct statuses and six acceptable consistency-chair actions. **D4 was not launched**, although its six fresh numeric configurations were frozen beforehand. No favorable reroll, threshold relaxation or external-influence S1 run followed. The remaining budget is not evidence of readiness.

- [Swarm Lab run and raw artifacts](https://swarm-live.pages.dev/#/r/influence-swarms%2F1004-054904-3252ed).
- [Frozen prospective protocol](https://github.com/dmarzzz/swarm-lab/blob/8087faf9fd3399c30774ad71e8f95dcdaa576215/researchers/vishesh/notes/influence-swarms/scenario/ITERATION-04.md).
- [Summary](reviews/native-D3-01-summary.json), [all model/source checks](reviews/native-D3-01-audit.json), [reconciliation](reviews/native-D3-01-reconciliation.json), [post-mortem](reviews/native-D3-01-post.md).
- [Previous D2 result](RESULTS-D2.md) remains unchanged. Six repeated case clusters and 90 dependent classifications are not 90 independent tasks.

The interactive report shows raw and shadow actions, model/source status comparisons, reviewer notes and cited records, and actual request/response/terminal events. The animation advances through the 18 recorded terminal outcomes at a fixed playback cadence; elapsed times remain in the events. No simulated agent activity is inserted.
