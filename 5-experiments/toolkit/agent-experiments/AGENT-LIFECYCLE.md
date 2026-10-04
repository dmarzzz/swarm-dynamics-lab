# Reconstructing an agent: identity, context and lifecycle

Status: **recommended standard and runbook, 2026-10-04 UTC**. This document adds a conceptual contract to the existing [guide](GUIDE.md), [harness notes](HARNESS.md) and [templates](templates/protocol.md). Its companion [research supplement](AGENT-LIFECYCLE-RESEARCH.md) and [source register](research/agent-lifecycle-sources.json) connect the design to research and practitioner evidence. It does not implement a production launcher. The included harness implements only the scripted subset described below.

The practical target is a reconstructable initial state, controlled differences between conditions, and an auditable sequence of changes. “The same agent every time” means the same declared system and starting state within a stated reproducibility boundary. It does not promise the same answer from a hosted model.

## 1. Five identities to keep separate

| Identity | What it fixes | When it changes |
| --- | --- | --- |
| Agent definition | Model settings, role policy, prompts, tools, memory rules, permission rules and adaptation policy | Any intended change to those rules creates a new version and content hash |
| Agent instance | One identity and mutable state within a world; references a definition | Creating a new identity, whether initialized fresh or cloned with recorded inherited state |
| Episode | One world reset, allocation, execution and terminal outcome | A genuinely new world execution, including prespecified fresh repetitions |
| Attempt | A request or execution retry within that episode | A retry; retains episode identity and consumed budget |
| Checkpoint or fork | A saved state and its parent lineage | A new snapshot or branch; inherited history remains shared |

A persona name is a role label. It is not a reproducibility guarantee or an independent training history. Five instances of one model can share systematic errors. A checkpoint resumed twice creates two continuations conditional on one past, not two independent worlds.

Keep `definition_id` in the agent-definition artifact and record the artifact's content hash in its manifest or initialization receipt. This avoids a self-referential hash and requires no unsupported field in the existing definition schema. Keep the instance ID, episode `run_id`, role assignment and lifecycle lineage in the run ledger. The current toy's `agent_id` is local to its run, so the identifying key is `(study_id, run_id, agent_id)`.

## 2. Reuse the existing three specifications

| Existing artifact | Responsibility | Required completion before real use |
| --- | --- | --- |
| [Agent definition](templates/agent-definition.json) | Policy, model, prompts, tools, memory rules, credential aliases | Replace placeholders; hash every referenced public artifact; specify model/output settings and each state policy precisely |
| [Context and access](templates/context-access.json) | Source provenance, eligibility, initial access, retrieval, network and treatment differences | Resolve snapshots and permissions; specify actual context assembly and prove denied access at the environment boundary |
| [Run configuration](templates/run-config.json) | Population, pairing, blocks, seeds, scheduler, budgets, retries, scoring and stopping | Resolve schedule and conditions; freeze interpretation of missing scores; bind the public plan and all effective inputs |

Use these as the source of intended behavior. Record **observed startup facts** in a separate initialization receipt referenced by the run ledger. Do not add unsupported keys to the existing schemas: they reject extra fields and deliberately validate template shape. A production implementation should version an extended schema before consuming the receipt. A short structured sidecar is enough; a new configuration service is unnecessary.

Before experimental implementation, write the plan. Before any Swarm Lab run, publish and verify its readable public plan, register the immutable URL and a condition-specific TLDR covering the question, treatment, comparator, metrics and limitations, and pass the project's `public_plan.py` preflight or equivalent. A local hash or an unfilled protocol template does not satisfy that requirement. If a historical run lacks evidence of prior registration, retain its execution results and record process compliance separately; any later plan is retrospective.

## 3. An initialization receipt that earns trust

The receipt should record values actually loaded by the controller, with stable identifiers for sensitive inputs. These are recommended fields, not claims about existing implementation. Mark unused subsystems as not applicable: a study without a browser, vector store, persistent memory or checkpoints does not need to build those systems to satisfy this contract.

| Area | Minimum facts to record and check |
| --- | --- |
| Registration | Protocol version/hash; verified immutable public URL; condition-specific TLDR; preflight outcome and time |
| Definition | Definition ID/hash; instance ID; role; parent instance/checkpoint, if any; declared treatment overlay |
| Model | Requested identifier and returned identifier when available; available revision/backend metadata; tokenizer/runtime for local models; temperature, top-p, seed semantics, reasoning setting, output format and limits |
| Code and environment | Launcher/policy/tool/scorer hashes; dependency or image identity; relevant runtime version; declared hardware precision boundary for local inference |
| Initial world | Scenario ID, replicate, generator/snapshot identity, named seed-stream identities; public-safe starting-state hash |
| Initial context | Renderer version; ordered message manifest; rendered public prompt hash; delivered observation/document hashes; truncation policy and actual truncation; input size |
| Access | Effective tool names and schemas; effective read/write/network scopes; namespace IDs; protected scorer/truth separation; access-check results |
| Memory | Initial snapshot/version or verified empty state; namespace; retrieval/update/eviction rules; retention or TTL; provenance and access metadata |
| Execution | Scheduler semantics; role/agent order; routing/topology; termination; aggregate budget and reservation policy; retry/fallback settings |
| Allocation | Planned run key; block/order; master-seed reference and named stream derivation; machine-readable treatment diff |

