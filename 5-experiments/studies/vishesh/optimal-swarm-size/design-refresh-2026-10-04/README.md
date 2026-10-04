# When should an agent team shrink?

2026-10-04. Exploratory question/design revision, not an accepted hypothesis, registered run, or execution approval. [Current setup](../SETUP.md), [latest scientific result](../reviews/q-a6-post.md), [Q-A7 operational hold](../reviews/q-a7-route-assessment.md), [search and evidence register](SOURCES.md). The frozen Q-A7 diagnostic is unchanged. No new model calls, machine allocation or budget is implied.

## Decision and proposed question

The broad question “which team size works best for which task?” is useful but crowded. Task-dependent scaling, dynamic spawning, correlated teams and shared-state concurrency already have close prior art. We should not sell that question as a new scaling law. [[kim-2025-towards]] [[costa-2026-agentspawn]] [[bertalanic-2026-ringelmann]] [[lyu-2026-coagent]]

**Recommended candidate:** Under a fixed total resource envelope, when a workflow moves from parallel investigation into coupled state-changing work, does reducing the active team improve verified completion compared with keeping the team large and improving synchronization? Can an observable conflict signal identify when contraction is useful on unseen cases?

This asks whether headcount reduction adds value beyond a good scheduler and concurrency control. It is a candidate contribution, not a verified novelty claim. The potentially distinctive element is the controlled interaction among workflow phase, state change and team contraction, including cases where contraction loses. Generic spawning, autoscaling, stale-state detection and hysteresis are not new inventions.

A result favoring a simple single controller or fixed synchronized team is useful: implement that and end the adaptive-team line. If contraction helps only an intentionally broken baseline, reject the research claim. If gains persist under the strongest control and transfer to held-out workflows, propose a larger policy study. Mixed or imprecise results justify no universal recommendation.

## Candidate directions and judgment scores

Scores are PI judgments, 1–5, not evidence confidence or probabilities. Novelty means relative promise after this bounded search; none has passed an exhaustive prior-art review.

| Candidate | Novelty promise | Practical value | Measurability | Visual potential | Main objection |
|---|---:|---:|---:|---:|---|
| Generic optimal N by task and budget | 2 | 5 | 4 | 4 | Strong overlap with existing scaling studies |
| Contraction versus better synchronization at a workflow transition | 4 | 5 | 4 | 5 | CoAgent and adaptive orchestration are close; strongest controls essential |
| Add a worker or spend the same allowance refreshing stale evidence? | 4 | 5 | 4 | 5 | Must match evidence access and account for refresh cost; alternative next study |
| Does prior team history change the best current size? | 4 | 4 | 2 | 5 | History, memory and phase effects easily confounded; defer |
| Hardware/context pressure predicts useful agent count | 2 | 5 | 4 | 4 | Primarily systems benchmarking; requires measurable local inference |

Recommendation: develop the contraction comparison first, use evidence-refresh as a later orthogonal contrast, and treat history dependence as exploratory until the basic instrument works.

## Operational definitions

| Term | Definition to freeze |
|---|---|
| Task/solution pair | A versioned environment and terminal success contract paired with one fixed model, toolset, prompts, memory policy, coordinator and integration procedure. A model or protocol change is a new cohort. |
| Agent | One separately addressable persistent model context. Count the coordinator and any model-based verifier/selector. Deterministic tooling is a controller, not a free hidden agent. |
| Team size N(t) | Number of live contexts eligible for new work at time t, including the coordinator. Also report distinct contexts ever created, actual used contexts, in-flight model calls, tool calls and peak concurrency separately. |
| Contraction | Stop assigning to retiring workers; let admitted calls finish, charge them, transfer their bounded records, then retire contexts. No mid-call cancellation savings or context disappearance is assumed. Report drain and handoff time. |
| Independent root | A separately constructed world/problem and causal structure. Arm variants, renamed entities, changed numbers, repeated seeds and model resamples are not new independent problems. Shared repository/template/source worlds form clusters. |
| Full success Y | Required environment predicates hold by deadline, all safety/consistency invariants hold, no duplicate forbidden action, and aggregate resource limits are met. Y is binary. Evaluator checks hidden tests/state, not persuasive final prose. |
| Quality Q | Prespecified fraction of required predicates satisfied, reported alongside full success and invariants. A critical invariant violation cannot be washed out by averaging easy subgoals. |
| Resource envelope r | Total model input/output and reasoning usage where returned, calls, dollars, elapsed deadline, tool capacity, context limits and measured hardware. All agents, coordination, retries, refreshes and selection count. Equal ceilings do not imply equal realized consumption. |
| Static useful size | Smallest tested N with success probability within a proposed 5 percentage points of the best feasible tested N, under the frozen task distribution and envelope. This is a decision tolerance, not precision available in a small pilot. Report an uncertain set when unresolved. |
| Dynamic useful policy | A mapping from permitted observations/history to bounded roster changes. Compare complete policies, including their decisions, warm-up, handoffs and drain cost; no timeless single N is inferred. |
| Coordination cost | Prespecified tokens/calls and elapsed intervals for delegation, messages, integration, conflict recovery and handoff. Keep overlapping durations separate; never sum concurrent service time and label it wall time. |
| Stale observation | A read whose relevant object version has changed before the dependent action. Version mismatch alone is not a semantic error; distinguish harmless changes, rejected attempts and committed invalid effects. |
| State-change exposure | Count/rate of relevant exogenous updates and actual inter-agent writes. Exogenous updates are randomized treatments; endogenous conflict rates are outcomes/mediators, not exogenous explanatory variables. |
| Practical advantage | Primary: higher probability of verified on-time completion. Secondary: lower total cost or completion time at equivalent quality. No post-hoc conversion of a fast wrong answer into success. |

