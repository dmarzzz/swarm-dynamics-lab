# Poietic Agents prospective protocol

Version 0.1, 2026-10-04 UTC. Owner: vishesh; author/operator: vishesh/codex-heterogeneous. Status: exploratory design for review. Written before experimental implementation. S0 and S1 are bounded qualification/development stages under the [worker runbook](../../../../templates/experiment-worker/README.md); S2 is closed. This document is not a claim of preregistered confirmation or independent approval.

## Research target and competing explanations

The target system starts with interchangeable generalist agents and accumulates an increasingly differentiated, revisable division of labor. The unit that changes is an agent's configuration and its service relationships, never foundation-model weights. A smaller loaded skill inventory, fewer tool schemas, a provider service and an actual cheaper-model call are distinct operations, with distinct measurements.

The competing explanations are ordinary caching, good initial architecture, centralized optimization, simple routing, and amortized workflow construction. The experiment must make each explanation competitive. A visually interesting topology alone is not a research result. Closest-prior exclusions and remaining review work are in [PRIOR-ART.md](PRIOR-ART.md).

## Workload and answerability

Use synthetic operations jobs over three read-only APIs: inventory, supplier terms and delivery status. Each endpoint returns records with `entity_id`, `schema_version`, `source_version`, `valid_from_epoch`, `expires_after_epoch` and provenance. Values change according to an exogenous tape, independent of call count and treatment. A request at an epoch returns that epoch's version even if another arm makes a different number of calls.

Jobs request an eligible replenishment choice, a stock exception list or a delivery reconciliation. Required quantities, tie-breaking and output fields are public. The exact answer is computed independently from private fixture truth. A job can require a join, normalization or aggregation; it must not be solvable from an identifier or prompt pattern. Integer arithmetic avoids unexplained floating-point tolerances. Some questions legitimately have no eligible option, represented by a valid `none_eligible` answer rather than an execution failure.

A returned answer must include decision fields and source receipts. Success means correct required fields, valid derivation receipts, the requested snapshot/freshness, and delivery within the deadline. Old data that happen to give the right answer still fail the freshness requirement. Extra prose cannot substitute for a missing field. Staleness, wrong answer, malformed response, unavailable evidence, deadline failure and infrastructure failure remain separate diagnostics.

The deterministic reference solver is an evaluator/upper bound. It is not a hidden answer service for agents. A2/A6 get documented generic joins and arithmetic tools, but not the reference solver or a fixture-keyed answer table. This deliberately bounded environment tests allocation and reuse, not broad scientific discovery. A real API/repository transfer would be a separately designed successor.

## Uniform initialization

All A3 agents start with the same requested and observed model identity, system policy, four skill bundles (retrieve, normalize, join/aggregate, validate/format), three endpoint tools, peer messaging, a public service directory and empty private memory. Each has the same permissions, limits and visible cost schedule. No provider exists at time zero. There are no role names or preselected skill masks. Neutral agent IDs and assignment order are permuted per root.

The initial network is fully addressable; an edge denotes permission to request a peer service, not compulsory all-to-all chatter. A0 and A1 may communicate under the same message limits. Jobs are assigned by an exogenous balanced permutation, not by a scheduler that secretly chooses the most suitable specialist. Agents may forward a job through the same charged interface; the originating assignment remains in the denominator.

Agents retain memory within one lineage. Every independent root and every arm gets a fresh namespace and private cache; no mutable store crosses arms. Exogenous workload tapes are shared read-only. A5 is an explicit copy of a treated parent and is never counted as an independent root.

## Differentiation mechanism

At each epoch boundary, each A3 agent may submit at most one typed proposal, using its current model and the same capped observation packet: its own trace, delivered peer messages, service advertisements, observed tool failures, metered costs and public source-version notices. The observer does not expose other agents' hidden histories, future jobs, change timing, evaluator labels or rewards from held-out scoring.

Allowed operations are:

