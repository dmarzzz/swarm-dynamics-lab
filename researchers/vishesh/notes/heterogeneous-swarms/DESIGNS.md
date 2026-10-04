# Five shortlisted experimental designs

**Status: prospective design sketches, not preregistrations, accepted hypotheses or runnable configurations.** No experimental implementation or model call was started. Each sketch needs a completed prior-art survey, independent review and a fully specified protocol. Before each actual run, publish and verify an immutable public plan URL, register its condition-specific TLDR and enforce the public-plan preflight. Keep execution outcomes separate from process compliance. A retrospective plan never repairs a missing preregistration.

## Shared integration and evaluation contract

Use a provider-neutral adapter with separate `propose(state)`, `choose(state, options)`, `verify(state, action)` and `observe(event)` interfaces. Jev supplies typed decisions; Haiku/Qwen can supply proposals, explanations and plans. Ordinary code owns legal actions, durable state, resource ledgers and execution. Every proposal carries a state version, option IDs, source IDs, author model revision and expiry; a validation failure is recorded rather than silently repaired. Treat a planner-plus-selector as a composite agent unless separate state/identity is intentional.

Pin exact served model IDs/revisions, Qwen size/quantization, reasoning settings, sampling parameters, prompts, adapters and task-generator hashes before launch. Provider aliases are not immutable identifiers. Estimate capability on a separate development set. Preserve failed qualifications and adapter diagnostics. Neither API-schema validity nor vendor calibration substitutes for local semantic tests. Record provider response model metadata; if immutable revision identity is unavailable, disclose that replication limitation and freeze the available snapshot metadata.

Primary unit: an independent task world or task graph, **not agents, messages or decisions inside one world**. Block by task family and difficulty; pair initial state, exogenous disturbances and evidence across arms, then randomize scheduling order. Pilot planning target: 12 independent development worlds per family for feasibility/variance only. A later confirmatory sample size must be computed from a declared minimum effect and pilot variance before held-out testing; the pilot itself cannot justify significance. Do not use an arbitrary small swarm count as statistical power.

Maintain separate caps for dollars, wall time, tool calls and communication/storage. Exact matched compute is unavailable across proprietary models: use dollar-and-deadline comparisons plus a fixed-call sensitivity analysis, and report realized resources including profiling, compilation, retries and judges. Freeze the price snapshot. Include a strong single agent, same-model repeated samples, independent ensemble, same-model role-diverse team, deterministic coordination and the relevant closest published method. Stage the study to avoid an unaffordable full factorial: isolate one mechanism first, then test transfer to a second task family.

Choose one primary contrast and endpoint per study. Estimate paired world-level differences with confidence intervals clustered by world; repeat seeds do not create independent task families. For multiple confirmatory contrasts use a prespecified familywise adjustment such as Holm. Report assigned denominators, timeout/budget failures, missing outcomes and adverse results. Protect evaluator truth and objective scoring outside agent write access. Stop only for fixed allocation or declared operational limits. A null result is not a reason to retune on the test set.

No infrastructure or paid-compute budget is authorized by these sketches. Actual model qualification and runs need the owner's dedicated-machine allocation workflow and an explicit experiment budget. Public artifacts contain synthetic state and non-secret metadata only; authorized local processes consume credentials without returning them in traces.

## HX-02 — Adaptive division of labor after a capability shock (92/100)

**Question.** Can a Jev allocator reassign Haiku/Qwen workers after a capability change faster and more economically than fixed specialization or a simple progress-based rule?

**Task.** A synthetic incident-repair graph has extraction, dependency diagnosis, plan construction and executable validation stages. Each stage has an objective success condition. Halfway through a paired episode, withdraw one tool or change one worker's error distribution. Fix disturbance time and severity before seeing outcomes. A same-model team with differentiated tools distinguishes role diversity from model diversity.

**Arms.** A: fixed roles chosen on development data. B: Jev reassignment from observed progress. C: deterministic response-threshold/progress assignment. D: a MasRouter-style learned allocation comparator, only if faithfully implementable with training costs charged. An oracle allocator is a separately labeled ceiling. A common task queue and equal permissible observations prevent the dynamic arm from seeing hidden failure labels.

**Primary contrast/metric.** B minus C in objectively verified task completion during a fixed post-shock window, with equal initial capacity and budgets. Secondary measures: adaptation delay, role-switch count, total cost, dependency starvation and pre-shock throughput. Compare honest, delayed and misleading progress signals as a follow-up rather than initially changing everything.

