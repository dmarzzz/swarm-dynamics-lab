# Knowledgeable newcomer experiment results: Sonnet 4.6 replication

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/newcomer-sonnet; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **2/4** — In this synthetic newcomer task, replacing the Haiku 4.5 synthesizer with Sonnet 4.6 on identical assignments did not materially change outcomes: the sleeper attack still sharply reduced specialist accuracy, the policy ranking was unchanged, and renewal minus reputation stayed inconclusive (+11.1 pp, interval -0.0 to +22.2 pp; +2.8 pp more than Haiku, interval -2.8 to +8.3 pp). Basis: Same-owner assessment: twenty-four paired roots, passed qualification, 1,944/1,944 outcomes paired by assignment with the Haiku cohort and fully reconciled. One task family, two models from one provider, scripted actors and descriptive unadjusted intervals limit stronger conclusions. Independent review was waived by the owner.
- **sample_size_summary:** Observed: 24 paired roots from one synthetic task family; 1,944/1,944 S1 outcomes analyzed, zero missing, each paired by assignment ID with the separate Haiku cohort (not pooled); 24 honest + 1/4/16 controller identities, one synthesizer model. Q0 separately: 36/36 clean calls.
<!-- experiment-evidence:end -->

Completed 2026-10-04. Run `sybil-newcomer-sonnet/50847934` on sim-dmarz-5, revision `bbd6a372ce982be4af17049262a1ba48635373e2`, model `claude-sonnet-4-6`. This is a model replication of [sybil-newcomer-api](../sybil-newcomer-api/RESULTS.md) (Haiku 4.5, S1 run `sybil-newcomer-api/8def40e4`) on identical assignments: same worlds 7100-7123, packets, expected answers and dispatch order. The two cohorts are separate and are never pooled. Cross-researcher review was waived by the owner (SETUP.md G0); no independent review was performed. Post-mortem: [reviews/s1-001-post.md](reviews/s1-001-post.md).

Exploratory S1: 1944 assigned, 1944 started, 1944 terminal, 1944 graded/analyzed; 0 invalid and 0 not started. Stage model calls: 1944; recorded stage cost $9.045309. Q0 cost is separate from this stage. 0 attempted calls lack reported usage. Runtime `a0fa76922ed6000bb07bca6c9d9bbae312b566f4e4cd7271e147c87f75833ed4`.

## Primary predeclared contrast

Renewal minus reputation auditing, sixteen controller identities, sleeper attack, round eight: **+11.1 pp (descriptive 95% interval -0.0 pp to +22.2 pp; 24 paired worlds)** in specialist accuracy. The planned useful-effect marker is +10 percentage points; descriptive intervals and this exploratory design do not establish confirmatory significance.

## Same-cost policy comparison

All policies used four audits, twelve admitted reports and sixteen controller messages per simulated round. The table is round eight of the sixteen-identity sleeper condition. Ownership share counts controller reports even when truthful; harmful share counts actually false current reports.

| Policy | Valid / assigned worlds | Specialist accuracy | Wrong non-null specialist outputs | Truth present in admitted packet | Honest specialist retention | Harmful reports | Controller reports | Same-packet plurality |
|---|---|---|---|---|---|---|---|---|
| random | 24/24 | 25.0% | 37.5% | 30.6% | 30.6% | 12.2% | 12.2% | 22.2% |
| renewal | 24/24 | 19.4% | 41.7% | 25.0% | 25.0% | 15.3% | 15.3% | 12.5% |
| reputation | 24/24 | 8.3% | 54.2% | 23.6% | 23.6% | 30.9% | 30.9% | 5.6% |

Renewal minus equal-cost random auditing: -5.6 pp (descriptive 95% interval -16.7 pp to +4.2 pp; 24 paired worlds). The strongest baseline is determined from the measured cells; the report does not presume renewal wins.

The available-truth diagnostic counts rare answers appearing in at least one admitted report. It diagnoses evidence loss, but is not a strict ceiling on lucky guessing. High output accuracy must be read alongside newcomer retention and false-output share.

## Fixed-resource identity splitting

The controller always sends sixteen reports per round and uses zero model computation. These paired contrasts change one identity into sixteen at round eight under the sleeper attack. The number of active veteran identities and public reputation concentration also change; these are part of the manipulation.

