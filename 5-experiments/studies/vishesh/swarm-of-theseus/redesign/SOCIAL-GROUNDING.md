# X discussion check and scenario selection

2026-10-04 UTC. Targeted user-requested research, not a representative survey of X, a completed novelty gate, or a new model experiment. Conclusion: **do not claim the original three scenarios are the most compelling or novel**. The sources support a practical continuity problem, while also showing that memory benefits and intergenerational behavior are already familiar ideas.

## Sources actually checked

Original public X pages were opened in the browser. Search-engine copies helped discovery; they were not treated as proof that an account or conversation was still available. No messages, likes, follows or posts were sent. Summaries below distinguish author claims from our proposed tests. No engagement count is used as evidence of scientific validity.

| Source and date | Access and evidence level | Relevant point | Design consequence |
|---|---|---|---|
| [sysls, long-running autonomous engineering workflows](https://x.com/systematicls/status/2038241033755168959), March 29, 2026 | Full article body read on the original X page; replies not reviewed. Practitioner explanation with a product interest, not a controlled study. | Describes handoff fidelity, gradual deviation from requested work, weak verification, and contradictions between changed code and old documentation. | Measure whether inherited practices preserve original acceptance criteria across replacements. Score outcomes with an evaluator the crew cannot rewrite; distinguish archive contents from actual use. |
| [Edward Hughes, cultural evolution of cooperation](https://x.com/edwardfhughes/status/1868624695329018072), December 16, 2024 | Original root and first five author replies read live; remaining author-thread text read in the existing lab archive, not independently re-fetched. Author research thread linked to [[vallinder-2024-cultural]]. | Reports different cooperation dynamics by base model, generational strategy transmission and increasing strategy complexity. | Multi-generation behavior is prior art. Add model-family replacement as a separate factor; qualify each model individually and avoid attributing raw capability changes to cultural loss. |
| [Letta, managed memory and terminal tasks](https://x.com/Letta_AI/status/1952803317836304450), August 5, 2025 | Selected post and two visible preceding author posts read on original X page. Vendor benchmark claim; linked blog redirect unavailable through the web reader and benchmark not reproduced. | Attributes long-running task gains to managed context/memory. | Memory-helpfulness is a baseline, not a novelty claim. Include the budget-matched single-controller baseline and strong ordinary handoff practices. |
| [witcheer, structured workspace memory](https://x.com/witcheer/status/2034535160641716730), March 19, 2026 | Original post and visible reply discussion read. Practitioner setup report and prospective observations; not a completed success evaluation. | The author plans to watch whether end-of-session writes happen and whether accumulating entries degrade context quality. Replies discuss dynamic updates and bridging OpenClaw-oriented files into Hermes; a portability claim in one reply is partially truncated. | Separate checkpoint production, retrieval and application. Include interrupted sessions and contradictory archives. Test behavioral portability instead of inferring it from file portability. |
| [Bobby Hansen Jr., four-week agent report](https://x.com/bobbyhansenjr/status/2023246258438095287), February 15, 2026 | Search-indexed article read; original X page now says the account no longer exists. Historical, unverifiable anecdote at this access time; low weight. | Reports stale checkpoints after compaction and problems with indiscriminate memory collection. | Corroborating motivation only. Do not treat its numerical claims as benchmark evidence or as a current live thread. |

A separate primary engineering source supports the practical relevance: [Anthropic, Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), November 26, 2025. The article reports session discontinuity, unfinished undocumented work, premature completion and weak end-to-end verification. It uses progress records and incremental workflows, and explicitly leaves open the comparison between one general agent and specialized multi-agent arrangements. This is engineering evidence for a problem and useful baseline ideas; it does not establish that our cultural-continuity experiment is novel.

The earlier targeted review also checked the [Succession Study](https://successionstudy.org/) framing and [governed collaborative memory](https://arxiv.org/abs/2605.04264). Together these make broad claims about inventing institutional memory, succession or memory governance untenable.

## Search and exclusion record

Search batches covered (1) culture/files/inheritance and succession; (2) compaction, handoffs and institutional knowledge; (3) stale or contradictory memory; (4) emergent conventions and author discussions; (5) prominent-builder memory discussions. Existing lab thread records were searched for related work. Specific discovered URLs were checked directly rather than relying on platform search rankings alone.

Some web queries returned irrelevant Grok-share pages and automatic X trend summaries. Those were excluded. Product announcements about durable storage were screened as demand signals, not evidence that useful practices survive turnover. The Project Sid repost in the library adds no author analysis, so it was not counted as independent confirmation. No claims were attributed to Karpathy merely because another poster mentioned him. No complete-thread claim is made where only a root, selected replies or a cached article was read.

Search coverage is biased toward English, accessible/indexed posts and currently visible conversations. Threads can identify important failure modes and competing framings; they cannot establish absence of prior art, prevalence of a failure, or the best possible scenario selection.

## Revised priorities

### 1. The release crew: preserve what done means

Promote this over the harbor as the flagship. A planner, implementer and verifier learn a working review practice in a small synthetic repository. Over two full replacement waves, the code, tests and handoff records persist, but private member context does not. The task includes changes that pass superficial tests while violating a fixed user contract. One learned check remains useful; a different check becomes obsolete after a declared API change. The correct revised procedure is not supplied.

The core outcome is whether later crews deliver the required behavior, preserve valid checks, and retire obsolete ones without relaxing the contract. Freeze evaluator-only acceptance tests before acquisition. Actors can create or change their own tests, but cannot change the independent score. Measure unsupported completion claims, actual regressions, duplicated work and selective correction retention. A short attractive handoff is not automatically a successful handoff.

To retain a cultural rather than merely coding interpretation, measure a group-acquired, behaviorally observable practice over repeated tasks: for example, which evidence is required before accepting a peer's completion claim. Do not preload the desired norm. Compare a supplied best-practice checklist as an engineering ceiling, and a single controller as an explanatory baseline. If a fixed checklist explains all gains, report that result plainly.

### 2. The incident guild: remember the exception and retire the obsolete rule

Keep the night-watch mechanism, with a more explicit operational interpretation. Repeated crews handle routine service events and rare failures in a deterministic simulator. They learn a costly verification practice from experience. A long uneventful interval puts that practice at risk of deletion; a later environment change invalidates only one precaution. A surviving precaution still prevents a rare failure.

Measure risk-stratified loss, false alarms, useful-precaution retention and obsolete-precaution retirement. This tests over-retention as well as forgetting. It is not equivalent to the release crew: delayed rare feedback and the cost of prevention are central. The specific rare-hazard construction is our extrapolation from continuity/curation concerns, not something the X sources demonstrated or requested.

### 3. Model/runtime migration: a cross-cutting intervention, not a third story

Run the strongest qualified task under same-model fresh instances and a separately qualified model-family change. In a later engineering replication, change the runtime while holding model, files, tools and budgets constant. Never vary model and runtime together and call the effect cultural loss. Persisted bytes, successful retrieval, understood instructions and reproduced behavior are four different outcomes.

Use A-to-A, B-to-B, A-to-B and B-to-A controls where feasible. Include a reference-procedure competence control on both models, a no-inheritance prior baseline, and an exact archive transplant. Counterbalance labels and compare each receiving model to its own baseline. Matching budgets does not equate model capability. The Hughes thread motivates model dependence; it did not test this migration intervention. The workspace-memory discussion motivates runtime portability; it did not demonstrate behavioral invariance.

The harbor remains a compact coordination control or visualization-friendly extension. Glassmaking remains a later causal-transfer extension. Neither is discarded as uninteresting, but neither currently has stronger practical grounding than repeated software handoffs. There is no evidential reason to require exactly three separate task worlds.

## Concrete changes to the design

- Split the intervention into checkpoint creation, memory selection, and recipient application; log each separately.
- Compare graceful replacement with a prespecified interrupted checkpoint. If the archive was never written, classify that as checkpoint-production failure, not failed social learning.
- Match the artifact snapshot within causal comparisons. Keep generated code/tests/environment state as explicit inheritance channels, rather than claiming notes are the only memory while leaving solutions in a repository.
- Use controlled redundant, superseded and contradictory entries. Equalize total context ceilings; report actual bytes, retrieval access and calls. Label engineered corruption as a treatment, not spontaneous drift.
- Retain frozen archives, rolling archives, archive transplantation, retained members, no-inheritance and the single-controller baseline from the prior draft. Do not expand to the entire Cartesian product immediately.
- Freeze original acceptance criteria and evaluator tests independently from actor-maintained progress files. Measure actual behavior, not claims of completion or identity.
- Test descendant-to-descendant transmission, untouched task combinations, and a correction surviving the second turnover wave.
- Show a replay of an inherited claim, its evidence, the successor's action and the resulting outcome. Files surviving is not the visual success criterion.

## What would earn an interesting result

A useful result would quantify a failure boundary or tradeoff after strong controls: for example, copying an archive preserves a mistaken practice better than it preserves the evidence needed to correct it, or an update mechanism preserves the valid exception while retiring the obsolete rule after all original members have gone. These are prospective examples of discriminating findings, not predictions we have verified.

If ordinary structured handoffs match every richer condition, or a single controller matches the swarm, the study should say so and narrow its claim. If migration changes performance only because the receiving model lacks task competence, it is not a cultural-transmission finding. Before declaring novelty, compare the exact protocol with agent-memory, long-horizon coding, continual adaptation and cultural-evolution benchmarks through the full prior-art/review process.

No model run, new empirical result, paid allocation or simulated animation was created for this review. The immediate output is a better-grounded, narrower experimental choice.
