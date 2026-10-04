# Antsy v5: is another check worth buying?

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `9781739c` ([registry](../../../evidence-metadata.json), [rubric](../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — Null-neutral updates fix a specific estimator defect and explicit-cost planning changes deterministic check allocation. Basis: Numerical reconstruction supports the narrow repair; saved purchases do not reveal counterfactual model behavior. D1 changes estimator and action allocation together; assumed check price is not measured economics. No fresh efficacy/generalization claim.
- **sample_size_summary:** Same70 v4 receipts reused as development diagnostics; D0=2,940 rows,D1=1,400 rows;20 historical calibration receipts;0 new model calls or fresh evaluation receipts.
<!-- experiment-evidence:end -->

Status: completed exploratory engineering repair; [results and plan assessment](RESULTS.md). Not an accepted hypothesis. Parent: [v4 completed assessment](../antsy-verification-v4/RESULTS.md). This iteration must distinguish an informative check from a change caused merely by the estimator's bookkeeping.

## Question and decision value

Can a receipt-processing system choose an OCR output more reliably when verification has an explicit cost, a no-information response cannot alter its ranking, and a cheap planner competes with agent suggestions? A successful repair need not make the committee win. It must make the comparison interpretable.

## Feedback incorporated

Repository refresh: `25531b6`. [Dmarz's conditional successor](../../dmarz/next-experiments-2026-10-04/README.md) asks for completed parent results, measured ambiguity/headroom, matched resources and a new evaluation sample. V4 is now complete. Its confidence-only baseline outperformed committee means; the adaptive intervention never activated. The v4 post-mortems additionally identify null QA, unequal regional weighting and weak stopping qualification. No new Antsy-specific peer review was found in the refreshed inbox or reviews.

## Plan before implementation

1. **D0 mechanism diagnostic.** Replay the recorded v4 verification purchases under three explicitly versioned estimators: original; null-neutral (retain the prior on a null response); global-empty (drop the discovered empty region for every configuration). Keep purchases and model responses fixed. Compare all 70 prior evaluation receipts, including every harmful switch, without selecting success cases. This is a retrospective estimator intervention, not a new agent trial or independent efficacy estimate. Test null-neutral rank invariance and genuine-zero updates directly.
2. **D1 cost-aware instrument.** Build a deterministic lookahead selector using only the old calibration receipts as a predictive distribution. Enumerate prospective observations from those development records, update the null-neutral estimator, and value the expected improvement over stopping. Charge a published normalized check cost. The actor never receives the current receipt's evaluator labels or a hindsight oracle action. Verify stop/continue controls, budget enforcement and no duplicate checks. Review cost is an assumed sensitivity parameter, not measured human labor.
3. **Qualification and next-evaluation gate.** Use the old validation corpus only as development/diagnostic data. Before opening a new split, inspect D0/D1: can the information model choose both stop and continue; do checks measure something useful; can numerical quality and cost claims be reconstructed? A defect blocks a broad model sweep. Do not retune the same 70 receipts and call the result an independent win.

## Frozen D0 protocol

Units: the same 70 v4 receipt IDs 30–99. Conditions: two backend histories × seven original arms × three estimators. Controls have no new model calls; shared controls are counted once. Recompute final choice using recorded purchases, preserving true numeric observations, budget and provenance. No claim that a model would make the same purchases under changed feedback. Primary diagnostic: number and magnitude of harmful switches versus each estimator's no-check choice. Report overall recall, regret, null-check counts, exact paired deltas and worst cases. No confirmatory p-values.

## Frozen D1 protocol

Predictive distribution: calibration IDs 0–19, excluding all 70 evaluated receipts. For each possible mode/region action, simulate its response from each calibration record with equal weight, update a copy of the actual observable board using null-neutral semantics, and average the change in the selected output’s measured quality within that calibration scenario (relative to stopping in that same scenario). The one-step rule buys the highest positive net-value check, or stops. At most two checks; choose among all unchecked mode/region pairs, with deterministic ties. Compare to zero-check confidence, two random checks, and forced-two-check lookahead. Cost sensitivity: 0, 0.01, 0.02, 0.05, 0.10 recall units per check. This is an empirical approximate value-of-information baseline, not a calibrated posterior or optimal policy. Pre-implementation refinement: value a changed choice against its calibration-scenario quality, rather than the maximum updated estimate; maximizing a noisy estimate alone can reward optimism without correctness. The calibration scenarios remain equally weighted after checks, an explicit limitation to audit.

D1 acceptance: no true labels in action selection; null returns preserve every prior score; real zero is evidence; no duplicate/budget violation; zero model/API calls; at least one stop and one continue on explicit mechanism controls; identify natural-corpus stop/continue counts and generalization limits. Null results remain results. If the planner exploits spurious estimator optimism, diagnose rather than launch agents against it.

## Practical scope and what remains outside this iteration

The operational choice is whether the expected OCR quality improvement merits another review. Token recall and an assumed check cost are not exact amount correctness or payment safety. Field-level extraction, real reviewer timing/error and calibration of uncertainty remain prerequisites for a production claim. These will not be described as solved by an estimator patch. Same-checkpoint roles remain correlated; no new swarm-superiority claim is licensed.

## Visualization mapping

D0: paired before/after recall and harmful-switch counts; diagnostic replay of all steps for the first three assigned receipts plus a clearly labeled largest-loss case. Show purchased true response, including null, and all three estimator scores. Reveal evaluator truth only at commitment. D1: quality versus checks/cost, stop/continue counts and trace of chosen checks. Display measured replay events, never invented movement. Keep numeric traces; PNG >=1600px and GIF or self-contained replay. Public plan and condition TLDR must be verified before fleet execution.

## Resources and promotion

One fresh exclusive fleet allocation, maximum 10 minutes each D0/D1, CPU only, zero new hosted/model calls. Preserve v4's cumulative Jev ledger; this iteration does not reset it. Output directories are immutable. Commit pre-run, run, write post-mortem and compare against acceptance. A separate committed plan is required for any new OCR corpus measurement or real-model qualification; neither is implicitly authorized by this plan's engineering gate.

## Practical successor

[NEXT-STUDY.md](NEXT-STUDY.md) specifies receipt intake, required-field scoring, abstention, measured checker costs, matched inference budgets and fresh vendor/layout splits. These application gates remain distinct from the completed estimator diagnostics.

## External study-review proposals — 2026-10-04

[Recommendation dispositions and next-step acceptance checks](EXTERNAL-REVIEW-PROPOSALS.md). These reconcile the external review with newer evidence; they are proposals, not completed fixes or changes to frozen runs. Use the latest owning post-mortem and current diagnostic authority before acting.
