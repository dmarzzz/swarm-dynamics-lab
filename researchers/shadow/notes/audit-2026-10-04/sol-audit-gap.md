# Strategy audit: make the investigation tool the headline

Author: shadow/sol-audit-gap. Cutoff: 2026-10-04 15:02Z, repository `66fa0aa6`; report fetched 14:58Z. This is a strategy judgement, not a published judging rubric. The event has no published scoring rubric. The local owner-provided BRIEF-2026-10-03.md transcribes the organisers' project examples and submission requirements.

## What judges are likely to value

The event's stated motivation is tools they wished they had for the Hugging Face incident. Its examples explicitly include reusable questions about multi-agent groups, information spread, beyond-transcript forensics and incident meta-science. I would optimise for: (1) a stranger can load an incident export and get an answer in one command, (2) one nontrivial, checkable result on the supplied real data, (3) uncertainty and provenance are visible, (4) a two-minute demonstration with a clear changed decision. These are my inferred priorities, not promises about Grove/AI Village judges.

The present packet is credible but aimed at a somewhat different project. [WRITEUP](../submission/WRITEUP.md) leads with 3,300 library entries, 157 agent ids and pipeline gates. [RESULTS](../submission/RESULTS.md) correctly says all its findings are synthetic. The [public report](https://swarm-report-shadow.pages.dev) repeats that no supplied incident dataset was analysed. The strong Sybil experiments and independent [xcheck](../completed-findings-xcheck/README.md) are valuable and should stay, but another synthetic setting has diminishing submission value relative to one real-data, reproducible forensic view.

We are not missing an entire project. The pipeline, saved records and checks exist. The missing layer is an incident-facing front door, a validated answer, and a short story connecting the real-data tool to the team's strongest theme: **more records or identities do not mean more independent evidence**. [Landscape](../../../../synthesis/landscape.md) section 4 already identifies that shared theme across dmarz and vishesh. Avoid implying that library counts or gate compliance prove research quality: the same map says the LLM survey still has a revise verdict, and the submission acknowledges review waivers.

## Ranked additional findings, cheapest first

Estimates are bounded working time, not guarantees; all dollar figures are incremental API spend. Active Wave 3 lanes retain their ownership.

| Rank | Question / deliverable | Hours | USD | Owner and non-overlap | Submission value / kill criterion |
|---|---|---:|---:|---|---|
| 1 | **Evidence depth in SwarmTraces:** how often does a payload have a linked response rather than only another recovered artifact? How much do redacted duplicate rows and child artifacts distort record counts? Exact parent-graph census plus a reusable coverage card. | 1–2 | 0 | **us, sol-audit-gap, selected now.** Not identity extraction, chronology, lexical clustering or adoption. | Turns a known qualitative limitation into auditable denominators. Helps investigators distinguish attempted activity, reconstruction and observed response. If almost all payloads have responses, report that; never infer success from a response-kind label. |
| 2 | **Deletion is not containment:** page-level return after observed wiki delete events, restricted to exact page links and reliable clocks; report same-page later saves and administrative ambiguity. | 2–3 | 0 | us, only after checking no owner has claimed it; currently not selected. | A concrete incident-response question outside prior copying work. Stop if deletion-to-page linkage or timestamp quality cannot identify a denominator; no causal claim that deletion caused persistence or failure. |
| 3 | **Provenance changes a decision, not just a chart:** duplication-invariance test on an existing lineage fixture, comparing baseline, explicit ancestry, and exact-root aggregation under fixed underlying evidence. | 2–3 | 0 pool, at most 5 fallback if separately allocated | vishesh owns Quorum of Mirrors; us/factory can run a separate authorised replica, not edit or launch their run. | Bridges forensic provenance and vishesh's 0/8 full-lineage result. Must first pass a clean/no-copy control and show valid paired cases; a baseline failure is diagnostic, not a successful intervention. Lower priority because it remains synthetic and factory may cover it. |

The largest *overall* remaining payoff is already owned: AskSwarm plus half-life and identity comparisons on real corpora. Do not spawn a duplicate fifth clustering pipeline. My rank 1 is the highest-value unowned addition, not a claim it outranks delivery of those existing lanes.

## What not to do in the remaining hours

- Do not expand the library merely to raise its count. The landscape's transfers are post-hackathon directions, not a mandate to start transfer entropy, quorum mechanisms or a new physics sweep tonight.
- Do not label lexical reuse as causal influence, wiki retained text as a fresh endorsement, null SwarmTraces clocks as a timeline, or nicknames as verified agents. The [AskSwarm plan](../wild-askswarm/PLAN.md) already gets these limits right.
- Do not advertise a ranked leaderboard across datasets with incompatible collection mechanisms. Show coverage and unavailable fields beside each number.
- Do not spend the afternoon launching every READY study. Deliver a narrow tool plus three well-supported results, with the rest linked in an appendix.
- Do not call a self-check independent review, a model-call count an independent sample size, or a corrected historical plan preregistration.

## Top five actions before 00:00Z

1. **us / sol-askswarm + sol-submit:** lead the demo with one input command and three honest coverage cards; include one real incident and our own git swarm. Payoff: direct fit to the organisers' tool categories in the first 30 seconds.
2. **us / sol-audit-gap:** ship the parent-linked evidence-depth census and explicit missing-outcome card. Payoff: a zero-dollar real-data result and guard against turning attempted actions into success claims.
3. **us / sol-halflife + sol-identity:** prioritise a defensible common metric and its measurement sensitivity over additional charts. Preserve null times and identity ambiguity. Payoff: cross-swarm extension rather than re-discovery of arXiv 2609.09150.
4. **dmarz:** nominate two strongest completed, re-scored Sybil findings and freeze their exact numbers/links for submission; label scripted admission versus model synthesis. Payoff: retain the strongest experimental evidence without a catalogue of ten competing headlines. No request to change or launch their files is made here.
5. **vishesh + us / sol-submit:** use lineage/Phantom Coast as the mechanism bridge, but call failed qualification and small synthetic fixtures what they are; refresh WRITEUP/RESULTS/report once real-data outputs land and rehearse a two-minute offline demo. Payoff: one coherent story and no stale 'no wild data' statement.

## Sources and scope

Read: submission WRITEUP and RESULTS at this cutoff; live public report; synthesis/landscape.md; Gaps in surveys/sybil-resistance.md, fork-merge-security.md, vishesh-decision-models.md and llm-agent-swarms.md; owner brief and Wave 3/4 lane list. The Sybil survey's provenance-detection gap and the decision-model survey's requirement for an identifiable intervention favour a lineage-aware forensic view. The fork-merge survey gaps concern fresh experiments that cannot credibly be resolved by an afternoon's paperwork. Source reports already disclose missing times and incomplete outcomes; our selected analysis is a measurement and tooling contribution, not discovery of those facts.
