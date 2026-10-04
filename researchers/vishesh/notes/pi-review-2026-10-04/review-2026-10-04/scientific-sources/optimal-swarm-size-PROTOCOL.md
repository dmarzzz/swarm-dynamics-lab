# Swarm-size protocol refinement

Author: vishesh/codex-idea-scores. 2026-10-04 UTC.

**Exploratory design addendum, not an approved protocol or a preregistration.** Read with [the design](README.md). These are proposed conventions to review before implementation. No fixtures, models or experiments were run to produce this document.

## A comparison an operator could actually use

The unit is a task root under a fixed resource profile and solution method. The operator supplies a deadline, aggregate spending cap, allowed tools and measured hardware constraints, then receives a roster recommendation. A recommendation must pay for feature extraction, admission and startup before doing useful work. Its clock starts when the request arrives, not after the recommendation is ready.

The headline comparison is the conditional rule against the development-selected fixed size. Compare assigned requests, including refusals and failed launches. Refusal can be a sensible operational action but scores zero on verified delivery; report its rate and avoided spending separately. A policy that refuses most tasks cannot appear better solely by dropping them from the denominator.

## One coordination protocol across the roster grid

The following proposed centralized protocol makes the solution method reviewable. It is not a claim that this architecture is best.

1. **Admission:** start the clock, extract only permitted input features, choose N, and check initialization and completion reserves. Return a recorded refusal when the request cannot fit. Roster size is fixed thereafter; unused contexts are allowed and reported.
2. **Planning:** context 0 receives the task, tool descriptions, budgets and submission contract. It emits a bounded JSON work plan with work-item IDs, prerequisites and output contracts. All sizes use the same schema and planning prompt apart from the explicit roster description. Malformed plans consume their actual usage; at most one charged repair request is permitted, then fail the episode.
3. **Dispatch:** a deterministic scheduler validates the plan for cycles and unknown prerequisites, then assigns ready items in stable ID order to idle contexts. Context 0 can execute work when it is not planning or integrating. At N=1 it executes all items serially. At N>1 the same context may work alongside N−1 workers. The scheduler performs no reasoning or hidden task decomposition.
4. **Work:** one actor turn may return a tool request, a work-item artifact, or a blocked/failure report. Its stateful context stays attached to that actor. Tool results return only to the requesting actor unless explicitly written to the shared ledger. Work-item completion releases declared dependants, even if its substantive answer is wrong; only the final evaluator knows correctness.
5. **Shared ledger:** append-only entries contain item ID, actor, source/tool-result references and an explicit artifact. Actors retrieve entries through the same charged interface. No automatic broadcast of everyone's full history. Retrieving source material remains available to N=1. Ledger content included in a model prompt consumes tokens. Infrastructure storage and tool costs are separately metered where applicable.
6. **Integration:** when all items finish or the reserved integration boundary arrives, context 0 receives an index of completed, failed and missing work. It retrieves what it needs and produces one final artifact within its reserve. There is no evaluator feedback or hidden-test retry. Optional public tests are allowed only if all sizes have them and their use is charged.
7. **Termination:** freeze the final artifact on submission or deadline. Cancel pending work at the hard stop; account for unavoidable in-flight charges. Retain incomplete artifacts as diagnostics, never score a post-deadline answer as on-time success.

Per-turn output ceiling, tool limits, work-item limit, ledger retrieval limit, initialization requirements, integration time/token reserve and context truncation policy must be pinned from development-only qualification. The machine-readable draft keeps these values unset. A run cannot silently choose defaults for them. The same profile uses the same aggregate reserve across N; increasing N must not increase the cap.

No worker-to-worker private channel in the core. Adding debate, voting, specialist prompts or dynamic spawning changes the solution method. M2 removes durable shared storage but specifies an explicit charged relay through context 0; it is a separate protocol variant, not a RAM experiment.

## Resource accounting without races

Keep a single atomic ledger per episode and one shared stage budget. Before dispatching each billable call, reserve its known input charge, maximum possible output charge and any bounded tool charge. Concurrent callers cannot each see the same unspent balance. Reconcile reservations against actual usage; retain a reservation until cancellation or billing is settled. Stop admitting calls when a remaining worst-case charge would cross either cap.

If the provider cannot bound a billable operation, the protocol cannot promise a hard dollar cap for that operation. Use a conservative documented bound or disallow it; report settlement overrun explicitly. Tool-wall-time and model-wall-time share the episode deadline. Actor concurrency is capped by runnable slots, while tool concurrency is separately pinned. Queueing counts toward latency. An OOM after admission is a measured failure, not an excluded observation.

Count separately: logical contexts allocated, contexts used, active requests, total requests, actor tokens, selector tokens, evaluator tokens, actor cost and evaluation cost. Evaluation is excluded from the operator's actor budget but included in the study's spending ceiling. No evaluator messages enter the actor system. Retries keep their original episode ID, charges and clock; failed attempts cannot be replaced by an uncharged fresh episode.

## Training, freezing and genuine policy evaluation

Qualification roots are disjoint from core roots. Within each of the four core family/structure cells, split the eight roots into four fit roots and four validation roots, with all profiles, sizes, samples and descendants of a root staying together. This is a deliberately small exploratory split. Use fit roots for the response model; validation roots select one predeclared complexity setting and the best fixed N. Freeze the feature extractor, tie rule, admission check and selector before transfer. Do not refit on validation outcomes afterward for this version.

