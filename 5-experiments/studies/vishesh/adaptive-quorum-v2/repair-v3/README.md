# Antsy: commit now, or wait for better evidence?

<!-- experiment-evidence:start -->
## Evidence metadata

Assessed 2026-10-04 by vishesh/codex-pi-review; source `9781739c` ([registry](../../../../evidence-metadata.json), [rubric](../../../../EVIDENCE-METADATA.md)). Scores describe evidence for the stated claim, not a probability of truth.

- **evidence_confidence:** **1/4** — Adaptive thresholds trade abstention against late correction or misinformation in the guarded factual selector. Basis: Every learned-policy choice matched symbolic control; guarded host logic limits AI claims. Twelve engineered clusters are the task diversity, not 2,688 independent outcomes. Rendering failure and exact-prefix recovery preserved.
- **sample_size_summary:** S1:12 task clusters × 2 populations × 2 deadlines × 4 worlds × 2 schedules =384 paired blocks;7 policies →2,688 outcomes. Q2:22/22 pass.
<!-- experiment-evidence:end -->

Antsy tests when a team should stop gathering evidence and choose an API under a deadline. Its visual story is a race between agreement, corroboration and newly arriving misinformation. This is a **synthetic engineering experiment**, not an accepted lab hypothesis or a production procurement benchmark.

## Current result

[Full assessment and post-mortem](reviews/S1-attempt-2-post.md): Q2 passed 22/22; the 384-block/2688-outcome sweep completed with zero actor/schema failures after a preserved rendering failure and exact-prefix recovery. Adaptive helped with late corrections and hurt with late misinformation. Every policy choice matched the symbolic baseline. The result supports this synthetic mechanism demonstration, not an AI advantage. [Counts](results/S1/summary.json) · [Integrity](results/S1/integrity.json) · [All outcomes](results/S1/outcomes.csv).

## Question

Does reducing a requirement from three supporting source roots to two at the final tick reduce costly abstention? When does it instead admit a bad choice? Is that policy better than simply using a constant two-root rule? These comparisons distinguish a useful stopping mechanism from an attractive animation.

## Setup

Five or nine scouts choose among three fictional invoice-extraction providers. Eligibility requires scanned-PDF support, zero-day retention, and at least 90% accuracy. Prices select among eligible providers; NONE means all three are observed to be ineligible. Missing provider coverage means WAIT. Accuracy in this version is a **supplied synthetic report value**, not a measured live API benchmark. No real invoices, provider calls or customer data are used.

Four source roots each issue three provider rows. Every population receives the same total evidence, divided into private deliveries and shared one tick later. Roots carry supplied ancestry; distinct roots need not be statistically independent or truthful. Copies share their original root. Later revisions supersede earlier visible values; this declared assumption is deliberately stressed by misleading late reports.

Agents use pinned local Laya for three yes/no fact predicates per provider. Host code intersects the model's eligible set with hard constraints on the observed typed facts, then chooses its cheapest member. **This is a guarded hybrid**, not repaired general reasoning. False source facts can still defeat it. All predicate decisions and guard blocks are retained. A symbolic comparator can solve the toy facts without a model; whether the model adds value is explicitly measured.

## Protocol

[Full specification](SPEC.md) · [Agent contract](agent-spec.json) · [Audit](AUDIT.md) · [Pre/post-run reviews](reviews/) · [Runbook](RUN.md).

The historical v2 pilot failed clean-task competence. D0 isolated a small-fact versus combined-decision gap. Q1 passed ordinary tasks but failed a one-day-retention boundary. Q2 tests the explicit safety guard on disjoint tasks. The stress sweep is blocked unless Q2 passes all 22 cases without invalid encodings. Preserve every failed attempt. This version does not pool results with v1/v2 or claim independent cross-researcher acceptance.

The completed S1 engineering matrix contains 12 task clusters, two populations, two deadlines, four evidence worlds and two arrival schedules: 384 paired blocks, 2,688 policy outcomes. Seven policies consume matched ballot histories: majority, fixed-two, fixed-three, adaptive, deadline vote, central deadline and symbolic deadline. The two centralized controls receive the union of evidence delivered by cutoff, an explicit aggregation advantage. S2 remains disabled.

## Metrics