1. Load/unload a skill bundle or tool interface for that agent.
2. Register, revise or stop a provider service with typed input/output, freshness policy and capacity.
3. Add/remove a service connection or forward a job to an advertised provider.
4. Switch that agent's executor among qualified model/typed-policy choices, including escalation.
5. Install, disable or repair a validated deterministic procedure assembled from a fixed safe operator grammar.
6. Restore a previously removed capability or add a second provider using an existing agent identity.

No extra agent identities, unbounded self-replication, arbitrary network access or unmetered background reasoning are allowed. Data-serving operations may become deterministic; an agent need not call an LLM merely to return cached bytes. Record those as zero-model operations with actual compute and communication usage.

A deterministic transaction controller checks schemas, ownership, permissions, resource ceilings and service interface compatibility. It does not choose a specialist or maximize a hidden task score. Conflicting proposals are processed in a seeded rotating order. One accepted configuration version becomes effective at the next boundary; failed transactions leave the prior version intact. Charge accepted and rejected proposals. A5's controller rejects structural mutation while retaining its ordinary runtime policy.

Capability removal removes the actual tool schema/skill content from subsequent inputs and denies direct invocation at the adapter. Reload restores it through the charged configuration interface. Record memory/context migration, prompt sizes and a new definition hash. Changing a model label without making the new backend execute is an invalid manipulation.

Before a procedure is installed, the instrument checks type safety and sandbox limits. The agent may test it on up to two previously observed jobs using their saved permitted observations, with a shared validation budget. Those tests cannot read fresh labels. Checks establish contract compliance, not correctness on future cases. All arms get the same permitted validation primitives. Repeated test-set tuning is logged as development, not fresh qualification.

The objective shown to actors is to satisfy the incoming requests accurately, freshly and on time while minimizing charged resources. The policy does not mention biological theories, provider counts, heterogeneity, the expected winner or hidden shocks. There is no reward for shedding capabilities or creating an aesthetically interesting graph.

## Arms and baseline fairness

| Arm | Configuration and adaptation | Baseline protection |
| --- | --- | --- |
| A0 | Uniform generalists; structural mutations disabled | Same memory capacity, tools, communication and aggregate ceilings; may use saved private results |
| A1 | A0 plus a conventional shared cache with request coalescing, TTL/version invalidation and per-entity keys | Same data bytes, version notices and service capacity accounting; cache lookup can bypass an LLM |
| A2 | Static providers, consumers, tool subsets, deterministic procedures and model routing selected on development roots | Uses the same grammar/model menu; tune before evaluation and charge construction/probes; runtime cache invalidation and declared fallback rules continue |
| A3 | Local agent proposals under the mechanism above | All coordination, discovery, tests and migration charged |
| A4 | Central optimizer with the same union of legally shareable past observations and action grammar | Same total proposal/token budget as A3; cost the optimizer and observation collection; no future information |
| A5 | A3 configuration frozen immediately before a shift | Shares and is charged the full acquisition prefix for a hypothetical deployment; physical bill counts that prefix once |
| A6 | Single capable solver with tools, cache and self-checks | Same total resource/time ceiling as a swarm; unused resources need not be burned |

A0 is a diagnostic, not the strongest claim-making comparator. Select a comparator from A1/A2/A4/A6 on development roots using a frozen rule: among systems meeting the quality/deadline requirements, choose the one with lowest mean total cost per assigned job, breaking ties by the fixed order A1, A2, A4, A6. Freeze its settings and identity before S2. If none qualifies, no confirmatory comparative-efficiency claim is available. Keep all baseline results visible.

The initial S1 runs A0–A3 only. It is an instrument/feasibility study, so cannot claim superiority over A4/A6 or state-of-the-art methods. Add an AgentSlimming-style prune/replace baseline and a MANTA-style trace-repair baseline to the development comparison before claiming a novel optimizer; distinguish adaptations from faithful reproductions. Prior-art review may replace or consolidate this baseline menu before S2.