For a static policy, p_N(x,r)=P(Y=1 given task stratum x, envelope r, fixed protocol). The target is the smallest tested N within epsilon of max p_N, not the luckiest observed run. Estimate selection on development data and evaluate the frozen selection on unseen worlds. A finite grid cannot establish a global optimum. For dynamic policies replace N by the entire policy pi; report actual N(t).

A finite pilot should **not** certify a five-point non-inferiority margin. The first screen is feasibility and effect-size estimation. A later non-inferiority study must size its independent sample for the margin before observing its outcomes.

## Realistic task shortlist

These are candidate contracts, not built environments or claims that benchmark tasks have already been acquired. Prefer source-backed operational structure with a small executable sandbox over another arithmetic puzzle with a realistic story.

| Priority and task | Observable tools and changing world | Verifiable success / challenge | Independent cases and major risk |
|---|---|---|---|
| 1. Service incident response | Inspect logs/metrics/configs, trace dependencies, propose/apply reversible remediation. A rollout, failover or dependency health update changes relevant state. | Restore service-level checks without regressing a dependent service or violating change constraints. Parallel diagnosis may help; conflicting remediations may hurt. | Distinct service graphs and root causes, not copies of one outage. ITBench is a source of realistic structures; begin with a lightweight emulator, later validate in containers. Emulator validity is an explicit limitation. |
| 2. Multi-service API migration | Search and edit actual small repositories; run unit/integration tests; API contract or shared schema updates arrive during work. | All hidden cross-service tests pass on committed output; no consumer of a missing or outdated symbol. | Distinct projects/change requests and dependency graphs, clustered by repository. Select tractable development cases, then freeze unseen projects. Full SWE-bench Pro can be too difficult/costly for this budget. |
| 3. Disrupted delivery/field-service scheduling | Read routes, appointment windows and inventory; reserve/release slots; traffic or cancellations update availability. | Feasible complete schedule with deadline and capacity constraints, no duplicate booking or stranded dependency. | Separate network/demand patterns and disruption mechanisms. Compare an optimization solver given the same explicit data; if it wins, the LLM contribution may be only translating messy requests. |
| 4. Customer support with overlapping orders | Retrieve customer/order/policy records, reserve stock, amend/refund in a simulator; shared inventory changes. | Correct permitted resolution, no duplicate refund or over-allocation. | Distinct policy/transaction structures; strong deterministic transaction baseline. Avoid making the answer a hidden policy exception. |
| 5. Reconcile changing operational reports | Query structured records and documents, track timestamps/provenance, update a report after corrected source data. | Required totals, provenance and current-version claims verified by scripts. | Distinct schemas and discrepancy mechanisms. Pure joins/arithmetic may be solved entirely by SQL; retain that baseline. |
| 6. Travel disruption replanning | Search a frozen itinerary service; hold/release simulated bookings as cancellations arrive. | Complete feasible itinerary under constraints; no real purchases or messages. | Different route graphs and constraints. No live web prices; distinguish simulated practicality from deployment evidence. |
| 7. Multi-document launch package | Update release notes, migration guide and example configs after a contract change. | Executable examples and cross-document version invariants all consistent. | Different product contracts; prose aesthetics remain secondary and separately judged. |
| 8. Warehouse replenishment | Inspect stock/backorders and routes, reserve transport, handle delayed shipments. | Fulfilled priority demand with valid inventory accounting and bounded lateness. | Distinct network/failure structures. Operations-research solver is a required comparator. |