**Mechanism and prior-art boundary.** Adaptive specialization is established in robotics; role/model routing is established in MAS. Our target is allocation under stale or unreliable language-agent progress reports. [[emam-2020-adaptive]] [[yue-2025-masrouter]]

**Kill/decision rule.** If the simple allocator matches B within the prespecified useful-effect margin, adopt it. Reject a general heterogeneity claim if same-model capability partitioning supplies the same gain.

**Visualization mapping.** Agent color identifies model, shape identifies capability, links identify task dependencies. Plot queue length and verified throughput over time; mark the shock and each reassignment. Do not animate claimed progress as completed work. Retain task IDs, assignment versions, decision time and objective validation events.

**Condition TLDRs.** A tests frozen roles as comparator; B tests typed reassignment; C tests an inexpensive biological-threshold-inspired rule; D tests an established learned router. All ask whether adaptation restores verified throughput after the same shock. Limits: synthetic tasks, model-specific competence and potentially noisy progress estimates.

## HX-01 — Reflexes and deliberation (91/100)

**Question.** When does a fast Jev controller acting on a slower Haiku/Qwen plan become harmful, and can a state-validity contract prevent that?

**Task.** A changing service-routing world alternates load and available routes. A planner proposes a permitted action set; the fast controller chooses among it while the environment changes. The evaluator checks capacity and route validity. Inject known observation and planner delays independently of model identity, and log actual service times separately.

**Arms.** A: fixed-rate typed controller with no plan expiry. B: same controller with state-version and expiry checks plus bounded fallback. C: synchronous planner/controller. D: flat adaptive deterministic controller with the same total state budget. Add a homogeneous generative controller in a later transfer stage. Tune deterministic gains on development worlds; a weak memoryless baseline is insufficient.

**Primary contrast/metric.** B minus A in verified feasible actions by deadline at one frozen delay regime. A broader delay-by-refresh-rate phase diagram is exploratory. Secondary measures include overshoot, route flipping, settling time, stale actions, fallback frequency, cost and lost service while waiting.

**Mechanism and prior-art boundary.** Multirate control and latency limits are established. The causal-depth code demonstrates how memory can confound hierarchy comparisons and explicitly labels its LLM outputs as mocks. Our narrower question is semantic validity of typed actions against changing generated plans. [[li-2026-deadline]] [[gh-kuznetsovkarazin-causal-depth-limits]]

**Kill/decision rule.** If deterministic control is equally effective, use it. If a benefit disappears at equal total memory and action opportunities, do not attribute it to model heterogeneity. A replay-only result is scheduling evidence, not proof about model behavior.

**Visualization mapping.** Use aligned lanes for true state, observed state, planner version and controller action. Show staleness as packet age, not model color. Plot constraint violations and recovery alongside motion. Preserve event time, logical version and missing observations.

**Condition TLDRs.** A measures uncontrolled fast/slow staleness; B tests version/expiry protection; C is synchronized comparison; D tests whether ordinary control and memory suffice. Metrics are feasible actions, instability and total resources. Limits: task-specific delay range and unknown generality beyond the tested models.

## HX-03 — Diversity as a firebreak (90/100)

**Question.** Does a different-model sentinel reduce cascades because its mistakes are different, rather than because it sees better evidence or costs more?

**Task.** In a bounded synthetic dependency network, one erroneous report can cause downstream invalid task commitments. Truth and source ancestry are known to the evaluator. Agents can flag, recheck or abstain; there are no real external harmful actions.

**Arms.** Cross homogeneous versus Jev/LLM monitoring with independent versus copied upstream observations. Hold specialist count and topology fixed first; randomize placements in paired worlds. Compare equally budgeted no-monitor extra-solving and deterministic invariant checks. Bridge-placement is a later factor. Development data estimate detector sensitivity and specificity; report unmatched competence rather than pretending it was controlled away.

**Primary contrast/metric.** Difference-in-differences in false final commitments: mixed minus homogeneous monitors, comparing independent and shared evidence. This tests whether shared evidence erases the putative diversity benefit. Secondary metrics: ancestry-linked cascade size, conditional co-failure, false quarantine, correct rare evidence retained and total review cost.

**Mechanism and prior-art boundary.** Minority defense is prior art, including Cowpox; team complementarity is prior art. The experimental delta is separating error covariance, evidence ancestry and detector competence at the typed/generative boundary. [[wu-2025-cowpox]] [[teng-2026-which]]

**Kill/decision rule.** Reject model-family labels as a proxy for independence if common-source errors dominate. Prefer better provenance or invariant checks if they match protection without destroying useful minority knowledge. Propagation fitting is descriptive unless intervention randomization identifies a causal path.