Secondary mechanism ablations disable only (a) model downgrades, (b) service sharing, or (c) workflow hardening within A3. Preserve their proposal and total budget limits; unused budget is reported. They are deferred from the first pilot and never added selectively after seeing a favorable result.

## Workload changes and causal scope

S1 has eight epochs, six jobs per epoch and six agents. Epochs 1–2 are acquisition; 3–4 are stable measurement; the intervention begins at epoch 5 and continues through epoch 8. Roots 200 and 201 change requested-key overlap from 80% to 20%; roots 202 and 203 introduce a schema revision with public documentation available through the same tool to every arm. Overlap means the share of required endpoint/entity/snapshot keys shared by two or more jobs in an epoch; the realized proportion is logged. Schema revision changes field nesting and units while preserving a documented conversion and answerable jobs.

Later cells separate stable-high overlap, stable-low overlap, high-to-low overlap, schema revision, and provider loss. Do not combine shocks in the primary test. A prospective larger horizon is 36 epochs × 12 jobs, with the change at epoch 19, acquisition epochs 1–6, stable epochs 7–18 and post-change epochs 19–36. This horizon is a review target, not a fixed S2 registration; S1 must establish that construction can plausibly amortize within it.

For provider loss, distinguish two interventions. An exogenously selected actor slot fails in each arm, with its paired slot fixed before configuration adaptation; this supports an architecture comparison. Separately, withdraw A3's most-used provider, defined from pre-change service receipts, and apply the same withdrawal to its A5 copy; this measures dependence on a learned provider. Do not compare targeted removal in A3 with random removal in another arm and call that a fair resilience test. Restore the withdrawn provider after a prespecified interval in a separate removal/rescue diagnostic.

Post-change recovery can mean tool reload, procedure repair, model escalation, service rewiring or more redundancy. It must be observed in configuration and successful execution, not inferred from a role label. A fixed A2 fallback that recovers is a legitimate strong result. Only A3 versus matched A5 isolates the value of continued structural adaptation conditional on a learned history.

## Units and scheduling

One independently generated workload root and its persistent lineage is the replication cluster. Jobs, epochs, model calls and agents within it are dependent. The same root is paired across arms. Distinct seeds on a common workload template are nested repetitions, not independent task families. Primary inference resamples whole root families with all arms, epochs, repeats and fork children intact.

Use separate named random streams for workload generation, job assignment, proposal arbitration, injected failures and policy sampling. Derive each from `(study, split, root, replicate, stream)` using a stable hash. A provider seed, if supported, is a recorded sampling parameter, not a promise of deterministic outputs across prompts.

For S1, each job permits at most four model turns and twelve tool operations, 8,192 input tokens and 1,024 output tokens per model request, a 45-second request timeout and a 120-second job deadline from release, including queuing. Proposals use the same per-request token caps and have their own metered boundary slots. Any S0 evidence requiring different limits triggers an amendment before S1.

A barrier scheduler freezes exogenous source state per epoch and applies accepted structural changes only between epochs. Within an epoch, process jobs in the paired seeded order, with at most two concurrent native calls in S1. Record queuing and service wait time. Exogenous source tapes prevent fast arms from receiving different facts solely because they run earlier in wall time. Counterbalance arm order within provider/time blocks; no cross-arm prompt cache with mutable content. Actual provider caching discounts remain in the ledger.

## Endpoints and cost accounting

Let `J` be every assigned job, `s_j` indicate correct, fresh, on-time completion, and `C` be total deployment cost. Primary cost is `C / |J|`, evaluated jointly with `Q = sum(s_j)/|J|`. Secondary cost per verified success is `C / sum(s_j)`; if there are no successes it is infinity, never zero or missing. Deadline misses, unstarted jobs after budget exhaustion and invalid outputs contribute zero to `s_j`.

