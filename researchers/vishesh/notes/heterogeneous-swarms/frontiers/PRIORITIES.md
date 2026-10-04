# What to work on after owner feedback

2026-10-04 UTC · vishesh/codex-heterogeneous · research prioritization only

**Work on HX-31: self-differentiating swarms, starting from an initially uniform network.** The concrete objective is to discover which capabilities should remain distributed, which should become shared services, and which can be replaced by cheaper execution as experience accumulates. Test whether those changes preserve quality and can be reversed when conditions change.

The owner endorsed capability shedding and shared data providers, rejected the practicality of the organelle framing, found workspace inheritance useful but less exciting, questioned the practical case for speciation, and interpreted the fifth idea as workflow hardening. The numerical revisions are assistant judgments responding to that feedback; the owner did not assign numbers.

| Previous conversational item | Record | Old → revised | Current choice |
|---|---|---:|---|
| 1 — Black Queen / specialization | HX-31 | 93 → **94** | Main project; uniform start, differentiation as an outcome |
| 2 — Agent organelles | HX-32 | 92 → **34** | Drop from active work; ordinary modularity currently explains the practical problem |
| 3 — Ecological inheritance | HX-33 | 92 → **82** | Supporting workspace-hardening and portability study |
| 4 — Cultural speciation | HX-35 | 91 → **60** | Park until a convincing deployment scenario exists |
| 5 — Cognitive food webs | HX-37 | 90 → **66** | Consolidate into HX-31; no separate project |

Same rubric weights, with lower theory and practical scores where the analogy outran the engineering case. The consolidated HX-37 score measures residual standalone appeal; it does not discount the value of workflow hardening inside HX-31. The prior food-web question concerned concurrent salvage of failed work. The owner's temporal hardening interpretation is broader and now takes precedence in the active direction. [Dimension-level scores](SCORES.md) and [the full before/after record](priority-revision.json) preserve the distinction.

## The first concrete study

Use repeated, independently verifiable analysis jobs with overlapping data needs. Initially each agent uses the same model, tools, skills and data permissions. They all pay their own data-fetching, parsing and context costs. No agent starts as a specialist or server.

Allow the adaptive condition to discover repeated work, establish shared data providers, unload redundant skills, select cheaper models and change communication edges. Count the cost of discovering and implementing those changes. All variants must meet the same freshness and answer-quality requirements; cheaper but stale or incomplete answers are failures.

Compare four architectures:

1. Frozen generalists, preserving the initial uniform configuration.
2. Generalists with a straightforward shared cache/service, isolating ordinary deduplication.
3. A fixed specialist configuration optimized on development workloads.
4. An adaptive swarm that chooses and revises its own allocation.

The central result is a quality-constrained lifetime cost comparison, with duplicate API calls, context traffic and latency as diagnostic measures. A topology replay should show the actual transition from uniform agents to data providers and cheaper consumers; no emergent role should be declared solely from a prompt or label.

Then change the workload or remove a provider. Measure whether the adaptive swarm restores capabilities, adds redundancy or upgrades a model without losing its accumulated savings. This tests whether simplification remains useful under change. A single stable workload can show compression; it cannot establish adaptive organization.

## How the rest of the bank fits

| HX record | Use in the recommended project |
|---|---|
| HX-37 — workflow hardening | Across-time simplification: expensive discovery becomes a validated procedure, smaller-model execution or deterministic code. Add after shared-service differentiation is interpretable. |
| HX-33 — workspace hardening | Supporting ablation: how much capability comes from the model versus tools, schemas, tests and cached information? Does it transfer to another cheap model? |
| HX-02 — adaptive division of labor | Recovery phase: reallocation after workload changes or loss of a provider. |
| HX-01 — fast/slow coordination | Control for stale shared state and mismatched action/update timing. |
| HX-17 — selector outage | Reliability check so a new shared decision service does not silently become a single point of failure. |
| HX-28 — deterministic replacements | Mandatory engineering baseline; exact code may replace some reasoning steps entirely. |

These are related measurements within one program, not six independent projects to launch. Original bank scores still put HX-02 at 92 and HX-01 at 91. HX-03 and HX-38 remain 90. Their high historical scores do not make them better starting points than the newly clarified HX-31; the recommendation accounts for the owner's explicit interest, overlap and what one coherent study can establish.

HX-34, HX-36 and HX-38 retain their earlier reserve scores because this exchange reviewed the five presented ideas. They are not silently promoted into a replacement top-five list. Future reassessment can challenge those original biological scores too.

## What would change the recommendation

If a simple cache or fixed specialist architecture captures the savings, use that engineering result and narrow the research claim. If adaptive differentiation only wins because its optimizer gets hidden workload information or uncharged inference, the comparison is invalid. If savings vanish after a realistic workload shift, the system learned a brittle specialization.

No novelty claim follows from the new score. Caching, routing, workflow reuse and specialization remain close prior art. The research target is their automatic discovery, combination and revision under equal information and honest lifetime costs. The existing survey, review and public-plan prerequisites remain in place; this score revision launches nothing.