| Policy | Metric | 16 minus 1 identities |
|---|---|---|
| random | rare_accuracy | -2.8 pp (descriptive 95% interval -18.1 pp to +11.1 pp; 24 paired worlds) |
| reputation | rare_accuracy | +4.2 pp (descriptive 95% interval -4.2 pp to +13.9 pp; 24 paired worlds) |
| renewal | rare_accuracy | -9.7 pp (descriptive 95% interval -25.0 pp to +5.6 pp; 24 paired worlds) |
| random | harmful_seat_share | +6.2 pp (descriptive 95% interval -1.0 pp to +13.2 pp; 24 paired worlds) |
| reputation | harmful_seat_share | -1.4 pp (descriptive 95% interval -7.6 pp to +4.5 pp; 24 paired worlds) |
| renewal | harmful_seat_share | -2.8 pp (descriptive 95% interval -13.5 pp to +7.3 pp; 24 paired worlds) |
| random | newcomer_retention | +1.4 pp (descriptive 95% interval -15.3 pp to +16.7 pp; 24 paired worlds) |
| reputation | newcomer_retention | +5.6 pp (descriptive 95% interval -6.9 pp to +18.1 pp; 24 paired worlds) |
| renewal | newcomer_retention | -8.3 pp (descriptive 95% interval -22.2 pp to +5.6 pp; 24 paired worlds) |

The secondary interaction, (renewal minus reputation at sixteen identities) minus (renewal minus reputation at one), is -13.9 pp (descriptive 95% interval -30.6 pp to +2.8 pp; 24 paired worlds) for accuracy. All strategy/round/metric interactions are retained in the JSON.

## Clean counterfactual and relapse stress test

Clean worlds retain the same controller-owned identities and messages, but every claim is truthful. The coalition therefore also supplies correct rare information; the single-source honest-truth bottleneck applies during attack-active rounds. Relapse lies in rounds four, seven and eight and is a predeclared stress test, not an independent confirmatory holdout.

| Strategy | Policy | Valid / assigned | Round-8 accuracy, 16 identities | Harmful report share | Honest specialist retention |
|---|---|---|---|---|---|
| clean | random | 24/24 | 81.9% | 0.0% | 20.8% |
| clean | renewal | 24/24 | 83.3% | 0.0% | 19.4% |
| clean | reputation | 24/24 | 79.2% | 0.0% | 20.8% |
| relapse | random | 24/24 | 16.7% | 19.1% | 26.4% |
| relapse | renewal | 24/24 | 15.3% | 22.6% | 22.2% |
| relapse | reputation | 24/24 | 6.9% | 33.7% | 25.0% |

| Attack minus clean | Policy | Paired accuracy change |
|---|---|---|
| sleeper | random | -56.9 pp (descriptive 95% interval -68.1 pp to -44.4 pp; 24 paired worlds) |
| relapse | random | -65.3 pp (descriptive 95% interval -75.0 pp to -55.6 pp; 24 paired worlds) |
| sleeper | reputation | -70.8 pp (descriptive 95% interval -83.3 pp to -58.3 pp; 24 paired worlds) |
| relapse | reputation | -72.2 pp (descriptive 95% interval -83.3 pp to -59.7 pp; 24 paired worlds) |
| sleeper | renewal | -63.9 pp (descriptive 95% interval -73.6 pp to -54.2 pp; 24 paired worlds) |
| relapse | renewal | -68.1 pp (descriptive 95% interval -76.4 pp to -59.7 pp; 24 paired worlds) |

## Recorded temporal mechanism

The simulator retained every round from one through eight. The API synthesized separate current packets only at rounds four, five and eight; it had no cross-round memory. The animated replay shows recorded simulated trust/admission, while the model table shows sampled output observations. Non-sampled model rounds remain explicitly unavailable.

Three warm-up rounds permit only twelve total audits across the veteran population. This is limited trust formation, not a long established reputation history. Mean reputation is the Beta(1,1) public audit-pass estimate, grouped by evaluator-only controller ownership.

| Controller identities | Policy | Round-3 mean controller reputation | Cumulative controller audits | Audits per active controller identity | Round-8 unique admitted contributors |
|---|---|---|---|---|---|
| 1 | random | 57.6% | 0.50 | 0.50 | 11.46 |
| 1 | reputation | 57.5% | 0.75 | 0.75 | 9.12 |
| 1 | renewal | 59.2% | 0.75 | 0.75 | 10.29 |
| 4 | random | 60.4% | 1.42 | 0.71 | 11.67 |
| 4 | reputation | 57.2% | 1.54 | 0.77 | 11.08 |
| 4 | renewal | 58.9% | 1.50 | 0.75 | 11.08 |
| 16 | random | 55.9% | 3.92 | 0.49 | 12.00 |
| 16 | reputation | 54.7% | 4.54 | 0.57 | 12.00 |
| 16 | renewal | 55.6% | 4.12 | 0.52 | 12.00 |

## Missing observations, provenance and limitations

