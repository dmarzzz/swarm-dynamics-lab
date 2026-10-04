# Healing Helping Hands

A living evidence atlas with 200 document scouts. **Exploratory S0 reference pilot completed; Qwen-derived conditions remain unqualified.** [Full assessment](ASSESSMENT.md) · [Pilot-03 pre-run plan](reviews/pilot-03-pre.md) · [Pilot-03 post-mortem](reviews/pilot-03-post.md) · [Reproduction](DEPLOYMENT.md) · [Agent definitions](agent-definitions.json)

## TLDR

Can an evidence atlas recover when scouts lose memory and source reports are withdrawn? We compare sharing documents alone with sharing documents plus withdrawal notices, using the same reports and damage. The qualified Jev reference and exact controls completed 72 worlds across three synthetic corpora. Forwarding notices reduced mean post-event error by 28.1 percentage points and removed stale citations by the final frame. Qwen and Laya repairs failed competence gates; the 108 Qwen-derived assignments remain not-run. This validates a programmed evidence-repair mechanism with model-backed extraction, not autonomous scientific research or heterogeneous-head superiority.

[Watch the measured 200-scout replay](https://swarm-live.pages.dev/api/a/healing-helping-hands/pilot-03-review/recovery.gif) · [Outcome figure](https://swarm-live.pages.dev/api/a/healing-helping-hands/pilot-03-review/outcomes.png) · [Swarm Lab runs](https://swarm-live.pages.dev/#/x/healing-helping-hands)

## PI follow-through — 2026-10-04 UTC

The [practical-01 post-mortem](practical/POST-01.md) reports all 180 assignments complete with zero new model calls. No scenario met the prospective utility rule for peer-verified versus central-append; central-verified was stronger still. The [practical plan](practical/PLAN.md) incorporates the [PI review's](https://github.com/dmarzzz/swarm-lab/blob/e0a3170/researchers/dmarz/notes/next-experiments-2026-10-04/README.md) central-index, legitimate-learning and unreliable-lineage comparisons. This adverse saved-tape architecture result is retained separately from the pilot-03 model-extraction results below. Historical live reporting failed; retrospective publication does not repair that process outcome.

Interpret the planned peer policy against **central-verified** as well as central-append. Both verified policies use the same supplied issuer/root metadata. Beating an index that cannot process withdrawals would establish less than beating this stronger baseline. Supplied authentication is not a learned detector or a cryptographic implementation, and a missing target must remain unresolved rather than being recovered from evaluator truth.

The 180 assignments reuse three known semantic corpora with two placement layouts. Corpora are the semantic clusters; layouts, curators, claims and rounds are dependent repeats. Report corpus-level contrasts and ranges, not 180 independent replications or a fresh Jev competence result. Integrated incorrect-or-missing queries must be read jointly with legitimate-update retention, false invalidations, stale citations and traffic.

The central-outage condition disconnects central clients while preserving the mesh. It is an explicit architecture stress test, not evidence that decentralization is universally more reliable. Keep no-outage comparisons and the strong central cache/recovery baseline visible; report actual transport and latency differences rather than claiming equal resources. The [practical-02 assessment](practical/PRE-02.md) prospectively changes only the mesh packet cap from 4 to 16. This is a paired capacity sensitivity on reused evidence, not an independent replication or a warrant for further cap tuning until an advantage appears. A later efficacy study needs independently authored corpora and measured failure regimes. Prior outcomes and unqualified Qwen/Laya conditions are unchanged.

## Question and prediction

Does propagating source-withdrawal notices reduce atlas error and stale citations compared with keeping the same notices local? We expect a benefit when sources are withdrawn, and no benefit when no withdrawal occurs. A separate erasure scenario tests whether neighboring memories restore missing records. Exact extraction distinguishes semantic mistakes from memory-propagation mistakes. The original Qwen/independent-head question remains blocked by qualification; Jev-only was added as a separately named reference, never substituted into a Qwen condition.

## Setup

Twenty fictional improvement claims each have five independent source roots and two copies per root: 100 roots, 200 reports, 200 scout identities on a 20 × 10 four-neighbor grid. Scout i curates claim i modulo 20, giving ten curators per claim. Each model reads one claim/report pair and emits SUPPORT, REFUTE or UNCERTAIN. Source IDs and authenticated withdrawal notices are supplied metadata. The evaluator alone knows fixture labels and which sources remain valid.

Models perform semantic extraction once per report; all subsequent communication, deduplication, tombstones and aggregation are deterministic. These are separate memories and identities sharing model weights, not 200 independently loaded models or language agents reasoning every round. Source copies count once; contradictory copy labels become UNCERTAIN. A scout aggregates its local source-balanced evidence, and the atlas takes the majority of that claim's ten curators, with ties UNCERTAIN.

Gold is the source-balanced consensus of surviving fictional reports, not scientific truth. More supporting than refuting roots yields SUPPORT; the reverse yields REFUTE; ties/no informative roots yield UNCERTAIN.

## Protocol

The executed pilot-03 source and prospective plan are frozen at [46678b2b99936383d01b268075e0ae2cf8b405fc](https://github.com/dmarzzz/swarm-lab/blob/46678b2b99936383d01b268075e0ae2cf8b405fc/researchers/vishesh/notes/healing-helping-hands/README.md). The launcher verified the registered public plan and exact tracked source before calls. Every subsequent attempt requires a new pre-run assessment; this result page is not an instruction to rerun failed conditions.

Fresh qualification: 60 previously unexecuted reports, 20 per label, seed 8601; threshold >=85% overall, >=70% per label and no provider/schema errors. Jev uses `typesafe/jev-1.13`, TypeSafe-only routing, no fallbacks, and requires served snapshot `typesafe/jev-1.13-20260917`. Exact wire option order is preserved and audited. Jev passed 60/60 and classified all 600 pilot reports correctly.

Pilot seeds 8701–8703 are paired across policies/scenarios; each seed reuses one frozen extraction tape. Policies: no sharing, evidence-only, evidence plus withdrawal notices. Scenarios: no event, withdrawal only, erasure only, combined. Five assigned extraction definitions (exact, Qwen, Qwen+Qwen, Qwen+Laya, Jev reference) × three policies × four scenarios × three seeds = 180 assignments: 72 completed, 108 Qwen-derived not-run. No statistical independence is claimed for agents, frames or paired worlds.

All worlds have 24 synchronous rounds. Before round 10's exchange, withdrawal removes one seeded root per claim and delivers a notice to the original scout. Erasure clears memory/notices in a seeded contiguous 5 × 8 block of 40 scouts. Combined erases first, then delivers notices. A pre-exchange event snapshot verifies the damage; plotted round frames are measured after exchange. Both sharing policies propagate evidence; only the notice-sharing policy forwards withdrawal tombstones. No-sharing retains local information.

The dedicated sim-vishesh allocation, fixed source, response pins, append-only call journal, terminal assignment records and no-retry policy are documented in [deployment](DEPLOYMENT.md). The pilot used 660 Jev calls in 274.1 seconds; cumulative Jev usage, including the earlier qualification, was 720 calls / $0.013004124 against a single unchanged $0.10 ledger cap. Credentials stayed in the local forwarding process. Held-out seeds 8301–8310 remain untouched.

## Metrics

Primary: mean atlas error over post-exchange rounds 10–23, compared as notice-sharing minus evidence-only within seed/arm. Negative differences favor sharing notices. Report three seed-level contrasts and their mean/range, not confidence intervals or hundreds of false replicates.

Secondary: 200-scout local accuracy, 20-claim atlas accuracy, unique valid informative-source coverage, stale-citation fraction, abstention, false confident assertions, final accuracy and rounds to >=95% atlas accuracy for three rounds. A null recovery stays null. Interpret recovery with pre-event competence and actual initial damage. Calls, input tokens, costs, latency and failed/not-run denominators are retained. An always-uncertain baseline is a labeled post-hoc sanity check.

| Combined scenario, Jev reference | Seed 8701 | Seed 8702 | Seed 8703 |
|---|---:|---:|---:|
| Post-event error reduction vs evidence-only | 28.9 pp | 30.4 pp | 25.0 pp |
| Notice-sharing final accuracy | 100% | 100% | 100% |
| Evidence-only final accuracy | 65% | 65% | 70% |
| Notice-sharing final stale citations | 0% | 0% | 0% |
| Evidence-only final stale citations | 18.4% | 18.4% | 23.1% |
| Always-uncertain final accuracy | 75% | 65% | 50% |

No-event and erasure-only differences between sharing policies are exactly zero. Erasure-only loses 40 memories and drops coverage to 84% before exchange; coverage returns fully at rounds 12, 11 and 13. Exact and Jev trajectories coincide because Jev made no extraction errors on these fixtures. [Machine-readable summary](results-summary.json).

## Visualization and reliability

Recorded replay includes the 200-scout grid, 20-claim atlas, evaluator-labeled source inspection, paired curves, event boundary and pre-exchange damage count. Seed/arm/scenario controls expose the design; unavailable Qwen worlds show not-run. The representative animation is the planned first seed + combined case, not a best-outcome selection. Animation time is logical time, not inference wall time.

Public Swarm Lab supports the GIF and PNGs, plus per-world metric traces and final frames. The richer HTML player is available locally/private-download; standalone public HTML hosting has not been verified. Rendering uses saved data only. Keyboard/mobile/playback/missing-data checks passed. Twenty-two offline checks passed, all 144 completed worlds across the three pilots replayed exactly, and all 660 new API wire hashes reconciled with the budget ledger. This supports the bounded implementation; it does not guarantee no future failures.

## Attempt history and preserved failures

| Attempt | Outcome | Review |
|---|---|---|
| Routing v1 (`regrowth-200`) | Completed routing worlds, weak shortest paths; public plan missing at execution | [Original review](REVIEW.md); separate failed plan-registration audit retained |
| Pilot-01 | Qwen 25/30 failed; Laya 27/30 passed; 36 exact worlds, 108 model worlds not-run | [Review](ATTEMPT-01-REVIEW.md) |
| Pilot-02 | Typed Qwen interface 40/60 failed; Laya 51/60 failed per-class gate; 36 exact worlds, 108 not-run | [Review](reviews/pilot-02-post.md) |
| Diagnostic-03 | Neutral/thinking Qwen and explicit Laya all failed development gates | [Pre-run](reviews/diagnostic-03-pre.md), [review](reviews/diagnostic-03-post.md) |
| Diagnostic-04 | Report-only Qwen 12/18 and Laya 16/18 failed development gates | [Pre-run](reviews/diagnostic-04-pre.md), [review](reviews/diagnostic-04-post.md) |
| Jev qualification-01 | 60/60 semantic pass; option-order transport defect retained as failed control | [Pre-run](reviews/jev-qualification-01-pre.md), [review](reviews/jev-qualification-01-post.md) |
| Pilot-03 | Fresh ordered qualification 60/60; 72 reference worlds completed, 108 Qwen-derived not-run | [Pre-run](reviews/pilot-03-pre.md), [review](reviews/pilot-03-post.md) |

## Research basis and interpretation limits

[FEVER](https://fever.ai/dataset/fever.html) motivates three-way claim/evidence classification; [ALCE](https://arxiv.org/abs/2305.14627) motivates citation-support measurement; [FActScore](https://arxiv.org/abs/2305.14251) motivates atomic claim checks. These were inspected at abstract/task-description depth; this is neither their benchmark nor a gate-passed prior-art survey.

The study teaches that restoring missing documents and invalidating obsolete evidence need different messages, and that correct transport cannot replace semantic competence. It demonstrates a programmed mechanism with a qualified reference extractor on engineered fixtures. It does not establish successful Qwen heterogeneity, autonomous research, robustness to forged metadata/partitions, or performance on real scientific literature. [The assessment](ASSESSMENT.md) specifies those remaining gates.