Compare intended configuration to the receipt before admitting a run. A manifest saying “memory empty” is weaker than a check of the actual run namespace. A requested model alias is weaker than an available returned snapshot identifier. Where a provider exposes neither weights nor a stable snapshot, record the limitation; repeated behavior cannot certify hidden identity.

Hash public bytes and public synthetic state. Credential values must never enter receipts, hashes published as substitutes for secrecy, prompts, logs or reports. A local credential adapter consumes only the named secret and returns an allowlisted status. Restricted memory may need a protected snapshot reference and a reviewed public derivative rather than an exported content dump.

## 4. Make context assembly explicit

Eligibility, retrieval and delivery are different events. An agent allowed to read a document may never retrieve it; a retrieved document may be omitted by a context limit. The decision-relevant object is the context actually delivered at that step.

Define one assembly function in the protocol. A sensible default ordering, adjusted to the provider's message hierarchy, is:

1. Fixed system/developer instructions and tool schemas.
2. Frozen role policy and task constraints, with legitimate scenario substitutions.
3. The agent's initial private observation.
4. Retrieved memory/documents in a specified ranking order with source/version labels.
5. Delivered peer messages in the scheduler's specified order.
6. The current action request and output schema.

Freeze delimiters, ordering, timestamps visible to the agent, message roles, renderer, token-counting convention and truncation rule. State whether the private observation is repeated inside the peer-message packet. Otherwise the supposedly neutral renderer can give an agent's own evidence extra weight.

For paired conditions, corresponding agents receive matching baseline state and exogenous observations. Apply only the declared overlay afterward. Compare rendered inputs as well as access manifests. A treatment instruction may change token count legitimately; account for that change and keep the evidence payload unchanged when estimating the instruction's effect. Do not force different roles or private observations to become identical across agents within one world.

Give development, pilot, confirmatory and replication inputs separate namespaces. Keep truth, hidden tests, rubrics and future observations outside the agent's access domain. Prompt instructions alone do not enforce permissions. Verify allowed and denied operations using the actual sandbox/tool adapter before the study.

## 5. Memory is an experimental mechanism

For each memory store, specify the following in the existing memory/context descriptions or a referenced versioned manifest:

| Decision | Operational choice to freeze |
| --- | --- |
| Scope and ownership | Per agent, per swarm, per episode, or persistent cohort; exact reader/writer roles and namespace key |
| Initialization | Empty, specified public prior, or checkpoint; snapshot identity and allowed inherited history |
| Representation | Transcript, structured fact store, vector index or summary; serialization and source IDs |
| Update | Which events cause writes; who may revise/delete; conflict and duplicate handling; whether another model summarizes |
| Retrieval | Query construction, embedding/index versions, filters, ranking, top-k, ties and access checks |
| Expiry | Capacity and eviction policy; TTL and whether it uses wall time or logical episode/round time |
| Provenance | Original source, creation step, author, derivation/summary links, reliability status and permissions |
| Reset and export | What is deleted or recreated; what survives; retained audit record; approved public export |

Do not silently convert a model's inference into an established world fact. Distinguish observations, messages, hypotheses and validated facts. Summaries can introduce or drop information; retain derivation links and record the summarizer specification and cost. Memory inspection should use authorized state artifacts and concise decisions, not demand private reasoning traces.

Separate experiments answer different questions. Resetting all learned memory estimates performance of fresh agents. Carrying memory across episodes estimates a learning system, whose persistent cohort may be the experimental unit. Sharing one mutable store across treatment arms creates interference unless that sharing is explicitly the intervention. Freezing a store before allocation preserves a common prior; copying it after treatment begins imports treatment history.

## 6. A lean startup and execution runbook

Use a single launcher with these gates. A failed gate writes a sanitized controller record and prevents policy/model dispatch.

1. **Resolve and freeze.** Validate schemas and semantics, reject placeholders, verify the public registration, pin references, construct the planned ledger and record a resolved configuration.
2. **Allocate.** Set scenario, repetition, condition, role assignment, time/provider block and named random streams. Randomize or counterbalance roles, message order and source positions when they are nuisance factors; preserve them across corresponding paired conditions.
3. **Create state.** Start fresh run/agent namespaces, world state, memory, filesystem and tool session. Remove inherited browser/session/cache state that can carry experimental information. Separate a provider's immutable prompt cache from writable cross-run content, and record observable cache/latency effects if relevant.
4. **Load policy and context.** Load verified definitions and public inputs, assemble initial context, enforce permissions, apply the declared overlay, and compare the initialization receipt to the specification.
5. **Pass local checks.** Check endpoint/model metadata, remaining budget, allowed/denied access and protected scoring. Account for any provider probe as a separately registered pilot/smoke run with its cost; it is not a free preflight detail.
6. **Admit the run.** Write `run_start` only after successful gates. Execute the declared synchronous barrier or asynchronous delivery schedule; record actual routing, action results, memory changes, budget reservations, retries and human interventions.
7. **Close and reconcile.** Emit one terminal execution status, score independently, preserve missing/failed units, reconcile the planned ledger, and save authorized state/artifact references. Treat execution outcome, scientific validity and process compliance as separate fields.