Every assigned observation is retained. Failure/not-started records: 0; full identifiers, categories and accounting are in results-summary.json. The CSV contains every cell, valid/assigned denominators, complete-case means, same-packet plurality, recorded cost, and accuracy bounds assigning missing outcomes zero or one. Paired contrasts include only complete world pairs and report their pair count.

Twenty-four worlds, rather than identities or frames, are the planned independent clusters. Intervals are descriptive and unadjusted for multiple comparisons. All policies, reporters, auditing errors and attacks are scripted; one pinned model synthesizes packets of synthetic integers. The design uses scarce honest facts, a fixed audit-quality model, short warm-up, a fixed join schedule and ±7 fabrications. It does not establish open-world Sybil resistance or learned trust. At four/sixteen identities half the controller identities join in round four; at one identity it is a veteran throughout. New identities can be honest or adversarial. Source order and opaque names are randomized; hidden truth/ownership never enter policy or model inputs.

Independent review was waived by the owner and is not claimed. Formal S2 remains disabled. Valid adverse or null outcomes are retained, with no policy tuning or rerunning to obtain a favorable result. Verify verification-summary.json and deployed PNG/GIF playback before drawing conclusions.

## Sonnet minus Haiku on identical assignments

All 1944 assignments completed in both cohorts and were paired by assignment id; packet hashes, worlds and cells match exactly (checked by [compare_haiku.py](reporting/compare_haiku.py); output [records/s1-001-haiku-comparison.json](records/s1-001-haiku-comparison.json)). Differences are Sonnet minus Haiku, clustered by world.

Difference in the frozen primary contrast, (renewal minus reputation) for Sonnet minus the same for Haiku: **+2.8 pp (descriptive 95% interval -2.8 to +8.3 pp; 24 paired worlds)**. Sonnet's primary contrast is +11.1 pp; Haiku's was +8.3 pp.

| Strategy | Policy | Specialist accuracy, Sonnet minus Haiku | Wrong non-null specialist outputs, Sonnet minus Haiku |
|---|---|---|---|
| clean | random | +0.0 pp (descriptive 95% interval +0.0 to +0.0 pp; 24 paired worlds) | +0.0 pp (descriptive 95% interval +0.0 to +0.0 pp; 24 paired worlds) |
| clean | renewal | -1.4 pp (descriptive 95% interval -4.2 to +0.0 pp; 24 paired worlds) | +0.0 pp (descriptive 95% interval +0.0 to +0.0 pp; 24 paired worlds) |
| clean | reputation | -4.2 pp (descriptive 95% interval -13.9 to +4.2 pp; 24 paired worlds) | +0.0 pp (descriptive 95% interval +0.0 to +0.0 pp; 24 paired worlds) |
| relapse | random | +1.4 pp (descriptive 95% interval -2.8 to +5.6 pp; 24 paired worlds) | +0.0 pp (descriptive 95% interval -4.2 to +4.2 pp; 24 paired worlds) |
| relapse | renewal | +1.4 pp (descriptive 95% interval +0.0 to +4.2 pp; 24 paired worlds) | -0.0 pp (descriptive 95% interval -11.1 to +9.7 pp; 24 paired worlds) |
| relapse | reputation | -2.8 pp (descriptive 95% interval -6.9 to +0.0 pp; 24 paired worlds) | -6.9 pp (descriptive 95% interval -19.4 to +5.6 pp; 24 paired worlds) |
| sleeper | random | -1.4 pp (descriptive 95% interval -5.6 to +2.8 pp; 24 paired worlds) | +1.4 pp (descriptive 95% interval +0.0 to +4.2 pp; 24 paired worlds) |
| sleeper | renewal | -1.4 pp (descriptive 95% interval -4.2 to +0.0 pp; 24 paired worlds) | -2.8 pp (descriptive 95% interval -11.1 to +4.2 pp; 24 paired worlds) |
| sleeper | reputation | -4.2 pp (descriptive 95% interval -8.3 to +0.0 pp; 24 paired worlds) | -8.3 pp (descriptive 95% interval -18.1 to +0.0 pp; 24 paired worlds) |

Across all 81 cells the mean accuracy difference is -0.9 pp. Measured: changing the synthesizing model from Haiku 4.5 to Sonnet 4.6 moved no round-8, sixteen-identity cell by more than 4.2 pp of accuracy, and the policy ranking (random above renewal above reputation under the sleeper attack) is unchanged. Inferred, not separately tested: in this fixture the bottleneck is admission, not synthesis. The correct rare fact is present in only 24-31% of admitted round-8 sleeper packets, and neither model's accuracy exceeded that availability in any of these cells (it is a diagnostic, not a strict ceiling: a model could guess correctly without the fact).
