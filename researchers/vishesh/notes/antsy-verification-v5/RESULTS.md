# Antsy v5: repair the evidence update before adding agents

2026-10-04 UTC. **Execution and numerical repair qualification passed; practical efficacy remains unestablished.** Two bounded diagnostics completed on an exclusive host, with zero new model/API calls. Both preserve all 70 previously evaluated receipts as development data. No fresh agent behavior, independent replication or production benefit is claimed.

## What improved

The code now treats an unassessable region as missing evidence, preserving its prior estimate. A measured zero still updates the estimate. The original missing-region behavior remains reproducible as a separate diagnostic condition. A cost-aware deterministic baseline can choose any unchecked configuration/region pair and can stop when predicted benefit does not exceed the explicit check price. Its predictions use only the original 20 calibration receipts; current evaluation labels remain outside action selection.

The plan now separates missing-data semantics, verification allocation, stopping competence and practical field-level accuracy. [The next application contract](NEXT-STUDY.md) requires exact required-field decisions, abstention, independently measured checker errors/costs, resource-matched policies and fresh vendor/layout families. These requirements incorporate [Dmarz's conditional successor feedback](../../../dmarz/notes/next-experiments-2026-10-04/README.md); they are not retroactively claimed for v4/v5.

## D0: controlled estimator intervention

All past purchases and model responses stayed fixed. Every original arm choice and score reproduced before assessing the repairs. This isolates what the estimate update does for that fixed history; it does not predict how a model would choose new checks under changed feedback.

| Saved committee history | Original recall / harms | Null-neutral recall / harms | Global-empty recall / harms |
|---|---:|---:|---:|
| Laya | 56.30% / 4 | **57.78% / 3** | 56.44% / 6 |
| Jev | 55.72% / 5 | **56.47% / 2** | 55.89% / 4 |

A harm is a final recall below the no-check confidence choice for that receipt. Null-neutral gains 1.48 points for Laya's fixed purchases and 0.74 for Jev's. Dropping an empty region for all modes is a different update, with less benefit and additional harms. It remains reported, not silently discarded. The null-neutral design was selected for its no-information invariance before these results, not because its observed mean won.

This closes the specific null-induced rank-change defect. It does **not** close unequal-region weighting, imperfect confidence calibration, or harms from unrepresentative but real regional evidence. The remaining 3/2 harmful switches are a warning against saying the entire selector is fixed.

## D1: does a check earn its cost?

Four policies × five prespecified prices × 70 reused receipts = 1,400 condition rows, not 1,400 independent observations. The baseline uses a one-step lookahead through 20 historical calibration scenarios. It values the changed choice using measured quality in those scenarios rather than the maximum updated estimate. The scenarios remain equally weighted after checks; this approximation is not a coherent posterior and may misprice information.

| Assumed cost per check | Cost-aware recall | Checks/receipt | Net utility | No-check utility |
|---|---:|---:|---:|---:|
| 0 | 58.91% | 1.71 | 0.5891 | 0.5678 |
| 0.01 | 58.91% | 1.70 | 0.5721 | 0.5678 |
| 0.02 | 57.97% | 1.27 | 0.5543 | **0.5678** |
| 0.05 | 57.84% | 0.43 | 0.5570 | **0.5678** |
| 0.10 | 57.84% | 0.13 | 0.5656 | **0.5678** |

Utility is recall minus assumed price times checks. These are not measured dollars or human review minutes. The zero-cost policy matched forced-two recall while saving 20 of 140 checks; it stopped before two checks on 12/70 receipts. At costs .02/.05/.10 it stopped early on 30/64/68 receipts. The intervention now changes behavior, unlike v4's inactive adaptive stopping.

Forced-two achieves 58.91% recall and random-two 58.30%, both spending two checks. Confidence-only remains 56.78%. V5 changes the allowed region selection and estimator together for D1; do not attribute all of its gain to stopping or compare it to v4 as a one-factor agent experiment. D0 supplies the isolated estimator comparison.

The cost-aware baseline's mean utility exceeds forced-two at every positive tested price. It only exceeds the no-check baseline at prices 0 and .01. That is a useful boundary, not an economic optimality claim. A larger swarm has not earned a launch merely because an inexpensive baseline improved recall when checking was cheap.

## Assessment against the plan

| Requirement | Evidence | Status |
|---|---|---|
| Original results reproduce | All D0 original choices and scores match saved histories | Passed |
| Null cannot alter a prior score/rank | Regression cases and every D1 null purchase checked | Passed |
| Real zero remains evidence | Zero-response regression changes selection | Passed |
| Stop and continue both possible | Explicit controls; natural diagnostic shows both | Passed for deterministic baseline only |
| No hidden-label action selection | Action inputs limited to observable board plus calibration IDs0–19; audit reconstructs every planned D1 action | Passed |
| No duplicates/budget errors | Independent trace audit, two-check cap, full assignments | Passed |
| Practical field correctness and actual review cost | Not measured by these diagnostics | Open; successor gate |
| Model stopping competence | No new model invoked | Open; successor gate |
| Fresh evaluation and independent review | No new holdout opened | Open; successor gate |

Eleven offline regression tests passed. D0/D1 audits reconstructed 2,940/1,400 unique assigned rows, numeric scores, decisions where applicable and utility. Source scans found no secrets. D0/D1 worker time was 13.30/20.17 seconds excluding uploads, no execution failures. Source hashes and corpus hash are in each manifest. Old failures/results remain unchanged.

## Visual evidence and reproduction

[D0 dashboard](https://swarm-live.pages.dev/#/r/antsy-verification-v5%2FD0-attempt-1) shows the estimator comparison and eight chronological counterfactual GIFs: first IDs30–32 plus the largest original loss per backend, clearly selected post-hoc. [D1 dashboard](https://swarm-live.pages.dev/#/r/antsy-verification-v5%2FD1-attempt-1) shows cost-sensitive results and first-three-receipt decision replays at cost.02. Numeric histories and every GIF frame were decoded/checked; all graphics are 1800px wide. Evaluator truth appears only after commitment. These are measured policy/estimator states, not model reasoning.

Small summaries, manifests and audits are committed in `results/`; full numeric rows/traces are compressed there. No raw receipt images, merchant strings or credential values are included. Reproduce with the pinned source in each manifest and `src/study.py --stage D0|D1 --out NEW_DIRECTORY`; run `src/audit.py --run DIRECTORY` after decompressing row/trace JSON. Requires Pillow; corpus and calibration inputs come from the immutable v4 numeric artifacts. New experimental execution requires a fresh fleet claim and registered pre-run, even when CPU-only. Offline regression tests do not.

## Decision

**Complete this engineering repair; do not launch another broad committee sweep yet.** Retain null-neutral as the qualified missing-evidence contract and the explicit-cost planner as a stronger baseline. Use NEXT-STUDY.md to qualify an actual field checker and its cost before a new agent comparison. The old corpus can diagnose mechanisms but cannot certify a tuned successor's generalization. This iteration makes the failure explainable and the next application testable without presenting a favorable replay as a new scientific result.