See [twelve concrete candidate development worlds](CASES.md), including their checks and simple competitors. Start with incident response and API migration; retain scheduling as the first transfer family. Source inspirations: [[jha-2025-itbench]], [SWE-bench Pro](https://scaleapi.github.io/SWE-bench_Pro-os/) and [Gaia2](https://arxiv.org/html/2602.11964v1). These are sources of evaluation patterns, not interchangeable validated fixtures for this study.

Each root's scenario record must specify hidden world, actor-visible initial information, legal tools, independently implemented checker, exogenous event schedule, intended competing explanations and source/template cluster. Changes should vary causal dependencies, not just names. Actors see ordinary updated observations, never the evaluator's label, winning policy or future event tape.

## Baseline ladder

| Arm | Contract | What it rules out |
|---|---|---|
| S: one capable tool-using agent | Same model, complete permitted evidence access, scratchpad, scripts/calculator/tests and parallel non-model tool calls up to the common tool limit. | A weak N1 artificially creates swarm benefit. |
| I: independent attempts plus selection | Multiple independent candidates, shared total allowance; selection uses available public validation, all selector calls charged. Hidden tests never choose the winner. | Improvements are just more samples. For mutating tasks, each candidate has a reset sandbox; selection precedes final application. |
| F: fixed coordinated team | N=4 total including coordinator; same shared-state tool semantics and synchronization safeguards as contraction. | The primary paired comparator for roster policy. |
| D: deterministic scheduling control | Fixed team with explicit dependency/ownership scheduling and safe writes; no model chooses team size. | A conventional scheduler captures the benefit. Do not give it evaluator-only dependencies. |
| C: contraction policy | Start at N=4; drain to N=1 after a prespecified observable trigger. Same models, roles, tools, validation and message contract as F. | Candidate treatment. Both arms get the same checkpoint/status packet so only roster eligibility changes. |
| R: resource allocation control | Retain N=4 but spend the corresponding available allowance on checking/refresh rather than extra work. | The benefit comes from verification budget, not contraction; second-stage discriminator if C looks useful. |

Always include S, F and D before claiming C is useful. I is essential before claiming coordination beats independent search. R can follow a positive pilot, but until included do not claim contraction is better than every use of the saved budget. A stronger single-model baseline is a separately cost-matched practical comparator, not a clean count-only treatment.

For initial C, use a deterministic trigger over observed conflict/revalidation events rather than another model call: two rejected stale-version writes among the last four attempted writes, with no re-expansion within the episode. This is a **candidate development setting**, not a universal threshold or launch-ready default. An explicit phase-boundary contraction is a second diagnostic control. Calibrate on development cases; freeze before qualification. On never-coupled cases C should usually avoid unnecessary contraction; on late/no signal it may lose. That is a testable failure, not a reason to rewrite the trigger after seeing held-out data.

Normal consistency checks apply to every arm. Do not remove safety from F to manufacture a contraction advantage. Strict serializable tooling may eliminate any advantage; report that. A complete CoAgent implementation would be a stronger later baseline; a simple versioned-write check must not be mislabeled a CoAgent reproduction.

## Controlled contrast and data collection

First identify a minimum competent task family. Both S and a clean F run must show useful task understanding on disjoint development cases; a small screen does not prove general reliability. Scripted legal solutions must pass all checks. Wrong/stale/duplicate actions, plausible incorrect outputs and future-information leakage must be rejected offline. Include a negative control with independent read-only subtasks and a positive contention fixture with a known conflicting schedule. Neither scripted reference is model evidence.

For each root create a stable variant and a phase-changing variant with the same goals, amount of useful evidence and allowed operations wherever possible. Use an exogenous event tape anchored to simulation time, identical across arms, not to a particular agent's progress or evaluator verdict. Record whether each arm actually encountered the transition. A pilot-calibrated fixed event time avoids making the treatment wait for a losing arm. Include never-coupled and always-coupled development fixtures to check that the result is not merely a globally easier variant.

Primary causal contrast: the root-paired difference in C minus F success on phase-changing worlds. Secondary interaction: (C−F on changing worlds) − (C−F on stable worlds). Compare C with D and S before judging decision value. Randomize arm order within blocked root/variant runs; reset the world each time. Shared-provider load remains a nuisance: randomize across time blocks and report service queueing. Do not run treatment arms concurrently against a shared mutable world or let one arm's output leak to another.

Record full model requests/visible outputs, tool arguments/results, object versions, action accept/reject reasons, world-change times, scheduling decisions, N(t), blocked intervals, drain/handoff cost, raw usage, reservations and final checker results. Classify error paths: wrong diagnosis, stale but harmless read, rejected stale action, semantic conflict, duplicate work, integration omission and operational failure. Do not infer an agent's internal reasoning from an output.

Primary denominator is every admitted assigned episode; operational failures and unstarted episodes are explicit separate counts. Do not silently replace provider failures, treat them as cognitive errors, or drop them to improve the treatment effect. Report all-assigned operational completion and a clearly labeled conditional scientific analysis only if its missingness assumptions are defensible. Stop on first transport/accounting fault; retain unknown charges. Independent task timeouts are outcomes, not reasons for replacement.

## Independent cases, sample size and holdouts

Proposed offline case bank: 36 distinct root contracts, 12 per candidate family (incident, migration, scheduling). Per family allocate four development, four qualification and four sealed transfer cases, with entire source repositories/template mechanisms confined to one split. These counts are a preparation target, not an adequacy claim. Scheduling is held out from policy tuning: its development subset is for offline checker/tool validation only, not model behavior or policy-threshold selection. If only a few underlying templates are available, report that smaller cluster count and narrow generalization; changing seeds does not fix it.

First paid screen, **only if later approved and priced**: eight qualification roots from the first two families × two variants × four arms (S,F,D,C) =64 episodes; one sample per cell. This is eight root blocks, not64 independent observations. I is then needed before a coordination-over-independent-search claim; R before a verification-budget claim. Every pilot root becomes development evidence afterward. Do not use its favorable roots as a confirmation set.

For a later precision study, sample new roots and cluster at source/template level, keeping family strata explicit. For a paired binary success difference, approximate variance is (q−delta²)/n, where q is the discordant-pair rate and n is the number of independent root pairs. With q=.30 and delta near0, a95% interval half-width .10 needs about116 independent pairs; the conservative q=1 bound is about385. Eight roots plainly cannot establish a five-point margin. These are planning approximations, not powered-study promises; use pilot variability, cluster dependence and multiplicity to choose the actual next sample before running it. Repeated model samples estimate within-root variability, not more independent worlds.

Predeclare a minimally useful pilot signal as a10-percentage-point observed success improvement of C over F, no deterioration against D in the aggregate and acceptable actual cost; treat it only as a go/no-go development heuristic with uncertainty. A final efficacy claim requires a prespecified confidence criterion and adequate sample. If all capable baselines are at floor or ceiling, report that and redesign on development cases rather than replace scored holdouts.

## Physical interpretation and visualization

The useful physical analogy is competition between the time to exploit parallel work and the time for that work's premises to change. Candidate explanatory ratio chi=lambda_relevant × L, with relevant update rate lambda and median read-to-action lag L. It is dimensionless but not a universal law: dependence, relevance and nonstationarity can invalidate simple models. Work/span and queueing give comparison bounds; they do not predict LLM correctness by themselves. Use measured quantities and keep any unavailable hardware quantity marked unknown. API client RAM is not provider VRAM.

For a biological analogy, flexible workforce recruitment/withdrawal is an inspiration, not evidence that LLM teams reproduce insect behavior. No biological scaling claim is proposed without a separate primary-literature treatment.

Animate a service graph or repository dependency graph from actual trace events: investigation branches spread, changed objects pulse, stale plans acquire version markers, conflicts queue, and retired workers drain into a single integration lane. Compare fixed and contracting teams on the same wall-clock axis with success, spend and deadline visible. Add a static event table and reduced motion. A phase map shows observed case counts and uncertainty; never draw a smooth boundary from eight cases. The visual is useful precisely when a larger, busier team loses.

## Scope, costs and next concrete work

This revision does not modify or launch Q-A7. Q-A7 tests operand binding in a synthetic arithmetic family; a positive result would not qualify incident response or repository editing. Its diagnostic value should be considered separately rather than making it a mandatory ladder into this new question. Keep prior negative results intact.

Original remaining exposure headroom at the last verified ledger is USD17.968680 of the original USD20. The64-episode screen is unpriced and may not fit. At a hypothetical fully charged mean of USD0.20/episode it costs USD12.80 before qualification, infrastructure and contingencies; this illustration is not an enforceable bound. Obtain measured calibration and worst-case reservations before selecting a paid stage. Do not spend residual funds merely because they exist.

Concrete offline next work: author12 development contracts, prototype one incident emulator and one tiny multi-service repository, implement independent hidden-state/test checkers, demonstrate scripted failures and solutions, and finalize the S/F/D/C observation and tool interfaces. Estimated preparation effort is2–4 focused workdays plus case review, not a20-minute prompt tweak; compute requirements start with local CPU containers, with no cloud allocation yet. Then freeze the model, exact caps/deadline, cases, policy threshold, uncertainty plan and source, and present a priced bounded proposal. No automatic run, model switch, new machine or successor follows from this document.