Named random streams should separate environment, allocation, routing/delays, policy sampling and evaluation. Derive them from stable study/scenario/replicate keys, not from one shared RNG consumed in treatment-dependent order. Record a seed only when its semantics are known. A common seed cannot force equivalent randomness across different prompts or hosted services.

Budget policy belongs in the controller: reserve remaining allowance before a call, reconcile actual usage, include retries and supporting agents, and define missing usage metadata. A system-wide cap and per-agent limits answer different questions. A declared fallback model is part of the treatment; an undeclared fallback is a deviation.

## 7. Reset, resume and fork invariants

| Operation | Invariant | Evidence |
| --- | --- | --- |
| Fresh repetition | Same frozen specification, independently initialized mutable state and specified fresh exogenous randomness | New episode ID; reset checks; namespace/snapshot receipt; planned seed key |
| Paired condition | Same baseline world and corresponding initial observations, only the declared treatment difference | Initial-state/context comparison and machine-readable overlay diff |
| Retry | Same experimental unit; no erased prior failure, cost or side effect | Attempt ID, cause, cumulative budget, idempotency/reconciliation record |
| Resume | Continue the same episode without losing or replaying unrecorded effects | Checkpoint hash, last durable event, pending-call resolution and remaining budget |
| Fork | Preserve parent history; declare the divergence and dependency | Parent checkpoint and event IDs, fork operation, treatment allocation point |
| Cross-episode learning | Carry only the prespecified state, with held-out evaluation protection | Cohort identity, update/checkpoint history and evaluation split |

A checkpoint includes the world, each agent's visible context and memory, RNG states or next counter, routing queues, tool/session state, logical time, budget ledger, and pending actions. If those cannot be reconstructed, the operation is a restart or partial recovery, and its limitations must be reported. Reissuing a tool action after a timeout requires checking whether its effect already occurred.

Do not count replayed traces, retries, forks of one treated past, or repeated scoring of one output as independent replications. Analyze the common parent or scenario cluster where appropriate.

## 8. What to validate before trusting a result

One small acceptance suite should answer the following questions:

- Do all planned scenario × repetition × condition cells appear exactly once as units, with attempts attached correctly?
- Does each required agent have exactly one final decision or an explicit failure? Are IDs, role assignments and terminal counts consistent?
- Does evaluation truth match the frozen world, and does an independent calculation reproduce the endpoint?
- Do observed tool access, source visibility and memory reads/writes match permissions and topology?
- Are paired baseline contexts equal up to the registered difference? Does the reset eliminate prior experimental state?
- Are source/configuration/output hash inventories complete and verified, including the retained evidence being reported?
- Do missing output, duplicate response, timeout, malformed action and resume interruption produce visible failures instead of disappearing units?

Fault tests should assert semantic invariants. A hash chain can prove that a log is unchanged relative to its manifest; it cannot prove that the logged truth, permissions or outcome are correct. Recomputing with the same buggy scorer is weaker than a small independent reference calculation.

## 9. Current implementation boundary

| Capability | Included toy | Production recommendation |
| --- | --- | --- |
| Specification | Validated offline config; template shape checks | Resolved effective definitions/context, semantic checks and public-plan preflight |
| Startup | Keyed Python RNG streams and fresh world dictionaries | Full namespace/sandbox/tool/memory lifecycle and initialization receipt |
| Context | Synthetic source IDs and binary observations | Versioned assembly, actual delivered-content records, controlled truncation |
| Policy/model | Deterministic programmed majority rules; no model service | Requested/observed model metadata, explicit settings and observed variability |
| State | No persistent memory or untrusted tools | Scoped memory with provenance, updates, retrieval and verified reset |
| Ledger | Planned units, chained logical events and outcomes | Attempts, actual timing/routing, usage, checkpoints and interventions |
| Verification | Hash/score/pair checks and local behavior controls | Full saved-artifact reconciliation, semantic fault tests and independent endpoint checks |

The audit of the retained toy evidence found its reported numbers correct. The current validator nevertheless accepts several semantically inconsistent, rehashed copies: wrong evaluator truth, repeated decision agent IDs, wrong terminal counts/status, mismatched planned condition, and wrong source hashes. Those are documented verification gaps; this conceptual runbook does not claim they have been fixed in code. See the [project review](../../researchers/vishesh/notes/pi-review-2026-10-04/review-2026-10-04/methodology-guide-review.json).

For a small study, the necessary artifacts are one protocol, the three completed specifications, an initialization receipt per run, a planned/outcome ledger, and structured events with an independent analysis script. Add distributed storage or a new orchestration framework only when scale or failure recovery requires it.

The methodological basis and source limitations are described in the [literature review](LITERATURE.md), especially the sources on reproducible evaluation, agent reliability, coordination failure, simulation description and judge validity. Recommendations here apply that evidence to this project's lifecycle; no cited paper establishes that this particular unimplemented contract is sufficient by itself.
