# Phantom Coast PC-3: coverage guard results

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-phantom-coast; source `84d632b0` ([registry](../../../../../experiments/evidence-metadata.json), [rubric](../../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — In eight fresh synthetic roots, the explicit coverage guard changed misleading-team decision loss by -2.26 percentage points under the declared abstention cost. Basis: All assigned outcomes retained and operator-audited; enforced coverage is mechanical. Eight roots, two structural families, one model, unequal compute and utility assumptions limit generalization; no independent replication.
- **sample_size_summary:** Observed S1: 8 roots, 2 structural families, 96 dependent episodes; 1,784/1,792 valid calls, 8 nonvalid retained. Separate Q0: 4 roots, 24/24 valid, 432/432 map labels. PC-1 and PC-2 remain separate.
<!-- experiment-evidence:end -->


**1,784/1,792 valid pilot calls; 96/96 complete episodes across eight fresh roots.** The primary guarded-minus-unrestricted team loss difference under misleading reports is **-2.26 percentage points**. The prospective 5.56-point reduction threshold was not met.

[Prospective plan](PLAN.md) · [Post-mortem](reviews/S1-A1-POST.md) · [Audit](results/S1-A1-audit.json) · [Full analysis](results/S1-A1-analysis.json) · [Public experiment](https://swarm-live.pages.dev/#/x/phantom-coast-pc3)

## Misleading-report comparison

| Policy | Guard | Unique / 12 | Repeats | Report cells / 4 | Wrong / 288 | Unknown / 288 | Loss | Upper error |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| team | off | 4.25 | 7.75 | 3.00 | 8 | 246 | 24.13% | 88.19% |
| team | on | 12.00 | 0.00 | 1.50 | 20 | 172 | 21.88% | 66.67% |
| single | off | 4.00 | 8.00 | 3.00 | 8 | 248 | 24.31% | 88.89% |
| single | on | 12.00 | 0.00 | 1.00 | 24 | 168 | 22.92% | 66.67% |
| uniform | off | 12.00 | 0.00 | 1.62 | 11 | 181 | 19.53% | 66.67% |
| uniform | on | 12.00 | 0.00 | 1.62 | 13 | 179 | 20.05% | 66.67% |

Loss = (wrong + 0.25 × unknown)/36. The abstention cost is a prospective utility assumption. Wrong and unknown are displayed separately; upper error treats unknown as wrong and is not observed accuracy. Each row pools 8 dependent episodes, one per independent root.

Guarded team minus guarded uniform loss: **+1.82 points**; guarded team minus guarded single: **-1.04 points**. These are secondary comparisons with unequal inference compute. Uniform acquisition is identical across its guard/report arms; any endpoint variation remains in the outcomes.

## Evaluation against the plan

Primary paired standard error 2.06 points; descriptive t(7) interval [-7.13, 2.62] points. This small generated sample does not establish population reliability. True-error difference identification bounds [-81.25, 63.89] points are a separate missing-label statement, not a confidence interval.

| Geometry | Roots | Team guard loss difference |
| --- | ---: | ---: |
| block | 4 | -4.86 points |
| scattered | 4 | +0.35 points |

| Unknown penalty | Primary loss difference |
| --- | ---: |
| 0 | +4.17 points |
| 0.25 | -2.26 points |
| 0.5 | -8.68 points |
| 1 | -21.53 points |

All eight root effects and prespecified leave-one-out sensitivity remain in the analysis; none is excluded. Benign-report outcomes, terrain strata, direct/unobserved errors, report visits and yoked judgments are retained there.

Q0 passed before S1: 24/24 valid calls, 432 correct map labels, 4/4 guarded choices and 8/8 unrestricted strategic choices. This establishes the bounded interface, not strategic competence across twelve slots. S1 uses source `06ac568a23ae9212372b8e0156715a71adc5b598` and snapshot `typesafe/jev-1.13-20260917`. All 48 offline checks passed locally and on Linux. Owner waived researcher review and authorized direct launch; this is an operator audit, not independent review.

## Practical interpretation

The concrete tradeoff: misleading-team coverage rose from **4.25 to 12** unique cells, but distinct reported cells checked fell from **3.00 to 1.50**. Known wrong labels increased from **8 to 20 out of 288**; unknown labels fell from **246 to 172**. The guard solved repeat inspection while leaving more false source reports uncorrected. Uniform guarded loss was **20.05%**, versus **21.88%** for the guarded team. These are measured sample differences, not a general ranking.

The guard is an enforced action constraint. Better coverage under it must not be described as learned non-repetition or emergent team intelligence. Compare its loss with uniform and single-controller baselines before paying for a team. The original repeated-inspection result remains a valid finding; this cohort tests a separately planned intervention.

This result applies to stationary, noiseless sensing. A strict ban on revisits would be inappropriate when terrain changes or sensors are noisy. The immediate next comparison should add a fixed report-verification quota within the same twelve-slot budget, with uniform and guarded single baselines. Later stress tests can add changing terrain or noisy sensors and evidence-age/uncertainty-based revisits. See [next-iteration proposal](NEXT-ITERATION.md); it is not a launched or preregistered cohort. The single-model synthetic setting, two reused structural families, eight roots, chosen abstention cost and unequal compute limit transfer.

## Execution, cost and delivery

Assigned/started/terminal/valid: 1792/1792/1792/1784. Stop reason: None. Recorded stage wall time 427.80 seconds; sum of call intervals 376.91 seconds. The fsynced event journal preserves starts, terminals and sensing events; the audit reconstructs every request, event and endpoint.

PC-3 known API cost including Q0: $0.205530948. Cumulative known API cost: $0.562238208; conservative cumulative exposure: $0.574334208. The previous uncertain $0.001344 charge remains reserved. No new spending grant or machine was created. Final cleanup/delivery evidence: [closeout](results/CLOSEOUT.json).

[Measured replay](https://swarm-live.pages.dev/api/a/phantom-coast-pc3/s1-a1/replay.gif) · [Comparison figure](https://swarm-live.pages.dev/api/a/phantom-coast-pc3/s1-a1/results-frame.png). Interactive measured-replay.html is derived from the same saved events and available locally; no model calls are used to render it.

The prespecified loss contrast favors the guard only when unknown labels cost more than approximately **0.162** of a wrong answer (12 extra wrong / 74 fewer unknown). At zero unknown cost the guard is worse; the full sensitivity table above prevents hiding that tradeoff. A separately labeled [post-hoc diagnostic](results/S1-A1-order-diagnostic.json) found 0/570 guarded valid team proposals chose the first legal criterion; a simple first-option fallback is not supported by these traces. This does not rule out all presentation effects.

Known S1 API costs: team $0.135700110 for 1280 calls (including yoked endpoints), single $0.042144060 for 416 calls, uniform $0.022368528 for 96 endpoint calls. Those are unequal-compute policy totals, not cost-matched deployment comparisons.
