# New hunch: acknowledgment is not correction

2026-10-04 · prospective idea, not an accepted hypothesis or launch plan. Source: [[data-ai-village-2026]]. This is a candidate within the shared dataset preparation lane, not another funded experiment.

## TLDR

After agents say a problem is fixed, do their next relevant memories and actions support that closure? Compare an acknowledgment-only closure rule with one requiring fresh, task-relevant evidence from each affected role. Measure premature closure and useful closure delay on complete correction episodes. The Village's potentially linked chat, memory and action traces make this promising, but exposure and ground truth are not yet established.

## Question and prediction

An incident may be verbally acknowledged while stale state survives in another agent's memory or action. The candidate prediction is that action-backed closure reduces false closure relative to verbal acknowledgment at a cost in latency and evidence requests. The decision is whether a workflow should require demonstrated state updates before marking multi-agent corrections complete.

This differs from Theseus's handoff-recovery endpoint and the Memory brief's within-agent recurrence: the unit is a correction incident affecting several roles, and the endpoint is justified system-level closure. It overlaps both; if available data cannot support the cross-agent part, merge the annotation dimension into Telephone/Memory instead of creating a nominally new study.

## Setup

First perform an offline feasibility audit of eight development incident components: four candidate corrections, two accurate/no-change controls and two unresolved-evidence controls, conditional on source verification. Identify affected roles from pre-correction dependencies, not hindsight about who later fails. Require verifiable original state, correction evidence, actual or explicitly constructed exposure, subsequent memory where available, and a relevant action opportunity. Missing observation is censored/unknown, not proof of persistent error or successful closure.

Freeze a 48-hour recorded-time follow-up window for the descriptive audit before deeper outcome reading. Record wall-clock downtime, weekends and whether any relevant opportunity occurred; report opportunity-indexed outcomes alongside elapsed time. Do not interpret variable historical model/tool/goal regimes as treatment effects. Connected incidents sharing goals, artifacts or claim ancestry stay in one split.

## Protocol

Stage A, future offline annotation: compare acknowledgment-only, fixed waiting-window and evidence-backed retrospective closure classifiers against adjudicated receipt/action labels. Equalize their available archive at each time; the evidence-backed rule may abstain but cannot use future facts. Scoring truth may come from later follow-up, clearly separated from each classifier's information. Separate false early closure, correct delayed closure and still unresolved. This is a prediction/measurement comparison, not a causal intervention on historical agents.

Stage B, only if Stage A shows value: a prospective controlled task reconstruction with an explicit action-dependent sandbox, acknowledgment-only versus receipt-backed closure, and matched total verification effort. Include a central state register/simple controller baseline. Historical playback cannot supply other agents' counterfactual responses. The sandbox, model, tokenizer, request envelope, actual task count and cumulative cost are unresolved; no model stage is launch-ready.

## Metrics

Primary descriptive endpoint: false-closure fraction among all eligible incidents, with both classifier coverage and conditional error reported. Secondary: delay to correct closure, stale-memory/action recurrence, unnecessary verification and proportion censored. Never improve apparent safety by marking everything unresolved: require a declared coverage/delay comparison against the simple controller. Eight development incidents cannot estimate rare-event reliability. A possible 24-component sealed pilot would have roughly ±20 percentage-point uncertainty for a single rate near one half, before dependence; actual paired precision depends on discordance.

Stop/park if critical exposure or actions cannot be verified, if the simple register already solves the useful decision, or if apparent gains are only lower coverage. Favorable evidence motivates a separately costed bounded intervention; null/adverse evidence ends the standalone idea; incomplete evidence supports no efficacy claim. No automatic retry or favorable-result search.

## Feasibility, prior art and resources

The distinct affordance is crossing chat, compressed memory and observable action in long-running work. It is an inference from the documented schema and parsed structural prefixes, not a finding that complete incident chains have been recovered. LongMemEval already tests knowledge updates; LLM-Culture studies transmission; Docent supports auditable trace analysis. A focused survey of distributed incident closure, belief revision and multi-agent common knowledge is still needed before a novelty claim.

Offline annotation needs no allocated cloud machine or model spend; allow roughly half a day of operator preparation to establish feasibility, an estimate not measured work. A native successor needs a concrete owner scope decision, existing/default cumulative authority as applicable, data-transfer permission, qualification, public registration and exclusive approved-account allocation. No budget is created by naming this hunch.

Visualization, if pursued: private incident timeline showing correction delivery, acknowledgment, next memory and next relevant action, including missingness. Public report uses aggregate closure-delay/coverage tables without source text. No renderer or empirical result exists yet.

**evidence_confidence:** 0/4 for the closure-rule prediction; vishesh/codex-village-fit, 2026-10-04. **sample_size_summary:** 0 adjudicated incidents, 0 outcomes, 0 model calls; proposed eight development components not collected. Setup: [shared preparation record](SETUP.md).
