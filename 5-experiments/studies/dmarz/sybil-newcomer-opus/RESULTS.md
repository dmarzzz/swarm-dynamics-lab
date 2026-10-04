# Knowledgeable newcomer experiment results: Opus 5.5 cohort

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by dmarz/newcomer-opus; source `9781739c` ([registry](../../../../experiments/evidence-metadata.json), [rubric](../../../../experiments/EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **2/4** — In this synthetic newcomer task, an Opus 5.5 synthesizer (effort low) on assignments identical to the Haiku 4.5 and Sonnet 4.6 cohorts did not materially change outcomes: the policy ranking (random > renewal > reputation) was unchanged, renewal minus reputation stayed inconclusive (+9.7 pp, interval -1.4 to +20.8 pp), and the difference from Haiku in that contrast was +1.4 pp (interval -4.2 to +6.9 pp). Accuracy never exceeded the share of truth present in admitted packets. Basis: Same-owner assessment: twenty-four paired roots, passed probe and qualification, 1,944/1,944 outcomes paired by assignment with both earlier cohorts and fully recomputed from frozen runtime. The Opus request configuration differs from the earlier cohorts (no temperature, adaptive thinking at effort low); one task family, scripted actors and descriptive unadjusted intervals limit stronger conclusions. Independent review was waived by the owner.
- **sample_size_summary:** Observed: 24 paired roots from one synthetic task family; 1,944/1,944 S1 outcomes analyzed, zero missing, each paired by assignment ID with the separate Haiku and Sonnet cohorts (not pooled); 24 honest + 1/4/16 controller identities, one synthesizer model. Q0 separately: 36/36 clean calls plus one probe call.
<!-- experiment-evidence:end -->

Exploratory S1: 1944 assigned, 1944 started, 1944 terminal, 1944 graded/analyzed; 0 invalid and 0 not started. Stage model calls: 1944; recorded stage cost $14.478336. Q0 cost is separate from this stage. 0 attempted calls lack reported usage. Runtime `a21290e41d93c2634dd6824245cf9a8ce0900c9c00f1b9cb0c08640310206322`.

Run `sybil-newcomer-opus/14ea6e6b`, revision `d289769aede95922dd69318087f1e27f7a304d12`, host sim-dmarz-13, 2026-10-04. Model `claude-opus-5-5` at `effort: low`, no temperature field, no thinking field (Opus 5.5 rejects temperature and cannot disable thinking), `max_tokens` 4,000 with the visible answer capped at 2,000 characters. The Haiku 4.5 and Sonnet 4.6 cohorts ran at temperature 0 with thinking off, so this is a new model **and** configuration, not a model-only swap. Assignments, packets and dispatch order are identical across all three cohorts (1,944 ids and packet hashes match). Cohorts are compared, never pooled.

## Primary predeclared contrast

Renewal minus reputation auditing, sixteen controller identities, sleeper attack, round eight: **+9.7 pp (descriptive 95% interval -1.4 pp to +20.8 pp; 24 paired worlds)** in specialist accuracy. The planned useful-effect marker is +10 percentage points; descriptive intervals and this exploratory design do not establish confirmatory significance.

## Same-cost policy comparison

All policies used four audits, twelve admitted reports and sixteen controller messages per simulated round. The table is round eight of the sixteen-identity sleeper condition. Ownership share counts controller reports even when truthful; harmful share counts actually false current reports.

| Policy | Valid / assigned worlds | Specialist accuracy | Wrong non-null specialist outputs | Truth present in admitted packet | Honest specialist retention | Harmful reports | Controller reports | Same-packet plurality |
|---|---|---|---|---|---|---|---|---|
| random | 24/24 | 26.4% | 37.5% | 30.6% | 30.6% | 12.2% | 12.2% | 22.2% |
| renewal | 24/24 | 16.7% | 50.0% | 25.0% | 25.0% | 15.3% | 15.3% | 12.5% |
| reputation | 24/24 | 6.9% | 65.3% | 23.6% | 23.6% | 30.9% | 30.9% | 5.6% |

Renewal minus equal-cost random auditing: -9.7 pp (descriptive 95% interval -19.4 pp to +0.0 pp; 24 paired worlds). The strongest baseline is determined from the measured cells; the report does not presume renewal wins.

The available-truth diagnostic counts rare answers appearing in at least one admitted report. It diagnoses evidence loss, but is not a strict ceiling on lucky guessing. High output accuracy must be read alongside newcomer retention and false-output share.

## Three-cohort comparison (paired by world)

Round 8, sixteen controller identities, sleeper attack. Same packets for every model. The available-truth column is the share of rare answers present in at least one admitted report (identical across models because admission happens before the model is called).

| Policy | Opus 5.5 | Sonnet 4.6 | Haiku 4.5 | Truth present in admitted packet |
|---|---|---|---|---|
| random | 26.4% | 25.0% | 26.4% | 30.6% |
| renewal | 16.7% | 19.4% | 20.8% | 25.0% |
| reputation | 6.9% | 8.3% | 12.5% | 23.6% |

Primary contrast (renewal minus reputation) by cohort: Opus +9.7 pp (−1.4 to +20.8), Sonnet +11.1 pp, Haiku +8.3 pp. Difference in that contrast, paired by world: Opus minus Haiku +1.4 pp (−4.2 to +6.9); Opus minus Sonnet −1.4 pp (−4.2 to 0.0). Across all 81 cells the mean Opus-minus-Haiku accuracy difference is +0.6 pp (largest single cell 12.5 pp) and Opus-minus-Sonnet +1.5 pp (largest 13.9 pp). Mean specialist accuracy over all assignments: Opus 45.1%, Sonnet 43.6%, Haiku 44.4%; wrong non-null specialist outputs 32.4%, 30.1%, 32.0%.

Measured: in no assignment did Opus accuracy exceed the available-truth share. Interpretation (not separately tested): output accuracy in this design is bounded by which reports the admission policy lets through, and a stronger synthesizer does not move that bound; the policy ranking (random > renewal > reputation) is the same for all three models. Tables: [records/s1-001-opus-minus-haiku.json](records/s1-001-opus-minus-haiku.json), [records/s1-001-opus-minus-sonnet.json](records/s1-001-opus-minus-sonnet.json), produced by `reporting/compare_haiku.py` (cohort-agnostic despite its name).

## Fixed-resource identity splitting

The controller always sends sixteen reports per round and uses zero model computation. These paired contrasts change one identity into sixteen at round eight under the sleeper attack. The number of active veteran identities and public reputation concentration also change; these are part of the manipulation.

| Policy | Metric | 16 minus 1 identities |
|---|---|---|
| random | rare_accuracy | -2.8 pp (descriptive 95% interval -18.1 pp to +11.1 pp; 24 paired worlds) |
| reputation | rare_accuracy | +0.0 pp (descriptive 95% interval -9.7 pp to +9.7 pp; 24 paired worlds) |
| renewal | rare_accuracy | -13.9 pp (descriptive 95% interval -29.2 pp to +1.4 pp; 24 paired worlds) |
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
| clean | renewal | 24/24 | 84.7% | 0.0% | 19.4% |
| clean | reputation | 24/24 | 86.1% | 0.0% | 20.8% |
| relapse | random | 24/24 | 16.7% | 19.1% | 26.4% |
| relapse | renewal | 24/24 | 15.3% | 22.6% | 22.2% |
| relapse | reputation | 24/24 | 5.6% | 33.7% | 25.0% |

| Attack minus clean | Policy | Paired accuracy change |
|---|---|---|
| sleeper | random | -55.6 pp (descriptive 95% interval -68.1 pp to -43.1 pp; 24 paired worlds) |
| relapse | random | -65.3 pp (descriptive 95% interval -76.4 pp to -54.2 pp; 24 paired worlds) |
| sleeper | reputation | -79.2 pp (descriptive 95% interval -90.3 pp to -66.7 pp; 24 paired worlds) |
| relapse | reputation | -80.6 pp (descriptive 95% interval -90.3 pp to -69.4 pp; 24 paired worlds) |
| sleeper | renewal | -68.1 pp (descriptive 95% interval -76.4 pp to -59.7 pp; 24 paired worlds) |
| relapse | renewal | -69.4 pp (descriptive 95% interval -76.4 pp to -61.1 pp; 24 paired worlds) |

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
