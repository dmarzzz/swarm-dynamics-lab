# Verification budget and reliability: completed exploratory results

**More verification helps only under some conditions, and answer accuracy can conceal a worse admission outcome.** The prior large-world accuracy improvement reproduced on 24 fresh paired worlds: 108 versus four coverage checks raised specialist accuracy from 40.3% to 97.2% when attackers passed checks only 10% of the time. But the full budget grid is not monotone. At 324 identities, coverage met the joint engineering target with 32 checks and then failed it at 64 and 108 because attacker seat share rose, even as accuracy improved.

S1 run [`sybil-budget-api/46ebda03`](https://swarm-live.pages.dev/#/r/sybil-budget-api%2F46ebda03) completed all **2,880 assigned outcomes, with zero invalid, failed or not-started outcomes**. Every one of 120 cells has 24 observations. These are **24 independent sampled world clusters**, paired across conditions, not 2,880 independent worlds. The main collection cost **$39.349188**; Q0 plus S1 cost **$39.672176**. This is an owner-authorized exploratory result, with independent review explicitly waived and formal S2 disabled.

![Final accuracy and attacker-admission heatmaps](https://swarm-live.pages.dev/api/a/sybil-budget-api/46ebda03/final_frame.png)

Versioned figures are also retained on GitHub: [accuracy/admission](../../../../artifacts/sybil-budget-api-s1/sybil-budget-api-s1-v1.png) and [specialist retention](../../../../artifacts/sybil-budget-api-s1-retention/sybil-budget-api-s1-retention-v1.png).

The [retention companion](https://swarm-live.pages.dev/api/a/sybil-budget-api/46ebda03/retention.png) shows how many honest specialists remain admitted. The [25-frame replay](https://swarm-live.pages.dev/api/a/sybil-budget-api/46ebda03/replay.gif) shows recorded call completions, not agent interaction. Yellow outlines mark complete cells meeting both point-mean targets; they are not confidence or safety guarantees.

## What was tested

The grid crosses 324/972 identities, 4/8/16/32/64/108 checks, attacker check-pass probabilities of 10/30/50/70/90%, and random/topology-coverage checking. Honest identities pass with probability 90%; badges are visible. Half the population is admitted by the retained trust procedure. The model is the pinned `claude-haiku-4-5-20251001`, with one structured answer per packet, temperature zero and no retries. Identities, topology, checks and claims are simulated; the API supplies answer synthesis only.

Specialist accuracy is the fraction of three specialist facts correctly recovered in the answer; a wrong answer or abstention scores zero. Attacker seat share divides admitted attacker identities by all admitted identities. Honest specialist retention divides admitted honest specialists by all honest specialists. The three facts are repeated among many specialists, so high answer accuracy need not mean broad access for those specialists.

The predeclared engineering target requires **mean specialist accuracy ≥90% and mean attacker seat share ≤5%**. All observations, denominator checks and paired contrasts appear in the [120-cell CSV](results-cells.csv) and [full aggregate JSON](results-summary.json).

## The tested frontier is conditional and nonmonotone

Only **7 of 120 cells** met the point-mean target; all used the strongest tested checks, with attacker pass probability 10%. Five met the more stringent descriptive interval-envelope target. No cell passed at attacker pass probabilities 30%, 50%, 70% or 90%: all 96 such cells are retained in the full table.

| Identities | Policy | Smallest tested point-mean passing budget | All point-mean passing budgets | Interval-envelope passing budgets |
|---|---|---:|---|---|
| 324 | Random | 32 | 32, 64, 108 | 64, 108 |
| 324 | Coverage | 32 | 32 | 32 |
| 972 | Random | 64 | 64, 108 | 108 |
| 972 | Coverage | 108 | 108 | 108 |

This table applies only to attacker pass probability 10%. “Smallest” refers to the tested grid, not an estimated optimum or guarantee for larger budgets. The interval-envelope flag requires the accuracy interval's lower bound to be at least 90% and the attacker-seat interval's upper bound at most 5%. It is descriptive and unadjusted for searching many cells.

The nonmonotonicity is visible in the 324-identity coverage condition with strong checks:

| Checks | Specialist accuracy | Attacker seat share | Honest specialist retention | Point-mean target |
|---:|---:|---:|---:|---|
| 32 | 97.2% | 1.98% | 33.8% | Met |
| 64 | 98.6% | 8.51% | 64.6% | Missed |
| 108 | 100.0% | 10.70% | 80.0% | Missed |

More checks increased honest specialist retention and answer accuracy here, but also admitted a larger attacker share. The joint target therefore stops being met after 32 checks. This is an observed property of this checking and admission procedure; a mechanism claim would require a separate diagnostic. The result rules out describing the observed frontier as a universal “at least this many checks” threshold.

## Compare policies at the same budget

At 972 identities and attacker pass probability 10%, random checking reached the point-mean target at 64 checks, while coverage first reached it at 108. The defensible policy contrasts compare equal resources:

| Checks | Policy | Specialist accuracy | Attacker seat share | Honest specialist retention |
|---:|---|---:|---:|---:|
| 64 | Random | 100.0% | 4.82% | 52.9% |
| 64 | Coverage | 86.1% | 0.63% | 5.9% |
| 108 | Random | 100.0% | 3.40% | 52.4% |
| 108 | Coverage | 97.2% | 2.88% | 37.4% |

At 64 checks, coverage minus random was **−13.9 percentage points of accuracy** (paired 95% bootstrap interval −25.0 to −4.2), **−4.19 points of attacker seats** (−5.33 to −3.10), and **−47.0 points of specialist retention** (−50.5 to −43.6). Coverage admitted fewer attackers but excluded far more honest specialists and recovered fewer specialist facts. There is no single-policy winner across all three outcomes.

Random's 4.82% attacker seat mean at 64 checks is close to the 5% target; its descriptive interval is 3.74–5.88%, so it fails the interval-envelope flag. Its 100% accuracy means all 72 specialist fields in these 24 worlds were correct. A bootstrap interval of 100–100% at that ceiling does not establish perfect future accuracy.

At 108 checks, coverage minus random was −2.8 accuracy points (−6.9 to 0.0), −0.51 attacker-seat points (−1.50 to +0.40) and −14.9 retention points (−19.1 to −10.9). This does not establish a unique coverage advantage. Comparing random at 64 with coverage at 108 is useful to describe the tested frontier, but is not an equal-resource causal policy comparison.

## The prior endpoint result reproduces; weak checks do not

The predeclared primary contrast is 108 minus four coverage checks at 972 identities and attacker pass probability 10%:

| Outcome | Four checks | 108 checks | Paired difference, percentage points | Descriptive 95% interval |
|---|---:|---:|---:|---|
| Specialist accuracy | 40.3% | 97.2% | +56.9 | +43.1 to +70.8 |
| Attacker seat share | 11.53% | 2.88% | −8.65 | −10.25 to −7.11 |
| Honest specialist retention | 23.2% | 37.4% | +14.3 | +11.4 to +17.1 |

The accuracy endpoint corresponds to 29/72 versus 70/72 correct specialist fields, clustered into the same 24 worlds. The [previous study](../sybil-scale-api/RESULTS.md) reported 47.2% to 98.6% on its different worlds. The fresh result supports the same direction within this fixture; it is not a paired old-versus-new comparison or a test of equivalence. The aggregate JSON preserves 12 exact matched endpoint anchors. The earlier 324-identity/36-check condition is absent from this grid and is never treated as the new 32-check condition.

With attacker pass probability 90%, the corresponding 972-identity coverage comparison had **no mean accuracy gain**: 43.1% at both endpoints, difference 0.0 points with interval −15.3 to +15.3. Attacker seat share rose from 11.53% to 21.06%, a paired **+9.53 points** (+7.78 to +11.22). Adding many checks cannot be assumed useful when their outcomes scarcely distinguish honest identities from attackers.

## Accuracy is not inclusion or a unique model capability

Coverage at 972 identities and 108 strong checks recovered 97.2% of the specialist facts while rejecting **62.6% of honest specialists**. At 64 checks it recovered 86.1% while rejecting **94.1%**. Repetition lets a small surviving subset carry most of the facts. This is why the retention measure matters, and why scarce or nonredundant evidence is an important boundary for a successor study.

A simple plurality reference on the identical packets also reached 100% specialist accuracy for random at 64 and 108 strong checks. It matched coverage's 86.1% at 64 and reached 100% at 108, where the model reached 97.2%. Ties abstain in that scripted reference. These observations do not establish a distinct reasoning advantage for the model; the model remains the measured answer synthesizer in the declared protocol.

## Evidence, costs and limits

Worlds 7000–7023 were held fixed across all 120 cells and were disjoint from the preceding study. There are 24 sampled clusters, with 10,000 seeded world-bootstrap draws for the reported descriptive 95% intervals. Identities, three facts, repeated packets, cells and completion frames are not extra independent samples. Intervals and secondary contrasts have no multiple-comparison adjustment. Neither observed target attainment nor its interval-envelope version is a simultaneous or real-world safety guarantee.

The scientific runtime hash is `66ea4fe1465678ff66d099eec14ea11dbf5bc69063c00e3cc57249e06db98f08`, executed at revision `e9db4c58a8847d2f54d60a8ff3cc70f81f58263e`. The completed saved-data audit ran in the original Linux environment with Python 3.12 and frozen dependencies. It regenerated all assignments and world snapshots, verified packets and check trajectories, recomputed grades and the complete analysis, and reconciled calls, tokens, conservative reservations and reported costs. Every scientific field matched exactly; display coordinates also matched exactly (zero differences, within the verifier's 1e-15 platform tolerance). The redundant local full reconstruction was interrupted after this complete audit passed and is not counted as another pass. Local visuals were separately rebuilt, inspected and fully decoded, as recorded in the [local reporting receipt](records/s1-001-local-reporting.json). See the [verification receipt](verification-summary.json), [execution summary](execution-summary.json) and [post-mortem](reviews/s1-001-post.md).

Main S1 used 38,754,668 input tokens and 118,904 output tokens across 2,880 calls, all with reported usage. Preparation and collection took 3,475.74 seconds (57m55.7s), with rendering and upload additional. Q0 and S1 together used 2,896 calls and cost $39.672176. The $130.754844 cumulative conservative reservation is not the amount billed. [Reconciled accounting](records/followups-accounting.json) totals both follow-ups' Q0 and S1 stages at 4,876 calls and $42.804395, with no unknown usage; copied checkpoints and administrative peer-allocation holds are excluded.

The public repository retains the [complete compressed synthetic outcome journal](records/s1-001-episodes.jsonl.gz), all cell statistics, paired contrasts and [publication receipt](records/s1-001-artifact-receipt.json). Full assignment/world snapshots and original analysis remain in the durable run artifacts; frozen source and seeds regenerate the inputs. The outcome journal's SHA-256 is `d1ba1907bd5eb5ca51e9198ae0db760479120ba29864a4639b08c02ecb761822`.

The fixed graph family, two initial trust seeds, half-population admission, independent simulated checks, one attacker using a +7 fabrication, one pinned model and highly repeated facts limit generalization. This is not evidence about hundreds of autonomous model agents or adaptive real-world attackers.

The owner waived independent review; same-owner engineering and scoring audits do not replace it. Plans and source were preserved before paid collection, but the historical public registration used a mutable branch URL and lacks an immutable public-plan content-hash receipt. This is a **retrospective process failure**, not a passed preregistration gate; the later [setup index](SETUP.md) cannot repair its chronology. No held-out confirmation or S2 was run. This completed study motivates further plans but authorizes no new launch.