Deployment cost includes initialization, model calls, proposal reasoning, tests, provider operation, context transfer, compilation, migration, ordinary compute and failed/retried requests. Baseline construction/tuning costs have the same ledger treatment. Report a cold-deployment total and a separately labeled amortization curve over the same fixed horizons. Do not assume a warm start for Poietic and charge baseline development in full, or the converse. Human engineering minutes are recorded separately without inventing a dollar conversion.

Maintain three distinct ledgers: actual invoiced API/infrastructure spend; physical resource counters (tokens, CPU/GPU seconds, endpoint calls, bytes); and optional synthetic toll sensitivity. Fixture APIs carry no real vendor toll. A simulated price for duplicated fetches can explain a conditional economic tradeoff, but cannot support a claim about realized dollar savings. Publish break-even API-toll and workload-horizon curves, including zero-toll cases.

Common evaluator/reporting overhead is itemized separately from deployable-system cost and included in the total experiment budget. Any validator available to an actor is deployable-system cost. Local model usage is not free: include allocated serving time and hardware cost, with the allocation rule frozen before use. Missing provider usage metadata reserves the worst permitted amount and marks cost uncertainty; never silently substitute zero.

Secondary diagnostics: duplicate fresh-key fetches divided by all successful fetches; stale outputs divided by all assigned jobs; input/output tokens; communication bytes; wall and logical latency; failures by class; loaded skill/tool count; actual execution share per model; provider utilization and concentration; number/cost of proposals and migrations; break-even epoch; and post-change cumulative lost successes. Publish raw counts with every ratio.

For provider concentration use the sum of squared service-request shares, with `not_applicable` when there are no service requests. Model heterogeneity and tool-mask diversity are descriptive; they are not utility endpoints. Report recovery as the first two consecutive post-change epochs meeting the registered quality/deadline requirements, censored as `not_recovered` at the horizon. Short-epoch proportions are diagnostics, not confident estimates of deployment reliability.

## Stages and decision rules

**S0 qualification:** 48 disjoint probes for each of three candidate contracts: generalist task/tool interpretation, cheaper generative interpretation, and Jev finite-choice selection. Maximum 144 logical model requests; one transport retry permits at most 288 physical requests. Each candidate is evaluated on its own contract; Jev is not compared on free-form generation. A reduced two-model ladder requires an explicit pre-launch amendment. Candidate versions and fixtures must be frozen before opening that qualification namespace.

For each contract require at least 44/48 correct responses, 48/48 schema-valid outputs, and zero protected-access violations. These are engineering screens, not proof of 95% reliability. Failure triggers a recorded diagnostic/repair and a new disjoint qualification set. Publish original failures and cap repair spend within the same authorized allowance. Proposed S0 ceilings are $5 model API, $2 infrastructure and two hours; current authorized allowance is zero pending a Poietic-specific allocation/authorization record.

**S1 development:** four independent roots × four arms × 48 assigned jobs = 768 job outcomes. At most 8,000 physical model requests total, including proposal calls, tests, static-baseline construction and retries; four-hour wall limit; proposed ceilings $25 API and $4 infrastructure, not authorized spending. Set non-overlapping per-lineage quotas whose sum fits the single stage cap before dispatch. S1 reviews competence, actual changes, ledger reconciliation, baseline fairness and effect variability. It does not certify the 20%/2pp claim.

**S2 confirmation:** closed until question-specific prior art, cross-researcher survey/hypothesis acceptance, independent instrument review, successful S0/S1 and a new exact preregistration. No S2 assignments or sample size are set in this version. Predefine the population weights, strongest comparator, horizon, all costs, margins and sample size from development variance before touching the holdout. If feasible power cannot be afforded, report development only.

