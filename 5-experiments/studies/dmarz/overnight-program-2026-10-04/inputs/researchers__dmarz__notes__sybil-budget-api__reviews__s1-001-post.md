# Post-mortem: s1-001

- Experiment / owner / stage / date: sybil-budget-api / dmarz / exploratory S1 / 2026-10-04.
- Parent: [Q0 post-mortem](q0-001-post.md), run `sybil-budget-api/7b177592`; [S1 preassessment](s1-001-pre.md).
- Run: [`sybil-budget-api/46ebda03`](https://swarm-live.pages.dev/#/r/sybil-budget-api%2F46ebda03), one attempt on `sim-dmarz-4` under `dmarz-sybil-followups`.
- Execution revision: `e9db4c58a8847d2f54d60a8ff3cc70f81f58263e`. Scientific fingerprint: `66ea4fe1465678ff66d099eec14ea11dbf5bc69063c00e3cc57249e06db98f08`. Python 3.12, frozen pinned requirements and `claude-haiku-4-5-20251001`; no scientific source/config changes after qualification.
- Disposition: **complete-valid-result** for this bounded exploratory question. Resource release is complete; see the [closeout receipt](../records/closeout.json). No rerun, S2 or successor launch is authorized.
- Assessment: same-owner engineering and scientific audit. The owner explicitly waived independent review; none is represented as passed.

## What ran and what happened

The full grid crossed two population sizes, six checking budgets, five attacker check-pass probabilities and two policies: 120 cells, each measured on the same 24 fresh sampled world roots. All **2,880 assigned → 2,880 started → 2,880 terminal → 2,880 graded → 2,880 analyzed** outcomes reconcile. There were zero invalid, failed, missing or not-started outcomes and no duplicate episode IDs. Every declared cell and world is retained. The 240 stored world variants are generated from 24 paired roots, not 240 independent samples.

S1 made 2,880 API calls with usage reported for all of them, consuming 38,754,668 input tokens and 118,904 output tokens for **$39.349188**. Preparation and collection took 3,475.74 seconds; rendering and uploads followed. Two concurrent requests ran within one finite worker, with no retries or replacement attempts. No reporting errors were recorded. The worker exited after publishing its artifacts.

The combined budget-study Q0/S1 ledger reconciles 2,896 calls and **$39.672176 actual cost**, distinct from **$130.754844 cumulative conservative reservations**. The calls stayed below the 3,200 limit and reservations below $140. The fixed $10 peer-allocation hold on this host was an administrative spending reservation, not billed model work or unknown usage. The [combined ledger receipt](../records/followups-accounting.json) counts each study once and reports 4,876 calls / $42.804395 for both follow-ups' Q0 and S1, with zero unknown usage. Copied shared checkpoints and allocation holds are excluded.

The predeclared primary comparison, coverage at 972 identities with 10% attacker pass probability, reproduced the earlier direction. Increasing checks from four to 108 raised specialist accuracy from **40.3% to 97.2%**: **+56.9 percentage points**, paired descriptive 95% interval **+43.1 to +70.8**, using 24 world clusters. Attacker seat share fell by 8.65 points (−10.25 to −7.11), and honest specialist retention rose by 14.3 points (+11.4 to +17.1).

The grid adds a more consequential boundary: **seven cells met the point-mean joint target, all at attacker pass probability 10%; no cells met it at 30–90%**. Coverage at 324 identities passed with 32 checks but failed with 64 and 108 because attacker seat share rose from 1.98% to 8.51% and 10.70%, despite accuracy rising from 97.2% to 98.6% and 100%. The predeclared refusal to assume monotonicity was necessary.

Equal-budget comparisons reveal competing objectives. At 972 identities and 64 strong checks, random checking produced 100% accuracy / 4.82% attacker seats / 52.9% specialist retention, while coverage produced 86.1% / 0.63% / 5.9%. Coverage minus random accuracy was −13.9 points (−25.0 to −4.2), attacker seats −4.19 (−5.33 to −3.10) and retention −47.0 (−50.5 to −43.6). Random's attacker-seat interval crossed 5%, so its point-mean crossing is not a stable security boundary. Comparisons across different checking budgets are frontier descriptions, not equal-resource policy superiority claims.

At 972 identities and 90% attacker pass probability, four and 108 coverage checks both produced 43.1% accuracy. The paired difference was 0.0 points (−15.3 to +15.3), while attacker seat share rose 9.53 points (+7.78 to +11.22). Weakly distinguishing checks can worsen admission without improving answer recovery. Full results, retention measures, reference plurality outputs, all grid cells and 12 descriptive prior-study anchors are in [RESULTS.md](../RESULTS.md) and [aggregate JSON](../results-summary.json).

## Qualification and saved-data audit

Fleet S0 had passed all 256 scripted cases at the same fingerprint. The separate clean Q0 had passed all 16 packets, both population sizes and all 24 required missing-fact abstentions. Those competence gates establish that this unchanged instrument can parse the task and abstain when facts are absent; they do not establish security efficacy. S1's saved summary correctly has `qualification: null`. The hub's generic `qualification_passed` completion flag is not a new clean-competence test.

The same-owner [verifier](../reporting/verify_results.py) passed in the original Linux environment using Python 3.12 and frozen requirements. It regenerated all 2,880 assignments and 240 stored world variants from frozen source and declared seeds and compared all decision fields, actor packets, check trajectories, graph metrics, answers, grades and full analysis. It checks source/revision provenance, unique IDs, every execution counter, actual check counts, monotone completion times, request reservations, token prices, per-call usage and initial/final ledger deltas. Actor-packet keys exclude evaluator truth and principal ownership. No paid request is issued by this audit.

All scientific fields match exactly. The verifier permits a stated 1e-15 tolerance only for display-only `sin`/`cos` coordinates; the completed Linux audit observed zero such differences. The [verification receipt](../verification-summary.json) and its [exact archived copy](../records/s1-001-linux-verification.json) retain the full pass and verifier hash. A redundant local full reconstruction was interrupted, at the operator's direction, after this equivalent complete audit passed; it is not counted as a local verification pass or failed experimental attempt. No model call or worker was affected. The [local reporting receipt](../records/s1-001-local-reporting.json) records that distinction. All 25 locally regenerated GIF frames separately decoded at 1920×1440. The [execution summary](../execution-summary.json) records final counters and cost.

Saved-data reproduction, from the repository root in the matching Python/dependency environment, uses:

```sh
python researchers/dmarz/notes/sybil-budget-api/reporting/verify_results.py data/sybil-followups/budget-s1
python researchers/dmarz/notes/sybil-budget-api/reporting/build_report.py data/sybil-followups/budget-s1
```

The frozen `render.replay` was also rerun with saved episodes, stage S1, planned count 2,880 and the saved initial study accounting. These commands analyze retained observations only. The report builder emits aggregate tables and an initial report; the committed RESULTS prose adds the reviewed interpretation and process limits.

## Visualization review

[Mapping v1](../VISUALIZATION.md) was preserved. Published outputs include initial/progress/final PNGs, the retention companion and a 25-frame GIF sampling actual recorded completion progress from zero to all 2,880 outcomes. Static cells are final 24-world means; partial frames use only completed observations. Pending values are not zeros. Yellow outlines require a complete cell and both point-mean engineering thresholds.

Local final and retention images were rebuilt from the saved outcomes and visually inspected. Labels, complete counts, costs and key frontier cells agree with the aggregate analysis. The operator checksum-verified all ten durable artifacts, confirmed public final and retention views, and observed GIF progression from zero to 1,080 completions; the final PNG shows 2,880/2,880. The local decoder separately verified every GIF frame. The [publication receipt](../records/s1-001-artifact-receipt.json) preserves these distinct checks.

The animation depicts collection, not simulated conversations or temporal social behavior. It makes pending/completed coverage visible; the final heatmaps expose nonmonotonic admission and the retention companion exposes exclusion hidden by accuracy. No rendering defect required a model rerun. Future figures could make uncertainty more visible alongside the point-mean target, but changing the frozen figure after seeing results is not necessary to validate this run.

## Experiment-quality assessment

This run meaningfully tests its bounded budget/reliability question: the complete declared factorial grid, paired worlds, equal-budget comparator and retained exclusion metric distinguish accuracy gains from attacker exclusion and honest access. All outcomes are present and the unchanged inputs, grades and accounting are independently recomputed from saved records by the same owning workflow.

Its evidence remains fixture-bound. The independent unit is 24 sampled world roots; calls, identities and repeated facts do not increase that count. Descriptive intervals use 10,000 seeded bootstrap draws and are not adjusted for 120-cell exploration. A 100–100% bootstrap interval at an observed ceiling does not prove perfect future accuracy. A cell-mean target or its interval-envelope version is not a safety guarantee. No endpoint is held-out confirmation.

The single graph family, two trusted seeds, fixed admission fraction, independent simulated checks, +7 fabrication and one pinned synthesizer limit transfer. Three specialist facts are highly repeated: coverage with 108 strong checks at 972 identities recovered 97.2% while rejecting 62.6% of honest specialists. Simple plurality on the same packets can match or exceed the model in key high-accuracy cells. No unique model reasoning advantage or real-world Sybil resistance follows.

Scientific execution and qualification passed, but a historical process requirement did not: the registered public plan used a mutable branch URL and lacks a pre-launch immutable content-hash/fetch receipt. The later setup runbook and retrospective [SETUP.md](../SETUP.md) do not cure that chronology. Record this as a **retrospective process failure**, not a passed preregistration gate. The independent-review waiver is a separate explicit owner decision and does not waive accurate accounting or public-plan provenance.

For the shared evidence entry, the operator updates confidence and sample-size metadata after this audit. The supported sample statement is: S1 24 paired world clusters × 120 cells = 2,880/2,880 valid outcomes, zero missing; separate Q0 four worlds/16 exact packets. The appropriate rationale is completed, fully reconciled exploratory evidence for this synthetic grid, limited by 24 clusters, shared repeated facts and no independent review. Earlier cohorts remain separate; a successful execution is not itself evidence of general security.

## Failure and repair ledger

| ID / kind | Observed evidence | Cause / disposition | Repair or next requirement | Acceptance / status |
|---|---|---|---|---|
| Historical public-plan provenance | Mutable registered branch URL; no pre-launch immutable content-hash receipt | Retrospective process failure; does not invalidate saved arithmetic but limits preregistration claims | Apply current immutable-plan admission prospectively to any later attempt | Historical gap remains; never backfilled as passed |
| API or collection failure | Zero failed/invalid/not-started out of 2,880; all usage known | None observed | No rerun | Complete |
| Saved-input verification | All fields, counters and accounting reproduced on original Linux; zero display-coordinate differences | No discrepancy observed in completed audit | Preserve 1e-15 display tolerance and strict scientific comparisons | Full Linux receipt passed |
| Redundant local full audit | Still reconstructing when equivalent Linux audit passed | Operator ended redundant saved-data computation; no model work affected | Record interruption without claiming a local full pass; retain separately completed local image/replay checks | Local reporting receipt; no rerun |
| Nonmonotone target and weak-check harm | Coverage at N324 passes 32 then fails 64/108; weak N972 endpoint admits more attackers | Valid scientific adverse outcomes, not implementation failures | Report entire grid and retention; do not retry to improve scores | Complete valid result |
| Public visualization | Ten artifacts checksum-verified; local replay fully decoded; public views/playback observed | No observed reporting defect | Preserve receipts and source | Complete |
| Resource closure | Worker and audit exited; original accounting archived on private GitHub | PR167 merged; hub event 38372 confirms claim absent from active allocations | Existing host retained for owner lifecycle management; [receipt](../records/closeout.json) | Complete |

Earlier software-test and caption defects remain in the linked S0 post-mortems and were fixed before qualification. No runtime, scientific condition, seed or evaluator was repaired after S1 collection.

## Next work is a plan only

The [scarcity follow-up plan](../../sybil-scarcity-plan/README.md) joins this result with the separate newcomer study. A useful next question is whether apparently robust answer recovery survives when specialists carry scarce or nonredundant evidence; repetition is a plausible alternative explanation for high accuracy despite low retention. Its paired contrasts, controls, new fixtures and admission gates belong in that separate prospective plan.

The owner requested a plan without starting it. No attempt ID, model budget expenditure or new launch is created here. The current operational instruction prohibits new launches from halcyon; any future work requires the current runbook and the authorized remote-owner workflow. Formal S2 remains disabled and holdout 10000–19999 remains untouched. The [closeout receipt](../records/closeout.json) records completed resource release and archived accounting for this study.

### Final operational closeout

Merged claim release PR167 and hub release event 38372 were read back; the claim is absent from active allocations. The worker and saved-data audit have exited, all ten durable artifacts were verified, and original accounting archives are merged privately through PR166. The existing host is retained for owner lifecycle management. The release mirror initially used an interpreter without the reporting module; it failed before sending an event, was corrected to use the installed path, and then passed readback. No scientific run or model request was repeated.