**Visualization mapping.** Graph nodes show model family; edges show observed transmissions; claim color shows ancestry. Correct and false claims have separate evaluator-only overlays. Replay suppression and false positives as well as successful containment.

**Condition TLDRs.** Homogeneous and mixed arms compare monitor identity; independent and copied-evidence arms test common-source dependence; exact checks and extra-solving are cost controls. Outcome is false commitments plus retained useful work. Limits: synthetic error mechanisms and no assumed vendor independence.

## HX-05 — Diverse reserves for recovery (88/100)

**Question.** Does keeping a small reserve of different capabilities/models improve recovery enough to justify idle capacity?

**Task.** Reuse the incident task graph with partial worker-local memory. Predeclare family-correlated and independent failure schedules. A reserve can only recover state from surviving permitted records. Include clean worlds to measure the opportunity cost of not using those workers earlier.

**Arms.** A: all workers active, no reserve. B: homogeneous cold reserve. C: mixed-model cold reserve. D: equal-cost warm spares. E: deterministic fallback on supported subtasks. Keep total budget, model-loading charges, state storage and qualified capability explicit. A failed family should remove the same initial task capacity across paired designs.

**Primary contrast/metric.** C minus B in the area under the post-outage service-deficit curve; lower is better. Secondary metrics: time to restore capability coverage, deadline success, clean-world throughput, cold-start cost and wrong actions after restored memories. Failure to recover is censored/unrecovered at the deadline, not zero recovery time.

**Mechanism and prior-art boundary.** Functional redundancy and adaptive allocation are known, and team regrowth/Theseus work overlaps substantially. The narrower test is whether model-family response diversity survives correlated outages after paying the reserve's real opportunity cost. [[emam-2020-adaptive]] [[teng-2026-which]]

**Kill/decision rule.** Reject a resilience claim if faster recovery merely reflects less initial damage or simpler duties. Merge with existing recovery work if no additional mechanism remains after full-methods review.

**Visualization mapping.** Display capability coverage separately from live identity count. Shade failed family dependencies, show reserve activation and replay objective service restoration. An animated node reappearing is not recovery until its task output validates.

**Condition TLDRs.** A measures capacity without insurance; B tests same-model redundancy; C tests response diversity; D tests warm versus cold startup; E checks exact fallback. Compare service deficit and clean-world opportunity cost under identical failure schedules. Limits: selected outage model and bounded task coverage.

## HX-09 — Verification queues and the cost of saying no (85/100)

**Question.** Can cheap parallel proposals overwhelm a shared Jev verification layer, and which admission policy preserves verified throughput?

**Task.** Haiku/Qwen workers propose bounded actions on a shared synthetic work queue. The verifier accepts, rejects or requests revision. Endogenous retries can create load beyond external task arrivals. Inject a controlled false-rejection rate in replay to isolate queue feedback, then measure actual model behavior separately.

**Arms.** A: first-in-first-out verification and unrestricted bounded retries. B: backpressure with a reserved verification budget. C: priority based on observable task risk/age. D: deterministic invariant-only verification where applicable. Cross one versus several verifier instances at the same total resource cap; sharing a provider may correlate tail latency.

**Primary contrast/metric.** B minus A in verified tasks completed by deadline at a frozen near-capacity arrival regime. Secondary metrics: p95 waiting time, rework amplification, starvation, false acceptance, false rejection and total cost. Safety constraints remain explicit; merely refusing everything is not successful automation.

**Mechanism and prior-art boundary.** Queue stability and deadline scheduling are established, including agentic AI-RAN work. The narrower mechanism is rejection-induced feedback in a heterogeneous proposal/verification loop, with model error and workload coupled. [[li-2026-deadline]] [[gh-shapor-jev-sentinel]]

**Kill/decision rule.** If fixed admission limits eliminate the problem, prefer them. Reject gains achieved by skipping review, hiding dropped work or moving completion past the deadline. Do not claim an M/M/1 formula applies unless its assumptions are checked; service and arrivals may be dependent and heavy-tailed.

**Visualization mapping.** Animate arrivals, pending checks, accepted work and returned proposals; align queue occupancy with verified throughput. Distinguish fresh tasks from repeat attempts and show the resource ledger depleting.

**Condition TLDRs.** A exposes baseline overload; B tests backpressure/reserve; C tests priority; D tests whether exact checks suffice. Metrics are verified throughput, waiting time and error/cost tradeoffs. Limits: bounded retries, synthetic workload and measured provider latency distribution.