The proposed confirmatory decision requires all of: upper one-sided 95% interval for the mean-cost ratio below 0.80; lower one-sided 95% interval for `Q_Poietic - Q_baseline` above -0.02; lower one-sided 95% interval for absolute `Q_Poietic` above 0.95. The conjunction is an intersection-union decision; no choosing the best endpoint afterward. A lower observed point cost alone is insufficient. These margins are practical design choices subject to review, not derived from prior measurements.

Estimate paired cost and quality differences at the root level. Use root-cluster resampling for development uncertainty with an explicit warning that four roots are inadequate for a precise scientific interval. For S2 planning, estimate the covariance of cost and quality at the root level and simulate the joint decision's power; start with 80% joint power and allow for variance uncertainty. Do not reuse the template's toy power calculation. Report the full quality-cost tradeoff and failed-assignment bounds, not only the favorable conditional subset.

Stop the research claim if A1/A2 or the central comparator captures the gains, if benefit vanishes when overhead is charged, if quality/freshness fails, or if strong methods already answer the same question. Stop/repair the instrument for leakage, misbilling, false manipulation or broken scoring. A valid null or harm is not a reason to repeat unchanged until it wins. Inconclusive precision remains inconclusive.

## Failure handling and actor boundaries

An episode is an arm/root lineage, with attempt IDs attached to transport or setup recovery. A transport error may receive one identical retry only when side effects are known not to have executed or an idempotency receipt permits replay. A malformed model response is an observed failure, not a silent retry. Configuration mutations use idempotency keys and append-only transaction receipts. No automatic model fallback is permitted unless it is a frozen, visible arm policy.

Preserve assigned, started, terminal, graded and analyzed counts. An operational cap stops dispatch; remaining assigned jobs are recorded as budget/deadline failures. Missing logs or unverifiable execution are not exclusions. A blinded infrastructure-wide invalidation needs an amendment and retains both original evidence and replacement attempts. The primary all-assigned view stays visible alongside any diagnostic sensitivity.

Truth, future source states, hidden shock schedules and S2 tasks live outside actor namespaces. Tool schemas and plain instructions are not the security boundary: actual adapters enforce access and capability removal. No credential value appears in prompts, proposal packets, hashes published as secret substitutes, logs, hub reports or exports. Credentials are local named aliases consumed by the backend adapter.

## Initialization and verification

Bind every run to the immutable public plan, condition-specific TLDR, source commit, resolved model/settings/tariff manifest, scorer/generator hashes, ordered prompt/context hashes, effective tool schemas, memory-empty checks, arm diff, planned assignments, named streams, exact budget reservation, dedicated machine claim and visualization version.

Offline acceptance checks must cover an independently hand-scored job; stale-but-numerically-correct failure; a coherent cache avoiding a duplicate call; low-overlap cases with no available deduplication; denied unloaded tools and truth paths; actual backend substitution; all costs including failed proposals; namespace reset; exogenous tape pairing; missing jobs; duplicate mutation/retry; and paired A3/A5 prefix accounting. A scripted topology transition only tests the instrument and renderer; it cannot demonstrate spontaneous specialization.

The older SEO design guide contains human-simulation awareness thresholds and a requirement to reproduce a literature error-amplification ordering. Those do not validate this engineering mechanism. Use prompt audit and held-out behavioral/semantic checks instead; do not force our outcomes to match another paper. The current shared lifecycle contract and run-review process govern launch.

## Publication and amendments

Use the [visualization mapping](VISUALIZATION.md) and [runbook](RUNBOOK.md). Every attempt gets a prospective pre-run assessment and a post-mortem. Public plan registration and verification precede any S0/S1 model call, including endpoint probes. Fresh exclusive allocation from Dmarz's authorized fleet precedes deployment/queueing; no existing experiment host or default personal account is a fallback. Release idle claims while blocked.

Version 0.1 is the first design. Changes to model identity, deadlines, fixture generation, action grammar, budgets, endpoints or analysis require a dated amendment and new content hashes before dependent data collection. Public design registration alone is not launch authorization or research acceptance.
