# Results: Sybil resistance as swarms grow

Completed 2026-10-04. Exploratory S1, 24 paired world clusters, 100 conditions and 2,400 valid model answers. All planned calls completed once; no failed, missing, duplicate or retried assignments. Scripted rehearsal and clean API qualification passed before collection. Total reported-usage cost, including qualification: **USD 19.453925**.

Increasing the verification budget with population preserved specialist answers when checks distinguished honest identities from attackers. Keeping four coverage checks did not preserve the small-world behavior. The benefit is not unique to coverage selection: random checking at the same proportional budget reached the same largest-world accuracy. Weak checks did not provide a comparable security benefit.

## The scaling result

The table shows coverage selection with visible badges. “Strong” checks pass honest identities 90% of the time and attackers 10%; “weak” checks pass both 90%. Accuracy is correctness on the three specialist facts. Attacker share is the percentage of admitted seats occupied by attacker identities, not the percentage of attackers admitted.

| Identities | Fixed / proportional checks | Strong-check accuracy, fixed / proportional | Strong-check attacker share, fixed / proportional | Weak-check accuracy, fixed / proportional | Weak-check attacker share, fixed / proportional |
|---:|---:|---:|---:|---:|---:|
| 36 | 4 / 4 | 76.4% / 76.4% | 8.3% / 8.3% | 40.3% / 40.3% | 36.1% / 36.1% |
| 108 | 4 / 12 | 5.6% / 83.3% | 0.7% / 3.5% | 5.6% / 44.4% | 0.7% / 26.3% |
| 324 | 4 / 36 | 33.3% / 94.4% | 7.7% / 3.0% | 37.5% / 50.0% | 7.7% / 22.0% |
| 972 | 4 / 108 | 47.2% / 98.6% | 11.5% / 3.6% | 45.8% / 52.8% | 11.5% / 21.5% |

The frozen primary contrast at 972 identities is **+51.4 percentage points** of specialist accuracy, with a descriptive paired-world 95% bootstrap interval of **+38.9 to +62.5 points**. The 36-identity budget contrast is exactly zero because its four-check observation is reused. The primary difference exceeds the predeclared 10-point practical threshold in this fixture. Attacker seat share simultaneously falls by **7.9 points** (descriptive interval −9.1 to −6.7). This compares 108 checks with four, not equal-cost policies.

At 972 with weak checks, the accuracy difference is only **+6.9 points** (−5.6 to +19.4), while attacker seat share rises by **10.0 points** (+8.5 to +11.5). More checking can therefore make admission less secure when the check itself cannot distinguish the attacker. The 108-identity weak condition gains useful answers but also admits substantially more attackers; it should not be called a security success.

## What explains the change

The post-collection [selection diagnostic](selection-diagnostic.json) counts the saved verification events, once per world rather than once per badge display. With four checks at 36 identities, coverage checked outside identities in every case: an average 1.17 honest specialists and 2.83 attacker identities. At 108, 324 and 972, **all four checks went to core identities in every world**. The same network-coverage objective changes its allocation as uncovered core neighborhoods grow. This is a measured allocation mechanism, not a demonstrated general law for all graphs.

With 108 checks at 972 identities, coverage checked an average 60.79 core identities, 19.04 honest specialists and 28.17 attackers. Informative checks then provide useful outside seeds and reject most checked attackers. The dip at 108 and partial recovery with fixed checking are not a monotonic “bigger is worse” curve; topology, diffusion and admission also change under the chosen graph construction.

## Controls and secondary findings

- **Random checking is competitive.** At 972 with 108 strong checks and visible badges, both coverage and random achieve 98.6% specialist accuracy. Their paired accuracy difference is 0.0 points (−4.2 to +4.2). Attacker seat shares are 3.6% and 4.0%, respectively; their difference is −0.4 points (−1.4 to +0.6). With only four strong checks, random reaches 65.3% versus coverage's 47.2%. This study does not establish that coverage is the best selection rule.
- **Degree selection still excludes specialist knowledge.** At 972 with 108 strong checks, it reaches 44.4% specialist accuracy and rejects 93.4% of honest specialists. Low attacker share alone is an inadequate success measure.
- **Badges do not show a clear large-world advantage.** At 972 with proportional coverage checks, visible minus hidden accuracy is +2.8 points (−2.8 to +9.7) under strong checks and +1.4 points (−6.9 to +8.3) under weak checks. Badge effects across all cells are reported, without selecting a favorable cell.
- **The model is not necessary for the strongest result.** Simple plurality on the same 972-identity strong/proportional coverage packets reaches 100% specialist accuracy; Haiku reaches 98.6%. With four checks, Haiku reaches 47.2% versus plurality's 23.6%, but plurality abstains on ties. Correct tie-breaking can reflect fixture-specific heuristics; it is not evidence of a general reasoning or Sybil-detection ability.
- **Errors are not mainly abstentions in the largest coverage conditions.** Of 72 specialist fields, strong/fixed coverage produces 38 incorrect non-null answers and no abstentions; strong/proportional produces one incorrect non-null answer. Weak/fixed produces 39 incorrect non-null answers and weak/proportional 34, again with no abstentions.
- **Accuracy is not broad participation.** Even the 98.6%-accurate strong/proportional coverage condition rejects 62.8% of honest specialists. Three repeated specialist facts allow high accuracy from a minority of specialists; this result does not show preservation of every contributor's unique knowledge.