The transfer family has eight independent roots per structure. Its sweep estimates the response surface: 1 family × 2 structures × 4 profiles × 5 sizes × 8 roots × 2 samples = 640 episodes. These are evaluator-side mapping observations. They are not deployable policy trials.

**Add four separately executed policy arms:** always N=1; development-selected fixed N; capacity heuristic; conditional selector. Each arm runs 1 × 2 × 4 × 8 × 2 = 128 episodes, or **512 additional episodes**. Every arm receives the same paired roots and resource profiles, with independent actor samples and randomized execution order. Start timing before its selection/admission step. Do not reconstruct policy success by selecting the corresponding N from the response sweep, subtracting an estimated cost afterward, or reusing a trajectory generated with a larger remaining budget.

Freeze all policies before any transfer results are accessible. Keep the transfer sweep sealed while policy execution is in progress. The sweep can inform the evaluator's uncertain best-tested reference after unsealing, never the tested selector. Use independent roots or cross-fitting for selected-frontier estimates; with only eight roots per structure, report uncertainty rather than an exact oracle. The primary directly randomized policy comparison does not require naming that oracle.

Revised planned maximum: 80 qualification + 1,280 core map + 640 transfer map + 512 transfer policy trials = **2,512 episodes**. Adding the optional 1,280-episode resource extension gives **3,792**. This increase is an accounting correction to a draft, not spending authorization. If it is unaffordable, reduce the scientific scope before registration; do not omit the overhead test while retaining a deployability claim.

## Mechanisms that would explain a size change

These are diagnostic expectations derived from the proposed design, not established findings or new registered hypotheses.

| Candidate mechanism | Measure without circular prediction | Pattern to look for | What would weaken the explanation |
| --- | --- | --- | --- |
| Serial bottleneck | Recorded dependency path, actor service intervals, coordinator integration time. | Larger rosters stop improving latency when ready work is scarce or integration dominates. | The plateau occurs with abundant ready work and little coordinator time. |
| Queueing/contention | Request arrival, start and finish; slot occupancy; queue duration; tool service intervals. | Increasing N raises waiting time after available service capacity is saturated. | Gains disappear without rising waits; accuracy or redundant reasoning may dominate. |
| Finite-group information | Unique source IDs versus repeated claims; error overlap on paired roots. | More contexts spend more while adding little independent useful evidence. | Extra contexts consistently add distinct correct evidence and improve delivery within caps. |

For an illustrative deterministic task graph with known node service costs, total work W and longest dependency path L imply a lower bound max(W/c, L) on completion under c identical slots, before additional orchestration costs. This is a scheduling bound, not a fitted LLM law: model calls have variable service times and can change the amount of work performed. Use it only where its assumptions hold. Evaluator-known graph structure may explain outcomes; it is forbidden as a selector input unless the operator actually supplies it.

This gives the physical connection concrete meaning: finite processing capacity, dependency constraints, waiting and contention. The biological connection remains a comparison to finite-group information aggregation, not evidence that agents behave like a particular organism. A focused prior-art methods review is still outstanding.

## Visual demonstration: same task, three sizes

The proposed main view shows N=1, N=4 and N=16 solving the same root under one selected resource profile. Nodes are work items positioned by the declared dependency graph; actors are labeled markers moving only on recorded assignment or handoff events. Horizontal progress is elapsed time. A coordinator lane makes synthesis overhead visible. Queue lanes show requests that exist but cannot yet run. This avoids presenting every allocated actor as continuously productive.

Use two explicit replay modes: **wall-clock comparison** starts all three recordings at t=0 and holds completed lanes in place; **step inspection** pauses on an event and displays actor, evidence references, charges and task dependencies. A resource strip shows deadline, aggregate budget, reserved/in-flight cost, actual settled cost and memory only where measured. A red deadline line makes otherwise-correct late completion visible. Accessibility includes a static event table and reduced motion.

A profile switch selects another recorded episode; it must not imply a live rerun or interpolate unmeasured outcomes. The size map includes sample counts, intervals, infeasibility and uncertainty. “Suggested size” comes only from the frozen pre-launch rule; the evaluator's hindsight frontier is labeled separately.

Before outcomes are revealed, select the showcase root by a fixed hash order within the transfer-family manifest. Provide a browsable list of all eligible roots, including failed and missing traces. The default scene must not be chosen for a dramatic larger-is-better result. For a hand-built visual storyboard, label every frame “illustrative — no measured results.” No storyboard is empirical evidence.

## Review packet before implementation

A reviewer should be able to trace four hand-worked cases: a fully serial chain, independent equal-cost items, an integration-heavy task, and a cap too small for the proposed roster. For each, list legal ready work, slot admission, reservations, completion eligibility and final score. Include simultaneous budget reservations, cancelled in-flight billing, a late correct answer, an incorrect early answer, selector refusal and missing telemetry. These are planned fixtures, not checks claimed to have passed.

The next decision is to review this protocol and the exact task correctness contracts, then resolve the pinned runtime and qualification quote. Public-plan registration, independent review, machine allocation and stage spending gates from the parent document still apply. No launch is authorized by this addendum.