All-assigned correct selection, hard-constraint violations, abstention, false NONE, loss and commitment tick. Loss is 0 for best eligible/NONE when appropriate, 1 for an ineligible choice or invalid execution, 0.5 for abstention or false NONE, and 0.25 for a more expensive eligible choice. These utilities are chosen assumptions; report component metrics so conclusions do not depend on the aggregate alone.

Record physical calls, actual encoded input tokens, inference time, logical predicate invocations, cache hits and guard disagreements separately. Per-policy logical cost uses only its consumed ballot prefix. Shared cached execution time is not an independently measured per-policy deployment cost. Twelve controlled task clusters do not justify broad confidence claims, and thousands of repeated votes are not thousands of independent observations.

## Visualization

[Live Antsy dashboard](https://swarm-live.pages.dev/#/x/adaptive-quorum-api-v2). Public PNG/GIF views show recorded source arrival, scout ballots, supporting roots and policy commitment times. A policy's result appears only once it commits. Evaluator correctness is explicitly labeled and never sent to actors. Static diagnostic matrices preserve failed cases. The layout is a diagram, not simulated ant movement; source timing uses logical ticks rather than seconds.

## Research basis and limits

The original biological motivation is [Pratt and Sumpter's ant study](https://pmc.ncbi.nlm.nih.gov/articles/PMC1635101/) ([[pratt-2006-tunable]]). Reopened results/methods in this review: search and acceptance rates, as well as quorum, affect the tradeoff. Antsy isolates a software stopping rule; it does not replicate the colony mechanism. [Debate or Vote](https://arxiv.org/html/2508.17536v1) motivates retaining simple voting controls, with conclusions limited to that paper's tested assumptions. [StableToolBench](https://arxiv.org/html/2403.07714v3) motivates frozen service behavior for reproducibility; Antsy does not run that benchmark. These are focused primary-source checks, not a completed novelty survey.

Connects to the original [quorum](../../project-briefs/quorum.md), [collective sensing](../../project-briefs/collective-sensing.md), [coordination](../../project-briefs/coordination.md), [diversity](../../project-briefs/diversity.md), [dissent](../../project-briefs/dissent.md) and [institutions](../../project-briefs/institutions.md) briefs. The useful next external-validity step is cited evidence from realistic API documentation, tested against a held-out gold set, with calibrated latency and source reliability. Jev through OpenRouter remains deferred until secure routing/credentials exist and fresh qualification passes.

## Measured visual results

[Conditional tradeoffs](https://swarm-live.pages.dev/api/a/adaptive-quorum-api-v2/repair-v3-S1-attempt-2/tradeoffs.png) · [Late correction replay](https://swarm-live.pages.dev/api/a/adaptive-quorum-api-v2/repair-v3-S1-attempt-2/replay-early-wrong-late.gif) · [Late misinformation replay](https://swarm-live.pages.dev/api/a/adaptive-quorum-api-v2/repair-v3-S1-attempt-2/replay-late-wrong-late.gif). All eight selected replays and their final frames load on the [completed run](https://swarm-live.pages.dev/#/r/adaptive-quorum-api-v2%2Frepair-v3-S1-attempt-2).

## Prospective design amendment 2026-10-04

Incorporating [Dmarz's quorum recommendation](https://github.com/dmarzzz/swarm-lab/blob/e0a31706cdf1fb1d3864370b04f29bd4f93e2682/researchers/dmarz/notes/next-experiments-2026-10-04/README.md), the next useful extension changes a stopping decision through new evidence timing or reliability, rather than repeating symbolically equivalent choices at more sizes. The completed S1 results and scoring remain frozen.

Before a successor, write a small set of independently authored scenarios where waiting can reveal a correction, introduce misinformation, or miss an operational deadline. Specify the source-reliability and delay process separately from agent inference, retain constant-two, constant-three and deadline controls, and compare correct decisions together with abstention and deadline loss. Use task-specific costs to justify the utility weights; show component outcomes so a preferred conclusion cannot depend only on those weights.

Retain the symbolic/full-information reference as an explicitly advantaged ceiling and a competent N=1 solver with the same evidence actually available by cutoff. Measure actual verification and inference costs; cached shared histories do not constitute independently measured policy deployment costs. Pair conditions within fresh task roots and distinguish a treatment-specific size interaction from a raw increase in population. Freeze total-information and resource regimes before evaluating a semantic task. These requirements define a prospective extension, not a claim that the current guarded fact-selection model adds value beyond its symbolic baseline.
