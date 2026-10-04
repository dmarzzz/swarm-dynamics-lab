# Immune Response

## TLDR

Can an explicit evidence-freshness receipt help an agent choose between investigating, restarting, changing configuration and leaving a healthy service alone? Compare raw versus freshness-annotated shared advice on six constructed operational cases. Both conditions see identical source records and timestamps; the treatment annotates those records without choosing an action or revealing hidden runtime state. Measure healthy service ticks, redundant mutations and delayed repair separately. This is a bounded mechanism diagnostic, not a production reliability estimate.

## Question and prediction

A3 completed reliably but did not demonstrate an immune-response benefit: all eight paired health differences were zero, and every healthy control redundantly redeployed. Two scenario names shared the same initial deployment; live complete information made checking largely redundant. A boolean transcription check did not change behavior.

A4 asks whether a **timestamp/epoch receipt** improves decisions when previous observations may no longer describe the running service. Predict fewer mutations under a stale false alarm and faster diagnosis of a crash concealed by stale healthy telemetry, without suppressing a justified same-version restart. Null or adverse differences end the corresponding efficacy claim; do not rerun an unchanged design to obtain a preferred result.

Operational motivation: Kubernetes distinguishes liveness-driven restart from readiness (https://kubernetes.io/docs/concepts/workloads/pods/probes/). Google SRE describes both the value of repeatable fixes and the hazards of assumptions embedded in automation (https://sre.google/sre-book/automation-at-google/). We borrow these distinctions, not their incident frequencies. The model is a deterministic teaching simulator, not Kubernetes or a fitted outage process.

## Setup

Use the same pinned Haiku 4.5 model, temperature0, JSON actions and original cumulative USD8 ledger. Two model reviewers (configuration compatibility and runtime diagnosis) each see the same declared observation, with different task emphasis; no claim that these are independent experts. Their two recommendations are generated once per world and shared across the paired controllers. No hidden case name, scoring label, reference action or operator conversation is given to agents.

Six worlds: healthy fresh telemetry; healthy service with stale failing telemetry; crashed worker with fresh failing liveness; crashed worker masked by stale healthy telemetry; persisted-schema transition requiring a compatible two-component sequence; inaccessible registry with a local-catalog repair. Configuration, process liveness, cached probes and customer health are distinct state variables. A same-version deployment restarts the process: useful if down, redundant if already live. We model no unmeasured restart outage or invented monetary penalty.

Each world has two receipt arms and four action ticks: 12 episodes, 12 shared-reviewer calls plus48 controller calls = **60 calls**. Six paired constructed worlds are the units; calls, reviewers and frames are not replications. A4 seed9401 controls presentation/arm order only. Precision supports per-case diagnostic differences, not confidence about a production incident population. A5, if admitted, uses seed9402 as a representation stress check; it is not an independent topology replication. Historic holdout9200–9215 remains untouched.

## Protocol

Before implementation, freeze this plan and the PI critique. Generate fixtures, baseline checks and semantic fault tests offline. Publish an immutable plan and verify its exact content hash before each native stage. Acquire a fresh exclusively claimed machine in the verified Dmarz setup; never use another researcher's workload. Restore the existing ledger, currently387 calls and USD3.179489 reserved, without resetting it.

At t0 the actor receives configuration, local compatibility catalog, persisted schema, cached service probe plus liveness values, observation epoch and current deployment epoch. All are explicit source data. A stale observation has an earlier epoch; its health may disagree with hidden runtime state. Only `inspect` refreshes the runtime probe. `deploy` changes one binary and restarts that component; every accepted deployment increments the epoch and leaves the cached probe unchanged. `wait` does nothing. Tool results do not return hidden health. `refresh` consults the registry and can fail; it is not an oracle repair recommendation. There are no unannounced later faults: freshness tracks interventions and the initial incident boundary.

Raw and checked conditions receive the same source records, reviewer text and generic instruction to weigh current evidence. Checked receipts label each probe/advice observation as current or stale by comparing its reported epoch with the current epoch. The checker has no world state, health function, preferred action or case label. It never blocks or rewrites an action. Current does not mean an advisor's recommendation is correct.

Reference controller uses only actor-visible records and catalog: inspect if stale, restart a visibly failed process, otherwise choose a minimum-change compatible bundle, or wait if already healthy. Validate that it can solve every case within four ticks. A deliberately stale-trusting controller must fail at least one masked incident or false alarm; otherwise the manipulation is too weak and native collection is blocked.

A4 is the single bounded diagnostic authorized for this portfolio cycle: **one60-call native attempt**, followed by its operational and scientific post-mortem. This supersedes the earlier two-attempt allowance in this document. Stop on transport/response/accounting failure; preserve all assigned/not-started outcomes and ambiguous reservations, with no automatic retries. If capability fails, analyze the cause and prepare a prospective remedy; do not auto-launch A5. If the contrast is null or at ceiling without additional decision value, end collection. A new attempt is a later decision, not a consequence of budget remaining.

## Metrics

Primary: paired checked-minus-raw healthy customer ticks per case (0–4), reported without pooling away mechanisms. Co-primary operational restraint: redundant live same-version deployments and any mutation on healthy negative controls. Report true repairs, configuration changes, inspections, epoch mismatches, reviewer epoch-report errors (free-text factual correctness is not scored), rejected actions, customer-health loss, final health, invalid/missing outcomes, calls, tokens, actual/reserved dollars and wall latency separately. No synthetic weighted score.

Execution gate:12/12 episodes,60/60 calls, complete valid JSON and durable usage. Capability gate per arm: both healthy cases4/4 healthy ticks with zero deployments; incidents final healthy, at least2/4 healthy ticks, no rejected destructive action and no loss of previously fully healthy service. A useful restart of a crashed process is not a redundant deployment. Passing capability does not establish treatment efficacy; all-zero paired differences are a null result for these cases.

## Visualization mapping

One timeline panel per case, raw/checked trajectories from initial state through four measured ticks. Plot customer health, every deployment (separate useful restart, configuration change and redundant restart), inspection and stale/current observation state. Show actual state separately from actor-visible cached evidence. Use a time slider and a five-frame animation; expose action, justification, source epoch and receipt at each step. Missing cells remain missing. Include a metric table so overlapping health curves do not conceal redundant actions, as A3's plot did. Recompute visuals from saved events; record renderer/source/input hashes. No renderer influences the agent or scorer.


## Portfolio reconciliation — current cycle

A3 supersedes the older portfolio status:16/16 episodes and120 calls completed, all incident gates passed, all four healthy controls redundantly restarted the current version, and all eight paired health differences were zero. A3 supports a narrow null and an abstention failure; it does not establish peer-interaction benefit. A4 holds the advisory architecture fixed and tests metadata annotation, **not whether a team beats a solo agent**. The latter would require solo, compute-matched solo and evidence-matched team controls and remains deferred.

Empirically unknown: whether explicit freshness annotation changes information acquisition when the cached state and actual service differ. Support would justify a separately reviewed broader provenance test; null would favor raw metadata for these cases; harm or capability failure would stop escalation; incomplete calls would be an execution result, not a scientific contrast. Existing A3 traces cannot answer this because actual runtime liveness and stale cached observations were not separate state variables. The visible-reference solver establishes feasibility but cannot predict native use of the annotation.

The six fixed worlds provide failure-discovery scope, no population precision estimate. No assertion about unseen topologies, memory persistence, emergent immunity or collective advantage is supported. Expected operator effort for preparation and review is45–90 minutes; native requests roughly3–8 minutes plus rendering/transport, conditional on provider latency; these are planning estimates, not measured labor. Maximum additional API reservation remainsUSD1.14432; an already running dedicated allocation avoids new cloud provisioning but does not imply zero allocated infrastructure cost.

## Pre-dispatch trace amendment

Current Dmarz native-run review distinguishes valid but unproductive actions, explicit provider refusal and transport failure. A4 will retain the exact credential-free provider request body and an allowlisted response body (`id`, `model`, `stop_reason`, `usage`, `content`) before parsing the action. Join both to the durable request ID and request hash. Headers, keys, workspace routing, operator-session transcripts and arbitrary HTTP error bodies are excluded. Parsed decisions, simulator tool results and scored frames remain in the event journal. Retain these experimental traces locally for scientific closeout; this is not authorization to publish an operator transcript or a raw provider dump. This logging repair changes no prompt, scenario, arm, metric, model, call cap or stopping rule.

## Approved bounded continuation A5 — prospective

Following the A4 closeout, the owner approved completing this bounded comparison on2026-10-04. A5 is one new attempt, at most60 calls, with the same six paired worlds, seed9401, pinned model, prompts, arms, four ticks, metrics and thresholds. It is not the earlier proposed seed9402 representation stress check. A4 remains an immutable failed attempt with no native outcomes. No added scenario difficulty is justified by a transport error.

Use the tested safe HTTP diagnostics added after A4, preserve every request/output and inspect each qualification miss. No retry or provider/model fallback. A favorable contrast supports only these six cases; a null/adverse contrast is retained; incomplete transport remains scientifically inconclusive. No automatic A6. Restore the after-A4 ledger:388 calls,USD3.185495 reserved ofUSD8, including the uncertain A4 reservation. Additional conservative maximumUSD1.14432, leavingUSD3.670185 before any incremental infrastructure. Reuse an eligible exclusively claimed existing researcher machine; no new cloud resource is proposed.

Admission remains conditional on credible current direct-provider readiness, actual exclusive approved-account allocation, remote offline checks, immutable public registration/hash and single-writer ledger verification. Another study's OpenRouter success is not direct-Anthropic evidence. Coordinate with already authorized provider diagnostics instead of making redundant probes. The first real advisory response is part of the60-call cohort, not an uncounted health check; any transport/schema/usage failure stops the attempt. Native capability is still unestablished: all cases are bounded qualification evidence before broader expansion. Report six constructed paired units, never60 independent samples. Render native timelines/animation only when actual state trajectories exist.