## Evidence and uncertainty

All cells have 24 assigned and 24 valid observations. Independent units are worlds 6000–6023, paired across conditions. The 10,000-draw intervals are descriptive world-cluster bootstrap intervals; neither 972 identities, 72 fact fields nor 2,400 calls is the independent sample size. Secondary intervals have no multiplicity correction. There is one model invocation per assigned condition, not repeated sampling of model randomness.

Budget duplicates at 36 and no-verification budget duplicates were physically deduplicated. The planned reliability labels remain separate conditions; some no-check and core-only conditions therefore contain identical actor packets across reliability labels. Small answer differences in those controls can be model variability rather than a check-reliability effect. They are not treated as independent world replications.

This is one graph family with two initial trusted identities, fixed degree and changing graph distances, at a fixed 25% attacker population. The attacker controls more total reporting capacity as population grows. All identities, graphs and verification outcomes are simulated; only synthesis of admitted reports uses the API. The attack always fabricates truth +7 on a six-fact integer task. These results do not establish real-world identity security, robustness to adaptive attacks, or benefits from 972 independently reasoning model agents. The prior 12-world pilot used different worlds; its accuracy should not be compared with this new 36-identity sample as a matched treatment effect. No formal hypothesis was promoted and holdout 10000–19999 remains untouched.

## Validation, costs and reproduction

Nine regression tests passed, including exact agreement with the original 36-identity simulator. Fleet S0 completed 264 scripted cases. Q0 passed all 64 clean packets, 16 at each size, including every required abstention and inputs containing 972 reports. S1 then completed 2,400/2,400 once, using 18,296,288 input and 99,128 output tokens: USD 18.791928. Q0 used USD 0.661997. All 2,464 paid calls have usage records; the USD 68.300028 reservation is a conservative bound, not an additional charge. Preparation and S1 collection took 1,151.92 seconds; hub start-to-done, including final rendering/publication, was approximately 20 minutes.

Every answer was rescored against its saved assignment, packet hashes checked, scripted baselines recomputed and the full frozen analysis independently reproduced. Use Python 3.12 and the pinned requirements for bit-for-bit numeric agreement. The initial local Python 3.9/NumPy 2.0.2 check differed only in 302 floating-point entries by at most 3.33e−16; Python 3.12.13/NumPy 2.2.6 matched the Python 3.12.3 server exactly. No observation or frozen analysis was changed to obtain agreement. See [verification receipt](verification-summary.json), [aggregate JSON](results-summary.json), [all 100 cells](results-cells.csv), [deployment](DEPLOYMENT.md) and [post-mortem](reviews/s1-001-post.md).

```bash
python3.12 -m venv data/sybil-scale-api/analysis-venv
data/sybil-scale-api/analysis-venv/bin/pip install -r researchers/dmarz/notes/sybil-scale-api/requirements.txt
data/sybil-scale-api/analysis-venv/bin/python researchers/dmarz/notes/sybil-scale-api/reporting/build_report.py data/sybil-scale-api/s1-001 data/sybil-scale-api/s1-reconciled
data/sybil-scale-api/analysis-venv/bin/python researchers/dmarz/notes/sybil-scale-api/reporting/diagnose_selection.py data/sybil-scale-api/s1-001 data/sybil-scale-api/s1-reconciled/selection-diagnostic.json
```

Raw synthetic assignments, outcomes and worlds are durable hub artifacts available to the team; the public dashboard intentionally serves only allowed visual artifacts. Figures and aggregate tables are public. The worker has exited; see the deployment record for claim-release confirmation.

## Visuals and next experiment

[Completed run](https://swarm-live.pages.dev/#/r/sybil-scale-api%2F56defc84) · [final chart](https://swarm-live.pages.dev/api/a/sybil-scale-api/56defc84/final_frame.png) · [measured replay](https://swarm-live.pages.dev/api/a/sybil-scale-api/56defc84/replay.gif) · [hidden badges](https://swarm-live.pages.dev/api/a/sybil-scale-api/56defc84/badges_hidden.png). All 30 uploaded artifacts across the three fleet stages passed hash checks; all 99 GIF frames decoded. Replay shows accumulation of completed observations, not agent conversations. Final plots show all 24 worlds per cell; uncertainty is in the tables and paired contrasts.

The next useful study would locate the smallest reliable checking budget at 324 and 972 identities, comparing coverage with random selection at equal cost and sweeping intermediate attacker pass rates. Counterbalance fabrication direction and require more distinct specialist facts to test whether the current success depends on repeated easy facts. A fixed-attacker-resource identity-splitting condition would separately test Sybil amplification. These are recommendations, not additional runs launched under this completed plan.
